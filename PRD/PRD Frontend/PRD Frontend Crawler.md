# PRD Frontend Crawler BeeSense

| Atribut | Nilai |
| --- | --- |
| Versi | 1.1 |
| Tanggal | 29 Oktober 2026 |
| Status | Draf spesifikasi produk; belum diimplementasikan |
| Teknologi frontend | ReactJS dengan TypeScript, aplikasi web untuk operator |
| Bagian sistem | Crawler; frontend NLP Machine Learning dan Dashboard dibahas terpisah |
| Dokumen pendamping | [Rancangan layar](<Rancangan Layar Crawler.md>) · [Acceptance criteria](<Acceptance Criteria Crawler.md>) |

Implementasi frontend setelah penyusunan PRD tersedia pada [Crawler/Frontend](../../Crawler/Frontend/README.md). Mode simulasi dan typed API adapter sudah dibuat; layanan backend untuk kontrak ini masih diperlukan. Tabel kebutuhan di bawah tetap menjadi acuan produk, bukan klaim seluruh integrasi produksi telah tersedia.

## 1. Ringkasan produk

Frontend Crawler membantu tim riset penerimaan mahasiswa memperoleh dan memeriksa data dari media sosial serta survei calon mahasiswa dan orang tua. Pengguna dapat menentukan sumber, menjalankan akuisisi, menangani hambatan akses, memeriksa kualitas, lalu menyediakan dataset berversi untuk tahap NLP.

Di dalam frontend Crawler terdapat **dua menu utama**:

1. **Crawler Otomatis**: sistem menemukan post berdasarkan query, platform, rentang tanggal, dan filter, kemudian mengambil post beserta komentar/reply.
2. **Crawler Manual**: manusia memasukkan URL post tertentu atau data survei. Pilihan **Input URL** dan **Data Survei** berada di dalam menu ini.

“Otomatis” pada MVP berarti pencarian dan pengambilan dilakukan setelah operator memulai pekerjaan. Penjadwalan berulang bukan syarat MVP. “Manual” menyatakan asal masukan dari manusia; pengambilan konten URL tetap dikerjakan worker server.

## 2. Masalah dan hasil yang dituju

Pengaturan crawler saat ini bergantung pada konfigurasi dan perintah Python. Operator membutuhkan antarmuka untuk mengatur penelitian tanpa mengedit file, memahami kemajuan setiap platform, serta mengetahui alasan suatu data masuk, ditolak, atau belum memenuhi target. Data survei juga memerlukan jalur akuisisi dengan konteks responden dan pertanyaan yang terpelihara.

Hasil yang dituju:

- Operator dapat menyiapkan dan memvalidasi pekerjaan melalui formulir ReactJS.
- Progres menunjukkan target, post terkumpul, post memenuhi kriteria, komentar/reply, duplikasi, dan kendala secara terpisah.
- Refresh browser tidak memulai pekerjaan ulang atau menghilangkan progres server.
- URL dan survei dapat ditinjau sebelum dikomit; data yang tidak valid memiliki alasan dan cara memperbaiki.
- Dataset memiliki sumber, versi, audit, dan status kualitas yang jelas sebelum diteruskan ke NLP.

## 3. Pengguna dan izin

MVP menggunakan dua peran yang diusulkan berikut. Backend menjadi penegak izin; menyembunyikan tombol saja tidak cukup.

| Peran | Kebutuhan | Izin |
| --- | --- | --- |
| Operator riset | Mengatur akuisisi, memasukkan URL/survei, mengatasi hambatan, memeriksa hasil | Membuat dan menjalankan pekerjaan, menghentikan pekerjaan, menangani CAPTCHA untuk pekerjaan yang diizinkan, mengomit data manual, menyiapkan dataset untuk NLP. |
| Pengamat/analis | Memantau pekerjaan dan menilai kualitas data | Membaca pekerjaan/dataset di proyek yang diizinkan; unduh hanya bila izin ekspor diberikan. Tidak memulai, menghentikan, atau mengomit. |

Calon mahasiswa dan orang tua merupakan **kelompok responden survei**, bukan pengguna wajib frontend operator ini. MVP menerima jawaban yang sudah diperoleh manusia melalui formulir input operator atau impor file. Pembuatan formulir survei publik, distribusi kuesioner, dan manajemen penerimaan mahasiswa berada di luar lingkup.

## 4. Cakupan dan batas

### 4.1 Prioritas MVP

**P0** wajib tersedia sebelum rilis MVP. **P1** merupakan peningkatan setelah alur inti diterima.

| ID | Prioritas | Kebutuhan |
| --- | --- | --- |
| CR-01 | P0 | Shell dengan pilihan tiga frontend, konteks proyek, dan tepat dua menu utama Crawler. |
| CR-02 | P0 | Form Crawler Otomatis: sumber, query, tanggal, filter, target, durasi, dan pengecualian dataset. |
| CR-03 | P0 | Validasi rencana tanpa crawling, ringkasan konfigurasi, dan mulai pekerjaan sekali saja. |
| CR-04 | P0 | Monitor pekerjaan persisten: progres per platform, deadline, event, dan status koneksi. |
| CR-05 | P0 | Penanganan CAPTCHA manusia dan cooldown HTTP 429 sesuai sesi worker dan deadline. |
| CR-06 | P0 | Hentikan akuisisi dengan aman, finalisasi data parsial, riwayat, dan konfigurasi salinan untuk pekerjaan baru. |
| CR-07 | P0 | Crawler Manual Input URL: satu/banyak URL, validasi, deduplikasi, review, dan pengambilan URL terpilih. |
| CR-08 | P0 | Crawler Manual Data Survei: input formulir dan impor CSV/XLSX dengan mapping, preview, dan commit. |
| CR-09 | P0 | Deduplikasi dan provenance, termasuk baseline historis serta identitas respons survei. |
| CR-10 | P0 | Pemeriksaan dataset, status parsial, ekspor tervalidasi, dan handoff ke NLP berbasis versi. |
| CR-11 | P0 | Izin, perlindungan data responden, dan audit tindakan. |
| CR-12 | P0 | Aksesibilitas, responsivitas, penanganan error, dan pemulihan koneksi. |
| CR-13 | P1 | Preset konfigurasi bernama dan notifikasi dalam aplikasi yang dapat dikonfigurasi. |
| CR-14 | P0 | Pilihan tujuh platform: YouTube, Reddit, Instagram, TikTok, Threads, Facebook, dan X/Twitter, dengan kapabilitas adapter yang dinyatakan jelas. |

### 4.2 Di luar MVP

Penjadwalan rutin, ekspansi otomatis akun/proxy, penyelesaian CAPTCHA otomatis, pengambilan konten privat, dashboard insight topik, pelatihan model, penyuntingan dataset terbit secara langsung, dan penggabungan dataset otomatis tidak termasuk MVP. Tautan ke frontend lain menyampaikan konteks dataset, bukan menjalankan training.

### 4.3 Dasar sistem yang sudah ada

| Area | Kondisi kode saat penyusunan | Kebutuhan pengembangan |
| --- | --- | --- |
| Akuisisi sosial | YouTube dan Reddit; konfigurasi JSON; `plan()`/dry-run dan `run()` pada [social_crawler.py](../../social_crawler.py). | API dan worker persisten yang membungkus kapabilitas tersebut. |
| Eksekusi | Batas waktu global, round robin, deduplikasi historis, event progres, CAPTCHA manual, cooldown 429. | Pemetaan status/progres menjadi kontrak UI dan pengendalian pekerjaan yang aman. |
| Ekspor | Bundle audit, workbook sosial, summary, dan manifest. | Katalog dataset, kontrol akses, preview, dan unduh sesudah finalisasi. |
| Input URL | Crawler menerima URL di konfigurasi. | Mode URL saja yang menjamin tidak memicu discovery query sebagai fallback. |
| Survei | Belum ada jalur survei yang memenuhi spesifikasi dokumen ini. | Validasi/import/form dan skema survei berversi. |
| Frontend | Dashboard saat ini menggunakan [main.py](../../main.py), Streamlit. | Frontend Crawler ReactJS baru; tidak mengganti Dashboard dalam pekerjaan PRD ini. |

Rujukan perilaku crawler: [SOCIAL_CRAWLER.md](../../SOCIAL_CRAWLER.md) dan [social_crawler.json](../../social_crawler.json). Angka bawaan di bawah diambil dari konfigurasi proyek saat ini atau ditandai sebagai usulan produk.

## 5. Struktur informasi dan navigasi

```text
BeeSense — pemilih frontend: Crawler | NLP Machine Learning | Dashboard
└── Crawler — proyek aktif
    ├── Crawler Otomatis
    │   ├── Konfigurasi baru
    │   └── Riwayat → Detail pekerjaan → Hasil dataset
    └── Crawler Manual
        ├── Input URL
        ├── Data Survei
        └── Riwayat → Detail pekerjaan/import → Hasil dataset
```

Riwayat disajikan sebagai tab pada masing-masing menu, dengan filter sumber, status, tanggal, dan pencarian nama/ID. Detail pekerjaan dapat ditautkan langsung dan tetap menandai menu asalnya. Hasil dataset dibuka dari pekerjaan terkait. Tidak ada menu utama ketiga untuk riwayat atau dataset.

Rute yang diusulkan:

| Rute | Tampilan |
| --- | --- |
| `/crawler/automatic` | Konfigurasi otomatis dan tab Riwayat. |
| `/crawler/automatic/jobs/:jobId` | Monitor, event, dan hasil pekerjaan otomatis. |
| `/crawler/manual?tab=url` | Input URL dan riwayat manual. |
| `/crawler/manual?tab=survey` | Input/impor survei dan riwayat manual. |
| `/crawler/manual/jobs/:jobId` | Detail pekerjaan URL/import survei. |

Identitas proyek berasal dari konteks yang diverifikasi server. URL boleh menyimpan tab/filter/ID, bukan isi jawaban survei, token, atau informasi pribadi. Jika frontend NLP/Dashboard belum tersedia, tampilkan status belum tersedia; jangan menampilkan tautan yang rusak.

## 6. Crawler Otomatis

### 6.1 Alur pengguna

**Pilih proyek → tentukan sumber dan query → tetapkan filter/target → validasi rencana → tinjau → mulai → pantau → periksa hasil → siapkan untuk NLP.**

Form menggunakan empat langkah: **Sumber**, **Filter dan target**, **Pengecualian**, **Tinjau**. Pengguna dapat kembali ke langkah sebelumnya tanpa kehilangan input. Konfigurasi yang sedang berjalan bersifat tetap; perubahan menghasilkan draf pekerjaan baru.

### 6.2 Masukan dan validasi

| Kelompok | Field dan perilaku |
| --- | --- |
| Identitas | Nama pekerjaan wajib, proyek aktif, deskripsi opsional. Identitas operator dan waktu dicatat server. |
| Platform | Tujuh pilihan sumber: YouTube, Reddit, Instagram, TikTok, Threads, Facebook, dan X/Twitter. Minimal satu aktif. Seluruhnya dapat dicoba pada simulasi; mode API mengaktifkan pilihan sesuai capabilities backend dan menjelaskan adapter yang belum tersedia. |
| Query | Daftar query per platform; satu baris satu query, trim dan dedup. Minimal satu query efektif per platform otomatis; jangan diam-diam membuat query dari field lain. Maksimum 100 query/platform, 300 karakter/query sesuai validasi crawler saat ini. |
| Reddit | Pilihan subreddit; preset proyek dapat berisi `indonesia`, `karir`, `indotech`. Maksimum 10 sesuai adapter saat ini; tampilkan aturan nama dari capabilities server. |
| Tanggal konten | Mulai dan akhir dengan zona WIB. Mulai inklusif, akhir eksklusif; mulai harus lebih kecil dari akhir. Label contoh: “Sampai sebelum 30 Okt 2026, 00.00 WIB”. Waktu pengambilan merupakan field terpisah. |
| Keyword | Include, mode salah satu/semua, dan exclude. Exclude mengalahkan include. Tampilkan dampak terhadap root/thread dan komentar. |
| Target | Target post memenuhi kriteria per platform, minimum komentar unik/post, serta batas kandidat dan pengambilan. Target tidak menjanjikan hasil. |
| Waktu | Durasi maksimum akuisisi 3 jam pada preset proyek; nilainya dapat ditinjau sebelum mulai. Deadline dihitung dari waktu worker mulai, bukan saat membuka formulir/menunggu antrean. |
| Batas lanjut | Maksimum komentar/reply, jeda, timeout, retry 429, dan waktu tunggu CAPTCHA dalam panel Pengaturan lanjut. Nilai di luar kapabilitas backend ditolak. |
| Dataset pengecualian | Pilih satu atau lebih dataset terbit yang dapat diakses dari katalog. Tampilkan versi dan jumlah ID yang diindeks. Baseline `social_20261028_01` menjadi preset proyek bila tersedia. Tidak meminta operator mengetik path server. |

Nilai preset riset proyek saat ini:

| Pengaturan | Nilai |
| --- | --- |
| Target | 1.000 post memenuhi kriteria untuk YouTube dan 1.000 untuk Reddit. |
| Minimum komentar | 10 komentar unik termasuk reply per post. |
| Batas bersama | 10.800 detik; round robin, satu operasi platform pada satu waktu. |
| Batas per platform | Maksimum 4.000 percobaan post dan 6.000 kandidat. |
| Isi thread | Maksimum 100 komentar, 30 reply, 10 reply per thread sesuai konfigurasi adapter. |
| Jeda dan timeout | Jeda tetap 2 detik; timeout request 90 detik. |
| Reddit 429 | Cooldown awal 360 detik, maksimum 3 retry per pekerjaan; server Retry-After yang lebih lama dihormati. |
| Reddit CAPTCHA | Maksimum menunggu 600 detik; pemeriksaan worker setiap 5 detik. |

Tanggal penelitian historis tidak otomatis dipakai untuk penelitian baru. Operator harus memilih rentang tanggal; preset filter dapat diambil dari konfigurasi proyek dan ditinjau. Nilai batas final berasal dari capabilities backend agar frontend dan crawler tidak berbeda aturan.

Filter include diterapkan pada judul/deskripsi root. Komentar tidak wajib mengulang keyword include agar konteks diskusi tetap tersimpan. Root yang terkena exclude mengeluarkan seluruh thread; komentar yang terkena exclude dapat dikeluarkan sendiri. Post tanpa tanggal yang dapat dipastikan tidak lolos filter tanggal aktif; tanggal komentar perkiraan tetap ditandai sebagai perkiraan.

Jika kebijakan proyek mewajibkan baseline tertentu, mulai diblokir sampai indeks versi baseline tersebut tersedia dan valid. Operator tidak dapat menghapus baseline wajib untuk melewati pemeriksaan duplikasi.

Target post tidak boleh melebihi batas percobaan/kandidat; minimum komentar tidak boleh melebihi batas komentar. Validasi menunjukkan field yang salah, nilai yang diterima, dan tindakan perbaikan. Pemeriksaan rencana tidak melakukan request crawling ke platform.

### 6.3 Review dan mulai

Review menampilkan konfigurasi efektif per platform, target, kriteria post, tanggal, durasi, dataset pengecualian, serta peringatan kemampuan browser bila Reddit dipilih. Tombol **Mulai akuisisi** hanya aktif setelah validasi server berhasil dan input belum berubah. Setiap perubahan membatalkan hasil validasi sebelumnya.

Satu klik menghasilkan satu pekerjaan dengan idempotency key. Saat respons belum pasti karena koneksi terputus, frontend mencari hasil berdasarkan key yang sama; jangan mengirim pekerjaan baru dengan key baru. Submit dinonaktifkan selama permintaan diproses. Pekerjaan menunggu antrean memperoleh ID dan layar detail sebelum worker mulai.


### 6.4 Tujuh sumber media sosial

| Platform | ID konfigurasi | Jenis konten yang dipilih di UI | Status integrasi |
| --- | --- | --- | --- |
| YouTube | `youtube` | Video/Shorts, komentar, reply | UI/simulasi tersedia; crawler Python sudah ada, wrapper API diperlukan. |
| Reddit | `reddit` | Post, komentar, reply | UI/simulasi tersedia; crawler Python sudah ada, wrapper API/sesi worker diperlukan. |
| Instagram | `instagram` | Post, Reels, komentar | UI/simulasi tersedia; adapter akuisisi backend perlu dibuat. |
| TikTok | `tiktok` | Video/foto dan komentar | UI/simulasi tersedia; adapter akuisisi backend perlu dibuat. |
| Threads | `threads` | Post dan balasan | UI/simulasi tersedia; adapter akuisisi backend perlu dibuat. |
| Facebook | `facebook` | Post/Reel dan komentar | UI/simulasi tersedia; adapter akuisisi backend perlu dibuat. |
| X / Twitter | `x` | Post dan balasan | UI/simulasi tersedia; adapter akuisisi backend perlu dibuat. |

Setiap sumber mempunyai query, target, batas pengambilan, status, progres, serta penyaring hasil sendiri. Seri grafik dan filter tidak boleh mengasumsikan hanya dua platform. Dua sumber lama tetap dipilih pada preset awal; lima tambahan dapat dipilih eksplisit agar target total tidak berubah diam-diam.

Mode API memakai daftar sumber yang tersedia dari backend. Jika sebuah platform belum mempunyai adapter, tampilkan pilihan beserta alasan belum tersedia; jangan menyatakan crawling nyata berhasil. Bentuk pencarian, akses komentar/balasan, dan batas spesifik mengikuti kemampuan adapter, bukan anggapan semua platform mempunyai API atau jangkauan pencarian yang sama.

Normalisasi URL menghapus tracking dan mengenali alias domain yang didukung. Instagram/Threads memakai locator permalink sebelum ID final diverifikasi; Facebook dapat memerlukan resolusi alias halaman di backend. Deduplikasi lintas alias tidak dianggap tuntas hanya dari pola URL. Tautan pendek yang belum dapat diresolusi harus meminta permalink lengkap, bukan membuka host baru secara bebas.

## 7. Monitor dan kendali pekerjaan

### 7.1 Informasi utama

Monitor menampilkan nama, ID, mode, operator, waktu mulai, deadline, sisa waktu, waktu pembaruan terakhir, dan status koneksi. Deadline bersumber dari server; countdown lokal hanya penyajian dan disinkronkan ulang.

Setiap kartu platform memisahkan:

- Target dan **post memenuhi kriteria**, misalnya `300 / 1.000`.
- Post terkumpul unik, termasuk yang belum memenuhi minimum komentar.
- Komentar dan reply unik, kandidat diperiksa, duplikasi dilewati, serta data ditolak per alasan.
- Status platform, operasi terakhir, cooldown/CAPTCHA bila ada, dan alasan berhenti.

Persentase target memakai post memenuhi kriteria/target. Persentase waktu memakai waktu berlalu/durasi. Keduanya memiliki label berbeda; total baris dataset tidak menjadi persentase keberhasilan. Jika total kandidat tidak diketahui, tampilkan jumlah saja tanpa persentase rekaan.

Grafik operasional MVP: garis kumulatif post memenuhi kriteria per platform menurut waktu, komposisi post/komentar/reply, serta jumlah penolakan menurut alasan. Semua grafik mempunyai ringkasan teks dan tabel ekuivalen. Grafik dipakai untuk menjelaskan akuisisi, bukan insight topik NLP.

### 7.2 Model status yang diusulkan

Status API berikut merupakan rancangan wrapper baru, bukan nama status Python yang seluruhnya sudah tersedia.

| Status pekerjaan | Makna dan tindakan UI |
| --- | --- |
| `QUEUED` | Diterima server, belum mulai; deadline akuisisi belum berjalan. |
| `RUNNING` | Worker melakukan akuisisi atau menunggu akses platform; tampilkan status per platform. |
| `STOP_REQUESTED` | Permintaan berhenti diterima; tunggu worker menyelesaikan operasi secara aman. |
| `FINALIZING` | Akuisisi berakhir; ekspor, validasi, dan manifest sedang diselesaikan. Jangan tampilkan unduhan final. |
| `COMPLETED` | Tujuan mode terpenuhi dan dataset valid telah terbit. |
| `PARTIAL` | Dataset valid terbit, tetapi sebagian tujuan tidak tercapai. Tampilkan penyebab dan selisih target. |
| `FAILED` | Tidak ada dataset terbit yang dapat dipakai; tampilkan alasan dan jalur perbaikan. |
| `CANCELLED` | Dihentikan pengguna. Jika ada dataset parsial valid, tampilkan dataset itu dengan label parsial; jangan mengubahnya menjadi keberhasilan penuh. |

Status per platform: `PENDING`, `FETCHING`, `WAITING_CAPTCHA`, `RATE_LIMITED`, `TARGET_REACHED`, `EXHAUSTED`, `BLOCKED`, `STOPPED`, `ERROR`. Satu platform menunggu tidak otomatis menghentikan platform lain; worker tetap menentukan operasi yang aman.

`TARGET_MET` dari crawler otomatis dipetakan ke `COMPLETED` hanya setelah finalisasi berhasil. Mencapai target bukan bukti seluruh komentar di platform telah habis diambil. Tidak ada data karena filter atau kandidat habis ditampilkan sebagai hasil parsial kosong dengan alasan yang jelas; gangguan validasi/worker/ekspor merupakan kegagalan, bukan “nol data” yang menutupi error.

### 7.3 CAPTCHA dan HTTP 429

**CAPTCHA:** tampilkan pemberitahuan “Reddit memerlukan verifikasi manusia”, sisa jendela verifikasi, serta tombol **Buka sesi verifikasi**. Tombol membuka sesi browser terotorisasi yang dipakai worker: jendela Chrome worker pada instalasi lokal atau koneksi browser interaktif aman pada server jarak jauh. Membuka Reddit biasa di browser operator bukan bukti sesi worker sudah lolos.

Worker memeriksa pemulihan akses. Tombol **Periksa kembali** hanya meminta pengecekan, tidak menandai CAPTCHA selesai. Jika sesi tidak tersedia, akses ditolak, jendela habis, atau deadline global tercapai, tampilkan alasan dan lanjutkan finalisasi/pekerjaan platform lain sesuai status server. CAPTCHA tidak diselesaikan otomatis. Ketersediaan sesi browser harus lolos pemeriksaan sebelum alur Reddit dinyatakan siap rilis.

**HTTP 429:** kartu Reddit menampilkan waktu terdeteksi, durasi tunggu, waktu paling awal pemeriksaan ulang, serta retry keberapa dari batas maksimum. Cooldown efektif adalah nilai terbesar antara kebijakan konfigurasi dan Retry-After server. Contoh awal 360 detik bukan jaminan akses sudah pulih.

Tidak tersedia tombol yang mengabaikan cooldown. YouTube tetap dapat berjalan selama Reddit menunggu. Semua waktu tunggu termasuk batas akuisisi tiga jam. UI tidak memperpanjang deadline diam-diam; akuisisi baru memerlukan pekerjaan baru.

### 7.4 Berhenti, refresh, dan gangguan koneksi

**Hentikan akuisisi** meminta konfirmasi singkat yang menjelaskan penyimpanan hasil parsial, lalu mengirim stop sekali. UI tidak langsung menandai pekerjaan berhenti sebelum server mengonfirmasi. Pengguna boleh berpindah halaman atau menutup tab; worker tetap berjalan.

MVP menyediakan hentikan, bukan pause/resume umum. Pemulihan CAPTCHA/cooldown dalam pekerjaan aktif tetap didukung. **Buat pekerjaan baru dari konfigurasi ini** menyalin konfigurasi menjadi draf, memakai ID baru dan pengecualian dataset yang ditinjau kembali; ini bukan melanjutkan cursor lama secara implisit.

Saat offline atau heartbeat terlambat, pertahankan data terakhir dengan label **Status belum diperbarui**. Jangan menebak `FAILED` atau mengubah angka menjadi nol. Setelah tersambung, ambil snapshot server sebelum menerapkan event baru. Jika worker hilang, backend harus memberikan status pemulihan atau kegagalan eksplisit.

## 8. Crawler Manual melalui URL

### 8.1 Alur dan cakupan

**Input URL → validasi dan normalisasi → tinjau URL unik → tentukan batas pengambilan → mulai → pantau → periksa hasil.** Satu input dapat berisi satu URL atau beberapa baris URL dari tujuh platform yang terdaftar. Batas MVP usulan: 100 URL per pekerjaan manual; angka ini diterbitkan server sebagai capability.

Format URL awal mencakup video/Shorts YouTube, post Reddit, post/Reel Instagram, video/foto TikTok, post Threads, post/Reel Facebook, dan post X/Twitter. Validasi bentuk URL bukan bukti konten tersedia atau ID API sudah terverifikasi; adapter backend memeriksa akses dan identitas final. URL profil, kanal, hasil pencarian, playlist, tautan pendek yang belum didukung, host lain, atau skema non-HTTP(S) ditolak dengan alasan. Parameter tracking tidak membuat konten menjadi post baru. URL berisi kredensial ditolak, dan redirect harus tetap diverifikasi backend.

### 8.2 Review dan aturan eksekusi

Tabel review berisi input asal, platform, URL kanonik, ID post, status, alasan, dan pilihan sertakan. Status review: **Valid**, **Duplikat input**, **Sudah ada di dataset**, **Tidak didukung**, atau **Tidak valid**. Pengecekan konten terhapus/privat baru dapat dipastikan saat worker mengaksesnya; jangan menyatakan URL dapat diambil hanya berdasarkan format.

Duplikat tidak dapat dipilih ulang pada pekerjaan yang sama. URL invalid dapat diperbaiki/dihapus. Sebelum mulai, ringkasan menampilkan jumlah input, valid unik, duplikat, invalid, dan jumlah terpilih. Minimal satu URL valid unik terpilih diperlukan. Pengguna dapat melanjutkan hanya URL valid setelah mengakui item yang dilewati.

Mode URL tidak menjalankan discovery query, menambahkan URL pengganti, atau diam-diam mengisi target 1.000 post. Tujuannya memproses daftar terpilih. Tanggal/keyword dapat diaktifkan sebagai filter opsional dan selalu terlihat pada review; tidak ada filter tersembunyi dari pekerjaan otomatis sebelumnya.

Default usulan minimum komentar untuk URL adalah 0 agar URL yang diminta tetap dapat dikumpulkan meskipun komentarnya sedikit. Batas komentar/reply dan durasi ditampilkan sebelum mulai. Bila operator menetapkan minimum lebih tinggi, hasil tetap menunjukkan URL berhasil diambil dan apakah kriteria komentarnya terpenuhi sebagai dua hal berbeda.

Setiap URL mempunyai hasil akhir: diperoleh, tidak memenuhi filter, tidak tersedia/privat, gagal akses, atau tidak selesai sebelum deadline. Pekerjaan `COMPLETED` memerlukan semua URL terpilih diperoleh dan kriteria yang diaktifkan terpenuhi; URL yang terselesaikan sebagai penolakan/gagal menghasilkan `PARTIAL` dengan rincian. Kegagalan finalisasi tetap `FAILED`. Monitor, CAPTCHA, 429, dan ekspor menggunakan komponen bersama.

## 9. Crawler Manual untuk data survei

### 9.1 Jenis masukan

Menu **Data Survei** menyediakan **Input formulir** dan **Impor file**. Keduanya mencatat jawaban yang telah diperoleh manusia dari calon mahasiswa atau orang tua. Operator tidak diminta menebak peran responden berdasarkan isi jawaban.

Form mengikuti template survei berversi: pilih survei/versi, peran responden, kode responden pseudonim, ID respons, waktu pengisian, lalu jawaban sesuai pertanyaan. MVP mendukung jawaban teks, pilihan, dan angka/skala yang ditetapkan template. Tidak mencakup unggahan dokumen responden atau editor kuesioner bebas.

### 9.2 Kontrak data survei yang diusulkan

Untuk impor, **satu baris adalah satu jawaban untuk satu pertanyaan**. Satu respons dapat mempunyai beberapa baris dengan metadata respons yang konsisten.

| Field | Wajib | Aturan |
| --- | --- | --- |
| `survey_id`, `survey_version` | Ya | Cocok dengan template tersedia; versi tidak berubah setelah commit. |
| `response_id` | Ya | Identitas satu pengisian survei. Form dapat memperoleh ID baru dari server; impor menggunakan ID sumber yang stabil. |
| `respondent_code` | Ya | Pseudonim, bukan nama/NIK/nomor telepon. Dipakai untuk provenance, bukan untuk menyatukan orang lintas survei tanpa aturan. |
| `respondent_role` | Ya | `prospective_student` atau `parent`, berdasarkan informasi sumber. Tidak diketahui masuk daftar perlu perbaikan. |
| `submitted_at` | Ya | Tanggal/waktu pengisian dengan offset; UI menampilkan WIB. Waktu akuisisi dicatat terpisah. |
| `question_id` | Ya | Terdaftar pada versi template. Teks pertanyaan berasal dari template, bukan menjadi bagian otomatis teks jawaban. |
| `answer_text` | Kondisional | Wajib untuk pertanyaan teks yang diwajibkan template; tidak boleh hanya whitespace. |
| `answer_value` | Kondisional | Pilihan atau angka sesuai tipe/rentang template. Pertanyaan opsional dapat kosong dengan penanda jawaban kosong. |
| `usage_permission` | Ya | `granted`, `not_granted`, atau `unknown`, didukung pencatatan sumber. Hanya `granted` layak masuk dataset analisis MVP. Ini atribut izin pemanfaatan data, bukan sertifikasi hukum. |
| `source_reference` | Ya | Referensi internal asal pengumpulan, tanpa URL publik berisi data pribadi. |

`project_id`, `input_mode`, `source_kind=survey`, operator, waktu ingest, ID batch, checksum berkas, serta status validasi ditambahkan server. Contoh berkas/template menggunakan data sintetis saja. Pertanyaan skala/pilihan tetap disimpan meskipun belum ada teks yang layak untuk NLP.

### 9.3 Impor dan commit

**Pilih template → unggah → mapping → validasi → review → commit → hasil.** Format MVP: CSV UTF-8 dan XLSX tanpa macro. Batas usulan: 10 MB dan 10.000 baris jawaban per batch; satu sheet dipilih eksplisit pada XLSX. Batas dikirim server, dan validasi server tetap wajib.

Mapping menampilkan kolom sumber, field tujuan, contoh nilai, dan field wajib yang belum terpetakan. File dengan beberapa sheet tidak digabung diam-diam. UI tidak mengeksekusi formula atau menampilkan HTML aktif dari jawaban. Output spreadsheet menangani teks yang dapat ditafsirkan sebagai formula.

Review menampilkan jumlah respons, jumlah baris jawaban, peran, duplikat, invalid, serta tidak layak analisis. Error menyebut sheet/baris/field dan saran perbaikan. Operator dapat memperbaiki sumber lalu memvalidasi ulang, membatalkan, atau memilih **Impor respons valid saja** dengan ringkasan pengecualian eksplisit.

Unit commit adalah **respons lengkap**, bukan baris terpisah. Bila satu jawaban wajib pada respons invalid, seluruh respons ditahan agar pertanyaannya tidak terpotong. Respons tidak berizin atau tidak diketahui izinnya tidak ikut commit ke dataset analisis; tampilkan jumlah dan alasan. Berkas staging yang ditahan mengikuti retensi terbatas backend dan tidak muncul pada handoff NLP.

Tombol **Simpan respons**/**Impor respons valid** membutuhkan validasi server terbaru. Commit bersifat idempoten dan menghasilkan dataset/batch baru. Mengunggah ulang berkas yang sama tidak menggandakan data; perubahan jawaban dengan kunci sama menjadi konflik yang memerlukan review, bukan overwrite. Perbaikan setelah terbit menghasilkan versi dataset baru.

## 10. Aturan kualitas, duplikasi, dan provenance

| Jenis | Kunci dan perilaku |
| --- | --- |
| Root sosial | Platform + native post ID; URL kanonik sebagai pendukung/fallback terverifikasi. Varian URL video/post yang sama merupakan satu root. |
| Komentar/reply | Platform + native content ID jika tersedia, dengan relasi root/parent. Fallback harus stabil, terdokumentasi, dan tidak menyamakan komentar hanya karena teksnya sama. |
| Historis sosial | Bandingkan dengan dataset pengecualian yang dipilih sebelum pengambilan dan sebelum ekspor. Duplikat root beserta thread tidak diakuisisi ulang dalam kebijakan ini. Baseline tidak dimutasi. |
| Survei | Proyek + survei + versi + response ID + question ID. Kunci sama dan isi sama dilewati; kunci sama dan isi berbeda menjadi konflik. |
| Lintas sumber | Jawaban survei dan komentar sosial yang kebetulan sama teksnya tidak otomatis digabung. Kode responden tidak dipakai sebagai native ID sosial. |

Setiap record menyimpan sumber, mode akuisisi, waktu konten/pengisian, waktu ingest, referensi asal, ID pekerjaan/batch, dan alasan kelayakan. Ketidakpastian tanggal, komentar kehilangan parent yang terfilter, dan post di bawah minimum komentar tetap terlihat sebagai flag.

Peran calon mahasiswa/orang tua hanya ada bila dideklarasikan pada sumber survei. Untuk sumber sosial, peran responden tidak diketahui secara default. Pemisahan ini harus bertahan di preview, ekspor, dan handoff.

Jumlah duplikasi, penolakan, dan kelayakan dilaporkan dalam unit yang disebutkan jelas. UI tidak menjumlahkan root dan komentar sebagai “jumlah post”, atau jumlah jawaban sebagai “jumlah responden”.

## 11. Hasil dataset dan handoff

Halaman hasil dibuka setelah finalisasi, dengan tab **Ringkasan**, **Data**, **Kualitas**, dan **Berkas**. Isi minimum:

- Nama/ID dataset, versi, skema, sumber, mode, waktu, konfigurasi efektif, dan checksum manifest.
- Untuk sosial: post, komentar, reply, post memenuhi kriteria, serta gap target per platform.
- Untuk survei: respons dan jawaban per peran, jenis pertanyaan, jumlah tanpa teks, konflik/penolakan, dan kelayakan NLP.
- Tabel paginasi dengan filter platform/sumber, jenis konten, peran survei, tanggal, status kualitas, dan pencarian. Detail membuka konteks thread atau pertanyaan/jawaban, sesuai sumber.
- Grafik komposisi sumber/jenis konten, cakupan waktu, dan alasan penolakan; tidak menampilkan sentiment/topik yang belum dihitung.
- Daftar berkas siap unduh dengan format, ukuran, checksum, dan status validasi. Jangan menawarkan artefak setengah ditulis sebagai hasil final.

Bundle sosial mempertahankan workbook audit delapan sheet, workbook ringkas `social_data.xlsx` sepuluh kolom, JSONL, summary, dan manifest sesuai kemampuan eksportir saat ini. Dukungan metadata survei memerlukan skema baru serta representasi audit/ekspor tersendiri; jangan memaksa role/pertanyaan ke kolom judul atau menghilangkannya agar cocok dengan workbook sosial.

**Siapkan untuk NLP** menghasilkan pilihan input berisi ID dataset, versi, checksum, skema, dan ringkasan kelayakan. Untuk dataset parsial, operator harus menerima status parsial secara eksplisit. Jika adapter skema NLP belum mendukung survei, tindakan diblokir dengan alasan dan kebutuhan adapter; file tetap dapat diperiksa/diunduh oleh pengguna berizin. Dataset kosong tidak dapat disiapkan untuk training.

Tindakan ini tidak menggabungkan dataset, melatih model, atau menerbitkan Dashboard. Target jumlah topik dan coherence diatur di modul NLP. Dataset sumber tidak ditimpa, dan snapshot model aktif tidak berubah.

## 12. Kontrak integrasi yang diusulkan

Semua endpoint berikut adalah **usulan untuk backend baru**. Prefix proyek, autentikasi, payload final, dan OpenAPI akan dirinci pada PRD Backend. Frontend tidak membaca path lokal atau menjalankan Python dari browser.

| Operasi | Endpoint contoh | Keluaran yang diperlukan UI |
| --- | --- | --- |
| Kapabilitas dan template | `GET /api/v1/projects/:projectId/crawler/capabilities` | Platform/mode tersedia, batas field/upload, dukungan sesi CAPTCHA, template survei/versi, izin. |
| Katalog baseline | `GET /api/v1/projects/:projectId/datasets` | Dataset ID/versi/skema, status, jumlah, akses. |
| Validasi rencana | `POST /api/v1/projects/:projectId/acquisition-plans/validate` | Konfigurasi efektif, error field, warning, plan ID/hash dan waktu kedaluwarsa. Tanpa crawling. |
| Mulai pekerjaan | `POST /api/v1/projects/:projectId/acquisition-jobs` | Job ID, plan yang dipakai, status awal. Header `Idempotency-Key` wajib. |
| Daftar/detail | `GET /api/v1/projects/:projectId/acquisition-jobs[/:jobId]` | Riwayat terpaginasikan atau snapshot lengkap untuk job yang diizinkan. |
| Event pekerjaan | `GET /api/v1/projects/:projectId/acquisition-jobs/:jobId/events` | Stream SSE dengan event ID, urutan, waktu server, dan versi snapshot. Polling detail menjadi fallback. |
| Hentikan | `POST /api/v1/projects/:projectId/acquisition-jobs/:jobId/stop` | Stop diterima atau status terminal terkini; pengulangan aman. |
| Sesi verifikasi | `POST /api/v1/projects/:projectId/acquisition-jobs/:jobId/verification-session` | Akses browser worker berumur pendek, platform, expiry, dan status; hanya operator berizin. |
| Staging survei | `POST /api/v1/projects/:projectId/survey-imports` | Import ID dan metadata file/form. Data tidak langsung diterbitkan. |
| Validasi survei | `POST /api/v1/projects/:projectId/survey-imports/:importId/validate` | Mapping efektif, versi validasi, hitungan respons/baris, konflik, daftar error terpaginasikan. |
| Commit survei | `POST /api/v1/projects/:projectId/survey-imports/:importId/commit` | Job ID pemrosesan dan hasil akhir dataset; idempotency key serta versi validasi wajib. |
| Hasil dan berkas | `GET /api/v1/projects/:projectId/datasets/:datasetId/versions/:version` | Manifest, kualitas, preview terpaginasikan, izin dan akses unduh berumur pendek. |
| Handoff NLP | `POST /api/v1/projects/:projectId/nlp-input-selections` | Referensi dataset tetap dan status penerimaan parsial; tidak menjalankan training. |

Snapshot pekerjaan minimal memuat `job_id`, `mode`, `status`, `phase`, `created_at`, `started_at`, `deadline_at`, `updated_at`, `snapshot_version`, `platforms`, `counts`, `stop_reason`, `dataset_ref`, dan `allowed_actions`. `dataset_ref` kosong sampai finalisasi berhasil. Per platform tersedia target, acquired roots, qualified roots, komentar/reply unik, duplikasi, error, serta waktu CAPTCHA/cooldown.

Server memisahkan `counts` menurut unit. Event tidak boleh dipakai sebagai satu-satunya penyimpanan; snapshot menjadi dasar rekonsiliasi setelah refresh atau event terlewat. Error terstruktur memuat kode, pesan aman, field/baris terkait, tindakan perbaikan, dan correlation ID. `401/403`, validasi `422`, konflik `409`, backend sibuk, serta kegagalan jaringan memiliki tampilan berbeda. HTTP 429 dari API BeeSense dibedakan dari 429 Reddit di worker.

SSE atau polling terautentikasi menggunakan sesi yang aman; jangan memasukkan token jangka panjang pada query URL. Server mengotorisasi ulang setiap pekerjaan, dataset, ekspor, dan sesi verifikasi.

## 13. Rancangan teknis frontend ReactJS

### 13.1 Pilihan arsitektur

Usulan: **ReactJS + TypeScript + Vite**, React Router untuk rute, dan TanStack Query untuk state server. Bentuk SPA cocok untuk workspace operator ini yang tidak memerlukan halaman publik dengan SEO. Routing, data fetching, dan pengelolaan error harus disiapkan eksplisit; panduan React menjelaskan pilihan build tool serta tanggung jawab tambahan aplikasi SPA. [React](https://react.dev/learn/build-a-react-app-from-scratch)

TanStack Query digunakan untuk mengambil, menyimpan cache, dan menyinkronkan snapshot server. State formulir/draft tetap dipisahkan dari state pekerjaan yang dimiliki server. Versi dependensi dipilih dan dikunci saat implementasi, bukan menyalin nomor versi yang belum diuji ke PRD. [TanStack Query](https://tanstack.com/query/latest/docs/framework/react/overview)

Struktur direktori usulan, **belum dibuat sebagai aplikasi**:

```text
frontend/crawler/src/
  app/                 # router, session, project context, providers
  features/
    automatic/         # wizard konfigurasi
    manual-url/        # input dan review URL
    survey/            # form, mapping dan review impor
    jobs/              # monitor, history, events dan stop
    datasets/          # preview, quality, files dan handoff
  shared/
    api/               # typed client, error mapping, event reconciliation
    components/        # field, stepper, status, chart, table, dialog
    schemas/           # validasi UI yang selaras kontrak backend
```

Komponen bersama: `CrawlerShell`, `SourceSelector`, `ConfigWizard`, `UrlReviewTable`, `SurveyResponseForm`, `ImportMapping`, `ValidationSummary`, `JobMonitor`, `PlatformProgressCard`, `CaptchaNotice`, `CooldownTimer`, `DatasetPreview`, dan `QualitySummary`. Sumber data masuk melalui typed API client; komponen presentasi tidak menjalankan crawling atau menghitung status terminal sendiri.

### 13.2 Sinkronisasi dan penyimpanan

Query key memuat proyek dan ID/version agar cache tidak tercampur. Hapus cache sensitif saat logout/pergantian proyek. Polling fallback saat layar aktif diusulkan setiap 5 detik dengan backoff saat gagal; saat stream tersambung, polling agresif dihentikan. Perbarui kartu tanpa memuat ulang seluruh halaman dan rekonsiliasi versi event agar angka tidak mundur karena event lama.

Konfigurasi nonrahasia dapat disimpan sebagai draf; jawaban survei, token, cookies platform, dan sesi browser tidak disimpan dalam localStorage. Draf survei yang perlu disimpan harus disimpan server dengan akses dan retensi. Navigasi yang meninggalkan input belum tersimpan meminta konfirmasi. Navigasi meninggalkan monitor tidak meminta konfirmasi menghentikan worker.

Pekerjaan tiga jam harus tetap berjalan di worker ketika tab ditutup. Meng-host SPA saja, termasuk di hosting statis, tidak menyediakan worker/API/browser yang dibutuhkan. Streamlit Dashboard yang sudah ada tetap memiliki jalur deployment sendiri sampai ada keputusan migrasi khusus.

## 14. Kualitas pengalaman dan kebutuhan nonfungsional

| Area | Kriteria yang dituju |
| --- | --- |
| Bahasa | Bahasa Indonesia, WIB untuk tampilan, label istilah konsisten; timestamp API menyertakan offset/UTC. |
| Responsif | Layar utama operator nyaman pada desktop; pada lebar 360, 768, dan 1280 piksel tidak kehilangan tombol/status. Tabel boleh mempunyai area scroll sendiri dengan identitas baris tetap terbaca. |
| Aksesibilitas | Target WCAG 2.2 AA untuk implementasi. Semua kontrol berlabel, navigasi keyboard dan fokus terlihat, error terhubung ke field, status tidak hanya dibedakan warna. Update progres tidak merebut fokus; live announcement dibatasi pada perubahan penting. |
| Form panjang | Langkah dan ringkasan jelas, field dikelompokkan, error summary bisa memindahkan fokus. Panduan label, grup, validasi, dan notifikasi mengikuti [W3C WAI Forms](https://www.w3.org/WAI/tutorials/forms/). |
| Respons interaksi | Target respons visual lokal ≤200 ms; tidak menunggu crawling untuk memberi feedback submit. |
| Pembaruan progres | Saat server/koneksi sehat, target perubahan status terlihat ≤10 detik sejak event server. Waktu platform merespons bukan SLA UI. |
| Tabel/import | Preview paginasi 50 baris; parsing besar/validasi akhir di server. Target layar inti dapat digunakan ≤3 detik pada profil uji yang disepakati saat implementasi; ukur dan laporkan profilnya. |
| Ketahanan | Offline/stale, loading, kosong, forbidden, konflik, dan gagal ekspor memiliki state yang dapat dipahami. Retry UI tidak menggandakan side effect. |
| Keamanan tampilan | Teks sosial/survei sebagai teks aman, link eksternal terverifikasi, tanpa HTML aktif. Kredensial platform berada di worker dan tidak dikirim ke browser operator. |
| Privasi | Minimalkan identitas responden; tidak memuat jawaban/nama/token dalam URL, telemetry, pesan error publik, atau log browser. Ekspor sesuai izin. |
| Observabilitas | Audit mulai/stop/commit/handoff/unduh dan correlation ID; metrik operasional tanpa isi jawaban. |

Retensi data, penghapusan, ekspor terbatas, serta kebijakan izin pemanfaatan perlu dirinci bersama backend/pemilik data sebelum survei nyata diaktifkan. UI menampilkan kebijakan efektif, bukan mengklaim kepatuhan yang belum dievaluasi.


### 14.1 Tema putih oranye dan tipografi wajib

Ketentuan visual ini menggantikan rancangan hijau sebelumnya sesuai revisi pengguna.

| Token | Nilai | Pemakaian |
| --- | --- | --- |
| `surface` | `#FFFFFF` | Panel, sidebar, form, header. |
| `canvas` | `#FAFAFA` | Latar workspace netral terang. |
| `accent` | `#FF8A24` | Tombol utama, langkah aktif, aksen akuisisi. |
| `accent_hover` | `#FF7608` | Hover tombol utama. |
| `accent_soft` | `#FFF3E8` | Pilihan sumber, ringkasan, area bantuan. |
| `border` | `#E6DDD5` | Pemisah dan batas kontrol. |
| `text` | `#000000` | Seluruh teks, label, helper, placeholder, tabel, badge, dan tombol. |

**Ukuran teks minimum 13 px tanpa pengecualian**, termasuk sidebar, footer, legenda/tabel grafik, badge, input, pesan error, dan tampilan mobile. Body/input memakai 15 px, label/tombol 14 px, teks pendukung 13 px, judul utama 28–36 px. Label grafik dirender sebagai HTML atau cara lain yang mempertahankan ukuran aktual minimal 13 px saat grafik menyusut.

Semua teks berwarna hitam. Tombol oranye memakai teks hitam; kontrol disabled tetap terbaca dengan latar/border berbeda. Tidak memakai hijau untuk tema, logo, status, grafik, atau dekorasi. Status dijelaskan melalui teks, ikon, dan batas/latar; grafik membedakan sumber menggunakan oranye, hitam/abu netral, dan pola garis, disertai legenda teks hitam.

Verifikasi tampilan melalui computed style dan screenshot desktop/mobile. Tidak cukup memeriksa token root jika aturan komponen atau media query masih mengecilkan teks di bawah 13 px.

## 15. Ukuran keberhasilan dan penerimaan

Ukuran produk: tingkat operator menyelesaikan validasi rencana, waktu menyiapkan pekerjaan, tingkat keberhasilan commit respons valid, kegagalan yang dapat diperbaiki, serta aksesibilitas alur inti. Ukuran kualitas data: post qualified terhadap target, jumlah unik menurut jenis, rasio duplikasi, penolakan menurut alasan, dan kelengkapan provenance. Nilai target produk ditetapkan setelah uji pengguna awal; jangan mengartikan angka target akuisisi sebagai SLA pengumpulan.

Rilis MVP diterima bila semua kebutuhan P0 memiliki skenario lulus pada [Acceptance Criteria Crawler](<Acceptance Criteria Crawler.md>), kontrak API tersedia, worker/browser Reddit dapat diuji, serta tidak ada kehilangan metadata survei pada dataset/handoff. Uji frontend menggunakan fixture untuk state hambatan dan satu integrasi worker terkendali; tidak wajib mengakuisisi 1.000 post dari platform nyata untuk setiap pengujian UI.

## 16. Tahapan dan keputusan lanjutan

1. Tinjau PRD dan rancangan layar, terutama definisi post qualified serta template survei.
2. Susun PRD Backend dan kontrak skema/API, termasuk mode URL saja, worker persisten, dan sesi CAPTCHA jarak jauh.
3. Implementasikan shell React, wizard otomatis, monitor, dan riwayat memakai API/fixture yang disepakati.
4. Implementasikan URL manual dan survei, lalu validasi deduplikasi serta ekspor/handoff sesuai versi skema.
5. Jalankan acceptance criteria dan uji operator; lanjutkan PRD frontend NLP Machine Learning serta Dashboard.

Asumsi kerja yang dapat ditinjau tanpa menghambat PRD: pengguna adalah operator internal; tujuh pilihan sumber di frontend; adapter Python yang sudah ada masih YouTube/Reddit; survei telah dikumpulkan manusia; input survei mendukung form dan file; serta frontend tidak memerlukan SEO. Keputusan sebelum implementasi: template survei pertama, penyedia autentikasi, batas konkurensi/antrean worker, retensi staging, mekanisme sesi browser remote, dan kontrak survei yang didukung NLP.
