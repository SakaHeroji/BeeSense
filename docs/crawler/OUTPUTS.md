# Output social media per platform dan tanggal

Output standar `SocialCrawler` berada di
`outputs/crawling/<platform>/<YYYY-MM-DD>/social_data.xlsx`. Tanggal mengikuti
pengamatan pertama dalam **WIB**, bukan tanggal publikasi konten. Buka
[`outputs/crawling/README.md`](../../outputs/crawling/README.md) untuk indeks file.

Setiap ID asli platform muncul **sekali di seluruh partisi**, termasuk lintas
tanggal. Teks sama pada ID berbeda tetap dipertahankan. Jika record diobservasi
ulang, nilai dari pengamatan terbaru dipakai pada partisi hari pertama, dengan
jejak sumber lengkap. Identitas mencakup platform dan namespace native yang tepat;
angka yang kebetulan sama pada platform berbeda bukan record yang sama.

Kontrak Excel tetap satu sheet `Data` dengan sepuluh kolom BeeSense. Kolom tanggal
publikasi tidak diubah. `record_lineage.jsonl` mengikat nomor baris ke ID, sumber,
baris sumber dan waktu pengamatan. `native_roots.json` mempertahankan root Twitter.
Root dan komentar dapat berada pada hari berbeda; relasinya tetap menunjuk ID asli.

## Crawling berikutnya

```sh
python -m Crawler.Backend.social_crawler --dry-run
python -m Crawler.Backend.social_crawler
```

Atur `output_root` pada `config/social_crawler.json` untuk mengganti direktori
utama. Saat `--output-dir` tidak diberikan, crawler menyimpan bundle audit asli
di `output/crawler_runs/`, lalu memperbarui partisi per platform/tanggal secara
otomatis. Katalog lama dimuat dan dideduplikasi sebelum publikasi. Bundle parsial
juga dipertahankan. Penguncian lokal dan penggantian direktori dengan rollback
melindungi arsip dari dua publisher bersamaan atau kegagalan ekspor.

`--output-dir <folder-baru>` tetap tersedia untuk konsumen kontrak lama: ia menulis
satu bundle audit eksplisit ke folder itu. Untuk memasukkannya ke indeks standar,
jalankan organizer. `primary_files` pada laporan run standar menunjukkan file
harian; `primary_file` dan `output_dir` tetap menunjuk bundle audit asli.

## Konsolidasi dan arsip lama

```sh
python -m scripts.organize_social_outputs --dry-run
python -m scripts.organize_social_outputs --archive-raw
```

Organizer memilih bundle crawling asli, mengabaikan hasil gabungan turunan dan
data sintetis, serta membaca `observed_at` dari audit. Datetime audit Excel lama
adalah UTC yang timezone-nya dilepas oleh exporter; konversi WIB dilakukan setelah
UTC dipasang kembali. Record tanpa bukti tanggal tidak diberi tanggal tebakan.

Bundle mentah yang belum diterbitkan dipindahkan ke
`output/crawler_runs/legacy/<tanggal>/<nama-run>/`, beserta file progresnya.
`output/crawler_runs/relocations.json` menyimpan pemetaan lokasi lama/baru.
Sumber yang sudah tracked, model NLP dan data yang dirujuk snapshot tetap pada
path lamanya agar manifest, pembandingan dashboard dan reproducibility berlaku.

Audit hasil konsolidasi ada di `outputs/crawling/archive.json`, `records.jsonl`
dan `observations.jsonl`. Semua workbook dibaca kembali untuk memeriksa nilai,
jumlah baris, tanggal, checksum dan keunikan ID global sebelum direktori dipublikasi.

## Pemulihan campaign Instagram 30 Oktober

Sebanyak **1.058 ID** hanya tersedia pada workbook gabungan historis yang lolos
checksum. Provenance menyimpan rentang baris dan sumber campaign 30 Oktober 2026.
Record tersebut memakai `timestamp_precision: historical_campaign_day`, dengan
jam `first_seen`/`last_seen` bernilai `null`; jam yang tidak tersedia tidak ditebak.
Reproduksi pemulihannya:

```sh
python -m scripts.organize_social_outputs \
  --historical-merge outputs/social_20261030_combined_instagram_500_2h_02/social_data.xlsx \
  --historical-source-index 1 --campaign-date 2026-10-30
```

Hasil awal: **34.785 ID unik** pada empat platform dan sembilan partisi harian.
Tidak ada ID ganda lintas partisi. Snapshot model/dashboard tetap menggunakan
dataset historisnya yang tidak berubah; konsolidasi tidak menjalankan training.

**No migration required** untuk database. Arsip filesystem baru memiliki schema
`beesense-social-archive:1`; data mentah dan sumber model dipertahankan.
