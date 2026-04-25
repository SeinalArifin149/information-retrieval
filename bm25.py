# ==========================================
# SEARCH ENGINE BERITA MADURA
# METODE: BM25 MURNI
# ==========================================

from flask import Flask, render_template, request
import pandas as pd
import os
import re

# BM25
from rank_bm25 import BM25Okapi

# ==========================================
# PATH FILE
# ==========================================
base_dir = os.path.dirname(_file_)
csv_path = os.path.join(base_dir, "dataset_final_madura.csv")

# ==========================================
# LOAD DATA
# ==========================================
print("Loading dataset...")
df = pd.read_csv(csv_path, sep=";")

# Jika dataset besar dan berat, aktifkan ini:
# df = df.head(500)

print("Jumlah data:", len(df))

# pastikan tidak null
df["judul"] = df["judul"].fillna("").astype(str)
df["link"] = df["link"].fillna("").astype(str)
df["sumber"] = df["sumber"].fillna("").astype(str)

# ==========================================
# PREPROCESSING
# ==========================================
def preprocess(text):
    text = text.lower()
    text = re.sub(r'[^a-zA-Z0-9\s]', '', text)
    return text.split()

# tokenisasi semua judul
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
app = Flask(_name_)

# ==========================================
# SEARCH FUNCTION
# ==========================================
def search(query, top_n=5):
    if not query.strip():
        return []

    tokenized_query = preprocess(query)

    # hitung score BM25
    scores = bm25.get_scores(tokenized_query)

    # salin dataframe
    result = df.copy()
    result["score"] = scores

    # urutkan score terbesar
    result = result.sort_values(by="score", ascending=False)

    # ambil score > 0
    result = result[result["score"] > 0]

    return result[["judul", "link", "sumber", "score"]].head(top_n).to_dict(orient="records")

# ==========================================
# ROUTE
# ==========================================
@app.route("/", methods=["GET", "POST"])
def index():
    hasil = []
    query = ""

    if request.method == "POST":
        query = request.form.get("query", "")
        hasil = search(query)

    return render_template("index.html", hasil=hasil, query=query)

# ==========================================
# RUN
# ==========================================
if _name_ == "_main_":
    app.run(debug=False, use_reloader=False)