# BeeSense TikTok Connector 1.1.0

Pengguna sudah mengonfirmasi pemasangan paket lokal. Uji live versi 1.0.0 menghasilkan 13 post/93 komentar/261 balasan.
Reload paket 1.1.0 sebelum pemakaian berikutnya; perbaikan terbaru diuji offline. Baca [panduan dan hasil nyata](../../../../docs/crawler/TIKTOK_CHROME_LIVE.md).

Ekstensi Manifest V3 tanpa dependensi/kode remote. Dibutuhkan Chrome 118+.
Izin: debugger (inspeksi/kendali halaman dan respons jaringan), activeTab, storage;
host www.tiktok.com dan loopback 127.0.0.1. Chrome memberikan izin debugger luas;
kode hanya menempel pada tab TikTok yang dipilih lewat popup. Pemasangan memerlukan
persetujuan pengguna. Tidak membaca profil/cookie/auth.json atau menyimpan pairing
code. Storage.session hanya berisi status. Tidak memecahkan CAPTCHA otomatis.

Setelah disetujui: Load unpacked folder ini, jalankan CLI --chrome-extension,
buka bridge_url, lalu masukkan alamat lokal dan pairing code ke popup pada tab
TikTok. Lepas debugger lain dari tab itu sebelum Mulai. Stop melepas debugger
sendiri, tanpa menutup Chrome. Batas crawling berjalan setelah pairing berhasil.

Manifest key adalah kunci publik untuk ID extension stabil, bukan rahasia.
File sumber: background.mjs (pengendali), core.mjs (validasi/parser/UI),
popup.html/css/mjs (pairing/status), manifest.json. Tes di
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
