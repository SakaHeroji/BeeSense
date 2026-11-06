---
type: architecture
tags: [beesense, crawler, tiktok, chrome, sidebar, ui]
captured_at: 2026-11-06
---

# Sidebar TikTok Connector 20261106

[[TikTok Chrome Live Connector]] kini memakai sidebar native Chrome versi 1.4.0,
build `20261106-sidebar-v7`. [[TikTok Throughput 20261106]] tetap menjadi algoritma
akuisisinya. Klik ikon BeeSense membuka Side Panel, lalu pilih tab TikTok dan
isi alamat/kode crawler lokal. Popup lama telah dihapus.

Alur: toolbar → sidepanel.html → sidepanel.mjs → runtime message start/continue/
stop → background.mjs → bridge loopback → ChromeLiveWorker → SocialCrawler.
Status berjalan kembali ke storage.session dan UI melalui onChanged. Kode
pairing tidak masuk storage. Counter native ID dihitung setelah batch diterima
bridge; hasil akhir mengikuti filter Python, bukan angka qualified di sidebar.

Form ditampilkan sebelum koneksi, monitor selama berjalan, tombol lanjut hanya
saat CAPTCHA, dan data progres dipulihkan saat sidebar dibuka ulang. Restart
worker meminta pairing ulang. Tutup panel tidak menghentikan pengambilan.

Posisi kanan mengikuti Setelan Chrome → Tampilan → Panel samping → Kanan.
API tidak dapat memaksa posisi. Izin sidePanel ditambahkan tanpa host baru.

Verifikasi: 71 tes Python (8 UI Chromium), 14 Node, 45 Vitest dan 2 sinkronisasi;
lint dan build frontend lulus. SidePanel API asli berhasil dibuka pada Chromium
terisolasi dengan semua HTTP/HTTPS diblokir. Preview memakai fixture, bukan live.
Tidak ada migrasi DB atau deployment. Docker daemon belum aktif.

[Desain, penggunaan dan audit UI](../../docs/crawler/TIKTOK_SIDEBAR_20261106.md).
