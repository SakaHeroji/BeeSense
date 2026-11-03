---
type: trial
tags: [beesense, crawler, tiktok, pyktok, trial]
source_url: https://github.com/dfreelon/pyktok
captured_at: 2026-11-03
---

# TikTok Pyktok Uji 500 Post 20261103

[[TikTokCrawler Pyktok]] diuji 3 November 2026 mulai 14:04:53 WIB.
Target CLI 500 post, maksimum 1.800 detik; konfigurasi utama tetap 1.000/null.
Query pertama `biaya kuliah beasiswa` dari 25 query bersama, dengan rentang tanggal
publikasi dan filter yang sama. Tidak mengubah keyword menjadi hashtag.

**Gagal: 0/500 post**, 0 komentar/balasan, durasi 2,69 detik. Satu request HTTP200
menghasilkan JSON hydration tanpa objek video. Status PARTIAL dengan stop reason
CLIENT_UPGRADE_REQUIRED / pyktok_keyword_page_has_no_embedded_results. Ini berbeda
dari [[TikTok-Api Uji 500 Post 20261103]] yang ACCESS_BLOCKED. Tidak ada kesimpulan
bahwa token kedaluwarsa; auth tidak diubah.

Bundle `output/crawler_runs/social_20261103T070453Z_d6b0839f/` berisi Excel header
sepuluh kolom tanpa data serta dataset/JSONL/manifest audit. Tidak ada partisi
tanggal kosong atau data sintetis yang ditambahkan ke arsip. Pyktok tidak memiliki
API keyword; bridge hanya membaca satu halaman embedded. Hashtag opsional tidak
dipakai sebagai fallback pada trial ini. Laporan sumber:
`docs/crawler/TIKTOK_PYKTOK_TRIAL_20261103.md`.
