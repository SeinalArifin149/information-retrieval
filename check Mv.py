import pandas as pd

df = pd.read_csv("itb_news.csv")

# =========================
# CEK MISSING VALUE
# =========================
print("Jumlah Missing Value per kolom:")
print(df.isnull().sum())


# Cek string kosong
print("\nCek string kosong:")
print((df == "").sum())

# =========================
# CEK DUPLIKAT
# =========================
print("\nJumlah data duplikat (semua kolom):")
print(df.duplicated().sum())

print("\nDuplikat berdasarkan title:")
print(df.duplicated(subset=["title"]).sum())

print("\nDuplikat berdasarkan content:")
print(df.duplicated(subset=["content"]).sum())

print(df.shape)