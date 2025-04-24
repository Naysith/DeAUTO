import sqlite3

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