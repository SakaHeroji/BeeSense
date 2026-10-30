# SocialCrawler

[SocialCrawler](../../Crawler/Backend/social_crawler.py) menggabungkan YouTube melalui yt-dlp dan Reddit melalui **Reddrix 1.2.14**. Normalisasi, factory browser adaptif, worker Reddrix dan coordinator berada di `Crawler/Backend/social_crawler.py`; kontrak serta exporter audit tetap memakai [modul Reddit](../../Crawler/Backend/Reddit/crawl_reddit_single.py). Konfigurasi gabungannya berada dalam satu [social_crawler.json](../../config/social_crawler.json). Tidak memerlukan peta Obsidian untuk mengeksekusi crawler.

## Pemakaian

```bash
python -m pip install -r requirements/crawler.txt
reddrix install
python -m Crawler.Backend.social_crawler --dry-run
python -m Crawler.Backend.social_crawler --output-dir outputs/social_run_baru
```

Dry-run memvalidasi konfigurasi tanpa request. Konstruktor menerima path JSON atau dictionary; `plan()` menyusun rencana dan `run()` mengeksekusi. Gunakan guard __main__ untuk pemanggilan Python karena worker memakai multiprocessing spawn. Output yang sudah ada tidak ditimpa; run baru otomatis diabaikan Git.

```python
from Crawler.Backend.social_crawler import SocialCrawler

if __name__ == "__main__":
    report = SocialCrawler("config/social_crawler.json").run("outputs/social_run_baru")
    print(report["status"])
```

## Pengaturan utama

| Field | Makna |
|---|---|
| since / until | Waktu ISO dengan timezone; awal inklusif, akhir eksklusif |
| include_keywords / include_mode | Kata/frasa literal pada root post/video; any atau all |
| exclude_keywords | Buang root beserta threadnya atau komentar yang cocok |
| delay | Fixed seconds atau random min_seconds/max_seconds |
| timeout_seconds / total_seconds | Batas operasi dan keseluruhan run |
| platforms | YouTube/Reddit aktif, query/URL, target minimum dan batas maksimum |
| platform_execution | sequential atau round_robin; bergantian satu operasi per platform dengan satu deadline bersama |
| exclude_existing_datasets | Daftar direktori dataset atau workbook audit dataset.xlsx untuk pengecualian identitas post lama |
| min_posts | Minimum root yang memenuhi filter dan minimum komentar; video untuk YouTube |
| min_comments_per_post | Minimum komentar unik termasuk balasan agar root memenuhi target |
| max_posts / max_candidates | Batas pemeriksaan root dan penemuan permalink |
| max_comments / max_replies | Batas pengambilan komentar/balasan per root |
| platforms.reddit.backend | Default `reddrix`; `html`, `playwright`, dan `checkpoint` tersedia bila dipilih eksplisit |
| reddrix.display_mode | `auto`, `headless`, atau `virtual`; dapat di-override dengan `--display-mode` atau argumen class |

Jeda berlaku antar operasi, bukan setiap subrequest di dalam yt-dlp/browser. Minimum bukan jaminan hasil; pengambilan dapat berhenti parsial karena waktu, sumber, akses, CAPTCHA atau HTTP 429. Exclude menang atas include. Komentar tidak diwajibkan memuat include agar konteks tetap tersedia. Literal matcher bukan klasifikasi semantik semua konten politik.

Exclude proyek mencakup MBG/makan bergizi gratis, kopdes/koperasi desa merah putih, ijazah Jokowi/Gibran, DPR serta variasi dalam JSON. Root bertanggal tidak pasti dikeluarkan jika filter tanggal aktif; komentar bertanggal perkiraan masih bisa menjadi konteks. Balasan dapat mempertahankan unresolved_reference bila induknya dibuang oleh filter.

## Campaign 1.000 post baru per platform, 3 jam

Konfigurasi aktif memakai `total_seconds: 10800`, `timeout_seconds: 90` dan
`platform_execution: round_robin`. YouTube dan Reddit bergantian setelah setiap
operasi pencarian atau post, sehingga YouTube tidak menghabiskan seluruh waktu
sebelum Reddit mendapat giliran. Tidak ada request paralel baru. Rentang tanggal,
keyword include/exclude dan minimum 10 komentar unik per root tetap berlaku.

Masing-masing platform menargetkan `min_posts: 1000` root yang lolos filter dan
minimum komentar. `max_posts: 4000` membatasi percobaan root dan `max_candidates:
6000` membatasi penemuan permalink; keduanya bukan target ekspor. Komentar dibatasi
100, balasan 30 dan balasan per thread 10. Query diperluas menjadi 25, dengan sampai
500 hasil per pencarian YouTube atau 50 per pencarian Reddit.

`exclude_existing_datasets: ["outputs/social_20261028_01"]` membaca sheet Contents
dari dataset.xlsx secara read-only. Native ID dan canonical_url root harus cocok.
Identitas video YouTube atau ID post Reddit, bukan judul/teks, menjadi kunci;
variasi /shorts/, youtu.be atau permalink subreddit dinormalisasi. Semua post lama
beserta threadnya dilewati sebelum request; identitas hasil juga diperiksa sebelum
ekspor. Dataset referensi berisi 50 video dan 181 post Reddit. Checksum sumber dan
jumlah post lama yang dilewati dicatat dalam summary; workbook lama tidak diubah.

Pada campaign historis 29 Oktober, backend Playwright memakai Chrome dengan profil runner tersendiri dan terlihat. Ketika mendeteksi
CAPTCHA, crawler memancarkan event `captcha_required`, lalu hanya mengamati halaman
setiap 5 detik sampai 600 detik. Pengguna menyelesaikan CAPTCHA langsung di browser;
crawler tidak mengeklik challenge. Setelah challenge hilang, operasi dilanjutkan.
Waktu tunggu termasuk deadline global. HTTP 429 dapat dijeda dan dicoba kembali
sesuai konfigurasi cooldown di bawah. Blokir akses dan CAPTCHA yang belum
diselesaikan menghentikan platform terkait; hasil parsial tetap diekspor.

```bash
.venv-nlp/bin/python -m Crawler.Backend.social_crawler \
  --output-dir outputs/social_20261029_1000_3h_01
```

Progres atomik tersedia selama run pada
`outputs/social_20261029_1000_3h_01.progress.json`. Event JSON pada stdout dan file
progres memuat stage, jumlah per platform, sisa waktu dan kebutuhan CAPTCHA. Bundle
final baru dipublikasikan setelah pengambilan selesai; finalisasi Excel berlangsung
setelah deadline pengambilan. Target 1.000 bukan jaminan jika sumber membatasi akses
atau kandidat yang memenuhi filter tidak cukup. Ringkasan melaporkan kekurangan
secara eksplisit; post dengan komentar di bawah minimum dapat tetap menjadi bukti
parsial dalam bundle dan tidak menambah qualified_posts.

## Output

Output utama social_data.xlsx memiliki satu sheet Data: platform, jenis, judul_post, tanggal_post_wib, akurasi_tanggal_post, tanggal_konten_wib, akurasi_tanggal_konten, teks, url, teks_dipotong. Tanggal kalender WIB dibedakan pasti/perkiraan/tanggal_saja/tidak_diketahui. Estimasi waktu relatif mengacu pada observed_at sumber, bukan tanggal ekspor ulang.

Bundle crawl baru juga memuat JSONL audit, dataset.xlsx dan manifest. `export_compact(bundle_dir, output_dir)` atau `--from-bundle` dapat mengekspor ulang bundle yang disediakan sendiri setelah checksum/kontrak diverifikasi. Bundle historis tidak disertakan; satu Excel dan satu run NLP untuk dashboard dipertahankan sesuai README.

Target, kekurangan minimum dan alasan berhenti tersedia dalam summary.json. TARGET_MET tidak berarti semua komentar thread telah diambil. Exit 0 untuk dry-run/target terpenuhi, 2 untuk parsial/kesalahan, 130 untuk interupsi.

## Reddit

Mulai SocialCrawler **1.4.0**, backend default dan konfigurasi utama memakai **Reddrix**. `RedditCrawler` di `Crawler/Backend/reddit_crawler.py` menjadi pembungkus Reddit-only yang memakai implementasi sama, tanpa duplikasi worker. YouTube tetap yt-dlp; kedua platform berbagi batas waktu, scheduler, filter, indeks baseline, dan satu bundle Excel/JSONL. `config/social_crawler.json` tetap 10800 detik untuk kedua platform, sedangkan `config/reddit_crawler.json` tetap 1800 detik untuk percobaan Reddit saja. Integrasi ini tidak memulai crawling baru atau mengubah hasil percobaan sebelumnya.

`reddrix.display_mode: auto` memilih native headless di macOS meskipun ada XQuartz, virtual display pada Linux dengan Xvfb di PATH, dan native headless pada Linux tanpa Xvfb/Windows. Mode `headless` selalu native; `virtual` memerlukan Linux+Xvfb dan ditolak sebelum crawling bila tidak didukung. Factory Camoufox khusus modul Reddrix berlaku pada sesi awal/refresh. Plan menampilkan backend efektif dan mode display, sementara Sources/Contents mencatat provenance yang berbeda untuk yt-dlp dan Reddrix.

```bash
python -m Crawler.Backend.social_crawler --display-mode headless --dry-run
```

Reddrix memakai akses web tanpa Data API/OAuth, `stealth=False`, tanpa solver CAPTCHA atau proxy berbayar. Pencarian Reddrix memakai relevance meskipun `search_sort` disetel new; sort komentar tidak diekspos. Jeda BeeSense berlaku antaroperasi, retry internal library tetap terikat hard deadline subprocess. Exception anti-bot tanpa status tepercaya dicatat `ACCESS_BLOCKED`, bukan diasumsikan HTTP429/CAPTCHA. Hanya 429 yang terverifikasi memicu cooldown/Retry-After coordinator. Tidak ada fallback otomatis ke backend lama. `captcha_wait_seconds`/profil Chrome adalah opsi khusus backend Playwright, bukan mekanisme interaksi CAPTCHA Reddrix. Lihat [panduan Reddrix](REDDIT_CRAWLER.md).

Backend lama tetap dapat dipilih eksplisit untuk kompatibilitas: html memakai halaman publik, playwright memakai Chrome host/Playwright CLI, checkpoint memerlukan capture pengguna sendiri. `import_checkpoint_dir` default null dan ditolak bila dipadukan dengan backend Reddrix. CAPTCHA pada backend Playwright ditampilkan di Chrome headed dan ditunggu sesuai opsi manualnya. Profil/capture lokal berada di output/ dan diabaikan Git.

## Cooldown HTTP 429 untuk crawl berikutnya

Versi 1.3.0 menyediakan `platforms.reddit.rate_limit_cooldown_seconds: 360` dan
`rate_limit_max_retries: 3` pada konfigurasi utama. Jika field retry tidak diberikan,
default-nya 0 untuk mempertahankan perilaku berhenti pada pemanggil lama. Batas retry
berlaku untuk seluruh run, bukan direset setiap post.

Dasar pengamatan: operasi Reddit yang gagal terakhir selesai **29 Oktober 2026
10.36.39,685 WIB**; laporan pengguna bahwa refresh sudah berhasil diterima sekitar
**10.42.11 WIB**. Selisih **331,315 detik**, dibulatkan menjadi sekitar 332 detik.
Ini waktu sampai pemulihan dilaporkan, bukan pengukuran waktu minimum server.
Angka 360 detik (6 menit) menjadi kebijakan awal dan tidak menjamin bebas 429.
Receipt mencatat `retry_after_seconds:60`; halaman error Chrome tanpa header
menggunakan fallback 60 dari parser, sehingga angka itu bukan bukti Retry-After
server yang terkonfirmasi.

Pada 429, coordinator menyimpan receipt/event dan menunda operasi Reddit yang sama
selama `max(360, ceil(retry_after_seconds))`. Retry hanya dijadwalkan jika masih ada
anggaran retry/post/waktu. Waktu tunggu termasuk deadline global. Dalam round robin,
YouTube tetap mendapat giliran selama Reddit cooldown. Jika semua pekerjaan sedang
menunggu, scheduler tidur paling lama 30 detik per langkah. Tidak ada pergantian
profil/identitas. Blokir lain tetap menghentikan platform. Root parsial yang sudah
diekspor tidak dicoba ulang agar identitas dan hitungan ekspor tetap unik.

Progress memuat `last_rate_limited_at`, `rate_limit_cooldown_until`, `rate_limit_events`
dan `rate_limit_retries`, dengan event `rate_limit_cooldown`, `rate_limit_retry` atau
`rate_limited`. Bukti waktu dan keputusan ini dicatat di Obsidian. Atas instruksi
pengguna saat perubahan disiapkan, campaign `_03` **tidak direstart** dan tetap
menggunakan versi 1.2.0. Setelah instruksi baru sekitar 11.00 WIB untuk melanjutkan
Reddit, segmen `_03` difinalisasi dan kelanjutan `_04` memakai 1.3.0/cooldown ini.
Config: `output/crawl_20261029_1000_3h_resume04.json`; pengecualian mencakup baseline
dan seluruh segmen terdahulu, dengan sisa target 923 YouTube/974 Reddit serta
deadline awal sekitar 12.59.53 WIB. NLP tidak dijalankan ulang.

[README_playwright.md](../../Crawler/Backend/Reddit/README_playwright.md) menjelaskan runner. Helper [browser campaign](../../Crawler/Backend/Reddit/README_browser_campaign.md) tetap tersedia untuk alur lanjutan dan parser offline. Dashboard tidak memerlukan browser/CLI tersebut.

## Verifikasi

```bash
python -m unittest discover -s tests/crawler -p test_social_crawler.py -v
python -m unittest discover -s tests/crawler -p test_social_crawler_reddrix.py -v
python -m unittest discover -s tests/crawler -p test_reddit_crawler.py -v
python -m unittest discover -s Crawler/Backend/Reddit -p test_crawl_reddit_playwright.py -v
python -m Crawler.Backend.Reddit.crawl_reddit_single self-test
node --test Crawler/Backend/Reddit/browser_campaign.test.mjs Crawler/Backend/Reddit/browser_campaign_detail.test.mjs Crawler/Backend/Reddit/public_web_post.test.mjs
```

Fixture tes sintetis, tidak dimasukkan ke hasil nyata. Tes gabungan mencakup dispatch default Reddrix, satu workbook dua platform/provenance, baseline lintas platform, dependency failure tanpa fallback, retry 429, validasi display/checkpoint, serta spawn worker tanpa akses live. Regresi SocialCrawler/Selenium/integrasi: 57 tes, 56 lulus/1 skip; wrapper Reddrix: 16 lulus. **No migration required.** Dockerfile NLP tidak menjalankan crawler.

`deployment/docker/Dockerfile.crawler` sekarang menjalankan `Crawler/Backend/social_crawler.py` sebagai worker gabungan, memasang requirements-crawler (termasuk requirements-reddrix), library Camoufox, xvfb/xauth dan browser sebagai UID10001. Image satu proses tanpa port. Mount baseline/config read-only dan output writable oleh UID10001. Build/runtime Docker belum terverifikasi karena daemon lokal tidak aktif.

```bash
docker build -f deployment/docker/Dockerfile.crawler -t beesense-social-crawler:local .
docker run --rm beesense-social-crawler:local --dry-run
docker run --rm --shm-size=1g -v "$PWD/outputs/social_20261028_01:/app/outputs/social_20261028_01:ro" -v "$PWD/output/crawler-docker:/data" beesense-social-crawler:local --output-dir /data/run_01
```

## Jeda dan kelanjutan Reddit

Setelah HTTP 429 pada campaign 29 Oktober 2026 sekitar 10.09 WIB, pengguna meminta
Reddit dijeda. Platform berhenti dengan RATE_LIMITED tanpa retry otomatis. Setelah
pengguna melakukan refresh dan menyatakan Reddit bisa dibuka, platform diaktifkan
kembali (`platforms.reddit.enabled: true`). Segmen pertama disimpan sebagai bundle
INTERRUPTED sebelum menjalankan segmen `_02`; pengambilan melanjutkan sisa target
990 Reddit dan 999 YouTube, dengan sisa tenggat semula sekitar 12.59 WIB.
Konfigurasi resume ada di `output/crawl_20261029_1000_3h_resume.json`, dengan indeks
pengecualian dataset lama **dan** segmen pertama. Target utama tetap 1.000 per platform.
Descriptor campaign `output/campaign_20261029_1000_3h.json` mengikat kedua segmen
dan deadline awal. Kelanjutan ini atas instruksi pengguna, bukan retry setelah 429
secara otomatis. Jika 429 muncul lagi, platform kembali berhenti.

Ketika Reddit kembali 429 sekitar 10.20 WIB, pengguna melakukan refresh dan meminta
kelanjutan lagi. Segmen `_02` disimpan, lalu `_03` memakai sisa target 994 YouTube
dan 983 Reddit serta sisa deadline awal. Semua bundle segmen terdahulu masuk indeks
deduplikasi. Config kelanjutan: `output/crawl_20261029_1000_3h_resume03.json`.
Descriptor campaign selalu menjadi acuan segmen aktif/deadline; jalankan
`.venv-nlp/bin/python output/check_crawl_campaign.py` untuk jumlah kumulatif.

Query YouTube kini menyertakan petunjuk tanggal `after:2025-10-26 before:2026-10-28`.
Lima kandidat probe berada dalam periode, tetapi query sumber tidak dianggap bukti
kelayakan; filter timestamp coordinator tetap wajib. Resume ketiga mengambil 100
hasil per query agar variasi pencarian lebih cepat terjangkau. Target utama dan
minimum komentar tidak berubah.

Retry otomatis pada `_04` teramati berhasil setelah 362,526 detik (kebijakan 360
detik ditambah penjadwalan); pengamatan ini tidak membuktikan waktu minimum server.
Setelah batas retry run terpakai dan 429 kembali sekitar 11.49 WIB, campaign
dilanjutkan lewat `_05` sesudah cooldown sampai sekitar 11.55.30 WIB. Hasil `_04`
disimpan dan dikecualikan; target sisa 836 YouTube/943 Reddit dengan deadline awal
yang sama. Batas 3 retry berlaku per run, bukan tambahan waktu campaign. Config
kelanjutan: `output/crawl_20261029_1000_3h_resume05.json`. Browser yang masih
menampilkan error 429 pada awal proses diperlakukan sebagai barrier dan dapat
menimbulkan cooldown lagi. Status aktual harus mengikuti progress/summary.

## Menggabungkan workbook untuk NLP

`scripts/merge_social_datasets.py` menyatukan sheet Data berkolom sepuluh dengan urutan baseline terlebih dahulu, kemudian akuisisi baru. Identitas memakai ID asli video/thread/komentar, sehingga teks identik dari dua komentar berbeda tetap dipertahankan. ID berulang, komentar tanpa post induk, formula sumber, dan komentar dengan teks terpotong ditolak. Sumber diperiksa checksum sebelum/sesudah; hasil dibaca kembali sebelum dipublikasikan ke direktori versi baru. File provenans mencatat checksum sumber, rentang baris Excel, jumlah per platform/jenis, dan checksum gabungan.

```bash
.venv-nlp/bin/python scripts/merge_social_datasets.py \
  --source outputs/social_20261028_01/social_data.xlsx \
  --source outputs/social_20261029_1000_3h/social_data.xlsx \
  --output-dir outputs/social_gabungan_baru \
  --provenance output/merge_gabungan_baru.json
```

Konsolidasi segmen campaign memverifikasi manifest audit lebih dahulu. Workbook ringkas gabungan menjadi input training; bundle audit dan workbook sumber tetap terpisah. Corpus baru membutuhkan embedding baru, karena jalur reuse hanya menerima workbook/model/urutan kalimat yang identik. Tidak ada pengambilan ulang observasi saat penggabungan.

### Hasil akhir campaign 29 Oktober 2026

Pengambilan dimulai 09:59:53 WIB dan menerima sinyal berhenti pada 12:59:53 WIB. Tidak ada operasi baru yang dimulai setelah deadline; operasi terakhir yang sedang berjalan selesai sebagai INTERRUPTED pada 12:59:53,856 WIB. Publikasi workbook dilakukan sesudah pengambilan selesai.

| Platform | Post tersimpan | Memenuhi ≥10 komentar/balasan | Komentar | Balasan |
|---|---:|---:|---:|---:|
| YouTube | 1.188 | 300 | 15.006 | 3.027 |
| Reddit | 98 | 58 | 766 | 565 |

Status campaign **PARTIAL**: target 1.000 post memenuhi syarat per platform belum tercapai. Reddit menghabiskan kandidat dari kueri segmen terakhir. Seluruh lima segmen dipertahankan, termasuk root parsial; penggabungan tidak menghitung root tersebut sebagai qualified. Total terdapat 1.286 post baru dan 19.364 komentar/balasan, dengan pemeriksaan ID agar terpisah dari baseline 50 video +181 thread. Pada dua segmen versi 1.3 tercatat 7 event HTTP 429 dan 6 retry otomatis; batas retry diterapkan per run dan seluruh kelanjutan tetap memakai deadline awal.

Bundle konsolidasi berada di `outputs/social_20261029_1000_3h/`; workbook untuk analisis gabungan berada di `outputs/social_20261029_combined/social_data.xlsx`. Provenans penggabungan dicatat dalam `output/combined_dataset_20261029.json`. Perintah dan ringkasan audit lokal ini tidak mengubah workbook baseline.
