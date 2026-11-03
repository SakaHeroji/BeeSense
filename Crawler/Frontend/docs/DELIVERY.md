# Delivery frontend 1.2

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
