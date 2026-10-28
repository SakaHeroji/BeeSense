---
type: methodology
tags: [beesense, sbert, umap, dbscan, coherence]
---

# Metodologi Machine Learning Social NLP

[SocialNLPClusterer](../../social_nlp.py) memakai **SBERT multilingual → normalisasi L2 →
UMAP → DBSCAN Euclidean pada ruang UMAP → c-TF-IDF → artifact terverifikasi**.
[SocialNLPStreamlitApp](../../nlp_dashboard.py) membaca hasil tersimpan tanpa training pada rerun.

## Data dan hasil aktif

Input `outputs/social_20261028_01/social_data.xlsx` berisi 8.449 baris pada sheet Data.
8.218 komentar/balasan input menghasilkan 16.178 kemunculan, 15.878 kalimat unik,
300 pengulangan dan 1.045 potongan dilewati; 7.944 komentar/balasan terwakili.
Run aktif: `outputs/nlp_20261028_coherence_01`. Arsip `outputs/nlp_20261028_sbert_dbscan_01` dan `outputs/nlp_20261028_02` dipertahankan dengan checksum asli.
Workbook audit `outputs/social_20261028_01/dataset.xlsx` tidak diubah.

Hasil aktif: **52 topik**, coverage kalimat unik 95.11%, silhouette cosine -0.103367, ARI dua seed UMAP 0.825132. DBSCAN eps=0.3, min_samples=10. Noise: 776 kalimat unik dan 802 kemunculan. Fitting run publikasi 19.0 detik (embedding/UMAP dari cache tervalidasi).

## Encoder SBERT

`SentenceTransformer` memakai `sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2`,
revision immutable `e8f8c211226b894fcb81acc59f3b34ba3efd5f42`, 384 dimensi pada CPU.
Bobot native safetensors dimuat tanpa remote code. SHA-256 bobot/tokenizer dicatat.
Bobot pralatih tetap; proses ini melakukan fitting DBSCAN pada dataset, bukan
fine-tuning neural network tanpa label.

Tokenizer memakai 128 token, stride 24. Seluruh overflow window diteruskan melalui
modul SBERT, lalu dirata-ratakan per kalimat dan dinormalisasi L2. Kalimat panjang
tidak terpotong diam-diam. Cache mengikat revision, konfigurasi, versi encoder dan
seluruh embedding_text, beserta checksum matriks dan jumlah window.

## DBSCAN dan quality gate

Fitting memakai UMAP 10 dimensi (n_neighbors=15, min_dist=0, metric=cosine),
dua seed 42/43, lalu memilih parameter DBSCAN Euclidean pada hasil UMAP.
Embedding SBERT asli tetap menjadi ruang evaluasi. Tidak ada fallback HDBSCAN/KMeans. Jumlah cluster berasal dari kepadatan data. Radius graph Euclidean pada UMAP
dihitung per batch dan dipakai ulang pada grid eps/min_samples dalam social_nlp.json.
Zero-distance edges dipertahankan. Batas max_neighbor_edges mencegah alokasi
tetangga tak terkendali. Core point disimpan sebagai dbscan_core_point; label -1
adalah noise. membership_strength kosong karena DBSCAN tidak memberi probabilitas.

Satu sampel tetap hingga 1.800 kalimat dipakai untuk silhouette cosine pada embedding
asli. ARI membandingkan DBSCAN pada dua hasil UMAP ber-seed 42/43 untuk menguji
ketahanan terhadap variasi proyeksi. Shared noise dikeluarkan; noise lain diperlakukan sebagai
singleton. Ini pengukuran ketahanan terhadap proyeksi, bukan akurasi berlabel.

Kandidat eligible: minimal dua cluster, silhouette terdefinisi, coverage ≥0,4,
proporsi cluster terbesar ≤0,5 dari assigned, lalu coherence c_v ≥0,4. Skor:
`0.60*max(silhouette,0)*coverage + 0.25*max(ARI,0) + 0.15*coverage`.
Dalam toleransi 0,005 dari skor tertinggi, pilih silhouette, ARI, lalu coverage.
Tidak ada pengubahan quality gate otomatis; tanpa kandidat eligible, fitting berhenti.

## Coherence c_v dan ambang training

Coherence dihitung dengan Gensim 4.4.0 pada maksimum **10 istilah c-TF-IDF**
per topik dan sliding window **110 token**. Tokenisasi memakai analyzer
CountVectorizer yang sama: stopword Indonesia/Inggris dibuang, unigram diikuti
bigram, dan frasa bigram tetap satu token. Referensi adalah seluruh **15.878
kalimat unik embedding_text**, termasuk noise; kalimat tidak digabung per cluster
dan pengulangan occurrence tidak menambah bobot. Karena token mencakup frasa,
angka ini harus dibandingkan dengan evaluasi yang memakai protokol sama.

Skor akhir adalah **rata-rata tanpa bobot semua 52 topik non-noise**. Topik yang
kurang dari dua istilah valid, mengandung istilah di luar korpus atau menghasilkan
skor nonfinite membatalkan agregat; tidak dikeluarkan diam-diam. Istilah dengan
bobot c-TF-IDF nol tidak ditambahkan untuk memenuhi panjang daftar.

Baseline sebelum retrain **0,4097033012**; setelah retrain **0,4097033012**.
Target global **≥0,4 tercapai** sehingga tidak diperlukan perubahan parameter
untuk mengejar ambang tersebut. **31 dari 52 topik masih <0,4 secara individual**.
Ini bukan jaminan minimum setiap topik. Silhouette cosine SBERT asli tetap
**−0,103367**: coherence istilah yang lolos tidak menghapus tumpang tindih semantik.
Evaluasi memakai korpus training, bukan holdout atau akurasi anotasi manusia.

Ambang c_v ≥0,4 menjadi quality gate tambahan; batas cakupan dan dominasi cluster
sebelumnya tetap berlaku. Evaluasi coherence berjalan dari skor komposit tertinggi.
Semua kandidat dalam toleransi skor terbaik yang lolos c_v dihitung. Kandidat lebih
rendah yang tidak mungkin terpilih ditandai `not_evaluated_below_passing_score_band`,
bukan diklaim gagal coherence. Jika tidak ada kandidat lolos, pipeline berhenti.

`summary.json` menyimpan protokol, hash referensi token, skor setiap topik, baseline
beserta hash manifest/sumbernya, ambang, dan hasil pengujian. `topics.json` menyimpan
coherence setiap topik; `comparison.json` mencatat skor/status evaluasi kandidat.
Dashboard menampilkan skor global pada seluruh halaman, tabel per topik dan
perbandingan baseline pada **Metode & data**. Filter UI tidak menghitung ulang c_v.
Perubahan metadata bersifat aditif pada skema v2; snapshot v1/v2 lama tetap terbaca.

Referensi: [Gensim CoherenceModel](https://radimrehurek.com/gensim/models/coherencemodel.html).

## Kontrak Parquet dan artifact

Producer 2.1.0 memakai beesense-sentence-clusters:2. Sebelas artifact ditambah manifest:

| File | Isi |
|---|---|
| social_data.parquet | Semua baris Excel, source_row, tanggal WIB ISO |
| sentences.parquet | Kalimat unik, DBSCAN cluster/core point, centroid similarity |
| occurrences.parquet | Semua kemunculan, URL, source_row, span dan kepastian tanggal |
| skipped.parquet | Potongan yang dilewati beserta alasan |
| embeddings.npy / centroids.npy | Vektor SBERT/centroid asli float32, tanpa pickle |
| umap_embeddings.npz | Proyeksi dua seed UMAP yang dipakai fitting DBSCAN |
| topics.json / graph.json | Label c-TF-IDF dan graf cosine INFERRED |
| comparison.json / summary.json | Kandidat, parameter, evaluasi dan provenans |

manifest.json mengikat SHA-256 setiap artifact. Penulisan atomik menolak overwrite.
Loader menerima skema v1/v2; penjelasan v1 tidak memerlukan konfigurasi fitting lama.
Verifier memeriksa sumber, run aktif dan arsip NLP; output crawler terpisah tidak
dianggap bundle dashboard. --check-git juga memeriksa seluruh file publikasi terhadap
index Git, sehingga artifact baru harus masuk index sebelum pemeriksaan itu lulus.

## Pelatihan dan dashboard

```bash
python3.12 -m venv .venv-sbert
.venv-sbert/bin/python -m pip install -r requirements-sbert.txt
.venv-sbert/bin/python -u social_nlp.py --coherence-baseline outputs/nlp_20261028_sbert_dbscan_01 --output-dir outputs/nlp_run_baru
.venv-nlp/bin/python -m streamlit run nlp_dashboard.py --server.address=127.0.0.1 --server.port=8501
```

Mac Intel dapat memakai requirements-sbert-macos-intel.lock untuk versi teruji.
Environment training terpisah memakai PyTorch 2.2.2, NumPy 1.26.4, SciPy 1.15.3,
dan PyArrow 19.0.1; Gensim berada pada requirements-coherence.txt
(kebutuhan training/evaluasi saja); dashboard tetap memakai requirements.txt tanpa mengimpor Torch.
Parameter fit/data berada pada social_nlp.json. --run-dir/BEESENSE_NLP_RUN_DIR dapat
memilih run lain. Dashboard menunjukkan metode SBERT, eps/min_samples DBSCAN dan noise.

## Penjelasan, sumber dan batas interpretasi

Segmentasi mempertahankan kalimat asli, offset karakter, source_row, judul, URL,
tanggal WIB dan kepastian tanggal. Hanya embedding_text dinormalisasi; negasi tetap.
Dedup embedding mempertahankan seluruh occurrence. Judul/platform/tanggal bukan
fitur clustering. c-TF-IDF memakai unigram/bigram, stopwords Indonesia/Inggris dan
count per cluster; contoh dipilih berdasarkan cosine centroid, bukan teks generatif.

c-TF-IDF menjumlahkan count istilah per cluster. TF dinormalisasi L1; IDF memakai
log(1 + rata-rata panjang dokumen cluster / total count istilah lintas cluster).
Unigram/bigram dari cluster non-noise memberi kata pembeda dan label; seluruh
kalimat tetap menggunakan embedding SBERT untuk clustering, bukan c-TF-IDF.

MMR memilih kutipan sumber beragam. Theil–Sen/Kendall dan dua jendela waktu menyusun
arah deskriptif dengan pemeriksaan komentar, sumber, platform, bulan parsial dan
dukungan minimum. Tidak ada perubahan metode penjelasan/tren pada versi ini.
Porsi penjelasan menghitung komentar; ringkasan menghitung kemunculan kalimat.
Default tanggal adalah video/post induk; tanggal komentar YouTube bisa perkiraan.
Snapshot parsial bukan aktivitas seluruh platform. Label belum divalidasi manusia.

Graf topik memakai cosine centroid dan label INFERRED, bukan hubungan manusia atau
probabilitas. Filter mengubah volume/contoh; keanggotaan mengikuti model penuh.

## Verifikasi dan operasional

```bash
.venv-nlp/bin/python -m pip install -r requirements-coherence.txt
.venv-nlp/bin/python -m unittest discover -s tests/nlp -v
.venv-nlp/bin/python -m ruff check --isolated --select E4,E7,E9,F,I social_nlp.py nlp_dashboard.py scripts tests/nlp
.venv-nlp/bin/python -m ruff format --isolated --check social_nlp.py nlp_dashboard.py scripts tests/nlp
.venv-nlp/bin/python -m scripts.verify_dashboard_data
```

Tes mencakup kelompok sintetis, zero-distance DBSCAN, core/noise semantics, memory
guard, pembanding coherence pada korpus terkendali, gate c_v, istilah tidak valid, empat Parquet, checksum, v1/v2, penjelasan legacy dan lima tampilan UI tanpa
training. Pelatihan data asli memverifikasi integrasi SBERT native. Metrik internal
tidak membuktikan koherensi manusia setiap label atau cakupan sosial yang lengkap.

Tidak ada database atau migrasi. Konfigurasi Coolify dan Docker produksi tidak
diubah. Image dashboard membaca mount artifact read-only; Docker build/runtime
belum diverifikasi karena daemon lokal tidak aktif.

Referensi primer: [SBERT](https://sbert.net/),
[model card](https://huggingface.co/sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2),
[DBSCAN](https://scikit-learn.org/stable/modules/generated/sklearn.cluster.DBSCAN.html).


[[Dataset Dashboard]] · [[Arsitektur BeeSense]] · [[HOME]]
