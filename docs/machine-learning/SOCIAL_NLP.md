# Class NLP BeeSense: SBERT + UMAP + DBSCAN

[SocialNLPClusterer](../../MachineLearning/social_nlp.py) memakai **SBERT multilingual → normalisasi L2 →
UMAP → DBSCAN Euclidean pada ruang UMAP → penggabungan Ward berbobot kalimat → c-TF-IDF → artifact terverifikasi**.
[SocialNLPStreamlitApp](../../Dashboard/app.py) membaca hasil tersimpan tanpa training pada rerun.

## Data dan hasil aktif setelah tambahan Instagram

Input `outputs/social_20261030_combined_instagram_500_2h_02/social_data.xlsx` memuat **34.095 record unik**, **2.160 post asal**, dan **31.935 komentar/balasan**. Input menggabungkan 33.034 record sebelumnya dengan 301 post Instagram, 622 komentar dan 138 balasan baru. Pemeriksaan memastikan 0 duplikasi ID, 0 overlap post baru dengan baseline, dan semua nilai sel baseline tetap utuh.

Run aktif `outputs/nlp_20261030_instagram_500_topics20_gemini_02` menghasilkan **20 topik**, rata-rata **c_v 0,4386500025**, coverage **87,59%**, silhouette cosine **-0,018778**, dan ARI dua seed **0,739133**. DBSCAN eps=0,2/min_samples=10 menghasilkan 279 kelompok primer, lalu Ward berbobot menggabungkannya menjadi 20 topik. Encoding SBERT dihitung baru pada 51.979 kalimat unik; bobot encoder pralatih tetap. Persiapan menghasilkan 52.861 kemunculan, 882 pengulangan dan 5.931 segmen dilewati; 29.132 komentar/balasan terwakili. Noise terdiri atas 6.449 kalimat unik/6.523 kemunculan.

Excel `topic_sentences.xlsx` memuat **45.556 pasangan topik–kalimat asli unik**. Sheet Kalimat berisi tepat kolom `topik` dan `kalimat yang berada dalam cluster topik`; sheet Topik mencantumkan c_v dan jumlah kalimat setiap topik. Pengulangan teks yang sama dalam satu cluster disatukan; variasi asli yang berbeda tetap dipertahankan. Kalimat noise tersedia dalam artifact model dan jumlahnya dicatat pada Excel. Dashboard menyediakan unduhan Excel snapshot lengkap pada Kalimat & sumber; unduhan JSONL tetap mengikuti filter.

Ambang ≥0,4 berlaku pada **rata-rata tanpa bobot semua 20 topik**; **9/20 topik** masih di bawah 0,4 secara individual. Referensi coherence mencakup seluruh kalimat unik, termasuk noise, dengan top-10 istilah/window 110. Ini evaluasi in-sample, bukan akurasi berlabel; skor antar-korpus tidak dibandingkan sebagai kenaikan kualitas. Label c-TF-IDF dan seluruh keanggotaan cluster dipertahankan. Sesuai instruksi pengguna, `SocialNLPClusterer.generate_topic_narratives()` membuat 20 kalimat topik dan deskripsi bahasa Indonesia melalui Gemini `gemini-3.5-flash-lite`, masing-masing dari 10 keyword berbobot dan 10 kalimat representatif. CSV beserta provenance/checksum dibaca dashboard tanpa panggilan API pada rerun. Array, Parquet, keyword, skor coherence, dan Excel identik dengan snapshot clustering sebelumnya; kedua snapshot tetap disimpan.

## Riwayat sesi sebelumnya pada 30 Oktober 2026

Input `outputs/social_20261030_combined_3days_02/social_data.xlsx` memuat **33.034 record unik**, **1.859 root**, dan **31.175 komentar/balasan** dari hasil akuisisi 27–30 Oktober. Sebanyak 49.952 pengulangan antarberkas disisihkan; pemeriksaan menemukan 0 ID native ganda. Total Instagram 324 post/3.038 komentar mencakup batch terbaru 248 post/2.128 komentar dan trial sebelumnya 76 post/910 komentar. Pengguna menghentikan crawling setelah HTTP 429; target 1.000 post dan durasi 3 jam belum tercapai.

Run aktif `outputs/nlp_20261030_instagram_topics20_02` menghasilkan **20 topik**, rata-rata **c_v 0,4315219014**, coverage **94,67%**, silhouette cosine **-0,057864**, dan ARI dua seed **0,820417**. DBSCAN eps=0,25/min_samples=10 menghasilkan 165 kelompok primer, lalu Ward berbobot menggabungkannya menjadi 20 topik. Noise terdiri atas 2.751 kalimat unik. Persiapan menghasilkan 52.451 kemunculan/51.612 kalimat unik, 839 pengulangan dan 5.516 segmen dilewati; 28.758 komentar/balasan terwakili. Fitting inti berlangsung 1.195,5 detik sebelum tahap Gemini.

Gemini `gemini-3.5-flash-lite` menghasilkan **20 kalimat topik dan deskripsi bahasa Indonesia**, masing-masing dari 10 keyword c-TF-IDF berbobot tertinggi dan 10 kalimat terdekat dengan pusat topik. `topic_narratives.csv` beserta provenance/checksum masuk bundle model. UI membaca CSV tanpa API atau training saat rerun. Sebanyak 8 dari 20 topik masih memiliki c_v individual <0,4; ambang berlaku pada rata-rata. Evaluasi ini in-sample, bukan akurasi berlabel atau holdout. Skor dari korpus berbeda tidak menjadi perbandingan kualitas langsung.

## Riwayat 29 Oktober 2026

Input `outputs/social_20261029_combined/social_data.xlsx` menggabungkan baseline 8.449 baris dan akuisisi baru 20.650 baris: **29.099 baris**, **1.517 post asal**, dan **27.582 komentar/balasan**. Persiapan menghasilkan 46.916 kemunculan, 46.143 kalimat unik, 773 pengulangan dan 4.741 potongan dilewati; 25.739 komentar/balasan terwakili.

Run aktif: `outputs/nlp_20261029_combined_topics20_01`, dengan `target_topics: 20`. Empat Parquet dan manifest disimpan pada direktori versi baru; dua workbook baseline dan seluruh snapshot NLP sebelumnya dipertahankan. Tidak ada ID native ganda dalam workbook gabungan.

Hasil aktif: **20 topik**, c_v rata-rata **0,4720034334**, coverage kalimat unik **87,14%**, silhouette cosine **-0,000279**, ARI dua seed UMAP **0,764229**. DBSCAN eps=0.2, min_samples=10 menghasilkan 245 kelompok primer yang digabung menjadi 20 melalui Ward berbobot. Noise: 5.933 kalimat unik dan 6.029 kemunculan. Percobaan fitting terpublikasi 114,6 detik. Embedding SBERT dihitung baru untuk korpus gabungan, lalu dipakai dari cache terverifikasi pada percobaan radius yang sesuai batas memori; kedua UMAP juga memakai cache korpus yang sama.

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
Embedding SBERT asli tetap menjadi ruang evaluasi. Tidak ada fallback HDBSCAN/KMeans. DBSCAN menemukan kelompok dari kepadatan data, kemudian penggabungan berikut menentukan jumlah topik akhir. Radius graph Euclidean pada UMAP
dihitung per batch dan dipakai ulang pada grid eps/min_samples dalam config/social_nlp.json.
Zero-distance edges dipertahankan. Batas max_neighbor_edges mencegah alokasi
tetangga tak terkendali. Core point disimpan sebagai dbscan_core_point; label -1
adalah noise. membership_strength kosong karena DBSCAN tidak memberi probabilitas.

Run 29 Oktober memakai15 kandidat: eps 0,1/0,15/0,2/0,25/0,3 dan min_samples 3/5/10. Batas tetap 8.000.000 edge per proyeksi; radius maksimum 0,6 melampaui batas ini pada percobaan awal sehingga tidak dipublikasikan. Radius dipersempit tanpa mengubah ambang coherence/cakupan/dominasi. Embedding dan kedua proyeksi baru dipakai dari cache yang terverifikasi cocok dengan korpus gabungan. Kandidat terpilih eps=0,2/min_samples=10; hasil pencarian berlaku untuk grid yang dievaluasi ini.

Satu sampel tetap hingga 1.800 kalimat dipakai untuk silhouette cosine pada embedding
asli. ARI membandingkan topik akhir setelah penggabungan pada dua hasil UMAP ber-seed 42/43 untuk menguji
ketahanan terhadap variasi proyeksi. Shared noise dikeluarkan; noise lain diperlakukan sebagai
singleton. Ini pengukuran ketahanan terhadap proyeksi, bukan akurasi berlabel.

Kandidat eligible: tepat `target_topics` topik pada kedua seed (bila dikonfigurasi), minimal dua cluster, silhouette terdefinisi, coverage ≥0,4,
proporsi cluster terbesar ≤0,5 dari assigned, lalu coherence c_v ≥0,4. Skor:
`0.60*max(silhouette,0)*coverage + 0.25*max(ARI,0) + 0.15*coverage`.
Dalam toleransi 0,005 dari skor tertinggi, pilih silhouette, ARI, lalu coverage.
Tidak ada pengubahan quality gate otomatis; tanpa kandidat eligible, fitting berhenti.

## Penggabungan menjadi 20 topik

`target_topics: 20` mengaktifkan penggabungan hierarkis Ward berbobot jumlah kalimat
unik pada embedding SBERT asli. Untuk kelompok A dan B, biaya penggabungan adalah
`n_A*n_B/(n_A+n_B) * ||mean_A - mean_B||²`; mean berasal dari jumlah vektor asli,
bukan centroid yang dinormalisasi ulang. Pasangan berbiaya terkecil digabung sampai
tepat 20 kelompok. Kelompok DBSCAN tidak dipecah; noise -1 tetap tidak terkelompok.
ID akhir berurutan 0–19. `dbscan_cluster_id` mempertahankan ID sebelum penggabungan;
`summary.topic_reduction` menyimpan mapping lengkap dan biaya setiap langkah.

Penggabungan dilakukan pada setiap kandidat dan kedua seed **sebelum** silhouette,
ARI, proporsi kelompok terbesar dan coherence dihitung. Kandidat dengan kelompok
asal kurang dari 20 pada salah satu seed tidak dapat dipilih. Batas 2.048 kelompok
asal membatasi matriks pasangan dalam memori. `target_topics: null` mempertahankan
mode jumlah topik alami DBSCAN. Label c-TF-IDF, centroid, graf, contoh dan penjelasan
selalu dihitung dari keanggotaan topik akhir; UI tidak memotong daftar 52 topik.

## Coherence c_v dan ambang training

Coherence dihitung dengan Gensim 4.4.0 pada maksimum **10 istilah c-TF-IDF**
per topik dan sliding window **110 token**. Tokenisasi memakai analyzer
CountVectorizer yang sama: stopword Indonesia/Inggris dibuang, unigram diikuti
bigram, dan frasa bigram tetap satu token. Referensi adalah seluruh **kalimat unik embedding_text dari input run tersebut**, termasuk noise; kalimat tidak digabung per cluster
dan pengulangan occurrence tidak menambah bobot. Karena token mencakup frasa,
angka ini harus dibandingkan dengan evaluasi yang memakai protokol sama.

Skor akhir adalah **rata-rata tanpa bobot semua 20 topik non-noise**. Topik yang
kurang dari dua istilah valid, mengandung istilah di luar korpus atau menghasilkan
skor nonfinite membatalkan agregat; tidak dikeluarkan diam-diam. Istilah dengan
bobot c-TF-IDF nol tidak ditambahkan untuk memenuhi panjang daftar.

Run gabungan menghasilkan rata-rata c_v **0,4720034334**, memenuhi target **≥0,4**. **7 dari 20 topik masih <0,4 secara individual**; ambang ini berlaku pada rata-rata. Silhouette cosine SBERT asli -0,000279 tetap perlu dibaca bersama coverage dan keragaman sumber.

Hasil historis pada workbook baseline yang sama adalah 52 topik/c_v 0,4097033012 dan 20 topik/c_v 0,4143250939. Run gabungan memakai korpus dan hash referensi berbeda, sehingga selisih terhadap dua angka tersebut bukan perbandingan kualitas langsung. Coherence baseline dalam metadata run baru tidak diisi karena inputnya berbeda. Evaluasi tetap in-sample, bukan akurasi atau holdout berlabel manusia.

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

Producer 2.2.0 memakai beesense-sentence-clusters:2. Sebelas artifact ditambah manifest:

| File | Isi |
|---|---|
| social_data.parquet | Semua baris Excel, source_row, tanggal WIB ISO |
| sentences.parquet | Kalimat unik, cluster_id akhir, dbscan_cluster_id asal/core point, centroid similarity |
| occurrences.parquet | Semua kemunculan, cluster_id akhir, dbscan_cluster_id asal, URL, source_row, span dan kepastian tanggal |
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
.venv-sbert/bin/python -m pip install -r requirements/sbert.txt
.venv-sbert/bin/python -m MachineLearning.social_nlp --coherence-baseline outputs/nlp_20261029_combined_topics20_01 --output-dir outputs/nlp_run_baru
.venv-nlp/bin/python -m streamlit run streamlit_apps.py --server.address=127.0.0.1 --server.port=8501
```

Mac Intel dapat memakai requirements/sbert-macos-intel.lock untuk versi teruji.
Environment training terpisah memakai PyTorch 2.2.2, NumPy 1.26.4, SciPy 1.15.3,
dan PyArrow 19.0.1; Gensim berada pada requirements/coherence.txt
(kebutuhan training/evaluasi saja); dashboard memakai requirements.txt → requirements/dashboard.txt tanpa ONNX Runtime, Numba, UMAP, Gensim atau Torch. Runtime dashboard mendukung Python 3.12/3.14; training dan tes NLP penuh tetap Python 3.12.
Parameter fit/data berada pada config/social_nlp.json. --run-dir/BEESENSE_NLP_RUN_DIR dapat
memilih run lain. Dashboard menunjukkan metode SBERT, kelompok DBSCAN asal, jumlah topik akhir, coherence dan noise.

Untuk mengulang clustering tanpa mengunduh model atau menghitung embedding identik:

```bash
.venv-nlp/bin/python -m pip install -r requirements/dev.txt
.venv-nlp/bin/python -m MachineLearning.social_nlp \
  --reuse-embeddings-from outputs/nlp_20261029_combined_topics20_01 \
  --coherence-baseline outputs/nlp_20261029_combined_topics20_01 \
  --output-dir outputs/nlp_run_baru
```

Reuse memverifikasi seluruh checksum artifact, hash workbook, konfigurasi model,
urutan sentence_id/embedding_text dan normalisasi L2. Manifest sumber embedding
dicatat pada metadata. Ini refitting UMAP/DBSCAN dan penggabungan topik; bobot
neural SBERT tetap pralatih. Tidak perlu Torch untuk jalur reuse ini.

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
.venv-nlp/bin/python -m pip install -r requirements/dev.txt
.venv-nlp/bin/python -m unittest discover -s tests/nlp -v
.venv-nlp/bin/python -m ruff check --isolated --select E4,E7,E9,F,I MachineLearning/social_nlp.py Dashboard/app.py scripts tests/nlp
.venv-nlp/bin/python -m ruff format --isolated --check MachineLearning/social_nlp.py Dashboard/app.py scripts tests/nlp
.venv-nlp/bin/python -m scripts.verify_dashboard_data
```

Tes mencakup jumlah topik akhir, Ward berbobot kalimat, asal ID DBSCAN, kecocokan input/model untuk reuse embedding, kelompok sintetis, zero-distance DBSCAN, core/noise semantics, memory
guard, pembanding coherence pada korpus terkendali, gate c_v, istilah tidak valid, empat Parquet, checksum, v1/v2, penjelasan legacy dan lima tampilan UI tanpa
training. Retrain data asli memakai embedding SBERT native terverifikasi dari run sebelumnya. Metrik internal
tidak membuktikan koherensi manusia setiap label atau cakupan sosial yang lengkap.

Tidak ada database atau migrasi. Konfigurasi Coolify dan Docker produksi tidak
diubah. Image dashboard membaca mount artifact read-only; Docker build/runtime lokal sudah diverifikasi: image `beesense-nlp:main`, container
`beesense-dashboard`, health `healthy`, user 10001, mount artifact read-only dan http://127.0.0.1:8501.
Tes NLP/UI, merge dan verifikasi sumber lulus; kelima tampilan juga diuji dengan run 20 topik asli.

Referensi primer: [SBERT](https://sbert.net/),
[model card](https://huggingface.co/sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2),
[DBSCAN](https://scikit-learn.org/stable/modules/generated/sklearn.cluster.DBSCAN.html).

[Metodologi Obsidian](<../../graphify-out/obsidian/Metodologi Machine Learning Social NLP.md>).

## Tahap Gemini setelah clustering

Versi 2.4 menyimpan bobot istilah c-TF-IDF dan menambahkan tahap ringkasan Gemini opsional setelah gate 20 topik/c_v ≥0,4. Sepuluh keyword berbobot tertinggi per topik menghasilkan satu kalimat topik dan deskripsi bahasa Indonesia; CSV ber-checksum menjadi masukan dashboard. Lihat [konfigurasi, provenance dan validasi](GEMINI_TOPIC_NARRATIVES.md). Hasil model Instagram baru masih menunggu pipeline; angka aktif di atas merupakan snapshot historis.
