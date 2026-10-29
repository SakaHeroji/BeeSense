# Delivery dan Audit UI UX

Tanggal 29 Oktober 2026. Implementasi berada di `Crawler/Frontend`, berdasarkan PRD frontend Crawler. **Frontend dan simulasi telah diverifikasi; integrasi akuisisi produksi belum tersedia karena API/worker web belum dibangun.**

## Hasil implementasi

ReactJS/TypeScript memisahkan shell, fitur otomatis/manual, domain validation, HTTP adapter, dan adapter simulasi. Dua menu utama tetap dipertahankan. Otomatis menggunakan wizard sumber, filter/target, baseline, dan review. Manual menyediakan URL serta respons survei melalui form atau CSV/XLSX dengan pilihan sheet dan mapping.

Monitor memisahkan roots, qualified, komentar/reply, duplikasi, waktu, dan kendala akses. Hasil hanya dapat dibuka sesudah dataset terbit. Pemilihan input NLP menerima hasil parsial secara eksplisit, tanpa otomatis menjalankan training. Metadata survei tetap memiliki pertanyaan dan peran sumbernya; skema survei NLP yang belum didukung ditolak secara jelas.

Tujuh sumber UI/simulasi meliputi YouTube, Reddit, Instagram, TikTok, Threads, Facebook, dan X/Twitter. Query, target, kartu, grafik, riwayat, dan filter preview menggunakan daftar sumber yang sama. Lima sumber baru default nonaktif. Backend hanya mengaktifkan adapter melalui capabilities; UI dan simulasi tidak menambahkan lima adapter pada Python.

Semua contoh, angka, native ID baseline, dan unduhan dalam mode demo merupakan data sintetis. Browser tidak melakukan crawling tiga jam, dan refresh tidak memulai job baru. Survei demo disimpan dalam memori, bukan browser storage. Mode API gagal dengan pesan integrasi ketika backend belum tersedia, tanpa beralih ke data demo secara tersembunyi.

## Arah desain dan audit

Skill frontend-design digunakan untuk memilih tampilan workspace riset: form utama dengan ringkasan konteks, tipe Plus Jakarta Sans yang dibundel lokal, dan tema putih–oranye sesuai PRD 1.1: `#FFFFFF`, `#FAFAFA`, `#FF8A24`, `#FF7608`, `#FFF3E8`, dan border `#E6DDD5`. Semua teks `#000000`, body/input 15 px, label/tombol 14 px, teks pendukung minimum 13 px. Tidak ada hijau pada logo, status, atau grafik. Status memiliki ikon dan keterangan tertulis. Label grafik memakai HTML agar tidak menyusut bersama viewBox SVG.

Perbaikan hasil audit [Web Interface Guidelines](https://raw.githubusercontent.com/vercel-labs/web-interface-guidelines/main/command.md) berikut sudah diterapkan. Lokasi memakai file:line agar dapat ditinjau langsung.

| Lokasi                            | Temuan dan perbaikan                                                                  |
| --------------------------------- | ------------------------------------------------------------------------------------- |
| `src/shared/ui.tsx:86`            | Field kini mempunyai name/autocomplete, hint/error terhubung, dan aria-invalid.       |
| `src/shared/ui.tsx:157`           | Error memfokuskan field pertama; ringkasan dapat membuka field terkait.               |
| `src/features/Automatic.tsx:424`  | Masukan diperiksa per langkah, sebelum review terakhir.                               |
| `src/features/Automatic.tsx:472`  | Navigasi tab memakai tautan yang dapat dibuka langsung.                               |
| `src/app/Shell.tsx:47`            | Drawer mobile mempunyai Escape, siklus fokus, dan pengembalian fokus.                 |
| `src/app/Shell.tsx:92`            | Navigasi tersembunyi inert; isi utama inert saat drawer terbuka.                      |
| `src/features/DatasetView.tsx:38` | Pencarian memakai debounce dan mempertahankan tabel saat memuat.                      |
| `src/features/JobDetail.tsx:383`  | Sesi verifikasi dibuka lewat tautan pengguna, menghindari popup async yang terblokir. |
| `src/styles.css:53`               | Fokus terlihat; warna teks ditingkatkan, reduced motion dan area aman tersedia.       |

Submit untuk memulai akuisisi tetap memerlukan validasi rencana sesuai PRD. Isi jawaban/pencarian konten dataset tidak disimpan pada query URL; tab dan filter riwayat dapat ditautkan. Mode demo mempertahankan banner agar hasil simulasi tidak dianggap sebagai akuisisi sebenarnya.

Tambahan pemeriksaan state: respons validasi lama diabaikan ketika masukan telah berubah. Ini berlaku pada rencana, daftar URL, dan survei; regression test menahan respons URL lalu mengubah masukan sebelum respons diterima.

## Bukti verifikasi

| Pemeriksaan            | Hasil                                                                                                                                                                                                                |
| ---------------------- | -------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `npm run format:check` | Lulus.                                                                                                                                                                                                               |
| `npm run lint`         | Lulus, tanpa menonaktifkan aturan purity/effect React.                                                                                                                                                               |
| `npm run test`         | **50 tes lulus**, tiga file: domain, transport, dan workflow.                                                                                                                                                        |
| `npm run build`        | Lulus TypeScript dan build produksi API.                                                                                                                                                                             |
| Build demo Docker      | Berhasil pada Linux dengan lockfile yang sama; base image dikunci digest.                                                                                                                                            |
| Runtime container      | UID 101, port host localhost 4174; health check sehat.                                                                                                                                                               |
| HTTP lokal             | `/healthz` 200; `/crawler/manual` 200 dengan SPA root; API yang belum dirutekan mengembalikan JSON 503.                                                                                                              |
| Browser                | Desktop dan layout sempit aktual 400 px diperiksa. Drawer/Escape/fokus field invalid diverifikasi melalui UI. Override yang diminta 360 px dibatasi browser menjadi 400 px; tampilan aktual 360 px belum dibuktikan. |
| Tipografi browser      | Computed style pada konfigurasi: minimum 13 px, seluruh 96 elemen teks/input yang tampil hitam, tanpa pelanggaran.                                                                                                   |
| Screenshot             | `output/crawler_frontend_final.png` pada root repository, artefak lokal yang diabaikan Git.                                                                                                                          |
| Runtime lama           | Container Streamlit tetap sehat dan terpisah pada port 8501.                                                                                                                                                         |

Pengujian mencakup target/baseline invalid, normalisasi dan host URL tujuh platform, alias Threads/Instagram/Facebook/X, capability gating, query/target/kartu monitor tujuh sumber, duplikasi, respons survei atomik, izin/konflik, CSV serta XLSX multi-sheet, idempotency header, penolakan akses, navigasi mobile, hasil parsial, dan respons validasi yang terlambat. Tes simulasi tidak membuktikan integrasi browser worker atau keberhasilan target 1.000 post.

Tidak ada tabel/database, skema persisten server, atau model yang diubah. **No migration required.** File CI frontend ditambahkan, namun hasil GitHub Actions baru dapat diketahui setelah perubahan dipublikasikan.

## Batas integrasi dan pekerjaan berikutnya

Backend harus mengimplementasikan [kontrak API](API_CONTRACT.md), autentikasi/izin proyek, persistensi pekerjaan dan idempotensi, worker yang tetap berjalan sesudah tab ditutup, deduplikasi baseline nyata, browser CAPTCHA terotorisasi, serta ekspor final/checksum. Paginasi riwayat di server dan template survei dinamis perlu dirinci pada PRD Backend. Frontend awal membatasi tampilan riwayat menjadi 20 item per halaman dari koleksi yang dikirim server.

Berkas sosial delapan sheet dan verifikasi manifest sebenarnya berasal dari backend/exporter, bukan unduhan sintetis frontend. Handoff survei dan lima sumber sosial baru membutuhkan validasi adapter skema NLP; simulasi memblokirnya. Rilis akuisisi produksi belum dapat diterima sampai integrasi tersebut diuji dengan worker nyata; ini tidak menghalangi peninjauan UI melalui mode demo.

Pemetaan arsitektur dan dependensi diperbarui melalui Graphify; catatan [Obsidian Frontend React Crawler](<../../../graphify-out/obsidian/Frontend React Crawler.md>) membedakan implementasi UI dari layanan yang masih direncanakan. Batas ekstraksi graf dan biaya token tersedia di laporan Graphify root.
