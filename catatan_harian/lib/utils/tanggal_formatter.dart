import 'package:intl/intl.dart';

/// Helper untuk memformat tanggal dan waktu memakai paket intl.
///
/// Locale 'id_ID' dipakai agar nama hari dan nama bulan muncul
/// dalam Bahasa Indonesia, misalnya "Senin, 3 November 2026".
class TanggalFormatter {
  /// Format lengkap: Senin, 3 November 2026 • 14:30
  static String lengkap(DateTime tanggal) {
    return DateFormat('EEEE, d MMMM yyyy • HH:mm', 'id_ID').format(tanggal);
  }

  /// Format singkat untuk ditampilkan di daftar catatan: 3 Nov 2026, 14:30
  static String singkat(DateTime tanggal) {
    return DateFormat('d MMM yyyy, HH:mm', 'id_ID').format(tanggal);
  }

  /// Format tanggal saja: 3 November 2026
  static String tanggalSaja(DateTime tanggal) {
    return DateFormat('d MMMM yyyy', 'id_ID').format(tanggal);
  }

  /// Format jam saja: 14:30
  static String jamSaja(DateTime tanggal) {
    return DateFormat('HH:mm', 'id_ID').format(tanggal);
  }
}
