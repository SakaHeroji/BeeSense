---
type: trial
tags: [beesense, crawler, tiktok, trial]
source_url: https://playwright.dev/python/docs/network
captured_at: 2026-11-03
---

# TikTok Mandiri Uji 500 Post 20261103

[[TikTokCrawler Mandiri]] diuji 3 November 2026 dengan target CLI 500 post dan
maksimum 1.800 detik, query pertama biaya kuliah beasiswa dari 25 query universal.
Tanggal dan keyword utama tidak diubah, JSON utama tetap 1.000/null.

**Kedua uji gagal 0/500**, 0 komentar/balasan. Headless mulai 14:20:13 WIB, 4,79
detik. Browser terlihat mulai 14:21:55 WIB, 11,05 detik. Status keduanya PARTIAL
/ ACCESS_BLOCKED. Dua HTTP200 per run; uji terlihat mencatat kategori dokumen dan
/api/search/ dengan reason native_api_empty_or_invalid_json. Tidak ada bukti
HTTP403/429 atau kesimpulan token kedaluwarsa/ban permanen pada trial ini.

Bundle `output/crawler_runs/social_20261103T072013Z_c6377d98/` dan
`output/crawler_runs/social_20261103T072155Z_70cc1150/` berisi Excel berheader tanpa
data dan audit checksum. Run kosong tidak memublikasikan partisi atau menulis
ulang arsip. Auth tidak diubah. Fixture browser lokal terpisah memvalidasi post,
komentar, balasan, statistik dan cookie sebelum navigasi; tidak masuk arsip nyata.

Laporan sumber `docs/crawler/TIKTOK_NATIVE_TRIAL_20261103.md`.
Riwayat sebelumnya [[TikTok Pyktok Uji 500 Post 20261103]] dan
[[TikTok-Api Uji 500 Post 20261103]] juga gagal. Backend mandiri belum berhasil
mengatasi penghalang akses live; tidak ada solver atau rotasi akun/IP.
