---
type: implementation
status: frontend-first
tags: [beesense, react, crawler, frontend]
---

# Frontend React Crawler

[Crawler/Frontend](../../Crawler/Frontend/README.md) memakai React, TypeScript, Vite, React Router dan TanStack Query. Tujuh menu sosmed adalah satu-satunya navigasi utama. Menu/route/form Crawler Manual dan Migrasi Excel terpisah sudah dihapus sesuai koreksi lingkup; frontend dikerjakan terlebih dahulu.

[[Frontend Social Media Per Platform]] memuat formulir, hasil transaksi menurut tanggal eksekusi WIB, statistik lengkap dan [[Migrasi Transaksi per Sosmed]]. Mulai crawling tetap membuka monitor job dengan progres, aktivitas, konfigurasi dan dataset.

Development memakai simulasi berlabel, tanpa crawling/database/file nyata. Build API tidak fallback ke demo. Typed adapter di api.ts hanya menyiapkan [kontrak HTTP](../../Crawler/Frontend/docs/API_CONTRACT.md); gateway HTTP dan worker dashboard belum tersedia. Python SocialCrawler tetap CLI/library; TikTok memiliki transport Chrome/plugin nyata yang belum terhubung ke gateway frontend.

Form akun & sesi opsional menyiapkan penyimpanan config/auth.json untuk Instagram, X, Threads dan Facebook. Session ID disembunyikan, tidak dikembalikan server, tidak disimpan ke URL/localStorage/bundle dan dibersihkan setelah simulasi simpan. Metadata username/hasSession berada di memori demo. Frontend tidak membaca atau menulis file auth.json asli. TikTok memakai sesi Chrome melalui [[Frontend TikTok Plugin Chrome]].

Tema: #FFFFFF/#FAFAFA, teks #000000, aksen #FF8A24, pilihan #FFF3E8, garis #E6DDD5. Plus Jakarta Sans; teks minimum 12 px, pendukung 13 px, body/input 15 px, input mobile 16 px. [Audit dan delivery](../../Crawler/Frontend/docs/DELIVERY.md) mencatat bukti dan batas.

Utility backend/SQL/CI/image migrasi Excel sebelumnya sudah dihapus. Tidak ada migrasi database baru atau perubahan data asli. Docker frontend non-root UID101/8080 tetap; daemon tidak aktif, revisi image belum dibangun. Runtime lokal tetap http://127.0.0.1:5173.

[[Frontend Social Media Per Platform]] · [[Migrasi Transaksi per Sosmed]] · [[Arsitektur BeeSense]] · [[HOME]]
