---
type: dataset
tags: [beesense, provenance]
---

# Dataset Dashboard

[dataset.xlsx](../../outputs/social_20261028_01/dataset.xlsx) menyimpan audit lengkap delapan sheet, sedangkan [social_data.xlsx](../../outputs/social_20261028_01/social_data.xlsx) adalah input NLP satu sheet Data. Keduanya disertakan bersama [run NLP aktif](../../outputs/nlp_20261028_02/summary.json). Run memuat sembilan artifact dan manifest SHA-256; input ringkas cocok dengan hash pada metadata. Path sumber historis bukan syarat lokasi instalasi.

Workbook audit berukuran 6.480.303 byte, dengan 8.449 record pada Contents; SHA-256 `ccfc77dc136ed8e98bce5c2c11d6243d22ff9e2a3082d9e299847b8b5aec74b3`. Sheet lainnya: Relations, KeywordHits, Metrics, Runs, Sources, TextChunks dan Readme. File yang ditemukan kembali ini disimpan utuh; class NLP tetap membaca social_data.xlsx.

8.449 baris Excel; 8.218 baris komentar/balasan input; 7.944 menyumbang kalimat. Hasilnya 16.178 kemunculan, 15.878 kalimat unik, 51 topik dan 80 hubungan cosine. Cakupan 53,3% kemunculan versus 53,1% unik: penyebut berbeda.

Periode post asal 27 Oktober 2025–26 Oktober 2026. Sumber parsial dan tanggal komentar YouTube dapat berupa perkiraan. Bukan seluruh aktivitas platform. Porsi penjelasan menghitung komentar, termasuk noise dalam penyebut; satu komentar bisa memuat beberapa topik. Default waktu adalah post/video induk.

[Verifier](../../scripts/verify_dashboard_data.py) memeriksa integritas dan allowlist dua belas file data, termasuk daftar Git dengan opsi --check-git. Hash audit dilaporkan terpisah dan file kunci Excel sementara diabaikan. Run baru diabaikan Git; penjelasan dapat dihitung ulang tanpa encoding/training.

[[Arsitektur BeeSense]] · [[Menjalankan BeeSense]] · [[HOME]]
