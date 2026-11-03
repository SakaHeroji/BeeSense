---
type: index
tags: [beesense, dashboard]
---

# BeeSense

## Data dan konfigurasi yang dirapikan

[[Konfigurasi Universal NLP]] menjelaskan satu file NLP dan lima preset yang dihapus. [[Output Social Media Per Tanggal]] menghubungkan 34.785 ID unik pada empat platform dan sembilan partisi tanggal crawling WIB. Output standar crawler mengikuti struktur ini; bundle audit dan snapshot lama dipertahankan.

## Konfigurasi crawler

[[Frontend Social Media Per Platform]]: tujuh menu sosmed, konfigurasi dari JSON universal, Excel lokal default, pilihan PostgreSQL/keduanya dan hasil per tanggal eksekusi WIB. Layanan HTTP belum tersedia; UI lokal tetap simulasi berlabel. [[Migrasi Transaksi per Sosmed]] kini hanya frontend: tombol/review/progres di data tiap transaksi, statistik lengkap dan form akun/sesi opsional dengan tujuan config/auth.json. Menu Migrasi Excel/Crawler Manual serta utility backend migrasi sebelumnya sudah dihapus; file autentikasi dan database nyata tidak diubah.

[[Target 1000 Post Tanpa Batas Waktu]]: kelima platform aktif, minimal 1.000 post masing-masing, durasi dan kuota harian lokal nonaktif, seluruh komentar/balasan yang tersedia diambil tanpa cap. Filter root tetap berlaku; komentar tidak dibuang berdasarkan keyword root.

[[Konfigurasi Universal Social Crawler]]: edit satu `config/social_crawler.json` untuk keyword, query, periode, durasi, target, adapter dan flag aktif per platform. Delapan preset crawler duplikat sudah dihapus; runner mandiri mewarisi durasi file utama. Angka trial pada catatan lama adalah riwayat.

## Peta cara kerja

[[Peta Cara Kerja BeeSense]] menjelaskan alur pengambilan, penyaringan, pembentukan topik, Gemini, dan dashboard dengan bahasa sehari-hari. [Floor plan interaktif lokal](http://127.0.0.1:4378) memuat 139 berkas dan enam alur kerja. Layar crawler masih simulasi; proses pengambilan nyata berjalan melalui perintah Python.

[[Alur Clustering Sebelum dan Setelah Penyaringan]] memperlihatkan percabangan dari workbook yang sama: 52.450 teks unik tanpa mask atau 10.380 teks unik yang relevan, masing-masing melalui SBERT → UMAP → DBSCAN → Ward → 20 topik → evaluasi → Gemini → dashboard. Ketujuh platform ditampilkan; backend CLI kini tersedia untuk lima platform termasuk TikTok, sedangkan Threads/Facebook masih UI/rencana. Floorplan lama belum memuat integrasi TikTok. Di floorplan, pilih **Flows → 04** atau **05** untuk rincian clustering.

[[TwitterCrawler Scweet]] tersedia sebagai class mandiri dan backend SocialCrawler dengan kontrak Excel yang sama, penggabungan native ID, NLP dan dashboard. Konfigurasi sekarang memakai file universal; hasil trial 30 menit dan campaign tiga jam pada catatan tersebut merupakan riwayat.

Eksperimen lokal baru: [[Relevansi Konteks 20261102]] menyaring 10.496/53.332 kemunculan kalimat, lalu membentuk 20 topik dengan mean c_v 0,473339 dan 20 deskripsi Gemini dari keyword serta kalimat representatif. [Dashboard eksperimen](http://localhost:8502) menyediakan pembandingan sebelum/sesudah. Snapshot tersaring ber-Gemini kini menjadi default repository untuk publikasi; snapshot sebelum penyaringan tetap dipertahankan untuk pembandingan dan rollback.

Arsip sebelum penyaringan: **34.764 record unik, 20 topik, rata-rata c_v 0.424321**, 20 kalimat/deskripsi Gemini dan Excel 48.850 pasangan topik–kalimat. Lihat [[Twitter 20 Topik 20261102]]; angka lain di bawah adalah riwayat.

[[InstaloaderCrawler]] menjadi backend Instagram default SocialCrawler 1.6.0; catatannya memuat patch GraphQL web pengguna,
uji Excel/dedup dan batas aksesnya. Detail hasil terbaru ada pada catatan tersebut.

[[InstagramCrawler instagrapi]] terintegrasi dalam SocialCrawler 1.5.1. Akuisisi dihentikan pengguna setelah HTTP 429; batch terbaru menyimpan 248 post/2.128 komentar. Dataset gabungan 33.034 record unik sudah dilatih menjadi 20 topik/c_v 0,4315, lengkap dengan CSV [[Topik Gemini]]. Publikasi GitHub mengikuti pemeriksaan release.

[[Arsitektur BeeSense]] · [[Dataset Dashboard]] · [[Menjalankan BeeSense]] · [[Metodologi Machine Learning Social NLP]]

[[Crawler Selenium]] menjelaskan crawler Chrome baru dengan kontrak Excel yang sama.

[[PRD Frontend Crawler]] mencatat lingkup awal. Koreksi frontend 1.2 memakai tujuh menu sosmed, statistik serta migrasi pada transaksi; menu manual/survei tidak lagi menjadi fitur aktif. [Kumpulan PRD](../../PRD/README.md) memisahkan frontend, backend dan machine learning.

[[Frontend React Crawler]] tersedia di `Crawler/Frontend`: tujuh menu sosmed, monitor, statistik transaksi, migrasi inline dan akun/sesi opsional dengan adapter simulasi serta kontrak API. Tema putih–oranye, teks hitam minimum 12 px. UI masih memakai adapter simulasi; API frontend belum mengendalikan crawler. Backend CLI YouTube, Reddit, Instagram, X dan TikTok tersedia; mode simulasi tidak menjalankan crawling nyata.

[Buka dashboard](http://127.0.0.1:8501) · [README](../../README.md) · [Graf kode](../graph.html) · [Laporan Graphify](../GRAPH_REPORT.md) · [[graph.canvas|Canvas arsitektur]]

Vault memuat alur akuisisi → pemeriksaan ID/checksum → workbook gabungan → training → dashboard. Workbook baseline, sumber gabungan, snapshot aktif dan arsip sebelumnya dipertahankan. Lima bundle Twitter 2 November ikut dipublikasikan; runtime/auth tetap lokal.

Statistik graf, cohesion, biaya token dan keterbatasan ekstraksi tersedia pada [laporan aktif](../GRAPH_REPORT.md). [[Crawler Selenium]] menghubungkan backend browser baru dengan exporter dan kontrak Excel yang dipertahankan.

Riwayat retrain gabungan: **20 topik**, rata-rata **c_v 0,4720**, ambang rata-rata **0,4 tercapai**. 7/20 topik masih <0,4 individual. [[Dataset Dashboard]] dan [[Metodologi Machine Learning Social NLP]] memuat sumber/metode/batasnya.

[[Crawling 1000 Post Baru]]: target 1.000 post baru per platform dalam 3 jam, pengecualian ID dataset lama dan CAPTCHA manual di Chrome. Hasil: YouTube 1.188 post/300 qualified dan Reddit 98/58; target qualified belum tercapai. Hasil digabung dengan baseline dan dashboard memakai snapshot baru.

[[RedditCrawler Reddrix]] kini menjadi backend Reddit default SocialCrawler 1.4.0, dengan YouTube yt-dlp dalam scheduler/bundle yang sama. Wrapper Reddit-only tetap tersedia dan mewarisi durasi file universal; display adaptif macOS/Linux tetap berlaku. Percobaan sebelum integrasi selesai dengan 33 post/769 baris tanpa duplikasi baseline; integrasi tidak memulai crawl baru.

[[Struktur Proyek]] menjelaskan lokasi package, config, dependency, dokumentasi dan Docker setelah reorganisasi. Entry point Cloud tetap streamlit_apps.py di root. Verifikasi Docker pada catatan lama bersifat historis; image perubahan Twitter belum dibangun karena daemon lokal tidak aktif. Rincian ada di [[Menjalankan BeeSense]].

[[Topik Gemini]] menjelaskan sintesis satu kalimat/deskripsi dari 10 keyword c-TF-IDF per topik dan CSV model yang dibaca dashboard tanpa API pada rerun.

Model 30 Oktober sudah terverifikasi:33.034 record unik,20 topik/c_v 0,4315 danCSV 20 narasi [[Topik Gemini]]. [[Dataset Dashboard]] menyimpan perincian dan riwayat.

[[Instagram 500 Post 2 Jam]]: riwayat akuisisi Instagram dua jam dengan 324 ID baseline sebagai pengecualian. Snapshot Instagram dipertahankan sebagai arsip.

- [[Training Instagram 20 Topik]] — arsip model Instagram dan Excel kalimat anggota.

[[TikTokCrawler Mandiri]] menjadi backend TikTok aktif: Playwright tanpa SDK TikTok, hydration dan respons UI, pacing adaptif serta Retry-After persisten. [[TikTokCrawler Pyktok]], [[TikTokCrawler TikTok-Api]], [[TikTokCrawler Omkar]] dan [[TikTokCrawler PyTok]] adalah riwayat.

[[TikTok Mandiri Uji 500 Post 20261103]] — gagal 0/500 pada headless (4,79 detik) dan terlihat (11,05 detik), ACCESS_BLOCKED karena respons search kosong/bukan JSON. Fixture browser terpisah lulus, bukan hasil live. Sebelumnya [[TikTok Pyktok Uji 500 Post 20261103]] gagal tanpa objek video dan [[TikTok-Api Uji 500 Post 20261103]] gagal ACCESS_BLOCKED.

[[TikWM Probe TikTok 20261103]] — script pengguna diuji dengan query bersama,
target awal lima video dan dua puluh komentar per video. Gagal pada pencarian
pertama HTTP403, tanpa data; [[TikTokCrawler Mandiri]] tetap backend aktif.


[[TikTok Chrome Uji 20261103]] — tab Chrome pengguna yang sudah login berhasil
membaca1post dan10komentar ber-ID asli. Target500belum tercapai dan komentar belum
lengkap. ChromeCaptureWorker hanya mengimpor tangkapan; akuisisi masih dibantu agen
browser terhubung. Chromium manual dibatalkan sesuai koreksi pengguna.

[[TikTok Chrome Live Connector]]: uji ekstensi terpasang menghasilkan13post,
93komentar,261balasan (367IDunik) dalam656,6detik; target500belum tercapai.
Arsip35197IDunik tanpa duplikasi. Crawler2.5.0/Connector1.1.0 memperbaiki idle
pagination komentar dan balasan;39tesPython+10bridge+10Node lulus. Uji live baru
tidak dijalankan; crawler dihentikan sesuai permintaan. Reload ekstensi sebelum
run berikutnya. Streamlit tidak diredeploy; publikasi memakai branch terpisah.
