"""
Utility untuk generate file Excel dari data laporan.
"""
from io import BytesIO
from openpyxl import Workbook
from openpyxl.styles import Font, Alignment, PatternFill
from openpyxl.utils import get_column_letter


def export_rumusan_mk(data: dict) -> BytesIO:
    """Export laporan Rumusan MK (Tabel 19) ke Excel."""
    wb = Workbook()
    ws = wb.active
    ws.title = "Rumusan MK"

    # Header
    ws.append([f"Kelas: {data['kelas']} - {data['mk']} ({data['sks']} SKS)"])
    ws.append([f"Dosen: {data.get('dosen') or '-'}"])
    ws.append([])

    # Kolom header
    header = ["NIM", "Nama"] + data["cpmk_kolom"] + \
             ["Nilai Angka", "Huruf", "Lulus"]
    ws.append(header)

    # Styling header
    for col in range(1, len(header) + 1):
        cell = ws.cell(row=4, column=col)
        cell.font = Font(bold=True, color="FFFFFF")
        cell.fill = PatternFill("solid", fgColor="4F46E5")
        cell.alignment = Alignment(horizontal="center")

    # Data
    for m in data["mahasiswa"]:
        row = [m["nim"], m["nama"]]
        row += [m["cpmk_nilai"].get(k) for k in data["cpmk_kolom"]]
        row += [m["nilai_angka"], m["nilai_huruf"],
                "Ya" if m["lulus"] else "Tidak"]
        ws.append(row)

    # Auto width
    for i in range(1, len(header) + 1):
        ws.column_dimensions[get_column_letter(i)].width = 18

    buf = BytesIO()
    wb.save(buf)
    buf.seek(0)
    return buf


def export_rumusan_cpl(data: dict) -> BytesIO:
    """Export laporan Rumusan CPL (Tabel 20) ke Excel."""
    wb = Workbook()
    ws = wb.active
    ws.title = "Rumusan CPL"

    mhs = data["mahasiswa"]
    ws.append([f"Mahasiswa: {mhs['nim']} - {mhs['nama']}"])
    ws.append([f"Angkatan: {mhs['angkatan']}"])
    ws.append([])

    header = ["CPL", "Deskripsi", "Skor Maks", "Total", "Nilai", "Status"]
    ws.append(header)
    for col in range(1, len(header) + 1):
        cell = ws.cell(row=4, column=col)
        cell.font = Font(bold=True, color="FFFFFF")
        cell.fill = PatternFill("solid", fgColor="4F46E5")

    for c in data["cpl"]:
        ws.append([
            c["kode"], c["deskripsi"], c["skor_maks"],
            c["total"], c["nilai"], c["status"],
        ])

    for i, w in enumerate([12, 60, 12, 12, 12, 12], start=1):
        ws.column_dimensions[get_column_letter(i)].width = w

    buf = BytesIO()
    wb.save(buf)
    buf.seek(0)
    return buf


def export_transkrip(data: dict) -> BytesIO:
    """Export transkrip mahasiswa ke Excel."""
    wb = Workbook()
    ws = wb.active
    ws.title = "Transkrip"

    mhs = data["mahasiswa"]
    ws.append([f"Transkrip: {mhs['nim']} - {mhs['nama']}"])
    ws.append([f"Angkatan: {mhs['angkatan']}"])
    ws.append([])

    header = ["Semester", "Kode MK", "Nama MK", "SKS",
              "Nilai Angka", "Huruf", "Bobot", "Mutu"]
    ws.append(header)
    for col in range(1, len(header) + 1):
        cell = ws.cell(row=4, column=col)
        cell.font = Font(bold=True, color="FFFFFF")
        cell.fill = PatternFill("solid", fgColor="4F46E5")

    for n in data["nilai"]:
        ws.append([
            n["semester"], n["kode_mk"], n["mk"], n["sks"],
            n["nilai_angka"], n["nilai_huruf"], n["bobot"], n["mutu"],
        ])

    ws.append([])
    ws.append(["", "", "Total SKS:", data["total_sks"]])
    ws.append(["", "", "Total Mutu:", data["total_mutu"]])
    ws.append(["", "", "IPK:", data["ipk"]])

    for i, w in enumerate([10, 12, 40, 6, 12, 8, 8, 8], start=1):
        ws.column_dimensions[get_column_letter(i)].width = w

    buf = BytesIO()
    wb.save(buf)
    buf.seek(0)
    return buf