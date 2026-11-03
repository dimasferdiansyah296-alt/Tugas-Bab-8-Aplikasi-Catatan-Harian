import 'dart:convert';

import 'package:shared_preferences/shared_preferences.dart';

import '../models/catatan.dart';

/// Kelas yang bertugas menyimpan dan membaca daftar catatan
/// menggunakan paket shared_preferences.
///
/// shared_preferences menyimpan data dalam bentuk key-value sederhana,
/// sehingga daftar catatan diubah dulu menjadi String berformat JSON.
class CatatanStorage {
  /// Kunci (key) yang dipakai untuk menyimpan data di perangkat.
  static const String _kunciCatatan = 'daftar_catatan';

  /// Membaca seluruh catatan dari penyimpanan.
  Future<List<Catatan>> muatSemua() async {
    final prefs = await SharedPreferences.getInstance();
    final String? dataMentah = prefs.getString(_kunciCatatan);

    // Jika belum pernah ada data, kembalikan daftar kosong.
    if (dataMentah == null || dataMentah.isEmpty) {
      return <Catatan>[];
    }

    final List<dynamic> dataJson = jsonDecode(dataMentah) as List<dynamic>;
    return dataJson
        .map((item) => Catatan.fromJson(item as Map<String, dynamic>))
        .toList();
  }

  /// Menyimpan seluruh catatan ke penyimpanan perangkat.
  Future<void> simpanSemua(List<Catatan> daftarCatatan) async {
    final prefs = await SharedPreferences.getInstance();
    final String dataJson = jsonEncode(
      daftarCatatan.map((catatan) => catatan.toJson()).toList(),
    );
    await prefs.setString(_kunciCatatan, dataJson);
  }

  /// Menghapus semua catatan (dipakai untuk pengujian manual).
  Future<void> hapusSemua() async {
    final prefs = await SharedPreferences.getInstance();
    await prefs.remove(_kunciCatatan);
  }
}
