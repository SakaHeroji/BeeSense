# Uji TikTok 3 November 2026

Hasil: **PARTIAL — ACCESS_BLOCKED**, **0/500 post**, 0 komentar dan 0 balasan.
Batas durasi dikonfigurasi 1.800 detik; proses akuisisi berhenti setelah 0,61 detik
karena TikTok tidak memberikan data halaman bootstrap yang dapat dibaca scraper.
Ini bukan uji sukses selama 30 menit dan bukan bukti token kedaluwarsa.

- Waktu mulai: 3 November 2026, 13:01:30 WIB / 06:01:30 UTC.
- Backend: omkarcloud/tiktok-scraper, revision `683959302488fd773b56e2cf737e591bf12aa4be`.
- Runtime: Python 3.12.0, curl_cffi 0.14.0, openpyxl 3.1.5.
- Perintah: `.venv-tiktok/bin/python -m Crawler.Backend.tiktok_crawler --target-posts 500 --total-seconds 1800`.
- Query berasal dari 25 query konfigurasi universal. Query pertama: `biaya kuliah beasiswa`.
- Include: `kuliah`, `kampus`, `universitas`, `beasiswa`, `jurusan`.
- Rentang publikasi diwarisi: 27 Oktober 2025 10:17 WIB sampai sebelum 27 Oktober 2026 10:17 WIB.
- Target 500 dan 1.800 detik hanya override run ini. JSON utama tetap target 1.000 dan `total_seconds: null`.
- Satu request jaringan tercatat, HTTP 200; proses berhenti sebelum memperoleh kandidat.
- msToken tersedia dan dibaca dari entri TikTok di auth lokal. File auth tidak berubah.
- Tidak mengganti IP/sesi atau mengulangi crawl setelah penghalang akses.

Bundle audit lokal:
`output/crawler_runs/social_20261103T060130Z_867806bb/`.
`social_data.xlsx` dapat dibuka dan hanya memuat header; `dataset.xlsx`,
`Runs.jsonl`, `Sources.jsonl`, `manifest.json` dan `summary.json` menjelaskan
ketidakberhasilan ini. Tidak ada baris nyata TikTok atau partisi TikTok harian.
Arsip platform sebelumnya tetap memiliki 34.785 record unik dan 0 duplikasi ID.

Pada versi awal trial, organizer memverifikasi kembali arsip lama meski hasil
TikTok kosong. Implementasi akhir melewati publikasi organizer untuk run kosong
agar percobaan yang diblokir tidak menulis ulang arsip tanpa data baru.

Pengujian offline memverifikasi alur berhasil menggunakan fixture yang ditandai
sintetis. Hasil fixture bukan data TikTok nyata dan tidak dihitung menuju target.
