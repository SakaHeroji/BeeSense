---
type: index
tags: [beesense, dashboard]
---

# BeeSense

[[Arsitektur BeeSense]] · [[Dataset Dashboard]] · [[Menjalankan BeeSense]] · [[Metodologi Machine Learning Social NLP]]

[[Crawler Selenium]] menjelaskan crawler Chrome baru dengan kontrak Excel yang sama.

[[PRD Frontend Crawler]] merinci rencana ReactJS dengan dua menu: Crawler Otomatis dan Crawler Manual untuk URL/data survei. [Kumpulan PRD](../../PRD/README.md) memisahkan frontend, backend, dan machine learning; API/survei pada PRD masih merupakan rencana pengembangan.

[[Frontend React Crawler]] tersedia di `Crawler/Frontend`: UI otomatis/manual, monitor, survei, dan dataset dengan adapter simulasi serta kontrak API. Tujuh sumber tersedia di UI/simulasi dengan tema putih–oranye dan teks hitam minimum 13 px. Backend akuisisi web dan lima adapter sosial tambahan masih perlu dibuat; mode simulasi tidak menjalankan crawling nyata.

[Buka dashboard](http://127.0.0.1:8501) · [README](../../README.md) · [Graf kode](../graph.html) · [Laporan Graphify](../GRAPH_REPORT.md) · [[graph.canvas|Canvas arsitektur]]

Vault memuat alur akuisisi → pemeriksaan ID/checksum → workbook gabungan → training → dashboard. Tiga workbook diterbitkan bersama run aktif dan empat snapshot NLP sebelumnya. Bundle akuisisi lokal tetap tersedia untuk audit.

Statistik graf, cohesion, biaya token dan keterbatasan ekstraksi tersedia pada [laporan aktif](../GRAPH_REPORT.md). [[Crawler Selenium]] menghubungkan backend browser baru dengan exporter dan kontrak Excel yang dipertahankan.

Retrain gabungan aktif: **20 topik**, rata-rata **c_v 0,4720**, ambang rata-rata **0,4 tercapai**. 7/20 topik masih <0,4 individual. [[Dataset Dashboard]] dan [[Metodologi Machine Learning Social NLP]] memuat sumber/metode/batasnya.

[[Crawling 1000 Post Baru]]: target 1.000 post baru per platform dalam 3 jam, pengecualian ID dataset lama dan CAPTCHA manual di Chrome. Hasil: YouTube 1.188 post/300 qualified dan Reddit 98/58; target qualified belum tercapai. Hasil digabung dengan baseline dan dashboard memakai snapshot baru.
