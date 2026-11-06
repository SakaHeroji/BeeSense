---
type: architecture
tags: [beesense, crawler, tiktok, chrome]
captured_at: 2026-11-03
---

# TikTok Chrome Live Connector

Pembaruan aktif pada disk: Connector **1.4.0**, build `20261106-sidebar-v7`.
[[Sidebar TikTok Connector 20261106]] mengganti popup dengan panel Chrome native.
Lihat [[TikTok Throughput 20261106]] untuk kebijakan stagnasi, dua fase dan retry.
Hasil final uji 1 jam: 10 post, 1.348 komentar, 481 balasan; target 50 belum tercapai.


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
ada di [[Pemantauan TikTok 1000 Post 20261105]]; tidak ada klaim semua komentar atau target tercapai.

## Koreksi viewport komentar — Connector 1.2.3, 5 November 2026

Verifikasi live terbaru: bridge menerima versi 1.2.3/build
`20261105-comment-viewport-v5` pada 12.19.54 WIB. Post yang tertahan kemudian
naik dari 19 komentar/74 balasan menjadi 42 komentar/79 balasan. Run dan
deadline 14.25 WIB tetap sama. Lihat [[Pemantauan TikTok 1000 Post 20261105]]
untuk checkpoint; run masih berjalan dan target belum dinyatakan tercapai.

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


TikTokCrawler2.6.1 memakai ChromeLiveWorker1.2.1 dan ekstensi lokal1.2.1.
[[TikTokCrawler Mandiri]] tetap default NativeTikTokClient. Konfigurasi universal,
TikTokAdapter, SocialCrawler dan exporter Excel bersama tetap dipakai. Python
loopback mengirim tugas search/thread; ekstensi mengendalikan satu tab TikTok yang
dipilih dan menangkap respons JSON asli UI lewat Chrome.debugger. ID panjang
menjadi string sebelum parsing, root/parent/epoch diverifikasi, batch diakui server
sebelum ditandai terkirim. Tidak membaca cookie/profil/auth atau merekayasa signature.

Uji live transport agen 3November2026:2post+30komentar+13balasan=45record unik,
0duplikat,638.85detik,INTERRUPTED;target500belumtercapai,comments_complete false.
Output harian outputs/crawling/tiktok/2026-11-03/social_data.xlsx; arsip34830ID unik
pada10partisi. [[TikTok Chrome Uji 20261103]] adalah observasi/impor sebelumnya.

Pengguna sudah mengonfirmasi ekstensi terpasang. Pairing lokal telah berhasil pada uji versi1.0.0. Pembaruan1.1.0 diuji offline. Izin debugger luas dapat membaca dan
mengendalikan halaman/jaringan; kode membatasi ke tab TikTok pilihan dan localhost.
Halaman internal Chrome diblokir alat agen; pairing dilakukan pengguna di popup. Pairing sementara mendahului timer crawling.
CAPTCHA ditangani manusia lalu Lanjutkan, tetap tunduk deadline; 429 menyimpan
Retry-After dan menghentikan run baru selama cooldown. Tombol balasan lambat dicoba kembali;
komentar tanpa cap menunggu pagination sumber atau deadline, data parsial tetap masuk Excel. Tidak menjamin bebas blokir.

39tescrawler+10tesHTTPbridge+10tesNode lulus; tes Node parser/pengendali simulasi terpisah.
Ini bukan bukti kecepatan live500post. No migration required. Image Docker native
belum dibangun karena akses socket ditolak; bridge desktop berjalan di host lokal.
Panduan docs/crawler/TIKTOK_CHROME_LIVE.md; paket Crawler/Backend/Tiktok/chrome_extension.

Versi2.4.1 membedakan transport existing_chrome_extension dan versi manifest pada
plan/dry-run; event koneksi sebelum run, heartbeat menunggu tanpa menghitung waktu,
dan status CHROME_PAIRING_TIMEOUT tanpa memulai crawler. Tidak membaca daftar
seluruh tab privat atau memutari larangan halaman internal Chrome. Hasil lama
2post/30komentar/13balasan tetap riwayat, bukan hasil uji ulang ekstensi.

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
