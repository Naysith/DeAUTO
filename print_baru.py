from fpdf import FPDF
from datetime import datetime
import os

class CustomReceiptPDF(FPDF):
    def __init__(self):
        super().__init__(orientation='P', format=(45, 150))
        self.set_auto_page_break(auto=False)

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

def cetak_struk_baru(data):
    pdf = CustomReceiptPDF()
    pdf.add_page()
    pdf.set_font('Courier', '', 5)
    pdf.cell(0, 4, "=" * 40, 0, 1, 'C')

    durasi = (datetime.strptime(data["tanggal_kembali"], "%Y-%m-%d %H:%M:%S").date() -
              datetime.strptime(data["tanggal_sewa"], "%Y-%m-%d %H:%M:%S").date()).days + 1

    lines = [
        ("ID Transaksi", data["id_transaksi"]),
        ("Plat Nomor", data["plat_nomor"]),
        ("Nama Penyewa", data["nama_penyewa"]),
        ("Alamat Penyewa", data["alamat_penyewa"]),
        ("Tanggal Sewa", data["tanggal_sewa"]),
        ("Tanggal Kembali", data["tanggal_kembali"]),
        ("Durasi Sewa", f"{durasi} Hari"),
        ("Harga Sewa", f"Rp {data['harga_sewa_per_hari']:,}"),
        ("Deposit", f"Rp {data['deposit']:,}"),
        ("-" * 30, ""),
        ("Total Bayar", f"Rp {data['total_bayar_akhir']:,}"),
        ("-" * 30, ""),
        ("Terima kasih atas kepercayaan Anda!", ""),
        ("Follow kami di @DeAUTO", ""),
        ("=" * 40, "")
    ]

    for label, value in lines:
        pdf.set_x(0)
        pdf.cell(0, 4, f"{label:<18} {value}", 0, 1, "L")

    filename = f"struk_transaksi_{data['id_transaksi']}_baru.pdf"
    pdf.output(filename)

    # Optional auto-print (only works on Windows)
    if os.name == 'nt':
        os.startfile(filename, "print")
    else:
        print(f"🖨️ PDF saved as: {filename} — please print manually.")

    return filename
