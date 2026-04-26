import csv

input_file = "berita madura sebagian.csv"
output_file = "clean berita.csv"

# Buat list untuk menampung data yang sudah rapi
data_bersih = []

with open(input_file, "r", encoding="utf-8") as f:
    for line in f:
        # Bersihkan spasi kosong atau sisa titik koma di akhir kalimat
        line = line.strip().rstrip(';')
        if not line:
            continue
            
        # Pecah baris berdasarkan titik koma
        # (Asumsinya file awal Abang mayoritas pakai ;)
        row = line.split(';')
        data_bersih.append(row)

# Tulis ulang file dengan pemisah koma (,). 
# Python akan otomatis mengapit kalimat dengan tanda kutip ("") jika kalimat itu mengandung koma!
with open(output_file, "w", encoding="utf-8", newline="") as f:
    writer = csv.writer(f, delimiter=",", quoting=csv.QUOTE_MINIMAL)
    writer.writerows(data_bersih)

print("Selesai! File CSV sudah dirapikan dengan aman.")