# Acceptance Criteria Crawler

Dokumen pendamping [PRD Frontend Crawler](<PRD Frontend Crawler.md>), draf v1.1. Kriteria ini menerima implementasi yang akan dibuat; belum merupakan hasil pengujian aplikasi React. P0 wajib lulus untuk MVP, P1 diterima saat fiturnya dikerjakan.

## 1. Skenario penerimaan

| ID | Kebutuhan | Diberikan | Ketika | Hasil yang diharapkan |
| --- | --- | --- | --- | --- |
| AC-01 | CR-01 | Pengguna berizin membuka Crawler. | Meninjau navigasi lalu membuka URL/survei. | Dua menu utama saja: Otomatis dan Manual. Input URL/Data Survei berada dalam Manual. Pemilih tiga frontend dan proyek tetap jelas; frontend belum tersedia berlabel sesuai status. |
| AC-02 | CR-02 | Operator membuat pekerjaan otomatis. | Memilih platform, query, filter, tanggal, dan baseline. | Nilai tersimpan antar langkah, rentang WIB inklusif/eksklusif jelas, serta konfigurasi efektif per platform terlihat pada review. |
| AC-03 | CR-02, CR-03 | Target 1.000, batas kandidat 500 atau minimum komentar melebihi batas komentar. | Memvalidasi rencana. | Error menunjuk field dan batas yang benar, tombol mulai tidak aktif, tidak ada job atau request crawling platform. |
| AC-04 | CR-02, CR-03 | Konfigurasi valid dan rencana sudah divalidasi. | Mengubah query/filter atau rencana kedaluwarsa. | Hasil validasi dibatalkan, perlu validasi ulang sebelum mulai. Review tidak menampilkan hasil validasi dari input lama. |
| AC-05 | CR-03 | Operator menekan Mulai dan respons server terlambat/putus setelah job dibuat. | Klik ulang/refresh dan rekonsiliasi. | Idempotency key yang sama dipakai, hanya satu job ada, dan UI membuka job yang benar. Tidak menjalankan ulang akuisisi. |
| AC-06 | CR-04 | Job menunggu antrean kemudian worker mulai. | Membuka monitor. | QUEUED belum mempunyai countdown akuisisi aktif. Setelah mulai, deadline server dan durasi terlihat. Refresh mempertahankan ID/status/angka server. |
| AC-07 | CR-04 | Platform memiliki 450 root terkumpul tetapi hanya 300 memenuhi minimum komentar. | Melihat kartu/grafik. | Label menampilkan 450 terkumpul dan 300/1.000 qualified terpisah. Komentar/reply bukan post; progres target bukan progres waktu. |
| AC-08 | CR-04, CR-12 | Event terlambat, terbalik urutan, atau koneksi terputus. | Koneksi kembali. | UI menandai data stale, tidak mengubah ke nol/gagal, mengambil snapshot terbaru, mengabaikan event lama, dan angka konsisten dengan versi server. |
| AC-09 | CR-05 | Reddit menampilkan CAPTCHA dan sesi worker tersedia. | Operator membuka sesi dan menyelesaikan verifikasi. | Sesi yang benar terbuka bagi operator berizin; hanya konfirmasi worker yang mengubah status pulih. Menutup tab atau klik Periksa kembali tidak dianggap lolos. |
| AC-10 | CR-05 | Sesi CAPTCHA tidak tersedia atau waktu tunggu/deadline habis. | Membuka/menunggu verifikasi. | Alasan dan sisa waktu terlihat; tidak ada solver otomatis atau janji bahwa refresh browser biasa memulihkan worker. Platform lain/finalisasi mengikuti status server. |
| AC-11 | CR-05 | Cooldown konfigurasi 360 detik, Retry-After server 600 detik. | Worker menerima 429 Reddit. | Countdown efektif memakai 600 detik, retry dan waktu mulai ditampilkan, tidak ada bypass. YouTube dapat berjalan. Waktu tunggu tetap mengurangi deadline global. |
| AC-12 | CR-05, CR-06 | Retry 429 habis atau sisa deadline lebih pendek daripada tunggu. | Worker berhenti memproses Reddit. | UI menunjukkan alasan dan gap; tidak otomatis memperpanjang deadline atau memulai job baru. Hasil valid yang tersedia difinalisasi. |
| AC-13 | CR-06 | Job RUNNING memiliki data. | Operator mengonfirmasi Hentikan, lalu menekan lagi. | Stop idempoten, status STOP_REQUESTED mendahului finalisasi, dan data parsial valid dapat diterbitkan dengan label sesuai. |
| AC-14 | CR-04, CR-06, CR-10 | Akuisisi berakhir, ekspor masih berjalan atau gagal. | Melihat monitor/hasil. | FINALIZING belum menawarkan unduhan final. Sukses/parsial baru terbit setelah validasi; kegagalan ekspor ditampilkan FAILED dengan alasan, bukan COMPLETED. |
| AC-15 | CR-06 | Pengguna berada di monitor. | Menutup tab, membuka lagi, atau menyalin konfigurasi. | Menutup tab tidak menghentikan worker. Salin konfigurasi membuat draf baru dengan ID pekerjaan baru setelah submit; baseline ditinjau ulang. Tidak menjanjikan resume cursor lama. |
| AC-16 | CR-07, CR-09 | Daftar URL berisi varian URL video sama, URL historis, host eksternal, dan URL valid baru. | Memvalidasi URL. | Varian dinormalisasi, duplikat/historis ditandai, host ditolak, dan hanya URL valid unik terpilih dapat dimulai. Jumlah per kategori dan sumber baseline terlihat sesuai izin. |
| AC-17 | CR-07 | Operator memilih delapan URL valid; query otomatis lama pernah digunakan. | Memulai pekerjaan manual. | Hanya delapan URL itu diproses, tanpa discovery fallback/URL pengganti. Minimum komentar 0 dan filter yang aktif/nonaktif terlihat sebelum mulai. |
| AC-18 | CR-07 | URL format valid tetapi post sudah privat/terhapus atau tidak memenuhi filter. | Worker mengaksesnya. | Status per URL menjelaskan hasil sebenarnya. Daftar valid format tidak diklaim seluruhnya berhasil diambil; hasil akhir PARTIAL bila tujuan ada yang tidak terpenuhi. |
| AC-19 | CR-08 | Operator memasukkan respons survei calon mahasiswa/orang tua dengan template valid. | Validasi lalu Simpan. | Peran, pertanyaan, jawaban, izin, waktu, dan provenance tersimpan. ID dibuat/dijaga stabil. Respons berikutnya tidak membawa jawaban responden sebelumnya. |
| AC-20 | CR-08 | File survei CSV/XLSX, beberapa sheet, kolom berbeda, atau ukuran melebihi batas. | Mengunggah dan mapping. | Format/batas diperiksa server, sheet dipilih eksplisit, field wajib dipetakan, contoh nilai tersedia, dan file bermasalah tidak dikomit. |
| AC-21 | CR-08 | Respons berisi satu jawaban wajib invalid, peran tidak diketahui, atau izin bukan granted. | Review dan pilih impor valid saja. | Error per baris/field muncul, seluruh respons tersebut dikecualikan, dan jumlah respons valid/dilewati disebut eksplisit sebelum commit. Tidak mengimpor sebagian jawaban wajib respons. |
| AC-22 | CR-08, CR-09 | File/respons pernah dikomit atau kunci jawaban sama dengan isi berbeda. | Impor ulang atau ulangi request commit. | Isi identik tidak menambah record; request idempoten. Isi berbeda menjadi konflik, tidak overwrite. Perubahan mapping/data membatalkan validasi lama. |
| AC-23 | CR-09 | Ada jawaban survei dengan teks sama seperti komentar sosial dan akun sosial tanpa peran. | Preview/ekspor dataset. | Kedua sumber tetap mempunyai provenance sendiri; tidak digabung hanya karena teks sama. Peran sosial tetap tidak diketahui, tidak ditebak dari isi. |
| AC-24 | CR-09, CR-10 | Dataset baseline menjadi pengecualian dan akuisisi selesai. | Memeriksa audit hasil, atau memulai saat baseline wajib tidak tersedia. | ID post unik hasil tidak beririsan dengan baseline terpilih, checksum baseline tidak berubah, jumlah duplikasi dan aturan kanonisasi dapat ditelusuri. Baseline wajib yang tidak tersedia memblokir mulai dan tidak dapat dilewati operator. |
| AC-25 | CR-10 | Dataset selesai valid, parsial, kosong, atau skemanya belum didukung NLP. | Memilih Siapkan untuk NLP. | Versi/checksum dibawa, parsial membutuhkan penerimaan eksplisit, kosong/skema tak didukung diblokir dengan alasan. Tidak ada training, penggabungan, atau perubahan snapshot Dashboard otomatis. |
| AC-26 | CR-08, CR-10 | Dataset survei mempunyai metadata peran, versi pertanyaan, dan izin. | Mengekspor atau mengirim ke adapter NLP. | Tidak ada metadata hilang diam-diam agar cocok ke workbook sosial sepuluh kolom. Skema/adapter jelas; prompt pertanyaan terpisah dari teks jawaban. |
| AC-27 | CR-11 | Pengamat atau pengguna proyek lain membuka URL job/dataset langsung. | Mencoba mulai, stop, commit, verifikasi, handoff, atau unduh tanpa izin. | Backend menolak sesuai izin; UI menampilkan pesan tepat tanpa membocorkan data. Tombol tidak tersedia untuk tindakan yang dilarang. |
| AC-28 | CR-11, CR-12 | Konten memuat HTML/script, teks spreadsheet berawalan formula, atau data pribadi. | Preview/ekspor serta logout/ganti proyek. | Konten tidak dieksekusi, ekspor menangani formula, data sensitif tidak masuk URL/telemetry/localStorage, dan cache sensitif dibersihkan saat konteks berganti. |
| AC-29 | CR-12 | Pengguna keyboard/pembaca layar mengisi form, membuka dialog, dan memantau job. | Melakukan alur inti. | Label, error, fokus, dialog, dan status dapat dipahami tanpa mouse/warna. Update rutin tidak merebut fokus atau membacakan timer setiap detik; grafik punya ekuivalen teks/tabel. |
| AC-30 | CR-12 | Viewport 360, 768, atau 1280 piksel; API lambat/gagal. | Menggunakan form, tabel, monitor, dan review. | Tindakan utama tetap terjangkau, tabel tidak merusak halaman, loading/empty/error terpisah, dan retry tidak menggandakan job/commit. Target respons/pembaruan diukur sesuai profil PRD. |
| AC-31 | CR-13, P1 | Preset bernama atau notifikasi dalam aplikasi diaktifkan. | Mengubah/memakai preset atau terjadi status penting. | Preset menjadi draf yang divalidasi ulang; notifikasi terkait job yang diizinkan dan tidak berisi jawaban/data pribadi. |
| AC-32 | CR-14, P0 | Tujuh platform terdaftar di frontend. | Memilih Instagram, TikTok, Threads, Facebook, atau X/Twitter pada simulasi/API. | Query, target, URL, monitor, grafik, dan filter memakai platform terpilih. Simulasi mendukung tujuh sumber; mode API mengikuti capabilities. Platform tanpa adapter tidak dapat dimulai dan alasannya terlihat. |

## 2. Dataset uji dan batas pengujian

Gunakan fixture sintetis untuk survei dan simulasi worker untuk CAPTCHA/429/deadline. Minimum fixture: dua platform dengan root/komentar/reply; varian URL ID sama; baseline dengan beberapa ID bertumpang tindih; respons kedua peran; respons multi-pertanyaan; nilai kosong/invalid; duplikat identik dan konflik; izin tidak diberikan; skema NLP belum didukung; serta kegagalan ekspor.

Uji integrasi terkendali membuktikan adapter/wrapper benar-benar menerima konfigurasi, worker bertahan ketika tab ditutup, event/snapshot tersinkron, sesi CAPTCHA menunjuk browser worker, dan dataset terbit setelah validasi. Pengujian ini memerlukan backend yang diusulkan; fixture UI tidak menjadi bukti integrasi sudah tersedia.

## 3. Syarat siap rilis

- Semua AC P0 lulus, dengan bukti yang dapat ditinjau dan isu tersisa tercatat.
- Setiap CR P0 tercakup pada tabel; kontrak API/skema disepakati frontend dan backend.
- Alur otomatis, URL, survei, hasil parsial, dan akses pengamat dicoba operator.
- Dataset survei nyata belum diaktifkan sebelum akses, izin pemanfaatan, retensi, dan adapter ekspornya siap.
- Pengujian ini tidak mengharuskan target 1.000 post atau coherence model tercapai; keduanya berada pada pengukuran akuisisi nyata atau tahap NLP yang berbeda.

[Kembali ke indeks frontend](README.md)

## 4. Penerimaan revisi visual

- AC-33 (CR-12, P0): Pada desktop/mobile, seluruh teks aktual minimum 13 px dan hitam `#000000`, termasuk helper, sidebar, tabel, placeholder, badge, serta label grafik. Uji computed style dan screenshot; disabled tetap terbaca.
- AC-34 (CR-12, P0): Tema putih–oranye mengikuti token PRD bagian 14.1; tidak ada hijau pada UI, logo, atau grafik.
