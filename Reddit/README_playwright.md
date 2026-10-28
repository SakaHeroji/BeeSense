# Runner Reddit Playwright

crawl_reddit_playwright.py memakai Chrome terpisah melalui Playwright CLI; rendered_thread_dom.mjs mengekstrak post dan komentar yang sudah termuat. Tidak memakai RSS atau token Reddit API. CAPTCHA memerlukan tindakan manual; HTTP 429/cooldown dan penghalang akses menghentikan pengambilan.

Untuk crawl baru gunakan konfigurasi utama SocialCrawler dari root:

```bash
python social_crawler.py --dry-run
python social_crawler.py --output-dir outputs/social_run_baru
```

Instal Chrome dan Playwright CLI di host; executable playwright-cli yang ada pada PATH dicari lebih dulu. Field platforms.reddit.cli dapat menunjuk executable/CLI .js/wrapper .sh secara eksplisit. Dashboard tidak memerlukan dependensi browser ini. Profil runner baru disimpan di output/playwright/reddit/profile, bukan profil Chrome pribadi pengguna, dan diabaikan Git.

Runner lanjutan dapat melanjutkan campaign jika pengguna menyediakan config dan checkpoint candidates.json sendiri. Arsip checkpoint dan profil sesi historis telah dihapus; contoh berikut bukan perintah untuk melanjutkan data bawaan:

```bash
python Reddit/crawl_reddit_playwright.py \
  --config Reddit/config_reddit_1000.json \
  --support-dir outputs/checkpoint_pribadi --dry-run
```

Checkpoint memvalidasi ID/permalink/subreddit/tanggal dan disimpan atomik dengan kunci OS. Capture lama hanya dipakai kembali jika valid. Komentar/balasan yang belum termuat tidak diperluas; tidak ada klaim semua komentar diambil. Penghalang browser tidak membuktikan post dihapus.

Ekspor/verifikasi checkpoint yang disediakan sendiri memakai export_browser_campaign.py dan verify_browser_campaign.py; lihat [README_browser_campaign.md](README_browser_campaign.md). Tes offline:

```bash
python -m unittest discover -s Reddit -p test_crawl_reddit_playwright.py -v
```
