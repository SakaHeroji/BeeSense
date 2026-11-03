`# Cara BeeSense menyaring kalimat sebelum mencari topik

Penyaringan ini memilih kalimat yang membahas pendidikan tinggi dari hasil crawling. Kalimat yang lolos kemudian dikelompokkan menjadi 20 topik.

Prosesnya berjalan pada data yang sudah tersimpan. Operator menjalankan perintah penyaringan, menyimpan keputusannya, lalu menjalankan clustering dengan hasil tersebut. Crawler belum otomatis memanggil penyaring ini.

## 1. Tentukan pembahasan yang dicari

Keyword yang dipakai saat ini adalah **kuliah, kampus, universitas, beasiswa, dan jurusan**.

Dari keyword itu, lingkup pembahasannya ditetapkan: memilih kampus atau jurusan, biaya kuliah, beasiswa, penerimaan mahasiswa, pengalaman kuliah, serta pekerjaan setelah lulus.

Karena yang dicari adalah pembahasannya, kalimat seperti “UKT saya naik lagi semester ini” bisa berkaitan dengan lingkup tersebut walaupun tidak menyebut lima keyword tadi. Sebaliknya, kata “jurusan” dalam cerita perjalanan bus belum tentu berkaitan dengan pendidikan.

Keyword pencarian ini berbeda dari keyword c-TF-IDF yang muncul pada hasil topik. Keyword pencarian ditentukan sebelum penyaringan; keyword c-TF-IDF baru dihitung dari kelompok yang sudah terbentuk.

## 2. Siapkan contoh untuk membandingkan makna

Pengaturan di `config/context_relevance.json` menyediakan tiga kelompok contoh:

| Kelompok | Contoh dalam konfigurasi | Yang ingin dikenali |
|---|---|---|
| Relevan | “Bagaimana syarat pendaftaran beasiswa KIP Kuliah?” | Pembahasan dalam lingkup pendidikan tinggi |
| Interaksi umum | “Terima kasih kak atas informasinya.” | Ucapan, dukungan, atau tanggapan yang tidak menjelaskan persoalan pendidikan |
| Di luar lingkup | “Pertandingan sepak bola dan pemain favorit saya.” | Pembahasan lain |

Saat ini ada 24 contoh relevan, 14 contoh interaksi umum, dan 24 contoh di luar lingkup. Contoh-contoh ini menjadi pembanding bagi seluruh kalimat. Kita tidak perlu memberi label satu per satu pada semua komentar.

Setiap keyword wajib muncul sebagai kata utuh dalam setidaknya satu contoh relevan. Pemeriksaan ini mencegah keyword ditambahkan tanpa contoh pembahasan. Ia belum menjamin bahwa contoh yang dipilih sudah cukup baik.

Jika lingkup penelitian berubah, contoh pembandingnya juga perlu ditinjau. Mengganti daftar keyword saja tidak membuat penyaring memahami bidang baru. Dalam implementasi sekarang, perhitungan kemiripan memakai kalimat contoh; teks `scope` dan daftar keyword bukan prompt yang dibaca model untuk mengambil keputusan.

## 3. Pecah komentar menjadi kalimat

Program membaca workbook gabungan, lalu mengambil record berjenis komentar dan balasan. Teks post asal tetap disimpan untuk membantu membaca konteks.

Komentar yang berisi beberapa kalimat dipisah. Misalnya:

> Biaya kuliahnya naik lagi. Semoga tim bola saya menang malam ini.

Kedua kalimat dinilai secara terpisah. Lolosnya satu kalimat tidak otomatis meloloskan seluruh komentar.

Sebelum penilaian makna, program melewati teks kosong serta potongan yang tidak memenuhi batas minimal dua kata dan delapan karakter setelah dibersihkan. Potongan yang dilewati tetap dicatat. Posisi kalimat dalam teks asli, baris sumber, platform, dan URL juga disimpan.

Pada dataset 2 November 2026, tahap persiapan menghasilkan **53.332 kemunculan kalimat**, yang mewakili **52.450 teks unik**. Angka ini adalah jumlah kalimat, bukan jumlah post.

## 4. Hitung kemiripan kalimat dengan contoh

Model SBERT multibahasa mengubah kalimat menjadi deretan angka yang mewakili maknanya. Contoh pembanding pada langkah 2 diubah dengan model yang sama. Program kemudian menghitung kemiripannya menggunakan *cosine similarity*.

Untuk setiap kategori, program mengambil **nilai tertinggi terhadap satu contoh** di kategori tersebut. Jadi, sebuah kalimat mendapat tiga skor: relevan, interaksi umum, dan di luar lingkup. Skor ini tidak dijumlahkan menjadi 100% dan tidak menunjukkan peluang kebenaran.

Sebagai ilustrasi perhitungan, anggap hasilnya seperti ini. **Angka berikut adalah simulasi, bukan hasil pengukuran model terhadap kalimat tertentu.**

| Kategori | Skor |
|---|---:|
| Relevan | 0,67 |
| Interaksi umum | 0,18 |
| Di luar lingkup | 0,24 |

Pesaing terkuat kategori relevan adalah 0,24. Selisihnya menjadi `0,67 − 0,24 = 0,43`.

Model berjalan secara lokal. Bobot SBERT memakai model pralatih; penyaringan ini tidak melatih classifier baru dari label komentar pengguna dan tidak mengirim setiap komentar ke Gemini.

## 5. Periksa apakah makna kalimat sudah cukup jelas

Aturannya diperiksa dalam urutan berikut:

1. **Calon relevan:** skor relevan minimal **0,42**, dengan selisih minimal **0,035** dari kategori pesaing terkuat.
2. Jika syarat pertama tidak terpenuhi, pilih **interaksi umum** bila skornya minimal **0,42** dan lebih tinggi daripada kedua skor lain.
3. Jika kedua syarat tadi tidak terpenuhi, pilih **di luar lingkup** bila skornya minimal **0,42** dan lebih tinggi daripada kedua skor lain.
4. Jika belum memenuhi salah satu aturan, tandai **belum pasti**.

Pada simulasi langkah 4, skor relevan 0,67 dan selisih 0,43 memenuhi syarat awal. Namun, calon relevan masih melewati pemeriksaan kalimat pendek pada langkah berikutnya.

Skor tertinggi saja belum cukup. Misalnya, skor relevan 0,46 dan pesaing terkuat 0,45 hanya berselisih 0,01. Kalimat itu belum lolos sebagai relevan karena maknanya masih terlalu dekat dengan kategori lain.

## 6. Periksa lagi kalimat pendek yang maknanya belum kuat

Kalimat pendek sering bergantung pada percakapan sebelumnya. “Bisa sampai umur berapa?” dapat menanyakan batas usia beasiswa, tetapi juga dapat membahas hal lain.

Karena itu, calon relevan diubah menjadi **belum pasti** jika panjangnya paling banyak **14 kata** dan skor relevannya masih **di bawah 0,60**. Dalam pemeriksaan ini, kata dihitung dari pemisahan spasi.

Contoh simulasi: kalimat pendek memperoleh skor relevan 0,50 dengan selisih 0,36. Ia sudah memenuhi ambang awal 0,42, tetapi tetap membutuhkan pemeriksaan konteks karena skornya belum mencapai 0,60.

Kalimat pendek dengan skor relevan setidaknya 0,60 tidak terkena aturan tambahan ini, selama selisih skornya juga memenuhi syarat.

## 7. Cari konteks dari percakapan yang sama

Untuk kalimat yang belum pasti, program mencari post asal dan, jika tersedia, komentar induknya. Hubungannya dicocokkan melalui ID atau URL asli.

Komentar induk hanya dipakai jika catatan audit crawling mempunyai checksum yang cocok, teks target sesuai dengan data sumber, dan hubungan balasannya menunjuk percakapan yang sama. Parent yang hilang atau mempunyai hubungan bertentangan tidak ditebak dari kemiripan judul.

Pemeriksaan konteks hanya dijalankan jika seluruh syarat ini terpenuhi:

- Keputusan saat ini **belum pasti**.
- Kalimat paling banyak **14 kata**.
- Skor relevan dari kalimat itu sendiri minimal **0,22**.
- Ada teks post asal atau komentar induk yang tersedia melalui pencocokan sumber tadi.

Kalimat yang sudah diputuskan sebagai interaksi umum atau di luar lingkup tidak masuk pemeriksaan tambahan ini. Jadi, “terima kasih kak” yang sudah dikenali sebagai ucapan umum tidak diloloskan hanya karena muncul di bawah post beasiswa.

## 8. Nilai kalimat bersama konteksnya

Program menyusun satu teks berisi kalimat target, sampai 400 karakter awal komentar induk, dan sampai 650 karakter awal post asal. Teks gabungan ini dibandingkan lagi dengan tiga kelompok contoh.

Kalimat berubah menjadi relevan jika skor relevan kontekstual minimal **0,50** dan selisih terhadap pesaing terkuat minimal **0,035**. Jika tidak memenuhi keduanya, keputusan tetap **belum pasti**.

Sebagai contoh pembacaan konteks, pertanyaan “Bisa sampai umur berapa?” lebih mudah dipahami jika post asal menjelaskan pendaftaran beasiswa. Apakah contoh itu akhirnya lolos tetap bergantung pada skor model. Keberadaan kata “beasiswa” pada post tidak otomatis membuat semua balasannya relevan.

Konteks digunakan untuk memutuskan kelolosan. Kalimat yang nanti dikelompokkan tetap kalimat target aslinya; teks induk tidak ditambahkan sebagai isi kalimat clustering.

## 9. Simpan semua keputusan

Setiap kemunculan kalimat mendapat salah satu dari empat keputusan:

| Keputusan | Arti | Masuk clustering |
|---|---|---|
| `relevant` | Memenuhi aturan relevansi langsung atau dengan konteks | Ya |
| `generic` | Interaksi umum | Tidak |
| `irrelevant` | Pembahasan di luar lingkup | Tidak |
| `uncertain` | Bukti belum cukup atau konteks tidak menyelesaikan keraguan | Tidak |

Audit menyimpan kalimat, ID kemunculan, sumber, tiga skor awal, selisih skor, alasan keputusan, serta status penggunaan konteks dan skor relevan kontekstual jika diperiksa.

Penilaian dilakukan per kemunculan. Teks yang sama di dua percakapan dapat mempunyai keputusan berbeda karena konteksnya berbeda. Nilai kemiripan yang sama dapat digunakan ulang dari cache, tetapi pemeriksaan konteks tetap mengikuti masing-masing sumber.

## 10. Teruskan yang relevan ke clustering

Hasil penyaringan disimpan di folder baru. Program mencocokkan checksum workbook dan identitas kalimat sebelum memakai keputusan tersebut untuk memilih data training. Data sumber lengkap dan snapshot sebelum penyaringan tetap disimpan.

Hasil yang tersimpan pada 2 November 2026 adalah:

| Keputusan | Kemunculan kalimat |
|---|---:|
| Relevan | 10.496 |
| Interaksi umum | 18.990 |
| Di luar lingkup | 3.747 |
| Belum pasti | 20.099 |
| **Total** | **53.332** |

Dari 10.496 kemunculan yang lolos, terdapat **10.380 teks unik**. Teks unik ini menjadi masukan clustering; hubungan ke semua kemunculan yang lolos tetap dipertahankan. Setelah itu, UMAP, DBSCAN, penggabungan menjadi 20 topik, dan evaluasinya dijalankan kembali pada data tersaring.

Ambang relevansi di atas berbeda dari target coherence **0,4**. Coherence baru diperiksa setelah kelompok topik terbentuk. Ia mengukur keselarasan istilah dalam kelompok, bukan ketepatan keputusan penyaringan.

## Apa yang masih bisa keliru

Contoh pembanding dan ambang skor belum dikalibrasi dengan label manusia. Belum ada pengukuran precision atau recall untuk memastikan berapa banyak kalimat yang salah diterima atau terlewat. Jumlah 10.496 yang lolos adalah hasil aturan otomatis, bukan jumlah yang sudah dipastikan benar oleh penilai manusia.

Sindiran, singkatan, campuran bahasa, dan balasan yang sangat bergantung pada percakapan panjang dapat salah dibaca. Sebagian kalimat relevan juga mungkin tertahan sebagai belum pasti. Keputusan lengkap disimpan agar kasus seperti ini bisa diperiksa tanpa kehilangan sumbernya.

## Berkas untuk menelusuri prosesnya

- [Konfigurasi keyword, contoh, dan ambang](../../config/context_relevance.json).
- [Aturan keputusan dan pemeriksaan konteks](../../MachineLearning/context_relevance.py): `classify_many()` dan `build_units()`.
- [Perhitungan embedding dan kemiripan](../../MachineLearning/relevance_semantic.py): `LocalSemanticBackend`.
- [Perintah penyaringan dataset tersimpan](../../scripts/filter_context_relevance.py).
- [Pemilihan kalimat untuk clustering](../../MachineLearning/social_nlp.py): `prepare_excel()` dan `_apply_context_relevance()`.
- [Laporan hasil penyaringan 2 November 2026](../../outputs/relevance_20261102_01/relevance_report.json).
- [Panduan teknis dan cara menjalankan proses](CONTEXT_RELEVANCE.md).

Dokumen ini mengikuti kode, konfigurasi, dan laporan hasil yang tersedia pada 2 November 2026. Contoh penjelasan serta angka simulasi di dalamnya tidak berasal dari pengujian model baru.
