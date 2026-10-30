# SocialCrawlerSelenium

[social_crawler_selenium.py](../../Crawler/Backend/social_crawler_selenium.py) menyediakan class
`SocialCrawlerSelenium(SocialCrawler)`. Pencarian, video/post dan komentar YouTube
serta Reddit diperoleh dari halaman publik yang dirender Chrome melalui Selenium
4.51.0. Selenium Manager memilih ChromeDriver resmi yang cocok dengan Chrome lokal
([dokumentasi](https://www.selenium.dev/documentation/selenium_manager/)).

## Menjalankan

Python 3.12 dan Chrome terpasang, dari root proyek:

```bash
.venv-nlp/bin/python -m pip install -r requirements/selenium.txt
.venv-nlp/bin/python -m Crawler.Backend.social_crawler_selenium --dry-run
.venv-nlp/bin/python -m Crawler.Backend.social_crawler_selenium \
  --output-dir outputs/social_selenium_run_baru
```

Default membaca `config/social_crawler.json` yang sama, termasuk seluruh query, periode,
subreddit, keyword, target, batas komentar/balasan, jeda dan batas waktu. Field
backend/CLI/profile/checkpoint Playwright tidak dipakai. Konfigurasi yang menunjuk
`import_checkpoint_dir` ditolak agar snapshot lama tidak dikira hasil Selenium live.
Tidak ada file konfigurasi kedua yang mengubah target secara diam-diam.

Konfigurasi penuh saat implementasi menargetkan 500 root berkualifikasi per
platform, minimal 10 komentar termasuk balasan per root, jeda 2 detik, dan batas
keseluruhan 3.600 detik. Platform diproses berurutan seperti crawler lama: YouTube
lebih dahulu, lalu Reddit dengan sisa waktu global. Target bukan jaminan hasil.

Opsi `--headless` menjalankan Chrome tanpa jendela. `--chrome-binary` dan
`--driver-path` menerima executable eksplisit. `--remote-url` memakai Selenium Grid;
gunakan server milik sendiri. Tidak ada pengambilan profil pribadi, penyalinan
cookie, login otomatis, penanganan CAPTCHA atau pengabaian sertifikat TLS.

```python
from Crawler.Backend.social_crawler_selenium import SocialCrawlerSelenium

if __name__ == "__main__":
    crawler = SocialCrawlerSelenium("config/social_crawler.json", headless=True)
    report = crawler.run("outputs/social_selenium_run_baru")
    print(report["status"], report["primary_file"])
```

Guard `__main__` wajib karena setiap operasi memiliki worker `spawn` sendiri.
Sesi Chrome/profile guest terpisah per operasi, ditutup setelah selesai; supervisor
memutus worker dan turunannya saat timeout. Event yang sudah diterima tetap
dieksport. Progress operasi dicetak ke stderr; laporan akhir JSON ke stdout.
Ctrl+C menerbitkan bundle parsial, kemudian keluar dengan kode 130. Kode 0 untuk
dry-run/target terpenuhi/ekspor ulang, 2 untuk parsial atau kesalahan.

## Kontrak Excel

Exporter, pemilihan root, deduplikasi, target minimum, proteksi formula, pemecahan
teks panjang dan checksum diwarisi dari `SocialCrawler`. Satu extension hook pada
crawler lama membuat metadata sumber dapat menyebut backend yang benar.

- `social_data.xlsx`: satu sheet `Data`, sepuluh kolom dalam urutan asli:
  `platform`, `jenis`, `judul_post`, `tanggal_post_wib`, `akurasi_tanggal_post`,
  `tanggal_konten_wib`, `akurasi_tanggal_konten`, `teks`, `url`, `teks_dipotong`.
- `dataset.xlsx`: delapan sheet `Contents`, `Relations`, `KeywordHits`, `Metrics`,
  `Runs`, `Sources`, `TextChunks`, `Readme`, dengan fingerprint kontrak asli.
- JSONL audit, `contract.json`, `manifest.json` dan `summary.json` tetap tersedia.
  `extraction_method` untuk data dan sumber adalah `selenium_rendered_dom`.

Format sama tidak berarti baris atau jumlah hasilnya identik: halaman publik,
urutan komentar, reply tersembunyi dan waktu pengambilan bisa berbeda. Angka metrik
yang tidak terbaca tidak diisi nol. Timestamp relatif komentar YouTube tetap
perkiraan kalender WIB, tidak diubah menjadi waktu pasti. Root tanpa timestamp
timezone yang terverifikasi dikeluarkan saat filter tanggal aktif.

Selenium men-scroll pencarian dan komentar, serta mencoba membuka balasan YouTube
sesuai cap. Balasan Reddit yang tidak dirender tidak diperluas. Sort komentar
YouTube dicoba melalui menu UI; jika tidak bisa diverifikasi, warning disimpan.
Layout yang tidak dikenali, rate limit, CAPTCHA, login wall dan TLS error dicatat;
hambatan akses menghentikan platform. Snapshot selalu non-exhaustive.

Excel diterbitkan secara atomik setelah run berhenti; direktori tujuan yang sudah
ada tidak ditimpa. Selama berjalan, JSONL sementara berada di direktori staging
`.source-export-*` di bawah `outputs/`. Run baru diabaikan Git. Dataset dashboard
bawaan tidak diubah dan tidak ada training otomatis.

Ekspor ulang bundle terverifikasi tanpa membuka browser:

```bash
.venv-nlp/bin/python -m Crawler.Backend.social_crawler_selenium \
  --from-bundle outputs/social_selenium_run_baru \
  --output-dir outputs/social_selenium_ringkas
```

## Pengujian

```bash
.venv-nlp/bin/python -m unittest discover -s tests/crawler -p 'test_social_crawler*.py' -v
BEESENSE_TEST_SELENIUM=1 .venv-nlp/bin/python -m unittest discover \
  -s tests -p test_social_crawler_selenium.py -v
.venv-nlp/bin/python -m ruff check --isolated --select E4,E7,E9,F,I \
  Crawler/Backend/social_crawler_selenium.py tests/crawler/test_social_crawler_selenium.py
```

Suite pertama menggunakan fixture sintetis offline. Opsi environment di suite
kedua membuka Chrome asli pada fixture HTML lokal untuk menguji selector DOM dan
ID native; Selenium Manager mungkin perlu mengunduh driver. Fixture tidak masuk
ke hasil crawl live. Cakupan meliputi kedua workbook/header, checksum, formula
literal, waktu relatif, relasi balasan, identitas/subreddit, hambatan akses, timeout,
penutupan driver dan penolakan overwrite.

## Docker lokal

`deployment/docker/Dockerfile.selenium` terpisah dari image dashboard. Memerlukan BuildKit modern
untuk memakai `deployment/docker/Dockerfile.selenium.dockerignore`; context hanya berisi kode dan
kontrak yang diperlukan. Container crawler non-root memakai Selenium Grid yang
disediakan terpisah pada network Docker privat. Tidak perlu memublikasikan port
Grid. Browser Grid dan direktori output harus disediakan operator.

```bash
DOCKER_BUILDKIT=1 docker build -f deployment/docker/Dockerfile.selenium -t beesense-selenium .
docker run --rm beesense-selenium --dry-run
# Di network privat dengan service Grid bernama selenium dan volume writable:
docker run --rm --network beesense-selenium \
  -v "$PWD/outputs:/app/outputs" beesense-selenium \
  --headless --remote-url http://selenium:4444 \
  --output-dir outputs/social_selenium_container
```

Direktori mount harus writable oleh UID 10001. Pada Grid, atur batas idle sesi
agar sesi remote yang terputus oleh hard timeout dapat dibersihkan server. Build
dan runtime Docker belum diverifikasi: daemon mesin ini tidak aktif. Perintah
native Chrome telah diuji. Tidak ada perubahan konfigurasi Coolify/produksi dan
tidak perlu migrasi database.

Peta: [Obsidian](<../../graphify-out/obsidian/Crawler Selenium.md>),
[graf](../../graphify-out/graph.html), [laporan](../../graphify-out/GRAPH_REPORT.md).
