import 'package:flutter/material.dart';

import '../models/catatan.dart';
import '../services/catatan_storage.dart';
import '../utils/tanggal_formatter.dart';
import 'form_catatan_screen.dart';

/// Halaman utama: menampilkan daftar catatan harian.
class DaftarCatatanScreen extends StatefulWidget {
  const DaftarCatatanScreen({super.key});

  @override
  State<DaftarCatatanScreen> createState() => _DaftarCatatanScreenState();
}

class _DaftarCatatanScreenState extends State<DaftarCatatanScreen> {
  final CatatanStorage _storage = CatatanStorage();

  List<Catatan> _daftarCatatan = <Catatan>[];
  bool _sedangMemuat = true;

  @override
  void initState() {
    super.initState();
    _muatCatatan();
  }

  /// Mengambil data dari shared_preferences (fitur paket 1).
  Future<void> _muatCatatan() async {
    final data = await _storage.muatSemua();
    // Urutkan dari tanggal terbaru ke terlama.
    data.sort((a, b) => b.tanggal.compareTo(a.tanggal));

    if (!mounted) return;
    setState(() {
      _daftarCatatan = data;
      _sedangMemuat = false;
    });
  }

  /// Menyimpan daftar terbaru ke penyimpanan perangkat.
  Future<void> _simpanKePerangkat() async {
    await _storage.simpanSemua(_daftarCatatan);
  }

  /// Membuka form untuk menambah catatan baru.
  Future<void> _tambahCatatan() async {
    final hasil = await Navigator.push<Catatan>(
      context,
      MaterialPageRoute(
        builder: (context) => const FormCatatanScreen(),
      ),
    );

    if (hasil == null) return;

    setState(() {
      _daftarCatatan.add(hasil);
      _daftarCatatan.sort((a, b) => b.tanggal.compareTo(a.tanggal));
    });
    await _simpanKePerangkat();
    _tampilkanPesan('Catatan berhasil disimpan');
  }

  /// Membuka form untuk mengubah catatan yang sudah ada.
  Future<void> _ubahCatatan(Catatan catatan) async {
    final hasil = await Navigator.push<Catatan>(
      context,
      MaterialPageRoute(
        builder: (context) => FormCatatanScreen(catatanAwal: catatan),
      ),
    );

    if (hasil == null) return;

    setState(() {
      final indeks = _daftarCatatan.indexWhere((item) => item.id == hasil.id);
      if (indeks != -1) {
        _daftarCatatan[indeks] = hasil;
      }
      _daftarCatatan.sort((a, b) => b.tanggal.compareTo(a.tanggal));
    });
    await _simpanKePerangkat();
    _tampilkanPesan('Catatan berhasil diperbarui');
  }

  /// Menghapus catatan setelah dikonfirmasi pengguna.
  Future<void> _hapusCatatan(Catatan catatan) async {
    final konfirmasi = await showDialog<bool>(
      context: context,
      builder: (context) => AlertDialog(
        title: const Text('Hapus Catatan'),
        content: Text('Yakin ingin menghapus "${catatan.judul}"?'),
        actions: [
          TextButton(
            onPressed: () => Navigator.pop(context, false),
            child: const Text('Batal'),
          ),
          FilledButton(
            onPressed: () => Navigator.pop(context, true),
            child: const Text('Hapus'),
          ),
        ],
      ),
    );

    if (konfirmasi != true) return;

    setState(() {
      _daftarCatatan.removeWhere((item) => item.id == catatan.id);
    });
    await _simpanKePerangkat();
    _tampilkanPesan('Catatan berhasil dihapus');
  }

  void _tampilkanPesan(String pesan) {
    if (!mounted) return;
    ScaffoldMessenger.of(context).showSnackBar(
      SnackBar(content: Text(pesan), duration: const Duration(seconds: 2)),
    );
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        backgroundColor: Theme.of(context).colorScheme.primaryContainer,
        title: const Text('Catatan Harian'),
        actions: [
          if (_daftarCatatan.isNotEmpty)
            Padding(
              padding: const EdgeInsets.only(right: 16),
              child: Center(
                child: Text(
                  '${_daftarCatatan.length} catatan',
                  style: Theme.of(context).textTheme.bodySmall,
                ),
              ),
            ),
        ],
      ),
      body: _bangunIsi(),
      floatingActionButton: FloatingActionButton.extended(
        onPressed: _tambahCatatan,
        icon: const Icon(Icons.add),
        label: const Text('Tambah'),
      ),
    );
  }

  Widget _bangunIsi() {
    if (_sedangMemuat) {
      return const Center(child: CircularProgressIndicator());
    }

    if (_daftarCatatan.isEmpty) {
      return _bangunTampilanKosong();
    }

    return ListView.builder(
      padding: const EdgeInsets.fromLTRB(12, 12, 12, 90),
      itemCount: _daftarCatatan.length,
      itemBuilder: (context, indeks) {
        final catatan = _daftarCatatan[indeks];
        return _kartuCatatan(catatan);
      },
    );
  }

  Widget _bangunTampilanKosong() {
    return Center(
      child: Padding(
        padding: const EdgeInsets.all(32),
        child: Column(
          mainAxisAlignment: MainAxisAlignment.center,
          children: [
            Icon(
              Icons.menu_book_outlined,
              size: 80,
              color: Theme.of(context).colorScheme.primary.withValues(alpha: 0.5),
            ),
            const SizedBox(height: 16),
            Text(
              'Belum ada catatan',
              style: Theme.of(context).textTheme.titleMedium,
            ),
            const SizedBox(height: 8),
            Text(
              'Tekan tombol "Tambah" untuk membuat catatan harian pertama Anda.',
              textAlign: TextAlign.center,
              style: Theme.of(context).textTheme.bodyMedium,
            ),
          ],
        ),
      ),
    );
  }

  Widget _kartuCatatan(Catatan catatan) {
    return Card(
      margin: const EdgeInsets.only(bottom: 10),
      child: ListTile(
        contentPadding: const EdgeInsets.symmetric(horizontal: 16, vertical: 8),
        leading: CircleAvatar(
          backgroundColor: Theme.of(context).colorScheme.primaryContainer,
          child: const Icon(Icons.edit_note),
        ),
        title: Text(
          catatan.judul,
          maxLines: 1,
          overflow: TextOverflow.ellipsis,
          style: const TextStyle(fontWeight: FontWeight.w600),
        ),
        subtitle: Column(
          crossAxisAlignment: CrossAxisAlignment.start,
          children: [
            const SizedBox(height: 4),
            Text(
              catatan.isi,
              maxLines: 2,
              overflow: TextOverflow.ellipsis,
            ),
            const SizedBox(height: 6),
            // Menampilkan tanggal memakai paket intl (paket 2).
            Text(
              TanggalFormatter.lengkap(catatan.tanggal),
              style: Theme.of(context).textTheme.labelSmall?.copyWith(
                    color: Theme.of(context).colorScheme.primary,
                  ),
            ),
          ],
        ),
        trailing: IconButton(
          tooltip: 'Hapus',
          icon: const Icon(Icons.delete_outline),
          onPressed: () => _hapusCatatan(catatan),
        ),
        onTap: () => _ubahCatatan(catatan),
      ),
    );
  }
}
