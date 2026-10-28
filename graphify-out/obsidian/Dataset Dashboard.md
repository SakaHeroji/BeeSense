---
type: dataset
tags: [beesense, provenance]
---

# Dataset Dashboard

Hanya [social_data.xlsx](../../outputs/social_20261028_01/social_data.xlsx) dan [run NLP aktif](../../outputs/nlp_20261028_02/summary.json) yang disertakan. Run memuat sembilan artifact dan manifest SHA-256; Excel cocok dengan hash input pada metadata. Path sumber historis bukan syarat lokasi instalasi.

8.449 baris Excel; 8.218 baris komentar/balasan input; 7.944 menyumbang kalimat. Hasilnya 16.178 kemunculan, 15.878 kalimat unik, 51 topik dan 80 hubungan cosine. Cakupan 53,3% kemunculan versus 53,1% unik: penyebut berbeda.

Periode post asal 27 Oktober 2025–26 Oktober 2026. Sumber parsial dan tanggal komentar YouTube dapat berupa perkiraan. Bukan seluruh aktivitas platform. Porsi penjelasan menghitung komentar, termasuk noise dalam penyebut; satu komentar bisa memuat beberapa topik. Default waktu adalah post/video induk.

[Verifier](../../scripts/verify_dashboard_data.py) memeriksa integritas dan allowlist sebelas file data, termasuk daftar Git dengan opsi --check-git. Run baru diabaikan Git. Cache model, dataset lain, checkpoint dan ekspor penjelasan historis telah dibersihkan; penjelasan dapat dihitung ulang tanpa encoding/training.

[[Arsitektur BeeSense]] · [[Menjalankan BeeSense]] · [[HOME]]
