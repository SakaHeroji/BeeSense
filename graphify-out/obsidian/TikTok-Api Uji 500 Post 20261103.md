---
type: trial
tags: [beesense, crawler, tiktok, partial]
---

# TikTok-Api Uji 500 Post 20261103

[[TikTokCrawler TikTok-Api]] diuji ulang 3 November 2026 pukul 13:38:13 WIB.
Target 500 post dalam maksimal 1.800 detik; hasil nyata **0/500 post, 0 komentar,
0 balasan**. Status `PARTIAL`, alasan `ACCESS_BLOCKED`, durasi 33,27 detik.
Respons pencarian kosong menghentikan run; tiga respons HTTP200 tercatat.

Keyword/query dan periode publikasi diwarisi dari [[Konfigurasi Universal Social Crawler]].
Pencarian video berkeyword pada API versi ini eksperimental. Token tersedia,
dipakai hanya pada TikTok dan tidak berubah; hasil ini tidak membuktikan token
kedaluwarsa. Tidak ada retry, proxy, rotasi akun atau solver CAPTCHA setelah barrier.

Bundle `output/crawler_runs/social_20261103T063813Z_d46f8359/` menyimpan
`social_data.xlsx` kosong berheader dan audit lengkap. [[Output Social Media Per Tanggal]]
tetap 34.785 record unik tanpa duplikasi, tanpa partisi TikTok kosong.
[Laporan](../../docs/crawler/TIKTOK_API_TRIAL_20261103.md).

Ini hasil akhir uji nyata setelah pengguna mengembalikan pilihan library dari
[[TikTokCrawler PyTok]]; fixture sintetis tidak dihitung sebagai keberhasilan.
