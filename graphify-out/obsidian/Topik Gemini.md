---
type: architecture
tags: [beesense, nlp, gemini, dashboard]
---

# Topik Gemini

[[Arsitektur BeeSense]] menambahkan tahap Gemini pada SocialNLPClusterer 2.4.
Setelah 20 topik dan rata-rata c_v ≥0,4 lolos, setiap topik mengirim 10 keyword
berbobot c-TF-IDF tertinggi dan sampai 10 kalimat representatif untuk satu kalimat
topik dan deskripsi bahasa Indonesia. Kalimat dipilih berdasarkan kedekatan
cosine dengan centroid pada cluster yang sama, dengan ID sebagai pemecah seri.
Gemini tidak mengubah cluster atau skor coherence. Contoh kalimat asli dikirim
sesuai permintaan pengguna; API key hanya dibaca dari auth.json lokal yang
diabaikan Git. Prompt versi 2 meminta narasi yang mengalir dan menghindari
daftar keyword, hubungan yang dipaksakan, serta pengulangan penjelasan.

`MachineLearning/topic_narratives.py` menangani request terstruktur, validasi,
retry terbatas dan receipt cache yang mengikat sumber/prompt/keyword/kalimat.
Extension CSV versi 2 memvalidasi contoh terhadap Parquet; versi 1 tetap dibaca
dengan prompt historisnya. CSV 20 baris
disimpan dalam bundle model, diperiksa checksum/provenance saat dibaca dashboard.
UI menyediakan tabel, unduhan CSV, kalimat/deskripsi topik terpilih dan bobot
keyword. Rerun Streamlit tidak memanggil API. Sintesis AI tetap model penuh saat
filter statistik berubah; kutipan sumber dipakai untuk meninjau bukti.

Uji API nyata satu topik historis berhasil; sembilan tes offline lulus. Hasil model baru sudah terverifikasi: 20 topik/c_v 0,4315 dan 20 narasi Gemini. Publikasi mengikuti pemeriksaan release.

[Panduan lengkap](../../docs/machine-learning/GEMINI_TOPIC_NARRATIVES.md) · [[HOME]]

## Model 30 Oktober terverifikasi

Input `outputs/social_20261030_combined_3days_02/social_data.xlsx` memuat **33.034 record unik**, **1.859 root**, dan **31.175 komentar/balasan** dari hasil akuisisi 27–30 Oktober. Sebanyak 49.952 pengulangan antarberkas disisihkan; pemeriksaan menemukan 0 ID native ganda. Total Instagram 324 post/3.038 komentar mencakup batch terbaru 248 post/2.128 komentar dan trial sebelumnya 76 post/910 komentar. Pengguna menghentikan crawling setelah HTTP 429; target 1.000 post dan durasi 3 jam belum tercapai.

Run aktif `outputs/nlp_20261030_instagram_topics20_02` menghasilkan **20 topik**, rata-rata **c_v 0,4315219014**, coverage **94,67%**, silhouette cosine **-0,057864**, dan ARI dua seed **0,820417**. DBSCAN eps=0,25/min_samples=10 menghasilkan 165 kelompok primer, lalu Ward berbobot menggabungkannya menjadi 20 topik. Noise terdiri atas 2.751 kalimat unik. Persiapan menghasilkan 52.451 kemunculan/51.612 kalimat unik, 839 pengulangan dan 5.516 segmen dilewati; 28.758 komentar/balasan terwakili. Fitting inti berlangsung 1.195,5 detik sebelum tahap Gemini.

Gemini `gemini-3.5-flash-lite` menghasilkan **20 kalimat topik dan deskripsi bahasa Indonesia**, masing-masing dari 10 keyword c-TF-IDF berbobot tertinggi dan 10 kalimat terdekat dengan pusat topik. `topic_narratives.csv` beserta provenance/checksum masuk bundle model. UI membaca CSV tanpa API atau training saat rerun. Sebanyak 8 dari 20 topik masih memiliki c_v individual <0,4; ambang berlaku pada rata-rata. Evaluasi ini in-sample, bukan akurasi berlabel atau holdout. Skor dari korpus berbeda tidak menjadi perbandingan kualitas langsung.

Publikasi memakai GitHub main, entry `streamlit_apps.py`, target `https://beesense.streamlit.app`. Pemeriksaan lokal mendahului push; API key tidak diperlukan pada Cloud. No migration required. Docker daemon tidak tersedia sehingga build/startup image belum diverifikasi.

## Verifikasi publikasi

Commit `194e0b1` telah di-push dan dashboard live terverifikasi pada 30 Oktober 2026.
Unduhan CSV dari beesense.streamlit.app identik byte per byte dengan berkas lokal:
20 narasi, 200 kalimat representatif, prompt `beesense-topic-id:2`. Coherence
model tetap 0,4315219014; hanya CSV, summary dan manifest narasi yang direvisi.
CI GitHub lulus untuk job utama serta runtime dashboard Python 3.12 dan 3.14.
