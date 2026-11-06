# BeeSense TikTok Connector 1.4.0

## Sidebar Chrome — 6 November 2026

Klik ikon BeeSense pada toolbar untuk membuka sidebar native Chrome. UI popup
telah diganti dengan `sidepanel.html/css/mjs`; izin `sidePanel` ditambahkan.
ID ekstensi, host yang diizinkan, protokol komentar dan minimum bridge 1.3.0
tetap kompatibel. Build aktif: `20261106-sidebar-v7`.

1. Reload ekstensi di `chrome://extensions` dari folder ini.
2. Jalankan crawler lokal dan buka tab TikTok yang sudah login.
3. Klik ikon BeeSense, pilih tab, lalu tempel alamat lokal dan kode pasangan.
4. Tekan **Hubungkan & mulai**. Progres post/komentar/balasan muncul di sidebar.
5. Jika CAPTCHA muncul, selesaikan di TikTok lalu tekan **Validasi selesai, lanjutkan**.
6. Tekan **Hentikan pengambilan** untuk melepas tab; data yang diterima tetap ada.

Menutup sidebar tidak menghentikan worker. Membuka kembali memulihkan status
dari `storage.session`. Jika service worker benar-benar dimuat ulang, UI meminta
pairing ulang dan tidak mengklaim koneksi masih berjalan. Kode pasangan tidak
disimpan di storage. Penghitung hanya mencakup native ID record yang diterima
bridge dalam sesi konektor ini; hasil ekspor akhir mengikuti filter Python.

Posisi panel mengikuti pengaturan Chrome. Jika tampil di kiri, pilih
**Setelan → Tampilan → Panel samping → Kanan**. API ekstensi tidak dapat memaksa
posisi panel. [Rincian desain dan pengujian](../../../../docs/crawler/TIKTOK_SIDEBAR_20261106.md).

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


Pengguna sudah mengonfirmasi pemasangan paket lokal. Uji live versi 1.0.0 menghasilkan 13 post/93 komentar/261 balasan.
Reload paket 1.1.0 sebelum pemakaian berikutnya; perbaikan terbaru diuji offline. Baca [panduan dan hasil nyata](../../../../docs/crawler/TIKTOK_CHROME_LIVE.md).

Ekstensi Manifest V3 tanpa dependensi/kode remote. Dibutuhkan Chrome 118+.
Izin: debugger (inspeksi/kendali halaman dan respons jaringan), activeTab, storage, sidePanel;
host www.tiktok.com dan loopback 127.0.0.1. Chrome memberikan izin debugger luas;
kode hanya menempel pada tab TikTok yang dipilih lewat sidebar. Pemasangan memerlukan
persetujuan pengguna. Tidak membaca profil/cookie/auth.json atau menyimpan pairing
code. Storage.session berisi status, nama tab dan hitungan progres sesi. Tidak memecahkan CAPTCHA otomatis.

Setelah disetujui: Load unpacked folder ini, jalankan CLI --chrome-extension,
buka bridge_url, lalu masukkan alamat lokal dan pairing code ke sidebar BeeSense.
Pilih tab TikTok dan lepas debugger lain dari tab itu sebelum menghubungkan. Stop melepas debugger
sendiri, tanpa menutup Chrome. Batas crawling berjalan setelah pairing berhasil.

Manifest key adalah kunci publik untuk ID extension stabil, bukan rahasia.
File sumber: background.mjs (pengendali), core.mjs (validasi/parser/UI),
sidepanel.html/css/mjs (pairing/status), manifest.json. Tes di
`tests/crawler/test_tiktok_chrome_extension.mjs`; server HTTP diuji pada
`tests/crawler/test_tiktok_chrome_bridge.py`.

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
