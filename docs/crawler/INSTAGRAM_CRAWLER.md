# InstagramCrawler: instagrapi dan Chrome

## Integrasi dan run tiga jam

Instruksi baru pengguna mengizinkan integrasi tanpa menunggu trial lama yang
dihentikan. `SocialCrawler` 1.5 kini menggunakan worker dan `InstagramAdapter`
dari modul ini, dengan kontrak Excel yang sama. Preset
`config/social_crawler_instagram_3h.json` hanya mengaktifkan Instagram, 10.800 detik,
target 1.000 post dengan minimum 10 komentar; YouTube/Reddit tidak di-crawl ulang.
Run `outputs/social_instagram_20261030_1000_3h_01` mulai 30 Oktober **13.28 WIB**,
deadline sekitar **16.28 WIB**. Hasil akhir belum ditetapkan selama proses berjalan.

Pengguna mengonfirmasi penggabungan berdasarkan tanggal hasil crawling **27–30
Oktober 2026**, bukan filter tanggal publikasi post. Seluruh hasil asli dipertahankan;
dataset baru menghapus pengulangan native ID lintas run/aggregate, menyimpan record
terbaru sesuai urutan sumber dan audit lineage. Teks sama dengan ID berbeda tetap
dipertahankan. Perubahan klasifikasi comment/reply diaudit; konflik root ditolak.
Rencana akhir: [pipeline akuisisi sampai deployment](INSTAGRAM_PIPELINE_20261030.md).

## Jalur Chrome yang sedang diuji

Setelah instagrapi dan Instaloader tetap ditolak, pengguna memilih Chrome/Playwright
dengan login manual. Class `InstagramCrawler` sekarang dapat memilih `backend:
"browser"` lewat `config/instagram_browser_crawler.json`. Worker
`instagram_browser.py` memakai **@playwright/cli 0.1.22** dan Chrome terpasang.
Instagrapi tetap tersedia melalui konfigurasi semula.

```sh
.venv-instagram/bin/python -m pip install -r requirements/instagram-browser.txt
# Node.js 22 dan Google Chrome diperlukan. Buka profil khusus, lalu login manual:
npx --yes --package @playwright/cli@0.1.22 playwright-cli -s=beesense-instagram open \
  https://www.instagram.com/ --browser chrome --headed --persistent \
  --profile "$PWD/output/instagram_browser/chrome_profile"
.venv-instagram/bin/python -m Crawler.Backend.instagram_crawler \
  --config config/instagram_browser_crawler.json \
  --output-dir outputs/instagram_browser_trial_baru
```

Gunakan versi CLI dan nama sesi yang sama saat login dan crawling. Instalasi CLI
yang berbeda dapat memakai daemon terpisah; dua daemon tidak boleh membuka profil
yang sama bersamaan. Login manual pertama berhasil sebagai `researchinnovationsocs`.
Worker Python telah memverifikasi **1 post dan 15 komentar** dengan native ID asli.
Trial penuh `outputs/instagram_browser_20261030_30m_02` dimulai sekitar **13.08 WIB**
pada 30 Oktober 2026. Pengguna kemudian meminta stop. Status akhir **INTERRUPTED**:
**76 post, 910 komentar, 0 balasan**, 59 post memenuhi minimum 10 komentar;
elapsed 718.82 detik (sekitar 12 menit). Excel berisi 986 baris; 12 checksum manifest
terverifikasi, root unik, baseline tidak berubah. `live_access_verified: true`,
`trial_passed: false`; trial 30 menit belum selesai dan integrasi belum dilakukan.
Hasil: `outputs/instagram_browser_20261030_30m_02/social_data.xlsx`. Run `_01`+dihentikan lebih awal untuk memperbaiki pembacaan komentar, lalu diganti dengan
anggaran penuh 1800 detik pada `_02`; keduanya bukan dua dataset untuk digabung.

Discovery mengikuti halaman hashtag yang dapat dialihkan Instagram ke pencarian
keyword. Urutan hasil mengikuti UI Instagram; pengaturan `search_tab` mobile tidak
mengatur urutan UI browser. Scroll dibatasi, kandidat dideduplikasi, tanggal dan
keyword tetap disaring lokal. Caption dibaca dari hydration JSON yang memang
tertanam pada dokumen post, bukan login/API mobile tambahan. Karena caption dan
komentar tiba dalam script berbeda, worker menunggu stream dokumen. Komentar dari
script terpisah hanya diterima jika native ID-nya ada pada permalink komentar DOM
untuk shortcode post yang sama. Data rekomendasi post lain tidak ikut diekspor.
Komentar awal yang tersedia di dokumen dipertahankan; thread lanjutan tidak diklaim
lengkap. Gambar/video, inbox, cookies, password dan payload autentikasi tidak diambil.

Browser memakai satu profil persisten selama run, berada di `output/` yang diabaikan
Git. Screenshot diagnostik menutup seluruh input login. Jangan menyalin profil Chrome
pribadi. CAPTCHA/login/429 menghentikan akuisisi dan membiarkan browser untuk tindakan
manual; default tidak ada retry 429. Saat selesai normal, browser ditutup dan profil
lokal dipertahankan. Tidak perlu login password pada setiap post.

`browser.headed: true` membuka jendela di macOS. Pada Linux tanpa desktop gunakan
`false` setelah menyiapkan sesi manual di lingkungan server yang sama; sesi Chrome
macOS tidak dianggap portabel ke Linux. Mode headed Linux memerlukan DISPLAY yang
disediakan operator. Image terpisah `deployment/docker/Dockerfile.instagram-browser`
memuat Python, Node, CLI dan Chrome; kredensial/profil hanya di-mount saat runtime.
Docker daemon lokal belum tersedia, sehingga build dan startup image belum terverifikasi:

```sh
docker build --platform linux/amd64 -f deployment/docker/Dockerfile.instagram-browser \
  -t beesense-instagram-browser .
docker run --rm beesense-instagram-browser
```

Filter, baseline read-only, kontrak Excel/JSONL dan scheduler tetap digunakan bersama
backend instagrapi. Provenance browser dicatat sebagai
`playwright_chrome_rendered_document`, bukan instagrapi. Worker fixture tetap synthetic;
keberhasilan offline tidak meluluskan trial live. Integrasi SocialCrawler menunggu hasil
trial yang menghasilkan post beserta komentar nyata tanpa hambatan terminal.

## Backend instagrapi dan riwayat diagnosis

`Crawler/Backend/instagram_crawler.py` menyediakan class `InstagramCrawler` dan CLI
standalone memakai instagrapi 3.2.2, Python 3.11+. Caption foto, video, Reels dan
album menjadi satu root per media. Komentar dan balasan menyimpan native ID,
parent, tanggal sumber dan provenance. Gambar/video tidak diunduh.

## Instalasi dan konfigurasi

Jalankan dari root repository:

```sh
python3.12 -m venv .venv-instagram
.venv-instagram/bin/python -m pip install -r requirements/instagram.txt
.venv-instagram/bin/python -m Crawler.Backend.instagram_crawler --dry-run
```

`config/instagram_crawler.json` mempertahankan rentang tanggal, include/exclude
keyword dan baseline `outputs/social_20261028_01` dari percobaan Reddit.
Anggaran akuisisi **1800 detik (30 menit)**, timeout operasi 90 detik, target
1000 root dengan minimum 10 komentar/balasan unik. Target adalah batas aspirasi,
bukan jaminan. Pencarian memakai hashtag kuliah/kampus/universitas/beasiswa/jurusan;
pencarian hashtag bukan pencarian frasa Reddit. Pagination menyimpan cursor selama
run dan berhenti pada cursor berulang, batas halaman/kandidat/post atau deadline.
Hasil recent Instagram tidak dijamin lengkap atau kronologis; tanggal dan keyword
root tetap diperiksa lokal. since inklusif, until eksklusif. Komentar dipertahankan
sebagai konteks kecuali terkena exclude.

## Login lokal

Login normal hanya dilakukan eksplisit. Crawling memakai sesi yang telah disimpan,
tanpa mengulang password login di setiap operasi.

```sh
.venv-instagram/bin/python -m Crawler.Backend.instagram_crawler --login
# Atau memakai file kredensial lokal yang disediakan pengguna:
.venv-instagram/bin/python -m Crawler.Backend.instagram_crawler --login --auth-file config/auth.json
# Pola load settings -> login(username,password) -> simpan settings:
.venv-instagram/bin/python -m Crawler.Backend.instagram_crawler --login --auth-file config/auth.json --login-method password
.venv-instagram/bin/python -m Crawler.Backend.instagram_crawler --check-session
```

Input password/2FA di terminal disembunyikan. Format file auth adalah object atau
array object dengan `sosmed: "instagram"`, `username`, `password`, serta opsional
`verification_code`. Harus ada tepat satu entri Instagram. Kredensial tidak
diterima dalam konfigurasi crawling, argumen password, metadata output, atau log.
`config/auth.json` diabaikan Git. File sesi default
`output/instagram/session.json` juga diabaikan Git dan ditulis atomik dengan mode
0600. File itu baru ada setelah login berhasil; file auth adalah input login,
sedangkan file sesi adalah hasil login. Sesi lama yang diberikan operator dapat
dipilih melalui `instagrapi.session_file` pada konfigurasi. Path relatif mengacu
pada root repository, bukan folder kerja saat perintah dipanggil.

Alternatif cookie browser: setelah login Instagram di Chrome, buka DevTools
(macOS ⌥⌘I), Application → Cookies → https://www.instagram.com, lalu salin Value
cookie `sessionid` ke field `sessionid` pada entri Instagram di auth lokal. Jalankan
perintah `--login --auth-file config/auth.json` yang sama. Jika field ini ada,
`login_by_sessionid()` digunakan dan password login tidak dicoba. Cookie browser
bisa ditolak oleh API privat; keberadaan cookie tidak membuktikan akses crawler.
Setelah diterima, settings disimpan pada path sesi yang sama. Nilai cookie tidak
boleh dikirim melalui chat/log/Git. Login ini tetap dibatasi timeout subprocess.

`--login-method auto` mempertahankan pemilihan cookie jika field `sessionid` ada.
Gunakan `--login-method password` untuk memuat device/settings yang tersimpan lalu
memanggil `login(username,password)`, sekalipun auth lokal juga berisi cookie.
`--login-method sessionid` memilih cookie secara eksplisit. Pilihan ini hanya
berlaku bersama `--login --auth-file` dan tidak menjadi kredensial konfigurasi.
Settings dengan authorization kosong boleh dimuat pada login eksplisit agar
perangkat tetap konsisten; operasi akuisisi tetap memerlukan user terautentikasi.

`login_with_saved_password()` memvalidasi sesi melalui `login()`. Jika exception
`LoginRequired` masih diteruskan oleh SDK, helper mencoba `relogin()` satu kali
pada client yang sama. Kode verifikasi eksplisit diteruskan melalui
`login(..., relogin=True, verification_code=...)`, karena helper `relogin()` SDK
tidak meneruskan kode itu. Upgrade/challenge/rate limit tidak diulang. Settings
hanya disimpan atomik setelah login diterima; kegagalan tidak menimpa file sesi
sebelumnya. Akuisisi tidak memuat password atau melakukan pemulihan login otomatis.

Library menggunakan API privat Instagram yang tidak resmi. Tidak ada API resmi
berbayar, proxy berbayar, solver CAPTCHA, rotasi akun/perangkat atau pengulangan
login otomatis. Challenge/2FA/password reset memerlukan tindakan operator dan
menghentikan worker. `ClientNeedsUpgradeError` diberi status
`CLIENT_UPGRADE_REQUIRED`, terpisah dari HTTP 429 dan password salah. Respons
library tidak dicetak; error yang diekspor hanya kode/jenis exception.

## Menjalankan percobaan

```sh
.venv-instagram/bin/python -m Crawler.Backend.instagram_crawler \
  --output-dir outputs/instagram_instagrapi_trial_02
```

Setiap operasi berjalan dalam subprocess spawn dengan hard deadline. Waktu
pencarian, pengambilan komentar, retry internal dan cooldown termasuk batas
1800 detik; finalisasi Excel terjadi sesudah akuisisi. Pacing antaroperasi dan
request upstream masing-masing 2 detik. instagrapi tetap memiliki retry internal
khusus timeout/incomplete-read, sehingga hard deadline subprocess tetap perlu.
429 memakai cooldown minimal 360 detik atau Retry-After numerik yang lebih lama;
default retry 0. Jika diaktifkan, retry tetap tunduk pada deadline dan batas run.
Challenge/login/upgrade menghentikan pengambilan dan mempertahankan bukti parsial.
Tiga error sumber/timeout berturut-turut menghentikan run.

Output direktori baru berisi `social_data.xlsx` satu sheet **Data** dengan 10 kolom
yang sama dengan SocialCrawler, `dataset.xlsx` delapan sheet audit, JSONL delapan
tabel, contract, manifest dengan SHA256 dan summary. Waktu Excel ditampilkan WIB;
waktu JSONL UTC. Native ID/shortcode/parent diperiksa; object key dan URL kanonik
mencegah duplikasi. Baseline dibaca read-only dan hash dicatat. Row budget 500000;
formula Excel diperlakukan sebagai teks dan teks panjang penuh tetap ada di JSONL.
`SocialExportMixin` menyediakan seleksi root dan proyeksi Excel bersama; pemindahan
fungsi tersebut tidak mendaftarkan backend Instagram ke SocialCrawler.

Progress atomik berada di file `<output-dir>.progress.json` di sebelah direktori
bundle. Status PARTIAL/shortfall tetap jujur jika target tidak tercapai. Fixture
offline selalu `synthetic: true` dan tidak pernah meluluskan uji live. Trial live
baru lulus bila menghasilkan root beserta komentar/balasan nyata, tanpa invalid
row atau hambatan terminal. Ini berbeda dengan mencapai target 1000 post.

## Hasil percobaan 30 Oktober 2026

Login password menggunakan auth pengguna ditolak oleh Instagram dengan
`ClientNeedsUpgradeError` / `needs_upgrade`. Runtime instagrapi 3.2.2 sudah memakai
profil Android bawaan 449.0.0.52.84. Pada percobaan awal ini belum ada sesi tersimpan.
Tidak ada upaya mengganti perangkat/identitas atau mengulang login diam-diam.

Pemanggilan class dengan konfigurasi 1800 detik menghasilkan bundle nyata
`outputs/instagram_instagrapi_20261030_30m_01`, status **PARTIAL / LOGIN_REQUIRED**,
**0 post, 0 komentar, 0 balasan**, elapsed akuisisi **0.23 detik**.
**Uji pengambilan data selama 30 menit belum dapat berlangsung**; 1800 adalah
konfigurasi, bukan durasi uji yang telah selesai. `trial_passed: false` dan
`live_access_verified: false`. Workbook kosong hanya bukti penanganan hambatan,
bukan hasil crawling yang berhasil. Login receipt lokal tersimpan di
`output/instagram_work/login_result.json` tanpa nilai kredensial.

Sesuai syarat pengguna, backend Instagram **belum digabungkan/diaktifkan** pada
`social_crawler.py` maupun `config/social_crawler.json`. YouTube/Reddit tetap
memakai backend dan batas waktu sebelumnya. Integrasi dan uji ulang gabungan
menunggu keberhasilan uji live dengan sesi yang diterima Instagram.

Upstream: [getting started](https://subzeroid.github.io/instagrapi/latest/getting-started/),
[hashtag](https://subzeroid.github.io/instagrapi/latest/usage-guide/hashtag/),
[comment](https://subzeroid.github.io/instagrapi/latest/usage-guide/comment/),
[login migration](https://subzeroid.github.io/instagrapi/latest/usage-guide/login-migration/),
[changelog needs_upgrade](https://github.com/subzeroid/instagrapi/blob/master/CHANGELOG.md).

### Percobaan cookie browser dan pemuatan ulang

Pengguna kemudian menyediakan `sessionid` melalui auth lokal. Login cookie dan
satu baca privat akun berhasil; settings tersimpan di `output/instagram/session.json`.
Uji kedua dimulai **30 Oktober 2026 11:20:33 WIB**, anggaran 1800 detik, tetapi
permintaan hashtag pertama ditolak `LOGIN_REQUIRED` setelah **5.64 detik**.
Bundle `outputs/instagram_instagrapi_20261030_30m_02` tetap PARTIAL, 0 post,
0 komentar, 0 balasan, `trial_passed: false`. Ini bukan uji 30 menit yang selesai.

Satu pemeriksaan baca akun sesudah pemuatan ulang juga ditolak LOGIN_REQUIRED.
Pemeriksaan lokal tanpa jaringan memastikan cookie, authorization, UUID perangkat
dan header authorization dipulihkan; hanya pacing request berubah dari 1 ke 2 detik.
Ini tidak membuktikan alasan server, tetapi tidak menunjukkan kehilangan kredensial
pada pemuatan ulang. Sesuai dokumentasi upstream, cookie browser dapat ditolak atau
dibatalkan oleh API privat. Tidak ada pengulangan impor cookie atau password login.

Probe terpisah metode web terdokumentasi `hashtag_medias_paginated_gql` juga tidak
menghasilkan data: AttributeError `get` pada `instagrapi/mixins/public.py:467`,
dipanggil dari `hashtag.py:227`. Probe diagnostik hanya menyimpan tipe error dan
lokasi kode, tanpa isi respons atau nilai cookie. Hasilnya bukan bukti akses web
yang berhasil dan tidak mengubah backend produksi.

### Alternatif Instaloader yang diminta pengguna

Instaloader **4.16** dipasang pada environment Instagram untuk percobaan akses
terpisah (`requirements/instaloader.txt`). Dengan sessionid lokal, `test_login()`
gagal dengan `ConnectionException` sebelum discovery hashtag. Satu login normal
memakai username/password lokal juga gagal dengan `LoginException` pada
`instaloadercontext.py:344` (respons login berstatus gagal). Tidak ada bukti cukup
untuk menyebutnya HTTP 429, password salah, atau CAPTCHA. Tidak ada data diambil.

Percobaan ini hanya preflight akses, **bukan uji crawling 30 menit** dan bukan
penggantian backend yang sudah teruji. Tidak ada retry login lanjutan atau
integrasi Instaloader ke SocialCrawler. Receipt yang disanitasi berada di
`output/instagram_work/instaloader_probe_result.json` dan
`output/instagram_work/instaloader_password_probe_result.json`; keduanya tidak
memuat nilai kredensial, cookie atau isi respons. Library rate controller tidak
dimatikan, max_connection_attempts=1 dan batas subprocess 80 detik.

Instaloader mendokumentasikan pemakaian ulang sesi dan memperingatkan bahwa
restart berulang dapat mengganggu penghitungan rate limit. Bila pengembangan
dilanjutkan setelah akses valid, worker perlu mempertahankan satu konteks/rate
controller sepanjang run. Lihat [penggunaan sebagai module](https://instaloader.github.io/as-module.html)
dan [troubleshooting sesi/rate limit](https://instaloader.github.io/troubleshooting.html).

### Kembali ke instagrapi dan referensi pengguna

Pengguna meminta kembali memakai instagrapi dan mengonfirmasi bahwa login baru
secara manual dengan password lokal berhasil. Instagrapi tetap menjadi backend
class; Instaloader hanya eksperimen preflight sebelumnya. Versi rilis upstream
terbaru yang diperiksa tetap 3.2.2.

[Panduan scraper yang diberikan pengguna](https://instagrapi.com/guides/instagram-scraper-python)
dan [panduan persistensi sesi](https://instagrapi.com/guides/instagrapi-session-persistence)
menempatkan pemuatan settings sebelum `login()`, pemakaian perangkat yang sama,
penyimpanan settings sesudah login, request serial, pagination terbatas dan pacing
sebagai alur dasar. `set_settings/get_settings` adalah padanan in-memory helper
file. Implementasi memakai prinsip tersebut pada login eksplisit; worker akuisisi
hanya memulihkan sesi dan tidak mengulang password login pada setiap request.
Credential tidak ditambahkan ke konfigurasi crawling.

Diagnostik login upstream dijalankan sekali dengan profil/perangkat tersimpan.
CAA mengembalikan HTTP 200 tetapi tidak menerbitkan sesi; alur fallback legacy
mengembalikan HTTP 400 `needs_upgrade`. Tidak ditemukan konteks verifikasi 2FA
yang dapat dilanjutkan. Beberapa request persiapan `qe/sync` mengembalikan 405;
penyebab dan pengaruhnya belum terbukti. Receipt disanitasi tersedia lokal pada
`output/instagram_work/login_diagnostic_current.json`. Status 200 pada CAA tidak
diperlakukan sebagai bukti login berhasil, dan `needs_upgrade` tidak dipakai
untuk menyimpulkan password pengguna salah.

Pemeriksaan kompatibilitas tanpa password login juga mempertahankan UUID perangkat
dan memeriksa hipotesis URL decoding cookie. Pembacaan `accounts/current_user`
gagal HTTP 403 `login_required` pada transport curl dan requests. Tidak ada 429
atau data post yang diperoleh. URL decoding tidak terbukti memperbaiki akses;
implementasi akhir mempertahankan nilai cookie persis sebagaimana diberikan.
Saat impor cookie eksplisit, authorization/cookie lama dibersihkan hanya di memori
sebelum `login_by_sessionid` agar header Bearer lama tidak terbawa ke lookup awal.
Device settings tetap dipertahankan, dan file sesi sebelumnya baru diganti jika
impor serta pembacaan akun privat berhasil.

Validasi impor cookie asli setelah perbaikan header tetap gagal dengan
`AttributeError` dari alur SDK, sebelum sesi baru disimpan. Ini tidak membuktikan
akses berhasil dan tidak mengubah hasil dua pembacaan akun 403 di atas.

### Uji pola persistensi sesi yang dikirim pengguna

Perintah upgrade `pip install --upgrade instagrapi` telah dijalankan pada
`.venv-instagram`; PyPI tetap menyediakan versi 3.2.2 yang sudah terpasang.
Pengguna kemudian meminta pola muat settings, `login()`, tangkap `LoginRequired`
dan `relogin()`, lalu simpan settings setelah berhasil. Mode password eksplisit
di atas mencegah field cookie mengambil alih percobaan ini.

Uji live pola tersebut memuat settings dengan berhasil dan mempertahankan UUID.
Validasi `accounts/current_user` mendapat HTTP 403 `login_required`; SDK otomatis
memanggil alur login dengan `relogin=True`. Dua respons CAA HTTP 200 tidak
menerbitkan sesi/konteks 2FA, lalu fallback legacy HTTP 400 berakhir dengan
`ClientNeedsUpgradeError`. Elapsed **27.15 detik**, `stage: login`, file sesi tidak
berubah. Fallback `relogin()` tambahan di helper tidak dipanggil karena exception
akhir bukan `LoginRequired`. Receipt tanpa kredensial tersedia di
`output/instagram_work/user_session_persistence_result.json`.

Pemeriksaan dua request persiapan tanpa password menunjukkan GET `qe/sync` HTTP
405 tetap menyertakan key ID dan kunci RSA publik yang dapat dibaca. Metode POST
`sync_device_features(login=True)` yang tersedia di SDK mendapat HTTP 500 tanpa
kunci tersebut. Hasil ini belum mendukung mengganti GET menjadi POST sebagai
perbaikan login; tidak ada patch protokol/versi aplikasi yang diterapkan.
Receipt lokal: `output/instagram_work/qe_sync_probe_result.json`.

Referensi ini membantu memeriksa implementasi, tetapi belum menyelesaikan penolakan
autentikasi akun tersebut. Uji live 30 menit dan integrasi SocialCrawler masih
menunggu sesi yang diterima API instagrapi. Tidak ada crawling aktif atau klaim
berhasil berdasarkan fixture maupun workbook kosong.

## Verifikasi dan Docker

Verifikasi setelah perubahan persistensi: **27 tes Instagram lulus; 100 tes crawler
dijalankan, 99 lulus dan 1 tes browser opsional dilewati**. Fixture menguji reuse
perangkat, cookie tidak dipilih dalam mode password, satu pemulihan LoginRequired,
penerusan kode verifikasi, kegagalan terminal tanpa retry dan sesi lama tidak
tertimpa. Tes offline tidak membuktikan akses akun live.

```sh
.venv-instagram/bin/python -m unittest discover -s tests/crawler -p test_instagram_crawler.py -v
.venv-nlp/bin/python -m unittest discover -s tests/crawler -v
docker build -f deployment/docker/Dockerfile.instagram -t beesense-instagram:local .
docker run --rm beesense-instagram:local --dry-run
```

Docker terpisah menjalankan UID10001 dan hanya memasukkan source, config crawl
dan requirements; auth, sesi, data dan virtual environment tidak masuk konteks.
Mount sesi read-only pada `/app/output/instagram/session.json`, baseline read-only
pada `/app/outputs/social_20261028_01`, serta output writable di `/data`, lalu
tambahkan `--output-dir /data/trial_01`. Image crawler/Selenium memasukkan
`social_export.py` sebagai dependency bersama. Dashboard tidak membutuhkan
instagrapi. **No migration required**; kontrak tabel tidak berubah. Build/runtime
Docker perlu diverifikasi saat daemon tersedia.

## Pemulihan HTTP 429 dan Chrome (30 Oktober)

Run pertama berhenti PARTIAL/CONSECUTIVE_SOURCE_ERRORS setelah 2.940 detik: 248 post,
2.128 komentar, 130 root dengan ≥10 komentar. Batas tiga jam dan target 1.000 belum
tercapai. Percobaan pemulihan kedua 25 detik menghasilkan0 record. Pengguna kemudian
mengonfirmasi HTTP 429 pada Chrome; error CLI sebelumnya hanya merekam kegagalan
navigasi, sehingga tidak boleh diklaim sebagai status429 terukur oleh crawler lama.

SocialCrawler 1.5.1 kini menetapkan jeda Instagram360 detik dan maksimum3 retry,
seperti preset Reddit. Waktu tunggu memakai nilai terbesar antara konfigurasi dan
Retry-After. Retry mempertahankan operasi/URL yang sama dan tidak melampaui deadline
global awal16.28WIB. Konfigurasi resume mengecualikan seluruh post tersimpan dan
memakai sisa anggaran; preset utama tetap10.800 detik/target 1.000. Tidak ada crawling
YouTube/Reddit baru, solver, rotasi identitas atau password login ulang.

Browser mengamati status429 dari respons Instagram, termasuk respons main-document
CDP ketika Chrome melempar ERR_HTTP_RESPONSE_CODE_FAILURE sebelum mengembalikan
Response. Hanya status dan Retry-After dipilih; cookie/header otentikasi tidak dicatat.
Respons429 GraphQL yang diminta halaman Instagram juga menghentikan operasi sebelum
scroll berikutnya. Error navigasi umum tetap SOURCE_ERROR, bukan diasumsikan429.

Pada429, challenge, timeout atau errorCLI, Chrome dibiarkan terbuka untuk pemeriksaan.
Penutupan sebelumnya berasal dari finally crawler, bukan pembersihan macOS. Tujuh
belas tes terfokus memeriksa parsing/status/header, kode browser hasil generator,
privasi header, batasretry, Retry-After lebih lama, deadline dan pencegahan duplikasi.
Run03 dijadwalkan setelah cooldown awal berakhir14.47WIB. Hasil final masih menunggu;
training sementara ditunda, lalu pipeline akan menggabungkan ke direktori versi02.
