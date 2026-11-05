# Active backend: BeeSense native TikTok browser crawler

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


TikTokCrawler 2.6.1 / NativeTikTokClient / BeeSenseNative 1.3.0.
Dependencies: Playwright 1.62.0 (Apache-2.0), OpenPyXL 3.1.5 (MIT).
Written in BeeSense; no third-party TikTok SDK is imported. No Chinel0 repository
code was imported after the user cancelled that integration.

The ordinary browser reads hydration, rendered video links and JSON responses
made by the search/comment UI. Only observed native video/comment IDs enter the
shared Dataset/Excel exporter. Scroll and reply controls trigger ordinary loading;
no forged/signed API requests, fingerprint patches, proxy/account rotation or
CAPTCHA solver. Invalid source metadata stays unknown rather than synthesized.

One context receives the local TikTok cookie before navigation. Request pacing
honors shared delay, and server 5xx increases it. HTTP429 persists Retry-After in
an ignored operational cache; subsequent processes stop until that time. Access
barriers terminate acquisition and preserve partial output. Auth is not changed,
profile cookies are not read, and debug bodies/credential values are not exported.

Primary Playwright references consulted:
- https://playwright.dev/python/docs/network
- https://playwright.dev/python/docs/api/class-browsercontext#browser-context-add-cookies
- https://playwright.dev/python/docs/api/class-page#page-goto

Live tests on 2026-11-03: headless 0/500 after 4.79 seconds, headed 0/500 after
11.05 seconds; PARTIAL / ACCESS_BLOCKED. The headed search response was empty or
invalid JSON despite HTTP200. Fixture browser acquisition passed separately.
See docs/crawler/TIKTOK_NATIVE_TRIAL_20261103.md. No promise of unblocked access.


Optional manual preflight2.1 supports an owned visible persistent Chromium profile,
private control-file human confirmation, cancellation and global time budget.
The user cancelled that browser trial and requested their already-open Chrome.
It is not the transport used by the successful small Chrome observation.

ChromeCaptureWorker1.0 imports public records previously observed by the connected
browser agent in the user's existing Chrome tab. It never connects to Chrome,
launches a browser, reads auth/cookies or sends network requests. Same shared
Dataset/Excel/native-ID archive; explicit source beesense_existing_chrome_capture.
Captured1post+10comments,0replies on3November2026; target500 not reached, comments
completeness unverified. Not an unattended Python-to-Chrome integration.
Captures remain in ignored .cache; no credential/profile material is indexed.
See docs/crawler/TIKTOK_CHROME_TRIAL_20261103.md. No migration required.

ChromeLiveWorker1.1 adds a loopback task/result bridge and optional local Chrome
extension. Agent-driven live trial exported2posts,30comments,13replies (45unique)
in638.85seconds before interruption;500target not reached. Source for that trial
was BeeSenseChromeLive1.0.0. New extension1.0.0 captures UI-generated public JSON
through Chrome.debugger and automates the selected TikTok tab. At initial
implementation it was not installed/live-tested; current user-reported
installation and pairing requirements are described in Update2.4.1 below.
Pairing precedes global crawl timer. Public native IDs remain strings; stale
responses, wrong roots and unobserved parents are rejected. See
docs/crawler/TIKTOK_CHROME_LIVE.md for exact permission scope and test evidence.

Update2.4.1: user reports extension installed. Browser policy prevents agent
inspection of chrome://extension/popup pages; pair manually in the selected TikTok
popup. CLI now distinguishes the actual extension transport/version and emits
connection-ready and waiting heartbeats without starting the crawl clock early.
Pairing timeout is explicit and leaves the crawler unstarted.36crawler+10bridge
Python tests pass. Prior45-record trial remains historical, not a new run result.

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

## Kompatibilitas dependency — 5 November 2026

Pin Playwright 1.62.0 dipilih agar environment crawler gabungan kompatibel dengan
Camoufox 0.5.8 yang memerlukan Playwright <1.63. Konflik pin 1.64.1 pada CI lama
diperbaiki tanpa mengubah protokol ekstensi Chrome atau dependency dashboard.
Riwayat trial bertanggal 3 November tetap mencatat versi yang digunakan saat itu.
