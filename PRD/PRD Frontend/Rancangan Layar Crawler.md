# Rancangan Layar Crawler

Dokumen pendamping [PRD Frontend Crawler](<PRD Frontend Crawler.md>), draf v1.1. Wireframe berikut menentukan hierarki dan interaksi untuk implementasi ReactJS; bukan screenshot aplikasi yang sudah berjalan. Seluruh nama pekerjaan dan angka pada wireframe merupakan contoh ilustratif.

## 1. Shell dan aturan tampilan

Pemilih frontend berada di header: **Crawler**, **NLP Machine Learning**, **Dashboard**. Sidebar Crawler hanya berisi **Crawler Otomatis** dan **Crawler Manual**. Proyek aktif, identitas pengguna, dan status koneksi selalu dapat ditemukan. Halaman detail mempertahankan menu asal dan menyediakan tautan kembali.

Arah visual: workspace riset dengan tema putih–oranye, seluruh teks hitam, minimum huruf 13 px, dan kartu ringkas untuk status. Gunakan label teks/ikon bersama warna untuk sukses, peringatan, dan gagal. Satu area mempunyai satu tindakan utama yang jelas; pengaturan teknis jarang dipakai masuk panel Pengaturan lanjut.

Informasi utama dibaca berurutan: **apa yang dikerjakan → status → jumlah/target → kendala → tindakan berikutnya**. Jangan menaruh log mentah di atas status yang dibutuhkan operator. Semua grafik mempunyai tabel atau ringkasan ekuivalen.

## 2. Layar A — Crawler Otomatis

```text
┌ BeeSense  [Crawler ▾]       Proyek: Riset Kampus ▾       Operator ┐
│ Crawler Otomatis │ Crawler Otomatis                             │
│ Crawler Manual   │ [Konfigurasi baru] [Riwayat]                  │
│                  │ Nama pekerjaan: [Riset minat kuliah       ] │
│                  │                                              │
│                  │ 1 Sumber → 2 Filter/target → 3 Pengecualian  │
│                  │                                → 4 Tinjau    │
│                  │ Sumber                                      │
│                  │ [✓] YouTube          [✓] Reddit              │
│                  │ Query YouTube        Query Reddit            │
│                  │ [beasiswa kuliah ]   [biaya kuliah        ]  │
│                  │ [jurusan kampus  ]   Subreddit [indonesia ]  │
│                  │ Satu query per baris                         │
│                  │                                              │
│                  │                        [Lanjutkan]            │
└──────────────────┴──────────────────────────────────────────────┘
```

Langkah 2 mengelompokkan rentang tanggal, keyword, kriteria post, dan batas waktu. Setiap target melekat pada platform yang dipilih, bukan satu angka total ambigu. Bantuan **Apa yang dihitung sebagai post memenuhi kriteria?** menjelaskan minimum komentar unik dan membedakan komentar dari post.

Langkah 3 menampilkan katalog baseline dengan nama, versi, jumlah ID, dan status akses. Bila baseline tidak tersedia, tampilkan peringatan dan blokir mulai sampai pilihan diperbaiki. Baseline wajib proyek tidak dapat dihapus operator; untuk baseline opsional saja, pilihan tanpa baseline harus eksplisit. Jangan diam-diam menganggap indeks kosong.

Langkah 4 memperlihatkan ringkasan efektif. Tindakan **Validasi rencana** menampilkan valid/error/warning tanpa melakukan crawling. Sesudah valid, **Mulai akuisisi** menjadi tindakan utama. Mengubah field membatalkan hasil validasi. Draft lokal yang aman boleh dipulihkan, tetapi tetap memerlukan validasi server baru.

Keadaan layar: capabilities sedang dimuat, backend tidak tersambung, konfigurasi tidak valid, tidak ada platform tersedia, valid dengan warning, dan submit diterima. Tombol retry mengambil ulang kapabilitas; tidak memulai pekerjaan.

## 3. Layar B — Monitor pekerjaan

```text
┌ Crawler Otomatis > Riset minat kuliah                    RUNNING ┐
│ Mulai 09.00 WIB   Deadline 12.00 WIB   Sisa 02:18:42             │
│ Pembaruan 09.41.18 WIB                  [Hentikan akuisisi]     │
│                                                               │
│ ┌ YouTube — Mengambil ───────┐ ┌ Reddit — Menunggu 429 ──────┐ │
│ │ Memenuhi kriteria 300/1000 │ │ Memenuhi kriteria 58/1000   │ │
│ │ Post terkumpul        450 │ │ Post terkumpul          98 │ │
│ │ Komentar             3200 │ │ Komentar               700 │ │
│ │ Reply                 900 │ │ Reply                  200 │ │
│ │ Duplikat dilewati      45 │ │ Retry 1/3, tunggu 04:35    │ │
│ └───────────────────────────┘ └────────────────────────────┘ │
│                                                               │
│ [Progres] [Aktivitas] [Konfigurasi] [Hasil: belum tersedia]      │
│ Grafik kumulatif post memenuhi kriteria menurut waktu          │
│ Tabel angka per platform · penolakan menurut alasan            │
└───────────────────────────────────────────────────────────────┘
```

Angka di atas ilustrasi, bukan hasil pekerjaan baru. Pada tab Progres, grafik waktu mempunyai legenda platform dan target yang jelas. Tab Aktivitas berisi event ringkas dengan timestamp, platform, pesan, dan correlation ID jika error. Event dapat difilter; log mentah yang mengandung data sensitif tidak ditampilkan.

State **FINALIZING** mengganti fokus menjadi “Akuisisi selesai, menyiapkan dan memvalidasi berkas”. Jumlah akhir tetap terlihat, sedangkan tombol unduh belum aktif. State **PARTIAL** menampilkan alasan, misalnya “Batas waktu tercapai; target Reddit belum terpenuhi”, gap per platform, dan tautan hasil.

Saat status stale, banner menyatakan waktu pembaruan terakhir dan bahwa worker mungkin masih berjalan. Operator dapat mencoba menyambungkan kembali. Tombol Mulai tidak muncul pada monitor pekerjaan yang sudah mempunyai ID.

## 4. Layar C — Intervensi Reddit

### CAPTCHA

```text
Reddit memerlukan verifikasi manusia
Pekerjaan: Riset minat kuliah · Sesi worker: tersedia
Sisa jendela verifikasi 08:12 · Deadline pekerjaan 12.00 WIB

Buka sesi browser pekerjaan ini, lalu selesaikan verifikasi.
Status akan diperiksa worker setelah akses pulih.

[Buka sesi verifikasi]  [Periksa kembali]
```

Tampilkan sesi di tab/dialog terotorisasi tanpa membocorkan cookie/token worker. Setelah tab sesi ditutup, status tetap menunggu sampai worker mengonfirmasi. Bila sesi tidak tersedia, tampilkan “Sesi browser worker belum tersedia” beserta tindakan menghubungi operator infrastruktur melalui proses organisasi; UI tidak mengirim pesan eksternal otomatis. CAPTCHA kedaluwarsa memiliki pesan tersendiri.

### HTTP 429

Tampilkan kapan rate limit terjadi, countdown cooldown efektif, retry yang tersisa, dan deadline. Teks bantuan: “Reddit membatasi permintaan. Worker menunggu sebelum memeriksa kembali; YouTube dapat tetap berjalan.” Tidak ada tombol **Paksa lanjut**. Pemeriksaan sesudah countdown berasal dari worker, bukan dari timer browser.

## 5. Layar D — Crawler Manual Input URL

```text
┌ Crawler Manual ────────────────────────────────────────────────┐
│ [Input URL] [Data Survei] [Riwayat]                            │
│ Nama pekerjaan [Daftar video pilihan                       ]  │
│ URL, satu per baris                                           │
│ [ https://www.youtube.com/watch?v=...                       ] │
│ [ https://www.reddit.com/r/.../comments/...                  ] │
│ Batas: 100 URL · 7 platform · post/video                   │
│ [Validasi URL]                                                │
│                                                              │
│ Input 12 | Valid unik 8 | Duplikat 3 | Invalid 1               │
│ Pilih │ Platform │ URL kanonik │ Status/alasan │ Perbaiki     │
│  ✓    │ YouTube  │ ...         │ Valid         │              │
│  —    │ YouTube  │ ...         │ Sudah ada     │ Lihat asal   │
│  —    │ —        │ ...         │ Host ditolak  │ Edit/Hapus   │
│                                                              │
│ Pengambilan: 8 URL terpilih · minimum komentar 0 · 3 jam        │
│ Filter tanggal/keyword: Tidak aktif [Ubah]                     │
│ [ ] Saya memahami 4 input yang tidak akan diproses             │
│                                 [Mulai ambil 8 URL]          │
└──────────────────────────────────────────────────────────────┘
```

Munculkan checkbox pengakuan pengecualian hanya bila ada input dilewati. Angka tombol mengikuti pilihan aktual, tidak mengikuti jumlah seluruh input. Review menampilkan sumber dataset untuk duplikat bila pengguna berhak melihatnya. Sesudah mulai, gunakan monitor bersama dengan tabel progres per URL dan status akses sebenarnya.

## 6. Layar E — Data Survei

### Input formulir

```text
Crawler Manual > Data Survei
[Input formulir] [Impor file]
Survei [Minat studi ▾]  Versi [1 ▾]
Peran responden (*)  ( ) Calon mahasiswa  ( ) Orang tua
Kode responden (*) [RESP-001]  ID respons [Dibuat server]
Waktu pengisian (*) [tanggal dan jam, WIB]
Referensi sumber (*) [Kode pengumpulan internal]
Izin pemanfaatan (*) [Diberikan / Tidak / Belum diketahui ▾]

Q01 — Apa pertimbangan utama memilih jurusan?
[Jawaban teks responden                                    ]
Q02 — Prioritas biaya kuliah (skala 1–5) [ ▾ ]

[Validasi respons]                         [Simpan respons]
```

Tanda wajib dijelaskan di awal. Teks pertanyaan dan batas jawaban berasal dari template. Ringkasan error muncul di atas form sekaligus di field terkait. Simpan dinonaktifkan untuk respons yang invalid atau tidak layak berdasarkan izin pemanfaatan; berikan alasan. Setelah simpan, tampilkan referensi batch/dataset dan pilihan **Input respons berikutnya** tanpa membawa jawaban sebelumnya.

### Impor file

Stepper: **Template dan file → Mapping → Review → Hasil**. Area unggah mendukung tombol file chooser selain drag-and-drop. Cantumkan format, ukuran maksimum, unit satu baris satu jawaban, dan tautan template sintetis. Untuk XLSX, minta pengguna memilih sheet sebelum mapping.

Mapping menampilkan contoh beberapa baris, target field, dan penanda wajib. Review menunjukkan **respons** dan **baris jawaban** dalam kartu berbeda:

```text
Respons: 120 total | 100 valid | 8 duplikat | 7 invalid | 5 tanpa izin
Jawaban: 600 baris · peran calon mahasiswa/orang tua terpisah

[Semua] [Invalid] [Konflik] [Tidak layak] [Duplikat]
Sheet │ Baris │ Response ID │ Field │ Masalah │ Perbaikan

[Kembali ke mapping] [Batalkan]
[ ] Saya memahami 20 respons tidak dimasukkan
[Impor 100 respons valid]
```

Angka ilustrasi mengasumsikan kategori respons akhir saling eksklusif; backend menyediakan kategori agar kartu tidak menghitung respons yang sama dua kali. Error dapat berjumlah lebih dari satu per respons dan ditampilkan sebagai hitungan error terpisah. Respons dengan satu baris wajib invalid tidak diimpor sebagian.

## 7. Layar F — Hasil dataset

```text
Dataset Riset minat kuliah · versi 1 · PARTIAL
Sumber: YouTube + Reddit   Akuisisi: Otomatis   Skema: sosial v1
Alasan parsial dan selisih target per platform

[Ringkasan] [Data] [Kualitas] [Berkas]
Kartu jumlah menurut unit · grafik komposisi dan cakupan waktu
Tabel preview dan detail thread / pertanyaan-jawaban

[Unduh berkas ▾]                          [Siapkan untuk NLP]
```

Untuk survei, ganti kartu sosial dengan jumlah respons/jawaban menurut peran serta kelayakan teks. Jangan memakai label “post” untuk respons survei. Tab Berkas menampilkan checksum/ukuran dan status verifikasi; tautan unduh memerlukan izin dan tidak dipublikasikan permanen.

Siapkan untuk NLP membuka review versi dan kualitas. Dataset parsial memerlukan pengakuan eksplisit. Skema belum didukung atau dataset kosong menghasilkan alasan pemblokiran yang dapat ditindaklanjuti. Tombol ini tidak bernama **Training sekarang**.

## 8. Pola responsif dan aksesibilitas

Pada desktop, sidebar dan dua kartu platform dapat terlihat berdampingan. Pada tablet/mobile, menu menjadi drawer dan kartu bertumpuk. Ringkasan status/deadline muncul sebelum grafik; tindakan utama tidak tertutup sticky footer atau keyboard layar. Tabel padat memakai scroll dalam area tabel, bukan memaksa seluruh halaman melebar.

Fokus pindah ke judul langkah/error summary setelah navigasi yang relevan; pembaruan progres tidak memindahkannya. Dialog stop mengembalikan fokus ke pemicu sesudah ditutup. Semua form dapat dipakai keyboard; chart mempunyai ringkasan dan tabel. Timer tidak diumumkan setiap detik oleh pembaca layar. Peringatan CAPTCHA/terminal diumumkan satu kali saat status berubah.

## 9. Pesan dan tindakan pemulihan

| Keadaan | Pesan contoh | Tindakan |
| --- | --- | --- |
| Belum ada pekerjaan | “Belum ada akuisisi pada proyek ini.” | Buat konfigurasi/input pertama. |
| Validasi gagal | “Target Reddit melebihi batas kandidat.” | Fokus ke field dan tampilkan batas. |
| Backend tidak terhubung | “Konfigurasi belum dapat divalidasi. Input Anda masih tersedia.” | Coba lagi, tanpa membuat job. |
| Progres stale | “Terakhir diperbarui 09.41 WIB. Menyambungkan kembali.” | Rekonsiliasi snapshot. |
| Berkas belum siap | “Akuisisi berakhir. Berkas sedang divalidasi.” | Tunggu status server. |
| Parsial | “Target belum tercapai. Hasil yang tersedia telah disimpan.” | Periksa kualitas atau buat pekerjaan baru. |
| Survei konflik | “ID respons dan pertanyaan sudah ada dengan jawaban berbeda.” | Review asal/perbaiki, tanpa overwrite. |
| Tidak berizin | “Anda tidak memiliki izin melakukan tindakan ini pada proyek tersebut.” | Kembali ke konteks yang diizinkan. |
| Ekspor gagal | “Berkas belum dapat diterbitkan. Referensi masalah: …” | Lihat status/retry server yang diizinkan; jangan unduh berkas setengah jadi. |

[Kembali ke indeks frontend](README.md)

## 10. Revisi tema dan pilihan sumber

Palet wajib mengikuti bagian 14.1 PRD: putih `#FFFFFF`, aksen oranye `#FF8A24`, teks hitam `#000000`, ukuran minimum 13 px. Hapus seluruh aksen hijau. Kartu sumber menampilkan YouTube, Reddit, Instagram, TikTok, Threads, Facebook, dan X/Twitter, dengan deskripsi konten masing-masing. Pada desktop sumber dapat disusun dua kolom; mobile satu kolom agar label 13–15 px tetap terbaca. Form query, monitor, legenda/grafik, filter, dan hasil menyesuaikan sumber yang dipilih.
