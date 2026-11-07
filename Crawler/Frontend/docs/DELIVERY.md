# Delivery frontend 1.3

## Conversation-first crawling — 7 November 2026

Seluruh frontend yang terdampak kini memisahkan konteks riset dari operasi
crawling. Menu **Persiapan → Conversation** menjadi library dan editor berversi untuk
judul, tujuan, tanggal konten, keyword include/exclude, mode pencocokan, query,
hashtag, subreddit, scope, contoh relevansi dan threshold. Conversation dapat ditulis
manual atau dibuat sebagai draf Gemini; request generator hanya mengirim `title`,
dan draf harus ditinjau serta disimpan sebelum dapat dipakai. Tabel library kini
terpisah dari form editor. Form dapat mengunduh prompt Markdown berbasis judul dan
membaca workbook `.xlsx` tiga sheet untuk mengisi discovery/relevansi lalu menyimpan
conversation ber-origin Excel. Parser menolak struktur asing dan formula.

Menu **Crawling → Parallel** dan tujuh halaman platform tidak lagi meminta ulang
field riset. Operator memilih conversation tersimpan, melihat ringkasannya, lalu hanya
mengatur platform, target, durasi, storage dan koneksi sumber. Review membekukan
seluruh conversation sebagai snapshot ID/versi/waktu. Mode parallel menggunakan satu
snapshot yang sama untuk minimal dua platform; mode platform tunggal memakai
alur review yang sama. Perubahan conversation berikutnya tidak mengubah job lama.

Kontrak HTTP menambahkan list/detail/create/update conversation dan generator
server-side. Demo menyediakan library localStorage serta generator deterministik
berlabel, tanpa API key atau rahasia. Endpoint, pemanggilan Gemini nyata,
persistensi backend dan runner paralel tetap pekerjaan backend berikutnya.
Frontend tidak menulis database, `auth.json`, Compose, env produksi atau layanan
aktif. **No migration required.**

Verifikasi revisi ini lulus:

- `npm run test`: 59 tes Vitest dan 2 tes Node.
- `npm run lint`, `npm run typecheck`, `npm run format:check`.
- `npm run build` untuk mode API dan `npm run build:demo`.
- Browser nyata pada 1440 px, mobile 375 px dan landscape 812×375; tidak ada
  horizontal overflow, error console atau warning console.
- Audit pedoman web terbaru: struktur landmark, label/error inline, fokus,
  keyboard, hit area, responsif dan reduced motion lulus untuk perubahan ini.

Screenshot berada di `output/playwright/conversation-*.png`,
`output/playwright/parallel-*.png`, dan
`output/playwright/youtube-conversation-desktop.png`.

Dockerfile tetap memakai build Node dan Nginx non-root UID 101 dengan health
`/healthz`. Build/start image belum dapat diverifikasi karena Docker Desktop lokal
tidak aktif; runtime container alternatif tidak dinyalakan atau dipasang. Status deployment tetap
**Not fully verified**; jalankan
`docker build -t beesense-crawler-frontend:conversation-v1.3 Crawler/Frontend` saat
daemon tersedia. Keterbatasan ini tidak memengaruhi build Vite API/demo yang lulus.

## TikTok plugin Chrome — 5 November 2026

Frontend TikTok kini mengikuti urutan konfigurasi → review → pairing Chrome →
progres pada transaksi yang sama. Panel koneksi menampilkan alamat server dashboard,
kode sementara tersembunyi dengan tombol salin, versi minimum plugin dari manifest,
status menunggu/terhubung/putus/kedaluwarsa, serta arahan CAPTCHA manual. Form sesi
TikTok diganti petunjuk penggunaan tab Chrome yang sudah login. Query dan hashtag
dapat dipakai bergantian; tanggal, include/exclude, target, jam opsional dan storage
tetap berasal dari konfigurasi universal. Statistik serta migrasi tetap pada hasil
transaksi per sosmed.

Keputusan desain: palet BeeSense dipertahankan, Plus Jakarta Sans, body/input
baru 16 px dan label/petunjuk 14 px. Tiga langkah menjelaskan urutan nyata;
panel koneksi menjadi fokus monitor, bukan menu baru. Angka post aktif dipisahkan
dari operasi selesai, dengan aktivitas dan peringatan bila tidak ada ID baru.
Review visual memperbaiki padding petunjuk Chrome dan menggelapkan indikator
langkah #B84D00 agar angka putih kecil tetap terbaca.

Kontrak API privat terikat job/proyek pada origin dashboard yang sama. Tidak ada
hardcoded port bridge atau permintaan ke server kedua. Kode pairing hanya di
memori halaman; Job publik hanya memuat ringkasan state/versi/lastSeenAt.
Pengamat tidak meminta endpoint privat. Timer menunggu verifikasi koneksi;
reconnect mempertahankan deadline. Tombol lanjut setelah CAPTCHA mempertahankan
state yang dikembalikan server sampai worker memverifikasi pemulihan.

**Batas implementasi:** tahap ini tetap frontend terlebih dahulu. Gateway HTTP
dan worker terintegrasi belum dibuat; build API memerlukan capability
`tiktokConnectorAvailable` dan endpoint pada API_CONTRACT.md. Preview demo berlabel
tidak mengendalikan Chrome atau run CLI nyata. Tidak ada restart crawler aktif,
perubahan auth.json, PostgreSQL, konfigurasi produksi atau redeploy Streamlit.
No migration required.

Verifikasi revisi ini: `npm run check` lulus lint, 45 Vitest, 2 tes Node proyeksi,
TypeScript dan build API. Cakupan baru memeriksa alur konfigurasi/pairing/monitor,
hashtag/validasi/fokus, role pengamat, expiry/rotasi, clock/reconnect, rahasia di
memori, keterikatan origin/job dan CAPTCHA yang belum diverifikasi server.
`npm run format:check` dan `npm run build:demo` menjadi bagian pemeriksaan akhir.

Browser uji terisolasi memeriksa konfigurasi/review/pairing, status terhubung,
CAPTCHA serta koneksi terputus pada runtime Vite proyek yang sama:
http://127.0.0.1:5173. Desktop 1440×1080 dan mobile 390×844; mobile scrollWidth
390 dan teks main terkecil 13 px, memenuhi minimum 12 px. Screenshot lokal
`output/playwright/tiktok-plugin-*.png`. Console tanpa error aplikasi; Chrome
memberi informasi nonfatal untuk input password readonly di luar form.

Audit [pedoman web terbaru](https://raw.githubusercontent.com/vercel-labs/web-interface-guidelines/main/command.md)
diambil 5 November 2026:

- `src/features/TikTokConnector.tsx` — pass: label, aksi button, status live,
  kode tersembunyi, expiry, feedback clipboard, format Intl dan heading semantik.
- `src/features/PlatformWorkspace.tsx` — pass: validasi inline/fokus pertama,
  dirty guard, input bernama, review modal serta CTA sesuai langkah.
- `src/features/JobDetail.tsx` — pass untuk perubahan TikTok: status menunggu
  koneksi, waktu belum dimulai, route sumber dan pemisahan angka operasi/thread.
- `src/styles.css` — pass untuk perubahan TikTok: fokus, hit area, type scale,
  overflow lokal dan kolom bertumpuk pada mobile; tidak menambah animasi.

Release guard lulus tanpa finding terhadap origin/main termasuk working tree.
Docker daemon lokal tidak berjalan, sehingga build/start image belum diverifikasi;
Dockerfile/Nginx/dependensi tidak berubah. Status deployment: **Not fully verified**.
Perintah tersisa saat daemon tersedia:
`docker build -t beesense-crawler-frontend:api Crawler/Frontend` dari root repo.
Graphify/Obsidian mencatat kontrak gateway satu origin dan pemisahan simulasi/live.

## Riwayat frontend per sosmed

3 November 2026. Lingkup yang disetujui adalah frontend terlebih dahulu. **Migrasi dan penyimpanan akun hanya simulasi antarmuka; tidak ada penulisan PostgreSQL atau auth.json.** Runtime lokal tetap Vite pada 127.0.0.1:5173. Tidak ada perubahan runtime/database produksi.

## Rancangan dan koreksi

Operator meninjau data satu sosmed menurut transaksi crawling. Tujuh sosmed menjadi satu-satunya navigasi utama. Rancangan warna tetap BeeSense: putih #FFFFFF, canvas #FAFAFA, teks #000000, aksi #FF8A24, pilihan #FFF3E8, garis #E6DDD5. Plus Jakarta Sans: heading 28–36 px, angka statistik 27–30 px, body/input 15 px, label 14 px, pendukung 13 px, badge minimal 12 px. Input mobile 16 px.

Tata letak rata kiri, mengikuti kepemilikan data:

```text
Menu sosmed | Konfigurasi / Hasil per tanggal
            | Transaksi: Statistik | Lihat data | Migrasi ke PostgreSQL
            | Data transaksi terpilih
            |   Review target PostgreSQL / Progres migrasi
            |   Preview post, komentar dan balasan
```

Review rancangan menghapus halaman migrasi umum dan unggah file: operator sudah memilih sumber pada transaksi sehingga tidak perlu memilih file/sosmed lagi. Statistik berupa satu kisi angka dengan garis pemisah, bukan kartu identik berulang. Setelah render, ringkasan progres yang berulang disembunyikan pada tab statistik agar angka lengkap langsung terlihat. Form migrasi dipindahkan ke atas preview dan diberi fokus/scroll saat aksi migrasi dipilih.

## Perubahan

- Hapus menu, route, frontend Migrasi Excel dan Crawler Manual termasuk URL/survei serta wizard/riwayat lama yang sudah tidak digunakan. Dependensi papaparse dihapus.
- Hapus utility Python/SQL/tes database/CI/image migrasi Excel yang sempat dibuat. Tidak menghapus database atau data Excel yang ada. **No migration required**.
- Tombol migrasi berada pada baris/data transaksi per sosmed, dengan review job/platform/dataset-version-checksum, PostgreSQL, kebijakan lewati ID, progres dan hitungan hasil. Tidak ada file upload. Pengulangan simulasi dataset/target yang sama menambahkan nol ID.
- Statistik lengkap per transaksi memisahkan post, qualified, komentar, balasan, total konten unik, kandidat, duplikat, penolakan, target/persentase/gap, durasi, waktu WIB dan versi dataset. Route salah sosmed tidak menampilkan job.
- Akun & sesi opsional untuk Instagram, X, TikTok, Threads dan Facebook. Input terpisah dari plan crawling. Form menyiapkan penyimpanan config/auth.json, menyembunyikan session ID dan membersihkannya setelah simulasi simpan. File asli tidak dibaca/diubah oleh frontend. Metadata saja disimpan di memori demo; token tidak masuk URL/localStorage atau snapshot job.

## Audit pedoman web

Diperiksa dengan [Web Interface Guidelines](https://raw.githubusercontent.com/vercel-labs/web-interface-guidelines/main/command.md) yang diambil ulang pada 3 November 2026.

- `src/features/PlatformResults.tsx` — pass: aksi terkait transaksi, tautan statistik semantik, filter URL atomik, preview maksimal 50 baris, paging serta ID unik.
- `src/features/TransactionMigration.tsx` — pass: fokus menuju aksi yang dipilih, label/error, review modal, snapshot expiry, respons lama ditolak, polling dan pemisahan processed/inserted, tanpa kredensial pada URL/review.
- `src/shared/AuthSettings.tsx` — pass: username tanpa spellcheck, session password/show, label, feedback penyimpanan, izin/capability, input kosong mempertahankan nilai tersimpan.
- `src/features/JobStatistics.tsx` — pass: dl semantik, Intl angka/waktu WIB, progress berlabel, statistik penuh dari snapshot per sumber.
- `src/app/Shell.tsx` — pass: tujuh tautan sosmed, mobile drawer/fokus/Escape/inert, skip link, banner simulasi tetap.
- `src/styles.css` — pass: font minimum 12 px, fokus terlihat, tabel horizontal mandiri, kisi statistik dua kolom mobile, reduced motion.

## Verifikasi

`npm run check`: lint, 38 Vitest + 1 tes Node proyeksi, typecheck dan build API lulus. Tes pembuatan manual/unggah Excel dihapus bersama fitur yang secara eksplisit dibatalkan; diganti cakupan navigasi tujuh sumber, statistik lengkap per sosmed, migrasi terikat transaksi/ID/role, auth opsional/rahasia serta kontrak HTTP yang direncanakan. Pemeriksaan format dan build demo juga dijalankan.

Browser pada runtime lokal yang sama memeriksa statistik, tombol migrasi transaksi, review/progres dan form akun. Screenshot lokal berada pada output/playwright. Tidak ada crawling atau sambungan PostgreSQL nyata. Hash auth.json tetap sama. Docker daemon tidak aktif; build image frontend belum diverifikasi. Perintah tersisa saat daemon tersedia: `docker build -t beesense-crawler-frontend:api Crawler/Frontend`.

Status: **Not fully verified untuk deployment**. Frontend dapat ditinjau; layanan HTTP/worker, penyimpanan auth.json dan migrasi PostgreSQL adalah tahap berikutnya. Compose/env/infrastruktur produksi dipertahankan. Graphify dan Obsidian mencatat lingkup frontend serta penghapusan utility migrasi lama.

## Koreksi tombol dan tabel hasil

Statistik sebelumnya berupa inline-link dan Migrasi memakai ghost button. Kini `PlatformResults.tsx` memakai tautan navigasi berbentuk tombol berbingkai dengan ikon grafik; migrasi menjadi tombol oranye dengan ikon database. `JobStatistics.tsx` memakai gaya migrasi yang sama. Latar putih #FFFFFF, teks #000000, border Statistik #737373, migrasi #FF8A24 dengan border #A44800; Plus Jakarta Sans 14 px dan tinggi nominal minimal 44 px. Hover/fokus memberi batas yang lebih tegas.

Tabel kini mempunyai tujuh kolom berproporsi tetap. Angka rata kanan/tabular, komentar dan balasan terpisah, nama/waktu pada dua baris, label penyimpanan tidak membungkus, header Tindakan terlihat. Grid aksi menyusun Statistik/Lihat data pada baris pertama dan Migrasi pada baris penuh berikutnya. Border baris dan padding konsisten; scroller mobile berfokus dan mempunyai petunjuk geser.

Audit terbaru terhadap pedoman web: `src/features/PlatformResults.tsx` pass (scope header, tabel semantik, link navigasi tetap link, aksi tetap button, ikon dekoratif tersembunyi); `src/features/JobStatistics.tsx` pass; `src/styles.css` pass (fokus, hit area, teks, hover dan overflow lokal). Pemeriksaan memakai npm run check, build:demo, format:check serta visual browser pada runtime Vite yang sama. Tidak ada perubahan perilaku backend atau database; No migration required.
