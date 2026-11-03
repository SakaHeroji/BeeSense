# Satu konfigurasi social crawler

Semua runner memakai [`config/social_crawler.json`](../../config/social_crawler.json).
Ubah file ini untuk run berikutnya; tidak perlu membuat preset JSON per platform,
tanggal, durasi, atau resume. `schema_version: 1` menandai format universal.

## Default aktif: 1.000 post per platform

YouTube, Reddit, Instagram, Twitter dan TikTok aktif. `platform_defaults.min_posts: 1000`
berlaku untuk masing-masing platform, dengan `min_comments_per_post: 0`: post tanpa
komentar tetap dihitung. `total_seconds: null` menonaktifkan batas durasi run.
Crawler berhenti saat target terpenuhi, kandidat habis, pengguna menghentikan proses,
atau akses/sumber gagal. Target adalah tujuan akuisisi, bukan jaminan hasil.

`max_posts`, `max_candidates`, `max_comments`, `max_replies`,
`max_replies_per_thread`, `max_search_pages`, `max_searches` dan
`max_comment_threads` bernilai `null` bila tersedia: tidak ada cap jumlah lokal.
Komentar dan balasan dipaginasi sampai iterator/cursor sumber selesai. Angka
`search_results` tetap ukuran hasil per pencarian, bukan target total.
`comment_exclude_keywords: []` mempertahankan semua teks komentar, termasuk yang
mengandung kata exclude root. Filter keyword dan tanggal pada root tetap berlaku.
Isi `comment_exclude_keywords: null` untuk mewarisi exclude root seperti perilaku lama,
atau berikan daftar sendiri bila memang ingin menyaring komentar.

`scweet.daily_requests_limit` dan `scweet.daily_tweets_limit` bernilai `null`.
Adapter `scweet_limits.py` menghapus hanya predikat kuota harian dari repository
Scweet; counter tersimpan, lease, autentikasi dan cooldown tetap berlaku. Tidak
memakai angka besar sebagai pengganti unlimited. Batas window dan jeda request
mengatur pacing dan tidak dihapus. Respons HTTP429/login/challenge tetap dilaporkan.

`timeout_seconds: 90` masih melindungi pencarian dan operasi biasa; socket/request
memiliki timeout tersendiri. Operasi pagination komentar tanpa cap tidak dipotong
oleh timeout seluruh operasi, tetapi tetap tunduk pada durasi run jika diisi angka.
Backend browser/HTML hanya dapat mengekspor data yang dirender atau tersedia pada
sumber; tidak menjamin seluruh komentar tersembunyi, dihapus atau tidak dapat diakses.

## Bagian yang biasa diubah

| Bagian | Kegunaan |
| --- | --- |
| `output_root` | Direktori hasil per platform/tanggal; default `outputs/crawling`. |
| `project_id` | Nama proyek dalam audit hasil. |
| `since`, `until` | Periode publikasi root, ISO datetime dengan timezone; `until` eksklusif. |
| `include_keywords`, `exclude_keywords`, `include_mode` | Filter root bersama semua platform. |
| `comment_exclude_keywords` | `[]` mengambil semua komentar; `null` mewarisi exclude root; daftar untuk filter komentar tersendiri. |
| `queries` | Pencarian bersama YouTube, Reddit, Twitter dan TikTok. Tidak berisi tanggal yang harus diedit ulang. |
| `total_seconds`, `timeout_seconds`, `delay` | Durasi run opsional (`null` tanpa batas), timeout request/operasi, dan jeda scheduler. |
| `platform_defaults` | Target/batas bersama: `min_posts`, `min_comments_per_post`, `max_posts`, `max_candidates`, `max_comments`, `search_results`. |
| `platforms.<nama>` | Aktif/nonaktif, URL, dan override pengaturan khusus platform. |
| `exclude_existing_datasets` | Direktori bundle atau workbook lama yang ID-nya harus dilewati. |
| `reddrix`, `instaloader`, `instagrapi`, `instagram_browser`, `scweet` | Opsi adapter dan path sesi/auth dalam file yang sama. |
| `instagram_pacing` | Jeda per batch dan cooldown Instagram dalam coordinator gabungan. |

Nilai pada `platforms.<nama>` mengalahkan `platform_defaults`. Contoh: ubah
`platform_defaults.min_posts` sekali untuk target semua platform, atau tambahkan
`platforms.instagram.min_posts` untuk target Instagram yang berbeda. Daftar
`platforms.twitter.queries` menggantikan query bersama; `[]` dapat dipakai bersama
`urls` untuk crawling URL saja. Instagram memakai `hashtags`, bukan `queries`.

Tanggal diperiksa kembali terhadap timestamp hasil akuisisi. Query bersama tidak
menyimpan operator tanggal lama yang dapat bertentangan dengan `since`/`until`.
Jeda request adapter tetap berlaku selain jeda scheduler; kuota harian lokal opsional.

## Memilih platform dan menjalankan

Konfigurasi aktif mengaktifkan lima platform. Untuk Instagram saja, ubah flag dalam file:

```json
"platforms": {
  "youtube": { "enabled": false },
  "reddit": { "enabled": false },
  "instagram": { "enabled": true },
  "twitter": { "enabled": false },
  "tiktok": { "enabled": false }
}
```

Contoh tersebut hanya menunjukkan flag yang diubah; pertahankan opsi lainnya.
Periksa rencana sebelum menjalankan crawler:

```sh
python -m Crawler.Backend.social_crawler --dry-run
python -m Crawler.Backend.social_crawler
```

`total_seconds: null` adalah default tanpa batas jam. Jika ingin durasi terbatas,
set `total_seconds: 1800` untuk 30 menit atau `10800` untuk tiga jam seluruh run,
bukan per platform. Angka cap lama tetap didukung; nol bukan sinonim unlimited.
`max_replies: 0` tetap berarti tidak mengambil balasan.
Coordinator mendukung jeda fixed/random; runner Instagram/Twitter mandiri memerlukan
jeda fixed. Konfigurasi awal memakai fixed dua detik, ditambah pacing HTTP adapter.

Runner mandiri juga membaca file utama dan memilih platformnya secara eksplisit,
termasuk ketika flag platform itu nonaktif untuk run gabungan:

```sh
python -m Crawler.Backend.reddit_crawler --dry-run
python -m Crawler.Backend.instaloader_crawler --dry-run
python -m Crawler.Backend.instagram_crawler --dry-run
python -m Crawler.Backend.twitter_crawler --dry-run
```

`InstaloaderCrawler` selalu memakai Instaloader. `InstagramCrawler` mempertahankan
adapter instagrapi, atau browser jika `platforms.instagram.backend` diubah menjadi
`browser`; `SocialCrawler` mengikuti backend yang dipilih dalam file. Pengaturan
batch `instagram_pacing` hanya berlaku pada `SocialCrawler`. Semua runner mandiri
mewarisi periode, keyword, target dan durasi yang sama; tidak ada durasi trial
tersembunyi. CLI masih menerima `--config <path>` dan dictionary lama tetap didukung.

## Melanjutkan pengambilan dan file lain

Tambahkan direktori bundle run sebelumnya ke `exclude_existing_datasets`, lalu
gunakan direktori output baru. Atur target dan sisa durasi dalam file utama.
Ini akuisisi baru yang melewati ID lama, bukan pemulihan seluruh state scheduler.

Delapan preset crawler terpisah telah dihapus. Angka dan nama preset dalam catatan
campaign bertanggal adalah riwayat; konfigurasi efektif sekarang terlihat pada
`--dry-run`. Konfigurasi NLP, relevansi, dan dashboard tetap terpisah karena
mengatur pipeline yang berbeda dan snapshot model yang masih digunakan.
`config/auth.json` tetap menjadi penyimpanan kredensial lokal yang diabaikan Git.
Konfigurasi runner arsip di `Crawler/Backend/Reddit` dan `Youtube` memakai kontrak
lamanya dan tidak menjadi sumber konfigurasi `SocialCrawler`.

Runner Selenium juga membaca file utama dan memilih YouTube/Reddit yang didukungnya.

Loader universal berada di
[`crawler_config.py`](../../Crawler/Backend/crawler_config.py). Ia menyalin input,
menerapkan default/override, lalu memakai validator adapter yang sudah ada.
Dry-run tidak membaca kredensial atau memulai koneksi crawling.
Loader konfigurasi dan frontend tidak mengubah database. **No migration required**.

Output standar sekarang mengikuti [platform dan tanggal crawling WIB](OUTPUTS.md), dengan keunikan ID lintas hari. `--output-dir` tetap menulis bundle eksplisit untuk kompatibilitas.

## Frontend dan penyimpanan

Halaman sosmed di `Crawler/Frontend` mewarisi nilai awal melalui proyeksi publik otomatis dari file utama, bukan preset yang diedit terpisah. Jalankan `npm --prefix Crawler/Frontend run sync:config` setelah mengubah JSON sebelum build dengan context frontend terisolasi.

`storage.destination` menerima `excel` (default), `postgresql` atau `both`. Host/IP dan port berada pada `storage.postgresql`; string koneksi dibaca dari env server yang namanya ditentukan `connection_string_env` (default `BEESENSE_POSTGRESQL_DSN`). Jangan menaruh DSN/password nyata pada JSON atau env publik Vite. Form dapat mengirim URI sementara saat validasi plan.

Pilihan database masih kontrak frontend: layanan HTTP dan penulisan langsung crawler ke PostgreSQL belum diintegrasikan. Migrasi transaksi kini hanya frontend, ditempatkan pada data crawling masing-masing sosmed. Utility CLI/SQL/Docker migrasi Excel yang sempat dibuat telah dihapus sesuai perubahan lingkup. Runner CLI tetap menolak tujuan database sebelum akuisisi. Tidak ada perubahan pada dataset, database atau auth.json nyata.

Form akun/sesi opsional disediakan untuk Instagram, X/Twitter, TikTok, Threads dan Facebook. Tujuan penyimpanan kontrak server adalah `config/auth.json`, dengan entri `{sosmed, username, sessionid}` dan `x` dipetakan menjadi `twitter`. Hanya metadata username/keberadaan sesi boleh dikembalikan ke frontend. Demo tidak membaca atau menulis file autentikasi. Lihat [README frontend](../../Crawler/Frontend/README.md) dan [kontrak frontend](../../Crawler/Frontend/docs/API_CONTRACT.md).

## TikTok: browser mandiri BeeSense

`platforms.tiktok` memakai NativeTikTokClient dan Playwright 1.64.1, tanpa SDK
TikTok pihak ketiga. Query diwarisi bersama, halaman search/tag dirender lalu
respons jaringan UI, JSON hydration dan link native dibaca. Lihat
[TIKTOK_CRAWLER.md](TIKTOK_CRAWLER.md). `sort` hanya `relevance`; `headless` default
true, `browser` chromium. `auth_file` menunjuk satu entri TikTok di auth lokal;
msToken tidak masuk konfigurasi universal atau output.

Pengaturan tambahan di JSON yang sama: `request_interval_seconds: 3`,
`scroll_pause_seconds: 3`, `idle_scroll_limit: 3` (integer 1–3600). Interval request
juga menghormati delay bersama yang lebih besar. Server 5xx memperlambat pacing;
HTTP429 menyimpan Retry-After ke cache operasional dan menghentikan akuisisi sampai
cooldown habis. Login/CAPTCHA/respons API kosong menghentikan run. Tidak ada retry
setelah barrier, rotasi akun/IP atau solver CAPTCHA.

```sh
python -m Crawler.Backend.tiktok_crawler --install-browser
python -m Crawler.Backend.tiktok_crawler --dry-run
python -m Crawler.Backend.tiktok_crawler --target-posts 500 --total-seconds 1800
python -m Crawler.Backend.tiktok_crawler --headed --target-posts 500 --total-seconds 1800
```

Override CLI tidak mengubah JSON utama: default tetap 1.000 post, durasi null dan
komentar/balasan tanpa cap. Run kosong menyimpan audit/Excel berheader tanpa partisi
kosong atau perubahan arsip. Bundle parsial dan arsip ID membantu run lanjutan;
resume cursor komentar persis belum disediakan. Uji live headless dan terlihat
terbaru gagal 0/500, dijelaskan pada [laporan](TIKTOK_NATIVE_TRIAL_20261103.md).

### Validasi manusia untuk TikTok

`manual_wait_seconds: 0` tetap default. Untuk validasi manual gunakan nilai positif
(maksimum3600), `headless: false`, `browser: chromium`. `manual_poll_seconds` adalah
integer1–30 (default2); `manual_profile_dir` default `.cache/tiktok/chromium-profile`
dan harus tetap di direktori privat `.cache/tiktok`. CLI `--manual-validation`
mengaktifkan mode terlihat dengan waktu tunggu600detik tanpa mengubah JSON.
Konfirmasi manusia memakai wait_id/file kontrol lokal, bukan CAPTCHA solver.
Profil Chromium menyimpan sesi pengguna, sedangkan auth.json tetap tidak berubah.


### Hasil dari Chrome yang sudah terbuka

TikTokCrawler2.2.0 menerima `--chrome-capture <artefak.json>` untuk mengimpor data
publik yang telah diamati melalui tab Chrome terhubung. Ini bukan konfigurasi
kedua atau proses crawling otomatis: semua filter/target/output tetap memakai
social_crawler.json. Tidak membaca auth.json, membuka browser atau mengirim request
pada mode impor. Jangan gabungkan dengan --headed/--manual-validation/--install-browser.
File hasil berisi source existing_chrome_public_page, schema_version1, query,
captured_at UTC dan records dengan ID string. Detail di TIKTOK_CRAWLER.md.

### Konektor Chrome lokal 2.5.0

`--chrome-extension` memilih transport desktop, bukan preset bisnis baru. Query,
tanggal, target, caps komentar/balasan dan pacing tetap dari JSON universal.
Batas durasi dimulai setelah pairing, tanpa membaca auth/cookie profil. Uji ekstensi lokal terpasang menghasilkan
13 post/93 komentar/261 balasan, dihentikan sebelum target 500. Pagination 1.1.0
diperbaiki dan diuji offline; reload ekstensi sebelum run berikutnya.
Lihat [panduan konektor](TIKTOK_CHROME_LIVE.md).

## Status akhir 3 November 2026 — crawler dihentikan

Uji ekstensi terpasang dengan TikTokCrawler 2.4.1 / BeeSenseChromeLive 1.1.0
menyimpan **13 post, 93 komentar, 261 balasan (367 record unik)** dalam 656,6 detik.
Run `social_20261103T094828Z_23fb8a79` berstatus INTERRUPTED; target 500 belum
tercapai (kurang 487). Dua belas kandidat di luar tanggal dan dua kandidat tanpa
include keyword disaring. `comments_complete: false`; angka komentar pada TikTok
bukan jumlah yang sudah diperoleh. Excel: `outputs/crawling/tiktok/2026-11-03/social_data.xlsx`.
Arsip gabungan setelah run: **35.197 ID unik, 0 duplikat native ID**.

TikTokCrawler **2.5.0**, BeeSenseNative **1.2.0**, dan Connector **1.1.0** memperbaiki
penghentian tiga putaran idle pada komentar tanpa cap. Komentar menunggu akhir
pagination `has_more: false` dari sumber dan balasan tiap parent sampai habis;
metadata yang tidak tersedia tetap belum membuktikan lengkap. Kontrol balasan yang
lambat dicoba kembali dengan jeda, bukan dilewati permanen. Deadline global,
Stop, CAPTCHA/login dan pembatasan sumber tetap berlaku; hasil parsial disimpan.
Tanpa deadline, proses dapat terus menunggu sumber sampai operator menghentikannya.
Batas idle pencarian serta cap eksplisit tetap berlaku. Deduplikasi memakai ID asli.

Status terhubung kini ditampilkan setelah GET tugas lolos autentikasi. Kesalahan
pairing tidak ditimpa status pelepasan debugger normal. Izin dan ID ekstensi sama.
**Reload ekstensi lokal sebelum penggunaan berikutnya.** Perbaikan terbaru diuji
offline; tidak dilakukan uji live baru karena pengguna meminta proses berhenti.
Tidak ada migrasi database, perubahan auth.json, atau redeploy Streamlit.
Seluruh perubahan diterbitkan melalui branch terpisah dari main agar branch
Streamlit yang tercatat di README tidak diperbarui.
