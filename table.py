import sqlite3
from datetime import datetime, timedelta
from print_baru import cetak_struk_baru

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

    #Check kalo ada data yang sama
    try:
        c.execute("""
            SELECT COUNT(*) FROM jenis_kendaraan 
            WHERE nama_jenis = ? AND tahun = ? AND warna_default = ? AND jumlah_kursi = ? AND harga_sewa = ?
        """, (nama, tahun, warna, kursi, harga))
        result = c.fetchone()

        if result[0] > 0:
            print("❌ Gagal menambahkan jenis kendaraan: Data yang dimasukkan sudah ada.")
        else:
            # Insert the new vehicle data if it's not a duplicate
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
#function CRUD table unit

#create = tambah_unit_kendaraan()
def tambah_unit_kendaraan():
    tampilkan_jenis_kendaraan()
    id_jenis = input("Masukkan ID jenis kendaraan: ").strip()
    plat_nomor = input("Masukkan plat nomor: ").upper().strip()
    tanggal_masuk = datetime.now().strftime("%Y-%m-%d")
    
    try:
        c.execute("""
            INSERT INTO unit_kendaraan (id_jenis, plat_nomor, tanggal_masuk)
            VALUES (?, ?, ?)
        """, (id_jenis, plat_nomor, tanggal_masuk))
        conn.commit()
        print("✅ Unit kendaraan berhasil ditambahkan!")
    except sqlite3.IntegrityError:
        print("❌ Plat nomor sudah digunakan!")
    except Exception as e:
        print("❌ Gagal menambahkan unit:", e)

#read = tampilkan_unit_kendaraan()
def tampilkan_unit_kendaraan():
    c.execute("""
        SELECT unit.id_unit, jenis.nama_jenis, unit.plat_nomor, unit.status, unit.tanggal_masuk
        FROM unit_kendaraan unit
        JOIN jenis_kendaraan jenis ON unit.id_jenis = jenis.id_jenis
    """)
    data = c.fetchall()

    if not data:
        print(" Belum ada unit kendaraan.")
        return

    print("\n Daftar Unit Kendaraan:")
    print("-" * 60)
    for row in data:
        print(f"ID: {row[0]} | Jenis: {row[1]} | Plat: {row[2]} | Status: {row[3]} | Masuk: {row[4]}")
    print("-" * 60)

#update = update_unit_kendaraan()
def update_unit_kendaraan():
    tampilkan_unit_kendaraan()
    id_unit = input("Masukkan ID unit yang ingin diupdate: ")

    c.execute("SELECT * FROM unit_kendaraan WHERE id_unit = ?", (id_unit,))
    unit = c.fetchone()

    if not unit:
        print("❌ Unit tidak ditemukan.")
        return

    plat_baru = input(f"Plat baru [{unit[2]}]: ").upper() or unit[2]
    status_baru = input(f"Status baru (tersedia/disewa/maintenance) [{unit[3]}]: ").lower() or unit[3]

    if status_baru not in ['tersedia', 'disewa', 'maintenance']:
        print("❌ Status tidak valid.")
        return

    c.execute("""
        UPDATE unit_kendaraan
        SET plat_nomor = ?, status = ?
        WHERE id_unit = ?
    """, (plat_baru, status_baru, id_unit))
    conn.commit()
    print("✅ Data unit kendaraan berhasil diperbarui.")

#delete = hapus_stok_kendaraan()
def hapus_unit_kendaraan():
    tampilkan_unit_kendaraan()
    id_unit = input("Masukkan ID unit yang ingin dihapus: ")

    c.execute("SELECT * FROM unit_kendaraan WHERE id_unit = ?", (id_unit,))
    unit = c.fetchone()

    if not unit:
        print("❌ Unit tidak ditemukan.")
        return

    confirm = input(f"Yakin ingin menghapus unit dengan plat {unit[2]}? (y/n): ").lower()
    if confirm == 'y':
        c.execute("DELETE FROM unit_kendaraan WHERE id_unit = ?", (id_unit,))
        conn.commit()
        print("✅ Unit kendaraan berhasil dihapus.")
    else:
        print("❌ Penghapusan dibatalkan.")

#////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////
#function CRUD table transaksi

#create = tambah_transaksi()
def tambah_transaksi():
    print("\n🆕 Tambah Transaksi Baru")

    c.execute("""
        SELECT unit.id_unit, unit.plat_nomor, jenis.nama_jenis, jenis.harga_sewa
        FROM unit_kendaraan unit
        JOIN jenis_kendaraan jenis ON unit.id_jenis = jenis.id_jenis
        WHERE unit.status = 'tersedia'
    """)
    units = c.fetchall()

    if not units:
        print("❌ Tidak ada unit kendaraan tersedia.")
        return

    print("\n📋 Unit Kendaraan Tersedia:")
    for unit in units:
        print(f"ID: {unit[0]} | Plat: {unit[1]} | Nama Jenis: {unit[2]} | Harga Sewa: Rp{unit[3]:,}")

    id_unit = input("Masukkan ID unit yang disewa: ")

    # Cari harga sewa dan nama mobil dari ID yang dipilih
    selected_unit = None
    for unit in units:
        if str(unit[0]) == id_unit:
            selected_unit = unit
            break

    if not selected_unit:
        print("❌ ID unit tidak valid.")
        return

    nama = input("Masukkan nama penyewa: ").strip()
    alamat = input("Masukkan alamat penyewa: ").strip()
    jumlah_unit = 1  # Biasanya 1 mobil per transaksi

    # Ambil tanggal sekarang
    tanggal_sewa = datetime.now()
    tanggal_sewa_str = tanggal_sewa.strftime("%Y-%m-%d %H:%M:%S")

    # User input berapa hari sewa
    durasi_sewa_hari = int(input("Masukkan durasi sewa (berapa hari): "))
    tanggal_rencana_kembali = tanggal_sewa + timedelta(days=durasi_sewa_hari)
    tanggal_rencana_kembali_str = tanggal_rencana_kembali.strftime("%Y-%m-%d 23:59:59")

    # Deposit = harga sewa
    harga_sewa = selected_unit[3]
    deposit = harga_sewa

    try:
        c.execute("""
            INSERT INTO transaksi (
                id_unit, nama_penyewa, alamat_penyewa, jumlah_unit,
                tanggal_sewa, tanggal_rencana_kembali,
                deposit, status_transaksi
            )
            VALUES (?, ?, ?, ?, ?, ?, ?, 'disewa')
        """, (id_unit, nama, alamat, jumlah_unit, tanggal_sewa_str, tanggal_rencana_kembali_str, deposit))

        c.execute("UPDATE unit_kendaraan SET status = 'disewa' WHERE id_unit = ?", (id_unit,))

        conn.commit()
        print(f"✅ Transaksi berhasil dibuat! Sewa selama {durasi_sewa_hari} hari. Deposit: Rp{deposit:,}")
    except Exception as e:
        print("❌ Gagal membuat transaksi:", e)

#read = tampilkan_unit_kendaraan()
def tampilkan_transaksi():
    c.execute("""
        SELECT transaksi.id_transaksi, unit.plat_nomor, transaksi.nama_penyewa, transaksi.tanggal_sewa, transaksi.tanggal_rencana_kembali, transaksi.status_transaksi
        FROM transaksi
        JOIN unit_kendaraan unit ON transaksi.id_unit = unit.id_unit
    """)
    data = c.fetchall()

    if not data:
        print("📭 Tidak ada transaksi tercatat.")
        return

    print("\n📋 Daftar Transaksi:")
    print("-" * 70)
    for row in data:
        print(f"ID: {row[0]} | Plat: {row[1]} | Penyewa: {row[2]}")
        print(f"  Tgl Sewa: {row[3]} | Tgl Kembali Rencana: {row[4]} | Status: {row[5]}")
    print("-" * 70)

#update = proses_pengembalian()
def proses_pengembalian():
    tampilkan_transaksi()
    id_transaksi = input("Masukkan ID transaksi yang akan diproses pengembalian: ")

    # Get transaction info with plat & id_jenis
    c.execute("""
        SELECT transaksi.*, unit.plat_nomor, unit.id_jenis
        FROM transaksi
        JOIN unit_kendaraan unit ON transaksi.id_unit = unit.id_unit
        WHERE transaksi.id_transaksi = ?
    """, (id_transaksi,))
    transaksi = c.fetchone()

    if not transaksi:
        print("❌ Transaksi tidak ditemukan.")
        return

    if transaksi[11] == 'dikembalikan':
        print("⚠️ Transaksi ini sudah dikembalikan sebelumnya.")
        return

    tanggal_rencana_kembali = datetime.strptime(transaksi[6], "%Y-%m-%d %H:%M:%S")
    tanggal_sewa = datetime.strptime(transaksi[5], "%Y-%m-%d %H:%M:%S")
    tanggal_kembali = datetime.now()

    # Hitung keterlambatan
    terlambat = (tanggal_kembali.date() - tanggal_rencana_kembali.date()).days
    denda = max(terlambat, 0) * 50000

    # Ambil harga sewa dari jenis_kendaraan
    id_jenis = transaksi[13]
    c.execute("SELECT harga_sewa FROM jenis_kendaraan WHERE id_jenis = ?", (id_jenis,))
    harga_row = c.fetchone()
    if not harga_row:
        print("❌ Harga sewa tidak ditemukan!")
        return

    harga_sewa_per_unit = harga_row[0]

    # Hitung durasi sewa dan total bayar
    durasi_hari = (tanggal_rencana_kembali.date() - tanggal_sewa.date()).days + 1
    total_sewa = harga_sewa_per_unit * durasi_hari
    deposit = transaksi[8]
    total_bayar = total_sewa + denda - deposit

    # Update transaksi & unit
    c.execute("""
        UPDATE transaksi
        SET tanggal_kembali = ?, denda = ?, total_bayar_akhir = ?, status_transaksi = 'dikembalikan'
        WHERE id_transaksi = ?
    """, (tanggal_kembali.strftime("%Y-%m-%d %H:%M:%S"), denda, total_bayar, id_transaksi))

    c.execute("UPDATE unit_kendaraan SET status = 'tersedia' WHERE id_unit = ?", (transaksi[1],))

    conn.commit()

    print(f"✅ Pengembalian berhasil. Denda: Rp{denda:,}")

    # Cetak struk otomatis
    cetak_struk_baru({
        "id_transaksi": transaksi[0],
        "plat_nomor": transaksi[12],
        "nama_penyewa": transaksi[2],
        "alamat_penyewa": transaksi[3],
        "tanggal_sewa": transaksi[5],
        "tanggal_kembali": tanggal_kembali.strftime("%Y-%m-%d %H:%M:%S"),
        "harga_sewa_per_hari": harga_sewa_per_unit,
        "deposit": deposit,
        "total_bayar_akhir": total_bayar
    })

#delete = hapus_transaksi()
def hapus_transaksi():
    tampilkan_transaksi()
    id_transaksi = input("Masukkan ID transaksi yang ingin dihapus: ")

    c.execute("SELECT * FROM transaksi WHERE id_transaksi = ?", (id_transaksi,))
    transaksi = c.fetchone()

    if not transaksi:
        print("❌ Transaksi tidak ditemukan.")
        return

    confirm = input("Yakin ingin menghapus transaksi ini? (y/n): ").lower()
    if confirm == 'y':
        c.execute("DELETE FROM transaksi WHERE id_transaksi = ?", (id_transaksi,))
        conn.commit()
        print("✅ Transaksi berhasil dihapus.")
    else:
        print("❌ Penghapusan dibatalkan.")

#////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////
#function Laporan transaksi

#total dari semua transaksi yang di table transaksi
def laporan_total_omset():
    print("\n===== LAPORAN TOTAL OMSET =====")
    c.execute("""
        SELECT SUM(total_bayar_akhir) FROM transaksi
        WHERE status_transaksi = 'dikembalikan'
    """)
    result = c.fetchone()
    total = result[0] if result[0] is not None else 0
    print(f"💰 Total Omset dari semua transaksi: Rp{total:,}")

#total semua sewa yang pernah terjadi
def laporan_jumlah_unit_disewa():
    print("\n===== LAPORAN JUMLAH UNIT DISEWA =====")
    c.execute("""
        SELECT COUNT(*) FROM transaksi
        WHERE status_transaksi IN ('disewa', 'dikembalikan')
    """)
    result = c.fetchone()
    jumlah = result[0] if result[0] is not None else 0
    print(f"🚗 Total unit kendaraan pernah disewa: {jumlah}")

#Cek total kendara di sewa per jenis kemudian di order paling banyak disewa kemudian tampilkan paling atas
def laporan_jenis_paling_laris():
    print("\n===== JENIS KENDARAAN PALING LARIS =====")
    c.execute("""
        SELECT jk.nama_jenis, COUNT(*) AS total_disewa
        FROM transaksi t
        JOIN unit_kendaraan uk ON t.id_unit = uk.id_unit
        JOIN jenis_kendaraan jk ON uk.id_jenis = jk.id_jenis
        WHERE t.status_transaksi IN ('disewa', 'dikembalikan')
        GROUP BY jk.nama_jenis
        ORDER BY total_disewa DESC
        LIMIT 1
    """)
    result = c.fetchone()
    if result:
        print(f"🏅 Jenis Kendaraan Paling Laris: {result[0]} (Total disewa: {result[1]} kali)")
    else:
        print("❌ Belum ada data transaksi.")
