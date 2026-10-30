---
type: architecture
tags: [beesense, nlp, gemini, dashboard]
---

# Topik Gemini

## Snapshot aktif setelah tambahan Instagram

Label c-TF-IDF dan seluruh keanggotaan cluster dipertahankan. Sesuai instruksi pengguna, `SocialNLPClusterer.generate_topic_narratives()` membuat 20 kalimat topik dan deskripsi bahasa Indonesia melalui Gemini `gemini-3.5-flash-lite`, masing-masing dari 10 keyword berbobot dan 10 kalimat representatif. CSV beserta provenance/checksum dibaca dashboard tanpa panggilan API pada rerun. Array, Parquet, keyword, skor coherence, dan Excel identik dengan snapshot clustering sebelumnya; kedua snapshot tetap disimpan.

Run `outputs/nlp_20261030_instagram_500_topics20_gemini_02`: rata-rata c_v **0,4386500025**, 20 topik, 51.979 kalimat unik. Excel 45.556 pasangan topik–kalimat tetap identik; 9 skor individual di bawah 0,4.

[CSV 20 topik Gemini](../../outputs/nlp_20261030_instagram_500_topics20_gemini_02/topic_narratives.csv) · [[Training Instagram 20 Topik]]

| Topik | Kalimat bahasa Indonesia |
|---|---|
| T01 | Penyampaian doa, harapan baik, serta berbagai ungkapan apresiasi menjadi ragam tanggapan dalam percakapan. |
| T02 | Pembahasan mengenai batasan usia, tahun kelulusan, dan jangka waktu menjadi perhatian dalam berbagai tanggapan. |
| T03 | Pilihan pendidikan tinggi dan jurusan menjadi bahan pembahasan yang berkaitan dengan peluang kerja serta pembiayaan. |
| T04 | Respons dan tanggapan emosional muncul terhadap karakter ibu dalam suatu cerita atau adegan. |
| T05 | Pembahasan mencakup dinamika hubungan keluarga dan pernikahan bersama pengalaman sehari-hari. |
| T06 | Pembahasan mengenai pendaftaran dan informasi tertentu diwarnai berbagai tanggapan serta pertanyaan dari peserta. |
| T07 | Berbagai tanggapan mengenai kondisi sosial dan kebijakan publik di Indonesia menjadi bahan perbincangan di tengah masyarakat. |
| T08 | Proses pendaftaran seleksi masuk perguruan tinggi dan program bantuan biaya pendidikan menjadi pokok pertanyaan para peserta. |
| T09 | Ungkapan terima kasih dan permohonan informasi menjadi bentuk interaksi yang dominan dalam percakapan ini. |
| T10 | Berbagai tanggapan dan ungkapan spontan muncul dalam percakapan yang membahas beragam topik tanpa fokus utama yang jelas. |
| T11 | Permasalahan korupsi dan penegakan hukum menjadi sorotan dalam kaitan dengan pengelolaan keuangan negara serta dampaknya terhadap kesejahteraan rakyat. |
| T12 | Penggunaan berbagai bahasa asing serta terjemahan dokumen menjadi bahan pembahasan dalam konteks pendidikan dan persiapan studi di luar negeri. |
| T13 | Tanggapan terhadap tayangan video yang dibagikan mencakup apresiasi atas manfaat isi konten serta izin pemanfaatannya. |
| T14 | Profesi dokter, spesialis, dan tenaga kesehatan menjadi topik pembahasan yang mencakup bidang kedokteran serta psikologi. |
| T15 | Pembahasan mencakup berbagai pandangan tentang cara menjalani hidup, pengambilan keputusan yang bijak, serta berbagai aktivitas keseharian. |
| T16 | Kritik terhadap kinerja serta kepemimpinan pejabat negara menjadi pokok pembahasan utama dalam berbagai tanggapan masyarakat. |
| T17 | Berbagai tanggapan penonton menyoroti alur cerita dan drama yang diangkat dari kisah nyata. |
| T18 | Pilihan belajar dan kuliah di negara-negara Asia seperti China dan Jepang menjadi bahan perbincangan terkait bahasa serta peluang kerja. |
| T19 | Perkembangan kecerdasan buatan yang sangat masif memicu pembahasan mengenai dampaknya terhadap berbagai jenis pekerjaan manusia. |
| T20 | Pertanyaan santai dan ungkapan keheranan mendominasi percakapan yang membahas berbagai informasi dengan beragam tanggapan. |

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

## Riwayat sebelum tambahan Instagram

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
