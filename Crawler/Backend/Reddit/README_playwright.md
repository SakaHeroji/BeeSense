# Runner Reddit Playwright

crawl_reddit_playwright.py memakai Chrome terpisah melalui Playwright CLI; rendered_thread_dom.mjs mengekstrak post dan komentar yang sudah termuat. Tidak memakai RSS atau token Reddit API. CAPTCHA memerlukan tindakan manual. Coordinator SocialCrawler dapat menunggu sampai platforms.reddit.captcha_wait_seconds (aktif 600 detik), mengamati halaman setiap captcha_poll_seconds (aktif 5 detik), lalu melanjutkan setelah pengguna menyelesaikannya. Chrome tetap terlihat; waktu tunggu termasuk deadline global. Runner standalone berhenti pada HTTP 429/cooldown. Coordinator SocialCrawler 1.3.0 dapat menunda Reddit 360 detik atau lebih sesuai Retry-After, dengan maksimal 3 retry per run pada konfigurasi utama; YouTube tetap berjalan dalam round robin. Lihat [kebijakan dan dasar pengamatan](../../../docs/crawler/SOCIAL_CRAWLER.md#cooldown-http-429-untuk-crawl-berikutnya). Penghalang akses lain tetap menghentikan platform.

Untuk crawl baru gunakan konfigurasi utama SocialCrawler dari root:

```bash
python -m Crawler.Backend.social_crawler --dry-run
python -m Crawler.Backend.social_crawler --output-dir outputs/social_run_baru
```

Instal Chrome dan Playwright CLI di host; executable playwright-cli yang ada pada PATH dicari lebih dulu. Field platforms.reddit.cli dapat menunjuk executable/CLI .js/wrapper .sh secara eksplisit. Dashboard tidak memerlukan dependensi browser ini. Profil runner baru disimpan di output/playwright/reddit/profile, bukan profil Chrome pribadi pengguna, dan diabaikan Git.

Runner lanjutan dapat melanjutkan campaign jika pengguna menyediakan config dan checkpoint candidates.json sendiri. Arsip checkpoint dan profil sesi historis telah dihapus; contoh berikut bukan perintah untuk melanjutkan data bawaan:

```bash
python -m Crawler.Backend.Reddit.crawl_reddit_playwright \
  --config Crawler/Backend/Reddit/config_reddit_1000.json \
  --support-dir outputs/checkpoint_pribadi --dry-run
```

Checkpoint memvalidasi ID/permalink/subreddit/tanggal dan disimpan atomik dengan kunci OS. Capture lama hanya dipakai kembali jika valid. Komentar/balasan yang belum termuat tidak diperluas; tidak ada klaim semua komentar diambil. Penghalang browser tidak membuktikan post dihapus.

Ekspor/verifikasi checkpoint yang disediakan sendiri memakai export_browser_campaign.py dan verify_browser_campaign.py; lihat [README_browser_campaign.md](README_browser_campaign.md). Tes offline:

```bash
python -m unittest discover -s Crawler/Backend/Reddit -p test_crawl_reddit_playwright.py -v
```
