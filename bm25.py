# ==========================================
# SEARCH ENGINE BERITA MADURA (BM25)
# ==========================================

from flask import Flask, render_template, request
import pandas as pd
import os
import re
from rank_bm25 import BM25Okapi

# ==========================================
# PATH FILE
# ==========================================
base_dir = os.path.dirname(__file__)
csv_path = os.path.join(base_dir, "data", "Master_Berita_Madura.csv")

# ==========================================
# LOAD DATA
# ==========================================
print("Loading dataset...")
df = pd.read_csv(csv_path)  # pakai koma (default)

print("Jumlah data:", len(df))

# bersihin data
df["judul"] = df["judul"].fillna("").astype(str)
df["link"] = df["link"].fillna("").astype(str)
df["sumber"] = df["sumber"].fillna("").astype(str)

# ambil semua sumber unik
semua_sumber = sorted(df["sumber"].unique())

# ==========================================
# PREPROCESSING
# ==========================================
def preprocess(text):
    text = text.lower()
    text = re.sub(r'[^a-zA-Z0-9\s]', '', text)
    return text.split()

corpus = df["judul"].apply(preprocess).tolist()

# ==========================================
# BUILD BM25
# ==========================================
print("Membangun BM25...")
bm25 = BM25Okapi(corpus)
print("BM25 siap!")

# ==========================================
# FLASK
# ==========================================
app = Flask(__name__)

# ==========================================
# SEARCH FUNCTION
# ==========================================
def search(query, sumber_filter=None, top_n=5):
    if not query.strip():
        return []

    tokenized_query = preprocess(query)
    scores = bm25.get_scores(tokenized_query)

    result = df.copy()
    result["score"] = scores

    result = result.sort_values(by="score", ascending=False)
    result = result[result["score"] > 0]

    # filter sumber
    if sumber_filter:
        result = result[result["sumber"].isin(sumber_filter)]

    return result[["judul", "link", "sumber", "score"]].head(top_n).to_dict(orient="records")

# ==========================================
# ROUTE
# ==========================================
@app.route("/", methods=["GET", "POST"])
def index():
    hasil = []
    query = ""
    sumber_terpilih = []

    if request.method == "POST":
        query = request.form.get("query", "")
        sumber_terpilih = request.form.getlist("sumber")

        hasil = search(query, sumber_filter=sumber_terpilih)

    return render_template(
        "index.html",
        hasil=hasil,
        query=query,
        semua_sumber=semua_sumber,
        sumber_terpilih=sumber_terpilih
    )

# ==========================================
# RUN
# ==========================================
if __name__ == "__main__":
    app.run(debug=True)