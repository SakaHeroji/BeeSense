---
type: architecture
tags: [beesense, crawler, tiktok]
source_url: https://github.com/davidteather/TikTok-Api
captured_at: 2026-11-03
---

# TikTokCrawler TikTok-Api

Riwayat backend langsung davidteather/TikTok-Api, kini digantikan
[[TikTokCrawler Mandiri]] sesuai pilihan pengguna terbaru.
Class `TikTokCrawler` 1.2.0 terintegrasi dengan SocialCrawler 1.10.0; dependency
aktif TikTokApi 7.3.3, Playwright 1.64.1 dan openpyxl 3.1.5. Lisensi upstream MIT.
Provenance: `Crawler/Backend/Tiktok/TIKTOK_API.md`.

[[Konfigurasi Universal Social Crawler]] menyediakan keyword, queries, tanggal,
target 1.000 dan durasi/cap komentar `null`. `platforms.tiktok` menyediakan `browser`,
`headless`, `hashtags`, `urls` dan `auth_file`. Uji 500/1.800 detik memakai override
CLI. Pencarian keyword memakai search_type item yang eksperimental pada 7.3.3;
iterator hashtag didukung. Tidak mengganti query atau memperluas tanggal diam-diam.

Worker terpisah memakai satu browser per worker, msToken dari auth lokal sebelum
navigasi pertama, request timeout/pacing dan barrier terminal. Tidak ada login
otomatis, proxy, rotasi akun atau solver CAPTCHA. Token tidak masuk output/log/graph
dan auth tidak diubah. Baris parsial dipertahankan ketika deadline habis.

Post hasil pencarian dipakai kembali; root tidak lolos tanggal/keyword tidak
mengambil komentar. Semua komentar/balasan yang tersedia dipaginasi, balasan memakai
ID video yang benar dan cursor berulang dihentikan. Native ID string, statistik
post serta relasi memakai kontrak `ContentInput`/`Dataset` dan Excel bersama.
[[Output Social Media Per Tanggal]] menjaga deduplikasi lintas hari WIB; run kosong
menyimpan audit/Excel berheader tanpa menulis ulang arsip.

[[TikTok-Api Uji 500 Post 20261103]] gagal memperoleh post: ACCESS_BLOCKED setelah
33,27 detik, 0/500. [[TikTokCrawler Omkar]] dan [[TikTokCrawler PyTok]] adalah riwayat
percobaan yang juga gagal. [Panduan](../../docs/crawler/TIKTOK_CRAWLER.md).
No migration required. Dockerfile worker memasang Chromium, tetapi build/runtime
Docker belum diverifikasi karena daemon lokal tidak tersedia.
