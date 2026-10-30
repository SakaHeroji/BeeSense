# Helper campaign Reddit

Helper ini mempertahankan parser dan alur campaign lanjutan untuk checkpoint yang disediakan pengguna. Hasil crawl, cuplikan, screenshot, profil browser dan 1.000 metadata post historis telah dibersihkan. Dataset repository dibatasi pada yang dipakai dashboard; lihat [README proyek](../../../README.md).

- browser_campaign.mjs: menyaring search card bertanggal dan menggabungkan native ID.
- browser_campaign_detail.mjs: batch capture thread publik melalui tab browser terhubung.
- rendered_thread_dom.mjs: post/komentar yang sudah termuat pada DOM.
- public_web_post.mjs dan import_public_web_sections.py: cuplikan terbatas dengan penandaan ketidakpastian; tidak dianggap semua isi/komentar thread.
- export_browser_campaign.py: mengekspor checkpoint ke kontrak delapan sheet.
- verify_browser_campaign.py: memeriksa tanggal, ID, skema, hitungan dan checksum bundle.

Helper browser terhubung membutuhkan tab dari API browser yang didukung; bukan proses crawling mandiri. Untuk alur utama gunakan SocialCrawler dan [runner Playwright](README_playwright.md). CAPTCHA, penghalang akses atau rate limit menghentikan batch. Tidak menyalin kredensial/profil browser pribadi.

Contoh dengan checkpoint milik pengguna sendiri:

```bash
python -m Crawler.Backend.Reddit.export_browser_campaign \
  --support-dir outputs/checkpoint_pribadi --output-dir outputs/reddit_export_baru
python -m Crawler.Backend.Reddit.verify_browser_campaign outputs/reddit_export_baru
```

Default eksportir membutuhkan target capture sesuai config; --dom-only mengecualikan cuplikan web, sedangkan --allow-metadata membuat preview dengan isi kosong yang eksplisit. Metadata kandidat bukan bukti isi thread telah diambil. JSONL mempertahankan native ID/provenans dan tidak menyimpulkan sentimen atau peran penulis.

Tes offline tidak membutuhkan checkpoint historis:

```bash
node --test Crawler/Backend/Reddit/browser_campaign.test.mjs Crawler/Backend/Reddit/browser_campaign_detail.test.mjs Crawler/Backend/Reddit/public_web_post.test.mjs
python -m unittest discover -s Crawler/Backend/Reddit -p test_crawl_reddit_playwright.py -v
```
