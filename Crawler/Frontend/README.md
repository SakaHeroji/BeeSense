# BeeSense Crawler Frontend

React, TypeScript dan Vite untuk conversation riset, crawling parallel, serta tujuh sumber: YouTube, Reddit, Instagram, TikTok, Threads, Facebook dan X/Twitter. Lingkup versi 1.3 tetap **frontend terlebih dahulu**. Tidak ada menu/perangkat Migrasi Excel terpisah atau Crawler Manual. Form URL/survei dan penulis migrasi PostgreSQL yang sempat dibuat telah dihapus sesuai koreksi lingkup.

## Menjalankan

Node.js ≥22.12 dan npm:

```sh
cd Crawler/Frontend
npm ci
npm run dev
```

Buka http://127.0.0.1:5173. Development memakai simulasi berlabel. Tidak ada crawling, pembacaan arsip Excel, penulisan database atau perubahan auth.json. Hanya metadata crawling demo tersimpan di browser; simulasi migrasi/akun berada di memori dan hilang saat refresh. Gunakan input sintetis untuk demo.

```sh
npm run check
npm run format:check
npm run build:demo
npm run preview
```

Build produksi memakai mode API dan tidak fallback diam-diam ke simulasi. Konfigurasi publik berada di `.env.example`; VITE_* tidak boleh memuat token, cookie atau DSN.

## Alur conversation-first

Konteks riset sekarang disiapkan terpisah di `/crawler/conversations`. Tabel library dan form editor tidak ditampilkan bersamaan: operator membuka conversation baru atau versi yang dipilih pada form tersendiri. Satu conversation menyimpan judul, tujuan, include/exclude beserta mode pencocokan, query, hashtag, subreddit, ruang lingkup relevansi, contoh klasifikasi dan threshold.

Operator dapat mengisi semuanya manual, meminta draf Gemini hanya dari judul, atau mengunduh prompt Markdown berbasis judul untuk menghasilkan workbook `.xlsx` melalui AI eksternal. Workbook memakai tiga sheet tetap: `conversation`, `discovery`, dan `relevance_examples`. Upload lokal memeriksa ekstensi, ukuran, sheet, header, tipe baris, threshold, formula, dan validasi domain sebelum langsung menyimpan conversation berversi. Workbook hanya mengisi tujuan, discovery, keyword, dan relevansi; rentang publikasi bukan bagian dari Conversation. Workbook tidak dikirim ke endpoint upload frontend.

Menu `/crawler/parallel` dan setiap `/crawler/:platform` memilih conversation lalu mengatur transaksi: rentang publikasi, platform, target, durasi, penyimpanan, serta akun bila diperlukan. Saat dipilih, conversation dibekukan menjadi snapshot berisi ID, versi dan waktu pembekuan; rentang publikasi dibekukan pada `Config` transaksi. Perubahan conversation berikutnya tidak mengubah job yang sudah ditinjau. Mode parallel memakai satu snapshot dan satu rentang transaksi yang sama untuk seluruh platform terpilih, sementara kegagalan satu platform tidak dimodelkan sebagai pembatalan platform lain.

Demo menyimpan library conversation di localStorage tanpa rahasia. Generator demo deterministik dan berlabel; mode API memakai endpoint conversation pada kontrak HTTP. Gemini/API key tidak pernah berada di frontend. Origin conversation membedakan `manual`, `gemini`, dan `excel`.

## Konfigurasi per sosmed

`config/social_crawler.json` adalah sumber nilai awal. `scripts/sync-config.mjs` membuat proyeksi publik `src/shared/crawler-defaults.json` sebelum dev/test/build. Edit JSON root, bukan snapshot; regenerasikan sebelum membangun dari context Docker frontend terisolasi. Proyeksi tidak membaca auth.json atau menyertakan rahasia.

Form platform tidak lagi mengulang judul, keyword, query, hashtag, subreddit, atau relevansi. Seluruh konteks tersebut berasal dari snapshot conversation yang terlihat sebelum review. Form transaksi mengatur rentang publikasi, target post dan batas waktu jam opsional untuk sumber aktif. Default 1.000 post, komentar/balasan tanpa cap, tanpa batas durasi. Excel lokal default; PostgreSQL/keduanya menyediakan host/IP, port dan URI sementara.

Akun & sesi opsional ditampilkan untuk Instagram, X/Twitter, Threads dan Facebook. Username/session ID disiapkan untuk `config/auth.json` melalui kontrak HTTP tersendiri; bukan bagian konfigurasi crawling. Session ID disembunyikan, bisa ditampilkan dengan tombol, tidak disimpan ke URL/localStorage dan dibersihkan setelah simulasi simpan. Isian kosong mempertahankan nilai yang ada. Simpan perubahan akun sebelum meninjau crawling. Demo hanya menyimpan metadata akun di memori, tanpa menyimpan session ID atau mengubah file nyata. TikTok memakai sesi pada tab Chrome melalui plugin.

Panduan lipat pada bagian akun menjelaskan cookie `sessionid` Instagram dan
`auth_token` X melalui Chrome DevTools. TikTok menggunakan sesi tab Chrome dan
pairing; Threads/Facebook menjelaskan backend yang belum tersedia. Lihat
[panduan sesi per sosmed dan verifikasi](docs/SESSION_GUIDE.md).

## TikTok melalui plugin Chrome

Konfigurasi → tinjau → hubungkan Chrome → pantau hasil berada pada menu TikTok dan transaksi yang sama. Setelah review, monitor menampilkan alamat server dashboard, kode pairing sementara yang tersembunyi, versi minimum plugin, status koneksi dan petunjuk validasi manual. Versi minimum diproyeksikan dari manifest publik Connector, tanpa menyalin key atau permissions.

Waktu pengambilan baru dimulai setelah server memverifikasi plugin. Koneksi ulang mempertahankan deadline. CAPTCHA/login diselesaikan pengguna pada tab TikTok; tombol lanjut meminta server memeriksa ulang, bukan menandai validasi selesai dari browser. Jumlah komentar/balasan post aktif dipisahkan dari operasi selesai; kelengkapan memerlukan akhir pagination yang terverifikasi, bukan kesamaan dengan statistik sumber.

Chrome dan tab TikTok harus tetap terbuka. Untuk penelusuran UI yang paling andal, biarkan tab TikTok aktif dan jendela tidak diminimalkan; sidebar Connector boleh ditutup. Biarkan plugin menggulir, membuka balasan dan berpindah post; hindari navigasi/refresh manual kecuali menyelesaikan CAPTCHA atau login ketika diminta. Aktivitas halaman latar dapat diperlambat browser. Ini pertimbangan operasi, bukan bukti penyebab stagnasi run tertentu.

Adapter HTTP menggunakan API proyek yang sama. Respons pairing wajib terikat job dan origin dashboard; tidak ada port bridge tetap, server kedua atau menu plugin terpisah. Kode pairing hanya berada di memori halaman, tidak di URL/localStorage/snapshot publik job. Pengamat tidak meminta endpoint privat. Mode demo menyediakan tombol simulasi berlabel yang **tidak mengendalikan crawler nyata**.

Integrasi gateway HTTP/worker masih tahap berikutnya. Server nantinya harus melayani dashboard dan penghubung plugin pada origin yang sama, menyediakan endpoint dalam [kontrak API](docs/API_CONTRACT.md), dan mengiklankan `tiktokConnectorAvailable` hanya setelah siap. Bridge CLI desktop yang sedang berjalan tetap independen pada tahap frontend ini; preview tidak menghubungkannya diam-diam.

## Data, statistik dan migrasi transaksi

Tab Hasil per tanggal memakai tanggal eksekusi `startedAt` dalam WIB. Tanggal publikasi dan waktu pembuatan job tidak menjadi tanggal crawling. Filter/pagination/ID transaksi berada pada URL. Transaksi dideduplikasi menurut ID; preview maksimal 50 baris dengan pencarian dan ekspor Excel halaman aktif.

Setiap transaksi mempunyai aksi Statistik, Lihat data dan Migrasi ke PostgreSQL. Statistik lengkap berada di `/crawler/:platform/jobs/:id?panel=statistics`: post, qualified, komentar, balasan, total konten unik, kandidat, duplikat, penolakan, target/gap/persentase, waktu, penyimpanan dan versi dataset. Transaksi multi-sumber dibatasi ke sosmed pada route.

Migrasi terbuka di data transaksi yang sama: `/crawler/:platform?view=results&transaction=:id&action=migrate`. Tidak ada unggah file atau halaman migrasi umum. Sumber dikunci ke job, sosmed dan versi/checksum dataset. Review menampilkan tanggal crawling, jumlah seluruh jenis konten, target PostgreSQL dan kebijakan lewati ID yang ada. Progres berada inline pada data tersebut. Simulasi ulang dataset/target yang sama melewati seluruh ID; ini ilustrasi frontend, bukan bukti database nyata. Pada refresh penuh, progres simulasi dapat tidak tersedia karena state hanya berada di memori.

Mulai crawling membuka monitor job untuk progres, aktivitas, konfigurasi dan dataset. Tautan monitor lama otomatis tetap didukung. Menu/form manual sudah tidak tersedia.

## Batas backend dan database

[Kontrak API](docs/API_CONTRACT.md) adalah rancangan untuk tahap berikutnya. HTTP server/worker, penyimpanan conversation persisten, pemanggilan Gemini server-side, penyimpanan auth.json dan migrasi transaksi PostgreSQL **belum diimplementasikan**. Tombol API hanya aktif bila capability tersedia. SocialCrawler Python tetap CLI/library; TikTok memiliki transport Chrome/plugin nyata yang belum terhubung ke gateway frontend. Penulisan langsung PostgreSQL belum tersedia dan runner menolak opsi tersebut sebelum crawling.

Utility `excel_postgresql.py`, SQL, tes database khusus, job CI dan image utility migrasi Excel telah dihapus. Database serta sumber Excel yang sudah ada tidak disentuh. **No migration required** untuk perubahan frontend ini.

## Docker

```sh
docker build -t beesense-crawler-frontend:api Crawler/Frontend
```

Jalankan dari root repository. Image frontend tetap Nginx non-root UID 101, port 8080, health `/healthz`, SPA fallback. Tidak ada perubahan Compose/env/infrastruktur produksi. Docker daemon lokal tidak aktif sehingga image revisi ini belum dibangun. [Delivery dan audit UI](docs/DELIVERY.md) memuat bukti verifikasi.
