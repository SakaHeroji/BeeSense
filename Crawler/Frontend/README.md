# BeeSense Crawler Frontend

React, TypeScript dan Vite untuk tujuh menu: YouTube, Reddit, Instagram, TikTok, Threads, Facebook dan X/Twitter. Lingkup versi 1.2 adalah **frontend terlebih dahulu**. Tidak ada menu/perangkat Migrasi Excel terpisah atau Crawler Manual. Form URL/survei dan penulis migrasi PostgreSQL yang sempat dibuat telah dihapus sesuai koreksi lingkup.

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

## Konfigurasi per sosmed

`config/social_crawler.json` adalah sumber nilai awal. `scripts/sync-config.mjs` membuat proyeksi publik `src/shared/crawler-defaults.json` sebelum dev/test/build. Edit JSON root, bukan snapshot; regenerasikan sebelum membangun dari context Docker frontend terisolasi. Proyeksi tidak membaca auth.json atau menyertakan rahasia.

Form menyediakan tanggal publikasi WIB dari/sampai sebelum, include/exclude keywords, query atau hashtag Instagram/TikTok, subreddit Reddit, target post dan batas waktu jam opsional. Hanya sumber halaman yang aktif. Default 1.000 post, komentar/balasan tanpa cap, tanpa batas durasi. Excel lokal default; PostgreSQL/keduanya menyediakan host/IP, port dan URI sementara.

Akun & sesi opsional ditampilkan untuk Instagram, X/Twitter, Threads dan Facebook. Username/session ID disiapkan untuk `config/auth.json` melalui kontrak HTTP tersendiri; bukan bagian konfigurasi crawling. Session ID disembunyikan, bisa ditampilkan dengan tombol, tidak disimpan ke URL/localStorage dan dibersihkan setelah simulasi simpan. Isian kosong mempertahankan nilai yang ada. Simpan perubahan akun sebelum meninjau crawling. Demo hanya menyimpan metadata akun di memori, tanpa menyimpan session ID atau mengubah file nyata. TikTok memakai sesi pada tab Chrome melalui plugin.

## TikTok melalui plugin Chrome

Konfigurasi → tinjau → hubungkan Chrome → pantau hasil berada pada menu TikTok dan transaksi yang sama. Setelah review, monitor menampilkan alamat server dashboard, kode pairing sementara yang tersembunyi, versi minimum plugin, status koneksi dan petunjuk validasi manual. Versi minimum diproyeksikan dari manifest publik Connector, tanpa menyalin key atau permissions.

Waktu pengambilan baru dimulai setelah server memverifikasi plugin. Koneksi ulang mempertahankan deadline. CAPTCHA/login diselesaikan pengguna pada tab TikTok; tombol lanjut meminta server memeriksa ulang, bukan menandai validasi selesai dari browser. Jumlah komentar/balasan post aktif dipisahkan dari operasi selesai; kelengkapan memerlukan akhir pagination yang terverifikasi, bukan kesamaan dengan statistik sumber.

Chrome dan tab TikTok harus tetap terbuka. Untuk penelusuran UI yang paling andal, biarkan tab TikTok aktif dan jendela tidak diminimalkan; popup Connector boleh ditutup. Biarkan plugin menggulir, membuka balasan dan berpindah post; hindari navigasi/refresh manual kecuali menyelesaikan CAPTCHA atau login ketika diminta. Aktivitas halaman latar dapat diperlambat browser. Ini pertimbangan operasi, bukan bukti penyebab stagnasi run tertentu.

Adapter HTTP menggunakan API proyek yang sama. Respons pairing wajib terikat job dan origin dashboard; tidak ada port bridge tetap, server kedua atau menu plugin terpisah. Kode pairing hanya berada di memori halaman, tidak di URL/localStorage/snapshot publik job. Pengamat tidak meminta endpoint privat. Mode demo menyediakan tombol simulasi berlabel yang **tidak mengendalikan crawler nyata**.

Integrasi gateway HTTP/worker masih tahap berikutnya. Server nantinya harus melayani dashboard dan penghubung plugin pada origin yang sama, menyediakan endpoint dalam [kontrak API](docs/API_CONTRACT.md), dan mengiklankan `tiktokConnectorAvailable` hanya setelah siap. Bridge CLI desktop yang sedang berjalan tetap independen pada tahap frontend ini; preview tidak menghubungkannya diam-diam.

## Data, statistik dan migrasi transaksi

Tab Hasil per tanggal memakai tanggal eksekusi `startedAt` dalam WIB. Tanggal publikasi dan waktu pembuatan job tidak menjadi tanggal crawling. Filter/pagination/ID transaksi berada pada URL. Transaksi dideduplikasi menurut ID; preview maksimal 50 baris dengan pencarian dan ekspor Excel halaman aktif.

Setiap transaksi mempunyai aksi Statistik, Lihat data dan Migrasi ke PostgreSQL. Statistik lengkap berada di `/crawler/:platform/jobs/:id?panel=statistics`: post, qualified, komentar, balasan, total konten unik, kandidat, duplikat, penolakan, target/gap/persentase, waktu, penyimpanan dan versi dataset. Transaksi multi-sumber dibatasi ke sosmed pada route.

Migrasi terbuka di data transaksi yang sama: `/crawler/:platform?view=results&transaction=:id&action=migrate`. Tidak ada unggah file atau halaman migrasi umum. Sumber dikunci ke job, sosmed dan versi/checksum dataset. Review menampilkan tanggal crawling, jumlah seluruh jenis konten, target PostgreSQL dan kebijakan lewati ID yang ada. Progres berada inline pada data tersebut. Simulasi ulang dataset/target yang sama melewati seluruh ID; ini ilustrasi frontend, bukan bukti database nyata. Pada refresh penuh, progres simulasi dapat tidak tersedia karena state hanya berada di memori.

Mulai crawling membuka monitor job untuk progres, aktivitas, konfigurasi dan dataset. Tautan monitor lama otomatis tetap didukung. Menu/form manual sudah tidak tersedia.

## Batas backend dan database

[Kontrak API](docs/API_CONTRACT.md) adalah rancangan untuk tahap berikutnya. HTTP server/worker, penyimpanan auth.json dan migrasi transaksi PostgreSQL **belum diimplementasikan**. Tombol API hanya aktif bila capability tersedia. SocialCrawler Python tetap CLI/library; TikTok memiliki transport Chrome/plugin nyata yang belum terhubung ke gateway frontend. Penulisan langsung PostgreSQL belum tersedia dan runner menolak opsi tersebut sebelum crawling.

Utility `excel_postgresql.py`, SQL, tes database khusus, job CI dan image utility migrasi Excel telah dihapus. Database serta sumber Excel yang sudah ada tidak disentuh. **No migration required** untuk perubahan frontend ini.

## Docker

```sh
docker build -t beesense-crawler-frontend:api Crawler/Frontend
```

Jalankan dari root repository. Image frontend tetap Nginx non-root UID 101, port 8080, health `/healthz`, SPA fallback. Tidak ada perubahan Compose/env/infrastruktur produksi. Docker daemon lokal tidak aktif sehingga image revisi ini belum dibangun. [Delivery dan audit UI](docs/DELIVERY.md) memuat bukti verifikasi.
