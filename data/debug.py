import pandas as pd

# df = pd.read_csv("Full Data berita madura.csv")
# df = pd.read_csv("clean berita.csv")
df = pd.read_csv("Master_Berita_Madura.csv")
# df = pd.read_csv("data kabar madura.csv")

# cek sumber unik
print("Sumber unik:")
print(df["sumber"].unique())

# cek dimensi
print("\nDimensi data (baris, kolom):")
print(df.shape)

# opsional: tampilkan detail
print("\nJumlah baris:", df.shape[0])
print("Jumlah kolom:", df.shape[1])