# TikTokCrawler mandiri BeeSense

Backend aktif `TikTokCrawler` 2.5.0 memakai `NativeTikTokClient` buatan BeeSense
(`BeeSenseNative:1.2.0`) dan Playwright 1.64.1. Tidak memakai Pyktok, PyTok,
TikTok-Api atau kode dari repo Chinel0 yang dibatalkan pengguna. Kontrak
`SocialCrawler` 1.10.0, normalisasi ID, filter dan Excel bersama tetap dipakai.

## Menjalankan

```sh
python3 -m venv .venv-tiktok
.venv-tiktok/bin/python -m pip install -r requirements/tiktok.txt
.venv-tiktok/bin/python -m Crawler.Backend.tiktok_crawler --install-browser
.venv-tiktok/bin/python -m Crawler.Backend.tiktok_crawler --dry-run
.venv-tiktok/bin/python -m Crawler.Backend.tiktok_crawler --target-posts 500 --total-seconds 1800
# Perbandingan mode terlihat, tanpa mengubah JSON:
.venv-tiktok/bin/python -m Crawler.Backend.tiktok_crawler --headed --target-posts 500 --total-seconds 1800
```

Default tetap 1.000 post, tanpa batas jam atau kuota request harian lokal.
`--config` memilih konfigurasi universal; `--output-dir` memilih bundle eksplisit
sehingga organizer arsip tidak berjalan. Dry-run tidak membaca token atau jaringan.
`--headed` hanya override `headless: false` untuk satu proses, bukan login otomatis.

## Satu konfigurasi

Semua pengaturan ada di `config/social_crawler.json`. Query, include/exclude,
rentang publikasi dan cap diwarisi bersama. `platforms.tiktok` menyediakan:

- `urls`, `hashtags`, `queries`, `search_results`: sumber dan batas kandidat unik.
- `browser`: chromium/firefox/webkit; `headless`: default true; `sort`: relevance.
- `auth_file`: default `config/auth.json`.
- `request_interval_seconds: 3`: jeda minimum antar dokumen/API akuisisi; nilai yang
  lebih besar antara pengaturan ini dan delay bersama yang digunakan.
- `scroll_pause_seconds: 3`: tunggu UI setelah navigasi/gulir.
- `idle_scroll_limit: 3`: batas idle pencarian dan mode komentar dengan cap eksplisit.

Tiga pengaturan pacing/idle merupakan integer 1–3600. Batas idle tidak menghentikan
pagination komentar tanpa cap; ini bukan kuota harian. Komentar dan
balasan default tetap `null` (tanpa cap lokal); nol menonaktifkan jenis tersebut.
Tanggal root tetap `since` inklusif dan `until` eksklusif. Tidak mengganti query
menjadi hashtag atau memperluas tanggal untuk memenuhi target.

## Akuisisi browser

Satu worker memiliki satu browser dan konteks biasa. Query membuka halaman search,
hashtag membuka halaman tag. Crawler membaca JSON hydration, respons API yang
benar-benar dibuat UI, dan link video/foto yang terlihat pada DOM. Hasil yang hanya
memiliki URL harus memperoleh metadata asli dari halaman post sebelum dipilih.
Gulir UI memuat halaman berikutnya; tidak membuat signature atau request API sendiri.

Root lolos tanggal/keyword sebelum komentar diambil. Crawler membuka panel komentar,
menggulir daftar, dan menekan kontrol balasan yang tersedia. Respons komentar dan
balasan harus membawa ID asli; root dan parent diverifikasi. Teks DOM tanpa native
ID tidak dibuatkan ID sintetis. Timestamp/statistik yang tidak tersedia tetap tidak
diketahui, bukan diganti nol. Parent balasan yang tidak diamati diberi warning dan
balasannya tidak diekspor sebagai relasi palsu.

Event request diberi epoch operasi sehingga respons terlambat dari pencarian/post
sebelumnya tidak tercampur. ID ganda disaring. State browser bersifat sementara;
raw signed URL, cookie dan body debug tidak diekspor. Telemetri hanya jumlah
respons, status HTTP, kategori endpoint dan kandidat tidak valid.

## Pacing, barrier dan progres

Jeda request diserialkan. Respons server 5xx menaikkan interval request berikutnya.
HTTP429 menghentikan akuisisi dan menyimpan waktu `Retry-After` (detik atau HTTP date)
pada `.cache/tiktok/native_cooldown.json`; proses baru tidak mengirim request selama
cooldown itu masih berlaku. Ini cache operasional, bukan file konfigurasi atau
penyimpanan kredensial. HTTP401/403, CAPTCHA/login wall, respons verify dan API
kosong/bukan JSON juga menghentikan proses. Tidak ada retry otomatis setelah barrier,
proxy/rotasi akun, patch fingerprint, solver CAPTCHA, atau ekstraksi cookie profil.

`auth.json` tetap lokal dan tidak diubah. Satu entri `sosmed: tiktok` menerima
`msToken`, `ms_token`, `mstoken`, atau alias lama `sessionid` berisi msToken. Alias
berbeda nilainya ditolak. Token dipasang pada domain `.tiktok.com` sebelum navigasi.
Keberadaan token tidak menjamin akses atau membuktikan bahwa token kedaluwarsa.

Baris disalurkan ke parent selama operasi berlangsung dan tetap diekspor ketika
worker mencapai deadline. Bundle parsial dan arsip native ID menjadi dasar memulai
run lanjutan tanpa mengekspor post yang sudah ada lagi. Ini **bukan resume cursor
komentar persis**; komentar parsial dari root lama tidak otomatis dilengkapi ulang.
Cakupan UI tidak dijamin lengkap; `comments_complete` tetap false. Tidak ada janji
bahwa crawler tidak akan diblokir.

## Output dan deduplikasi

`TikTokAdapter` memakai `ContentInput`/`Dataset`: video, komentar, balasan, relasi,
timestamp UTC dan statistik tersedia. Native ID disimpan sebagai string agar
presisi Excel terjaga. ID video yang sama tetap satu identitas walau username
berubah; hyperlink mempertahankan URL sumber yang benar.

`social_data.xlsx` memiliki sheet `Data` dengan sepuluh kolom bersama.
`dataset.xlsx` serta JSONL/manifest menyimpan audit dan statistik. Run default
berdata memperbarui `outputs/crawling/tiktok/<tanggal-crawling-WIB>/social_data.xlsx`
dengan deduplikasi native ID lintas hari. Bundle audit ada di
`output/crawler_runs/social_<UTC>_<run-id>/`. Run kosong hanya menyimpan Excel
berheader dan audit, tanpa partisi tanggal kosong atau perubahan arsip lama.

## Pengujian dan Docker

```sh
python -m unittest discover -s tests/crawler -p test_tiktok_crawler.py -v
docker build -f deployment/docker/Dockerfile.tiktok -t beesense-tiktok:local .
docker run --rm beesense-tiktok:local --dry-run
```

Fixture browser nyata (respons sepenuhnya dicegat) memvalidasi cookie sebelum
navigasi, hydration post, komentar/balasan dan statistik; fixture tidak masuk arsip
nyata. Dockerfile yang sama memasang Chromium dan dependensi minimal dari
`requirements/tiktok.txt`. Mount auth read-only dan volume hasil pada runtime.
Mode native tidak membuka port HTTP. Mode Chrome live membuka loopback di host.
Akses socket Docker lokal ditolak, sehingga image belum
dibangun/dijalankan untuk validasi. No migration required; tidak menulis PostgreSQL.

Uji live mandiri: [TIKTOK_NATIVE_TRIAL_20261103.md](TIKTOK_NATIVE_TRIAL_20261103.md).
Riwayat gagal: [Omkar](TIKTOK_TRIAL_20261103.md),
[PyTok](TIKTOK_PYTOK_TRIAL_20261103.md), [TikTok-Api](TIKTOK_API_TRIAL_20261103.md),
[Pyktok](TIKTOK_PYKTOK_TRIAL_20261103.md).

## Probe TikWM dari pengguna

Script TikWM yang diberikan pengguna sudah dicoba tanpa modifikasi: uji awal lima
video/dua puluh komentar per video gagal pada pencarian pertama dengan HTTP403,
exit code2, tanpa data. Jalur pihak ketiga ini belum menjadi backend aktif. Auth
tidak dibaca/dikirim. Lihat [laporan probe](TIKTOK_TIKWM_PROBE_20261103.md).

## Validasi CAPTCHA/login manual di Chromium

```sh
.venv-tiktok/bin/python -m Crawler.Backend.tiktok_crawler \
  --manual-validation --manual-wait-seconds 600 \
  --target-posts 500 --total-seconds 1800
```

TikTokCrawler 2.1.0 / BeeSenseNative 1.1.0 menyediakan preflight manual. Chromium
terlihat dibuka dengan profil khusus `.cache/tiktok/chromium-profile`, bukan profil
browser pribadi. Pengguna boleh menyelesaikan CAPTCHA/login di jendela tersebut.
Crawler berhenti melakukan aksi akuisisi saat menunggu konfirmasi manusia. Request
UI selama tahap manual tetap bisa berjalan agar pengguna dapat memvalidasi sesi;
HTTP429 tetap menghentikan proses dan cooldown tidak dapat ditimpa konfirmasi.

Flag CLI mengaktifkan Chromium terlihat dan `manual_wait_seconds` (default override
600) untuk satu run. JSON utama menyediakan `manual_wait_seconds: 0` (nonaktif),
`manual_poll_seconds: 2` dan `manual_profile_dir` relatif ke direktori privat
`.cache/tiktok`. Aktifkan manual dengan durasi positif, headless false dan browser
chromium. Profil disimpan oleh Chromium agar login manual dapat dipakai kembali;
isi profil tidak dimasukkan ke graph, Git, log atau bundle hasil.

Event `manual_validation` mencantumkan wait_id, file kontrol lokal dan sisa batas
waktu. Operator mengonfirmasi setelah CAPTCHA/login selesai dengan aksi `continue`
untuk wait_id yang sama; aksi `cancel` menghentikan run. Token konfirmasi lama tidak
berlaku. Konfirmasi diperiksa kembali terhadap CAPTCHA/login yang terlihat, tetapi
bukan bukti crawling berhasil. Data nyata tetap harus diperoleh dan dinormalisasi.

Scheduler memperpanjang anggaran operasi pencarian dengan waktu tunggu manual,
tetap tunduk pada total durasi run. Tidak ada solver otomatis. Setelah preflight,
barrier baru tetap menghentikan run; fitur ini bukan loop retry tanpa batas.
`auth.json` tidak diubah. Profil dan file kontrol merupakan state operasional lokal.
Mode manual membutuhkan layar lokal; mode Docker headless memakai durasi manual nol.


## Chrome yang sudah terbuka (pengambilan dibantu agen)

Permintaan terbaru memilih **tab Chrome pengguna yang sudah login**, tanpa membuka
Chromium baru atau menutup/restart Chrome. Pengujian melalui koneksi browser Codex
berhasil membaca satu post dan sepuluh komentar dengan ID asli. Ini belum memenuhi
500 post/30 menit dan belum membuktikan kelengkapan komentar.

`ChromeCaptureWorker` menerima tangkapan publik yang telah dibaca agen melalui UI
Chrome. Worker ini **mengimpor tangkapan**, bukan driver yang otomatis menempel ke
Chrome. Tidak membaca auth.json/cookie, tidak membuka browser, tidak membuat request
TikTok dan tidak memakai SDK. Pengambilan live melalui tab tetap membutuhkan agen
browser terhubung. Kemampuan kontrol tab tersebut tidak menyediakan endpoint Python
Playwright. Menjalankan perintah impor tidak menambah post baru di luar tangkapan.

```sh
.venv-tiktok/bin/python -m Crawler.Backend.tiktok_crawler \
  --chrome-capture .cache/tiktok/chrome_public_capture_20261103.json \
  --target-posts 500 --total-seconds 1800
```

Format data: objek JSON dengan `schema_version: 1`, `source:
"existing_chrome_public_page"`, `query`, `captured_at` UTC dan `records` berisi
record post/comment/reply sesuai normalizer TikTok. Ini artefak hasil, bukan file
konfigurasi kedua; query/filter/target/penyimpanan tetap dari social_crawler.json.
Native ID wajib string. Komentar wajib memiliki root dan balasan wajib mempunyai
parent komentar yang diamati. Duplikasi disaring sebelum ekspor dan di arsip.
Statistik hanya angka sumber; angka singkatan yang tidak pasti tidak dianggap exact.
Tanggal post memakai timestamp sumber yang cocok dengan ID halaman. Tanggal komentar
yang hanya tampilan relatif tetap unknown dengan published_display, tidak direkayasa.

Provenance: `beesense_existing_chrome_capture` / `BeeSenseChromeCapture:1.0.0`,
`capture_not_refreshed`, `comments_completeness_unverified`. Waktu kompilasi
capture dicatat; jendela observasi manual dicantumkan terpisah pada artefak uji.
Impor menggunakan kontrak, filter, Excel dan organizer arsip yang sama. Reimport
menghormati indeks ID lama. Tidak menandai komentar lengkap karena UI menampilkan
jumlah lebih banyak daripada ID yang berhasil diamati.

Lihat [uji Chrome](TIKTOK_CHROME_TRIAL_20261103.md). Untuk driver Python langsung,
Playwright membutuhkan endpoint CDP yang memang tersedia; Chrome 136+ membatasi
remote debugging pada direktori data default. Tidak me-restart Chrome pribadi,
menyalin profil atau mengubah pengaturan debugging pada uji ini. Rujukan primer:
[Chrome remote debugging](https://developer.chrome.com/blog/remote-debugging-port)
dan [Playwright connect_over_cdp](https://playwright.dev/python/docs/api/class-browsertype#browser-type-connect-over-cdp).

## Konektor Chrome otomatis

Versi 2.4.1 menyediakan `--chrome-extension` dan ChromeLiveWorker 1.1.0.
Uji live transport agen sebelumnya menyimpan 2 post + 30 komentar + 13 balasan,
target 500 belum tercapai. Pengguna sudah mengonfirmasi pemasangan ekstensi. Koneksi dan hasil live baru
masih harus diverifikasi melalui pairing lokal. Konfigurasi dan exporter tetap bersama. Lihat
[TIKTOK_CHROME_LIVE.md](TIKTOK_CHROME_LIVE.md) untuk alur, izin, tes dan batasnya.

## Status akhir 3 November 2026 — crawler dihentikan

Uji ekstensi terpasang dengan TikTokCrawler 2.4.1 / BeeSenseChromeLive 1.1.0
menyimpan **13 post, 93 komentar, 261 balasan (367 record unik)** dalam 656,6 detik.
Run `social_20261103T094828Z_23fb8a79` berstatus INTERRUPTED; target 500 belum
tercapai (kurang 487). Dua belas kandidat di luar tanggal dan dua kandidat tanpa
include keyword disaring. `comments_complete: false`; angka komentar pada TikTok
bukan jumlah yang sudah diperoleh. Excel: `outputs/crawling/tiktok/2026-11-03/social_data.xlsx`.
Arsip gabungan setelah run: **35.197 ID unik, 0 duplikat native ID**.

TikTokCrawler **2.5.0**, BeeSenseNative **1.2.0**, dan Connector **1.1.0** memperbaiki
penghentian tiga putaran idle pada komentar tanpa cap. Komentar menunggu akhir
pagination `has_more: false` dari sumber dan balasan tiap parent sampai habis;
metadata yang tidak tersedia tetap belum membuktikan lengkap. Kontrol balasan yang
lambat dicoba kembali dengan jeda, bukan dilewati permanen. Deadline global,
Stop, CAPTCHA/login dan pembatasan sumber tetap berlaku; hasil parsial disimpan.
Tanpa deadline, proses dapat terus menunggu sumber sampai operator menghentikannya.
Batas idle pencarian serta cap eksplisit tetap berlaku. Deduplikasi memakai ID asli.

Status terhubung kini ditampilkan setelah GET tugas lolos autentikasi. Kesalahan
pairing tidak ditimpa status pelepasan debugger normal. Izin dan ID ekstensi sama.
**Reload ekstensi lokal sebelum penggunaan berikutnya.** Perbaikan terbaru diuji
offline; tidak dilakukan uji live baru karena pengguna meminta proses berhenti.
Tidak ada migrasi database, perubahan auth.json, atau redeploy Streamlit.
Seluruh perubahan diterbitkan melalui branch terpisah dari main agar branch
Streamlit yang tercatat di README tidak diperbarui.
