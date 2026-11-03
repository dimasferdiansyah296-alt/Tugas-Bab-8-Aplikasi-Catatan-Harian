import 'package:flutter/material.dart';
import 'package:intl/date_symbol_data_local.dart';

import 'screens/daftar_catatan_screen.dart';

Future<void> main() async {
  // Wajib dipanggil karena kita menunggu proses async sebelum runApp().
  WidgetsFlutterBinding.ensureInitialized();

  // Memuat data locale agar paket intl bisa memformat tanggal
  // ke dalam Bahasa Indonesia (locale id_ID).
  await initializeDateFormatting('id_ID', null);

  runApp(const AplikasiCatatanHarian());
}

class AplikasiCatatanHarian extends StatelessWidget {
  const AplikasiCatatanHarian({super.key});

  @override
  Widget build(BuildContext context) {
    return MaterialApp(
      title: 'Catatan Harian',
      debugShowCheckedModeBanner: false,
      theme: ThemeData(
        colorScheme: ColorScheme.fromSeed(seedColor: Colors.teal),
        useMaterial3: true,
      ),
      home: const DaftarCatatanScreen(),
    );
  }
}
