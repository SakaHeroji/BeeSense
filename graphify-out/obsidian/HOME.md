---
type: index
tags: [beesense, dashboard]
---

# BeeSense

## Peta cara kerja

[[Peta Cara Kerja BeeSense]] menjelaskan alur pengambilan, penyaringan, pembentukan topik, Gemini, dan dashboard dengan bahasa sehari-hari. [Floor plan interaktif lokal](http://127.0.0.1:4378) memuat 139 berkas dan tiga alur kerja. Layar crawler masih simulasi; proses pengambilan nyata berjalan melalui perintah Python.

[[TwitterCrawler Scweet]] menambahkan class X/Twitter mandiri dengan konfigurasi percobaan 30 menit dan kontrak Excel yang sama. Kini terhubung ke SocialCrawler 1.7.0 dengan preset Twitter-only 3 jam/1.000 post, penggabungan native ID, NLP dan dashboard. Hasil uji live dicatat pada catatan tersebut.

Eksperimen lokal baru: [[Relevansi Konteks 20261102]] menyaring 10.496/53.332 kemunculan kalimat, lalu membentuk 20 topik dengan mean c_v 0,473339 dan 20 deskripsi Gemini dari keyword serta kalimat representatif. [Dashboard eksperimen](http://localhost:8502) menyediakan pembandingan sebelum/sesudah. Snapshot tersaring ber-Gemini kini menjadi default repository untuk publikasi; snapshot sebelum penyaringan tetap dipertahankan untuk pembandingan dan rollback.

Arsip sebelum penyaringan: **34.764 record unik, 20 topik, rata-rata c_v 0.424321**, 20 kalimat/deskripsi Gemini dan Excel 48.850 pasangan topik–kalimat. Lihat [[Twitter 20 Topik 20261102]]; angka lain di bawah adalah riwayat.

[[InstaloaderCrawler]] menjadi backend Instagram default SocialCrawler 1.6.0; catatannya memuat patch GraphQL web pengguna,
uji Excel/dedup dan batas aksesnya. Detail hasil terbaru ada pada catatan tersebut.

[[InstagramCrawler instagrapi]] terintegrasi dalam SocialCrawler 1.5.1. Akuisisi dihentikan pengguna setelah HTTP 429; batch terbaru menyimpan 248 post/2.128 komentar. Dataset gabungan 33.034 record unik sudah dilatih menjadi 20 topik/c_v 0,4315, lengkap dengan CSV [[Topik Gemini]]. Publikasi GitHub mengikuti pemeriksaan release.

[[Arsitektur BeeSense]] · [[Dataset Dashboard]] · [[Menjalankan BeeSense]] · [[Metodologi Machine Learning Social NLP]]

[[Crawler Selenium]] menjelaskan crawler Chrome baru dengan kontrak Excel yang sama.

[[PRD Frontend Crawler]] merinci rencana ReactJS dengan dua menu: Crawler Otomatis dan Crawler Manual untuk URL/data survei. [Kumpulan PRD](../../PRD/README.md) memisahkan frontend, backend, dan machine learning; API/survei pada PRD masih merupakan rencana pengembangan.

[[Frontend React Crawler]] tersedia di `Crawler/Frontend`: UI otomatis/manual, monitor, survei, dan dataset dengan adapter simulasi serta kontrak API. Tujuh sumber tersedia di UI/simulasi dengan tema putih–oranye dan teks hitam minimum 13 px. UI masih memakai adapter simulasi; API frontend belum mengendalikan crawler. Backend CLI YouTube, Reddit, Instagram dan X tersedia; mode simulasi tidak menjalankan crawling nyata.

[Buka dashboard](http://127.0.0.1:8501) · [README](../../README.md) · [Graf kode](../graph.html) · [Laporan Graphify](../GRAPH_REPORT.md) · [[graph.canvas|Canvas arsitektur]]

Vault memuat alur akuisisi → pemeriksaan ID/checksum → workbook gabungan → training → dashboard. Workbook baseline, sumber gabungan, snapshot aktif dan arsip sebelumnya dipertahankan. Lima bundle Twitter 2 November ikut dipublikasikan; runtime/auth tetap lokal.

Statistik graf, cohesion, biaya token dan keterbatasan ekstraksi tersedia pada [laporan aktif](../GRAPH_REPORT.md). [[Crawler Selenium]] menghubungkan backend browser baru dengan exporter dan kontrak Excel yang dipertahankan.

Riwayat retrain gabungan: **20 topik**, rata-rata **c_v 0,4720**, ambang rata-rata **0,4 tercapai**. 7/20 topik masih <0,4 individual. [[Dataset Dashboard]] dan [[Metodologi Machine Learning Social NLP]] memuat sumber/metode/batasnya.

[[Crawling 1000 Post Baru]]: target 1.000 post baru per platform dalam 3 jam, pengecualian ID dataset lama dan CAPTCHA manual di Chrome. Hasil: YouTube 1.188 post/300 qualified dan Reddit 98/58; target qualified belum tercapai. Hasil digabung dengan baseline dan dashboard memakai snapshot baru.

[[RedditCrawler Reddrix]] kini menjadi backend Reddit default SocialCrawler 1.4.0, dengan YouTube yt-dlp dalam scheduler/bundle yang sama. Wrapper Reddit-only tetap tersedia; konfigurasi gabungan 3 jam dan percobaan 30 menit memakai display adaptif macOS/Linux. Percobaan sebelum integrasi selesai dengan 33 post/769 baris tanpa duplikasi baseline; integrasi tidak memulai crawl baru.

[[Struktur Proyek]] menjelaskan lokasi package, config, dependency, dokumentasi dan Docker setelah reorganisasi. Entry point Cloud tetap streamlit_apps.py di root. Verifikasi Docker pada catatan lama bersifat historis; image perubahan Twitter belum dibangun karena daemon lokal tidak aktif. Rincian ada di [[Menjalankan BeeSense]].

[[Topik Gemini]] menjelaskan sintesis satu kalimat/deskripsi dari 10 keyword c-TF-IDF per topik dan CSV model yang dibaca dashboard tanpa API pada rerun.

Model 30 Oktober sudah terverifikasi:33.034 record unik,20 topik/c_v 0,4315 danCSV 20 narasi [[Topik Gemini]]. [[Dataset Dashboard]] menyimpan perincian dan riwayat.

[[Instagram 500 Post 2 Jam]]: riwayat akuisisi Instagram dua jam dengan 324 ID baseline sebagai pengecualian. Snapshot Instagram dipertahankan sebagai arsip.

- [[Training Instagram 20 Topik]] — arsip model Instagram dan Excel kalimat anggota.
