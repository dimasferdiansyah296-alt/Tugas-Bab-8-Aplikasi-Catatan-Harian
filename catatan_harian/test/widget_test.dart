import 'package:catatan_harian/models/catatan.dart';
import 'package:catatan_harian/screens/daftar_catatan_screen.dart';
import 'package:catatan_harian/services/catatan_storage.dart';
import 'package:catatan_harian/utils/tanggal_formatter.dart';
import 'package:flutter/material.dart';
import 'package:flutter_test/flutter_test.dart';
import 'package:intl/date_symbol_data_local.dart';
import 'package:shared_preferences/shared_preferences.dart';

void main() {
  setUpAll(() async {
    // Menyiapkan data locale agar intl dapat memformat tanggal Bahasa Indonesia.
    await initializeDateFormatting('id_ID', null);
  });

  setUp(() {
    // Mengosongkan penyimpanan tiruan sebelum setiap pengujian.
    SharedPreferences.setMockInitialValues(<String, Object>{});
  });

  Widget bangunAplikasi() {
    return const MaterialApp(home: DaftarCatatanScreen());
  }

  group('Pengujian halaman daftar catatan', () {
    testWidgets('menampilkan tampilan kosong saat belum ada catatan',
        (tester) async {
      await tester.pumpWidget(bangunAplikasi());
      await tester.pumpAndSettle();

      expect(find.text('Belum ada catatan'), findsOneWidget);
      expect(find.text('Tambah'), findsOneWidget);
    });

    testWidgets('berhasil menambah catatan baru dan menampilkannya',
        (tester) async {
      await tester.pumpWidget(bangunAplikasi());
      await tester.pumpAndSettle();

      // Tekan tombol Tambah.
      await tester.tap(find.text('Tambah'));
      await tester.pumpAndSettle();

      expect(find.text('Tambah Catatan'), findsOneWidget);

      // Isi form.
      await tester.enterText(
        find.widgetWithText(TextFormField, 'Judul Catatan'),
        'Belajar Flutter',
      );
      await tester.enterText(
        find.widgetWithText(TextFormField, 'Isi Catatan'),
        'Mempelajari paket shared_preferences dan intl.',
      );

      await tester.tap(find.text('Simpan Catatan'));
      await tester.pumpAndSettle();

      // Kembali ke daftar dan catatan muncul.
      expect(find.text('Belajar Flutter'), findsOneWidget);
      expect(find.text('1 catatan'), findsOneWidget);
      expect(find.text('Belum ada catatan'), findsNothing);
    });

    testWidgets('menolak simpan jika judul dan isi kosong', (tester) async {
      await tester.pumpWidget(bangunAplikasi());
      await tester.pumpAndSettle();

      await tester.tap(find.text('Tambah'));
      await tester.pumpAndSettle();

      await tester.tap(find.text('Simpan Catatan'));
      await tester.pumpAndSettle();

      // Tetap berada di form dan muncul pesan validasi.
      expect(find.text('Judul catatan tidak boleh kosong'), findsOneWidget);
      expect(find.text('Isi catatan tidak boleh kosong'), findsOneWidget);
    });
  });

  group('Pengujian penyimpanan shared_preferences', () {
    test('menyimpan lalu membaca kembali catatan dengan data yang sama',
        () async {
      final storage = CatatanStorage();
      final catatan = Catatan(
        id: '1',
        judul: 'Catatan Uji',
        isi: 'Isi catatan uji',
        tanggal: DateTime(2026, 11, 3, 14, 30),
      );

      await storage.simpanSemua(<Catatan>[catatan]);
      final hasil = await storage.muatSemua();

      expect(hasil.length, 1);
      expect(hasil.first.id, '1');
      expect(hasil.first.judul, 'Catatan Uji');
      expect(hasil.first.isi, 'Isi catatan uji');
      expect(hasil.first.tanggal, DateTime(2026, 11, 3, 14, 30));
    });

    test('mengembalikan daftar kosong saat belum ada data', () async {
      final storage = CatatanStorage();
      final hasil = await storage.muatSemua();

      expect(hasil, isEmpty);
    });
  });

  group('Pengujian format tanggal dengan intl', () {
    test('memformat tanggal ke format Bahasa Indonesia', () {
      final tanggal = DateTime(2026, 11, 3, 14, 30);

      expect(TanggalFormatter.lengkap(tanggal), 'Selasa, 3 November 2026 • 14:30');
      expect(TanggalFormatter.singkat(tanggal), '3 Nov 2026, 14:30');
      expect(TanggalFormatter.tanggalSaja(tanggal), '3 November 2026');
      expect(TanggalFormatter.jamSaja(tanggal), '14:30');
    });
  });
}
