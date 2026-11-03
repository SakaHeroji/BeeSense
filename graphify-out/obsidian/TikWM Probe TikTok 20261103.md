---
type: trial
tags: [beesense, crawler, tiktok, tikwm, probe]
captured_at: 2026-11-03
---

# TikWM Probe TikTok 20261103

Pengguna memberikan tiktok_probe.py, SHA-256
`deda610b6236bef9a307b64e7b5a9b6390b94ccbf49584977ba710c5228f3797`.
File asli diperiksa dan dijalankan tanpa modifikasi pada 3 November 2026.

Script memakai requests ke TikWM API pihak ketiga untuk pencarian dan komentar,
bukan [[TikTokCrawler Mandiri]]. Query pertama konfigurasi bersama adalah biaya
kuliah beasiswa; probe meminta lima video dan maksimal dua puluh komentar per video.
Tidak mengirim msToken/sessionid/password dan tidak membaca atau mengubah auth.json.

**Gagal: 0 video, 0 komentar**, pencarian pertama HTTP403, exit code2. Tahap komentar
belum berjalan dan CSV tidak dibuat. Ini bukan uji500post/30menit. Tidak ada data
baru pada arsip atau perubahan dependensi/konfigurasi aplikasi. HTTP403 tidak
menentukan asal penolakan atau membuktikan token kedaluwarsa maupun ban permanen.

Backend aktif tetap [[TikTokCrawler Mandiri]] karena jalur TikWM belum lolos probe.
Laporan sumber `docs/crawler/TIKTOK_TIKWM_PROBE_20261103.md`; riwayat terkait
[[TikTok Mandiri Uji 500 Post 20261103]]. No migration required; tidak ada eksekusi
produksi atau perubahan Docker. Log probe lokal di /tmp/beesense-tikwm-probe.log.
