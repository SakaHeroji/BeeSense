# Retraining gabungan sosial dan Twitter — 2 November 2026

[Input gabungan](../../outputs/social_20261102_combined_twitter_01/social_data.xlsx) memuat **34.764 record unik** dari YouTube, Reddit, Instagram dan Twitter, termasuk trial Twitter 31 Oktober serta seluruh hasil crawling hari ini. Verifikasi native ID: **0 duplikasi**. Conversation root X berasal dari audit terverifikasi/sidecar yang terikat checksum, bukan tebakan judul/tanggal.

[Snapshot model](../../outputs/nlp_20261102_twitter_topics20_gemini_01/summary.json) dihasilkan SocialNLPClusterer 2.5.0. Konfigurasi eksperimen tersimpan pada bagian `config` di summary snapshot tersebut. [Konfigurasi NLP utama](CONFIGURATION.md) kini menjadi satu file untuk kustomisasi. Eksperimen ini memakai dataset tersebut, tepat **20 topik**, mean c_v minimum **0,4**, dan Gemini enabled.

## Fitting dan evaluasi

- Input 34.764 record; 32.238 komentar/balasan eligible. Root post/video dipertahankan sebagai konteks, bukan dijadikan kalimat training.
- 53.332 kemunculan, 52.450 kalimat unik, 882 pengulangan, 5.959 segmen dilewati.
- SBERT multilingual pralatih tetap, normalisasi L2, UMAP dua seed, DBSCAN eps=0.2/min_samples=5, lalu Ward berbobot kalimat menjadi **20 topik**. 319 kelompok primer; noise dipertahankan.
- Rata-rata **c_v 0.4243209772**; gate 0,4 lulus. **9/20 topik** masih di bawah 0,4 secara individual. Referensi coherence mencakup seluruh kalimat unik, termasuk noise, top-10 istilah/window 110.
- Coverage **93.09%**, silhouette cosine **-0.022359**, stability ARI **0.793974**. Noise 3.626 kalimat unik/3.677 kemunculan.

Evaluasi merupakan coherence in-sample dan ketahanan terhadap dua proyeksi, bukan akurasi holdout berlabel. Skor korpus berbeda tidak menjadi bukti kenaikan kualitas. Metode lengkap: [SOCIAL_NLP](SOCIAL_NLP.md).

## Gemini dan dashboard

[CSV Gemini 20 topik](../../outputs/nlp_20261102_twitter_topics20_gemini_01/topic_narratives.csv) berisi satu kalimat topik dan deskripsi bahasa Indonesia per topik, dibuat dari 10 keyword c-TF-IDF positif tertinggi dan hingga 10 kalimat representatif yang diurutkan menurut cosine centroid. Model `gemini-3.5-flash-lite`, prompt `beesense-topic-id:2`. Ini sintesis AI, bukan kutipan sumber atau skor coherence tambahan.

Excel topic_sentences.xlsx memuat **48.850 pasangan topik–kalimat asli unik**, sheet Kalimat dua kolom dan sheet Topik dengan c_v/jumlah kalimat. Noise dikecualikan dari Excel dan tetap tersedia di artifact. Dashboard menyediakan filter X / Twitter, grafik sumber/cakupan/tren/jaringan, bukti dengan native root, CSV Gemini dan unduhan Excel. Runtime membaca artifact tersimpan tanpa training atau panggilan Gemini pada rerun.

Source SHA-256: `de6caf9b30724cc3d990ce25c81859b895559cd4be28f7ccbf95528613ce5990`. Manifest memverifikasi seluruh Parquet, array, metadata, CSV dan Excel. [Bukti crawling](../crawler/TWITTER_ACQUISITION_20261102.md). Snapshot sebelumnya dipertahankan. Tidak diperlukan migrasi database aplikasi.
