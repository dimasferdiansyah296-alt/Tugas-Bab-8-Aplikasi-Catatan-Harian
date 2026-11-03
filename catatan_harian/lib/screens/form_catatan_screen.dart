import 'package:flutter/material.dart';

import '../models/catatan.dart';
import '../utils/tanggal_formatter.dart';

/// Halaman form untuk menambah atau mengubah catatan.
///
/// Jika [catatanAwal] bernilai null berarti mode "Tambah Catatan",
/// jika tidak null berarti mode "Ubah Catatan".
class FormCatatanScreen extends StatefulWidget {
  const FormCatatanScreen({super.key, this.catatanAwal});

  final Catatan? catatanAwal;

  @override
  State<FormCatatanScreen> createState() => _FormCatatanScreenState();
}

class _FormCatatanScreenState extends State<FormCatatanScreen> {
  final _formKey = GlobalKey<FormState>();
  late final TextEditingController _judulController;
  late final TextEditingController _isiController;

  bool get _modeUbah => widget.catatanAwal != null;

  @override
  void initState() {
    super.initState();
    _judulController = TextEditingController(text: widget.catatanAwal?.judul ?? '');
    _isiController = TextEditingController(text: widget.catatanAwal?.isi ?? '');
  }

  @override
  void dispose() {
    _judulController.dispose();
    _isiController.dispose();
    super.dispose();
  }

  void _simpan() {
    if (!_formKey.currentState!.validate()) return;

    final catatan = Catatan(
      // Saat mengubah catatan, ID dan tanggal dibuat tetap sama.
      id: widget.catatanAwal?.id ?? DateTime.now().millisecondsSinceEpoch.toString(),
      judul: _judulController.text.trim(),
      isi: _isiController.text.trim(),
      tanggal: widget.catatanAwal?.tanggal ?? DateTime.now(),
    );

    Navigator.pop(context, catatan);
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        backgroundColor: Theme.of(context).colorScheme.primaryContainer,
        title: Text(_modeUbah ? 'Ubah Catatan' : 'Tambah Catatan'),
      ),
      body: SingleChildScrollView(
        padding: const EdgeInsets.all(16),
        child: Form(
          key: _formKey,
          child: Column(
            crossAxisAlignment: CrossAxisAlignment.stretch,
            children: [
              if (_modeUbah)
                Card(
                  child: ListTile(
                    leading: const Icon(Icons.event),
                    title: const Text('Dibuat pada'),
                    subtitle: Text(
                      TanggalFormatter.lengkap(widget.catatanAwal!.tanggal),
                    ),
                  ),
                ),
              const SizedBox(height: 8),
              TextFormField(
                controller: _judulController,
                textInputAction: TextInputAction.next,
                decoration: const InputDecoration(
                  labelText: 'Judul Catatan',
                  hintText: 'Contoh: Belajar Flutter',
                  border: OutlineInputBorder(),
                  prefixIcon: Icon(Icons.title),
                ),
                validator: (nilai) {
                  if (nilai == null || nilai.trim().isEmpty) {
                    return 'Judul catatan tidak boleh kosong';
                  }
                  if (nilai.trim().length < 3) {
                    return 'Judul minimal 3 karakter';
                  }
                  return null;
                },
              ),
              const SizedBox(height: 16),
              TextFormField(
                controller: _isiController,
                maxLines: 8,
                decoration: const InputDecoration(
                  labelText: 'Isi Catatan',
                  hintText: 'Tuliskan isi catatan harian Anda di sini...',
                  border: OutlineInputBorder(),
                  alignLabelWithHint: true,
                ),
                validator: (nilai) {
                  if (nilai == null || nilai.trim().isEmpty) {
                    return 'Isi catatan tidak boleh kosong';
                  }
                  return null;
                },
              ),
              const SizedBox(height: 24),
              FilledButton.icon(
                onPressed: _simpan,
                icon: const Icon(Icons.save),
                label: Text(_modeUbah ? 'Perbarui Catatan' : 'Simpan Catatan'),
                style: FilledButton.styleFrom(
                  padding: const EdgeInsets.symmetric(vertical: 14),
                ),
              ),
              const SizedBox(height: 8),
              OutlinedButton(
                onPressed: () => Navigator.pop(context),
                child: const Text('Batal'),
              ),
            ],
          ),
        ),
      ),
    );
  }
}
