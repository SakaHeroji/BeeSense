# Akuisisi Twitter/X — 2 November 2026

SocialCrawler 1.7.0 memakai TwitterCoordinatorWorker dan Scweet dengan kontrak Excel BeeSense. Hanya Twitter yang dicrawl; YouTube, Reddit dan Instagram dibaca dari data yang sudah ada.

## Hasil terverifikasi

Target konfigurasi **1.000 post** dalam batas global **10.800 detik / 3 jam**. Hasil baru **333 post, 187 komentar, 104 balasan**. Target belum tercapai; stop reason setiap batch dicatat apa adanya. Tidak ada record sintetis atau penggandaan untuk memenuhi target.

Jendela sejak `2026-11-02T01:50:48.113836+00:00` sampai `2026-11-02T03:25:32.027636+00:00` berlangsung **5683.91 detik**, termasuk checkpoint dan jeda antarbatches. Total runtime akuisisi **4840.35 detik**. Ini bukan klaim request kontinu selama tiga jam.

| Batch | Post | Komentar | Balasan | Runtime detik | Stop reason |
| --- | ---: | ---: | ---: | ---: | --- |
| 01 | 12 | 0 | 0 | 280.68 | INTERRUPTED |
| 02 | 92 | 62 | 45 | 701.17 | INTERRUPTED |
| 03 | 28 | 125 | 59 | 1360.72 | CANDIDATES_EXHAUSTED |
| 04 | 3 | 0 | 0 | 1051.02 | CANDIDATES_EXHAUSTED |
| 05 | 198 | 0 | 0 | 1446.76 | ACCOUNT_UNAVAILABLE |

Batch 01/02 menjadi checkpoint sebelum penyesuaian cache dan sampling komentar. Batch 03/04 memakai query OR lima keyword; kandidat dari rencana pencarian tersebut habis. Batch 05 memakai **25 variasi query yang sama persis dengan Reddit**, dengan include/exclude yang juga sama. Query YouTube menambahkan operator tanggal. Semua resume memakai sisa deadline awal, akun/state/counter yang sama, dan native ID seluruh batch sebelumnya sebagai pengecualian. Batas pencarian bukan bukti bahwa seluruh post X yang relevan telah ditemukan.

Telemetry HTTP: `{'200': 371}`. Cooldown pool berdasarkan keadaan Scweet dibedakan dari HTTP429 aktual; scheduler hanya menunggu jika masih muat dalam deadline. Tidak ada reset counter atau rotasi akun/proxy. Chrome pengguna tidak dipakai.

Batch 05 berhenti ACCOUNT_UNAVAILABLE setelah kuota harian Scweet terpakai. Counter akhirnya **306/300 request** dan **1422/6000 tweet**. Pemeriksaan eligibility terjadi antar-operasi; paginasi operasi terakhir melewati angka konfigurasi request. Cap library ini bukan hard cap pada setiap request transport. Seluruh respons HTTP yang teramati tetap 200; status ini bukan bukti login akun ditolak.

Audit kontrak/manifest: **0 ID ganda antarbatch, 0 parent unresolved, 0 parent lintas-root**. Teks curated Scweet memiliki flag upstream_text_completeness_unknown; komentar adalah sampel, bukan cakupan seluruh percakapan.

## Konfigurasi dan output

[Preset publik](../../config/social_crawler_twitter_3h.json): Twitter-only, 25 query, 200 hasil per pencarian, jendela tujuh hari, maksimal 200 pencarian, minimum lima detik antar-request dan 15 detik antar-operasi jaringan. Sampel maksimal 50 thread/10 komentar per root; batch 04/05 memprioritaskan root tanpa komentar tambahan. Cap lokal 300 request/6.000 tweet per hari mempertahankan penggunaan sebelumnya dan tidak mengubah batas server. Auth dan SQLite tetap diabaikan Git.

Preset berikutnya mengizinkan maksimal 4.000 pemeriksaan root untuk mencapai target 1.000 post yang lolos filter. max_posts menghitung percobaan, bukan jumlah ekspor; run berhenti ketika 1.000 root qualified tercapai. Batch live hari ini mempertahankan nilai konfigurasi aslinya dalam audit Sources, tidak dieksekusi ulang untuk perubahan preset ini.

Angka 300 request/6.000 tweet per akun per hari UTC merupakan default Scweet, bukan batas resmi X atau jaminan bebas blokir. Scweet juga menghormati header sisa kuota/reset server. [Dokumentasi primer](https://github.com/Altimis/Scweet/blob/master/DOCUMENTATION.md#rate-limiting).

Lima folder `outputs/social_twitter_20261102_3h_01/` hingga `_05/` memuat workbook ringkas sepuluh kolom, workbook audit delapan sheet, delapan JSONL, contract, manifest dan summary. Log/progress runtime tetap lokal.

[Dataset gabungan](../../outputs/social_20261102_combined_twitter_01/social_data.xlsx): **34.764 record unik**, **2.526 root**, **32.238 komentar/balasan**. Sumbernya baseline 34.095 record, trial Twitter 45 record dan seluruh hasil lima batch. Total Twitter: `{'twitter/comment': 198, 'twitter/post': 366, 'twitter/reply': 105}`. Native ID global menghasilkan **0 duplikasi**; teks yang sama pada ID berbeda dipertahankan.

native_roots.json mengikat conversation root X pada checksum workbook. record_lineage.jsonl, duplicate_records.jsonl dan merge_report.json menyimpan provenans. Root tidak ditebak dari judul atau tanggal. [Hasil retraining](../machine-learning/TWITTER_RETRAIN_20261102.md).
