import os
from fpdf import FPDF
import sqlite3
from datetime import datetime

# Setup koneksi dan cursor database
conn = sqlite3.connect('databaseDeAuto.db')
c = conn.cursor()
pdf = FPDF()

class ReceiptPDF(FPDF):
    def __init__(self):
        super().__init__(orientation='P', format=(45 , 150))
        self.set_auto_page_break(auto=False)
        # Set ukuran halaman (58mm x 3276mm)
        

    def header(self):
        self.set_font('Courier', 'B', 10)
        self.cell(0, 7, "DeAUTO Rental Motor", 0, 1, 'C')
        self.set_font('Courier', '', 6)
        self.cell(0, 5, "Jl. Contoh Alamat No.123", 0, 1, 'C')
        self.cell(0, 3, "Kota Contoh", 0, 1, 'C')
        self.cell(0, 5, "Telp: 0812-3456-7890", 0, 1, 'C')
        self.ln(3)
        self.line(0, self.get_y(), 200, self.get_y())
        self.ln(3)

    def footer(self):
        self.set_y(-30)
        self.set_font('Courier', '', 6)
        self.cell(0, 5, "Terima kasih atas kepercayaan Anda!", 0, 1, 'C')
        self.cell(0, 5, "Follow kami di @DeAUTO", 0, 1, 'C')

def cetak_struk(id_transaksi):
    pdf = ReceiptPDF()
    pdf.add_page()

    # Ambil data transaksi dari database
    c.execute("""
        SELECT transaksi.id_transaksi, unit_kendaraan.plat_nomor, transaksi.nama_penyewa,
               transaksi.alamat_penyewa, transaksi.tanggal_sewa, transaksi.tanggal_rencana_kembali,
               transaksi.deposit, transaksi.total_bayar_akhir
        FROM transaksi
        JOIN unit_kendaraan ON transaksi.id_unit = unit_kendaraan.id_unit
        WHERE transaksi.id_transaksi = ?
    """, (id_transaksi,))
    data = c.fetchone()

    if not data:
        print("❌ Tidak ada data transaksi untuk dicetak.")
        return

    # Menambahkan informasi transaksi ke struk
    pdf.set_font('Courier', '', 5)  
    page_width = 0
    pdf.cell(0, 4, "========================================", 0, 1, 'C')
    pdf.set_x(0)
    pdf.cell(page_width, 4, f"ID Transaksi     : {data[0]}", 0, 1,  "L")
    pdf.set_x(0)
    pdf.cell(page_width, 4, f"Plat Nomor       : {data[1] if data[1] is not None else 'N/A'}", 0, 1, "L")
    pdf.set_x(0)
    pdf.cell(page_width, 4, f"Nama Penyewa     : {data[2] if data[2] is not None else 'N/A'}", 0, 1, "L")
    pdf.set_x(0)
    pdf.cell(page_width, 4, f"Alamat Penyewa   : {data[3] if data[3] is not None else 'N/A'}", 0, 1,  "L")
    pdf.set_x(0)
    pdf.cell(page_width, 4, f"Tanggal Sewa     : {data[4] if data[4] is not None else 'N/A'}", 0, 1,  "L")
    pdf.set_x(0)
    pdf.cell(page_width, 4, f"Tanggal Kembali  : {data[5] if data[5] is not None else 'N/A'}", 0, 1,  "L")
    pdf.set_x(0)
    pdf.cell(page_width, 4, f"Durasi Sewa      : 5 Hari", 0, 1,  "L")  # Hardcoded as per your request
    pdf.set_x(0)
    pdf.cell(page_width, 4, f"Harga Sewa       : Rp 500.000", 0, 1,  "L")  # Hardcoded as per your request
    pdf.set_x(0)
    pdf.cell(page_width, 4, f"Deposit          : Rp {data[6] if data[6] is not None else 0:,}", 0, 1,  "L")
    pdf.set_x(0)
    pdf.cell(page_width, 4, "--------------------------------", 0, 1,  "L")
    pdf.set_x(0)
    pdf.cell(page_width, 4, f"Total Bayar      : Rp {data[7] if data[7] is not None else 0:,}", 0, 1,  "L")
    pdf.set_x(0)
    pdf.cell(page_width, 4, "--------------------------------", 0, 1,  "L")
    pdf.cell(0, 4, "Terima kasih atas kepercayaan Anda!", 0, 1, "C")
    pdf.cell(0, 4, "Follow kami di @DeAUTO", 0, 1, "C")
    pdf.cell(0, 4, "========================================", 0, 1, "C")

    # Menyimpan file PDF
    pdf_file_name = f"struk_transaksi_{id_transaksi}.pdf"
    pdf.output(pdf_file_name)
    print(f"✅ PDF berhasil dibuat: {pdf_file_name}")

    # Cetak PDF setelah dibuat
    print_pdf(pdf_file_name)

def print_pdf(pdf_file_name):
    if os.name == 'nt':
        try:
            os.startfile(pdf_file_name, "print")
        except Exception:
            print(f"❌ Tidak bisa cetak otomatis. Buka dan print manual: {pdf_file_name}")
    else:
        print(f"🖨️ File disimpan. Silakan cetak manual: {pdf_file_name}")



def menu_print():
    while True:
        print("\n===== MENU CETAK =====")
        print("1. Cetak Struk Transaksi")
        print("2. Kembali")
        pilihan = input("Pilih menu: ")

        if pilihan == '1':
            id_transaksi = input("Masukkan ID Transaksi: ")
            cetak_struk(id_transaksi)
        elif pilihan == '2':
            break
        else:
            print("❌ Pilihan tidak valid.")

# Jika Anda ingin memanggil menu_print dari dashboard, Anda bisa melakukannya seperti ini:
# from print import menu_print
# menu_print()
menu_print()
