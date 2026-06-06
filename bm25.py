# ==========================================
# SEARCH ENGINE BERITA MADURA
# BM25 + COSINE SIMILARITY
# ==========================================

from flask import Flask, render_template, request
import pandas as pd
import os
import re

from rank_bm25 import BM25Okapi

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
# BM25
# ==========================================

corpus = df["judul"].apply(
    preprocess
).tolist()

print("Membangun BM25...")

bm25 = BM25Okapi(corpus)

print("BM25 siap!")

# ==========================================
# COSINE SIMILARITY (TF-IDF)
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
# FLASK
# ==========================================

app = Flask(__name__)

# ==========================================
# SEARCH BM25
# ==========================================

def search_bm25(
    query,
    sumber_filter=None,
    top_n=10
):

    if not query.strip():
        return []

    tokenized_query = preprocess(query)

    scores = bm25.get_scores(
        tokenized_query
    )

    result = df.copy()

    result["score"] = scores

    result = result.sort_values(
        by="score",
        ascending=False
    )

    result = result[
        result["score"] > 0
    ]

    if sumber_filter:
        result = result[
            result["sumber"].isin(
                sumber_filter
            )
        ]

    return result[
        ["judul", "link", "sumber", "score"]
    ].head(top_n).to_dict(
        orient="records"
    )

# ==========================================
# SEARCH COSINE
# ==========================================

def search_cosine(
    query,
    sumber_filter=None,
    top_n=10
):

    if not query.strip():
        return []

    query_vec = vectorizer.transform(
        [query]
    )

    scores = cosine_similarity(
        query_vec,
        tfidf_matrix
    ).flatten()

    result = df.copy()

    result["score"] = scores

    result = result.sort_values(
        by="score",
        ascending=False
    )

    result = result[
        result["score"] > 0
    ]

    if sumber_filter:
        result = result[
            result["sumber"].isin(
                sumber_filter
            )
        ]

    return result[
        ["judul", "link", "sumber", "score"]
    ].head(top_n).to_dict(
        orient="records"
    )

# ==========================================
# ROUTE
# ==========================================

@app.route("/", methods=["GET", "POST"])
def index():

    hasil = []

    query = ""

    metode = "bm25"

    sumber_terpilih = []

    if request.method == "POST":

        query = request.form.get(
            "query",
            ""
        )

        metode = request.form.get(
            "metode",
            "bm25"
        )

        sumber_terpilih = request.form.getlist(
            "sumber"
        )

        if metode == "cosine":

            hasil = search_cosine(
                query,
                sumber_filter=sumber_terpilih,
                top_n=10
            )

        else:

            hasil = search_bm25(
                query,
                sumber_filter=sumber_terpilih,
                top_n=10
            )

    return render_template(
        "index.html",
        hasil=hasil,
        query=query,
        metode=metode,
        semua_sumber=semua_sumber,
        sumber_terpilih=sumber_terpilih
    )

# ==========================================
# RUN
# ==========================================

if __name__ == "__main__":
    app.run(debug=True)