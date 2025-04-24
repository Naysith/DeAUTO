import sqlite3
import table

def main_menu():
    while True:
        print("\nMenu:")
        print("1. Tambah user")
        print("2. Tampilkan user")
        print("3. Update user")
        print("4. Hapus user")
        print("5. Keluar")

        pilihan = input("Pilih aksi (1/2/3/4/5): ")

        if pilihan == "1":
            table.tambah_user()
        elif pilihan == "2":
            table.tampilkan_user()
        elif pilihan == "3":
            table.update_user()
        elif pilihan == "4":
            table.hapus_user()
        elif pilihan == "5":
            print("Keluar dari program.")
            break
        else:
            print("❌ Pilihan tidak valid, coba lagi.")

while table.login() == False:
    table.login()

main_menu()