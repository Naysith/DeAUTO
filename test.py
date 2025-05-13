import sqlite3

conn = sqlite3.connect('databaseMTR.db')

c = conn.cursor()

#buat foreign key

c.execute("PRAGMA foreign_keys = ON")

#buat Table SQL kaalaau belum ada

c.execute("""
CREATE TABLE IF NOT EXISTS motor (
    id_Mtr INTEGER PRIMARY KEY AUTOINCREMENT,
    jenis_Mtr TEXT,
    tahun_Mtr INTEGER,
    plat_Mtr TEXT,
    warna_Mtr TEXT,
    CC INTEGER,
    harga INTEGER,
    deposit INTEGER,
    status INTEGER DEFAULT 1 
)
""")

#status 1 = true / 0 = false

conn.commit()

# function buat masukin motor sapa tau butuh

def insert_motor(dMTR):
    with conn:
        c.execute("INSERT INTO motor VALUES (:jenis_Mtr, :tahun_Mtr, :plat_Mtr :warna_Mtr :CC :harga : deposit)"
                  , {'jenis_Mtr': dMTR.jenis_Mtr,'tahun_Mtr': dMTR.tahun_Mtr,'plat_Mtr': dMTR.plat_Mtr,'warna_Mtr': dMTR.warna_Mtr,'CC': dMTR.CC,'harga': dMTR.harga,'deposit': dMTR.deposit})
    
#looping tambah motor sementara

lanjut = "y"

while lanjut == "y" :
    jenis = input("Masukkan jenis motor      : ").strip()
    tahun = int(input("Masukkan tahun(4 digit): "))
    plat = input("Masukkan plat nomor contoh:(B-1234-ABC): ").strip()
    warna = input("Masukkan warna motor      : ").strip()
    cc = int(input("Masukkan kapasitas CC     : "))
    harga = int(input("Masukkan harga sewa       : "))
    deposit = int(input("Masukkan nilai deposit    : "))
    status = input("Apakah motor tersedia? (1 = ya, 0 = tidak) [default: 1]: ").strip()

    print(jenis, tahun, plat, warna, cc, harga, deposit, status)

    cek = input("apakah sudah benar? (y/n)").lower()
    if cek == "y":
        try:
            c.execute("""
                INSERT INTO motor (jenis_Mtr, tahun_Mtr, plat_Mtr, warna_Mtr, CC, harga, deposit, status)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?)
            """, (jenis, tahun, plat, warna, cc, harga, deposit, status))
            conn.commit()
            print("✅ Data motor berhasil ditambahkan!")
        except Exception as e:
            print(f"❌ Gagal menambahkan data: {e}")

    lanjut = input("Tambaahkan motor lagi? y/n :")

conn.commit()

conn.close()