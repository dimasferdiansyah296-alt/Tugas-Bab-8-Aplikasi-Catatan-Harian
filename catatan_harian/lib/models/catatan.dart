/// Model data untuk satu buah catatan harian.
class Catatan {
  Catatan({
    required this.id,
    required this.judul,
    required this.isi,
    required this.tanggal,
  });

  /// ID unik catatan, dibuat dari waktu pembuatan (milidetik).
  final String id;
  final String judul;
  final String isi;
  final DateTime tanggal;

  /// Mengubah objek menjadi Map agar bisa disimpan sebagai teks di
  /// shared_preferences (paket hanya mendukung tipe primitif dan `List<String>`).
  Map<String, dynamic> toJson() {
    return {
      'id': id,
      'judul': judul,
      'isi': isi,
      'tanggal': tanggal.toIso8601String(),
    };
  }

  /// Mengubah kembali Map (hasil decode JSON) menjadi objek Catatan.
  factory Catatan.fromJson(Map<String, dynamic> json) {
    return Catatan(
      id: json['id'] as String,
      judul: json['judul'] as String,
      isi: json['isi'] as String,
      tanggal: DateTime.parse(json['tanggal'] as String),
    );
  }
}
