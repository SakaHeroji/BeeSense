---
type: run-monitor
tags: [beesense, crawler, tiktok, monitoring]
captured_at: 2026-11-05
---

# Pemantauan TikTok 1000 Post — 5 November 2026

Status: **seluruh rangkaian dihentikan pada batas 16.00 WIB; hasil parsial terverifikasi**. Angka checkpoint
dibedakan dari hasil final setiap segmen. Batas keseluruhan diperpanjang oleh
pengguna menjadi **16.00 WIB**, bukan total durasi empat jam.
Run `6cd0ad73-adb8-4138-8935-54317a83bfb7` mulai 11.25.26 WIB dengan target
1.000 post dan seluruh komentar/balasan, paling lama sampai 14.25.26 WIB.
Python dijalankan melalui caffeinate; Chrome pengguna tetap milik pengguna.
Simpanan lokal Excel, tanpa PostgreSQL atau redeploy Streamlit.

Konfigurasi memakai 25 query dan seluruh include/exclude keyword pada
`config/social_crawler.json`. Include mode `any`: kuliah, kampus, universitas,
beasiswa, jurusan. Komentar tidak perlu cocok keyword. Batas komentar dan
balasan `null`; semua query mengantre, belum tentu semuanya sempat berjalan.

## Checkpoint setiap 15 menit

Kolom thread berjalan adalah **komentar utama / balasan** yang belum masuk
hitungan operasi selesai. Jangan menjumlahkannya sebagai hasil Excel final.

| Waktu WIB | Post selesai | Komentar selesai | Balasan selesai | Thread berjalan |
| --- | ---: | ---: | ---: | --- |
| 11:40:26 | 1 | 0 | 0 | 91 / 51 |
| 11:55:27 | 3 | 197 | 114 | 105 / 249 |
| 12:10:28 | 4 | 302 | 363 | 19 / 74 |
| 12:25:29 | 4 | 302 | 363 | 59 / 99 |
| 12:40:30 | 4 | 302 | 363 | 79 / 114 |
| 12:55:26 | 4 | 302 | 363 | 79 / 114 |
| 13:10:27 | 4 | 302 | 363 | 97 / 114 |
| 13:25:27 | 4 | 302 | 363 | 97 / 114 |
| 13:40:28 | 4 | 302 | 363 | 97 / 114 |
| 13:55:29 | 4 | 302 | 363 | 117 / 114 |
| 14:10:30 | 4 | 302 | 363 | 117 / 114 |
| 14:25:31 | 5 | 458 | 479 | — |

Snapshot 11.55.27 masih memuat tiga post selesai; sesudah operasi berakhir,
checkpoint 11.55.47 menjadi 4 post, 302 komentar, dan 363 balasan.

## Perbaikan dan verifikasi live

Pada post `7696082885442293012`, 91 komentar dan 51 balasan sempat tidak
bertambah meskipun Comments aktif. Setelah klik balasan manual oleh pengguna,
operasi selesai dengan 155 komentar dan 81 balasan; total 236 masih di bawah
statistik sumber 239. Tidak ada klaim semua komentar dalam statistik terambil.

Connector 1.2.2 diverifikasi sekitar 11.56 WIB. Pada post berikutnya
`7615256610599898389`, data kembali tertahan pada 19 komentar dan 74 balasan
sementara statistik sumber 273. Uji offline menemukan tombol di luar area
komentar yang terpotong masih lolos getClientRects; scrollIntoView menarik
posisi kembali ke tombol lama di atas.

Pada 12.19.54 WIB, bridge memverifikasi Connector **1.2.3**, build
`20261105-comment-viewport-v5`, protokol `source-pagination-v3` setelah Reload
dan pairing ulang pengguna. Run ID dan deadline tetap sama. Hitungan thread
tersebut kemudian bertambah menjadi **42 komentar dan 79 balasan** pada
12.22 WIB. Ini bukti data live kembali mengalir, bukan bukti seluruh thread
atau target 1.000 sudah selesai.

Pada 12.33 WIB thread aktif mencapai 79 komentar dan 114 balasan, masih sama
pada checkpoint 12.55. Pengguna melaporkan popup “menggulir komentar” dan
daftar terus turun dengan komentar yang tampak baru. Gerakan UI tidak membuktikan
ID native baru; monitor tetap menghitung ID unik yang diterima, tanpa menandai
273 statistik sumber sebagai sudah lengkap.

Pemeriksaan sekitar 13.45 WIB: server bridge masih merespons HTTP 200 dan
menampilkan handshake terakhir Connector 1.2.3. ID terakhir masuk 13.06.47 WIB;
97 komentar/114 balasan belum bertambah sekitar 39 menit. Tidak ada exception,
CAPTCHA atau detach baru di log. Dua SOURCE_ERROR pada 11.26 dan 11.55 adalah
kejadian lama, bukan bukti error baru pada 13.45. Bridge tidak mencatat heartbeat
guliran saat tanpa data, sehingga HTTP 200/handshake tersimpan tidak membuktikan
plugin masih bergerak. Ini indikasi stagnasi, bukan keberhasilan pengambilan.
Mode seluruh komentar menunggu akhir pagination atau deadline; proses hidup dapat
tetap tertahan pada satu post. Status popup terbaru diminta untuk membedakan loop
UI tanpa ID baru dari worker/koneksi yang berhenti merespons.

Pengguna kemudian memastikan daftar masih bergerak dan popup masih menunjukkan
“menggulir komentar”. Pada 13.51.17 WIB data baru masuk: thread menjadi
117 komentar/114 balasan, bertambah 20 komentar. Ini memperbarui diagnosis:
terjadi jeda panjang tanpa ID, tetapi bukan bukti proses sepenuhnya berhenti.
Chrome dan tab harus tetap terbuka; tab aktif/jendela tidak diminimalkan disarankan
untuk operasi UI, popup boleh ditutup. [Chrome menjelaskan pembatasan aktivitas
halaman latar](https://developer.chrome.com/blog/background_tabs), tetapi tidak ada
log visibility yang membuktikan itulah penyebab jeda run ini.

Patch hanya membuka balasan yang beririsan dengan viewport dan clipping
ancestor, memisahkan identitas kontrol, mencoba ulang per kontrol, serta memberi
giliran scroll setelah tiga klik tanpa data. Tiga klik adalah cadence navigasi,
bukan batas komentar atau penghentian thread. Popup menampilkan jumlah dan aksi.
Validasi: 7 fixture DOM offline, 11 tes Node, 53 tes TikTok/bridge lulus.

[[TikTok Chrome Live Connector]] menjelaskan detail penelusuran dan uji regresi.
## Final run awal dan restart

Run `6cd0ad73` selesai pada 14.26 WIB dengan status PARTIAL/TIME_BUDGET_EXHAUSTED:
**5 post, 458 komentar, 479 balasan = 942 ID native unik**, tanpa ID duplikat.
Seluruh 12 checksum berkas manifest cocok. Target 1.000 dan kelengkapan seluruh
komentar belum tercapai. Thread terakhir memperoleh 156 komentar/116 balasan,
total 272 dari statistik 273, tanpa bukti akhir pagination yang lengkap.
Arsip gabungan ketika itu memuat 36.139 ID unik dalam 11 partisi, tanpa duplikat.

Kelanjutan `56cf3232` terhubung melalui Connector 1.2.3 pada 14.28.45 WIB.
Pengguna kemudian meminta melewati post `7615256610599898389`; Python dihentikan
secara teratur pada 14.33 WIB. Bundle INTERRUPTED menyimpan 118 record
(1 post, 42 komentar, 75 balasan); semuanya sudah ada pada run awal, jadi tidak
menambah hitungan unik kampanye. Dua belas checksum cocok dan tidak ada ID ganda.

Metadata audit memiliki dua keterbatasan yang dipertahankan apa adanya: runner lama
menandai pekerja yang diinjeksi sebagai synthetic meskipun bridge Chrome nyata;
CLI kini menetapkan false untuk worker live. Operasi bridge yang diinterupsi juga
kehilangan source_version sehingga adapter memakai label beesense_native_browser.
Ini bukan data fixture: handshake dan log bridge live diverifikasi. Manifest lama
tidak ditulis ulang, dan label native-browser hanya diizinkan untuk run interupsi
tertentu pada pemeriksaan kelanjutan. Tes CLI dan lint/format Python lulus.

Upaya restart pertama berhenti pada pemeriksaan label tersebut sebelum server
siap. Setelah diperbaiki, pengguna menghubungkan kode baru tanpa Reload/install.
Run baru `be2ee5c5-9ddf-4d10-a1d0-cc82fad01452` mulai **14.38.45 WIB**,
Connector **1.2.3**, build `20261105-comment-viewport-v5`, source-pagination-v3.
Target segmen baru 1.000 post; deadline tetap **16.00 WIB**. Pencarian kembali
dari query awal konfigurasi; semua 25 query tetap masuk antrean. Post yang
diminta dilewati dan lima root lama dikecualikan, tanpa resume thread lama.
Hasil run lama dipakai untuk deduplikasi, bukan dihitung sebagai capaian baru.
Belum ada klaim bahwa 1.000 atau seluruh komentar berhasil diambil.


## Penutupan 16.00 WIB dan tahap NLP

Kelanjutan be2ee5c5 dihentikan atas permintaan pengguna sekitar 14.55 WIB setelah
menyimpan 2 post baru, 34 komentar dan 58 balasan. Dua belas checksum cocok,
seluruh native ID berupa string dan tidak ganda. Label source_version fallback
pada interupsi dipertahankan dalam audit, bukan ditulis ulang.

Restart berikutnya 978c061b-beeb-4d18-8ed4-ef57329fd957 terhubung melalui Connector
1.2.3, mulai 14.57.51 WIB, dan mengecualikan tujuh root yang sudah tersimpan.
Pencarian menghasilkan 167 kandidat. Pada `7642218587217775880`, checkpoint 15.10
39 komentar/142 balasan, 15.25 76/156, 15.40 76/190, 15.55 95/196; terakhir 115/196.
Angka ini hanya observasi thread. Saat finalisasi, tidak ada record lolos seleksi:
dua root di luar periode dan satu gagal include keyword. Karena itu 311 komentar/
balasan teramati tersebut tidak ditambahkan ke Excel hasil atau capaian model.

Guard mengirim SIGINT teratur tepat pada 16.00 WIB, status akhir INTERRUPTED.
Gabungan empat segmen hari ini: **7 post, 492 komentar, 537 balasan = 1.036 ID unik**,
0 duplikat. Seluruh 48 checksum berkas manifest cocok; native ID Excel disimpan
sebagai string. Arsip seluruh sosmed 36.233 ID unik / 11 partisi / 0 duplikat. `config/auth.json`
tidak berubah. Target 1.000 post dan seluruh komentar belum tercapai. Run kosong terakhir
melewati organisasi output sehingga tidak menghapus hasil sebelumnya.

Pengguna kemudian menginstruksikan penggabungan data seluruh sosmed, retraining
20 topik / coherence 0,4, rebuild dashboard dan commit/push main. Penggabungan serta
fitting lokal dimulai setelah pemeriksaan akhir. Lihat
[[Retraining Gabungan TikTok 20261105]] untuk tahap berikutnya.
