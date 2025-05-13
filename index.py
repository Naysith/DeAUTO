import table  # Import semua function dari table.py (CRUD)
import fpdf
from fpdf import FPDF
from print_baru import cetak_struk_baru

# ==== LOGIN SYSTEM ====
def login():
    print("===== LOGIN =====")
    username = input("Username: ")
    password = input("Password: ")
    
    if username == "master" and password == "master123":
        print("\n Login sebagai MASTER")
        dashboard_master()
        return

    # Cek user di database
    table.c.execute("SELECT * FROM user WHERE username = ? AND password = ?", (username, password))
    user = table.c.fetchone()

    if user:
        print(f"\n✅ Login berhasil sebagai {user[3].upper()}!")
        if user[3] == 'admin':
            dashboard_admin()
        elif user[3] == 'staff':
            dashboard_staff()
        else:
            print("❌ Role tidak dikenali.")
    else:
        print("❌ Login gagal. Username atau password salah.")

def dashboard_master():
    while True:
        print("\n===== MASTER MENU =====")
        print("1. Tambah User (admin/staff)")
        print("2. Hapus User")
        print("3. Lihat Semua User")
        print("4. Logout")
        pilihan = input("Pilih menu: ")

        if pilihan == '1':
            table.tambah_user()
        elif pilihan == '2':
            table.hapus_user()
        elif pilihan == '3':
            table.tampilkan_user()
        elif pilihan == '4':
            print("👋 Logout master...")
            break
        else:
            print("❌ Pilihan tidak valid.")


# ==== DASHBOARD ADMIN ====
def dashboard_admin():
    while True:
        print("\n===== DASHBOARD ADMIN =====")
        print("1. CRUD Jenis Kendaraan")
        print("2. Input Stok Kendaraan")
        print("3. Pecah Stok menjadi Unit Kendaraan")
        print("4. Menu Transaksi")
        print("5. Logout")
        pilihan = input("Pilih menu: ")

        if pilihan == '1':
            menu_jenis_kendaraan()
        elif pilihan == '2':
            menu_stok_kendaraan()
        elif pilihan == '3':
            menu_unit_kendaraan()
        elif pilihan == '4':
            menu_transaksi()
        elif pilihan == '5':
            print("\n🚪 Logout berhasil.")
            break
        else:
            print("❌ Pilihan tidak valid.")


# ==== DASHBOARD STAFF ====
def dashboard_staff():
    while True:
        print("\n===== DASHBOARD STAFF =====")
        print("1. Transaksi Penyewaan")
        print("2. Transaksi Pengembalian")
        print("3. Laporan")
        print("4. Cetak Struk Transaksi Sebelumnya")
        print("5. Logout")
        pilihan = input("Pilih menu: ")

        if pilihan == '1':
            table.tambah_transaksi()
        elif pilihan == '2':
            table.proses_pengembalian()
        elif pilihan == '3':
            menu_laporan()
        elif pilihan == '4':
            menu_cetak_struk()
        elif pilihan == '5':
            print("\n🚪 Logout berhasil.")
            break
        else:
            print("❌ Pilihan tidak valid.")


# ==== MENU CRUD JENIS KENDARAAN ====
def menu_jenis_kendaraan():
    while True:
        print("\n===== MENU JENIS KENDARAAN =====")
        print("1. Tambah Jenis")
        print("2. Tampilkan Jenis")
        print("3. Update Jenis")
        print("4. Hapus Jenis")
        print("5. Kembali")
        pilihan = input("Pilih menu: ")

        if pilihan == '1':
            table.tambah_jenis_kendaraan()
        elif pilihan == '2':
            table.tampilkan_jenis_kendaraan()
        elif pilihan == '3':
            table.update_jenis_kendaraan()
        elif pilihan == '4':
            table.hapus_jenis_kendaraan()
        elif pilihan == '5':
            break
        else:
            print("❌ Pilihan tidak valid.")


# ==== MENU CRUD AKUN USER ====
def menu_edit_akun():
    while True:
        print("\n===== MENU EDIT AKUN =====")
        print("1. Tambah Akun")
        print("2. Tampilkan List Akun")
        print("3. Update Akun")
        print("4. Hapus Akun")
        print("5. Kembali")
        pilihan = input("Pilih menu: ")

        if pilihan == '1':
            table.tambah_user()
        elif pilihan == '2':
            table.tampilkan_user()
        elif pilihan == '3':
            table.update_user()
        elif pilihan == '4':
            table.hapus_user()
        elif pilihan == '5':
            break
        else:
            print("❌ Pilihan tidak valid.")


# ==== MENU CRUD STOK KENDARAAN ====
def menu_stok_kendaraan():
    while True:
        print("\n===== MENU STOK KENDARAAN =====")
        print("1. Input Stok Kendaraan")
        print("2. Tampilkan Stok")
        print("3. Update Stok")
        print("4. Hapus Stok")
        print("5. Kembali")
        pilihan = input("Pilih menu: ")

        if pilihan == '1':
            table.tambah_stok_kendaraan()
        elif pilihan == '2':
            table.tampilkan_stok_kendaraan()
        elif pilihan == '3':
            table.update_stok_kendaraan()
        elif pilihan == '4':
            table.hapus_stok_kendaraan()
        elif pilihan == '5':
            break
        else:
            print("❌ Pilihan tidak valid.")


# ==== MENU CRUD UNIT KENDARAAN ====
def menu_unit_kendaraan():
    while True:
        print("\n===== MENU UNIT KENDARAAN =====")
        print("1. Tambah Unit")
        print("2. Tampilkan Unit")
        print("3. Update Unit")
        print("4. Hapus Unit")
        print("5. Kembali")
        pilihan = input("Pilih menu: ")

        if pilihan == '1':
            table.tambah_unit_kendaraan()
        elif pilihan == '2':
            table.tampilkan_unit_kendaraan()
        elif pilihan == '3':
            table.update_unit_kendaraan()
        elif pilihan == '4':
            table.hapus_unit_kendaraan()
        elif pilihan == '5':
            break
        else:
            print("❌ Pilihan tidak valid.")

# ==== MENU TRANSAKSI ====
def menu_transaksi():
    while True:
        print("\n===== MENU TRANSAKSI =====")
        print("1. Tambah Transaksi Penyewaan")
        print("2. Tampilkan Semua Transaksi")
        print("3. Proses Pengembalian Kendaraan")
        print("4. Hapus Transaksi")
        print("5. Kembali")
        pilihan = input("Pilih menu: ")

        if pilihan == '1':
            table.tambah_transaksi()
        elif pilihan == '2':
            table.tampilkan_transaksi()
        elif pilihan == '3':
            table.proses_pengembalian()
        elif pilihan == '4':
            table.hapus_transaksi()
        elif pilihan == '5':
            break
        else:
            print("❌ Pilihan tidak valid.")

# ==== MENU PRINT ====
def menu_cetak_struk():
    while True:
        print("\n===== MENU CETAK STRUK =====")
        print("1. Cetak Struk Transaksi Sebelumnya")
        print("2. Kembali")
        pilihan = input("Pilih menu: ")

        if pilihan == '1':
            # Tampilkan transaksi yang sudah dikembalikan
            table.c.execute("""
                SELECT t.id_transaksi, u.plat_nomor, t.nama_penyewa, t.tanggal_kembali
                FROM transaksi t
                JOIN unit_kendaraan u ON t.id_unit = u.id_unit
                WHERE t.status_transaksi = 'dikembalikan'
                ORDER BY t.tanggal_kembali DESC
                                                                                                            """)
            records = table.c.fetchall()

            if not records:
                print("📭 Belum ada transaksi yang dikembalikan.")
                continue

            print("\n📋 Transaksi Selesai:")
            print("-" * 50)
            for r in records:
                print(f"ID: {r[0]} | Plat: {r[1]} | Penyewa: {r[2]} | Kembali: {r[3]}")
            print("-" * 50)

            # Minta input ID
            id_transaksi = input("Masukkan ID Transaksi yang ingin dicetak: ")

            # Fetch full transaction data by ID
            table.c.execute("""
                SELECT t.id_transaksi, u.plat_nomor, t.nama_penyewa, t.alamat_penyewa,
                       t.tanggal_sewa, t.tanggal_kembali, t.deposit, t.total_bayar_akhir,
                       u.id_jenis
                FROM transaksi t
                JOIN unit_kendaraan u ON t.id_unit = u.id_unit
                WHERE t.id_transaksi = ? AND t.status_transaksi = 'dikembalikan'
            """, (id_transaksi,))
            data = table.c.fetchone()
            
            if not data:
                print("❌ Transaksi tidak ditemukan atau belum dikembalikan.")
                continue

            # Get harga sewa per hari
            table.c.execute("SELECT harga_sewa FROM jenis_kendaraan WHERE id_jenis = ?", (data[8],))
            harga_row = table.c.fetchone()
            harga_sewa = harga_row[0] if harga_row else 0

            cetak_struk_baru({
                "id_transaksi": data[0],
                "plat_nomor": data[1],
                "nama_penyewa": data[2],
                "alamat_penyewa": data[3],
                "tanggal_sewa": data[4],
                "tanggal_kembali": data[5],
                "harga_sewa_per_hari": harga_sewa,
                "deposit": data[6],     
                "total_bayar_akhir": data[7]
            })

        elif pilihan == '2':
            break
        else:
            print("❌ Pilihan tidak valid.")


# ==== MENU LAPORAN ADMIN ====
def menu_laporan():
    while True:
        print("\n===== MENU LAPORAN =====")
        print("1. Laporan Total Omset")
        print("2. Laporan Jumlah Unit Disewa")
        print("3. Laporan Jenis Kendaraan Paling Laris")
        print("4. Kembali")
        pilihan = input("Pilih menu: ")

        if pilihan == '1':
            table.laporan_total_omset()
        elif pilihan == '2':
            table.laporan_jumlah_unit_disewa()
        elif pilihan == '3':
            table.laporan_jenis_paling_laris()
        elif pilihan == '4':
            break
        else:
            print("❌ Pilihan tidak valid.")


# ==== START PROGRAM ====
if __name__ == "__main__":
    while True:
        login()
