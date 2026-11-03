# TikTok: Chrome pengguna dan konektor lokal

TikTokCrawler 2.5.0 memakai ChromeLiveWorker (BeeSenseChromeLive 1.1.0).
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
