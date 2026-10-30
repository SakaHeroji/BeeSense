---
type: runbook
tags: [beesense, crawler, deduplication, captcha]
---

# Crawling 1000 Post Baru

[SocialCrawler](../../Crawler/Backend/social_crawler.py), producer 1.3.0, membaca [konfigurasi tunggal](../../config/social_crawler.json). Segmen `_01`–`_03` memakai 1.2.0; kelanjutan sejak `_04` memakai 1.3.0.
Target: **1.000 post baru yang memenuhi filter per platform**; batas pengambilan
**10.800 detik (3 jam)**. Rentang publikasi dan keyword yang sudah ada dipertahankan.

- Round robin memberi giliran satu operasi pencarian/post kepada YouTube dan Reddit.
- Minimum tetap 10 komentar/balasan unik; 100 komentar, 30 balasan, 10 balasan per thread.
- Batas percobaan 4.000 root dan penemuan 6.000 kandidat per platform. Batas ini bukan jumlah ekspor.
- CAPTCHA Reddit terlihat di Chrome profil runner. Pengguna mengeklik sendiri; crawler hanya mengamati setiap 5 detik, maksimal 600 detik dan dibatasi deadline global.
- Segmen `_01`–`_03` berhenti pada HTTP 429. Versi 1.3.0 mendukung cooldown terbatas; blokir akses lain tetap menghentikan platform.

## Pengecualian dataset lama

`exclude_existing_datasets` menunjuk `outputs/social_20261028_01`.
Sheet Contents pada workbook audit memuat **50 video YouTube dan 181 post Reddit**.
Native ID dan canonical URL harus cocok. URL dinormalisasi; post lama beserta threadnya
dilewati sebelum request, dan identitas hasil diperiksa kembali sebelum ekspor.
Judul/teks sama pada post berbeda bukan kunci duplikasi. Workbook dibaca read-only.

SHA-256 dataset.xlsx: `ccfc77dc136ed8e98bce5c2c11d6243d22ff9e2a3082d9e299847b8b5aec74b3`.
Checksum dan jumlah skipped tersimpan pada ringkasan run. Data sumber dashboard
[[Dataset Dashboard]] dan run NLP 20 topik tetap tersedia.

## Run 29 Oktober 2026

Pengambilan dimulai **09.59.53 WIB**; deadline sekitar **12.59.53 WIB**.
Output baru: `outputs/social_20261029_1000_3h_01`.
Progres selama run: `outputs/social_20261029_1000_3h_01.progress.json`.
Log: `output/crawl_20261029_1000_3h_01.log`.

Status awal: RUNNING; jumlah aktual/shortfall harus dibaca dari progress/summary,
bukan diasumsikan dari konfigurasi. Finalisasi Excel berlangsung setelah pengambilan.
Tidak ada migrasi database. Crawler menggunakan Chrome host, terpisah dari container
dashboard yang sudah berjalan.

44 tes crawler lulus (1 tes browser opsional dilewati), 12 tes runner Reddit lulus.
Tes baru mencakup pengecualian post historis, pemeriksaan identitas hasil, pembagian
giliran/deadline bersama dan penantian CAPTCHA tanpa klik otomatis.

[Runbook teknis](../../docs/crawler/SOCIAL_CRAWLER.md) · [[Arsitektur BeeSense]] · [[Menjalankan BeeSense]] · [[HOME]]

## Jeda Reddit setelah HTTP 429

Pada sekitar **10.09 WIB**, Reddit mengembalikan HTTP 429. Coordinator otomatis
menghentikan platform dengan `RATE_LIMITED`, tanpa retry atau pergantian identitas.
Pengguna meminta Reddit dijeda. Konfigurasi `platforms.reddit.enabled` saat itu false
untuk mencegah run baru mencoba Reddit; YouTube pada run yang sama tetap berjalan
dengan deadline semula. Sampai jeda, 10 post Reddit memenuhi minimum dan 17 post
diekspor sebagai bukti parsial. Angka final tetap mengikuti summary run. Pengaktifan
ulang Reddit menunggu instruksi pengguna dan berakhirnya cooldown.

## Dilanjutkan setelah refresh pengguna

Pengguna melakukan refresh dan menyatakan Reddit dapat diakses kembali. Reddit
diaktifkan lagi pada konfigurasi utama. Segmen `_01` disimpan secara graceful
(status INTERRUPTED): 1 post YouTube memenuhi minimum dan 10 post Reddit memenuhi
minimum (17 post Reddit diekspor sebagai bukti parsial). Segmen `_02` menjalankan
sisa target **999 YouTube dan 990 Reddit**, dengan sisa tenggat awal sekitar 12.59 WIB.
Indeks deduplikasi sekarang mencakup dataset lama dan bundle segmen `_01`.
Konfigurasi resume: `output/crawl_20261029_1000_3h_resume.json`.
Descriptor dua segmen/deadline: `output/campaign_20261029_1000_3h.json`.
Progres aktif: `outputs/social_20261029_1000_3h_02.progress.json`.
YouTube memakai 200 hasil per query pada resume dan urutan query dilanjutkan.
Target utama tetap 1.000 per platform; jumlah campaign adalah gabungan kedua segmen.
Tidak ada retry 429 tanpa instruksi pengguna; 429 berikutnya kembali menghentikan Reddit.

## Kelanjutan kedua dan pemantauan berkala

Reddit kembali berhenti karena HTTP 429 sekitar 10.20 WIB. Setelah pengguna
melakukan refresh dan meminta dilanjutkan, segmen `_02` disimpan. Total sebelum
segmen `_03`: **6 YouTube dan 17 Reddit qualified**; post bukti parsial yang
diekspor masing-masing 8 dan 31. Kelanjutan `_03` dimulai sekitar 10.24 WIB dengan
sisa target 994 YouTube dan 983 Reddit. Dataset lama serta seluruh bundle segmen
terdahulu masuk indeks pengecualian. Deadline awal tetap sekitar 12.59.53 WIB.

Query YouTube diberi petunjuk `after:2025-10-26 before:2026-10-28` agar penemuan
lebih sesuai periode. Lima kandidat probe memiliki tanggal publikasi dalam rentang;
ini bukan jaminan sumber mematuhi query. Pemeriksaan timestamp persis pada coordinator
tetap menentukan kelayakan. Resume memakai 100 hasil per query untuk menjangkau
variasi pencarian lebih cepat. Konfigurasi: `output/crawl_20261029_1000_3h_resume03.json`.

Segmen aktif dan deadline selalu dibaca dari descriptor campaign, bukan diasumsikan
dari paragraf riwayat ini. `output/check_crawl_campaign.py` menjumlahkan qualified,
post parsial yang diekspor, dan percobaan seluruh segmen. Pengguna meminta update
chat setiap 15 menit selama pemantauan aktif, mulai sekitar 10.30 WIB.

## Pengamatan cooldown untuk run berikutnya

429 terakhir selesai **10.36.39,685 WIB**; pengguna melaporkan Reddit sudah dapat
direfresh sekitar **10.42.11 WIB**, selisih **331,315 detik (sekitar 332 detik)**.
Ini batas waktu observasi sampai laporan pemulihan, bukan waktu minimum server.
Receipt menyebut 60 detik, yang dapat berasal dari fallback parser halaman Chrome.

Atas pilihan pengguna, kebijakan ditempatkan di `Crawler/Backend/social_crawler.py` dan JSON,
bukan pipeline NLP. Versi 1.3.0: `rate_limit_cooldown_seconds:360`,
`rate_limit_max_retries:3`; default retry 0 jika tidak dikonfigurasi. Retry menunggu
nilai terbesar antara kebijakan dan Retry-After, dibatasi deadline serta anggaran
post/retry run. Operasi gagal yang sama dilanjutkan; YouTube tetap berjalan selama
Reddit cooldown dalam round robin. Root yang sudah diekspor tidak diulang.
Event dan summary menyimpan waktu 429, cooldown-until serta hitungan retry.

Pada saat perubahan, pengguna meminta **crawl berikutnya tanpa eksekusi ulang**.
Saat itu campaign `_03` dan NLP tidak direstart; Reddit tetap berhenti,
YouTube meneruskan pengambilan. Tes memakai sumber sintetis
dan jam palsu, terpisah dari data crawl nyata. Tidak ada migrasi database.

Verifikasi cooldown: 50 tes crawler dijalankan, 49 lulus dan 1 tes browser opsional
dilewati; 12 tes runner Reddit lulus. Cakupan baru: YouTube tetap berjalan saat
Reddit menunggu, Retry-After lebih lama, batas retry/deadline, retry query yang sama,
validasi konfigurasi dan nilai tunggu server di luar kapasitas datetime.

## Kelanjutan atas instruksi baru sekitar 11.00 WIB

Pengguna kemudian menegaskan Reddit sudah bisa dan meminta crawling dimulai lagi.
Segmen `_03` difinalisasi secara graceful. Jumlah kumulatif saat peralihan:
**77 YouTube qualified dari 325 post tersimpan** dan **26 Reddit qualified dari
47 post tersimpan**. Kelanjutan `_04` menjalankan sisa target 923 YouTube dan
974 Reddit memakai 1.3.0 beserta cooldown 360 detik/maksimum 3 retry.

Config: `output/crawl_20261029_1000_3h_resume04.json`. Indeks pengecualian meliputi
baseline dan seluruh segmen `_01`–`_03`; deadline campaign tetap sekitar 12.59.53 WIB.
Reddit berhasil mengambil post baru lagi sekitar 11.00 WIB. Ini instruksi baru
yang mengizinkan kelanjutan, setelah perubahan sebelumnya disiapkan tanpa restart.
NLP tidak dijalankan ulang. Descriptor campaign menjadi acuan status/counter terbaru.

## Hasil pengamatan retry dan kelanjutan campaign

Retry otomatis pertama pada `_04` dimulai **11.13.27,076 WIB**, yaitu
**362,526 detik** setelah 429 teramati pada 11.07.24,550 WIB; operasi selesai
11.13.32,391 dengan `FINISHED_BEST_EFFORT`. YouTube tetap menulis data selama jeda.
Dua cooldown berikutnya juga berhasil memulihkan pengambilan. Bukti rinci:
`output/reddit_cooldown_observations_20261029.json`. Keberhasilan ini tidak
menentukan waktu minimum server.

Setelah batas 3 retry run `_04` terpakai, Reddit kembali 429 pada
**11.49.30,342 WIB**. Untuk melanjutkan target campaign yang diminta, coordinator
dioperasikan kembali melalui segmen `_05` setelah cooldown sampai **11.55.30 WIB**;
hasil `_04` disimpan lebih dahulu. Kumulatif saat peralihan: **164 YouTube qualified
dari 726 post tersimpan**, **57 Reddit qualified dari 97 post tersimpan**.
Sisa target `_05`: 836 YouTube/943 Reddit. Config:
`output/crawl_20261029_1000_3h_resume05.json`. Maksimum 3 retry tetap berlaku per run;
kelanjutan campaign memakai sisa deadline awal, tidak mendapat tambahan 3 jam.

Dataset baseline dan semua segmen sebelumnya dikecualikan. Pada awal `_05`, tampilan
browser masih menunjukkan barrier 429, sehingga coordinator kembali menunggu
cooldown sebelum request berikutnya. Status aktual selalu dibaca dari descriptor
dan progress, bukan diasumsikan berhasil dari waktu tunggu saja.

## Akuisisi selesai dan data gabungan

Campaign berakhir 29 Oktober 2026 pada deadline 12:59:53 WIB. Tidak ada operasi baru sesudah deadline; operasi in-flight terakhir berhenti pada 12:59:53,856 WIB. Kelima segmen terverifikasi dan disatukan menjadi [bundle audit hari ini](../../outputs/social_20261029_1000_3h/summary.json). Tidak ada native root ganda antarsegmen maupun overlap dengan baseline. Workbook audit baseline tetap ber-checksum `ccfc77dc136ed8e98bce5c2c11d6243d22ff9e2a3082d9e299847b8b5aec74b3`.

| Platform | Post tersimpan | Qualified ≥10 komentar/balasan | Komentar + balasan |
|---|---:|---:|---:|
| YouTube | 1.188 | 300 | 18.033 |
| Reddit | 98 | 58 | 1.331 |

Status **PARTIAL**, target 1.000 qualified per platform belum tercapai. Kandidat Reddit pada segmen akhir habis. Segmen 04/05 memakai versi 1.3 dengan total 7 rate-limit events dan 6 retry otomatis; hitungan ini tidak mencakup event pada runner lama yang belum mencatat counter tersebut.

[Workbook gabungan](../../outputs/social_20261029_combined/social_data.xlsx) memuat baseline 8.449 baris + akuisisi baru 20.650 = **29.099 baris**, **1.517 video/thread**, dan **27.582 komentar/balasan**. SHA-256 workbook gabungan: `7711aae01ca6b700b9842bddcd8c9c597e054947d4c5c1680cc9f61f9723aff9`. Pemeriksaan script merge lolos tanpa ID native ganda, orphan comment, formula sumber, maupun komentar terpotong. Teks identik dari ID berbeda tetap dipertahankan.

[scripts/merge_social_datasets.py](../../scripts/merge_social_datasets.py) mempertahankan urutan baseline kemudian data baru, mencatat rentang baris/checksum dalam [provenans lokal](../../output/combined_dataset_20261029.json), dan mempublikasikan workbook secara atomik. [[Dataset Dashboard]] kini menunjuk `outputs/nlp_20261029_combined_topics20_01` setelah tepat 20 topik dan rata-rata c_v 0,4720 ≥0,4 terverifikasi. Persiapan korpus baru menghasilkan 46.916 kemunculan dan 46.143 kalimat unik; embedding dihitung dengan SBERT asli pada revision tetap, tanpa memakai matriks korpus lama yang tidak cocok.

Training gabungan selesai: 20 topik, c_v 0,4720034334, 7 topik di bawah 0,4 individual. Runtime lokal `beesense-dashboard` dibangun ulang dan memakai mount read-only snapshot baru; health/non-root/sumber terverifikasi.
