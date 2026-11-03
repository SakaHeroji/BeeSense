---
type: trial
tags: [beesense, crawler, tiktok, partial]
---

# TikTok Uji 500 Post 20261103

Uji [[TikTokCrawler Omkar]] dimulai 3 November 2026 pukul 13:01:30 WIB dengan target
500 post, batas 1.800 detik dan keyword/tanggal dari [[Konfigurasi Universal Social Crawler]].
Hasil nyata: **0/500 post, 0 komentar, 0 balasan; ACCESS_BLOCKED**.

TikTok menjawab satu request bootstrap dengan HTTP 200 tanpa data halaman yang
dapat diurai scraper. Akuisisi berhenti setelah 0,61 detik. Batas 30 menit tidak
dijalankan penuh; token yang tersedia bukan bukti akses berhasil maupun bukti
kedaluwarsa. Tidak ada pergantian IP/sesi atau retry untuk melewati penghalang.

Bundle `output/crawler_runs/social_20261103T060130Z_867806bb/` menyimpan
`social_data.xlsx` berheader dan audit lengkap termasuk summary dan manifest.
Tidak ada data TikTok yang ditambahkan ke arsip nyata. [[Output Social Media Per Tanggal]]
tetap memiliki 34.785 record unik dari platform sebelumnya, tanpa duplikasi ID.
File auth tetap lokal dan tidak berubah. Fixture pengujian diberi tanda sintetis
dan tidak dihitung sebagai data nyata.

[Laporan uji](../../docs/crawler/TIKTOK_TRIAL_20261103.md) memuat perintah dan batas
hasil. Konfigurasi utama tetap 1.000 post/tanpa batas durasi; tidak dibuat preset
JSON tambahan untuk percobaan.
