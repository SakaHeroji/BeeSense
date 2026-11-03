# Uji PyTok 3 November 2026 — riwayat

**Gagal mencapai target: 0/500 post, 0 komentar dan 0 balasan.**
Status akhir `PARTIAL`, alasan `CAPTCHA_REQUIRED`, durasi akuisisi 159,81 detik.
Batas yang diminta 1.800 detik tidak dipakai penuh karena CAPTCHA menghentikan run.

Backend percobaan: MEOMcGill/PyTok 0.3.0 revision
`e6ad007bc66919e03c63334c75b985ed3e1daadd`, Camoufox 0.5.9 dengan browser
158.0.1-beta.41. Dimulai 3 November 2026 pukul 13:28:41 WIB.

Perintah: `.venv-tiktok/bin/python -m Crawler.Backend.tiktok_crawler --target-posts 500 --total-seconds 1800`.
Keyword, 25 query dan tanggal publikasi diwarisi dari JSON universal.
Pencarian pertama timeout setelah sekitar 91 detik; worker ditutup. Pencarian
kedua pada worker baru berhenti ketika CAPTCHA muncul. Tidak ada solver otomatis
atau pergantian akun/IP setelah CAPTCHA. Empat HTTP200 tercatat pada worker akhir;
jumlah request worker yang timeout tidak terakumulasi, jadi angka empat bukan
total pasti seluruh run. CAPTCHA tidak membuktikan token kedaluwarsa.

Bundle lokal: `output/crawler_runs/social_20261103T062841Z_36c5ff66/`.
Excel `social_data.xlsx` hanya berheader; `dataset.xlsx`, JSONL, summary dan manifest
menyimpan audit. Tidak ada partisi TikTok nyata atau duplikasi ID yang ditambahkan.
Auth lokal tidak diubah. Default utama tetap target 1.000, durasi dan cap komentar
`null`; tidak dibuat preset JSON tambahan.

Pengguna kemudian mengembalikan backend ke davidteather/TikTok-Api. PyTok dan
Camoufox tidak lagi menjadi dependency aktif. Ini hasil uji nyata, terpisah dari
fixture sintetis pengujian offline.
