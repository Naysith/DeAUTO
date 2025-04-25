import sqlite3
from datetime import datetime

#konek ke databes
conn = sqlite3.connect('databaseDeAuto.db')

#cursor
c = conn.cursor()

#buat foreign key
c.execute("PRAGMA foreign_keys = ON")

#table user
c.execute("""
CREATE TABLE IF NOT EXISTS user (
    id_user INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT UNIQUE NOT NULL,
    password TEXT NOT NULL,
    role TEXT CHECK(role IN ('admin', 'staff')) NOT NULL
)
""")

#table jenis
c.execute("""
CREATE TABLE IF NOT EXISTS jenis_kendaraan (
    id_jenis INTEGER PRIMARY KEY AUTOINCREMENT,
    nama_jenis TEXT,
    tahun INTEGER,
    warna_default TEXT,
    jumlah_kursi INTEGER,
    harga_sewa INTEGER 
)
""")

#table unit
c.execute("""
CREATE TABLE IF NOT EXISTS unit_kendaraan (
    id_unit INTEGER PRIMARY KEY AUTOINCREMENT,
    id_jenis INTEGER,
    plat_nomor TEXT,
    status TEXT CHECK(status IN ('tersedia', 'disewa', 'maintenance')) DEFAULT 'tersedia',
    tanggal_masuk TEXT,
    FOREIGN KEY (id_jenis) REFERENCES jenis_kendaraan(id_jenis)
)
""")

#table stok
c.execute("""
CREATE TABLE IF NOT EXISTS stok_kendaraan (
    id_stok INTEGER PRIMARY KEY AUTOINCREMENT,
    id_jenis INTEGER,
    tanggal_input TEXT,
    jumlah_unit INTEGER,
    jumlah_unit_keluar INTEGER,
    jumlah_unit_tersisa INTEGER,
    FOREIGN KEY (id_jenis) REFERENCES jenis_kendaraan(id_jenis)
)
""")

#table transaksi
c.execute("""
CREATE TABLE IF NOT EXISTS transaksi (
    id_transaksi INTEGER PRIMARY KEY AUTOINCREMENT,
    id_unit INTEGER,
    nama_penyewa TEXT,
    alamat_penyewa TEXT,
    jumlah_unit INTEGER,
    tanggal_sewa TEXT,
    tanggal_rencana_kembali TEXT,
    tanggal_kembali TEXT,
    deposit INTEGER,
    denda INTEGER,
    total_bayar_akhir INTEGER,
    status_transaksi TEXT CHECK(status_transaksi IN ('disewa', 'dikembalikan')) DEFAULT 'disewa',
    FOREIGN KEY (id_unit) REFERENCES unit_kendaraan(id_unit)
)
""")

conn.commit()
#////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////
#function login user
def login():
    username = input("Username: ").strip()
    password = input("Password: ").strip()

    c.execute("SELECT * FROM user WHERE username = ? AND password = ?", (username, password))
    user = c.fetchone()

    if user:
        print(f"✅ Selamat datang, {username}!")
        return True
    else:
        print("❌ Login gagal. Cek username/password.")
        return False

#////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////
#function CRUD table user

#create = tambah_user()
def tambah_user():
    username = input("Masukkan username: ").lower()
    # while loop biar user input pass min 8 char
    while True:
        password = input("Masukkan password (min 8 karakter): ")
        if len(password) >= 8:
            break
        print("❌ Password terlalu pendek, coba lagi.")
    role = input("Masukkan role (admin/staff): ").lower()
    # check kalo yang diketik rolenya bener
    if role not in ['admin', 'staff']:
        print("❌ Role tidak valid! Gunakan 'admin' atau 'staff'.")
        return
    # input data ke SQL kalo return = error ga diinput
    try:
        c.execute("""
            INSERT INTO user (username, password, role)
            VALUES (?, ?, ?)
        """, (username, password, role))
        conn.commit()
        print("✅ User berhasil ditambahkan!")
    except sqlite3.IntegrityError as e:
        print("❌ Gagal menambahkan user:", e)

#read = tampilkan_user()
def tampilkan_user():
    c.execute("SELECT id_user, username, role FROM user")
    data = c.fetchall()
    #check kalau data kosong
    if not data:
        print(" Tidak ada user yang terdaftar.")
        return
    #buat daftar ga termasuk password, biar aman lah cok
    print("\n Daftar User:")
    print("-" * 30)
    for row in data:
        print(f"ID: {row[0]} | Username: {row[1]} | Role: {row[2]}")
    print("-" * 30)

#update = update_user()
def update_user():
    tampilkan_user()
    user_id = input("Masukkan ID user yang ingin diubah: ")
    #check user nya ada di databes ga
    c.execute("SELECT * FROM user WHERE id_user = ?", (user_id,))
    user = c.fetchone()

    if user is None:
        print("❌ User tidak ditemukan!")
        return
    
    print("\nPilih data yang ingin diubah:")
    print("1. Ganti password")
    print("2. Ganti role (admin/staff)")
    pilihan = input("Masukkan pilihan (1/2): ")
    #ini buat ganti pw
    if pilihan == "1":
        # loop check lagi kalo pass baru min 8 char
        while True:
            new_password = input("Masukkan password baru (min 8 karakter): ")
            if len(new_password) < 8:
                print("❌ Password terlalu pendek, coba lagi.")
            else:
                break
        c.execute("UPDATE user SET password = ? WHERE id_user = ?", (new_password, user_id))
        conn.commit()
        print("✅ Password berhasil diubah!")
    #ini buat ganti role
    elif pilihan == "2":
        new_role = input("Masukkan role baru (admin/staff): ").lower()
        # check user input salah satu bukan selain admin/staff
        if new_role not in ['admin', 'staff']:
            print("❌ Role tidak valid.")
            return
        c.execute("UPDATE user SET role = ? WHERE id_user = ?", (new_role, user_id))
        conn.commit()
        print("✅ Role berhasil diubah!")
    #kalo user salah pilih
    else:
        print("❌ Pilihan tidak valid.")

#delete = hapus_user()
def hapus_user():
    tampilkan_user()
    user_id = input("Masukkan ID user yang ingin dihapus: ")

    #check user nya ada di databes ga
    c.execute("SELECT * FROM user WHERE id_user = ?", (user_id,))
    user = c.fetchone()

    if user is None:
        print("❌ User tidak ditemukan!")
    else:
        # konfirmasi delet
        confirm = input(f"Apakah Anda yakin ingin menghapus user {user[1]} (username)? (y/n): ").lower()
        if confirm == 'y':
            c.execute("DELETE FROM user WHERE id_user = ?", (user_id,))
            conn.commit()
            print(f"✅ User {user[1]} berhasil dihapus!")
        else:
            print("❌ Penghapusan dibatalkan.")

#////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////
#function CRUD table jenis

#create = tambah_jenis_kendaraan()
def tambah_jenis_kendaraan():
    nama = input("Masukkan nama jenis kendaraan (brand)(tipe): ").strip()
    tahun = int(input("Masukkan tahun produksi: "))
    warna = input("Masukkan warna mobil: ").strip()
    kursi = int(input("Masukkan jumlah kursi: "))
    harga = int(input("Masukkan harga sewa per hari: "))

    try:
        c.execute("""
            INSERT INTO jenis_kendaraan (nama_jenis, tahun, warna_default, jumlah_kursi, harga_sewa)
            VALUES (?, ?, ?, ?, ?)
        """, (nama, tahun, warna, kursi, harga))
        conn.commit()
        print("✅ Jenis kendaraan berhasil ditambahkan!")
    except Exception as e:
        print("❌ Gagal menambahkan jenis kendaraan:", e)

#read = tampilkan_jenis_kendaraan()
def tampilkan_jenis_kendaraan():
    c.execute("SELECT * FROM jenis_kendaraan")
    data = c.fetchall()

    if not data:
        print("Belum ada jenis kendaraan terdaftar.")
        return

    print("\nDaftar Jenis Kendaraan:")
    print("-" * 50)
    for row in data:
        print(f"ID: {row[0]} | Nama: {row[1]} | Tahun: {row[2]} | Warna: {row[3]} | Kursi: {row[4]} | Harga: Rp{row[5]:,}")
    print("-" * 50)

#update = update_jenis_kendaraan()
def update_jenis_kendaraan():
    tampilkan_jenis_kendaraan()
    id_jenis = input("Masukkan ID jenis kendaraan yang ingin diubah: ")

    c.execute("SELECT * FROM jenis_kendaraan WHERE id_jenis = ?", (id_jenis,))
    jenis = c.fetchone()

    if not jenis:
        print("❌ ID tidak ditemukan.")
        return

    nama = input(f"Nama baru [{jenis[1]}]: ") or jenis[1]
    tahun = input(f"Tahun baru [{jenis[2]}]: ") or jenis[2]
    warna = input(f"Warna baru [{jenis[3]}]: ") or jenis[3]
    kursi = input(f"Jumlah kursi baru [{jenis[4]}]: ") or jenis[4]
    harga = input(f"Harga sewa baru [{jenis[5]}]: ") or jenis[5]

    c.execute("""
        UPDATE jenis_kendaraan
        SET nama_jenis=?, tahun=?, warna_default=?, jumlah_kursi=?, harga_sewa=?
        WHERE id_jenis=?
    """, (nama, tahun, warna, kursi, harga, id_jenis))
    conn.commit()
    print("✅ Data jenis kendaraan berhasil diperbarui.")

#delete = hapus_jenis_kendaraan()
def hapus_jenis_kendaraan():
    tampilkan_jenis_kendaraan()
    id_jenis = input("Masukkan ID jenis kendaraan yang ingin dihapus: ")

    c.execute("SELECT * FROM jenis_kendaraan WHERE id_jenis = ?", (id_jenis,))
    jenis = c.fetchone()

    if not jenis:
        print("❌ ID tidak ditemukan.")
        return

    confirm = input(f"Yakin ingin menghapus '{jenis[1]}'? (y/n): ").lower()
    if confirm == 'y':
        c.execute("DELETE FROM jenis_kendaraan WHERE id_jenis = ?", (id_jenis,))
        conn.commit()
        print("✅ Jenis kendaraan berhasil dihapus.")
    else:
        print("❌ Penghapusan dibatalkan.")

#////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////
#function CRUD table stok

#create = tambah_stok_kendaraan()
def tambah_stok_kendaraan():
    tampilkan_jenis_kendaraan()
    id_jenis = input("Masukkan ID jenis kendaraan: ")
    jumlah_unit = int(input("Jumlah unit masuk: "))
    jumlah_keluar = int(input("Jumlah unit keluar (jika ada): "))

    # Hitung jumlah tersisa otomatis
    jumlah_tersisa = jumlah_unit - jumlah_keluar
    tanggal_input = datetime.now().strftime("%Y-%m-%d")

    try:
        c.execute("""
            INSERT INTO stok_kendaraan (id_jenis, tanggal_input, jumlah_unit, jumlah_unit_keluar, jumlah_unit_tersisa)
            VALUES (?, ?, ?, ?, ?)
        """, (id_jenis, tanggal_input, jumlah_unit, jumlah_keluar, jumlah_tersisa))
        conn.commit()
        print("✅ Data stok berhasil ditambahkan.")
    except Exception as e:
        print("❌ Gagal menambahkan stok:", e)

#read = tampilkan_stok_kendaraan()
def tampilkan_stok_kendaraan():
    c.execute("""
        SELECT stok.id_stok, jenis.nama_jenis, stok.tanggal_input, stok.jumlah_unit,
               stok.jumlah_unit_keluar, stok.jumlah_unit_tersisa
        FROM stok_kendaraan stok
        JOIN jenis_kendaraan jenis ON stok.id_jenis = jenis.id_jenis
    """)
    data = c.fetchall()

    if not data:
        print("📭 Tidak ada data stok kendaraan.")
        return

    print("\n📋 Daftar Stok Kendaraan:")
    print("-" * 60)
    for row in data:
        print(f"ID: {row[0]} | Jenis: {row[1]} | Tanggal: {row[2]}")
        print(f"  Masuk: {row[3]} | Keluar: {row[4]} | Tersisa: {row[5]}")
    print("-" * 60)

#update = update_stok_kendaraan()
def update_stok_kendaraan():
    tampilkan_stok_kendaraan()
    id_stok = input("Masukkan ID stok yang ingin diupdate: ")

    c.execute("SELECT * FROM stok_kendaraan WHERE id_stok = ?", (id_stok,))
    stok = c.fetchone()

    if not stok:
        print("❌ ID stok tidak ditemukan.")
        return

    jumlah_unit = input(f"Jumlah unit masuk baru [{stok[3]}]: ") or stok[3]
    jumlah_keluar = input(f"Jumlah unit keluar baru [{stok[4]}]: ") or stok[4]
    jumlah_tersisa = int(jumlah_unit) - int(jumlah_keluar)

    c.execute("""
        UPDATE stok_kendaraan
        SET jumlah_unit = ?, jumlah_unit_keluar = ?, jumlah_unit_tersisa = ?
        WHERE id_stok = ?
    """, (jumlah_unit, jumlah_keluar, jumlah_tersisa, id_stok))
    conn.commit()
    print("✅ Data stok berhasil diperbarui.")

#delete = hapus_stok_kendaraan()
def hapus_stok_kendaraan():
    tampilkan_stok_kendaraan()
    id_stok = input("Masukkan ID stok yang ingin dihapus: ")

    c.execute("SELECT * FROM stok_kendaraan WHERE id_stok = ?", (id_stok,))
    stok = c.fetchone()

    if not stok:
        print("❌ Data stok tidak ditemukan.")
        return

    confirm = input("Yakin ingin menghapus data stok ini? (y/n): ").lower()
    if confirm == 'y':
        c.execute("DELETE FROM stok_kendaraan WHERE id_stok = ?", (id_stok,))
        conn.commit()
        print("✅ Data stok berhasil dihapus.")
    else:
        print("❌ Penghapusan dibatalkan.")

#////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////