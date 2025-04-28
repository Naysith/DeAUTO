import table  # Import semua function dari table.py (CRUD)

# ==== LOGIN SYSTEM ====
def login():
    print("===== LOGIN =====")
    username = input("Username: ").strip()
    password = input("Password: ").strip()

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


# ==== DASHBOARD ADMIN ====
def dashboard_admin():
    while True:
        print("\n===== DASHBOARD ADMIN =====")
        print("1. CRUD Jenis Kendaraan")
        print("2. Input Stok Kendaraan")
        print("3. Pecah Stok menjadi Unit Kendaraan")
        print("4. Logout")
        pilihan = input("Pilih menu: ")

        if pilihan == '1':
            menu_jenis_kendaraan()
        elif pilihan == '2':
            menu_stok_kendaraan()
        elif pilihan == '3':
            menu_unit_kendaraan()
        elif pilihan == '4':
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
        print("4. Logout")
        pilihan = input("Pilih menu: ")

        if pilihan == '1':
            table.tambah_transaksi()
        elif pilihan == '2':
            table.proses_pengembalian()
        elif pilihan == '3':
            menu_laporan()
        elif pilihan == '4':
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
    login()