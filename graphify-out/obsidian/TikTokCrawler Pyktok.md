---
type: architecture
tags: [beesense, crawler, tiktok, pyktok]
source_url: https://github.com/dfreelon/pyktok
captured_at: 2026-11-03
---

# TikTokCrawler Pyktok

Riwayat `TikTokCrawler` 1.3.0 pada `SocialCrawler` 1.10.0 memakai
dfreelon/Pyktok 0.0.31, BSD-3-Clause. Berbeda dari [[TikTokCrawler PyTok]].
TikTokApi 7.3.3 dan Playwright 1.64.1 tetap dipin sebagai backend browser transitif.
Provenance: `Crawler/Backend/Tiktok/PYKTOK.md`.

[[Konfigurasi Universal Social Crawler]] tetap menyediakan query, keyword, tanggal,
target 1.000 post dan durasi/cap komentar null. Pyktok tidak mempunyai pencarian
keyword: bridge eksperimental membaca objek video dari JSON satu halaman search
melalui parser Pyktok, tanpa pagination keyword atau penggantian query menjadi
hashtag. Hashtag opsional memakai `get_video_urls()`; komentar memakai
`get_comments()`, balasan memakai transport browser transitif dengan ID video.

Satu worker memiliki sesi HTTP dan browser yang dibuka bila diperlukan. msToken
dibaca dari auth lokal ke cookie TikTok, tidak diubah atau diekspor. Tidak ada
ekstraksi cookie profil browser, login otomatis, proxy, rotasi akun atau solver.
Baris komentar dialirkan saat iterasi, sehingga hasil parsial tetap tersimpan.
Filter root diterapkan sebelum komentar. Native ID dan statistik memakai kontrak
bersama serta [[Output Social Media Per Tanggal]]; run kosong tidak menulis ulang arsip.

[[TikTok Pyktok Uji 500 Post 20261103]] gagal: **0/500**, 2,69 detik,
CLIENT_UPGRADE_REQUIRED karena JSON halaman keyword tidak memuat video.
[[TikTokCrawler TikTok-Api]] dan [[TikTokCrawler Omkar]] adalah riwayat sebelumnya.
No migration required; build/runtime Docker belum diverifikasi (daemon tidak aktif).

Backend ini sudah diganti [[TikTokCrawler Mandiri]]; Pyktok/TikTokApi tidak lagi
menjadi dependensi aktif crawler TikTok.
