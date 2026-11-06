# Audit dan optimasi crawler X / Instagram — 6 November 2026

Backend aktif pada konfigurasi proyek adalah Scweet 5.8.2 untuk X dan
Instaloader 4.16 untuk Instagram. Perubahan ini mengurangi kerja yang tidak
diperlukan; jeda minimum request 5 detik, concurrency X=1, rate controller
Instaloader, kuota, sesi, serta penghentian login/challenge/429 dipertahankan.
Tidak ada rotasi akun/proxy, pengulangan login atau solver CAPTCHA baru.
Platform tetap dapat membatasi akses; optimasi ini tidak menjamin bebas blokir.

## Kelemahan yang dibuktikan dan perbaikan

| Area | Sebelumnya | Sekarang |
|---|---|---|
| Rentang pencarian X | Batas jam dibulatkan menjadi tanggal pada setiap jendela; satu hari dapat dicari ulang pada jendela berikutnya | Batas bawah kalender menjadi batas atas eksklusif jendela berikutnya; cakupan hari utuh terjaga dan filter timestamp root tetap tepat |
| Seleksi root X | Koordinator dapat mengambil replies sebelum root ditolak tanggal/keyword | Metadata root dari pencarian diperiksa dengan aturan ekspor yang sama sebelum operasi jaringan lanjutan |
| Seleksi root Instagram | Komentar dapat diminta sebelum root ditolak oleh selektor | Setelah metadata root terverifikasi, aturan tanggal/include/exclude yang sama dijalankan sebelum komentar |
| Iterator balasan Instagram | Konstruktor NodeIterator langsung meminta halaman pertama, termasuk saat replies akhirnya tidak digunakan | Konstruktor ditunda sampai balasan dikonsumsi; halaman embedded yang memiliki page_info/cursor asli dipakai melalui first_data |
| Urutan Instagram | Balasan induk pertama dapat mendahului halaman komentar utama berikutnya | Komentar utama dikumpulkan dahulu, baru balasan; cap global/per-parent dan native parent tetap berlaku |
| Cap dan payload Instagram | max_comments=0 masih dapat membuka iterator; halaman terakhir meminta jumlah cap total | Cap nol tidak membuka iterator; parameter first memakai sisa cap, maksimal 20 |
| Pagination web Instagram | Cursor berulang dapat dianggap selesai; cursor baru dengan ID duplikat bisa terus berjalan | Cursor hilang/berulang saat sumber mengklaim halaman lanjutan, atau dua halaman berturut tanpa ID baru, menghasilkan PARTIAL; baris yang sudah dikirim tetap dipertahankan |
| Gangguan server | 5xx jatuh sebagai error umum dan dapat diikuti operasi lain | SERVER_UNAVAILABLE menghentikan run pada kegagalan server pertama; jeda minimal 60 detik atau Retry-After yang lebih panjang |
| Cooldown Instagram antarrun | Proses baru tidak memiliki ingatan cooldown sebelumnya | Sidecar berversi 1 di samping session_file menyimpan batas waktu; worker baru tidak dibuat selama cooldown |

## Batas dan pemulihan

`social_export.root_rejection` adalah satu aturan bersama bagi pemeriksaan awal
dan seleksi ekspor. Waktu `since` tetap inklusif, `until` eksklusif; unknown date,
mode include any/all dan prioritas exclude tetap sama. Root ditolak tetap
dikembalikan ke koordinator untuk audit alasan, tanpa mengakuisisi anaknya.

X mempertahankan `barrier.json`: RATE_LIMITED dan SERVER_UNAVAILABLE dapat
kedaluwarsa; login/challenge/akses ditolak tetap membutuhkan penanganan operator.
Instaloader menyimpan `<session_file>.cooldown.json` secara atomik dengan mode 0600,
schema_version=1, username, status dan not_before. Tidak ada cookie/token di file
ini. HTTP 429 memakai cooldown platform (default 360 detik), sedangkan server
memakai minimal 60 detik; Retry-After yang lebih panjang selalu dihormati.
File cooldown tidak valid menggagalkan operasi sebelum jaringan dibuka.

PARTIAL karena pagination macet bukan bukti komentar habis. Pada backend web
Instagram, operasi berikutnya dapat berjalan; tidak ada retry agresif untuk post
tersebut. Jalur query_hash masih menggunakan iterator asli dan batas waktu worker.
Metadata hasil pencarian X, cache Post Instagram, session dan rate controller
persisten yang sudah ada tetap digunakan.

## Pengukuran sebelum / sesudah

Pembanding: source commit `d896cade2719d77b0498e87d5c79504cbf483894` dan working
tree baru, fixture offline yang sama; tidak mengirim request ke X/Instagram.
Data mesin: `output/x_instagram_performance_20261106/benchmark.json`.

| Fixture | Lama | Baru | Makna |
|---|---:|---:|---|
| X: 4 jendela untuk 29 hari kalender | 32 kunjungan hari, 3 berulang | 29 kunjungan hari, 0 berulang | Cakupan tetap 29 hari dan jumlah operasi tetap 4; ini bukan pengukuran jumlah HTTP live |
| Instagram: replies cap 0 | 2 request simulasi | 1 request simulasi | ID hasil tetap `1,21`; satu permintaan replies yang tidak diperlukan dihapus |
| Instagram: replies cap 1 dengan embedded page | 2 request simulasi | 1 request simulasi | ID hasil tetap `1,21,22`; cap terpenuhi dari respons yang sudah tersedia |
| Root di luar tanggal/keyword | Membuka iterator/request anak | 0 request anak | Dibuktikan dengan tes yang gagal jika callback jaringan anak dipanggil |

Penghematan 50% berlaku pada fixture embedded-page tersebut, bukan klaim seluruh
crawl dua kali lebih cepat. Kecepatan nyata dipengaruhi jumlah post relevan,
panjang thread, respons platform dan cooldown. Scweet mengembalikan daftar hasil
setelah operasi SDK selesai; streaming per halaman belum tersedia pada wrapper
yang dipakai. Tidak dilakukan fork SDK atau perubahan paket terpasang.

## Verifikasi dan rilis

Tes mencakup rentang tanggal tanpa overlap/gap, seleksi awal tanpa request anak,
urutan root-parent-reply, cap nol/global, reuse first_data dengan NodeIterator asli,
pagination macet, 429/503, cooldown antarrun, mode file dan ekspor parsial.
Perintah utama:

```sh
.venv-twitter/bin/python -m unittest discover -s tests/crawler -p test_twitter_crawler.py -q
.venv-instagram/bin/python -m unittest discover -s tests/crawler -p test_instaloader_crawler.py -q
.venv-instagram/bin/python -m unittest discover -s tests/crawler -p 'test_instagram*.py' -q
.venv-tiktok/bin/python -m unittest discover -s tests/crawler -p test_social_crawler.py -q
```

Hasil: 223 tes relevan lulus (29 X, 30 Instaloader, 36 Instagram alternatif,
37 koordinator, 14 integrasi Instagram, 7 konfigurasi, 7 integrasi Reddrix,
63 regresi TikTok). Tes unlimited tambahan menjalankan 8 tes: 6 lulus,
2 dilewati karena SDK opsional. Formatter, lint dan dry-run kedua entry point
lulus. Rangkaian koordinator yang lebih luas menjalankan 71 tes dengan 2 error
karena Selenium belum terpasang dan 1 skip; ini tidak dilaporkan sebagai lulus.
Daemon Docker tidak aktif, sehingga image belum dibangun atau dijalankan ulang.

Tidak ada perubahan tabel, skema SQLite Scweet atau PostgreSQL. **No migration
required**. Sidecar cooldown memiliki penanda versi agar perubahan format di
masa depan dapat dikenali. Dockerfile/allowlist yang ada sudah menyalin semua
modul yang berubah; verifikasi image memerlukan daemon Docker aktif:

```sh
docker build -f deployment/docker/Dockerfile.twitter -t beesense-twitter:local .
docker run --rm beesense-twitter:local --dry-run
docker build -f deployment/docker/Dockerfile.instaloader -t beesense-instaloader:local .
docker run --rm beesense-instaloader:local --dry-run
```

Uji live X/Instagram belum dilakukan dalam perubahan ini. Referensi SDK:
[NodeIterator dan first_data](https://instaloader.github.io/module/nodeiterator.html),
[Scweet read API](https://altimis.github.io/Scweet/).
