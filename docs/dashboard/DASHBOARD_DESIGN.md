# Dashboard BeeSense

[SocialNLPStreamlitApp](../../Dashboard/app.py) membaca snapshot aktif dari [social_nlp.json](../../config/social_nlp.json). Dashboard tidak melakukan crawling atau training. Jumlah topik, coherence, volume, tanggal, dan bukti selalu dibaca dari artifact terverifikasi, bukan angka yang ditulis di UI.

Instagram kini didukung pada filter, reset, judul, hitungan, ranking, cakupan/noise,
grafik bulanan, porsi topik, tabel dan kutipan sumber. Warna Instagram #A93A82, berbeda
dari YouTube #C64D36 dan Reddit #3568B3. Pada data tiga platform, warna node menandai
platform dengan kalimat terbanyak dan hover menampilkan ketiga jumlah. Snapshot lama
dua platform tetap memakai skala proporsi terdahulu. Snapshot baru lolos 20 topik/c_v 0,4315 dan memuat 20 narasi Gemini; angka 29 Oktober di bawah adalah riwayat.

## Alur eksplorasi

1. **Ringkasan:** komentar dan kalimat pada filter, 12 topik terbesar per platform, cakupan/noise, serta distribusi menurut bulan post induk. Pilihan topik mempunyai tombol **Jelaskan topik ini**.
2. **Peta topik:** posisi model penuh tetap di bawah filter. Ukuran menunjukkan kemunculan kalimat; warna menunjukkan campuran YouTube/Reddit. Garis adalah kemiripan semantik. Dropdown memberikan alternatif keyboard untuk pemilihan node.
3. **Penjelasan topik:** fokus pada topik terpilih terlebih dahulu. Empat card merangkum komentar unik, porsi komentar, post asal, dan coherence topik dengan rata-rata model sebagai pembanding. Grafik menunjukkan istilah, platform, lima post penyumbang, serta porsi bulanan. Kutipan asli dan tautan sumber membantu memeriksa penjelasan. Perbandingan seluruh topik berada dalam panel terlipat.
4. **Kalimat & sumber:** tabel maksimal 1.000 baris, detail tanggal/judul/URL, unduhan seluruh hasil filter, serta graf maksimal 100 kalimat representatif.
5. **Metode & data:** protokol coherence, skor per topik, evaluasi kandidat, konfigurasi, checksum, bagian terlewat, dan keterbatasan. Catatan pembentukan topik juga tersedia di bagian bawah halaman.

## Arti angka

Kemunculan, kalimat unik, komentar, dan post asal adalah unit berbeda. Komentar memakai platform + source_row Excel; satu komentar dapat menyumbang beberapa kalimat dan topik. Porsi topik memakai komentar bertopik dibagi seluruh komentar terwakili pada filter, termasuk noise, sehingga porsi antar topik tidak harus berjumlah 100%.

Grafik istilah menghitung kalimat unik terfilter yang memuat istilah c-TF-IDF model penuh dengan batas kata/frasa. Ini frekuensi kehadiran, bukan bobot c-TF-IDF atau probabilitas. Grafik sumber menghitung komentar unik per video/thread; ID induk menjaga dua post dengan judul sama tetap terpisah. Jika identitas induk memakai hash konteks, UI memberi catatan. Sumber dominan >60% juga mendapat catatan.

Coherence c_v model penuh dan coherence topik terpilih ditampilkan terpisah. Target rata-rata ≥0,4 tidak menjamin setiap topik mencapai 0,4. Filter mengubah jumlah serta bukti; keanggotaan dan skor model tidak dihitung ulang. Skema artifact lama tetap terbaca. Coherence adalah keselarasan leksikal pada korpus, bukan akurasi, validasi manusia, atau ukuran keterwakilan platform.

Distribusi default memakai tanggal post/video asal, bukan riwayat penulisan komentar. Tanggal perkiraan diberi tanda. Grafik porsi meninggalkan celah pada bulan parsial, tanpa pengamatan, atau dengan dukungan kecil. Narasi arah mengikuti dukungan dan pemeriksaan campuran platform dalam [EXPLAINABLE_TOPICS.md](../machine-learning/EXPLAINABLE_TOPICS.md).

## Interaksi dan aksesibilitas

Kontrol native Streamlit memakai binding query-params untuk platform, tanggal, pencarian literal, topik, tampilan, dan slider. Memilih grafik/tabel atau membuka penjelasan mempertahankan filter. Reset mengembalikan lingkup data. Nilai slider dibatasi sebelum dibuat saat hasil mengecil; kasus satu/nol topik aman. Kondisi kosong menyertakan tindakan pemulihan.

Palet putih, latar #F4F7FB, tinta #172D43, teks sekunder #52657B, aksen #116D78; warna platform tetap konsisten. Avenir Next memakai fallback sistem tanpa unduhan font. Angka menggunakan locale Indonesia melalui Babel dan tabular numerals. Fokus keyboard terlihat, reduced motion dihormati, judul/teks panjang membungkus, dan card menjadi dua kolom pada layar sempit. Grafik memiliki deskripsi dan tabel alternatif. Kutipan HTML di-escape; link sumber hanya HTTP(S).

Review memakai [Web Interface Guidelines](https://raw.githubusercontent.com/vercel-labs/web-interface-guidelines/main/command.md). Pemeriksaan mencakup label, struktur heading, skip link bawaan Streamlit, fokus, URL state, kondisi kosong, bounded tables, reduced motion, dan overflow. Pengujian ini bukan sertifikasi aksesibilitas penuh terhadap seluruh komponen pihak ketiga.

## Verifikasi dan runtime

Tes unit memeriksa identitas komentar/post, istilah berbatas kata, judul sumber identik, noise, filter, posisi stabil, dan pemisahan data/model. Streamlit AppTest mencakup seluruh tampilan, navigasi ke penjelasan dengan topik/filter tetap, URL/reset, serta guard tanpa training. Pemeriksaan browser desktop dan layar sempit memastikan card/grafik/bukti tampil dan tidak terjadi overflow horizontal.

Image `deployment/docker/Dockerfile.dashboard` telah dibangun dan container lokal `beesense-dashboard` diganti pada `http://127.0.0.1:8501`. Runtime non-root UID 10001 membaca snapshot melalui bind mount read-only, healthcheck aktif, dan hanya port loopback yang diterbitkan. Runtime akhir telah diverifikasi memakai run gabungan `outputs/nlp_20261029_combined_topics20_01`: 20 topik dan rata-rata c_v 0,4720. Grafik/card/bukti mengikuti filter pada snapshot tersebut. Tidak ada migrasi database.

## Kalimat topik Gemini

Bundle model baru dapat membawa topic_narratives.csv dengan 20 kalimat topik/deskripsi. UI menampilkan tabel seluruh topik dan unduhan CSV, lalu kalimat/deskripsi pada konteks topik terpilih serta 10 keyword dan bobot pada detail penjelasan. Provenance menyatakan sintesis Gemini dari keyword model penuh; filter tidak meregenerasi label. Streamlit hanya membaca CSV terverifikasi dan tidak membutuhkan key atau memanggil Gemini. Snapshot lama tanpa CSV tetap kompatibel. Lihat [panduan Gemini](../machine-learning/GEMINI_TOPIC_NARRATIVES.md).

## Model 30 Oktober terverifikasi

Input `outputs/social_20261030_combined_3days_02/social_data.xlsx` memuat **33.034 record unik**, **1.859 root**, dan **31.175 komentar/balasan** dari hasil akuisisi 27–30 Oktober. Sebanyak 49.952 pengulangan antarberkas disisihkan; pemeriksaan menemukan 0 ID native ganda. Total Instagram 324 post/3.038 komentar mencakup batch terbaru 248 post/2.128 komentar dan trial sebelumnya 76 post/910 komentar. Pengguna menghentikan crawling setelah HTTP 429; target 1.000 post dan durasi 3 jam belum tercapai.

Run aktif `outputs/nlp_20261030_instagram_topics20_02` menghasilkan **20 topik**, rata-rata **c_v 0,4315219014**, coverage **94,67%**, silhouette cosine **-0,057864**, dan ARI dua seed **0,820417**. DBSCAN eps=0,25/min_samples=10 menghasilkan 165 kelompok primer, lalu Ward berbobot menggabungkannya menjadi 20 topik. Noise terdiri atas 2.751 kalimat unik. Persiapan menghasilkan 52.451 kemunculan/51.612 kalimat unik, 839 pengulangan dan 5.516 segmen dilewati; 28.758 komentar/balasan terwakili. Fitting inti berlangsung 1.195,5 detik sebelum tahap Gemini.

Gemini `gemini-3.5-flash-lite` menghasilkan **20 kalimat topik dan deskripsi bahasa Indonesia**, masing-masing dari 10 keyword c-TF-IDF berbobot tertinggi dan 10 kalimat terdekat dengan pusat topik. `topic_narratives.csv` beserta provenance/checksum masuk bundle model. UI membaca CSV tanpa API atau training saat rerun. Sebanyak 8 dari 20 topik masih memiliki c_v individual <0,4; ambang berlaku pada rata-rata. Evaluasi ini in-sample, bukan akurasi berlabel atau holdout. Skor dari korpus berbeda tidak menjadi perbandingan kualitas langsung.

Publikasi memakai GitHub main, entry `streamlit_apps.py`, target `https://beesense.streamlit.app`. Pemeriksaan lokal mendahului push; API key tidak diperlukan pada Cloud. No migration required. Docker daemon tidak tersedia sehingga build/startup image belum diverifikasi.
