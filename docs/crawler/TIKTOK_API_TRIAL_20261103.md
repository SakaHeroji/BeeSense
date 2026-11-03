# Uji ulang TikTok-Api 3 November 2026

**Gagal mencapai target: 0/500 post, 0 komentar dan 0 balasan.**
Status akhir `PARTIAL`, alasan `ACCESS_BLOCKED`, durasi akuisisi **33,27 detik**.
TikTok mengembalikan respons pencarian kosong. Ini bukan uji sukses selama 30 menit.

- Backend aktif: davidteather/TikTok-Api, TikTokApi 7.3.3, Playwright 1.64.1, Chromium.
- Mulai: 3 November 2026, 13:38:13 WIB / 06:38:13 UTC.
- Perintah: `.venv-tiktok/bin/python -m Crawler.Backend.tiktok_crawler --target-posts 500 --total-seconds 1800`.
- Target 500 post dan batas 1.800 detik hanya override CLI; JSON utama tetap 1.000/null.
- Pencarian pertama: `biaya kuliah beasiswa`, dari 25 query universal.
- Include: `kuliah`, `kampus`, `universitas`, `beasiswa`, `jurusan`.
- Periode publikasi: 27 Oktober 2025 10:17 WIB sampai sebelum 27 Oktober 2026 10:17 WIB.
- Tiga respons HTTP200 tercatat; respons kosong dari endpoint pencarian menghentikan run.
- Token tersedia dan dipasang pada cookie TikTok; file auth tidak berubah. Tidak ada kesimpulan bahwa token kedaluwarsa.
- Tidak ada proxy/rotasi akun atau solver CAPTCHA; tidak ada retry setelah barrier.

Bundle lokal: `output/crawler_runs/social_20261103T063813Z_d46f8359/`.
`social_data.xlsx` valid dengan satu sheet `Data` dan header sepuluh kolom, tanpa
baris data. `dataset.xlsx`, `Runs.jsonl`, `Sources.jsonl`, `manifest.json` dan
`summary.json` menyimpan audit kegagalan. Tidak ada publikasi partisi kosong;
arsip lama tetap 34.785 native ID unik dan tanpa duplikasi.

Pencarian memakai `search.search_type(query, "item")`, yang memiliki parser video
di source 7.3.3 tetapi belum merupakan pencarian video yang didukung secara resmi.
Hashtag adalah opsi yang didukung dan tersedia dalam konfigurasi, tetapi tidak
diaktifkan sebagai fallback tersembunyi pada uji ini.

Hasil sebelumnya: [Omkar](TIKTOK_TRIAL_20261103.md),
[PyTok](TIKTOK_PYTOK_TRIAL_20261103.md). Keduanya tetap riwayat; implementasi aktif
sudah kembali ke TikTok-Api sesuai pilihan akhir pengguna.
