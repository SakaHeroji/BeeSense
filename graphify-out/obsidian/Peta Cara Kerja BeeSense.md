---
type: architecture
tags: [beesense, floorplan, alur-kerja]
---

# Cara kerja BeeSense

BeeSense mengumpulkan percakapan media sosial, memilih kalimat yang sesuai dengan konteks pendidikan, lalu mengelompokkannya menjadi topik yang bisa ditelusuri di dashboard. Berkas hasil menghubungkan tahap-tahap ini. Saat ini operator masih menjalankan pengambilan, penggabungan, penyaringan, dan pelatihan lewat perintah terpisah.

[Buka floor plan interaktif](http://127.0.0.1:4378). Peta lokal berada di `floorplan/index.html`; susunannya ada di `floorplan/architecture.json` dan penjelasan tiap berkas di `floorplan/descriptions/`. Folder ini diabaikan Git. Peta mencakup 139 berkas, semuanya sudah diberi nama dan penjelasan berbahasa Indonesia. Tiga alur dan tujuh pemberhentian pengantar membantu pembaca mengikuti pekerjaan dari awal.

## Layar crawler dan proses pengambilan

Layar pada `Crawler/Frontend/` menyediakan menu otomatis, masukan URL manual, impor survei, rincian pekerjaan, serta penjelajah dataset. Mode pengembangannya memakai simulasi. Penghubung permintaan ke server sudah disiapkan di `Crawler/Frontend/src/shared/api.ts`, tetapi server penerima permintaannya belum dibuat dalam repository ini. Menekan tombol pada mode contoh tidak menjalankan crawler Python.

Pengambilan nyata berada di `Crawler/Backend/social_crawler.py`. Program ini membaca pengaturan pencarian, memilih sumber yang aktif, mengatur batas waktu dan jeda, serta menghindari post yang sudah ada. YouTube memakai yt-dlp, Reddit memakai Reddrix, Instagram memakai Instaloader dengan penyesuaian permintaan web, dan X memakai Scweet. Pilihan pengambilan lama tetap tersedia untuk kebutuhan tertentu. Sumber masih bisa membatasi akses atau meminta verifikasi; jeda program tidak menjamin pembatasan tidak akan muncul.

`Crawler/Backend/social_export.py` menyamakan hasil ke Excel dan catatan audit. Identitas post, komentar, hubungan balasan, serta asal pengambilan disimpan agar hasil bisa digabung dan diperiksa.

## Dari hasil crawling menjadi topik

`scripts/merge_social_datasets.py` menggabungkan workbook berdasarkan ID asli post atau komentar. Teks yang sama dari dua record berbeda tetap dipertahankan. Dataset sumber yang aktif berisi 34.764 record unik dari empat platform dan tidak memiliki ID ganda.

`scripts/filter_context_relevance.py` menjalankan `ContextRelevanceFilter` dari `MachineLearning/context_relevance.py`. Kalimat dibandingkan dengan contoh konteks pendidikan, interaksi umum, dan pembahasan di luar lingkup. `LocalSemanticBackend` pada `MachineLearning/relevance_semantic.py` membandingkan maknanya secara lokal. Konteks post atau balasan induk hanya dipakai jika hubungan sumbernya terverifikasi. Kalimat yang meragukan tetap dicatat tetapi tidak masuk clustering. Ambangnya belum dikalibrasi dengan label manusia.

Hasil terakhir menerima 10.496 dari 53.332 kemunculan kalimat. `MachineLearning/social_nlp.py` mengelompokkan 10.380 kalimat unik yang lolos menjadi 20 topik. Rata-rata coherence adalah 0,4733391691; tujuh topik individual masih di bawah 0,4. Nilai ini mengukur keselarasan istilah, bukan akurasi relevansi. Perbedaan skor sebelum dan sesudah penyaringan tidak menjadi bukti kenaikan kualitas karena korpusnya berbeda.

## Peran Gemini

`MachineLearning/topic_narratives.py` meminta satu kalimat topik dan paragraf deskripsi dari Gemini, dengan sepuluh keyword c-TF-IDF dan sepuluh kalimat representatif untuk tiap topik. Gemini menjelaskan kelompok yang sudah terbentuk; ia tidak memilih anggota kelompok. `scripts/generate_topic_narratives.py` juga dapat menambahkan deskripsi ke model yang sudah selesai tanpa mengulang clustering.

CSV tersimpan di `outputs/nlp_20261102_relevance_topics20_gemini_02/topic_narratives.csv`. Model, keputusan relevansi, berkas sumber, dan checksum tetap tersedia untuk pemeriksaan. Password, sesi akun, serta API key berada di penyimpanan lokal yang diabaikan Git.

## Membaca dan membandingkan hasil

`streamlit_apps.py` membuka tampilan pada `Dashboard/app.py`. Dashboard membaca hasil tersimpan, sehingga membuka halaman atau mengganti filter tidak memulai crawling, training, maupun permintaan Gemini.

`config/dashboard.json` menetapkan dua model untuk radio pembandingan. Sebelum penyaringan memuat 53.332 kemunculan kalimat dengan rata-rata coherence 0,4243; setelah penyaringan memuat 10.496 kemunculan dengan rata-rata 0,4733. Kedua model mempunyai 20 topik dan deskripsi Gemini. Snapshot lama dipertahankan agar hasil bisa dibandingkan atau dikembalikan.

Kode dan hasil tersaring dipublikasikan melalui commit `778cb81`; perbaikan radio Cloud berada di `3987e04`. [Dashboard online](https://beesense.streamlit.app/) sudah direstart dan kedua pilihan radio sudah dicoba langsung. Pemeriksaan GitHub memakai Python 3.12 dan 3.14. Tidak diperlukan migrasi database aplikasi; Docker lokal belum dapat diuji karena daemon tidak aktif.

## Yang perlu diperhatikan dari peta

Peta tidak menemukan masalah tingkat tinggi pada pemeriksaan otomatisnya. Enam berkas besar mendapat catatan tingkat menengah: pengolah NLP, dashboard, pengatur crawler, crawler Reddit lama, pengambil Instagram lama, dan pengambil X. Masing-masing menampung banyak tugas; pemisahan menurut tanggung jawab dapat dipertimbangkan pada pekerjaan berikutnya. Catatan otomatis ini bukan audit keamanan lengkap.

Sambungan impor dan alamat layanan pada peta berasal dari pemeriksaan kode. Hubungan perpindahan berkas ditambahkan dari alur yang benar-benar dijalankan. Tidak ada rute server Python yang terdeteksi; alamat permintaan pada layar crawler merupakan persiapan sambungan yang belum tersedia.

[[Relevansi Konteks 20261102]] · [[Arsitektur BeeSense]] · [[Metodologi Machine Learning Social NLP]] · [[HOME]]
