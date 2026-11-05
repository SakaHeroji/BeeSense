---
type: implementation
status: frontend-first
tags: [beesense, frontend, tiktok, chrome, connector]
---

# Frontend TikTok Plugin Chrome

Menu TikTok menyatukan konfigurasi, review, pairing Chrome dan progres dalam satu
transaksi. Form memakai proyeksi publik `config/social_crawler.json`: tanggal
publikasi WIB, include/exclude, 25 query awal, hashtag opsional, target 1.000 post,
batas jam opsional dan Excel lokal default. Seluruh komentar/balasan dicoba
sampai akhir pagination terverifikasi atau batas waktu; hasil parsial dipertahankan.
Login TikTok memakai tab Chrome pengguna, sehingga form username/session ID
TikTok diganti petunjuk Connector. Akun sosmed lain tetap mempunyai form tersendiri.
Petunjuk menjelaskan Chrome/tab tetap terbuka, tab aktif dan jendela tidak
diminimalkan disarankan; popup Connector boleh ditutup. Hindari navigasi/refresh
manual saat plugin menggulir dan membuka balasan; validasi CAPTCHA/login dilakukan
ketika diminta. Ini kebutuhan operasi UI,
bukan klaim penyebab pasti stagnasi run tertentu.

`TikTokConnector.tsx` berada pada monitor JobDetail. Halaman menampilkan alamat
server dashboard dan kode sementara tersembunyi, status koneksi, versi minimum
Connector, validasi manual, aktivitas serta komentar/balasan post aktif. Hitungan
thread sementara tidak dijumlahkan sebagai hasil operasi selesai. Tidak ada ID
baru selama satu menit ditampilkan sebagai kondisi data, bukan bukti Chrome putus.

Job dibuat WAITING_CONNECTOR tanpa startedAt/deadlineAt. Server memulai waktu
tepat sekali setelah handshake kompatibel. Koneksi ulang mempertahankan deadline
dan hasil. Tombol lanjut setelah CAPTCHA meminta verifikasi server; tidak
menganggap validasi selesai hanya karena tombol diklik.

Adapter `api.ts` menyiapkan tiga endpoint privat per job di API proyek yang sama:
GET tiktok-connector, POST tiktok-connector/pairing dan POST tiktok-connector/resume.
Respons diperiksa terhadap job dan origin dashboard, tanpa port bridge tetap.
Pairing hanya tersedia bagi operator dan tinggal di memori halaman, tidak di
snapshot Job publik, URL atau localStorage. Versi minimum mengikuti manifest
publik ekstensi lewat sync-config, tanpa key, permissions atau auth.json.

Ini **frontend terlebih dahulu**. Gateway HTTP dan worker yang menyatukan server
dashboard dengan protokol [[TikTok Chrome Live Connector]] belum diimplementasikan.
Capability tiktokConnectorAvailable harus false/tidak ada sampai layanan siap.
Mode demo memiliki tombol simulasi berlabel yang tidak mengendalikan Chrome
atau [[Pemantauan TikTok 1000 Post 20261105|run live yang sedang berlangsung]].

Desain mengikuti BeeSense putih/oranye dan Plus Jakarta Sans. Alur tiga langkah
menjelaskan urutan kerja, panel koneksi menjadi fokus monitor. Body/input TikTok
16 px, label/petunjuk 14 px, seluruh teks minimal 12 px. Preview lokal berada
di http://127.0.0.1:5173/crawler/tiktok. Backend aktif tidak direstart.

Validasi frontend: 45 Vitest dan 2 tes Node proyeksi, lint, TypeScript dan build
API lulus. Audit/browser desktop dan mobile serta build demo dicatat pada
[delivery](../../Crawler/Frontend/docs/DELIVERY.md). Docker daemon tidak aktif,
sehingga image belum dibangun. Tidak ada perubahan skema: No migration required.

[[Frontend React Crawler]] · [[Frontend Social Media Per Platform]] · [[HOME]]
