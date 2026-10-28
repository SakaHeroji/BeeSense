# SocialCrawler

[SocialCrawler](social_crawler.py) menggabungkan adapter [YouTube](Youtube/crawl_youtube.py) dan [Reddit](Reddit/crawl_reddit_single.py). Konfigurasi gabungannya berada dalam satu [social_crawler.json](social_crawler.json). Tidak memerlukan peta Obsidian untuk mengeksekusi crawler.

## Pemakaian

```bash
python -m pip install -r requirements-crawler.txt
python social_crawler.py --dry-run
python social_crawler.py --output-dir outputs/social_run_baru
```

Dry-run memvalidasi konfigurasi tanpa request. Konstruktor menerima path JSON atau dictionary; `plan()` menyusun rencana dan `run()` mengeksekusi. Gunakan guard __main__ untuk pemanggilan Python karena worker memakai multiprocessing spawn. Output yang sudah ada tidak ditimpa; run baru otomatis diabaikan Git.

```python
from social_crawler import SocialCrawler

if __name__ == "__main__":
    report = SocialCrawler("social_crawler.json").run("outputs/social_run_baru")
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
| min_posts | Minimum root yang memenuhi filter dan minimum komentar; video untuk YouTube |
| min_comments_per_post | Minimum komentar unik termasuk balasan agar root memenuhi target |
| max_posts / max_candidates | Batas pemeriksaan root dan penemuan permalink |
| max_comments / max_replies | Batas pengambilan komentar/balasan per root |

Jeda berlaku antar operasi, bukan setiap subrequest di dalam yt-dlp/browser. Minimum bukan jaminan hasil; pengambilan dapat berhenti parsial karena waktu, sumber, akses, CAPTCHA atau HTTP 429. Exclude menang atas include. Komentar tidak diwajibkan memuat include agar konteks tetap tersedia. Literal matcher bukan klasifikasi semantik semua konten politik.

Exclude proyek mencakup MBG/makan bergizi gratis, kopdes/koperasi desa merah putih, ijazah Jokowi/Gibran, DPR serta variasi dalam JSON. Root bertanggal tidak pasti dikeluarkan jika filter tanggal aktif; komentar bertanggal perkiraan masih bisa menjadi konteks. Balasan dapat mempertahankan unresolved_reference bila induknya dibuang oleh filter.

## Output

Output utama social_data.xlsx memiliki satu sheet Data: platform, jenis, judul_post, tanggal_post_wib, akurasi_tanggal_post, tanggal_konten_wib, akurasi_tanggal_konten, teks, url, teks_dipotong. Tanggal kalender WIB dibedakan pasti/perkiraan/tanggal_saja/tidak_diketahui. Estimasi waktu relatif mengacu pada observed_at sumber, bukan tanggal ekspor ulang.

Bundle crawl baru juga memuat JSONL audit, dataset.xlsx dan manifest. `export_compact(bundle_dir, output_dir)` atau `--from-bundle` dapat mengekspor ulang bundle yang disediakan sendiri setelah checksum/kontrak diverifikasi. Bundle historis tidak disertakan; satu Excel dan satu run NLP untuk dashboard dipertahankan sesuai README.

Target, kekurangan minimum dan alasan berhenti tersedia dalam summary.json. TARGET_MET tidak berarti semua komentar thread telah diambil. Exit 0 untuk dry-run/target terpenuhi, 2 untuk parsial/kesalahan, 130 untuk interupsi.

## Reddit

Backend html memakai halaman publik; playwright memakai Chrome host dan Playwright CLI; checkpoint memerlukan checkpoint milik pengguna sendiri. import_checkpoint_dir default null karena checkpoint historis telah dibersihkan. Profil browser dan capture baru berada di output/ dan diabaikan Git. Penghalang akses menghentikan crawler; CAPTCHA dilakukan manual dan cooldown dipatuhi.

[README_playwright.md](Reddit/README_playwright.md) menjelaskan runner. Helper [browser campaign](Reddit/README_browser_campaign.md) tetap tersedia untuk alur lanjutan dan parser offline. Dashboard tidak memerlukan browser/CLI tersebut.

## Verifikasi

```bash
python -m unittest discover -s tests -p test_social_crawler.py -v
python -m unittest discover -s Reddit -p test_crawl_reddit_playwright.py -v
python Reddit/crawl_reddit_single.py self-test
node --test Reddit/browser_campaign.test.mjs Reddit/browser_campaign_detail.test.mjs Reddit/public_web_post.test.mjs
```

Fixture tes sintetis, tidak dimasukkan ke hasil nyata. Tidak ada migrasi database. Dockerfile NLP tidak menjalankan crawler Chrome host.
