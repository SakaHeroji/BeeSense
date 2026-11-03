---
type: architecture
tags: [beesense, crawler, tiktok, pytok]
source_url: https://github.com/MEOMcGill/pytok
captured_at: 2026-11-03
---

# TikTokCrawler PyTok — riwayat

Pengguna mengembalikan backend ke [[TikTokCrawler TikTok-Api]] setelah uji ini gagal pada CAPTCHA.

Backend percobaan `TikTokCrawler` 1.1.0 pada SocialCrawler 1.10 memakai
MEOMcGill/PyTok revision `e6ad007bc66919e03c63334c75b985ed3e1daadd` (0.3.0) dan
Camoufox 0.5.9. Dependency dipasang dari URL Git yang dipin; paket PyPI dengan nama
`pytok` adalah proyek berbeda. Lisensi sumber menyatakan PolyForm Noncommercial
1.0.0 AND MIT; provenance ada di `Crawler/Backend/Tiktok/PYTOK.md`.

[[Konfigurasi Universal Social Crawler]] tetap menjadi satu file pengaturan.
Query pendidikan, tanggal publikasi, include/exclude serta target diwarisi;
`headless`, `cache_dir`, `hashtags` dan `auth_file` diatur pada `platforms.tiktok`.
Default 1.000 post/tanpa batas waktu dan cap komentar/balasan `null` tetap berlaku.
Override CLI 500/1.800 detik hanya untuk uji.

Worker proses terpisah memakai satu browser. msToken lokal dimasukkan sebagai
cookie domain TikTok sebelum navigasi pertama; tidak dibuat AccountsPool, login
otomatis atau rotasi akun. Solver CAPTCHA otomatis dinonaktifkan oleh wrapper;
CAPTCHA/login/penolakan akses menghentikan akuisisi. msToken bukan jaminan sesi
login penuh. Browser disimpan di cache khusus proyek supaya tidak mengubah cache
Camoufox proyek lain. File auth tidak diubah atau dimasukkan ke hasil/graph/image.

Pencarian video memakai halaman dan scroll PyTok; root gagal filter tidak mengambil
komentar. Iterator komentar dan pagination balasan memakai ID video asli. Data
dinormalisasi ke `ContentInput`/`Dataset`, statistik/relasi serta Excel bersama.
[[Output Social Media Per Tanggal]] menerima native ID TikTok tanpa duplikasi dan
tanggal transaksi crawling WIB. Run kosong hanya menghasilkan audit/Excel
berheader; fixture sintetis terpisah dari data nyata.

[[TikTokCrawler Omkar]] dan [[TikTok Uji 500 Post 20261103]] adalah percobaan lama
yang gagal. Hasil PyTok dicatat pada [[TikTok PyTok Uji 500 Post 20261103]].
[Panduan operasi](../../docs/crawler/TIKTOK_CRAWLER.md). No migration required.
Docker daemon tidak tersedia, sehingga build/runtime image belum diverifikasi.
