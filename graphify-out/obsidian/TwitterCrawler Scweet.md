---
type: architecture
tags: [beesense, crawler, twitter, scweet]
---

# TwitterCrawler Scweet

Pembaruan 6 November: [[Optimasi Crawler X dan Instagram 20261106]] menjelaskan
penghematan request, pemeriksaan root, pagination dan cooldown antarrun.

Class `TwitterCrawler` pada `Crawler/Backend/twitter_crawler.py` merupakan percobaan X/Twitter mandiri dengan Scweet 5.8.2. Konfigurasi `config/twitter_crawler.json` menetapkan 30 menit, target percobaan 1.000 post, maksimal 10 komentar/balasan per post dan query pendidikan dari preset Reddit. Kini diintegrasikan ke SocialCrawler 1.7.0 melalui TwitterCoordinatorWorker, dengan preset Twitter-only 3 jam/1.000 post pada config/social_crawler_twitter_3h.json.

## Alur dan kontrak

`config/auth.json` lokal → satu `ScweetWorker` persisten → pencarian/lookup/replies → normalisasi native ID → filter tanggal/kata kunci → `RecordFactory`/`Dataset`/`BundleSink` → `SocialExportMixin` → Excel dan manifest.

Entri `sosmed: twitter` menyimpan username dan sessionid; sessionid dipetakan ke cookie `auth_token`. Sesi diterima atau ditolak oleh X saat live, bukan dibuktikan hanya dari keberadaan file. Rahasia tidak dibaca saat dry-run dan tidak ditulis ke ekspor. State SQLite di `output/scweet` tetap diabaikan Git serta dipertahankan antar-run agar counter/cooldown tidak hilang.

## Pemilihan dan audit

Root menggunakan filter tanggal publikasi, include/exclude, dan mengabaikan retweet/balasan pencarian. Identitas `twitter:x_post:<native-id>` menyatukan domain x.com/twitter.com; ID yang sama tidak diekspor ulang meski teks berubah. Komentar/balasan mempertahankan native parent ID. Cakupan komentar dibatasi dan kelengkapan teks tidak dijamin. Parent yang tidak ada di ekspor tetap unresolved.

`social_data.xlsx` memakai sheet `Data` dan sepuluh kolom WIB yang sama dengan [[InstaloaderCrawler]] dan [[RedditCrawler Reddrix]]. `dataset.xlsx` dan JSONL memakai delapan tabel audit BeeSense. Manifest mencakup checksum; sel Excel berjenis teks agar caption tidak menjadi formula.

## Akses dan lifecycle

Satu concurrency; jeda minimum 5 detik antar-request dan 15 detik antar-operasi; konfigurasi limiter upstream 20 request/jendela 900 detik dan 120 request/hari. Window limiter Scweet diinisialisasi per operasi, sehingga bukan batas global lintas-operasi. Counter harian dan cooldown berada dalam SQLite. HTTP429/login/challenge menghentikan request berikutnya dan menyimpan hasil parsial. Default cooldown 429 minimal 900 detik, mengikuti Retry-After/reset jika lebih panjang. Adapter 1.0.1 menunggu cooldown pool Scweet yang hanya berupa `cooldown` jika masih muat dalam sisa anggaran; cap harian tetap terminal, HTTP429 transport tidak diulang, akun/state tetap sama dan counter tidak direset. Tidak ada pergantian identitas otomatis dan tidak ada Chrome pengguna yang ditutup.

`--dry-run` tidak menghubungi X. Uji unit memeriksa kontrak Excel, dedup, parent, batas waktu, worker persisten serta guard HTTP429 sinkron/asinkron. Image `deployment/docker/Dockerfile.twitter` non-root dengan allowlist, tanpa auth/state. Tidak perlu migrasi database aplikasi. Build/start Docker belum terverifikasi karena daemon tidak aktif.

## Hasil uji 31 Oktober 2026

Jendela percobaan sekitar 30 menit termasuk diagnosis cooldown dan pembaruan/resume; total runtime akuisisi sekitar 27 menit. Batch 1 (adapter 1.0.0) menyimpan 19 post/10 komentar/1 balasan sebelum berhenti `ACCOUNT_UNAVAILABLE`. SQLite menunjukkan cooldown rate limit/kode internal 429, sementara seluruh 65 respons HTTP tercatat 200. Batch 2 (adapter 1.0.1) melanjutkan setelah cooldown berakhir dengan akun/state/counter yang sama, mengecualikan ID batch pertama, lalu menyimpan 14 post baru/1 komentar hingga sisa anggaran 755 detik habis. Seluruh 59 respons HTTP batch kedua tercatat 200; tunggu cooldown otomatis diuji offline dan tidak terpicu lagi dalam run live kedua.

Total **33 post + 11 komentar + 1 balasan = 45 record unik**, 0 duplikasi native ID, 0 parent unresolved dan 0 parent lintas-root. Tidak ada respons HTTP429 yang teramati. Target 1.000 post belum tercapai. Satu event sumber invalid ditolak.

Hasil gabungan `outputs/twitter_scweet_20261031_30m_combined/social_data.xlsx` memakai sepuluh kolom standar. Folder gabungan mempertahankan Contents JSONL serta provenance/checksum; delapan tabel audit lengkap dan dataset.xlsx tetap berada pada dua folder batch sumber `twitter_scweet_20261031_30m_01` dan `_02`. Tidak ada training/deploy/dashboard yang dijalankan.

17 uji TwitterCrawler lulus; regresi SocialCrawler 71 pengujian, 70 lulus/1 optional skip. Header Excel/row kontrak/checksum/ID/parent/sel formula/ketiadaan cookie lokal dalam ekspor diverifikasi. Ruff/pip check serta allowlist Moby dan dry-run context terisolasi lulus. Tidak perlu migrasi; Docker build/start tetap belum terverifikasi karena daemon tidak aktif. Detail dan batas ada di [panduan crawler](../../docs/crawler/TWITTER_CRAWLER.md).

Lihat [[Struktur Proyek]], [[Arsitektur BeeSense]] dan [[HOME]].

## Integrasi pipeline 2 November 2026

SocialCrawler → TwitterCoordinatorWorker → ScweetWorker menggunakan sesi dan counter yang sama. Root hasil pencarian di-cache; hanya operasi jaringan yang menunggu jeda. Native X ID tetap unik lintas jenis record. Cooldown akun dapat ditunggu bila muat anggaran, HTTP429 aktual/login/challenge/cap harian menghentikan run dengan output parsial.

Merge dataset membaca root X dari audit Contents yang terverifikasi, menerbitkan native_roots.json yang terikat checksum workbook, lalu SocialNLPClusterer mempertahankan thread_root_key pada Parquet. Target 20 topik dan mean c_v ≥0,4 tetap merupakan gate publikasi. Setelah lulus, Gemini memakai top-10 keyword dan top-10 kalimat untuk 20 kalimat/deskripsi CSV; dashboard memakai artifact tersimpan tanpa crawling atau API saat rerun.

Angka pada bagian hasil 31 Oktober adalah riwayat; hasil 2 November akan dicatat setelah run selesai dan tervalidasi.
