---
type: acquisition_run
tags: [beesense, instagram, crawling]
---

# Instagram 500 Post — 2 Jam

Status: **PARTIAL**. Mulai 30-10-2026 20.11.01 WIB; batas akuisisi 30-10-2026 22.11.01 WIB.

## Tujuan dan Kriteria

- Instagram saja, target 500 post baru yang belum ada di baseline, dengan anggaran waktu keseluruhan 7.200 detik.
- Preset menghitung post dengan minimal 10 komentar unik termasuk balasan sebagai post memenuhi target. Post tersimpan dan post memenuhi target dilaporkan terpisah.
- Tanggal root: sejak 27-10-2025 10.17.00 WIB sampai sebelum 31-10-2026 00.00.00 WIB. Batas akhir diperpanjang atas instruksi pengguna agar seluruh 30 Oktober 2026 diterima.
- Keyword include/exclude mengikuti preset proyek; publikasi root, bukan tanggal komentar, menentukan rentang.
- Backend: SocialCrawler 1.6.0 → Instaloader 4.16 → `apply_browser_patch(loader.context)`. Komentar memakai transport `query_hash`/`NodeIterator`.
- Autentikasi run memakai cookie sesi (`sessionid`); username mengidentifikasi akun pada `load_session`. Password tidak dipakai untuk login.
- Pacing: jeda acak 5–10 detik antaroperasi, interval HTTP 5 detik, istirahat 120 detik setiap 20 operasi. Patch menjaga kompatibilitas, bukan menjamin bebas rate limit; backoff tetap berlaku.
- Deadline keseluruhan dipertahankan saat run dilanjutkan; waktu tidak direset menjadi dua jam baru.

## Baseline dan Pemeriksaan ID

- Baseline: `outputs/social_20261030_combined_3days_02/social_data.xlsx`, **33,034 record** dan **324 native ID post Instagram**.
- SHA-256 awal baseline: `ad3bfce17d8056712b4cd0bd6e673aebdcfbd318f2aab756d459d8d180ebf4e1`.
- Semua root ID Instagram baseline diekstrak dari Data, lalu dimasukkan ke workbook Contents untuk pengecualian crawler. Post, komentar dan balasan baru diperiksa ulang berdasarkan native ID sebelum merge.
- Root yang overlap baseline dikeluarkan seluruhnya dari input baru; ID konten berulang diperiksa, konflik provenance ditolak. Merge menolak duplikasi dan komentar tanpa root.

## Hasil

- Post Instagram baru unik: **301**.
- Kekurangan dari target 500 post tersimpan: **199**.
- Komentar: **622**; balasan: **138**.
- Post memenuhi minimum komentar: **16**.
- Record baru unik: **1061**.
- Post overlap baseline setelah pemeriksaan: **0**; duplikasi native ID: **0**.
- Baseline cocok dengan checksum awal: **True**.
- Status merge: `PASS`.

- Rate limit tercatat seluruh segmen: **0**.

Dataset gabungan: [outputs/social_20261030_combined_instagram_500_2h_02/social_data.xlsx](../../outputs/social_20261030_combined_instagram_500_2h_02/social_data.xlsx), **34,095 record**.
SHA-256 hasil: `ff4555a814e345573225fcce14c33d5fa549ef3800b885659df63998c6cc0a12`.

Audit independen: **PASS**. Semua nilai sel dari 33,034 record baseline dan 1,061 record baru dipertahankan persis. Rentang post baru aktual: 10-08-2026 16.47.33 WIB sampai 30-10-2026 21.48.32 WIB.

## Batas Cakupan

- Alasan berhenti run terakhir: `TIME_BUDGET_EXHAUSTED`. Target preset tercapai: `False`.
- Komentar yang tersedia tidak dijamin mencakup semua komentar Instagram. Angka yang dilaporkan berasal dari ekspor aktual.

## Pembaruan dan Snapshot

| Waktu WIB | Post baru | Memenuhi target | Komentar | Balasan |
|---|---:|---:|---:|---:|
| 30-10-2026 20.24.48 WIB | 0 | 0 | 0 | 0 |
| 30-10-2026 20.26.36 WIB | 0 | 0 | 0 | 0 |
| 30-10-2026 20.28.43 WIB | 0 | 0 | 0 | 0 |
| 30-10-2026 20.41.04 WIB | 50 | 2 | 38 | 18 |
| 30-10-2026 20.56.06 WIB | 102 | 4 | 85 | 43 |
| 30-10-2026 21.11.07 WIB | 154 | 6 | 131 | 50 |
| 30-10-2026 21.19.17 WIB | 175 | 9 | 284 | 75 |
| 30-10-2026 21.26.02 WIB | 192 | 9 | 284 | 75 |
| 30-10-2026 21.41.03 WIB | 240 | 10 | 371 | 90 |
| 30-10-2026 21.56.04 WIB | 266 | 14 | 524 | 135 |
| 30-10-2026 22.11.04 WIB | 301 | 16 | 622 | 138 |

Snapshot hanya memuat record lengkap yang sudah tersimpan dan dapat tertinggal dari hitungan live karena buffer penulisan.

- [30-10-2026 20.37.25 WIB](../../output/instagram_20261030_500_2h_01/checkpoints/minute_015/social_data.xlsx): 38 post, 94 record; overlap baseline 0, duplikasi ID 0.
- [30-10-2026 20.41.28 WIB](../../output/instagram_20261030_500_2h_01/checkpoints/minute_030/social_data.xlsx): 50 post, 106 record; overlap baseline 0, duplikasi ID 0.
- [30-10-2026 20.56.11 WIB](../../output/instagram_20261030_500_2h_01/checkpoints/minute_045/social_data.xlsx): 102 post, 230 record; overlap baseline 0, duplikasi ID 0.
- [30-10-2026 21.11.11 WIB](../../output/instagram_20261030_500_2h_01/checkpoints/minute_060/social_data.xlsx): 154 post, 335 record; overlap baseline 0, duplikasi ID 0.
- [30-10-2026 21.26.09 WIB](../../output/instagram_20261030_500_2h_01/checkpoints/minute_075/social_data.xlsx): 191 post, 550 record; overlap baseline 0, duplikasi ID 0.
- [30-10-2026 21.41.11 WIB](../../output/instagram_20261030_500_2h_01/checkpoints/minute_090/social_data.xlsx): 241 post, 704 record; overlap baseline 0, duplikasi ID 0.
- [30-10-2026 21.56.14 WIB](../../output/instagram_20261030_500_2h_01/checkpoints/minute_105/social_data.xlsx): 265 post, 924 record; overlap baseline 0, duplikasi ID 0.

## Catatan Eksekusi

- Checkpoint awal mengekspor nol post: 53 kandidat di luar rentang preset lama dan satu root belum terverifikasi.
- Pencarian top mengembalikan tiga SOURCE_ERROR/KeyError; run kembali ke iterator recent yang berhasil.
- Pengguna kemudian mengizinkan seluruh 30 Oktober, sehingga batas akhir diperpanjang. Tiga segmen awal mengekspor nol post.
- Segmen 04 menyimpan 175 post, 284 komentar dan 75 balasan sebelum satu operasi mencapai timeout 90 detik. Kelanjutan memakai timeout operasi 300 detik, mengecualikan 175 post tersebut bersama 324 post baseline; deadline keseluruhan tidak berubah. Semua segmen berdata ikut snapshot dan merge final.
- Bundle final: `outputs/social_instagram_20261030_500_2h_05`. Bukti konfigurasi, log dan verifikasi: `output/instagram_20261030_500_2h_01`.
- Nilai kredensial tidak dicatat dalam catatan atau laporan dataset.

[[InstaloaderCrawler]] · [[Dataset Dashboard]] · [[Crawling 1000 Post Baru]] · [[HOME]]
