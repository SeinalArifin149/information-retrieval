import pandas as pd

# 1. Baca data pertama yang pemisahnya titik koma (;)
df1 = pd.read_csv("dataset_final_madura(2).csv", sep=';')

# 2. Baca data kedua yang pemisahnya koma (,)
# Karena koma adalah bawaan (default) Pandas, tidak perlu tulis sep=',' tidak apa-apa
df2 = pd.read_csv("data kabar madura.csv")

# --- LANGKAH PENGAMANAN (SANGAT PENTING) ---
# Sebelum di-concat, pastikan nama kolom di kedua file SAMA PERSIS 
# (huruf besar/kecil dan spasinya). Kita seragamkan jadi huruf kecil tanpa spasi berlebih:
df1.columns = df1.columns.str.lower().str.strip()
df2.columns = df2.columns.str.lower().str.strip()

# 3. Gabungkan (Concat) kedua data tersebut!
# ignore_index=True fungsinya agar nomor urut baris direset ulang dari 0 sampai akhir
df_gabungan = pd.concat([df1, df2], ignore_index=True)

# 4. Cek hasil gabungannya
print("--- Data Berhasil Digabung ---")
print("Dimensi data baru:", df_gabungan.shape)
print("\nSumber Unik:")
print(df_gabungan['sumber'].astype(str).str.strip().unique())

# 5. Simpan jadi file CSV "Master" baru yang sudah seragam
# Kita jadikan koma (,) sebagai standar pemisah akhirnya
df_gabungan.to_csv("Master_Berita_Madura.csv", index=False)

print("\nMantap! Data sudah bersatu dan tersimpan sebagai 'Master_Berita_Madura.csv'")