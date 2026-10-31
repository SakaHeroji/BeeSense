# TwitterCrawler — Scweet

`Crawler/Backend/twitter_crawler.py` menyediakan class Python `TwitterCrawler` untuk percobaan Twitter/X secara terpisah. Akuisisi memakai **Scweet 5.8.2**, sedangkan filter, kontrak record, relasi, checksum dan Excel memakai komponen BeeSense yang sudah ada. Class ini belum dimasukkan ke `SocialCrawler` atau dashboard.

## Menjalankan dari root repository

```sh
python3 -m venv .venv-twitter
.venv-twitter/bin/python -m pip install -r requirements/twitter.txt
.venv-twitter/bin/python -m Crawler.Backend.twitter_crawler --dry-run
.venv-twitter/bin/python -m Crawler.Backend.twitter_crawler \
  --config config/twitter_crawler.json \
  --output-dir outputs/twitter_scweet_trial_baru
```

Nama direktori output harus baru. `--dry-run` memvalidasi konfigurasi tanpa membaca kredensial atau menghubungi X.

```python
from Crawler.Backend.twitter_crawler import TwitterCrawler

crawler = TwitterCrawler("config/twitter_crawler.json")
summary = crawler.run("outputs/twitter_scweet_trial_baru")
```

## Konfigurasi dan autentikasi

Preset `config/twitter_crawler.json` mengatur batas **1.800 detik / 30 menit**, target percobaan **1.000 post**, maksimal **10 komentar/balasan per post**, 20 hasil per pencarian, query pendidikan yang sama dengan preset Reddit, bahasa Indonesia, serta filter include/exclude dan tanggal publikasi root. Pencarian membagi periode menjadi jendela tujuh hari dari yang terbaru; timestamp UTC lokal diperiksa kembali setelah hasil diterima. Batas `until` eksklusif. Target merupakan batas/tujuan percobaan, bukan jaminan hasil; proses dapat selesai lebih awal jika akses ditolak atau kandidat habis.

`scweet.auth_file` menunjuk `config/auth.json`, yang tetap diabaikan Git. Loader memilih tepat satu entri `sosmed: twitter` (alias `x` didukung), membaca `username`, lalu memetakan **`auth_token` atau `sessionid` → cookie X `auth_token`**. `ct0` opsional; Scweet dapat mengambilnya dari sesi. Tidak ada login password otomatis, token di argumen terminal, penyalinan rahasia ke konfigurasi publik, atau pencatatan nilai cookie.

State Scweet (`output/scweet/state.db`, file SQLite WAL/SHM, identitas lokal dan barrier) mengandung materi autentikasi dan tetap di luar Git maupun image Docker. Direktori dibuat dengan izin 0700 dan file baru 0600. Satu worker persisten menggunakan satu client sepanjang run. Saat state sudah ada, provisioning tidak diulang sehingga counter harian, lease dan cooldown upstream dipertahankan. State yang berbeda dari kredensial lokal ditolak untuk mencegah pemakaian akun lain secara tidak sengaja.

Preset membatasi satu concurrency, minimum 5 detik antar-request curl, 15 detik antar-operasi, serta mengonfigurasi limiter Scweet menjadi 20 request per jendela 900 detik dan 120 request per hari. Limiter window Scweet diinisialisasi per operasi; angka 20 tersebut bukan batas global lintas-operasi. Counter harian dan cooldown akun disimpan dalam SQLite. Ini pengaturan konservatif, **bukan jaminan bebas HTTP 429**. Bootstrap/manifest memakai request tambahan; deadline keseluruhan tetap berlaku. Tidak ada pergantian akun, proxy atau identitas otomatis.

Versi adapter 1.0.1 membedakan **cooldown pool Scweet** dari respons HTTP429. Scweet dapat mengistirahatkan akun berdasarkan header rate limit meski respons terakhir HTTP200; jika diagnosis pool hanya `cooldown` dan waktu tunggunya masih muat dalam anggaran run, scheduler menunggu lalu mengulang operasi yang sama dengan client/state yang sama. Akun tidak dirotasi, counter tidak direset, dan cap harian tetap terminal. Cooldown yang sudah ada diperiksa sebelum manifest di-refresh. HTTP429 yang benar-benar diterima transport tetap menghentikan run dan tidak dicoba ulang otomatis.

HTTP 429, login, challenge, atau penolakan 400/403 dicatat sebagai barrier. Transport menolak request berikutnya dalam worker yang sama, dan scheduler menghentikan run sambil menyimpan hasil sebelumnya. Retry-After/reset rate limit dipertimbangkan pada `barrier.json`, dengan jeda minimal 900 detik untuk 429. Barrier login/challenge membutuhkan penanganan manual dan tidak dibersihkan otomatis. Timeout operasi menghentikan subprocess milik crawler; Chrome pengguna tidak dibuka/ditutup oleh class ini.

## Output Excel dan audit

- **`social_data.xlsx`**: satu sheet `Data`, sepuluh kolom identik dengan crawler lain: `platform`, `jenis`, `judul_post`, `tanggal_post_wib`, `akurasi_tanggal_post`, `tanggal_konten_wib`, `akurasi_tanggal_konten`, `teks`, `url`, `teks_dipotong`.
- **`dataset.xlsx`**: delapan sheet audit kontrak bersama (`Contents`, `Relations`, `KeywordHits`, `Metrics`, `Runs`, `Sources`, `TextChunks`, `Readme`).
- JSONL per tabel, `contract.json`, `manifest.json` dengan checksum, dan `summary.json`.
- `<output-dir>.progress.json`: snapshot progres di sebelah folder hasil, diperbarui setiap operasi. Proses ekspor memakai staging atomik sehingga folder final muncul setelah penyimpanan selesai.

`platform=twitter`, namespace `x_post`, dan native tweet ID disimpan sebagai string. URL X/Twitter dinormalisasi ke `https://x.com/i/web/status/<id>` dan harus cocok dengan ID. Seluruh record dideduplikasi berdasarkan native ID meski teks berubah. `exclude_existing_datasets` dapat menunjuk bundle audit sebelumnya atau file `Contents.jsonl` untuk pengecualian lintas-run; input historis tidak diubah. Pengecualian belum memakai workbook ringkas karena file itu tidak menyimpan kolom native ID.

Post balasan/retweet dari pencarian tidak dijadikan root mandiri. Komentar langsung memakai native `in_reply_to_tweet_id`; balasan bertingkat mempertahankan parent aslinya. Parent yang tidak ikut terambil tidak dianggap pasti ada dalam ekspor. Jumlah komentar dibatasi, bukan cakupan lengkap. Teks lengkap/truncation tidak dijamin oleh curated schema Scweet sehingga audit menandai `text_complete=false`; teks panjang tetap disimpan utuh di JSONL/TextChunks. Excel memakai sel teks untuk mencegah formula injection.

`trial_passed`, `live_access_verified`, jumlah hasil, status barrier dan stop reason dibedakan dari pengujian sintetis. Sukses uji akses tidak berarti target 1.000 post tercapai atau seluruh komentar berhasil dibaca.

## Verifikasi dan Docker

```sh
.venv-twitter/bin/python -m unittest discover -s tests/crawler -p test_twitter_crawler.py -v
docker build -f deployment/docker/Dockerfile.twitter -t beesense-twitter:local .
docker run --rm beesense-twitter:local --dry-run
```

Image berjalan sebagai UID 10001. Mount `config/auth.json` secara read-only dan direktori state/output yang dapat ditulis saat menjalankan crawl live; keduanya tidak dimasukkan ke image. Tidak ada perubahan skema database aplikasi atau migrasi yang diperlukan. SQLite internal Scweet adalah cache baru milik library dan dibuat olehnya.

## Hasil uji live — 31 Oktober 2026

Percobaan berjalan dalam jendela sekitar **30 menit**, termasuk diagnosis cooldown dan pembaruan/resume adapter. Dua run akuisisi menghabiskan total sekitar **27 menit**; ini bukan klaim 30 menit request kontinu. Hanya Twitter/X yang diakses.

- Batch `outputs/twitter_scweet_20261031_30m_01/` (adapter 1.0.0): 864,74 detik, **19 post, 10 komentar, 1 balasan**. Berhenti `ACCOUNT_UNAVAILABLE`; state Scweet menunjukkan cooldown rate limit dengan kode internal 429, sedangkan seluruh **65 respons HTTP tercatat 200**.
- Batch `outputs/twitter_scweet_20261031_30m_02/` (adapter 1.0.1): memakai sisa jendela 755 detik, **14 post baru dan 1 komentar**, berhenti `TIME_BUDGET_EXHAUSTED`. Seluruh **59 respons HTTP tercatat 200**. State akun dan counter dipertahankan; semua ID batch pertama menjadi baseline pengecualian. Resume live dimulai setelah cooldown berakhir; mekanisme tunggu cooldown otomatis adapter 1.0.1 diverifikasi dengan pengujian offline, tidak terpicu lagi pada batch kedua.
- Total **33 post, 11 komentar, 1 balasan = 45 record unik**; **0 duplikasi native ID, 0 parent unresolved, 0 relasi parent lintas-root**. Tidak ada respons HTTP429 yang teramati. Satu event sumber batch pertama tidak lolos validasi dan tidak diekspor. Target percobaan **1.000 post belum tercapai**.

Workbook gabungan: **`outputs/twitter_scweet_20261031_30m_combined/social_data.xlsx`**. Folder ini adalah proyeksi ringkas dari dua bundle audit yang diverifikasi, dilengkapi `Contents.jsonl`, `merge_report.json` dan checksum manifest. Delapan tabel lengkap serta `dataset.xlsx` tetap berada di masing-masing folder batch sumber; provenance run/observation asli dipertahankan.

Verifikasi: **17 pengujian TwitterCrawler PASS**; regresi SocialCrawler **71 pengujian, 70 PASS/1 optional SKIP**. Header dua format Excel, seluruh row kontrak JSONL, seluruh checksum sumber, sel formula dan ketiadaan materi cookie lokal dalam ekspor diperiksa. `pip check`, Ruff check/format dan build-context allowlist Moby lulus; dry-run dari context terisolasi lulus. Tidak perlu migrasi database aplikasi. Build/start Docker belum diverifikasi karena daemon Docker lokal tidak aktif.

Referensi primer: [Scweet quickstart](https://altimis.github.io/Scweet/), [dokumentasi API dan konfigurasi](https://github.com/Altimis/Scweet/blob/master/DOCUMENTATION.md), [changelog 5.8.2](https://altimis.github.io/Scweet/changelog/).
