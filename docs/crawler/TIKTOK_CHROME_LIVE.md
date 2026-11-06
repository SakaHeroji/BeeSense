# TikTok: Chrome pengguna dan konektor lokal

UI aktif versi 1.4.0 memakai sidebar Chrome, build `20261106-sidebar-v7`.
Baca [panduan sidebar dan verifikasi UI](TIKTOK_SIDEBAR_20261106.md).

## Peningkatan throughput — Connector 1.3.0, 6 November 2026

Build `20261106-throughput-v6` menggunakan dua fase per post: kumpulkan komentar
utama sampai akhir pagination sumber (atau cap yang dikonfigurasi), kemudian
rewind panel dan telusuri balasan. Balasan bawaan dalam respons komentar tetap
disimpan; klik balasan ditunda sampai fase kedua.

`platforms.tiktok.comment_stagnation_seconds` default 75 (rentang 60–90).
Hanya ID komentar/balasan baru yang mereset timer; respons berulang atau metadata
post tidak meresetnya. Post yang stagnan mengirim status `PARTIAL` dan warning
`comment_stagnation_timeout`. Koordinator mengekspor progres, melanjutkan kandidat
baru dan pencarian, lalu mencoba ulang post parsial. `partial_retry_limit`
default 1 (rentang 0–3). Retry tetap tunduk target, deadline global dan cap post;
retry tidak menambah hitungan post yang dicoba atau menggandakan native ID.
Antrean belum selesai tersimpan dalam `tiktok_retry_queue.json` di bundle beserta
checksum manifest; tidak otomatis diimpor oleh run baru. `comments_complete`
tetap false. PARTIAL tidak lagi menghentikan seluruh kampanye.

Jeda minimum tetap mengikuti `request_interval_seconds` / `scroll_pause_seconds`.
Penalti idle tambahan dihapus. Setelah aksi, controller menunggu request relevan
beserta body respons, maksimal 10 detik; `Network.loadingFailed` melepaskan request.
Respons post lain tidak memengaruhi barrier, pacing atau data post aktif.
Backoff HTTP 5xx adalah 5/10/15 detik (maksimum 15), reset setelah HTTP 2xx.
Tiga 5xx beruntun memicu pause minimal 30 detik dan menghormati Retry-After yang
lebih panjang. Status pause dibagikan antar tugas agar perpindahan post tidak
melewati cooldown. 401/403/429 dan CAPTCHA tetap memakai penanganan sebelumnya.

Bridge mensyaratkan Connector >=1.3.0 agar timer run tidak dimulai dengan kode
lama. Reload ekstensi dari `Crawler/Backend/Tiktok/chrome_extension` dan pairing
ulang sebelum uji live. Izin dan ID ekstensi tidak berubah. Tidak ada migrasi DB.
Dockerfile native tetap menyalin package lengkap; Docker daemon lokal tidak aktif,
sehingga rebuild belum diverifikasi. Jalankan ketika Docker tersedia:
`docker build -f deployment/docker/Dockerfile.tiktok -t beesense-tiktok:local .`
lalu `docker run --rm beesense-tiktok:local --dry-run`.

Pengujian menggunakan fixture offline, termasuk 1.200 komentar +100 balasan
sintetis, bukan bukti kecepatan TikTok live. Uji yang diminta berikutnya: target
50 post, maksimal 3.600 detik, timer dimulai setelah pairing versi/build terverifikasi.


## Run awal selesai dan restart — 5 November 2026

Run 6cd0ad73 berakhir parsial sekitar 14.26 WIB: 5 post, 458 komentar dan 479
balasan, total 942 ID native unik, nol duplikat, 12 checksum manifest cocok.
Target 1.000 dan kelengkapan komentar belum tercapai. Pengguna memperpanjang
batas ke 16.00 WIB lalu meminta melewati post 7615256610599898389 dan restart.
Kelanjutan 56cf3232 diinterupsi; 118 barisnya seluruhnya merupakan ID yang sudah
tersimpan, bukan tambahan. Run baru be2ee5c5 dimulai 14.38.45 WIB dengan
Connector 1.2.3 dan target baru 1.000 post, mengantrekan seluruh 25 query root,
mengecualikan post lama, dan tetap mengambil seluruh komentar yang tersedia
sampai pagination terverifikasi atau deadline. Hasil lama dipertahankan.

CLI memperbaiki penanda synthetic untuk worker live; manifest lama tidak diubah.
Operasi yang diinterupsi dapat kehilangan source_version sehingga label adapter
menjadi native-browser. Pemeriksaan kelanjutan mengizinkan label itu hanya pada
run interupsi yang handshake live-nya sudah diaudit. Detail checkpoint dan bukti
ada di pemantauan Obsidian; tidak ada klaim semua komentar atau target tercapai.

## Koreksi viewport komentar — Connector 1.2.3, 5 November 2026

Pengamatan lanjutan pukul 12.05 WIB pada run yang sama: Connector 1.2.2 sudah
terverifikasi, tetapi post `7615256610599898389` tetap pada 19 komentar dan 74
balasan dari statistik sumber 273. Uji DOM baru membuktikan kondisi yang terlewat:
`getClientRects()` masih tersedia untuk tombol yang terpotong di atas panel.
Memilih tombol lama tersebut memicu `scrollIntoView()` kembali ke atas, sehingga
guliran ke halaman komentar berikutnya tidak maju.

Connector 1.2.3, build `20261105-comment-viewport-v5`, hanya membuka kontrol
balasan yang beririsan dengan viewport dan area gulir komentar yang terlihat.
Batas clipping setiap ancestor diperiksa, termasuk overflow auto/scroll/hidden.
Kontrol di luar layar dikunjungi ketika guliran normal mencapai posisinya, bukan
dengan melompat kembali ke tombol pertama. Perbaikan 1.2.2 tetap dipakai: retry
per kontrol, giliran scroll setelah tiga klik tanpa data, dan rewind setelah
bawah daftar. Popup menampilkan hitungan komentar/balasan dan aksi navigasi.

Tujuh fixture DOM offline, 11 tes Node, dan 53 tes TikTok/bridge lulus. Fixture
viewport gagal pada 1.2.2 dengan klik ke induk lama; pada patch baru ia membuka
balasan induk yang sedang terlihat tanpa mengubah guliran kembali ke atas.
Ini bukti regresi offline, bukan klaim seluruh komentar live sudah terambil.
Patch perlu Reload dan pairing ulang; versi/build aktif harus dibuktikan dari
handshake bridge. Run dan deadline 14.25 WIB dipertahankan saat reconnect.

Pada 12.19.54 WIB bridge memverifikasi Connector **1.2.3** dengan build tersebut
dan kebijakan `source-pagination-v3`. Thread yang tertahan kemudian mencapai
79 komentar/114 balasan pada 12.33 dan 97 komentar/114 balasan pada checkpoint
13.10 WIB. Operasi selesai saat itu tetap 4 post/302 komentar/363 balasan;
thread aktif belum termasuk. Run masih berjalan, bukan hasil akhir atau bukti
target 1.000 maupun seluruh statistik sumber sudah tercapai.

Frontend TikTok kini menyiapkan konfigurasi, pairing dan monitor pada transaksi
yang sama. Lihat `Crawler/Frontend/docs/API_CONTRACT.md`: gateway HTTP terintegrasi
masih kontrak tahap berikutnya, preview berlabel demo tidak mengendalikan run CLI.


## Investigasi guliran dan patch Connector 1.2.2 — 5 November 2026

Run `social_20261105T042526Z_6cd0ad73` mulai pukul 11.25 WIB, target
1.000 post, seluruh komentar/balasan, sampai paling lama 14.25 WIB. Handshake
awalnya memverifikasi Connector 1.2.1, build `20261105-comment-tab-v3`.
Pada post `7696082885442293012`, hitungan sempat berhenti pada 91 komentar dan
51 balasan meskipun tab Comments aktif dan tombol View replies masih tersedia.
Setelah pengguna mengklik balasan, data kembali mengalir dan operasi berakhir
pukul 11.46 WIB dengan 155 komentar dan 81 balasan. Total 236 masih di bawah
statistik sumber 239; akhir pagination tidak membuktikan semua komentar yang
tercantum dalam statistik tersedia. Run berlanjut ke post berikutnya.

Uji offline mereproduksi tiga masalah pada kode lama: tombol balasan tanpa hasil
dapat terus diulang sehingga tidak pernah scroll; label balasan yang sama dapat
memakai kunci kontrol induk yang salah; pemilihan panel dapat mengenai wrapper
luas sebelum daftar komentar sebenarnya. Patch 1.2.2, build
`20261105-reply-scroll-v4`, memprioritaskan daftar komentar, membedakan kontrol
per induk/posisi, menunda percobaan ulang per kontrol, dan menjamin scroll setelah
tiga percobaan tanpa data. Batas tiga ini hanya mengatur pergantian aksi UI;
bukan batas jumlah komentar atau alasan menghentikan pengambilan. Guliran
menelusuri hingga bawah sebelum kembali ke atas. Selesai tetap memerlukan bukti
akhir pagination komentar dan balasan atau berhenti dengan status parsial.

Patch pada disk tidak otomatis mengganti worker ekstensi yang sudah dimuat.
Setelah Reload 1.2.2 dan pairing ulang ke bridge yang sama, tugas aktif dapat
dibaca kembali; bridge mempertahankan native ID yang sudah diterima sehingga
pengiriman ulang tidak menambah duplikat. Deadline run tidak direset. Pergantian
versi/handshake harus diverifikasi sebelum mengklaim patch aktif.

Pukul 11.56 WIB, setelah Reload dan pairing ulang oleh pengguna, bridge benar-benar
memverifikasi versi 1.2.2, build `20261105-reply-scroll-v4`, protokol
`source-pagination-v3`. Python dan run ID tetap sama; deadline tetap 14.25 WIB.
Checkpoint setelah 30 menit: 4 post, 302 komentar, 363 balasan dari operasi yang
sudah selesai, belum termasuk thread berjalan. Target 1.000 belum tercapai.

Run memakai semua 25 query root dan semua include/exclude keyword dari
`config/social_crawler.json`. Include memakai mode `any`; komentar dan balasan
tidak memerlukan kecocokan keyword karena `comment_exclude_keywords` kosong.
Semua query masuk antrean, tetapi belum tentu sempat dieksekusi dalam tiga jam.

Validasi patch: 53 tes TikTok/bridge, 11 tes Node, dan 6 fixture DOM offline lulus.
Fixture tidak menghubungi TikTok dan tidak dihitung sebagai hasil crawling nyata.


## Pembaruan 5 November 2026: pagination komentar dan konektor 1.2.1

Perbaikan lanjutan1.2.1 mewajibkan pemilihan tab Comments/Komentar, termasuk ketika
You may like sedang aktif dan wrapper komentar tetap terlihat. Tombol balasan
dibatasi pada panel komentar; teks View more pada rekomendasi tidak diklik.
Redirect username diterima hanya jika origin dan ID post tetap sama. Error kontrol,
perubahan halaman dan timeout Chrome dicatat sebagai kode tetap tanpa signed URL.
Progres streaming mencatat post/komentar/balasan sebelum thread selesai.
Empat fixture DOM offline lulus, termasuk layout Comments(600)/You may like.

Run live1.2.0 `social_20261105T041318Z_3a84237a` menyimpan4post/92komentar/52balasan
(148record) dalam181,29detik sebelum CONSECUTIVE_SOURCE_ERRORS. Satu post mengekspor
40komentar+33balasan, cocok dengan statistik73 dan akhir pagination terverifikasi.
Target1000 belum tercapai; comments_complete false. Arsip35332IDunik/0duplikat.
Ini hasil TikTok nyata, berbeda dari1200komentar/100balasan pada fixture sintetis.
Pengguna mengamati You may like aktif pada post yang komentarnya terlewati; patch
1.2.1 ditujukan pada kondisi tersebut. Error sumber run1.2.0 tidak memuat penyebab
rinci, sehingga fixture bukan bukti bahwa semua penyebab live sudah terselesaikan.


TikTokCrawler 2.6.1 / BeeSenseNative 1.3.0 / BeeSenseChromeLive 1.2.1 memakai
Connector 1.2.1, build `20261105-comment-tab-v3`, kebijakan `source-pagination-v3`.
Tidak menambah izin Chrome, dependensi runtime, file konfigurasi atau migrasi DB.
Konfigurasi bisnis tetap `config/social_crawler.json`; auth.json tidak diubah.

Pada run sebelumnya pengguna melaporkan plugin 1.1.0, tetapi sembilan thread
berakhir dengan `visible_pagination_idle` saat komentar/balasan tanpa cap.
Contoh post memiliki statistik 73 komentar, sementara tidak ada komentar yang
terekam. Ini membuktikan hasil parsial, bukan membuktikan versi yang dipasang salah.
Angka `timeout_seconds: 90` pada audit adalah timeout konfigurasi, bukan bukti
operasi dipotong pada 90 detik; anggaran Chrome live mengikuti deadline global.

Perbaikan tidak menekan toggle ketika panel komentar sudah terbuka. Gulir thread
hanya menargetkan kontainer komentar, bukan video/feed di bawahnya. Balasan pada
parent yang terlihat dimuat sebelum daftar utama digulir; kontrol lambat dicoba
kembali dan daftar ditelusuri ulang. Akhir top-level dan balasan diverifikasi dari
pagination sumber. Respons kosong belum membuktikan lengkap ketika sumber
menyatakan ada komentar. Tidak ada batas jumlah komentar/balasan lokal; deadline,
Stop, CAPTCHA, login dan rate limit tetap berlaku. Selisih statistik sumber
terhadap data terbaca diberi warning, bukan diisi data buatan.

Sebelum timer mulai, bridge memeriksa versi, build dan kebijakan komentar dari
kode konektor yang berjalan. Nomor versi manifest saja tidak cukup. Klien lama
atau tanpa protokol ditolak HTTP409 sebelum crawling_started; popup/halaman lokal
menjelaskan perlunya Reload. Batch thread tanpa bukti akhir pagination ditandai
COMMENTS_INCOMPLETE dan menghentikan run; idle pada mode tanpa cap memerlukan
pembaruan klien. Keduanya mempertahankan data parsial dan tidak dihitung sukses.
Global comments_complete tetap false karena cakupan komentar tersembunyi/dihapus
tidak dapat dibuktikan melalui UI. Tidak ada rekayasa request API atau solver CAPTCHA.

Pengujian offline:247 tes crawler OK (4 dilewati dalam environment umum); tiga
tes DOM pada Chromium headless terisolasi lulus terpisah. Sebelas tes Node lulus,
termasuk **1.200 komentar + 100 balasan sintetis** dari beberapa halaman lambat,
chunk <=500 event dan tanpa duplikasi. Angka ini fixture, bukan hasil TikTok nyata.
Tes DOM memeriksa toggle idempoten, kontainer gulir/rewind, serta tombol balasan
Inggris/Indonesia. Handshake, autentikasi HTTP loopback dan bukti selesai diuji.

Uji live yang dihentikan pengguna:run `social_20261105T035305Z_fb80d44c`,246,66detik,
**9 post + 32 komentar + 8 balasan =49 record**,0duplikat dalam bundle, status
INTERRUPTED, target1.000 belum tercapai. Dua belas checksum bundle terverifikasi;
arsip35230IDunik/0duplikat. Excel harian di `outputs/crawling/tiktok/2026-11-05/`.
Finalisasi organizer lokal dipulihkan setelah interrupt; tidak ada crawling baru
selama pemulihan. Setelah pengguna meminta ulang, run baru memakai handshake1.2.1;
hasil akhirnya belum termasuk pada angka trial yang dihentikan ini.

Untuk penggunaan berikutnya, Reload ekstensi dari folder
`Crawler/Backend/Tiktok/chrome_extension`, lalu pairing ulang dengan kode proses
Python yang aktif. Popup menampilkan versi dan build. Paket ZIP lokal dibuat dari
allowlist file publik; tidak memuat auth, profil browser atau output crawling.
Streamlit tidak diredeploy; tidak ada penulisan PostgreSQL. Docker native build
belum diverifikasi ulang; bridge ekstensi desktop tetap dijalankan di host.


TikTokCrawler 2.6.1 memakai ChromeLiveWorker (BeeSenseChromeLive 1.2.1).
NativeTikTokClient tetap backend bawaan. Semua jalur memakai TikTokAdapter,
SocialCrawler, validasi native ID, filter, exporter Excel dan organizer WIB bersama.
Tidak ada konfigurasi bisnis kedua: query, tanggal, include/exclude, jumlah post,
komentar/balasan dan pacing tetap dari `config/social_crawler.json`.

## Status akhir 3 November 2026 — crawler dihentikan

Uji ekstensi terpasang dengan TikTokCrawler 2.4.1 / BeeSenseChromeLive 1.1.0
menyimpan **13 post, 93 komentar, 261 balasan (367 record unik)** dalam 656,6 detik.
Run `social_20261103T094828Z_23fb8a79` berstatus INTERRUPTED; target 500 belum
tercapai (kurang 487). Dua belas kandidat di luar tanggal dan dua kandidat tanpa
include keyword disaring. `comments_complete: false`; angka komentar pada TikTok
bukan jumlah yang sudah diperoleh. Excel: `outputs/crawling/tiktok/2026-11-03/social_data.xlsx`.
Arsip gabungan setelah run: **35.197 ID unik, 0 duplikat native ID**.

TikTokCrawler **2.5.0**, BeeSenseNative **1.2.1**, dan Connector **1.1.0** memperbaiki
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

## Alur otomatis yang disiapkan

Chrome extension pada `Crawler/Backend/Tiktok/chrome_extension` menempel pada satu
tab TikTok yang dipilih pengguna. Python membuka penghubung loopback 127.0.0.1;
extension melakukan polling tugas search/thread dan mengirim batch data publik.
Chrome.debugger menangkap JSON yang memang diminta UI TikTok melalui Network
getResponseBody. Navigasi, gulir dan tombol balasan biasa memicu pemuatan halaman;
tidak membuat signature, replay request bertoken, rotasi IP/akun atau solver CAPTCHA.

Native integer panjang dipertahankan sebagai string sebelum JSON.parse sehingga
ID video/komentar tidak dibulatkan. Epoch operasi dan video ID mencegah respons
terlambat masuk thread lain. Hydration pencarian SPA yang mungkin berasal dari
homepage diabaikan. Root thread harus cocok dengan ID tujuan; parent balasan harus
teramati. Data tanpa ID asli tidak dibuatkan ID sintetis. Batch dikirim bertahap
maksimal 500 event; pengakuan server mendahului penandaan ID terkirim.

Pencarian berhenti setelah idle_scroll_limit putaran tanpa ID baru. Komentar tanpa
cap menunggu akhir pagination sumber dan semua balasan parent yang teramati.
Kontrol lambat dicoba lagi dengan backoff; tiga putaran idle tidak menyatakan habis.
Jeda mengikuti scroll_pause_seconds dan request_interval_seconds. HTTP429 berhenti
dan menyimpan Retry-After ke cache operasional bersama, termasuk untuk run baru.
HTTP401/403 menghentikan operasi. CAPTCHA menjeda aksi sampai manusia menyelesaikan
dan menekan Lanjutkan di popup; deadline global tetap berlaku. Tidak menjamin bebas
blokir. Kelengkapan komentar tetap tidak diklaim. UI/capture selector TikTok dapat
berubah; konektor mengembalikan hasil parsial atau error saat sumber tidak tersedia.

## Izin, koneksi, dan pengoperasian setelah persetujuan

Manifest meminta `debugger`, `activeTab`, `storage`, host www.tiktok.com dan
127.0.0.1. Izin debugger dari Chrome bersifat luas; kode konektor membatasi operasi
ke tab TikTok terpilih. Izin ini dapat membaca/mengendalikan halaman serta respons
jaringan. Kode tidak membaca cookie/profile, auth.json, password atau request header;
hanya field publik yang diizinkan dikirim ke Python lokal. Kode pairing sementara
hanya ada pada halaman lokal dan memori ekstensi, tidak disimpan ke storage/log.
Storage.session hanya menyimpan status. Tidak ada dependensi atau kode remote.
Kunci publik manifest menjaga ID/origin extension tetap stabil; bukan kredensial.

1. Setelah disetujui, muat folder ekstensi melalui Chrome Load unpacked.
2. Lepaskan pengendali debugger lain dari tab TikTok itu. Jangan tutup Chrome.
3. Jalankan Python di host lokal yang sama (mode ini bukan koneksi Docker):

```sh
.venv-tiktok/bin/python -m Crawler.Backend.tiktok_crawler \
  --chrome-extension --target-posts 500 --total-seconds 1800
```

4. Buka bridge_url lokal yang dicetak. Salin URL dan pairing code dari bagian
   Connect BeeSense extension ke popup konektor pada tab TikTok yang dipilih.
5. Tekan Mulai di tab TikTok ini. Batas 30 menit baru dimulai setelah konektor
   melakukan pairing; waktu pemasangan tidak dihitung sebagai crawling. Pairing
   memiliki batas tunggu tersendiri 600 detik. Kode yang salah/origin asing ditolak.
6. Jika CAPTCHA muncul, selesaikan sendiri di TikTok lalu tekan Lanjutkan. Stop
   melepas debugger konektor sendiri, tidak menutup tab atau browser pengguna.

`--chrome-live` tetap menyediakan transport agen/form lokal untuk diagnosis.
`--chrome-capture` tetap importer offline, berbeda dari koneksi live. Kedua mode
Chrome tidak membaca msToken dari auth. `--dry-run --chrome-extension` tidak membuka
port, browser atau jaringan dan tidak membaca auth. Jangan mengekspos bridge lewat
proxy/LAN. Koneksi hanya localhost dan pairing berlaku sampai proses dihentikan.

## Verifikasi

```sh
.venv-tiktok/bin/python -m unittest discover -s tests/crawler -p test_tiktok_crawler.py -v
.venv-tiktok/bin/python -m unittest discover -s tests/crawler -p test_tiktok_chrome_bridge.py -v
node --test tests/crawler/test_tiktok_chrome_extension.mjs
```

39 tes crawler, 10 tes bridge dan 10 tes Node lulus pada pembaruan 2.5.0. Tes bridge memakai HTTP loopback nyata,
stream ke Excel bersama, autentikasi origin/Bearer, expiry, caps, parent, dedup,
Retry-After persisten dan durasi unlimited yang valid JSON. Tes Node memeriksa
presisi native ID, URL/task, parent balasan, Retry-After, cleanup debugger gagal,
dan pengendali dengan API Chrome serta jaringan simulasi. Perbaikan pagination 1.1.0 belum diuji live kembali; hasil ekstensi 1.0.0
yang terpasang dicatat di atas.

No migration required; tidak ada perubahan skema atau penulisan PostgreSQL.
Docker CLI native tetap memakai Dockerfile.tiktok, menyalin package termasuk
manifest. Bridge sengaja loopback dan tidak diekspos dari container; konektor untuk
Chrome desktop berjalan di host. Docker build/start belum diverifikasi: akses ke
socket Docker lokal ditolak. Perintah tersisa untuk image native:

```sh
docker build -f deployment/docker/Dockerfile.tiktok -t beesense-tiktok:local .
docker run --rm beesense-tiktok:local --dry-run
```

Referensi resmi: [Chrome debugger](https://developer.chrome.com/docs/extensions/reference/api/debugger),
[Network.getResponseBody](https://chromedevtools.github.io/devtools-protocol/tot/Network/#method-getResponseBody),
[service worker lifecycle](https://developer.chrome.com/docs/extensions/develop/concepts/service-workers/lifecycle).

## Pembaruan 2.4.1 setelah pemasangan oleh pengguna

Plan dan dry-run membedakan existing_chrome_extension dari transport agen serta
menampilkan versi ekstensi/bridge yang sebenarnya, bukan Playwright untuk jalur
Chrome. CLI mencetak chrome_extension_connected setelah pairing dan sebelum run;
heartbeat menandai crawling_started false setiap 15 detik selama menunggu.
Pairing timeout mengembalikan CHROME_PAIRING_TIMEOUT dan tidak memulai crawler.
Tes CLI membuktikan konstruktor crawler belum dipanggil saat pairing berlangsung,
serta batas uji 500 post/1800 detik diteruskan setelah koneksi berhasil.

Pengendali browser agen tidak dapat membuka chrome://extensions atau popup internal;
pengguna melakukan pairing dari popup pada tab TikTok sendiri. Daftar seluruh tab
pribadi tidak diambil. Ini batas alat browser, bukan bukti ekstensi gagal dipasang.
Jangan membaca profil, memakai CDP mentah, atau mem-proxy halaman internal sebagai
jalan memutari penolakan. Penghubung HTTP lokal milik aplikasi tetap dapat dibuka.
