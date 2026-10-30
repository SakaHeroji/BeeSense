---
type: index
tags: [beesense, dashboard]
---

# BeeSense

Snapshot aktif: **34.095 record, 20 topik, rata-rata c_v 0,43865**, dilengkapi 20 terjemahan/deskripsi [[Topik Gemini]] dan Excel 45.556 pasangan topik–kalimat. Lihat [[Training Instagram 20 Topik]] serta [[Dataset Dashboard]]. Catatan angka lain di bawah merupakan riwayat.

[[InstaloaderCrawler]] menjadi backend Instagram default SocialCrawler 1.6.0; catatannya memuat patch GraphQL web pengguna,
uji Excel/dedup dan batas aksesnya. Detail hasil terbaru ada pada catatan tersebut.

[[InstagramCrawler instagrapi]] terintegrasi dalam SocialCrawler 1.5.1. Akuisisi dihentikan pengguna setelah HTTP 429; batch terbaru menyimpan 248 post/2.128 komentar. Dataset gabungan 33.034 record unik sudah dilatih menjadi 20 topik/c_v 0,4315, lengkap dengan CSV [[Topik Gemini]]. Publikasi GitHub mengikuti pemeriksaan release.

[[Arsitektur BeeSense]] · [[Dataset Dashboard]] · [[Menjalankan BeeSense]] · [[Metodologi Machine Learning Social NLP]]

[[Crawler Selenium]] menjelaskan crawler Chrome baru dengan kontrak Excel yang sama.

[[PRD Frontend Crawler]] merinci rencana ReactJS dengan dua menu: Crawler Otomatis dan Crawler Manual untuk URL/data survei. [Kumpulan PRD](../../PRD/README.md) memisahkan frontend, backend, dan machine learning; API/survei pada PRD masih merupakan rencana pengembangan.

[[Frontend React Crawler]] tersedia di `Crawler/Frontend`: UI otomatis/manual, monitor, survei, dan dataset dengan adapter simulasi serta kontrak API. Tujuh sumber tersedia di UI/simulasi dengan tema putih–oranye dan teks hitam minimum 13 px. Backend akuisisi web dan lima adapter sosial tambahan masih perlu dibuat; mode simulasi tidak menjalankan crawling nyata.

[Buka dashboard](http://127.0.0.1:8501) · [README](../../README.md) · [Graf kode](../graph.html) · [Laporan Graphify](../GRAPH_REPORT.md) · [[graph.canvas|Canvas arsitektur]]

Vault memuat alur akuisisi → pemeriksaan ID/checksum → workbook gabungan → training → dashboard. Tiga workbook diterbitkan bersama run aktif dan empat snapshot NLP sebelumnya. Bundle akuisisi lokal tetap tersedia untuk audit.

Statistik graf, cohesion, biaya token dan keterbatasan ekstraksi tersedia pada [laporan aktif](../GRAPH_REPORT.md). [[Crawler Selenium]] menghubungkan backend browser baru dengan exporter dan kontrak Excel yang dipertahankan.

Riwayat retrain gabungan: **20 topik**, rata-rata **c_v 0,4720**, ambang rata-rata **0,4 tercapai**. 7/20 topik masih <0,4 individual. [[Dataset Dashboard]] dan [[Metodologi Machine Learning Social NLP]] memuat sumber/metode/batasnya.

[[Crawling 1000 Post Baru]]: target 1.000 post baru per platform dalam 3 jam, pengecualian ID dataset lama dan CAPTCHA manual di Chrome. Hasil: YouTube 1.188 post/300 qualified dan Reddit 98/58; target qualified belum tercapai. Hasil digabung dengan baseline dan dashboard memakai snapshot baru.

[[RedditCrawler Reddrix]] kini menjadi backend Reddit default SocialCrawler 1.4.0, dengan YouTube yt-dlp dalam scheduler/bundle yang sama. Wrapper Reddit-only tetap tersedia; konfigurasi gabungan 3 jam dan percobaan 30 menit memakai display adaptif macOS/Linux. Percobaan sebelum integrasi selesai dengan 33 post/769 baris tanpa duplikasi baseline; integrasi tidak memulai crawl baru.

[[Struktur Proyek]] menjelaskan lokasi package, config, dependency, dokumentasi dan Docker setelah reorganisasi. Entry point Cloud tetap streamlit_apps.py di root. Struktur Docker terbaru telah melewati build dan uji semua tampilan pada image bersih; rincian ada di [[Menjalankan BeeSense]].

[[Topik Gemini]] menjelaskan sintesis satu kalimat/deskripsi dari 10 keyword c-TF-IDF per topik dan CSV model yang dibaca dashboard tanpa API pada rerun.

Model 30 Oktober sudah terverifikasi:33.034 record unik,20 topik/c_v 0,4315 danCSV 20 narasi [[Topik Gemini]]. [[Dataset Dashboard]] menyimpan perincian dan riwayat.

[[Instagram 500 Post 2 Jam]]: run Instagram 2 jam, target 500 post baru; 324 ID baseline dikecualikan dan hasil akan digabung setelah verifikasi.

- [[Training Instagram 20 Topik]] — model terbaru 20 topik dan Excel seluruh kalimat anggota.
