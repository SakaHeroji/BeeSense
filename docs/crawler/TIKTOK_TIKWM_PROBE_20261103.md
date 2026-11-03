# Probe TikWM dari pengguna — 3 November 2026

**Uji awal gagal: 0 video dan 0 komentar diperoleh.**
Script `tiktok_probe.py` yang dilampirkan pengguna dijalankan tanpa modifikasi,
menggunakan Python dari `.venv-tiktok`. Request pencarian pertama menerima
**HTTP403**. Script mencetak `GAGAL pencarian: HTTP 403: ditolak / dibatasi oleh
penyedia layanan`, lalu berhenti dengan exit code **2**.

## Sumber dan perintah

File pengguna: `/Users/socs3/Downloads/tiktok_probe.py`.
SHA-256: `deda610b6236bef9a307b64e7b5a9b6390b94ccbf49584977ba710c5228f3797`.
File diperiksa sebelum eksekusi dan tidak diubah. Komentar/contoh pada file
merupakan isi dokumen; cakupan pekerjaan mengikuti permintaan pengguna untuk
mencoba file tersebut pada masalah crawler TikTok yang sedang dikerjakan.

```sh
.venv-tiktok/bin/python /Users/socs3/Downloads/tiktok_probe.py \
  --keyword 'biaya kuliah beasiswa' --videos 5 --comments 20 \
  --output /tmp/beesense-tikwm-probe.csv
```

Query diambil dari query pertama konfigurasi universal; target awal lima video
dan maksimum dua puluh komentar per video. Ini probe kecil, bukan pengujian 500
post selama 30 menit. Karena pencarian ditolak, tahap komentar tidak dijalankan
dan CSV tidak dibuat. Tidak ada data baru atau perubahan pada arsip Excel.

## Perbedaan jalur akuisisi

Script memakai `requests.Session` ke `https://www.tikwm.com/api/feed/search` dan
merencanakan komentar melalui `/api/comment/list`. Ini API layanan pihak ketiga,
bukan browser native BeeSense atau API resmi TikTok. Query publik dikirim ke
TikWM. Script tidak membaca `auth.json`; msToken, sessionid dan password tidak
dikirim. File auth tetap tidak berubah. Log lokal:
`/tmp/beesense-tikwm-probe.log`.

HTTP403 membuktikan bahwa request probe dari lingkungan ini ditolak, tetapi belum
mengidentifikasi apakah penolakan berasal dari aplikasi penyedia, proteksi
jaringannya, atau jalur jaringan lokal. Tidak disimpulkan bahwa token TikTok
kedaluwarsa, akun diblokir permanen, atau TikWM selalu gagal di semua lingkungan.
Tidak ada retry, rotasi akun/IP, pembelian API atau percobaan melewati challenge.

## Keputusan implementasi

Backend aktif tetap TikTokCrawler 2.0.0 / NativeTikTokClient dengan konfigurasi,
filter, deduplikasi native ID dan Excel bersama. Jalur TikWM belum diintegrasikan
ke runtime karena gagal pada uji akses pertama. Tidak ada perubahan kode aplikasi,
dependensi, konfigurasi, database, Docker atau layanan produksi pada percobaan ini.
No migration required. Uji runtime/crawler penuh tidak diulang untuk perubahan
laporan saja; bukti baru adalah eksekusi probe asli di atas.

Lihat [panduan aktif](TIKTOK_CRAWLER.md) dan
[uji browser native sebelumnya](TIKTOK_NATIVE_TRIAL_20261103.md).
