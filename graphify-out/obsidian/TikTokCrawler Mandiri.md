---
type: architecture
tags: [beesense, crawler, tiktok, playwright]
source_url: https://playwright.dev/python/docs/network
captured_at: 2026-11-03
---

# TikTokCrawler Mandiri

Backend aktif TikTokCrawler 2.5.0 memakai NativeTikTokClient (BeeSenseNative 1.2.0)
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
