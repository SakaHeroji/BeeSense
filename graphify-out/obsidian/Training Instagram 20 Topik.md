---
type: training_run
tags: [beesense, sbert, clustering, excel]
---

# Training Instagram 20 Topik

Input `outputs/social_20261030_combined_instagram_500_2h_02/social_data.xlsx` memuat **34.095 record unik**, **2.160 post asal**, dan **31.935 komentar/balasan**. Input menggabungkan 33.034 record sebelumnya dengan 301 post Instagram, 622 komentar dan 138 balasan baru. Pemeriksaan memastikan 0 duplikasi ID, 0 overlap post baru dengan baseline, dan semua nilai sel baseline tetap utuh.

Run aktif `outputs/nlp_20261030_instagram_500_topics20_gemini_02` menghasilkan **20 topik**, rata-rata **c_v 0,4386500025**, coverage **87,59%**, silhouette cosine **-0,018778**, dan ARI dua seed **0,739133**. DBSCAN eps=0,2/min_samples=10 menghasilkan 279 kelompok primer, lalu Ward berbobot menggabungkannya menjadi 20 topik. Encoding SBERT dihitung baru pada 51.979 kalimat unik; bobot encoder pralatih tetap. Persiapan menghasilkan 52.861 kemunculan, 882 pengulangan dan 5.931 segmen dilewati; 29.132 komentar/balasan terwakili. Noise terdiri atas 6.449 kalimat unik/6.523 kemunculan.

Excel `topic_sentences.xlsx` memuat **45.556 pasangan topik–kalimat asli unik**. Sheet Kalimat berisi tepat kolom `topik` dan `kalimat yang berada dalam cluster topik`; sheet Topik mencantumkan c_v dan jumlah kalimat setiap topik. Pengulangan teks yang sama dalam satu cluster disatukan; variasi asli yang berbeda tetap dipertahankan. Kalimat noise tersedia dalam artifact model dan jumlahnya dicatat pada Excel. Dashboard menyediakan unduhan Excel snapshot lengkap pada Kalimat & sumber; unduhan JSONL tetap mengikuti filter.

Ambang ≥0,4 berlaku pada **rata-rata tanpa bobot semua 20 topik**; **9/20 topik** masih di bawah 0,4 secara individual. Referensi coherence mencakup seluruh kalimat unik, termasuk noise, dengan top-10 istilah/window 110. Ini evaluasi in-sample, bukan akurasi berlabel; skor antar-korpus tidak dibandingkan sebagai kenaikan kualitas. Label c-TF-IDF dan seluruh keanggotaan cluster dipertahankan. Sesuai instruksi pengguna, `SocialNLPClusterer.generate_topic_narratives()` membuat 20 kalimat topik dan deskripsi bahasa Indonesia melalui Gemini `gemini-3.5-flash-lite`, masing-masing dari 10 keyword berbobot dan 10 kalimat representatif. CSV beserta provenance/checksum dibaca dashboard tanpa panggilan API pada rerun. Array, Parquet, keyword, skor coherence, dan Excel identik dengan snapshot clustering sebelumnya; kedua snapshot tetap disimpan.

[Excel topik dan kalimat](../../outputs/nlp_20261030_instagram_500_topics20_gemini_02/topic_sentences.xlsx) · [Summary model](../../outputs/nlp_20261030_instagram_500_topics20_gemini_02/summary.json) · [Dataset sumber](../../outputs/social_20261030_combined_instagram_500_2h_02/social_data.xlsx)

| Topik | c_v |
|---|---:|
| T01 allah / semoga / sama | 0,4453 |
| T02 tahun / alumni / umur | 0,3250 |
| T03 kuliah / kerja / kampus | 0,5544 |
| T04 ibunya / ibu / anak | 0,5476 |
| T05 kek / istri / kip | 0,2991 |
| T06 gua / daftar / rocky | 0,2921 |
| T07 indonesia / malaysia / rakyat | 0,4360 |
| T08 lpdp / kip / snbp | 0,6656 |
| T09 terima kasih / terimakasih / thank | 0,5670 |
| T10 jangan / tidak / orang | 0,6176 |
| T11 korupsi / pajak / koruptor | 0,4091 |
| T12 bahasa / indo / inggris | 0,4300 |
| T13 video / videonya / youtube | 0,3451 |
| T14 dokter / psikolog / psikologi | 0,5189 |
| T15 game / seni / worth | 0,2758 |
| T16 negara / presiden / pemerintah | 0,5467 |
| T17 cerita / film / ceritanya | 0,3682 |
| T18 jepang / china / mandarin | 0,3951 |
| T19 ai / manusia / pekerjaan | 0,3961 |
| T20 kenapa / ngga / mana | 0,3382 |

Artifact Excel memiliki extension manifest `beesense-topic-sentences-excel:1`; loader memverifikasi checksum, sumber, jumlah topik dan jumlah pasangan kalimat sebelum UI menampilkan unduhan. Semua sel Excel dibandingkan ulang dengan kalimat dan cluster asli saat publikasi.

[[SocialNLPClusterer]] · [[Dataset Dashboard]] · [[Menjalankan BeeSense]] · [[Instagram 500 Post 2 Jam]] · [[HOME]]
