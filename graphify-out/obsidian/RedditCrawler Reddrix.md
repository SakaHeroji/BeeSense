---
type: implementation
status: implemented-live-trial-complete
tags: [beesense, reddit, reddrix, crawler, excel]
---

# RedditCrawler Reddrix

[`SocialCrawler`](../../Crawler/Backend/social_crawler.py) **1.4.0** kini memiliki backend Reddit **Reddrix 1.2.14** sebagai default. Normalisasi, iterator, display adaptif dan worker subprocess berada di Crawler/Backend/social_crawler.py. [`RedditCrawler`](../../Crawler/Backend/reddit_crawler.py) tetap subclass tipis untuk pemakaian Reddit-only, dengan implementasi bersama. Jalur: query/permalink → iterator async Reddrix → validasi native ID/root/parent → worker subprocess → seleksi/deduplikasi SocialCrawler → BundleSink → Excel/JSONL/manifest.

[[Arsitektur BeeSense]] memakai jalur gabungan YouTube yt-dlp dan Reddit Reddrix dalam satu scheduler/deadline/bundle. [[Crawler Selenium]] tetap memiliki entry point terpisah dan provenance Selenium. Backend HTML/Playwright/checkpoint lama hanya dipakai bila dipilih eksplisit; tidak ada fallback otomatis dari Reddrix. Artifact NLP/Dashboard tetap sama. [[Frontend React Crawler]] belum terhubung ke worker Reddrix.

## Konfigurasi dan output

[Konfigurasi percobaan](../../config/reddit_crawler.json) membatasi **1800 detik/30 menit**, menggunakan semua aturan Reddit dari config/social_crawler.json selain durasi dan pembatasan ke platform Reddit. [Konfigurasi utama](../../config/social_crawler.json) tetap **10800 detik/3 jam** untuk kedua platform. Keduanya kini memakai backend reddrix dan reddrix.display_mode=auto. Target 1000 qualified post dengan minimum 10 komentar unik, rentang 27 Oktober 2025 10:17 WIB sampai sebelum 27 Oktober 2026 10:17 WIB, keyword include/exclude, serta baseline [[Crawling 1000 Post Baru|social_20261028_01]] dipertahankan.

Output identik dengan SocialCrawler: `social_data.xlsx` satu sheet Data/sepuluh kolom, `dataset.xlsx` delapan sheet audit, delapan JSONL, contract.json, manifest SHA256, summary dan progres. Deduplikasi memakai native ID lintas run; artifact historis dibaca saja.

## Display adaptif

Adapter v1.1.0 menambahkan `reddrix.display_mode=auto` pada konfigurasi, serta override `--display-mode` dan argumen class. Auto memakai native headless di macOS meskipun XQuartz memasang Xvfb, virtual display di Linux dengan Xvfb, dan native headless di Linux tanpa Xvfb/Windows. Mode `headless` memaksa native; `virtual` ditolak kecuali Linux dengan Xvfb. Dockerfile Linux memasang xvfb/xauth.

Factory Camoufox khusus modul Reddrix berlaku pada sesi awal maupun refresh, tanpa mengubah stdlib/global Camoufox. Worker subprocess mempertahankan isolasi. Plan dan provenance menjelaskan mode efektif. Perubahan ini dibuat setelah run 30 menit selesai dan tidak memicu crawling ulang.

## Batas sumber

Reddrix menggunakan akses web tanpa Data API key/OAuth. Keyword search memakai relevance, sehingga konfigurasi sort pencarian tidak dijanjikan. Tidak ada sort komentar publik pada library. Internal request/retry Reddrix berbeda dari jeda antaroperasi BeeSense; deadline operasi tetap keras.

Exception anti-bot upstream tidak mengungkap status HTTP yang dapat dipercaya: dicatat ACCESS_BLOCKED, tidak ditebak sebagai 429/CAPTCHA. Jika 429 tersedia terverifikasi, coordinator tetap memakai maksimum cooldown/Retry-After, maksimal 3 retry dalam deadline sama. Tidak ada solver CAPTCHA atau proxy berbayar. Stealth eksplisit false.

Timestamp tanpa timezone tetap unknown; parent tidak tersedia tidak diasumsikan root. Username tidak diubah menjadi native ID author dan tidak ditebak peran demografisnya. Field provenance menandai reddrix_unofficial_web dan versi adapter.

## Verifikasi

16 tes adapter/exporter/display lulus; regresi SocialCrawler/Selenium/integrasi 57 tes, 56 lulus/1skip. Tujuh tes integrasi baru memeriksa dispatch Reddrix default, ekspor/provenance dua platform, baseline keduanya, dependency failure tanpa fallback, cooldown 429, validasi konfigurasi, dan spawn worker dengan fixture. Startup dan cleanup browser headless aktual macOS lulus; Linux diuji dengan matriks platform/Xvfb, belum pada server aktual. deployment/docker/Dockerfile.crawler kini ber-entrypoint Crawler/Backend/social_crawler.py, UID10001 dengan xvfb/xauth; build belum diverifikasi karena daemon lokal tidak aktif. requirements/crawler.txt menyertakan requirements/reddrix.txt, terpisah dari runtime Dashboard. No migration required.

Camoufox v156.0.1-beta.36 sudah dipasang. Run pertama PARTIAL/0 post karena bug virtual display Reddrix pada macOS. Run kedua memakai perbaikan awal v1.0.0 dan selesai 30 Oktober 2026 sekitar 08:52–09:22 WIB: **33 post, 359 komentar, 377 reply = 769 baris**. Sebanyak **25 qualified post**, 8 di bawah minimum; status PARTIAL/TIME_BUDGET_EXHAUSTED, target 1000 belum tercapai. Tidak ada crawling ulang sesudah perubahan display v1.1.0.

Integrasi SocialCrawler 1.4.0 juga tidak memulai crawling live baru. Hasil historis berikut tetap milik run sebelum integrasi.

Verifikasi checksum dan kontrak dua workbook lulus; tidak ada object key ganda atau invalid row. Root post tidak beririsan dengan 181 root baseline, dan baseline tidak berubah. Sepuluh kandidat baseline dilewati. Hasil lokal: [Excel utama](../../outputs/reddit_reddrix_20261030_30m_02/social_data.xlsx), [audit delapan sheet](../../outputs/reddit_reddrix_20261030_30m_02/dataset.xlsx). Folder hasil tidak di-commit. [Panduan](../../docs/crawler/REDDIT_CRAWLER.md) memuat konfigurasi, cara pakai, dan batas verifikasi.

[[HOME]] · [[Arsitektur BeeSense]] · [[Dataset Dashboard]]
