# -*- coding: utf-8 -*-
"""Membuat laporan praktik Bab 8 dalam format Microsoft Word (.docx).

Jalankan:  python buat_laporan.py
Hasil   :  Laporan_Bab8_Catatan_Harian.docx
"""

import re

from docx import Document
from docx.enum.table import WD_ALIGN_VERTICAL, WD_ROW_HEIGHT_RULE, WD_TABLE_ALIGNMENT
from docx.enum.text import WD_ALIGN_PARAGRAPH, WD_TAB_ALIGNMENT
from docx.oxml import OxmlElement
from docx.oxml.ns import qn
from docx.shared import Cm, Pt, RGBColor

OUT = "Laporan_Bab8_Catatan_Harian.docx"

HIJAU = RGBColor(0x00, 0x69, 0x5C)
HIJAU_TUA = RGBColor(0x00, 0x4D, 0x40)
GELAP = RGBColor(0x26, 0x32, 0x38)
ABU_TEKS = RGBColor(0x54, 0x6E, 0x7A)
PUTIH = RGBColor(0xFF, 0xFF, 0xFF)

WARNA_HEADER = "00695C"
WARNA_BARIS = "F4F7F7"
WARNA_KODE = "F2F4F5"

FONT = "Calibri"
FONT_KODE = "Consolas"

# ------------------------------------------------------------------ UTILITAS

_TOK = re.compile(r"(\*\*.+?\*\*|\*[^*]+?\*|`[^`]+?`)")


def isi_teks(par, teks, ukuran=None, warna=None):
    """Menambahkan teks ke paragraf dengan dukungan **tebal**, *miring*, `kode`."""
    for bagian in _TOK.split(teks):
        if not bagian:
            continue
        if bagian.startswith("**") and bagian.endswith("**"):
            run = par.add_run(bagian[2:-2])
            run.bold = True
        elif bagian.startswith("`") and bagian.endswith("`"):
            run = par.add_run(bagian[1:-1])
            run.font.name = FONT_KODE
            run.font.size = Pt((ukuran or 10.5) - 0.5)
        elif bagian.startswith("*") and bagian.endswith("*"):
            run = par.add_run(bagian[1:-1])
            run.italic = True
        else:
            run = par.add_run(bagian)
        if ukuran:
            run.font.size = Pt(ukuran)
        if warna:
            run.font.color.rgb = warna
    return par


def bayang(obj, warna):
    """Memberi warna latar pada paragraf atau sel tabel."""
    if hasattr(obj, "_tc"):
        pr = obj._tc.get_or_add_tcPr()
    else:
        pr = obj._p.get_or_add_pPr()
    shd = OxmlElement("w:shd")
    shd.set(qn("w:val"), "clear")
    shd.set(qn("w:color"), "auto")
    shd.set(qn("w:fill"), warna)
    pr.append(shd)


def par(doc, teks, ukuran=10.5, rata="kiri", spasi_setelah=6):
    p = doc.add_paragraph()
    p.alignment = {
        "kiri": WD_ALIGN_PARAGRAPH.LEFT,
        "tengah": WD_ALIGN_PARAGRAPH.CENTER,
        "kanan": WD_ALIGN_PARAGRAPH.RIGHT,
        "justify": WD_ALIGN_PARAGRAPH.JUSTIFY,
    }[rata]
    p.paragraph_format.space_after = Pt(spasi_setelah)
    p.paragraph_format.space_before = Pt(0)
    p.paragraph_format.line_spacing = 1.15
    isi_teks(p, teks, ukuran)
    return p


def judul1(doc, teks):
    p = doc.add_paragraph()
    p.paragraph_format.space_before = Pt(16)
    p.paragraph_format.space_after = Pt(6)
    run = p.add_run(teks)
    run.bold = True
    run.font.size = Pt(13.5)
    run.font.color.rgb = HIJAU
    # garis bawah tipis
    pr = p._p.get_or_add_pPr()
    bdr = OxmlElement("w:pBdr")
    bawah = OxmlElement("w:bottom")
    bawah.set(qn("w:val"), "single")
    bawah.set(qn("w:sz"), "6")
    bawah.set(qn("w:space"), "2")
    bawah.set(qn("w:color"), "B2DFDB")
    bdr.append(bawah)
    pr.append(bdr)
    return p


def judul2(doc, teks):
    p = doc.add_paragraph()
    p.paragraph_format.space_before = Pt(11)
    p.paragraph_format.space_after = Pt(4)
    run = p.add_run(teks)
    run.bold = True
    run.font.size = Pt(11.5)
    run.font.color.rgb = GELAP
    return p


def poin(doc, teks):
    p = doc.add_paragraph()
    p.paragraph_format.left_indent = Cm(0.75)
    p.paragraph_format.first_line_indent = Cm(-0.4)
    p.paragraph_format.space_after = Pt(3)
    p.paragraph_format.line_spacing = 1.1
    p.add_run("\u2022\t")
    isi_teks(p, teks, 10.5)
    return p


def nomor(doc, no, teks):
    p = doc.add_paragraph()
    p.paragraph_format.left_indent = Cm(0.75)
    p.paragraph_format.first_line_indent = Cm(-0.75)
    p.paragraph_format.space_after = Pt(3)
    p.paragraph_format.line_spacing = 1.1
    p.add_run("%s.\t" % no)
    isi_teks(p, teks, 10.5)
    return p


def kode(doc, teks):
    """Blok kode dengan latar abu-abu dan font Consolas."""
    baris = teks.split("\n")
    for i, isi in enumerate(baris):
        p = doc.add_paragraph()
        p.paragraph_format.left_indent = Cm(0.5)
        p.paragraph_format.right_indent = Cm(0.2)
        p.paragraph_format.space_before = Pt(3 if i == 0 else 0)
        p.paragraph_format.space_after = Pt(3 if i == len(baris) - 1 else 0)
        p.paragraph_format.line_spacing = 1.0
        bayang(p, WARNA_KODE)
        run = p.add_run(isi if isi else " ")
        run.font.name = FONT_KODE
        run.font.size = Pt(9)
        run.font.color.rgb = RGBColor(0x1B, 0x3A, 0x36)
    doc.add_paragraph().paragraph_format.space_after = Pt(2)


def isi_sel(cell, teks, tebal=False, ukuran=9.5, warna=None, rata="kiri"):
    cell.vertical_alignment = WD_ALIGN_VERTICAL.TOP
    p = cell.paragraphs[0]
    p.alignment = {
        "kiri": WD_ALIGN_PARAGRAPH.LEFT,
        "tengah": WD_ALIGN_PARAGRAPH.CENTER,
    }[rata]
    p.paragraph_format.space_after = Pt(1)
    p.paragraph_format.space_before = Pt(1)
    p.paragraph_format.line_spacing = 1.05
    isi_teks(p, teks, ukuran, warna)
    if tebal:
        for run in p.runs:
            run.bold = True
    return cell


def tabel(doc, data, lebar, header=True, tebal_header=True):
    t = doc.add_table(rows=len(data), cols=len(data[0]))
    t.style = "Table Grid"
    t.alignment = WD_TABLE_ALIGNMENT.CENTER
    t.autofit = False
    tblPr = t._tbl.tblPr
    layout = OxmlElement("w:tblLayout")
    layout.set(qn("w:type"), "fixed")
    tblPr.append(layout)

    for r, baris in enumerate(data):
        for c, isi in enumerate(baris):
            cell = t.cell(r, c)
            cell.width = Cm(lebar[c])
            if header and r == 0:
                bayang(cell, WARNA_HEADER)
                isi_sel(cell, isi, tebal=tebal_header, ukuran=9.5, warna=PUTIH)
            else:
                if r % 2 == 0:
                    bayang(cell, WARNA_BARIS)
                isi_sel(cell, isi, ukuran=9.5)
    doc.add_paragraph().paragraph_format.space_after = Pt(4)
    return t


def kotak_screenshot(doc, caption, tinggi=6.0):
    """Keterangan + kotak kosong tempat menempelkan screenshot."""
    p = doc.add_paragraph()
    p.paragraph_format.space_before = Pt(8)
    p.paragraph_format.space_after = Pt(3)
    run = p.add_run(caption)
    run.bold = True
    run.font.size = Pt(10)

    t = doc.add_table(rows=1, cols=1)
    t.style = "Table Grid"
    t.autofit = False
    cell = t.cell(0, 0)
    cell.width = Cm(17)
    cell.height = Cm(tinggi)
    t.rows[0].height_rule = WD_ROW_HEIGHT_RULE.AT_LEAST
    cell.vertical_alignment = WD_ALIGN_VERTICAL.CENTER
    par_kotak = cell.paragraphs[0]
    par_kotak.alignment = WD_ALIGN_PARAGRAPH.CENTER
    run2 = par_kotak.add_run("[ Tempelkan screenshot di sini ]")
    run2.italic = True
    run2.font.size = Pt(9)
    run2.font.color.rgb = ABU_TEKS
    doc.add_paragraph().paragraph_format.space_after = Pt(2)


def nomor_halaman(par_footer):
    run = par_footer.add_run()
    awal = OxmlElement("w:fldChar")
    awal.set(qn("w:fldCharType"), "begin")
    instr = OxmlElement("w:instrText")
    instr.set(qn("xml:space"), "preserve")
    instr.text = "PAGE"
    akhir = OxmlElement("w:fldChar")
    akhir.set(qn("w:fldCharType"), "end")
    run._r.append(awal)
    run._r.append(instr)
    run._r.append(akhir)


# ------------------------------------------------------------------ DOKUMEN

doc = Document()

# Format halaman A4 dengan margin 2 cm.
bagian = doc.sections[0]
bagian.page_width = Cm(21)
bagian.page_height = Cm(29.7)
bagian.left_margin = Cm(2)
bagian.right_margin = Cm(2)
bagian.top_margin = Cm(2)
bagian.bottom_margin = Cm(1.8)

# Font dasar dokumen.
normal = doc.styles["Normal"]
normal.font.name = FONT
normal.font.size = Pt(10.5)
normal.font.color.rgb = GELAP
normal.element.get_or_add_rPr().get_or_add_rFonts().set(qn("w:eastAsia"), FONT)

# Footer: teks kiri dan nomor halaman kanan.
footer = bagian.footer
par_footer = footer.paragraphs[0]
par_footer.text = ""
tab_stops = par_footer.paragraph_format.tab_stops
tab_stops.add_tab_stop(Cm(17), WD_TAB_ALIGNMENT.RIGHT)
r = par_footer.add_run("Laporan Bab 8 - Catatan Harian\t")
r.font.size = Pt(8.5)
r.font.color.rgb = ABU_TEKS
nomor_halaman(par_footer)
for run in par_footer.runs:
    run.font.size = Pt(8.5)
    run.font.color.rgb = ABU_TEKS

# ------------------------------------------------------------ HALAMAN JUDUL
p = par(doc, "LAPORAN PRAKTIKUM MOBILE PROGRAMMING", ukuran=11.5, rata="tengah",
        spasi_setelah=2)
for run in p.runs:
    run.font.color.rgb = ABU_TEKS

p = par(doc, "BAB 8", ukuran=20, rata="tengah", spasi_setelah=0)
for run in p.runs:
    run.bold = True
    run.font.color.rgb = HIJAU_TUA

p = par(doc, "MENGGUNAKAN PAKET DAN PLUGIN PADA FLUTTER", ukuran=15, rata="tengah",
        spasi_setelah=14)
for run in p.runs:
    run.bold = True
    run.font.color.rgb = HIJAU

p = par(doc, "Aplikasi Catatan Harian", ukuran=18, rata="tengah", spasi_setelah=18)
for run in p.runs:
    run.bold = True
    run.font.color.rgb = GELAP

tabel(doc, [
    ["Komponen", "Keterangan"],
    ["Mata Kuliah", "Mobile Programming"],
    ["Materi", "Bab 8 - Menggunakan Paket dan Plugin pada Flutter"],
    ["Jenis Tugas", "Praktik Individu"],
    ["Bentuk Tugas", "Pembuatan Aplikasi Flutter"],
    ["Tema yang Dipilih", "Catatan Harian (Tema Nomor 1)"],
    ["Paket/Plugin", "shared_preferences ^2.5.6 dan intl ^0.20.3"],
], [4.5, 12.5])

tabel(doc, [
    ["Nama Mahasiswa", "......................................................."],
    ["NIM", "......................................................."],
    ["Kelas", "......................................................."],
], [4.5, 12.5], header=False)

doc.add_page_break()

# ------------------------------------------------------------- 1. JUDUL
judul1(doc, "1.  Judul Aplikasi")
par(doc, "**Catatan Harian** (nama paket Dart: `catatan_harian`). Aplikasi ini dibuat "
         "menggunakan Flutter dengan menerapkan tema pertama pada lembar tugas, yaitu "
         "aplikasi untuk menulis dan menyimpan catatan harian beserta tanggal "
         "pembuatannya.", rata="justify")

# ------------------------------------------------------------- 2. TUJUAN
judul1(doc, "2.  Tujuan")
par(doc, "Tujuan pembuatan aplikasi ini adalah:", spasi_setelah=4)
nomor(doc, 1, "Menerapkan penggunaan paket dan plugin pihak ketiga dari pub.dev pada "
              "proyek Flutter.")
nomor(doc, 2, "Mengelola *dependencies* melalui file `pubspec.yaml`.")
nomor(doc, 3, "Membuat fitur CRUD (tambah, baca, ubah, hapus) catatan harian yang datanya "
              "tersimpan permanen di perangkat memakai paket `shared_preferences`.")
nomor(doc, 4, "Menampilkan tanggal dan waktu dalam format Bahasa Indonesia memakai paket "
              "`intl`.")
nomor(doc, 5, "Menguji fitur aplikasi melalui *widget test* dan pengujian langsung pada "
              "perangkat.")

# ------------------------------------------------------------- 3. PAKET
judul1(doc, "3.  Paket/Plugin yang Digunakan")
par(doc, "Aplikasi ini menggunakan dua paket dari pub.dev, yaitu:", spasi_setelah=6)

tabel(doc, [
    ["No", "Nama Paket", "Versi", "Fungsi dalam Aplikasi"],
    ["1", "shared_preferences", "^2.5.6",
     "Menyimpan data catatan secara permanen di penyimpanan lokal perangkat (key-value "
     "store). Data daftar catatan diubah menjadi String berformat JSON sebelum disimpan, "
     "sehingga tetap ada walaupun aplikasi ditutup."],
    ["2", "intl", "^0.20.3",
     "Memformat objek DateTime menjadi teks tanggal dan waktu berbahasa Indonesia, misalnya "
     "\u201cSelasa, 3 November 2026 \u2022 14:30\u201d, dengan menggunakan locale id_ID."],
], [1.1, 3.4, 1.8, 10.7])

par(doc, "Alamat dokumentasi paket:", spasi_setelah=4)
poin(doc, "shared_preferences - https://pub.dev/packages/shared_preferences")
poin(doc, "intl - https://pub.dev/packages/intl")

# ------------------------------------------------------------- 4. LANGKAH
judul1(doc, "4.  Langkah Implementasi")

judul2(doc, "4.1  Membuat Proyek Flutter")
par(doc, "Proyek dibuat melalui terminal Visual Studio Code dengan perintah berikut:")
kode(doc, "flutter create --org com.example --project-name catatan_harian "
          "--platforms android,windows catatan_harian")

judul2(doc, "4.2  Menambahkan Paket ke pubspec.yaml")
par(doc, "Paket ditambahkan pada bagian `dependencies` di file `pubspec.yaml`. Versi yang "
         "dipakai adalah versi terbaru yang kompatibel dan diperoleh melalui perintah "
         "`flutter pub add`, sehingga penulisan versi tidak dilakukan secara manual:",
    rata="justify")
kode(doc, "dependencies:\n"
          "  flutter:\n"
          "    sdk: flutter\n"
          "  cupertino_icons: ^1.0.8\n"
          "  shared_preferences: ^2.5.6   # menyimpan catatan\n"
          "  intl: ^0.20.3                # memformat tanggal")
par(doc, "Setelah itu dijalankan perintah `flutter pub get` untuk mengunduh paket. Hasilnya "
         "paket `shared_preferences` berhasil terpasang bersama paket pendukungnya "
         "(shared_preferences_android, shared_preferences_windows, dan lain-lain), serta "
         "paket `intl`.", rata="justify")

judul2(doc, "4.3  Mengimpor Paket ke dalam Kode")
par(doc, "Paket diimpor pada file yang membutuhkannya:")
kode(doc, "// lib/services/catatan_storage.dart\n"
          "import 'dart:convert';\n"
          "import 'package:shared_preferences/shared_preferences.dart';\n\n"
          "// lib/utils/tanggal_formatter.dart\n"
          "import 'package:intl/intl.dart';")
par(doc, "Khusus paket `intl`, data locale Bahasa Indonesia perlu dimuat terlebih dahulu "
         "pada fungsi `main()`:")
kode(doc, "await initializeDateFormatting('id_ID', null);")

judul2(doc, "4.4  Struktur Folder Proyek")
tabel(doc, [
    ["Berkas / Folder", "Keterangan"],
    ["lib/main.dart",
     "Titik masuk aplikasi, memuat locale id_ID dan tema Material 3."],
    ["lib/models/catatan.dart",
     "Model data Catatan beserta konversi toJson() dan fromJson()."],
    ["lib/services/catatan_storage.dart",
     "Penyimpanan data memakai shared_preferences (simpan, muat, hapus)."],
    ["lib/utils/tanggal_formatter.dart",
     "Pemformatan tanggal dan waktu memakai intl dengan locale id_ID."],
    ["lib/screens/daftar_catatan_screen.dart",
     "Halaman utama: menampilkan daftar catatan, tombol tambah, ubah, dan hapus."],
    ["lib/screens/form_catatan_screen.dart",
     "Form tambah/ubah catatan beserta validasi input."],
    ["test/widget_test.dart", "Pengujian fitur (widget test dan unit test)."],
], [6.2, 10.8])

judul2(doc, "4.5  Penerapan Paket shared_preferences")
par(doc, "Paket ini menyimpan data dalam bentuk key-value dan hanya mendukung tipe data "
         "primitif serta List<String>. Karena itu, daftar catatan diubah menjadi String JSON "
         "memakai `jsonEncode` sebelum disimpan:", rata="justify")
kode(doc, "// Menyimpan seluruh catatan\n"
          "final prefs = await SharedPreferences.getInstance();\n"
          "await prefs.setString('daftar_catatan', jsonEncode(daftarCatatan));\n\n"
          "// Membaca seluruh catatan\n"
          "final dataMentah = prefs.getString('daftar_catatan');\n"
          "final dataJson = jsonDecode(dataMentah) as List;")
par(doc, "Dengan cara ini, seluruh catatan yang pernah dibuat akan tetap ada saat aplikasi "
         "dijalankan kembali.", rata="justify")

judul2(doc, "4.6  Penerapan Paket intl")
par(doc, "Paket `intl` dipakai untuk mengubah objek `DateTime` menjadi teks tanggal "
         "berbahasa Indonesia:")
kode(doc, "DateFormat('EEEE, d MMMM yyyy \u2022 HH:mm', 'id_ID').format(tanggal);\n"
          "// Hasil: Selasa, 3 November 2026 \u2022 14:30")
par(doc, "Nama hari dan nama bulan otomatis mengikuti locale `id_ID`, sehingga tidak perlu "
         "membuat daftar nama hari dan nama bulan sendiri.", rata="justify")

judul2(doc, "4.7  Fitur Aplikasi")
poin(doc, "**Tambah catatan** - menekan tombol Tambah, mengisi judul dan isi, lalu menyimpan.")
poin(doc, "**Lihat daftar catatan** - catatan diurutkan dari tanggal terbaru ke terlama.")
poin(doc, "**Ubah catatan** - menekan salah satu kartu catatan untuk membuka form ubah.")
poin(doc, "**Hapus catatan** - menekan ikon hapus, lalu muncul dialog konfirmasi.")
poin(doc, "**Validasi input** - judul minimal 3 karakter dan isi tidak boleh kosong.")
poin(doc, "**Penyimpanan permanen** - data tetap tersimpan setelah aplikasi ditutup.")

doc.add_page_break()

# ------------------------------------------------------------- 5. HASIL
judul1(doc, "5.  Hasil Praktik")

judul2(doc, "5.1  Hasil Pemeriksaan Kode dan Pengujian")
par(doc, "Pemeriksaan kode dijalankan dengan perintah `flutter analyze` dan diperoleh hasil "
         "**No issues found!** Selanjutnya pengujian dijalankan dengan perintah "
         "`flutter test` dengan hasil sebagai berikut:", rata="justify")

tabel(doc, [
    ["No", "Nama Pengujian", "Jenis", "Hasil"],
    ["1", "Menampilkan tampilan kosong saat belum ada catatan", "Widget test", "Berhasil"],
    ["2", "Berhasil menambah catatan baru dan menampilkannya", "Widget test", "Berhasil"],
    ["3", "Menolak simpan jika judul dan isi kosong", "Widget test", "Berhasil"],
    ["4", "Menyimpan lalu membaca kembali catatan dengan data yang sama", "Unit test",
     "Berhasil"],
    ["5", "Mengembalikan daftar kosong saat belum ada data", "Unit test", "Berhasil"],
    ["6", "Memformat tanggal ke format Bahasa Indonesia", "Unit test", "Berhasil"],
], [1.1, 8.6, 2.5, 2.8])
par(doc, "Kesimpulan pengujian: **6 dari 6 pengujian lulus (All tests passed!)** dalam waktu "
         "5 detik.", ukuran=9.5, rata="tengah", spasi_setelah=10)

par(doc, "Selanjutnya aplikasi dikompilasi menjadi berkas APK Android menggunakan perintah "
         "`flutter build apk --debug` dan berhasil tanpa kesalahan:", rata="justify")
kode(doc, "Running Gradle task 'assembleDebug'...  1230.1s\n"
          "Built build\\app\\outputs\\flutter-apk\\app-debug.apk")
par(doc, "Berkas `app-debug.apk` tersebut dapat langsung dipasang pada emulator atau "
         "perangkat Android untuk pengujian fitur secara langsung.", rata="justify")

judul2(doc, "5.2  Panduan Pengambilan Screenshot")
par(doc, "Screenshot diambil dari emulator atau perangkat Android yang terhubung. Pada "
         "emulator dapat memakai tombol *screenshot*, sedangkan pada perangkat fisik dapat "
         "memakai kombinasi tombol Power + Volume Down. Daftar screenshot yang dibutuhkan "
         "adalah sebagai berikut:", rata="justify")

tabel(doc, [
    ["No", "Nama File Saran", "Yang Harus Terlihat pada Screenshot"],
    ["1", "01_pubspec.png",
     "Isi bagian dependencies pada file pubspec.yaml yang memperlihatkan baris "
     "shared_preferences dan intl."],
    ["2", "02_pub_get.png",
     "Terminal Visual Studio Code yang menampilkan hasil perintah flutter pub get beserta "
     "daftar paket yang berhasil diunduh."],
    ["3", "03_tampilan_kosong.png",
     "Tampilan awal aplikasi saat belum ada catatan (teks Belum ada catatan dan tombol "
     "Tambah)."],
    ["4", "04_form_tambah.png",
     "Form Tambah Catatan yang sudah terisi judul dan isi catatan."],
    ["5", "05_daftar_catatan.png",
     "Halaman utama yang sudah menampilkan catatan beserta tanggal berformat Bahasa "
     "Indonesia, misalnya Selasa, 3 November 2026."],
    ["6", "06_form_ubah.png",
     "Form Ubah Catatan yang menampilkan bagian Dibuat pada beserta tanggalnya."],
    ["7", "07_konfirmasi_hapus.png",
     "Dialog konfirmasi Hapus Catatan beserta nama catatan yang akan dihapus."],
    ["8", "08_hasil_test.png",
     "Terminal yang menampilkan hasil flutter test dengan tulisan All tests passed!"],
], [1.1, 3.6, 12.3])

judul2(doc, "5.3  Tempat Menempelkan Screenshot")
par(doc, "Klik pada kotak di bawah ini, lalu tempelkan gambar dengan menekan Ctrl + V. "
         "Sesuaikan ukuran gambar agar memenuhi kotak.", rata="justify", spasi_setelah=8)

kotak_screenshot(doc, "Gambar 1. Isi dependencies pada pubspec.yaml (01_pubspec.png)")
kotak_screenshot(doc, "Gambar 2. Hasil perintah flutter pub get (02_pub_get.png)")
kotak_screenshot(doc, "Gambar 3. Tampilan awal aplikasi saat belum ada catatan "
                      "(03_tampilan_kosong.png)")

doc.add_page_break()

kotak_screenshot(doc, "Gambar 4. Form Tambah Catatan yang sudah terisi (04_form_tambah.png)")
kotak_screenshot(doc, "Gambar 5. Daftar catatan beserta tanggal berformat Bahasa Indonesia "
                      "(05_daftar_catatan.png)")
kotak_screenshot(doc, "Gambar 6. Form Ubah Catatan beserta tanggal pembuatan "
                      "(06_form_ubah.png)")

doc.add_page_break()

kotak_screenshot(doc, "Gambar 7. Dialog konfirmasi Hapus Catatan (07_konfirmasi_hapus.png)")
kotak_screenshot(doc, "Gambar 8. Hasil pengujian flutter test (08_hasil_test.png)")

# ------------------------------------------------------------- 6. KESIMPULAN
judul1(doc, "6.  Kesimpulan")
par(doc, "Berdasarkan hasil praktik yang telah dilakukan, dapat disimpulkan bahwa:",
    spasi_setelah=4)
nomor(doc, 1, "Paket dan plugin membuat pengembangan aplikasi Flutter menjadi jauh lebih "
              "cepat karena fitur yang sulit dibuat sendiri sudah tersedia dan dapat "
              "langsung dipakai.")
nomor(doc, 2, "Paket `shared_preferences` berhasil digunakan untuk menyimpan data catatan "
              "secara permanen di perangkat. Data tetap tersimpan walaupun aplikasi ditutup, "
              "sehingga fitur utama aplikasi berjalan dengan baik.")
nomor(doc, 3, "Paket `intl` berhasil memformat tanggal dan waktu ke dalam Bahasa Indonesia "
              "hanya dengan menentukan locale id_ID.")
nomor(doc, 4, "Seluruh fitur aplikasi (tambah, lihat, ubah, hapus, dan validasi) berjalan "
              "sesuai rencana, dibuktikan dengan 6 pengujian yang semuanya lulus dan "
              "`flutter analyze` yang tidak menemukan masalah.")
nomor(doc, 5, "Aplikasi berhasil dikompilasi menjadi berkas APK Android "
              "(`app-debug.apk`) sehingga siap dipasang dan dijalankan pada emulator "
              "maupun perangkat Android.")

judul2(doc, "Kendala yang Dihadapi")
poin(doc, "*shared_preferences* hanya dapat menyimpan tipe data primitif dan List<String>, "
          "sehingga objek Catatan harus diubah menjadi String JSON terlebih dahulu memakai "
          "jsonEncode. Kendala ini diatasi dengan menambahkan metode toJson() dan fromJson() "
          "pada model Catatan.")
poin(doc, "Pemformatan tanggal sempat menampilkan teks berbahasa Inggris karena data locale "
          "belum dimuat. Masalah diatasi dengan memanggil initializeDateFormatting('id_ID', "
          "null) pada fungsi main() sebelum runApp().")
poin(doc, "Kompilasi pertama ke Android memerlukan waktu cukup lama karena Gradle harus "
          "mengunduh dan memasang komponen Android SDK yang belum tersedia, yaitu NDK "
          "28.2.13676358, Android SDK Platform 35 dan 36, serta CMake 3.22.1. Setelah "
          "komponen tersebut terpasang, proses build berikutnya menjadi jauh lebih cepat.")

judul2(doc, "Lampiran - Cara Menjalankan Aplikasi")
kode(doc, "flutter pub get\nflutter run")
par(doc, "Untuk menjalankan pengujian: `flutter test`. Untuk membuat berkas APK: "
         "`flutter build apk --release`.")

# ------------------------------------------------------------ PROPERTI FILE
doc.core_properties.title = "Laporan Bab 8 - Aplikasi Catatan Harian"
doc.core_properties.author = "Mahasiswa Mobile Programming"
doc.core_properties.subject = "Menggunakan Paket dan Plugin pada Flutter"

doc.save(OUT)
print("Selesai:", OUT)
