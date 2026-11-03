# Uji crawler TikTok mandiri — 3 November 2026

**Dua uji live gagal mencapai target: masing-masing 0/500 post**, 0 komentar dan
0 balasan. Backend mandiri tidak berhasil memperoleh data TikTok pada lingkungan
ini. Uji fixture browser berhasil, tetapi bukan hasil live.

| Mode | Mulai WIB | Durasi akuisisi | Hasil |
| --- | --- | --- | --- |
| Headless | 14:20:13 | 4,79 detik | PARTIAL / ACCESS_BLOCKED |
| Browser terlihat | 14:21:55 | 11,05 detik | PARTIAL / ACCESS_BLOCKED |

Keduanya menargetkan 500 post dengan maksimum 1.800 detik; tidak berjalan penuh
selama 30 menit karena barrier. Uji terlihat merupakan run pembanding terpisah,
bukan retry internal, rotasi akun/IP atau percobaan menyelesaikan CAPTCHA.

```sh
.venv-tiktok/bin/python -m Crawler.Backend.tiktok_crawler --target-posts 500 --total-seconds 1800
.venv-tiktok/bin/python -m Crawler.Backend.tiktok_crawler --headed --target-posts 500 --total-seconds 1800
```

Backend `TikTokCrawler` 2.0.0 / `BeeSenseNative:1.0.0;Playwright:1.64.1`.
Tidak memakai library TikTok pihak ketiga atau kode dari repo Chinel0 yang
pengguna batalkan. Query pertama tetap `biaya kuliah beasiswa` dari 25 query
konfigurasi universal. Include tetap `kuliah`, `kampus`, `universitas`, `beasiswa`,
`jurusan`, exclude tidak diubah. Tanggal publikasi tetap 27 Oktober 2025 10:17 WIB
sampai sebelum 27 Oktober 2026 10:17 WIB. JSON utama tetap target 1.000/null.

Masing-masing uji mencatat dua HTTP200 dan nol kandidat. Diagnostik uji terlihat
membedakan satu dokumen dan satu respons kategori `/api/search/`; reason spesifik
`native_api_empty_or_invalid_json`. Halaman terbuka, tetapi respons pencarian
kosong atau bukan JSON sehingga ditolak parser. Tidak ada bukti HTTP403/429 pada
kedua uji dan tidak disimpulkan bahwa token kedaluwarsa atau akun diblokir permanen.

Bundle headless: `output/crawler_runs/social_20261103T072013Z_c6377d98/`.
Bundle terlihat: `output/crawler_runs/social_20261103T072155Z_70cc1150/`.
Masing-masing `social_data.xlsx` valid dengan sheet `Data`, header sepuluh kolom,
tanpa baris data. Dataset/JSONL/manifest/summary menyimpan audit kegagalan. Run
kosong tidak memublikasikan partisi kosong atau menulis ulang arsip lama.
Auth tidak diubah atau diserialisasi ke artefak. Tidak ada data sintetis masuk arsip.

Fixture browser memakai respons lokal yang seluruhnya dicegat: tiga native ID
fixture (satu post, komentar, balasan), statistik play_count 123 dan cookie
sebelum navigasi tervalidasi. Ini hanya bukti pipeline browser/normalisasi bekerja.
Kontrol request, Retry-After/cooldown persisten, penolakan CAPTCHA, filter root,
ID unik serta hasil parsial timeout juga diperiksa secara offline.

No migration required; tidak menulis database atau konfigurasi produksi.
Docker belum diverifikasi karena daemon lokal tidak tersedia. Progres parsial
bisa diekspor, tetapi tidak ada resume cursor komentar persis. Cakupan komentar
antarmuka tidak dijamin lengkap dan keberhasilan akses live belum tercapai.
