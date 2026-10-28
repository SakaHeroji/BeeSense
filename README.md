# BeeSense

Clustering dan penelusuran percakapan YouTube/Reddit melalui dashboard Streamlit. SocialCrawler, class NLP, dan class UI terpisah. Dashboard membaca hasil clustering tersimpan sehingga dapat dibuka tanpa crawling, login Reddit, download model, atau training ulang.

## Menjalankan dashboard

Python **3.12**, dari root proyek:

```bash
python3.12 -m venv .venv-nlp
source .venv-nlp/bin/activate
python -m pip install -r requirements.txt
python -m scripts.verify_dashboard_data
python -m streamlit run nlp_dashboard.py --server.address=127.0.0.1 --server.port=8501
```

Buka **http://127.0.0.1:8501**. Environment lokal yang sudah ada dapat langsung dipakai melalui `.venv-nlp/bin/python`. Di Windows gunakan `.venv-nlp\Scripts\activate`; runner browser Reddit memerlukan host POSIX karena memakai `fcntl`.

Dashboard mempunyai lima tampilan: Ringkasan, Peta topik, Penjelasan topik, Kalimat & sumber, serta Metode & data. Filter tanggal/platform/kata dan pilihan topik disimpan dalam URL. Saat hasil pencarian menyusut, batas slider peta mengikuti jumlah topik yang tersedia.

## Dataset yang disertakan

Dua workbook sumber, run SBERT + UMAP + DBSCAN aktif, serta snapshot NLP sebelumnya dipertahankan:

| Lokasi | Fungsi |
|---|---|
| `outputs/social_20261028_01/dataset.xlsx` | Workbook audit lengkap, 8 sheet; 8.449 record pada Contents |
| `outputs/social_20261028_01/social_data.xlsx` | Excel sumber, satu sheet Data; 8.449 baris |
| `outputs/nlp_20261028_coherence_01/` | Run SBERT + UMAP + DBSCAN aktif dengan c_v 0,4097; sebelas artifact termasuk empat Parquet dan proyeksi UMAP, serta manifest SHA-256 |
| `outputs/nlp_20261028_sbert_dbscan_01/` | Snapshot SBERT/UMAP/DBSCAN sebelum penambahan evaluasi coherence |
| `outputs/nlp_20261028_02/` | Snapshot ONNX/UMAP/HDBSCAN sebelumnya untuk audit dan kompatibilitas |

Snapshot berisi 16.178 kemunculan kalimat, 15.878 kalimat unik, 7.944 komentar/balasan terwakili, dengan hasil topik DBSCAN pada `summary.json` run aktif. Rentang post asal 27 Oktober 2025–26 Oktober 2026. Pengambilan sumber parsial; tanggal komentar YouTube dapat berupa perkiraan. Ini bukan seluruh percakapan selama setahun dan label topik belum divalidasi manusia.

Input ringkas dan snapshot sebelumnya dipertahankan dengan checksum aslinya. Run aktif menggunakan SBERT native, reduksi UMAP dan DBSCAN Euclidean; jumlah topik berasal dari kepadatan data. Workbook audit yang ditemukan kembali ikut disimpan utuh; SHA-256 `ccfc77dc136ed8e98bce5c2c11d6243d22ff9e2a3082d9e299847b8b5aec74b3`. Sheet auditnya adalah Contents, Relations, KeywordHits, Metrics, Runs, Sources, TextChunks dan Readme. Input NLP tetap `social_data.xlsx`; penambahan workbook audit tidak menjalankan training ulang. Path absolut dalam metadata historis adalah provenans, bukan syarat lokasi instalasi. Konfigurasi aktif memakai path relatif. Penjelasan topik dihitung saat dibuka dari artifact tersebut; file ekspor penjelasan lama tidak diperlukan.

Checkpoint crawler, profile Chrome, screenshot, log percobaan dan cache model tidak disertakan. `.gitignore` memakai allowlist kedua workbook dan tiga run NLP tersebut; run lain secara default diabaikan Git. File kunci Excel sementara (`~$*.xlsx`) diabaikan oleh verifier dan Git. Fixture HTML kecil di `Reddit/fixtures` adalah data sintetis untuk pengujian parser.

Coherence c_v rata-rata **0,4097** memenuhi ambang **0,4** pada retrain terbaru;
31 dari 52 topik masih di bawah 0,4 secara individual. Protokol dan batas interpretasi
ada di [SOCIAL_NLP.md](SOCIAL_NLP.md#coherence-c_v-dan-ambang-training).

## Struktur

```text
social_crawler.py / social_crawler.json   Pengambilan dan filter YouTube/Reddit
social_nlp.py / social_nlp.json           Clustering, bukti sumber dan tren deskriptif
nlp_dashboard.py                         Class UI Streamlit
Youtube/                                Adapter YouTube dan kontrak ekspor
Reddit/                                 Adapter/runner/parser Reddit dan tes offline
outputs/                                Dua workbook sumber dan run NLP berversi
scripts/verify_dashboard_data.py         Checksum dan allowlist data
tests/                                 Tes crawler, NLP dan UI
graphify-out/                          Graf kode dan catatan Obsidian yang diringkas
```

## Crawling atau training baru

Versi class berbasis Selenium tersedia di [social_crawler_selenium.py](social_crawler_selenium.py).
Lihat [panduan Selenium](SELENIUM_CRAWLER.md) dan [peta Obsidian](graphify-out/obsidian/Crawler%20Selenium.md).
Versi ini membaca JSON yang sama dan mempertahankan format kedua workbook Excel.

Instalasi `requirements.txt` mencakup dependensi NLP dan crawler. Seluruh pengaturan crawl tetap berada dalam **social_crawler.json**; opsi NLP/penjelasan di **social_nlp.json**.

```bash
# Validasi konfigurasi; tidak mengakses jaringan.
python social_crawler.py --dry-run
# Pengambilan baru, jika memang dibutuhkan:
python social_crawler.py --output-dir outputs/social_run_baru
# Atau buka hasil baru tanpa mengubah run bawaan:
python -m streamlit run nlp_dashboard.py -- --run-dir outputs/nlp_run_baru
```

Untuk training SBERT native, gunakan environment tersendiri:

```bash
python3.12 -m venv .venv-sbert
.venv-sbert/bin/python -m pip install -r requirements-sbert.txt
.venv-sbert/bin/python -u social_nlp.py --output-dir outputs/nlp_run_baru
```

Mac Intel dapat memakai `requirements-sbert-macos-intel.lock` untuk versi yang diuji.
Model SBERT multilingual diunduh saat encoding baru; bobot pralatih tetap, lalu UMAP dan DBSCAN
melakukan fitting pada kalimat dataset. Cache model tidak masuk Git. Empat Parquet:
`social_data.parquet`, `sentences.parquet`, `occurrences.parquet`, `skipped.parquet`.
 Reddit Playwright memerlukan Chrome dan Playwright CLI terpasang di host, atau path CLI pada konfigurasi. CAPTCHA perlu diselesaikan manual; rate limit menghentikan pengambilan. Checkpoint historis telah dibersihkan dan `import_checkpoint_dir` default kini `null`.

## Pengujian

```bash
python -m scripts.verify_dashboard_data --check-git
python -m unittest discover -s tests/nlp -v
python -m unittest discover -s tests -p test_social_crawler.py -v
python -m unittest discover -s Reddit -p test_crawl_reddit_playwright.py -v
node --test Reddit/browser_campaign.test.mjs Reddit/browser_campaign_detail.test.mjs Reddit/public_web_post.test.mjs
python -m ruff check --isolated --select E4,E7,E9,F,I social_nlp.py nlp_dashboard.py scripts tests/nlp
python -m ruff format --isolated --check social_nlp.py nlp_dashboard.py scripts tests/nlp
```

Tes berjalan offline dengan fixture sintetis; validasi dataset memeriksa artifact asli yang disertakan. Workflow [GitHub Actions](.github/workflows/ci.yml) menjalankan pemeriksaan tersebut pada push/PR; hasil eksekusi jarak jauh dapat diperiksa pada tab Actions repository. Versi action mengikuti contoh resmi [checkout](https://github.com/actions/checkout) dan [setup-python](https://github.com/actions/setup-python).

## Docker

```bash
docker build -f Dockerfile.nlp -t beesense-nlp .
docker run --rm -p 127.0.0.1:8501:8501 \
  -v "$PWD/outputs/nlp_20261028_coherence_01:/data/nlp_run:ro" beesense-nlp
```

Image non-root membaca artifact melalui mount read-only. Docker tidak dipakai untuk mengontrol Chrome host. Build/runtime Docker belum diverifikasi pada mesin persiapan karena daemon belum aktif. Tidak ada database atau migrasi.

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
python -m scripts.verify_dashboard_data --check-git
git add <FILE_YANG_DIUBAH>
git commit -m "Describe the change"
git push origin main
```

Status pengujian jarak jauh tersedia pada tab Actions repository. Pemeriksaan lokal tidak menggantikan hasil workflow GitHub atau build/runtime Docker.
