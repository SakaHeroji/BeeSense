---
type: architecture
tags: [beesense, crawler, tiktok, playwright]
source_url: https://playwright.dev/python/docs/network
captured_at: 2026-11-03
---

# TikTokCrawler Mandiri

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


Backend aktif TikTokCrawler 2.6.1 memakai NativeTikTokClient (BeeSenseNative 1.3.0)
dan Playwright 1.64.1, tanpa Pyktok/PyTok/TikTokApi. Tidak memakai kode Chinel0 yang
pengguna batalkan. [[TikTokCrawler Pyktok]] dan [[TikTokCrawler TikTok-Api]] riwayat.

[[Konfigurasi Universal Social Crawler]] menyediakan query, tanggal, keyword,
target 1.000, durasi dan cap komentar null. Satu browser biasa memuat halaman
search/tag, membaca hydration, respons jaringan UI dan link native, lalu menggulir
untuk hasil lanjut. Post tanpa metadata harus dibaca dari halaman asli sebelum
lolos filter. Komentar dan balasan diperoleh dari kontrol UI, dengan native ID,
root dan parent yang diverifikasi; tidak membuat ID atau statistik sintetis.

Pacing menggunakan nilai terbesar dari request_interval_seconds dan delay bersama.
scroll_pause_seconds dan idle_scroll_limit mengendalikan UI tanpa kuota harian.
5xx memperlambat request. HTTP429 menyimpan Retry-After ke cache cooldown sehingga
restart tidak melewati masa tunggu. CAPTCHA/login wall/penolakan API menghentikan
akuisisi. Tidak ada proxy, rotasi akun, patch fingerprint atau solver CAPTCHA.

msToken dari auth lokal dipasang sebelum navigasi; auth tidak diubah atau diekspor.
Epoch request mencegah respons terlambat masuk operasi lain. Baris parsial tetap
mengalir ke parent dan diekspor pada timeout. Ini bukan resume cursor komentar
persis; comments_complete tetap false. [[Output Social Media Per Tanggal]] menjaga
ID unik lintas hari; run kosong tidak mengubah arsip.

[[TikTok Mandiri Uji 500 Post 20261103]]: headless 0/500 setelah 4,79 detik, browser
terlihat 0/500 setelah 11,05 detik. Keduanya PARTIAL/ACCESS_BLOCKED, respons search
kosong/bukan JSON walau HTTP200. Fixture browser terpisah berhasil tetapi bukan
bukti sukses live. Panduan `docs/crawler/TIKTOK_CRAWLER.md`, provenance
`Crawler/Backend/Tiktok/NATIVE.md`. No migration required; Docker belum diverifikasi.

[[TikWM Probe TikTok 20261103]] mencoba script pengguna melalui layanan pihak
ketiga. Pencarian pertama HTTP403, 0 video/komentar, exit code2. NativeTikTokClient
tetap backend aktif; konfigurasi dan kredensial tidak berubah.


[[TikTok Chrome Uji 20261103]] memakai tab Chrome pengguna yang sudah login setelah
Chromium manual dibatalkan. Berhasil mengamati1post+10komentar dengan nativeID dan
statistik; target500belum tercapai, komentar belum lengkap. ChromeCaptureWorker
mengimpor artefak publik ke exporter bersama, tanpa membaca auth/cookie, membuka
browser atau mengirim request. Pengambilan live masih dibantu agen browser;
bukan integrasi Python yang otomatis menempel ke sesi Chrome. Provenance terpisah
beesense_existing_chrome_capture; default NativeTikTokClient tidak berubah.

[[TikTok Chrome Live Connector]] menambah penghubung live dan ekstensi otomatis
yang sudah dikonfirmasi terpasang oleh pengguna. Uji agen live2post/30komentar/13balasan tersimpan tanpa ID duplikat,
target500belum tercapai. Pairing lokal di popup TikTok masih wajib diverifikasi sebelum uji ulang.

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
