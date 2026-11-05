---
type: training-run
tags: [beesense, nlp, tiktok, dashboard, retraining]
---

# Retraining Gabungan TikTok — 5 November 2026

Status: **kedua fitting selesai dan memenuhi gate**; 40 narasi terverifikasi pada dua snapshot final. Pengguna meminta
penggabungan seluruh sosmed setelah crawling berakhir 16.00 WIB, fitting/clustering
ulang tepat 20 topik dengan mean coherence c_v minimum 0,4, rebuild dashboard dan
commit/push GitHub main.

Sumber baru `outputs/social_20261105_combined_tiktok_01/social_data.xlsx` memuat
36.233 record unik: 2.552 root dan 33.681 komentar/balasan dari YouTube, Reddit,
Instagram, X/Twitter dan TikTok. Dua belas workbook digabung; 34.764 pengulangan
dihapus dari hasil, tanpa mengubah sumber. TikTok meliputi 25 post, 617 komentar
dan 806 balasan dari seluruh arsip tanggal, berbeda dari rangkaian hari ini yang
menyimpan 7 post/492 komentar/537 balasan. Lihat [[Pemantauan TikTok 1000 Post 20261105]].

Korpus NLP sebelum filter: 55.257 kemunculan, 53.967 kalimat unik, 1.290 pengulangan
kalimat dan 6.136 segmen dilewati. SBERT dipin tetap; embedding korpus baru dihitung
lokal, kemudian UMAP dua seed, DBSCAN dan Ward berbobot di-fit ulang. Hasil sebelum penyaringan **20 topik/c_v 0,4346102845**; sesudah filter
**20 topik/c_v 0,4666033620**, 11.185 kemunculan dan 10.795 kalimat unik.
Sepuluh topik sebelum dan enam sesudah masih <0,4 individual. Penyaringan
relevansi juga diulang karena keputusan lama terikat checksum input berbeda.

SocialNLP2.6.1 dan Dashboard kini mendukung native root TikTok video/photo, filter,
statistik/noise, bulanan, jaringan dan tren. Launcher mengambil pasangan before/
after dari config/dashboard.json. Semua pengaturan NLP tetap pada file universal;
konfigurasi efektif tersimpan pada masing-masing summary artifact.

Pengguna secara eksplisit mengizinkan pengiriman 400 keyword dan 400 kalimat
representatif ke Google Gemini untuk 40 narasi. Fitting dilakukan lokal tanpa API;
pengayaan CSV selesai: 20 narasi sebelum dan 20 sesudah; prompt hash cocok
dengan preview yang disetujui dan file fitted tetap identik. Kedua
snapshot tanpa narasi dan seluruh sumber lama tetap dipertahankan. Tidak ada
migrasi database atau perubahan konfigurasi produksi. Docker image baru belum
dibangun karena daemon tidak berjalan. Main dipublikasikan sesudah gate pemeriksaan data, kode dan Graphify.


[Catatan lengkap](../../docs/machine-learning/TIKTOK_RETRAIN_20261105.md) ·
[[Metodologi Machine Learning Social NLP]] · [[Dataset Dashboard]] · [[HOME]]
