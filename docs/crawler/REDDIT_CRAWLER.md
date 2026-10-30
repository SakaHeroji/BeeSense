# RedditCrawler dengan Reddrix

Class `RedditCrawler` berada di [reddit_crawler.py](../../Crawler/Backend/reddit_crawler.py) sebagai pembungkus Reddit-only untuk backend Reddrix yang sekarang terintegrasi dalam [SocialCrawler](../../Crawler/Backend/social_crawler.py) **1.4.0**. Normalisasi, display adaptif, iterator dan worker subprocess hanya diimplementasikan sekali di `Crawler/Backend/social_crawler.py`. Library sumber: [Reddrix](https://github.com/Coding-Doctor-Omar/reddrix) / [PyPI](https://pypi.org/project/reddrix/), versi 1.2.14. Tidak menggunakan Reddit Data API/OAuth atau layanan berbayar.

## Konfigurasi percobaan 30 menit

[`reddit_crawler.json`](../../config/reddit_crawler.json) mempertahankan bagian Reddit dan `total_seconds` **1800**. Konfigurasi utama `config/social_crawler.json` tetap **10800 detik** untuk YouTube+Reddit; keduanya sekarang memakai `backend=reddrix` dan `reddrix.display_mode=auto`. Target tetap 1000 qualified post, minimum 10 komentar/reply unik per post, batas 4000 percobaan/6000 kandidat, 100 komentar termasuk maksimum 30 reply dan 10 reply per thread, delay antaroperasi 2 detik, timeout operasi 90 detik. Target tidak dijamin tercapai dalam 30 menit.

Rentang tanggal tetap **27 Oktober 2025 10:17 WIB sampai sebelum 27 Oktober 2026 10:17 WIB**. Include/exclude keyword dan baseline `outputs/social_20261028_01` tetap mengikuti file sumber. Ini bukan pengambilan khusus postingan hari percobaan. Baseline hanya dibaca dan tidak diubah.

## Menjalankan

```sh
python3.12 -m venv .venv-reddrix
.venv-reddrix/bin/python -m pip install -r requirements/reddrix.txt
.venv-reddrix/bin/reddrix install
.venv-reddrix/bin/python -m Crawler.Backend.reddit_crawler --dry-run
.venv-reddrix/bin/python -m Crawler.Backend.reddit_crawler --config config/reddit_crawler.json --output-dir outputs/reddit_reddrix_trial_01
```

```python
from Crawler.Backend.reddit_crawler import RedditCrawler

crawler = RedditCrawler("config/reddit_crawler.json")
report = crawler.run("outputs/reddit_reddrix_trial_02")
print(report["primary_file"], report["status"])
```

Output harus folder baru. Dependency dipisahkan dari runtime Dashboard; instalasi Reddrix memerlukan browser Camoufox, termasuk unduhan binary terpisah yang besar. `RedditCrawler` hanya menjalankan Reddit meskipun diberi konfigurasi dua platform, dan memilih backend Reddrix secara eksplisit. Untuk menjalankan keduanya gunakan `SocialCrawler`/`python -m Crawler.Backend.social_crawler`; `requirements/crawler.txt` sudah mencakup requirements-reddrix. Plan/Sources/Contents mencatat backend efektif. Konfigurasi lama yang secara eksplisit memilih Playwright hanya dioverride oleh wrapper Reddit-only; SocialCrawler tetap menghormati pemilihan backend lama yang eksplisit.

## Display adaptif macOS dan Linux

Konfigurasi default:

```json
"reddrix": {"display_mode": "auto"}
```

| Lingkungan | Hasil mode `auto` |
| --- | --- |
| macOS, termasuk yang mempunyai XQuartz/Xvfb | Native headless (`headless=True`) |
| Linux server dengan binary `Xvfb` di PATH | Virtual display (`headless="virtual"`) |
| Linux tanpa Xvfb | Native headless (`headless=True`) |
| Windows | Native headless (`headless=True`) |

Mode `headless` memaksa native headless di semua platform. Mode `virtual` mewajibkan Linux dan Xvfb; konfigurasi yang tidak didukung ditolak sebelum crawling. Pada Debian/Ubuntu, pasang `xvfb xauth` jika ingin virtual display; keduanya sudah masuk `deployment/docker/Dockerfile.crawler`. Mode headless tetap memerlukan library sistem/browser Camoufox yang sesuai.

Override melalui CLI atau class:

```sh
.venv-reddrix/bin/python -m Crawler.Backend.reddit_crawler --display-mode headless --dry-run
```

```python
crawler = RedditCrawler("config/reddit_crawler.json", display_mode="auto")
print(crawler.plan()["display"])
```

Plan menampilkan mode yang diminta dan efektif, platform, hasil deteksi Xvfb, serta alasan pemilihan. Factory Camoufox hanya diganti di modul Reddrix dalam worker terisolasi, berlaku saat sesi awal maupun refresh cookie. Stdlib `shutil` dan modul global Camoufox tidak diubah. Konfigurasi dipertahankan dalam metadata sumber untuk run berikutnya. Perubahan adapter v1.1.0 ini dibuat **setelah** percobaan 30 menit selesai; tidak memulai crawling ulang.

## Kontrak output Excel

- `social_data.xlsx`: sheet `Data`, sepuluh kolom yang sama dengan SocialCrawler, tanggal kalender WIB, teks aman dari formula Excel.
- `dataset.xlsx`: delapan sheet `Contents`, `Relations`, `KeywordHits`, `Metrics`, `Runs`, `Sources`, `TextChunks`, `Readme`, memakai fingerprint kontrak lama.
- Delapan JSONL menjaga teks penuh, `contract.json`, `manifest.json` dengan SHA256, `summary.json`, dan file progres di samping folder output.

Normalisasi memakai native ID `t3_`/`t1_`, parent/root terverifikasi, timestamp exact hanya bila timezone sumber tersedia, metric hilang tetap null, dan actor unknown. Username tidak dianggap native author ID. Teks Reddrix adalah teks render; kelengkapan tidak diklaim. Deduplikasi input/baseline dan penerbitan folder atomik memakai SocialCrawler. Hasil percobaan tidak digabung ke korpus, tidak retrain NLP, dan tidak mengganti dashboard.

## Batas adapter

Reddrix keyword search memaksa relevance; konfigurasi search_sort/new tidak dapat dijanjikan. Library tidak menyediakan pengaturan sort komentar. Query diberi `subreddit:` dan hasil dibatasi kembali secara lokal. Request internal Reddrix mempunyai jitter/retry sendiri; `delay` BeeSense berlaku antaroperasi, bukan setiap request HTTP di dalam library.

Upstream anti-bot exception tidak memberikan HTTP status atau Retry-After yang dapat dipercaya. Karena itu blocker tersebut dicatat `ACCESS_BLOCKED`, bukan ditebak sebagai HTTP429. Jika exception menyediakan 429 yang terverifikasi, cooldown coordinator memakai maksimum konfigurasi dan Retry-After, dengan maksimal 3 retry dan deadline yang sama. Browser/headless tidak menjamin bebas CAPTCHA atau rate limit. Tidak ada solver CAPTCHA; opsi stealth eksplisit false.

Setiap operasi berada dalam subprocess dengan hard deadline; record yang telah diterima dipertahankan ketika timeout. Tidak ada fallback ke crawler/API lain. Dataset kosong/parsial saat akses gagal tetap dilaporkan sebagai parsial, bukan keberhasilan crawling.

## Verifikasi dan deployment

Tes offline wrapper/adapter (16 tes): `python -m unittest discover -s tests/crawler -p test_reddit_crawler.py -v`. Cakupan meliputi field/ID lintas thread, parent/tanggal unknown, batas reply, keyword/subreddit, konfigurasi 30 menit, baseline lintas run, struktur dua workbook, formula safety, manifest/checksum, status blocker, matriks display macOS/Linux/Windows, override konfigurasi, dan factory sesi awal/refresh. Worker sintetis ditandai synthetic=true. Regresi bersama SocialCrawler/Selenium/integrasi: 57 tes, 56 lulus/1 skip, termasuk 7 tes baru jalur gabungan dan spawn worker. Startup dan cleanup browser headless macOS aktual lulus; pemilihan mode Linux diuji dengan simulasi platform/Xvfb, belum dengan server Linux aktual.

Tidak ada perubahan database/model/kontrak persisten. **No migration required.**

`deployment/docker/Dockerfile.crawler` menyiapkan worker Linux UID10001 dan kini ber-entrypoint `Crawler/Backend/social_crawler.py` untuk kedua platform. Proses satu kali, tanpa port/health endpoint; readiness diperiksa melalui dry-run dan keberadaan binary browser. Mount baseline/config read-only dan folder hasil writable untuk UID10001 saat live (siapkan direktori host dengan izin yang sesuai). Docker daemon lokal tidak aktif; build/run image belum terverifikasi. Gunakan `--config config/reddit_crawler.json` bila ingin hanya konfigurasi percobaan Reddit.

```sh
docker build -f deployment/docker/Dockerfile.crawler -t beesense-reddit-reddrix:local .
docker run --rm beesense-reddit-reddrix:local --dry-run
docker run --rm --shm-size=1g -v "$PWD/outputs/social_20261028_01:/app/outputs/social_20261028_01:ro" -v "$PWD/output/reddrix-docker:/data" beesense-reddit-reddrix:local --config config/reddit_crawler.json --output-dir /data/trial_01
```

## Hasil live

Percobaan pertama `outputs/reddit_reddrix_20261030_30m_01` selesai PARTIAL/0 post karena Reddrix 1.2.14 salah menganggap Xvfb XQuartz di macOS sebagai Linux virtual display. Perbaikan awal adapter v1.0.0 membatasi lookup Xvfb modul Reddrix pada Linux. Percobaan kedua memakai perbaikan awal tersebut dan berjalan **30 Oktober 2026 sekitar 08:52–09:22 WIB**, dengan elapsed 1801,12 detik termasuk finalisasi. Perbaikan awal kemudian diganti konfigurasi display adaptif v1.1.0 setelah run selesai; hasil berikut bukan hasil pengulangan dengan versi baru.

| Hasil run kedua | Jumlah |
| --- | ---: |
| Post baru tersimpan | 33 |
| Komentar | 359 |
| Reply | 377 |
| Total baris Excel | 769 |
| Post memenuhi minimum 10 komentar/reply unik | 25 |
| Post di bawah minimum | 8 |

Status **PARTIAL / TIME_BUDGET_EXHAUSTED**: target 1000 qualified post belum tercapai. Sebanyak 73 post dicoba; 10 kandidat baseline dilewati. Verifikasi native root ID terhadap 181 post Reddit baseline menunjukkan **0 duplikasi**, baseline tidak berubah, seluruh checksum manifest lulus, dan kedua workbook memenuhi kontrak. Tidak ada invalid row atau object key ganda. Tidak ada 429 terverifikasi yang terekspos pada run ini; ini bukan bukti bahwa semua request internal bebas throttling.

- [Excel utama](../../outputs/reddit_reddrix_20261030_30m_02/social_data.xlsx)
- [Excel audit delapan sheet](../../outputs/reddit_reddrix_20261030_30m_02/dataset.xlsx)
- [Ringkasan run](../../outputs/reddit_reddrix_20261030_30m_02/summary.json)

Log lokal `output/reddit_reddrix_20261030_30m_02.log`; progres final `outputs/reddit_reddrix_20261030_30m_02.progress.json`. Browser Camoufox v156.0.1-beta.36 terpasang dan dependency pip check lulus. Folder output lokal diabaikan Git.
