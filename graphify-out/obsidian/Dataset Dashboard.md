---
type: dataset
tags: [beesense, provenance, sbert, dbscan, merged]
---

# Dataset Dashboard

## Snapshot aktif setelah tambahan Instagram

Input `outputs/social_20261030_combined_instagram_500_2h_02/social_data.xlsx` memuat **34.095 record unik**, **2.160 post asal**, dan **31.935 komentar/balasan**. Input menggabungkan 33.034 record sebelumnya dengan 301 post Instagram, 622 komentar dan 138 balasan baru. Pemeriksaan memastikan 0 duplikasi ID, 0 overlap post baru dengan baseline, dan semua nilai sel baseline tetap utuh.

Run aktif `outputs/nlp_20261030_instagram_500_topics20_gemini_02` menghasilkan **20 topik**, rata-rata **c_v 0,4386500025**, coverage **87,59%**, silhouette cosine **-0,018778**, dan ARI dua seed **0,739133**. DBSCAN eps=0,2/min_samples=10 menghasilkan 279 kelompok primer, lalu Ward berbobot menggabungkannya menjadi 20 topik. Encoding SBERT dihitung baru pada 51.979 kalimat unik; bobot encoder pralatih tetap. Persiapan menghasilkan 52.861 kemunculan, 882 pengulangan dan 5.931 segmen dilewati; 29.132 komentar/balasan terwakili. Noise terdiri atas 6.449 kalimat unik/6.523 kemunculan.

Excel `topic_sentences.xlsx` memuat **45.556 pasangan topik–kalimat asli unik**. Sheet Kalimat berisi tepat kolom `topik` dan `kalimat yang berada dalam cluster topik`; sheet Topik mencantumkan c_v dan jumlah kalimat setiap topik. Pengulangan teks yang sama dalam satu cluster disatukan; variasi asli yang berbeda tetap dipertahankan. Kalimat noise tersedia dalam artifact model dan jumlahnya dicatat pada Excel. Dashboard menyediakan unduhan Excel snapshot lengkap pada Kalimat & sumber; unduhan JSONL tetap mengikuti filter.

Ambang ≥0,4 berlaku pada **rata-rata tanpa bobot semua 20 topik**; **9/20 topik** masih di bawah 0,4 secara individual. Referensi coherence mencakup seluruh kalimat unik, termasuk noise, dengan top-10 istilah/window 110. Ini evaluasi in-sample, bukan akurasi berlabel; skor antar-korpus tidak dibandingkan sebagai kenaikan kualitas. Label c-TF-IDF dan seluruh keanggotaan cluster dipertahankan. Sesuai instruksi pengguna, `SocialNLPClusterer.generate_topic_narratives()` membuat 20 kalimat topik dan deskripsi bahasa Indonesia melalui Gemini `gemini-3.5-flash-lite`, masing-masing dari 10 keyword berbobot dan 10 kalimat representatif. CSV beserta provenance/checksum dibaca dashboard tanpa panggilan API pada rerun. Array, Parquet, keyword, skor coherence, dan Excel identik dengan snapshot clustering sebelumnya; kedua snapshot tetap disimpan.

[[Training Instagram 20 Topik]]

## Riwayat sesi sebelumnya 30 Oktober 2026

Input `outputs/social_20261030_combined_3days_02/social_data.xlsx` memuat **33.034 record unik**, **1.859 root**, dan **31.175 komentar/balasan** dari hasil akuisisi 27–30 Oktober. Sebanyak 49.952 pengulangan antarberkas disisihkan; pemeriksaan menemukan 0 ID native ganda. Total Instagram 324 post/3.038 komentar mencakup batch terbaru 248 post/2.128 komentar dan trial sebelumnya 76 post/910 komentar. Pengguna menghentikan crawling setelah HTTP 429; target 1.000 post dan durasi 3 jam belum tercapai.

Run aktif `outputs/nlp_20261030_instagram_topics20_02` menghasilkan **20 topik**, rata-rata **c_v 0,4315219014**, coverage **94,67%**, silhouette cosine **-0,057864**, dan ARI dua seed **0,820417**. DBSCAN eps=0,25/min_samples=10 menghasilkan 165 kelompok primer, lalu Ward berbobot menggabungkannya menjadi 20 topik. Noise terdiri atas 2.751 kalimat unik. Persiapan menghasilkan 52.451 kemunculan/51.612 kalimat unik, 839 pengulangan dan 5.516 segmen dilewati; 28.758 komentar/balasan terwakili. Fitting inti berlangsung 1.195,5 detik sebelum tahap Gemini.

Gemini `gemini-3.5-flash-lite` menghasilkan **20 kalimat topik dan deskripsi bahasa Indonesia**, masing-masing dari 10 keyword c-TF-IDF berbobot tertinggi dan 10 kalimat terdekat dengan pusat topik. `topic_narratives.csv` beserta provenance/checksum masuk bundle model. UI membaca CSV tanpa API atau training saat rerun. Sebanyak 8 dari 20 topik masih memiliki c_v individual <0,4; ambang berlaku pada rata-rata. Evaluasi ini in-sample, bukan akurasi berlabel atau holdout. Skor dari korpus berbeda tidak menjadi perbandingan kualitas langsung.

## Riwayat29 Oktober 2026


Input `outputs/social_20261029_combined/social_data.xlsx` menggabungkan baseline 8.449 baris dan akuisisi baru 20.650 baris: **29.099 baris**, **1.517 post asal**, dan **27.582 komentar/balasan**. Persiapan menghasilkan 46.916 kemunculan, 46.143 kalimat unik, 773 pengulangan dan 4.741 potongan dilewati; 25.739 komentar/balasan terwakili.

Run aktif: `outputs/nlp_20261029_combined_topics20_01`, dengan `target_topics: 20`. Empat Parquet dan manifest disimpan pada direktori versi baru; dua workbook baseline dan seluruh snapshot NLP sebelumnya dipertahankan. Tidak ada ID native ganda dalam workbook gabungan.

Hasil aktif: **20 topik**, c_v rata-rata **0,4720034334**, coverage kalimat unik **87,14%**, silhouette cosine **-0,000279**, ARI dua seed UMAP **0,764229**. DBSCAN eps=0.2, min_samples=10 menghasilkan 245 kelompok primer yang digabung menjadi 20 melalui Ward berbobot. Noise: 5.933 kalimat unik dan 6.029 kemunculan. Percobaan fitting terpublikasi 114,6 detik. Embedding SBERT dihitung baru untuk korpus gabungan, lalu dipakai dari cache terverifikasi pada percobaan radius yang sesuai batas memori; kedua UMAP juga memakai cache korpus yang sama.

[Workbook gabungan](../../outputs/social_20261029_combined/social_data.xlsx) menggabungkan baseline dan [akuisisi hari ini](../../outputs/social_20261029_1000_3h/summary.json). SHA-256: `7711aae01ca6b700b9842bddcd8c9c597e054947d4c5c1680cc9f61f9723aff9`. Baseline 8.449 baris dan audit delapan sheet tidak diubah; audit tetap ber-checksum `ccfc77dc136ed8e98bce5c2c11d6243d22ff9e2a3082d9e299847b8b5aec74b3`.

[Run aktif](../../outputs/nlp_20261029_combined_topics20_01/summary.json) memakai skema v2, sebelas artifact + manifest. Empat Parquet memisahkan source_data, kalimat unik, seluruh kemunculan, serta segmen dilewati. ID asal DBSCAN/core point dan mapping penggabungan dipertahankan. Penjelasan/filter memakai artifact tanpa melatih ulang.

Run gabungan menghasilkan rata-rata c_v **0,4720034334**, memenuhi target **≥0,4**. **7 dari 20 topik masih <0,4 secara individual**; ambang ini berlaku pada rata-rata. Silhouette cosine SBERT asli -0,000279 tetap perlu dibaca bersama coverage dan keragaman sumber.

Hasil historis pada workbook baseline yang sama adalah 52 topik/c_v 0,4097033012 dan 20 topik/c_v 0,4143250939. Run gabungan memakai korpus dan hash referensi berbeda, sehingga selisih terhadap dua angka tersebut bukan perbandingan kualitas langsung. Coherence baseline dalam metadata run baru tidak diisi karena inputnya berbeda. Evaluasi tetap in-sample, bukan akurasi atau holdout berlabel manusia.


Pemeriksaan source/checksum mencakup workbook aktif, baseline asli, dan semua snapshot NLP arsip. Akuisisi baru 1.286 root tidak bertumpang tindih dengan baseline; target qualified 1.000/platform belum tercapai. Tanggal komentar YouTube dapat berupa perkiraan. Snapshot parsial, bukan populasi platform.

[[Crawling 1000 Post Baru]] · [[Metodologi Machine Learning Social NLP]] · [[Arsitektur BeeSense]] · [[HOME]]
