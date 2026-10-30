# Pipeline Instagram, dataset tiga hari dan Streamlit

## Snapshot terbaru

Konfigurasi aktif kini memakai `outputs/nlp_20261030_instagram_500_topics20_01` dari `outputs/social_20261030_combined_instagram_500_2h_02/social_data.xlsx`: 20 topik, rata-rata c_v 0,4386500025. Excel snapshot lengkap berisi 45.556 pasangan topik–kalimat asli unik; label run ini c-TF-IDF lokal. Lihat [README](../../README.md) dan metode Social NLP untuk data serta batas interpretasi. Catatan hasil/narasi Gemini berikut merupakan riwayat snapshot sebelumnya.


Instruksi pengguna 30 Oktober 2026: gabungkan InstagramCrawler ke SocialCrawler,
ambil **hanya Instagram** selama maksimum **3 jam** dengan target **1.000 post**,
gabungkan hasil crawling 27–30 Oktober menjadi dataset versi baru tanpa ID ganda,
latih/uji model **20 topik** dengan **rata-rata coherence c_v ≥0,4**, lalu rebuild
dan deploy Streamlit melalui **commit dan push GitHub**. Definisi jendela berdasarkan
tanggal hasil akuisisi telah dikonfirmasi pengguna; post lama di dalamnya tetap ada.

## Akuisisi

`config/social_crawler_instagram_3h.json` memakai satu platform Instagram dan backend
Chrome/login manual. Worker browser serial, satu profil persisten di output/ yang
diabaikan Git, CLI dipatok 0.1.22. Tidak ada login password pada setiap request.
CAPTCHA/login/429 menghentikan run dengan bukti parsial, tanpa solver. Konfigurasi
menyimpan batas operasi 90 detik, 10.800 detik global, target 1.000 root dengan minimum
10 komentar unik, pacing dan batas scroll. Root yang lolos tetapi kurang komentar
tetap diekspor, dihitung terpisah dari root yang memenuhi target.

Run awal 13.28 WIB: `outputs/social_instagram_20261030_1000_3h_01`; deadline sekitar
16.28 WIB. Status akhir masih menunggu. Run lama 12 menit berisi 76 post/910 komentar
dipertahankan; root-nya menjadi baseline pengecualian run baru. Tidak ada crawl baru
YouTube atau Reddit. Lima tes integrasi baru dan suite crawler memeriksa kontrak.

## Dataset baru

`scripts.merge_social_datasets.py --duplicate-policy prefer_latest` menerima workbook
compact yang asli. Identitas memakai platform + namespace post/comment + ID native;
Instagram shortcode dipetakan ke media PK, comment/reply memakai ID komentar.
Permalink p/reel dan bentuk query/path komentar merujuk identitas yang sama.

Sumber diurutkan menurut tanggal akuisisi dan urutan observasi. Pengulangan ID ditulis
sekali memakai observasi terakhir; teks identik pada ID berbeda tetap dua record.
Perubahan comment/reply dipertahankan dari pengamatan terbaru dan diaudit. Konflik
induk/native ID, komentar tanpa root, formula Excel atau komentar terpotong ditolak.
Workbook sumber tidak diubah dan hash-nya diperiksa sebelum/sesudah penggabungan.

Direktori tujuan `outputs/social_20261030_combined_3days/` berisi workbook, laporan
penggabungan, `record_lineage.jsonl` dan `duplicate_records.jsonl`, semuanya dengan
checksum. Pemeriksaan baca ulang membuktikan satu record per ID. Uji awal pada sumber
yang selesai sebelum run tiga jam: 30.658 record unik, 1.611 root, 29.047 komentar/
balasan; 49.952 pengulangan lintas berkas dihapus. Ini **bukan hasil akhir**.

## Model dan dashboard

`MachineLearning/social_nlp.py` mendefinisikan default 20 topik dan c_v minimum 0,4;
`config/social_nlp_instagram_20261030.json` menetapkan input/output versi baru.
Pipeline tetap SBERT multilingual → dua proyeksi UMAP → pencarian DBSCAN → penggabungan
Ward berbobot menjadi 20 topik. Coherence mengukur seluruh topik terhadap referensi
korpus yang tetap; rata-rata 0,4 tidak menjamin tiap topik 0,4 dan bukan akurasi berlabel.
Coverage, dominasi, silhouette dan stabilitas ARI dua seed tetap diperiksa.

Instagram disertakan pada identitas root, hitungan, porsi/campuran platform, tren,
bukti dan peringatan dominasi. UI memakai tiga label/warna platform, filter/reset,
ranking, coverage/noise, tabel topik, grafik waktu dan sumber Instagram. Snapshot lama
dua platform tetap terbaca; dashboard membaca artifact dan tidak melatih saat rerun.

Konfigurasi aktif `config/social_nlp.json` baru dialihkan setelah manifest, sumber,
20 topik, coherence dan provenance Instagram lolos. Sampai itu terjadi dashboard
tetap memakai snapshot lama yang valid.

## Publikasi

Deployment berarti push ke `github.com/SakaHeroji/BeeSense`, branch main, entry
`streamlit_apps.py`, aplikasi `beesense.streamlit.app`. Versi source/workbook/Parquet/
array/manifest yang lengkap harus ikut GitHub. Input dan snapshot lama dipertahankan.
`scripts.verify_dashboard_data --check-git` memeriksa allowlist, checksum, gate model,
ID record unik dan audit penggabungan; auth.json/profil/session tidak boleh masuk Git.

Docker daemon lokal belum tersedia pada pemeriksaan terakhir. Image dan clean context
diinspeksi, tetapi build/startup image baru belum dibuktikan. Deployment Community
Cloud memakai requirements dashboard terpisah. **No migration required**: kontrak
tabular lama dipertahankan; tidak ada perubahan struktur database.

## Penambahan Gemini

Setelah gate 20 topik/c_v ≥0,4, konfigurasi run baru mengaktifkan Gemini. Setiap topik mengirim 10 keyword c-TF-IDF tertinggi beserta bobot untuk menghasilkan satu kalimat dan deskripsi bahasa Indonesia. CSV 20 baris wajib lengkap dan tercakup manifest sebelum konfigurasi aktif dialihkan/push GitHub. UI membaca CSV tanpa API saat rerun. Uji satu topik historis berhasil; hasil model baru menunggu akuisisi dan training. Lihat [panduan Gemini](../machine-learning/GEMINI_TOPIC_NARRATIVES.md).

## Pemulihan HTTP 429 dan Chrome (30 Oktober)

Run pertama berhenti PARTIAL/CONSECUTIVE_SOURCE_ERRORS setelah 2.940 detik: 248 post,
2.128 komentar, 130 root dengan ≥10 komentar. Batas tiga jam dan target 1.000 belum
tercapai. Percobaan pemulihan kedua 25 detik menghasilkan0 record. Pengguna kemudian
mengonfirmasi HTTP 429 pada Chrome; error CLI sebelumnya hanya merekam kegagalan
navigasi, sehingga tidak boleh diklaim sebagai status429 terukur oleh crawler lama.

SocialCrawler 1.5.1 kini menetapkan jeda Instagram360 detik dan maksimum3 retry,
seperti preset Reddit. Waktu tunggu memakai nilai terbesar antara konfigurasi dan
Retry-After. Retry mempertahankan operasi/URL yang sama dan tidak melampaui deadline
global awal16.28WIB. Konfigurasi resume mengecualikan seluruh post tersimpan dan
memakai sisa anggaran; preset utama tetap10.800 detik/target 1.000. Tidak ada crawling
YouTube/Reddit baru, solver, rotasi identitas atau password login ulang.

Browser mengamati status429 dari respons Instagram, termasuk respons main-document
CDP ketika Chrome melempar ERR_HTTP_RESPONSE_CODE_FAILURE sebelum mengembalikan
Response. Hanya status dan Retry-After dipilih; cookie/header otentikasi tidak dicatat.
Respons429 GraphQL yang diminta halaman Instagram juga menghentikan operasi sebelum
scroll berikutnya. Error navigasi umum tetap SOURCE_ERROR, bukan diasumsikan429.

Pada429, challenge, timeout atau errorCLI, Chrome dibiarkan terbuka untuk pemeriksaan.
Penutupan sebelumnya berasal dari finally crawler, bukan pembersihan macOS. Tujuh
belas tes terfokus memeriksa parsing/status/header, kode browser hasil generator,
privasi header, batasretry, Retry-After lebih lama, deadline dan pencegahan duplikasi.
Run03 dijadwalkan setelah cooldown awal berakhir14.47WIB. Hasil final masih menunggu;
training sementara ditunda, lalu pipeline akan menggabungkan ke direktori versi02.

## Akuisisi dihentikan atas instruksi pengguna

Pengguna menghentikan crawling setelah429 dan meminta proses dataset/training/deploy dilanjutkan. Run03 berstatus INTERRUPTED,0 record baru,1rate-limit event terverifikasi, tanpa retry yang dijalankan. Tidak ada crawl lagi setelah instruksi berhenti. Run01 menyumbang248 post/2.128 komentar; target 1.000 dan durasi3 jam tidak tercapai. Dataset gabungan final `outputs/social_20261030_combined_3days_02/social_data.xlsx` lolos33.034 record unik,1.859 root dan31.175 komentar/balasan,49.952 pengulangan disisihkan,0ID native ganda. TotalInstagram 324 post/3.038 komentar mencakup hasil76 post/910 komentar sebelumnya. Training model baru tetap menunggu hasil qualitygate; tidak ada klaimcoherence 20 narasi/deployment selesai.

## Model 30 Oktober terverifikasi

Input `outputs/social_20261030_combined_3days_02/social_data.xlsx` memuat **33.034 record unik**, **1.859 root**, dan **31.175 komentar/balasan** dari hasil akuisisi 27–30 Oktober. Sebanyak 49.952 pengulangan antarberkas disisihkan; pemeriksaan menemukan 0 ID native ganda. Total Instagram 324 post/3.038 komentar mencakup batch terbaru 248 post/2.128 komentar dan trial sebelumnya 76 post/910 komentar. Pengguna menghentikan crawling setelah HTTP 429; target 1.000 post dan durasi 3 jam belum tercapai.

Run sesi sebelumnya `outputs/nlp_20261030_instagram_topics20_02` menghasilkan **20 topik**, rata-rata **c_v 0,4315219014**, coverage **94,67%**, silhouette cosine **-0,057864**, dan ARI dua seed **0,820417**. DBSCAN eps=0,25/min_samples=10 menghasilkan 165 kelompok primer, lalu Ward berbobot menggabungkannya menjadi 20 topik. Noise terdiri atas 2.751 kalimat unik. Persiapan menghasilkan 52.451 kemunculan/51.612 kalimat unik, 839 pengulangan dan 5.516 segmen dilewati; 28.758 komentar/balasan terwakili. Fitting inti berlangsung 1.195,5 detik sebelum tahap Gemini.

Gemini `gemini-3.5-flash-lite` menghasilkan **20 kalimat topik dan deskripsi bahasa Indonesia**, masing-masing dari 10 keyword c-TF-IDF berbobot tertinggi dan 10 kalimat terdekat dengan pusat topik. `topic_narratives.csv` beserta provenance/checksum masuk bundle model. UI membaca CSV tanpa API atau training saat rerun. Sebanyak 8 dari 20 topik masih memiliki c_v individual <0,4; ambang berlaku pada rata-rata. Evaluasi ini in-sample, bukan akurasi berlabel atau holdout. Skor dari korpus berbeda tidak menjadi perbandingan kualitas langsung.

Publikasi memakai GitHub main, entry `streamlit_apps.py`, target `https://beesense.streamlit.app`. Pemeriksaan lokal mendahului push; API key tidak diperlukan pada Cloud. No migration required. Docker daemon tidak tersedia sehingga build/startup image belum diverifikasi.

## Pembaruan pacing setelah deployment 30 Oktober

Dashboard pada commit `194e0b1` sudah terverifikasi live di
https://beesense.streamlit.app: 20 topik, c_v 0,4315219014, dan CSV unduhan
identik dengan berkas lokal. Narasi Gemini memakai 10 keyword dan 10 kalimat
representatif per topik. Perbaikan crawler berikut dilakukan setelah verifikasi
tersebut; crawling tetap berhenti dan tidak ada uji jaringan Instagram baru.

`SocialCrawler` 1.5.2 menambahkan `instagram_pacing`. Preset
`config/social_crawler_instagram_3h.json` dan preset pemulihan kini memakai:

- Jeda antaroperasi acak 5–10 detik.
- Istirahat 120 detik setiap 20 operasi Instagram, hanya bila masih ada pekerjaan.
- Cooldown 429 bertahap 360, 720, 1.440, lalu maksimal 3.600 detik. Batas ini
  berlaku pada perhitungan lokal; `Retry-After` yang lebih lama tetap dihormati.
- Maksimum tiga retry dan batas waktu total tetap berlaku. Scheduler memberi
  kesempatan platform lain berjalan selama jeda Instagram pada mode round robin.
- Maksimal delapan scroll per halaman dengan jeda lima detik. Data yang belum
  terkumpul tetap ditandai parsial; target 1.000 post bukan jaminan throughput.

```json
"instagram_pacing": {
  "enabled": true,
  "batch_size": 20,
  "batch_pause_seconds": 120,
  "rate_limit_backoff_multiplier": 2,
  "max_cooldown_seconds": 3600
}
```

Konfigurasi lama yang tidak mengaktifkan blok ini mempertahankan cooldown tetap.
Hitungan `operations_completed` dan `batch_pauses` masuk ringkasan/progress.
Satu operasi browser dapat menghasilkan beberapa request HTTP; angka 20 di atas
merupakan batas batch lokal, bukan kuota resmi Instagram. Sesi Chrome persisten,
penghentian saat challenge/429, dan pengecualian ID post lama tetap dipakai.

Pola jeda acak, istirahat batch dan exponential backoff diadaptasi dari
[referensi DataDwip yang diberikan pengguna](https://www.datadwip.com/blog/how-to-scrape-instagram/).
Klaim kuota dalam artikel bukan jaminan platform. Makna HTTP 429 dan petunjuk
waktu tunggu mengacu pada [RFC 6585 bagian 4](https://www.rfc-editor.org/rfc/rfc6585#section-4)
dan [Retry-After pada RFC 9110](https://www.rfc-editor.org/rfc/rfc9110#section-10.2.3).
Pengaturan ini mengurangi laju akses; tidak menjamin HTTP 429 hilang. Uji jam
simulasi mencakup pertumbuhan/cap backoff, waktu tunggu server yang lebih lama,
jeda batch, dan penghentian pada deadline, tanpa membuka Instagram.
