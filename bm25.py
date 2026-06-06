# ==========================================
# SEARCH ENGINE BERITA MADURA
# BM25 + BM25 PLUS + COSINE SIMILARITY
# ==========================================

from flask import Flask, render_template, request
import pandas as pd
import os
import re

# Import BM25Okapi (standar) dan BM25Plus
from rank_bm25 import BM25Okapi, BM25Plus

from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

# ==========================================
# PATH FILE
# ==========================================

base_dir = os.path.dirname(__file__)
csv_path = os.path.join(
    base_dir,
    "data",
    "Master_Berita_Madura.csv"
)

# ==========================================
# LOAD DATA
# ==========================================

print("Loading dataset...")

df = pd.read_csv(csv_path)

print("Jumlah data :", len(df))

# ==========================================
# BERSIHKAN DATA
# ==========================================

df["judul"] = df["judul"].fillna("").astype(str)
df["link"] = df["link"].fillna("").astype(str)
df["sumber"] = df["sumber"].fillna("").astype(str)

semua_sumber = sorted(
    df["sumber"].unique()
)

# ==========================================
# PREPROCESSING
# ==========================================

def preprocess(text):

    text = text.lower()

    text = re.sub(
        r'[^a-zA-Z0-9\s]',
        '',
        text
    )

    return text.split()

# ==========================================
# CORPUS SETUP
# ==========================================

corpus = df["judul"].apply(
    preprocess
).tolist()

# ==========================================
# INSTANSIASI BM25 & BM25 PLUS
# ==========================================

print("Membangun BM25 Standar...")
bm25 = BM25Okapi(corpus)

print("Membangun BM25 Plus...")
bm25_plus = BM25Plus(corpus) # Menggunakan parameter default (delta=1.0)

print("Sistem BM25 & BM25 Plus siap!")

# ==========================================
# COSINE SIMILARITY SETUP (TF-IDF)
# ==========================================

documents = df["judul"].tolist()

vectorizer = TfidfVectorizer(
    lowercase=True
)

tfidf_matrix = vectorizer.fit_transform(
    documents
)

print("TF-IDF siap!")

# ==========================================
# FLASK APPLICATION
# ==========================================

app = Flask(__name__)

# ==========================================
# SEARCH FUNCTION: BM25 STANDAR
# ==========================================

def search_bm25(query, sumber_filter=None, top_n=10):

    if not query.strip():
        return []

    tokenized_query = preprocess(query)
    scores = bm25.get_scores(tokenized_query)

    result = df.copy()
    result["score"] = scores
    result = result.sort_values(by="score", ascending=False)
    result = result[result["score"] > 0]

    if sumber_filter:
        result = result[result["sumber"].isin(sumber_filter)]

    return result[["judul", "link", "sumber", "score"]].head(top_n).to_dict(orient="records")

# ==========================================
# SEARCH FUNCTION: BM25 PLUS
# ==========================================

def search_bm25_plus(query, sumber_filter=None, top_n=10):

    if not query.strip():
        return []

    tokenized_query = preprocess(query)
    scores = bm25_plus.get_scores(tokenized_query) # Memanggil objek bm25_plus

    result = df.copy()
    result["score"] = scores
    result = result.sort_values(by="score", ascending=False)
    result = result[result["score"] > 0]

    if sumber_filter:
        result = result[result["sumber"].isin(sumber_filter)]

    return result[["judul", "link", "sumber", "score"]].head(top_n).to_dict(orient="records")

# ==========================================
# SEARCH FUNCTION: COSINE SIMILARITY
# ==========================================

def search_cosine(query, sumber_filter=None, top_n=10):

    if not query.strip():
        return []

    query_vec = vectorizer.transform([query])
    scores = cosine_similarity(query_vec, tfidf_matrix).flatten()

    result = df.copy()
    result["score"] = scores
    result = result.sort_values(by="score", ascending=False)
    result = result[result["score"] > 0]

    if sumber_filter:
        result = result[result["sumber"].isin(sumber_filter)]

    return result[["judul", "link", "sumber", "score"]].head(top_n).to_dict(orient="records")

# ==========================================
# ROUTE UTAMA
# ==========================================

@app.route("/", methods=["GET", "POST"])
def index():

    hasil_bm25 = []
    hasil_bm25_plus = []
    hasil_cosine = []
    query = ""
    limit = 10
    sumber_terpilih = semua_sumber.copy()

    if request.method == "POST":

        query = request.form.get("query", "")
        sumber_terpilih = request.form.getlist("sumber")
        limit = int(request.form.get("limit", 10))

        top_n_val = len(df) if limit == 0 else limit

        if query.strip():
            
            # Jalankan ketiga algoritma pencarian sekaligus
            hasil_bm25 = search_bm25(
                query,
                sumber_filter=sumber_terpilih,
                top_n=top_n_val
            )

            hasil_bm25_plus = search_bm25_plus(
                query,
                sumber_filter=sumber_terpilih,
                top_n=top_n_val
            )

            hasil_cosine = search_cosine(
                query,
                sumber_filter=sumber_terpilih,
                top_n=top_n_val
            )

    return render_template(
        "index.html",
        hasil_bm25=hasil_bm25,
        hasil_bm25_plus=hasil_bm25_plus,
        hasil_cosine=hasil_cosine,
        query=query,
        limit=limit,
        semua_sumber=semua_sumber,
        sumber_terpilih=sumber_terpilih
    )

if __name__ == "__main__":
    app.run(debug=True)