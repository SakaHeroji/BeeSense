---
type: architecture
tags: [beesense, crawler, selenium, excel]
---

# Crawler Selenium

`SocialCrawlerSelenium` dalam [social_crawler_selenium.py](../../Crawler/Backend/social_crawler_selenium.py)
mewarisi `SocialCrawler`: filter tanggal/keyword, target minimum, deduplikasi dan
exporter Excel tetap menjadi satu sumber aturan. Pencarian dan pengambilan live
kedua platform memakai Selenium, dengan Chrome guest terpisah per operasi.

Alur: konfigurasi `config/social_crawler.json` → supervisor worker → ChromeDriver →
DOM publik YouTube/Reddit → event native → kontrak `Contents`/`Relations` →
`BundleSink` → `dataset.xlsx` + `social_data.xlsx`.

Hook `_source_metadata` menghindari pelabelan Selenium sebagai yt-dlp/Playwright.
`_normalize` membentuk record YouTube; Reddit memakai adapter kontrak yang sama
dan helper [captureRenderedThread](../../Crawler/Backend/Reddit/rendered_thread_dom.mjs), dengan
fallback parser HTML lama. EXTRACTED: pewarisan dan pemanggilan ini ada dalam kode.

Supervisor lama membatasi waktu proses dan mempertahankan event parsial. Tidak ada
ID buatan untuk komentar tanpa permalink. Tanggal relatif tetap perkiraan, parent
dari nesting ditandai, metrik yang tidak tersedia tidak diisi. Hambatan akses
menghentikan platform; hasil tidak dinyatakan lengkap.

## Menjalankan konfigurasi penuh

```bash
.venv-nlp/bin/python -m pip install -r requirements/selenium.txt
.venv-nlp/bin/python -m Crawler.Backend.social_crawler_selenium --dry-run
.venv-nlp/bin/python -m Crawler.Backend.social_crawler_selenium --output-dir outputs/social_selenium_run_baru
```

Target saat implementasi: 500 root per platform, minimal 10 komentar per root,
jeda 2 detik, waktu global satu jam. YouTube mendahului Reddit. Bundle dan Excel
diterbitkan saat run berhenti; output tidak menimpa run atau dataset dashboard.

[Panduan dan tes](../../docs/crawler/SELENIUM_CRAWLER.md) · [[Arsitektur BeeSense]] ·
[[Menjalankan BeeSense]] · [[Dataset Dashboard]] · [[HOME]]
