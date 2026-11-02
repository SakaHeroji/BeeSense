# Penyaringan relevansi konteks sebelum clustering

`ContextRelevanceFilter` pada `MachineLearning/context_relevance.py` membuat keputusan otomatis per kemunculan kalimat. Backend `LocalSemanticBackend` pada `MachineLearning/relevance_semantic.py` memakai encoder SBERT multibahasa pralatih yang sama dengan pipeline NLP. Tidak ada pelabelan setiap record oleh pengguna, training classifier berlabel, atau permintaan API per komentar.

## Ruang lingkup dan algoritma

`config/context_relevance.json` menyimpan keyword pencarian, definisi ruang lingkup, contoh konteks relevan/interaksi umum/di luar lingkup, revision model tetap, dan ambang cosine. Setiap keyword wajib memiliki contoh konteks relevan. Mengganti keyword ke domain lain membutuhkan pembaruan contoh konteks, bukan hanya mengganti daftar kata.

Untuk setiap kalimat, backend menghitung maksimum cosine terhadap contoh pada setiap kategori. Ini klasifikasi berdasarkan referensi semantik, bukan probabilitas atau pengukuran akurasi. Referensi adalah contoh rancangan; bukan label kebenaran untuk seluruh dataset.

- Relevan langsung: cosine kategori relevan ≥0,42 dan selisih dari kategori lain ≥0,035.
- Target pendek (maksimum 14 kata) dengan skor relevan <0,60 tetap memerlukan konteks, meskipun lolos ambang awal.
- Interaksi umum/di luar lingkup: kategori tersebut menang dan cosine ≥0,42. Post pendidikan tidak boleh meloloskan target yang sudah jelas melenceng.
- Target meragukan yang pendek dan skor langsung relevan ≥0,22 dapat diperiksa bersama konteks. Ia diterima jika cosine relevan kontekstual ≥0,50 dengan margin ≥0,035.
- Selain itu keputusan tetap `uncertain`. Hanya `relevant` masuk clustering. Semua keputusan dan sumber mentah dipertahankan.

Root percakapan ditentukan dari URL/native ID. Komentar induk dipakai hanya jika relasi dan teksnya cocok dengan audit crawling ber-checksum. Parent yang hilang atau konflik tidak ditebak. Konteks membantu seleksi; kalimat asli saja menjadi fitur clustering. Label cluster lama tidak dipakai sebagai aturan relevansi.

Ambang bersifat sementara dan belum dikalibrasi dengan label manusia. Uji contoh/perbandingan dua konteks memeriksa perilaku, bukan membuktikan precision/recall. Model NLI ringan sempat diuji lokal dan ditolak sebagai backend setelah hasil contoh Bahasa Indonesianya kurang memadai.

## Menjalankan eksperimen

Lingkungan pemrosesan memakai `requirements/sbert.txt`; dashboard memakai `requirements.txt`. Setelah persetujuan pengguna untuk publikasi, `config/social_nlp.json` mengarah ke snapshot tersaring `outputs/nlp_20261102_relevance_topics20_gemini_02/`. Preset Twitter sebelum penyaringan dan snapshot lamanya tetap tersedia untuk rollback. Entry point Streamlit Cloud tetap `streamlit_apps.py`; runtime tidak memakai API key.

```bash
.venv-sbert/bin/python -m scripts.filter_context_relevance \
  --source-run outputs/nlp_20261102_twitter_topics20_gemini_01 \
  --config config/context_relevance.json \
  --output-dir outputs/relevance_20261102_01

.venv-sbert/bin/python -m MachineLearning.social_nlp \
  --config config/social_nlp_relevance_20261102.json \
  --reuse-embeddings-from outputs/nlp_20261102_twitter_topics20_gemini_01

.venv-dashboard/bin/python -m scripts.relevance_dashboard
```

Penyaringan menghasilkan `relevance_decisions.parquet`, `filtered_sentences.parquet`, laporan, dan manifest. Artifact terikat checksum workbook sumber dan mencakup semua occurrence tepat sekali. Konfigurasi yang diberikan secara eksplisit harus menyebut `relevance_artifact` untuk memakai mask; ia tidak mewarisi mask snapshot aktif secara diam-diam. Pemanggilan tanpa konfigurasi tetap mengikuti default repository. Model baru menyertakan salinan keputusan/laporan melalui extension `beesense-context-relevance:1`.

Embedding target yang identik dapat digunakan kembali hanya setelah checksum sumber, konfigurasi encoder, sentence ID, teks, dan normalisasi diverifikasi. UMAP, DBSCAN, penggabungan menjadi 20 topik dan evaluasi dijalankan lagi pada kalimat yang lolos. Gate rata-rata c_v ≥0,4 tetap berlaku. Coherence sebelum/sesudah filter memiliki korpus referensi berbeda, sehingga bukan perbandingan kualitas langsung.

Setelah pengguna secara eksplisit meminta deskripsi Gemini untuk 20 topik tersaring, preset eksperimen mengaktifkan Gemini. Setiap topik mengirim 10 keyword c-TF-IDF tertinggi dan 10 kalimat representatif berurutan menurut cosine ke centroid, memakai prompt `beesense-topic-id:2`. Hasil satu kalimat topik beserta paragraf deskripsi disimpan di `outputs/nlp_20261102_relevance_topics20_gemini_02/topic_narratives.csv`. Ini sintesis AI dari bukti terpilih, bukan pengukuran popularitas atau validasi akurasi relevansi.

Snapshot tanpa narasi `outputs/nlp_20261102_relevance_topics20_01/` tetap utuh. Penambahan narasi menggunakan skrip berikut tanpa menjalankan training, UMAP, atau clustering ulang:

```bash
.venv-sbert/bin/python -m scripts.generate_topic_narratives \
  --source-run outputs/nlp_20261102_relevance_topics20_01 \
  --output-dir outputs/nlp_20261102_relevance_topics20_gemini_02 \
  --config config/social_nlp_relevance_20261102.json
```

Direktori contoh sudah terisi; gunakan nama output baru untuk percobaan berikutnya. Skrip menolak overwrite, memvalidasi checksum sumber sebelum/sesudah permintaan, menyalin file fitted apa adanya, dan mempublikasikan bundle secara atomik setelah CSV serta manifest lolos validasi. Dua belas file data/clustering/audit memiliki checksum identik dengan snapshot sebelum narasi. CSV mencakup tepat 20 topik, provenance prompt/model/sumber dan pemakaian token. API key hanya dibaca dari auth lokal yang diabaikan Git; tidak masuk konfigurasi atau bundle. Pembuatan narasi awal sempat ditolak persetujuan otomatis karena cakupan saat itu hanya lokal; permintaan eksplisit berikutnya memberi otorisasi untuk Gemini dan proses berhasil.

Dashboard lokal pada `http://localhost:8502` memiliki pilihan **Bandingkan snapshot**. Bagian **Metode & data** menampilkan kategori keputusan, distribusi platform, contoh audit dan unduhan CSV. Runtime dashboard membaca hasil tersimpan tanpa memuat Torch, menjalankan filter, atau memanggil Gemini.

## Rollback dan penyimpanan

Pilih **Sebelum penyaringan** pada sidebar untuk pembandingan langsung. Untuk menjalankan hanya baseline, hentikan proses dashboard lokal lalu jalankan:

```bash
.venv-dashboard/bin/python -m scripts.relevance_dashboard --baseline
```

Snapshot lama dan workbook gabungan dipertahankan. Konfigurasi sebelum penyaringan tersedia di `config/social_nlp_twitter_20261102.json`; konfigurasi aktif kini memakai preset relevansi setelah pengguna menyetujui publikasi. Cadangan kode sebelum eksperimen disimpan di `output/relevance_experiment_20261102/rollback/`, dengan hash checkpoint pada `baseline.json` di folder induknya. Untuk mengembalikan default repository, salin preset Twitter sebelum penyaringan ke `config/social_nlp.json`, verifikasi bundle, lalu commit/push agar Cloud memuatnya. Publikasi memakai bundle penuh dengan allowlist Git dan pemeriksaan `python -m scripts.verify_dashboard_data --check-git`; dataset penyaringan dicocokkan dengan keputusan fitted model.

Tidak diperlukan migrasi database aplikasi. Cache skor SQLite baru bersifat disposable dan menggunakan nama format `semantic_scores_v1.sqlite3`; artifact memiliki extension versi tersendiri. Docker dashboard tetap membaca bundle melalui volume; model/training tidak ditambahkan ke dependency runtime dashboard.

Referensi: [SBERT semantic similarity](https://sbert.net/docs/sentence_transformer/usage/semantic_textual_similarity.html).

## Hasil eksperimen lokal — 2 November 2026

- Sumber: 34.764 record unik; data asli dan konfigurasi aktif tidak berubah.
- Keputusan: 10,496 relevan, 18,990 interaksi umum, 3,747 di luar lingkup, 20,099 meragukan dari 53,332 kemunculan.
- Kalimat diterima: 10,380 unik dari 6.544 komentar/balasan sumber. Relasi parent terverifikasi tersedia pada 6,633 kemunculan.
- Clustering: 20 topik; mean c_v 0.4733391691; 7/20 topik masih <0,4 individual. Coverage unik 82.1676%, silhouette cosine 0.049654, ARI 0.811814.
- DBSCAN eps 0,25/min_samples 10 menghasilkan 66 kelompok primer, kemudian Ward berbobot menggabungkannya menjadi 20. Embedding SBERT identik digunakan kembali; proyeksi/clustering/evaluasi dijalankan ulang.
- Snapshot dashboard lokal: `outputs/nlp_20261102_relevance_topics20_gemini_02/`, dengan CSV 20 narasi Gemini. Snapshot clustering sebelum narasi: `outputs/nlp_20261102_relevance_topics20_01/`. Dataset keputusan: `outputs/relevance_20261102_01/`. Pengguna telah menyetujui commit/push dan redeploy snapshot ini.

Contoh kelompok berlabel negara/rakyat memuat pembahasan LPDP, tanggung jawab penerima beasiswa, biaya kuliah dan pendidikan. Label c-TF-IDF singkat tidak cukup untuk menentukan relevansi; periksa kalimat serta konteks audit. Ada risiko salah seleksi otomatis dan banyak kasus meragukan yang dipisahkan; belum ada pengukuran akurasi berlabel.
