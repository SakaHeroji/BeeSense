# Uji Pyktok 3 November 2026

**Gagal mencapai target: 0/500 post, 0 komentar, 0 balasan.**
Status akhir `PARTIAL`; operasi berhenti dengan `CLIENT_UPGRADE_REQUIRED`, alasan
`pyktok_keyword_page_has_no_embedded_results`. Durasi akuisisi **2,69 detik**.
Halaman search mengembalikan HTTP200 dan JSON hydration, tetapi tanpa objek video.
Ini bukan keberhasilan crawling selama 30 menit dan tidak membuktikan token kedaluwarsa.

- Backend: dfreelon/Pyktok 0.0.31, TikTokCrawler 1.3.0, metode `pyktok_public_web`.
- TikTokApi 7.3.3 dan Playwright 1.64.1 masih menjadi backend browser transitif
  Pyktok; browser tidak dibuka pada trial ini karena tahap keyword HTTP belum menghasilkan kandidat.
- Mulai: **3 November 2026, 14:04:53 WIB** / 07:04:53 UTC.
- Perintah: `.venv-tiktok/bin/python -m Crawler.Backend.tiktok_crawler --target-posts 500 --total-seconds 1800`.
- Target 500 dan batas 1.800 detik hanya override CLI; JSON utama tetap 1.000/null.
- Query pertama: `biaya kuliah beasiswa`, dari 25 query universal; tidak diganti menjadi hashtag.
- Include: `kuliah`, `kampus`, `universitas`, `beasiswa`, `jurusan`; exclude tetap dari konfigurasi.
- Rentang publikasi: 27 Oktober 2025 10:17 WIB sampai sebelum 27 Oktober 2026 10:17 WIB.
- Telemetri: satu request, satu HTTP200, nol kandidat tidak valid, nol post diperoleh.
- Auth dibaca dari file lokal dan tidak diubah. Tidak memakai cookie profil browser,
  login otomatis, proxy/rotasi akun atau solver CAPTCHA.

Pyktok tidak mempunyai pencarian keyword. Bridge BeeSense memakai parser
`alt_get_tiktok_json()` / `get_tiktok_json()` pada satu halaman search; tidak ada
pagination keyword. Halaman valid tanpa objek video menyebabkan penghentian yang
eksplisit. Keterbatasan ini berbeda dari ACCESS_BLOCKED pada percobaan sebelumnya.
Hashtag opsional memakai fungsi Pyktok yang tersedia, tetapi tidak dijalankan
sebagai pengganti query diam-diam pada trial ini.

Bundle: `output/crawler_runs/social_20261103T070453Z_d6b0839f/`.
`social_data.xlsx` valid, sheet `Data`, sepuluh kolom header, **tanpa baris data**.
`dataset.xlsx`, JSONL, manifest checksum dan summary menyimpan audit kegagalan.
Run kosong tidak memublikasikan partisi tanggal kosong dan tidak menulis ulang
arsip lama; tidak ada ID baru atau duplikat yang ditambahkan.

Pengujian offline memvalidasi parser Pyktok asli dengan respons fixture, sesi,
native ID, statistik, filter tanggal/keyword, komentar/balasan dan timeout. Fixture
tidak dianggap hasil live dan tidak masuk arsip nyata. No migration required.
Docker belum diverifikasi karena daemon lokal tidak tersedia.

Riwayat gagal: [Omkar](TIKTOK_TRIAL_20261103.md),
[MEOMcGill/PyTok](TIKTOK_PYTOK_TRIAL_20261103.md),
[TikTok-Api langsung](TIKTOK_API_TRIAL_20261103.md).
