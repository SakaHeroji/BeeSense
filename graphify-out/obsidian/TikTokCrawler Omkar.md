---
type: architecture
tags: [beesense, crawler, tiktok]
source_url: https://github.com/omkarcloud/tiktok-scraper
captured_at: 2026-11-03
---

# TikTokCrawler Omkar — riwayat

Backend Omkar berikut merupakan implementasi awal yang sudah diganti; pilihan akhir adalah [[TikTokCrawler TikTok-Api]] setelah percobaan [[TikTokCrawler PyTok]]. Uji gagal tetap disimpan sebagai riwayat.

[[Konfigurasi Universal Social Crawler]] mengaktifkan TikTok sebagai platform
kelima pada SocialCrawler 1.10.0. Class `TikTokCrawler` dan worker proses terpisah
ada di `Crawler/Backend/tiktok_crawler.py`. Backend memakai sumber Omkar Cloud yang
dipin ke revision `683959302488fd773b56e2cf737e591bf12aa4be`, beserta lisensi MIT dan
catatan provenance. Tidak menggunakan TikTok-Api David Teather atau RapidAPI.

Pencarian video memakai `queries` universal; hashtag dan URL dapat ditambahkan.
Filter tanggal/keyword diterapkan pada root sebelum komentar diambil. Target
default 1.000 post, durasi `null`, dan semua cap komentar/balasan `null`. Uji terbatas
memakai override CLI agar tidak membuat JSON tambahan.

Worker membaca msToken dari satu entri TikTok di auth lokal, memakai satu sesi
langsung dan berhenti ketika TikTok menolak akses. Token tidak disimpan di log,
hasil, graph, atau image Docker. Pagination cursor, deadline, deduplikasi ID serta
baris parsial diuji secara offline. Statistik post dan relasi komentar/balasan
masuk kontrak audit bersama; Excel ringkas memakai sepuluh kolom yang sama.

[[Output Social Media Per Tanggal]] menerima platform TikTok melalui identitas
native video/komentar dan tanggal crawling WIB. Output berisi data berada di
`outputs/crawling/tiktok/YYYY-MM-DD/social_data.xlsx`; run kosong hanya menyimpan
bundle audit dan workbook berheader tanpa memublikasikan partisi kosong.

[Panduan lengkap](../../docs/crawler/TIKTOK_CRAWLER.md). [[TikTok Uji 500 Post 20261103]]
mencatat akses awal diblokir, bukan hasil target tercapai. Frontend dashboard masih
memakai simulasi; backend CLI ini tidak mengubah status integrasi API frontend.
No migration required. Dockerfile worker disediakan, build/runtime Docker belum
terverifikasi karena daemon lokal tidak tersedia.
