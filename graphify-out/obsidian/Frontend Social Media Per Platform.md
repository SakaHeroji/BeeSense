---
type: implementation
status: frontend-first
tags: [beesense, frontend, crawler, konfigurasi, storage]
---

# Frontend Social Media Per Platform

Tujuh menu: YouTube, Reddit, Instagram, TikTok, Threads, Facebook, X/Twitter. Dropdown modul, Crawler Manual dan Migrasi Excel umum dihapus. `/crawler/:platform` menyediakan konfigurasi dan hasil per tanggal. [Preview lokal](http://127.0.0.1:5173/crawler/youtube) adalah simulasi berlabel.

## Sumber konfigurasi

[[Konfigurasi Universal Social Crawler]] tetap memakai config/social_crawler.json. Script sync-config.mjs membuat proyeksi publik sebelum dev/test/build; snapshot tidak memuat auth/DSN. Tanggal publikasi WIB, include/exclude, query/hashtag, subreddit, target dan jam opsional ditampilkan per sumber. Default 1.000 post, durasi dan cap komentar/reply null.

Storage default Excel lokal; PostgreSQL/keduanya memiliki IP/host, port dan URI sementara. JSON menyimpan nama env BEESENSE_POSTGRESQL_DSN, bukan DSN. CLI masih menolak tujuan database sebelum crawling karena penulisan langsung belum terintegrasi.

Akun & sesi opsional menyiapkan username/session ID di config/auth.json. Berlaku pada Instagram, X, Threads dan Facebook. TikTok memakai sesi Chrome melalui [[Frontend TikTok Plugin Chrome]]. Nilai kosong mempertahankan pengaturan yang ada; session ID baru tidak masuk plan crawling dan tidak dikembalikan sebagai metadata. Form simulasi tidak mengubah file asli.

## Transaksi sebagai pusat hasil

PlatformResults memakai startedAt dalam Asia/Jakarta, bukan tanggal publikasi/createdAt. Job antre belum mempunyai tanggal crawling. Filter tanggal, transaksi, aksi dan pagination dapat ditautkan; perubahan tanggal membersihkan pilihan lama. Preview dibatasi 50 baris per halaman dan ekspor berlabel halaman aktif.

Setiap baris mempunyai Statistik, Lihat data dan Migrasi ke PostgreSQL. JobStatistics memuat post, qualified, komentar, balasan, total konten unik, kandidat, duplikat, penolakan, target/persentase/gap, waktu/durasi dan versi dataset. Route `/crawler/:platform/jobs/:id?panel=statistics` membatasi angka ke sumber yang dipilih, termasuk job lama multi-sumber.

[[Migrasi Transaksi per Sosmed]] mengikat sumber ke dataset versi/checksum transaksi tersebut; tanpa unggah file atau halaman terpisah. Review dan progres berada pada data crawling sosmed itu. [[Output Social Media Per Tanggal]] tetap menjadi arsip nyata; SPA belum membaca arsip filesystem.

## Batas implementasi

Frontend terlebih dahulu. Tidak ada HTTP/worker baru, penulis PostgreSQL atau penyimpanan auth.json nyata. Utility migrasi Excel/SQL/CI/image yang sempat dibuat telah dihapus. Data sumber dan database yang ada dipertahankan. Simulasi migrasi/akun berada di memori dan dapat hilang saat refresh; metadata job crawling saja dapat bertahan di browser.

38 tes Vitest + satu tes Node proyeksi lulus. Build/lint/typecheck/format dan browser diperiksa; Docker daemon tidak aktif. Teks minimum 12 px. [Kontrak API](../../Crawler/Frontend/docs/API_CONTRACT.md) · [Audit delivery](../../Crawler/Frontend/docs/DELIVERY.md) · [[Frontend React Crawler]] · [[HOME]]

## Kerapian tabel dan tombol hasil

Tabel hasil memakai tujuh kolom dengan proporsi tetap: transaksi/waktu, status, post, komentar, balasan, penyimpanan dan tindakan. Nama transaksi dan waktu WIB berada pada dua baris, tanpa pengulangan tanggal tambahan. Angka rata kanan dan tabular; komentar/balasan dipisahkan. Label penyimpanan memiliki ikon dan tetap utuh. Tombol Statistik berbingkai jelas, sedangkan Migrasi PostgreSQL memakai oranye BeeSense. Kelompok tindakan memakai kisi dua kolom; migrasi menempati satu baris penuh, konsisten pada setiap transaksi. Teks tombol 14 px dan tinggi nominal minimal 44 px. Tabel mobile bergeser dalam scroller sendiri dengan petunjuk dan fokus keyboard.
