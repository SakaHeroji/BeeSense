# BeeSense

Clustering dan penelusuran percakapan YouTube/Reddit melalui dashboard Streamlit. SocialCrawler, class NLP, dan class UI terpisah. Dashboard membaca hasil clustering tersimpan sehingga dapat dibuka tanpa crawling, login Reddit, download model, atau training ulang.

## Menjalankan dashboard

Python **3.12** direkomendasikan; runtime dashboard juga mendukung **3.14**. Dari root proyek:

```bash
python3.12 -m venv .venv-nlp
source .venv-nlp/bin/activate
python -m pip install -r requirements.txt
python -m scripts.verify_dashboard_data
python -m streamlit run main.py --server.address=127.0.0.1 --server.port=8501
```

Buka **http://127.0.0.1:8501**. Environment lokal yang sudah ada dapat langsung dipakai melalui `.venv-nlp/bin/python`. Di Windows gunakan `.venv-nlp\Scripts\activate`; runner browser Reddit memerlukan host POSIX karena memakai `fcntl`.

Dashboard mempunyai lima tampilan: Ringkasan, Peta topik, Penjelasan topik, Kalimat & sumber, serta Metode & data. Filter tanggal/platform/kata dan pilihan topik disimpan dalam URL. Saat hasil pencarian menyusut, batas slider peta mengikuti jumlah topik yang tersedia. Penjelasan topik menampilkan card komentar/porsi/post/coherence, grafik istilah/platform/sumber, tren berpagar dukungan, dan kutipan bertautan. Lihat [desain dashboard](DASHBOARD_DESIGN.md).

## Deploy ke Streamlit Community Cloud

Entry point berada di root repository: **`main.py`**. Setelah perubahan dan dataset aktif di-commit serta di-push ke GitHub, buka [Streamlit Community Cloud](https://share.streamlit.io/) lalu pilih **Create app** dengan:

| Pengaturan | Nilai |
|---|---|
| Repository | `SakaHeroji/BeeSense` |
| Branch | `main` |
| Main file path | `main.py` |
| Advanced settings → Python version | `3.12` |

Pengaturan ini mengikuti [panduan deployment resmi Streamlit](https://docs.streamlit.io/deploy/streamlit-community-cloud/deploy-your-app/deploy). Cloud memasang dependency dari `requirements.txt` di root, yang hanya menyertakan `requirements-dashboard.txt`; keduanya harus ikut GitHub. Runtime dashboard dipisahkan dari dependency training/crawler dan diuji pada Python 3.12 serta 3.14. Lihat [aturan dependency Cloud](https://docs.streamlit.io/deploy/streamlit-community-cloud/deploy-your-app/app-dependencies).

Sertakan `main.py`, `social_nlp.py`, `social_nlp.json`, `.streamlit/config.toml`, dan **seluruh isi snapshot aktif** `outputs/nlp_20261029_combined_topics20_01/`, termasuk manifest, Parquet, JSON, dan array NumPy. `.gitignore` sudah mengizinkan file snapshot tersebut. Jalankan `python -m scripts.verify_dashboard_data --check-git` setelah staging untuk memastikan seluruh dataset yang diterbitkan masuk Git dan checksum valid. Workbook baseline/gabungan dan snapshot arsip tetap disertakan untuk audit serta CI.

Cloud memakai `output_dir` relatif pada `social_nlp.json`. Biarkan `BEESENSE_NLP_RUN_DIR` tidak diatur agar app memakai snapshot repository; `/data/nlp_run` hanya digunakan oleh container Docker lokal. Dashboard dapat dibuka tanpa secrets, API key, model download, atau training. Dockerfile tidak digunakan oleh Community Cloud.

Konfigurasi bersama tidak mengunci `server.address` ke loopback agar platform hosting dapat mengatur bind address. Perintah lokal di atas tetap memakai `--server.address=127.0.0.1`; Docker tetap menerbitkan port pada loopback host. Lihat [referensi konfigurasi Streamlit](https://docs.streamlit.io/develop/api-reference/configuration/config.toml).

### Error instalasi pada Python 3.14

Log deployment 29 Oktober 2026 memakai Python 3.14.10 dan gagal sebelum UI dimulai: ONNX Runtime 1.23.2 tidak memiliki wheel `cp314`, lalu Numba 0.61.2 menolak Python 3.14. Penyebabnya adalah root requirements lama menarik seluruh environment training dari `requirements-nlp.lock`.

Root requirements sekarang hanya memuat kebutuhan pemuatan artifact dan UI: NumPy/Pandas/PyArrow, SciPy/scikit-learn untuk penjelasan/tren, NetworkX, Plotly, Babel, OpenPyXL dan Streamlit. ONNX Runtime, Numba/llvmlite, UMAP, Torch, Gensim dan crawler tidak dipasang di Cloud. NumPy tetap 2.2.6 pada Python <3.14; Python 3.14 memakai wheel NumPy 2.3.5. Environment training terkunci tetap dipertahankan pada `requirements-nlp.lock` dan `requirements-sbert*`.

Push perubahan requirements ke `main`, lalu tunggu Cloud memasang dependency baru. Jika app berhenti pada error lama, gunakan **Reboot app**. Python 3.12 tetap pilihan yang disarankan untuk deployment baru; app Python 3.14 dapat memakai runtime dashboard baru. [Dependency dapat diperbarui pada app yang sama, sedangkan mengganti versi Python membutuhkan deploy ulang](https://docs.streamlit.io/deploy/streamlit-community-cloud/manage-your-app/upgrade-python).

Job CI `dashboard-runtime` memasang wheel saja pada Python 3.12/3.14 dan membuka kelima tampilan dari snapshot terbitan, termasuk topik terpilih. Tes juga memastikan paket training tidak terpasang/diimpor dan memblokir training selama UI berjalan:

```bash
python -m pip install --only-binary=:all: -r requirements.txt
python -m pip check
python -m unittest discover -s tests/cloud -v
```

Jalankan tes Cloud tersebut dalam environment dashboard bersih, terpisah dari `requirements-dev.txt`/training. Tidak ada retraining atau perubahan checksum dataset/model untuk perbaikan deployment ini.

## Dataset yang disertakan

Workbook gabungan, baseline asli, run 20 topik aktif dan seluruh snapshot sebelumnya dipertahankan:

| Lokasi | Fungsi |
|---|---|
| `outputs/social_20261028_01/dataset.xlsx` | Audit baseline 8 sheet, 8.449 record Contents; checksum asli tetap |
| `outputs/social_20261028_01/social_data.xlsx` | Baseline 8.449 baris; dipertahankan utuh |
| `outputs/social_20261029_combined/social_data.xlsx` | **29.099 baris**, **1.517 post**, **27.582 komentar/balasan**, tanpa ID native ganda |
| `outputs/nlp_20261029_combined_topics20_01/` | Aktif: **20 topik**, c_v **0,4720**; empat Parquet dan manifest SHA-256 |
| `outputs/nlp_20261029_topics20_01/` | Arsip 20 topik pada baseline lama, c_v 0,4143 |
| `outputs/nlp_20261028_coherence_01/` | Arsip 52 topik pada baseline lama, c_v 0,4097 |
| `outputs/nlp_20261028_sbert_dbscan_01/` | Arsip SBERT/UMAP/DBSCAN sebelum evaluasi coherence |
| `outputs/nlp_20261028_02/` | Arsip ONNX/UMAP/HDBSCAN untuk audit/kompatibilitas |

Snapshot aktif memuat **46.916 kemunculan**, **46.143 kalimat unik**, dan **25.739 komentar/balasan terwakili**. Coverage kalimat unik 87,14%; 5.933 kalimat unik tetap noise. Embedding korpus gabungan dihitung dengan SBERT native pada revision tetap, kemudian UMAP dan DBSCAN di-fit ulang dan kelompok digabung melalui Ward berbobot. Rata-rata c_v memenuhi ≥0,4, sedangkan 7/20 topik masih di bawah 0,4 secara individual. Protokol dan batas interpretasi ada di [SOCIAL_NLP.md](SOCIAL_NLP.md#coherence-c_v-dan-ambang-training).

Akuisisi 29 Oktober dibatasi tiga jam: YouTube 1.188 post tersimpan/300 qualified; Reddit 98/58. Qualified memerlukan ≥10 komentar/balasan unik. Target 1.000 qualified per platform belum tercapai. [Bundle audit hari ini](outputs/social_20261029_1000_3h/summary.json) dan segmen mentah disimpan lokal, di luar allowlist dataset dashboard. Data baru tidak bertumpang tindih dengan 50 video +181 thread baseline. [Script merge](scripts/merge_social_datasets.py) mempertahankan baris sumber dan menolak duplikasi ID; provenans lokal tersedia pada `output/combined_dataset_20261029.json`.

Pengambilan parsial dan tanggal komentar YouTube dapat berupa perkiraan. Label topik belum divalidasi manusia dan tidak mewakili seluruh percakapan platform. Skor historis pada korpus lama tidak langsung sebanding dengan skor korpus gabungan. Dua workbook baseline dan empat snapshot lama tetap memakai checksum aslinya. Path absolut pada metadata historis merupakan provenans; konfigurasi aktif memakai path relatif.

Checkpoint, profile Chrome, log dan cache model diabaikan Git. `.gitignore` mengizinkan tiga workbook yang diterbitkan dan lima snapshot NLP, serta mengabaikan file sementara Excel `~$*.xlsx`. Penjelasan topik dihitung saat dibuka; dashboard tidak melakukan training pada rerun.

## Struktur

```text
social_crawler.py / social_crawler.json   Pengambilan dan filter YouTube/Reddit
social_nlp.py / social_nlp.json           Clustering, bukti sumber dan tren deskriptif
main.py                         Class UI Streamlit
Youtube/                                Adapter YouTube dan kontrak ekspor
Reddit/                                 Adapter/runner/parser Reddit dan tes offline
outputs/                                Workbook gabungan, baseline dan snapshot NLP
scripts/verify_dashboard_data.py         Checksum dan allowlist data
tests/                                 Tes crawler, NLP dan UI
graphify-out/                          Graf kode dan catatan Obsidian yang diringkas
```

## Crawling atau training baru

Versi class berbasis Selenium tersedia di [social_crawler_selenium.py](social_crawler_selenium.py).
Lihat [panduan Selenium](SELENIUM_CRAWLER.md) dan [peta Obsidian](graphify-out/obsidian/Crawler%20Selenium.md).
Versi ini membaca JSON yang sama dan mempertahankan format kedua workbook Excel.

Untuk tooling crawler dan tes NLP lengkap pada Python 3.12, pasang `python -m pip install -r requirements-dev.txt`. `requirements.txt` hanya memasang runtime dashboard; training SBERT tetap memakai environment tersendiri di bawah. Seluruh pengaturan crawl tetap berada dalam **social_crawler.json**; opsi NLP/penjelasan di **social_nlp.json**.

```bash
# Validasi konfigurasi; tidak mengakses jaringan.
python social_crawler.py --dry-run
# Pengambilan baru, jika memang dibutuhkan:
python social_crawler.py --output-dir outputs/social_run_baru
# Atau buka hasil baru tanpa mengubah run bawaan:
python -m streamlit run main.py -- --run-dir outputs/nlp_run_baru
```

Konfigurasi crawling aktif menargetkan **1.000 post baru per platform dalam batas pengambilan 3 jam**, bergantian YouTube/Reddit. Post dari `outputs/social_20261028_01/dataset.xlsx` dikecualikan berdasarkan ID; CAPTCHA Reddit ditunggu untuk klik manual dalam Chrome yang terlihat. Progres per operasi tersedia pada `<output-dir>.progress.json`. Untuk crawl berikutnya, Reddit memiliki cooldown awal 360 detik pada HTTP 429, mengikuti Retry-After yang lebih lama dan maksimal 3 retry dalam deadline yang sama. Lihat [campaign dan batasnya](SOCIAL_CRAWLER.md#campaign-1000-post-baru-per-platform-3-jam) serta [dasar pengamatan cooldown](SOCIAL_CRAWLER.md#cooldown-http-429-untuk-crawl-berikutnya).

Untuk training SBERT native, gunakan environment tersendiri:

```bash
python3.12 -m venv .venv-sbert
.venv-sbert/bin/python -m pip install -r requirements-sbert.txt
.venv-sbert/bin/python -u social_nlp.py --output-dir outputs/nlp_run_baru
```

Mac Intel dapat memakai `requirements-sbert-macos-intel.lock` untuk versi yang diuji.
Model SBERT multilingual diunduh saat encoding baru; bobot pralatih tetap, lalu UMAP dan DBSCAN
melakukan fitting pada kalimat dataset. `target_topics: 20` kemudian menggabungkan kelompok melalui Ward berbobot jumlah kalimat; seluruh metrik dan label dihitung ulang. Cache model tidak masuk Git. Empat Parquet:
`social_data.parquet`, `sentences.parquet`, `occurrences.parquet`, `skipped.parquet`.

Untuk refitting dengan embedding tersimpan, gunakan `--reuse-embeddings-from outputs/nlp_20261029_combined_topics20_01` bersama `--coherence-baseline outputs/nlp_20261029_combined_topics20_01`. Jalur ini memverifikasi checksum, input/model dan urutan kalimat; tidak memerlukan Torch atau download model. Lihat [perintah lengkap](SOCIAL_NLP.md#pelatihan-dan-dashboard).

Reddit Playwright memerlukan Chrome dan Playwright CLI terpasang di host, atau path CLI pada konfigurasi. CAPTCHA perlu diselesaikan manual; HTTP 429 menjeda Reddit sesuai cooldown/Retry-After dan batas retry, sementara YouTube tetap berjalan. Checkpoint historis telah dibersihkan dan `import_checkpoint_dir` default kini `null`.

## Pengujian

Environment penuh Python 3.12, terpisah dari environment Cloud:

```bash
python -m pip install -r requirements-dev.txt
python -m scripts.verify_dashboard_data --check-git
python -m unittest discover -s tests/nlp -v
python -m unittest discover -s tests -p test_social_crawler.py -v
python -m unittest discover -s Reddit -p test_crawl_reddit_playwright.py -v
node --test Reddit/browser_campaign.test.mjs Reddit/browser_campaign_detail.test.mjs Reddit/public_web_post.test.mjs
python -m ruff check --isolated --select E4,E7,E9,F,I social_nlp.py main.py scripts tests/nlp tests/cloud
python -m ruff format --isolated --check social_nlp.py main.py scripts tests/nlp tests/cloud
```

Tes berjalan offline dengan fixture sintetis; validasi dataset memeriksa artifact asli yang disertakan. Workflow [GitHub Actions](.github/workflows/ci.yml) menjalankan pemeriksaan tersebut pada push/PR; hasil eksekusi jarak jauh dapat diperiksa pada tab Actions repository. Versi action mengikuti contoh resmi [checkout](https://github.com/actions/checkout) dan [setup-python](https://github.com/actions/setup-python).

## Docker

```bash
docker build -f Dockerfile.nlp -t beesense-nlp .
# Reproduksi runtime Cloud Python 3.14:
docker build --build-arg PYTHON_VERSION=3.14 -f Dockerfile.nlp -t beesense-nlp:py314 .
docker run --rm -p 127.0.0.1:8501:8501 \
  -v "$PWD/outputs/nlp_20261029_combined_topics20_01:/data/nlp_run:ro" beesense-nlp
```

Image non-root membaca artifact melalui mount read-only. Docker tidak dipakai untuk mengontrol Chrome host. Build/runtime Docker lokal sudah diverifikasi: image `beesense-nlp:main`, container `beesense-dashboard`, health `healthy`, user 10001, mount artifact read-only, melayani http://127.0.0.1:8501. Tidak ada database atau migrasi.

## Dokumentasi

- [Class crawler dan konfigurasi](SOCIAL_CRAWLER.md)
- [Clustering, evaluasi dan provenans](SOCIAL_NLP.md)
- [Metodologi ML terperinci](<graphify-out/obsidian/Metodologi Machine Learning Social NLP.md>)
- [Penjelasan serta tren topik](EXPLAINABLE_TOPICS.md)
- [Desain dashboard](DASHBOARD_DESIGN.md)
- [Graphify](graphify-out/GRAPH_REPORT.md) dan [Obsidian HOME](graphify-out/obsidian/HOME.md)

## Repository GitHub

Repository tujuan: [SakaHeroji/BeeSense](https://github.com/SakaHeroji/BeeSense), branch main. Source, dokumentasi dan allowlist dataset dilacak Git; environment lokal, cache dan profile browser diabaikan.

Untuk perubahan berikutnya, periksa diff dan verifikasi dataset/tes sebelum commit:

```bash
git status
git diff
git add <FILE_YANG_DIUBAH>
python -m scripts.verify_dashboard_data --check-git
git commit -m "Describe the change"
git push origin main
```

Status pengujian jarak jauh tersedia pada tab Actions repository. Pemeriksaan lokal tidak menggantikan hasil workflow GitHub atau build/runtime Docker.
