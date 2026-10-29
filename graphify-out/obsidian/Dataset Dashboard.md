---
type: dataset
tags: [beesense, provenance, sbert, dbscan, merged]
---

# Dataset Dashboard

Input `outputs/social_20261029_combined/social_data.xlsx` menggabungkan baseline 8.449 baris dan akuisisi baru 20.650 baris: **29.099 baris**, **1.517 post asal**, dan **27.582 komentar/balasan**. Persiapan menghasilkan 46.916 kemunculan, 46.143 kalimat unik, 773 pengulangan dan 4.741 potongan dilewati; 25.739 komentar/balasan terwakili.

Run aktif: `outputs/nlp_20261029_combined_topics20_01`, dengan `target_topics: 20`. Empat Parquet dan manifest disimpan pada direktori versi baru; dua workbook baseline dan seluruh snapshot NLP sebelumnya dipertahankan. Tidak ada ID native ganda dalam workbook gabungan.

Hasil aktif: **20 topik**, c_v rata-rata **0,4720034334**, coverage kalimat unik **87,14%**, silhouette cosine **-0,000279**, ARI dua seed UMAP **0,764229**. DBSCAN eps=0.2, min_samples=10 menghasilkan 245 kelompok primer yang digabung menjadi 20 melalui Ward berbobot. Noise: 5.933 kalimat unik dan 6.029 kemunculan. Percobaan fitting terpublikasi 114,6 detik. Embedding SBERT dihitung baru untuk korpus gabungan, lalu dipakai dari cache terverifikasi pada percobaan radius yang sesuai batas memori; kedua UMAP juga memakai cache korpus yang sama.

[Workbook gabungan](../../outputs/social_20261029_combined/social_data.xlsx) menggabungkan baseline dan [akuisisi hari ini](../../outputs/social_20261029_1000_3h/summary.json). SHA-256: `7711aae01ca6b700b9842bddcd8c9c597e054947d4c5c1680cc9f61f9723aff9`. Baseline 8.449 baris dan audit delapan sheet tidak diubah; audit tetap ber-checksum `ccfc77dc136ed8e98bce5c2c11d6243d22ff9e2a3082d9e299847b8b5aec74b3`.

[Run aktif](../../outputs/nlp_20261029_combined_topics20_01/summary.json) memakai skema v2, sebelas artifact + manifest. Empat Parquet memisahkan source_data, kalimat unik, seluruh kemunculan, serta segmen dilewati. ID asal DBSCAN/core point dan mapping penggabungan dipertahankan. Penjelasan/filter memakai artifact tanpa melatih ulang.

Run gabungan menghasilkan rata-rata c_v **0,4720034334**, memenuhi target **≥0,4**. **7 dari 20 topik masih <0,4 secara individual**; ambang ini berlaku pada rata-rata. Silhouette cosine SBERT asli -0,000279 tetap perlu dibaca bersama coverage dan keragaman sumber.

Hasil historis pada workbook baseline yang sama adalah 52 topik/c_v 0,4097033012 dan 20 topik/c_v 0,4143250939. Run gabungan memakai korpus dan hash referensi berbeda, sehingga selisih terhadap dua angka tersebut bukan perbandingan kualitas langsung. Coherence baseline dalam metadata run baru tidak diisi karena inputnya berbeda. Evaluasi tetap in-sample, bukan akurasi atau holdout berlabel manusia.


Pemeriksaan source/checksum mencakup workbook aktif, baseline asli, dan semua snapshot NLP arsip. Akuisisi baru 1.286 root tidak bertumpang tindih dengan baseline; target qualified 1.000/platform belum tercapai. Tanggal komentar YouTube dapat berupa perkiraan. Snapshot parsial, bukan populasi platform.

[[Crawling 1000 Post Baru]] · [[Metodologi Machine Learning Social NLP]] · [[Arsitektur BeeSense]] · [[HOME]]
