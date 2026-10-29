# BeeSense Crawler Frontend

Frontend **ReactJS + TypeScript + Vite** berdasarkan [PRD Crawler](<../../PRD/PRD Frontend/PRD Frontend Crawler.md>). Dua menu utama: Crawler Otomatis dan Crawler Manual. Pilihan URL dan survei berada di dalam Crawler Manual.

## Jalankan lokal

Gunakan Node.js 22.12 atau lebih baru dan npm. Dari root repository:

```sh
cd Crawler/Frontend
npm ci
npm run dev
```

Buka **http://127.0.0.1:5173**. Mode development menggunakan adapter **simulasi**, dengan banner tetap. Tidak ada request ke platform sosial, crawling, training, atau perubahan dataset sebenarnya. Metadata pekerjaan demo disimpan di localStorage agar monitor dapat dibuka setelah refresh. Jawaban survei dan indeks respons demo hanya berada di memori; gunakan data sintetis dan impor ulang sesudah refresh.

Untuk meninjau build demo:

```sh
npm run build:demo
npm run preview
```

Preview tersedia pada http://127.0.0.1:4173. Pekerjaan simulasi baru dipercepat menjadi sekitar 45 detik, bukan tiga jam pengambilan sesungguhnya. Melalui monitor, uji skenario CAPTCHA, 429, dan kegagalan ekspor. Mengembalikan skenario ke Normal memungkinkan simulasi berlanjut; ini bukan tombol melewati rate limit pada mode API.

## Mode backend API

Salin `.env.example` menjadi `.env.local`, tentukan `VITE_DATA_MODE=api`, alamat API, dan proyek. `npm run build` memakai mode API secara default; tidak fallback diam-diam ke demo ketika backend gagal. Nilai `VITE_*` bersifat publik dan ditanam saat build: jangan masukkan token, cookie, atau rahasia.

Typed HTTP adapter ada di `src/shared/api.ts`; kontrak transport ada di [docs/API_CONTRACT.md](docs/API_CONTRACT.md). API/worker/autentikasi belum disediakan oleh folder frontend ini. Mode API baru dapat mengakuisisi data setelah layanan backend mengimplementasikan kontrak tersebut. `social_crawler.py` saat ini adalah CLI/library, bukan HTTP server yang dapat langsung dipanggil SPA.

Backend wajib menegakkan izin, deduplikasi, validasi, idempotensi, penyimpanan pekerjaan persisten, dan otorisasi ekspor/sesi CAPTCHA. Role selector hanya ada pada demo; bukan mekanisme autentikasi. Mode API memperoleh sesi dari server. Polling snapshot setiap lima detik dipakai untuk sinkronisasi dan pemulihan; SSE dapat ditambahkan tanpa mengubah kepemilikan state server.

## Fitur

- Wizard otomatis empat langkah, target per platform, batas waktu, tanggal WIB, filter, baseline wajib, dan review rencana sebelum mulai.
- Riwayat/filter pekerjaan; monitor per platform, grafik dan tabel progres, penghentian aman, serta pemisahan hasil parsial/finalisasi/gagal.
- Input URL dengan normalisasi native ID, seleksi hasil valid, deteksi duplikat, dan mode tanpa discovery tambahan.
- Form survei atau impor CSV/XLSX, pemilihan sheet, mapping, review, dan commit respons lengkap. Template awal `minat-studi` versi 1 memerlukan Q01 teks dan Q02 skala 1–5.
- Preview dataset, kualitas, konteks sumber, ekspor sesuai izin, serta pilihan input NLP dengan penerimaan eksplisit terhadap hasil parsial.
- Form tidak menyimpan jawaban survei di URL/localStorage. Konten ditampilkan sebagai teks; CSV melindungi sel yang bisa ditafsirkan sebagai formula.

Data demo selalu sintetis. Daftar baseline demo beserta native ID contoh bukan indeks dari dataset produksi. Unduhan demo hanya preview CSV halaman aktif dan manifest simulasi; bukan delapan-sheet workbook audit atau manifest terverifikasi. Adapter survei NLP belum tersedia, sehingga handoff survei diblokir secara eksplisit.

## Pemeriksaan

```sh
npm run format:check
npm run lint
npm run test
npm run build
```

Vitest mencakup batas konfigurasi, normalisasi URL, survei atomik/duplikat/konflik, izin, transport API, dan interaksi inti. Uji terhadap adapter simulasi tidak membuktikan backend atau browser worker nyata telah tersedia. Hasil audit UX dan cakupan rilis dicatat di [docs/DELIVERY.md](docs/DELIVERY.md).

## Docker

Dari folder ini:

```sh
# Build API by default. Route /api/v1 to a backend through your ingress.
docker build -t beesense-crawler-frontend:api .

# Review UI with synthetic data only.
docker build --build-arg VITE_DATA_MODE=demo -t beesense-crawler-frontend:demo .
docker run -d --name beesense-crawler-frontend -p 127.0.0.1:4174:8080 beesense-crawler-frontend:demo
```

Container berjalan sebagai UID 101 di port 8080 dengan health check `/healthz`. SPA deep links memakai fallback ke index; request API yang belum dirutekan memperoleh JSON 503. Ini container baru untuk Crawler, terpisah dari runtime Streamlit. Tidak ada perubahan skema database atau migrasi pada pekerjaan frontend ini.

## Struktur

```text
src/app/        shell, router, provider, error boundary
src/features/   otomatis, manual URL, survei, riwayat, monitor, dataset
src/shared/     typed contract, HTTP/demo adapter, validasi, UI bersama
src/test/       unit dan workflow integration tests
docs/          kontrak integrasi, audit UX, dan hasil verifikasi
```

Pilihan visual memakai Plus Jakarta Sans yang dibundel lokal, tema putih–oranye dengan teks hitam minimum 13 px, dan tata letak form dengan ringkasan konteks. Rujukan teknologi: [React SPA](https://react.dev/learn/build-a-react-app-from-scratch), [Vite](https://vite.dev/guide/), [TanStack Query](https://tanstack.com/query/latest/docs/framework/react/overview), [React Router](https://reactrouter.com/start/declarative/installation), serta [SheetJS](https://docs.sheetjs.com/docs/getting-started/installation/nodejs/). SheetJS menggunakan tarball resmi 0.20.3; integrity dan dependency lain dikunci pada `package-lock.json`.

## Tema dan sumber sosial

Semua teks berwarna `#000000`, termasuk hint, placeholder, badge, tombol, dan teks nonaktif. Ukuran body/input 15 px, label/tombol 14 px, teks pendukung minimal 13 px. Permukaan putih `#FFFFFF`, canvas `#FAFAFA`, aksen `#FF8A24`, hover `#FF7608`, latar lembut `#FFF3E8`, border `#E6DDD5`. Warna hijau tidak digunakan. Aturan desain tercatat di [PRD §14.1](<../../PRD/PRD Frontend/PRD Frontend Crawler.md#141-tema-putih-oranye-dan-tipografi-wajib>).

UI dan simulasi menyediakan **YouTube, Reddit, Instagram, TikTok, Threads, Facebook, dan X/Twitter** pada pemilihan sumber, query/target, validasi URL lengkap, monitor, grafik, dan filter. YouTube/Reddit dipilih sebagai default; lima sumber baru bersifat opt-in. Mode API hanya mengaktifkan sumber yang dinyatakan tersedia oleh backend melalui capabilities. Python SocialCrawler saat ini baru memiliki adapter YouTube/Reddit; lima adapter lain dan normalisasi skema NLP perlu diimplementasikan serta diuji. Handoff dataset demo yang memuat sumber baru diblokir sampai adapter skema NLP siap.
