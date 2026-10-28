# Class NLP BeeSense

[SocialNLPClusterer](social_nlp.py) memproses komentar/balasan dari Excel SocialCrawler. [SocialNLPStreamlitApp](nlp_dashboard.py) membaca artifact tersimpan dan menampilkan dashboard. Class ML tidak bergantung pada Streamlit; rerun UI tidak melakukan training.

## Data aktif

- Input: `outputs/social_20261028_01/social_data.xlsx`, sheet Data, 8.449 baris.
- Baris komentar/balasan input: 8.218; yang menyumbang kalimat: 7.944.
- Kemunculan kalimat: 16.178; kalimat unik: 15.878.
- Run: `outputs/nlp_20261028_02`, 51 cluster dan 80 edge kemiripan.
- Tercluster: 8.427 kalimat unik (53,1%); 8.628 kemunculan (53,3%). Sisanya noise, bukan satu topik koheren.

Hanya Excel ini dan run ini disertakan. Semua run lama, salinan data dan bukti eksperimen telah dibersihkan untuk publikasi repository. Penjelasan topik dihitung dari run aktif; tidak membutuhkan ekspor penjelasan historis.

## Algoritma dan evaluasi

Model multilingual MiniLM menghasilkan embedding 384 dimensi melalui ONNX CPU, attention-mask mean pooling dan normalisasi L2. Teks panjang diproses dengan jendela bertumpang tindih. UMAP 10 dimensi diikuti scikit-learn HDBSCAN (`min_cluster_size=60`, `min_samples=10`, EOM); c-TF-IDF memberi istilah pembeda.

Sepuluh kandidat dibandingkan dengan silhouette cosine pada embedding asli, cakupan dan ARI. Skor tertinggi KMeans K40 sebesar 0,311448; HDBSCAN terpilih dengan 0,311392 karena berada dalam toleransi operasional 0,005 dan memiliki pemisahan embedding lebih baik. Silhouette HDBSCAN 0,0951 dan ARI 0,806. Toleransi ini heuristik, bukan uji signifikansi. Tidak ada label acuan untuk mengklaim akurasi semantik atau algoritma terbaik secara universal.

Data segmentasi mempertahankan teks asli, offset karakter, source_row Excel, judul, URL dan kepastian tanggal WIB. Hanya teks embedding dinormalisasi; negasi dipertahankan. Judul/platform/tanggal bukan fitur clustering. Dedup embedding mempertahankan semua occurrence asal. Bagian pendek/tidak informatif dicatat pada skipped.parquet.

Revision model immutable `e8f8c211226b894fcb81acc59f3b34ba3efd5f42`; SHA-256 bobot ONNX `98a01d88b7de996cdea58c32ca71208c09968d143798814b2ea09d3439dc334f`. Metadata dan parameter hasil asli tersimpan pada summary.json. Cache model diunduh ulang hanya saat training baru dan diabaikan Git.

## API

`prepare_excel()`, `encode()`, `compare()`, `describe_topics()`, `build_topic_graph()`, `fit_excel()`, `save()` dan `load_run()` menangani clustering. `explain_topics()`/`explain_artifacts()` serta `save_explanations()`/`load_explanations()` menangani penjelasan terpisah.

```python
from social_nlp import SocialNLPClusterer

saved = SocialNLPClusterer.load_run("outputs/nlp_20261028_02")
explanations = SocialNLPClusterer.explain_artifacts(saved)
# Training baru, jika diperlukan; direktori lama tidak ditimpa:
# SocialNLPClusterer("social_nlp.json").fit_excel().save("outputs/nlp_run_baru")
```

Semua pengaturan ada pada social_nlp.json. Dashboard dapat memakai `--run-dir` atau `BEESENSE_NLP_RUN_DIR` untuk run lain. Petunjuk instalasi, pengujian dan Docker: [README.md](README.md).

## Kontrak penyimpanan

Run asli memakai **beesense-sentence-clusters:1**, producer asli 1.0.0; kode kini producer 1.1.0. Sembilan artifact adalah summary.json, topics.json, graph.json, comparison.json, sentences.parquet, occurrences.parquet, skipped.parquet, embeddings.npy, centroids.npy. manifest.json mengikat sembilan SHA-256. Tidak memakai pickle. Loader memeriksa checksum, skema, path traversal dan kecocokan bentuk embedding.

[scripts/verify_dashboard_data.py](scripts/verify_dashboard_data.py) memverifikasi run, checksum Excel terhadap metadata, serta bahwa outputs hanya berisi sebelas file data yang diizinkan. Opsi `--check-git` juga memeriksa daftar file data yang dilacak Git. Path absolut sumber pada metadata historis tidak dipakai untuk membaca file saat dashboard dijalankan.

Ekspor penjelasan memakai skema sidecar **beesense-topic-explanations:1** dengan identitas source-manifest/input/hash kode; output baru atomik menolak overwrite. Ekspor baru otomatis diabaikan Git. Tidak ada perubahan database atau migrasi.

## Membaca hasil

Edge peta adalah cosine similarity centroid model penuh: **INFERRED**, bukan relasi manusia atau probabilitas. Filter mengubah volume/contoh, bukan keanggotaan, centroid atau posisi model. Porsi penjelasan menghitung komentar, sedangkan ringkasan utama menghitung kemunculan kalimat. Default waktu memakai tanggal post induk, bukan waktu aktivitas komentar.

Baca [DASHBOARD_DESIGN.md](DASHBOARD_DESIGN.md) untuk UI dan [EXPLAINABLE_TOPICS.md](EXPLAINABLE_TOPICS.md) untuk ringkasan MMR, arah Theil–Sen/Kendall, dukungan sumber dan keterbatasan. Noise dan pengambilan parsial tetap terlihat.

## Referensi primer

- [Model card MiniLM](https://huggingface.co/sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2).
- [HDBSCAN scikit-learn](https://scikit-learn.org/stable/modules/generated/sklearn.cluster.HDBSCAN.html).
- [Pola embedding/UMAP/HDBSCAN/c-TF-IDF BERTopic](https://maartengr.github.io/BERTopic/algorithm/algorithm.html); proyek tidak bergantung pada paket BERTopic.
- [Plotly selection Streamlit](https://docs.streamlit.io/develop/api-reference/charts/st.plotly_chart).

## Uraian metodologi terperinci

[Metodologi Machine Learning Social NLP](<graphify-out/obsidian/Metodologi Machine Learning Social NLP.md>) menguraikan seluruh alur fungsi, embedding tetap, fitting kandidat, rumus/policy evaluasi, c-TF-IDF, penjelasan/tren, semua field konfigurasi, default library, persistensi dan cakupan pengujian. Dokumen ini juga tersedia langsung sebagai catatan Obsidian.
