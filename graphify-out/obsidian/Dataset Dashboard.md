---
type: dataset
tags: [beesense, provenance, sbert, dbscan]
---

# Dataset Dashboard

[dataset.xlsx](../../outputs/social_20261028_01/dataset.xlsx) mempertahankan audit lengkap
delapan sheet. [social_data.xlsx](../../outputs/social_20261028_01/social_data.xlsx)
adalah input NLP satu sheet Data, 8.449 baris. Keduanya tidak diubah saat retraining.
SHA-256 audit: ccfc77dc136ed8e98bce5c2c11d6243d22ff9e2a3082d9e299847b8b5aec74b3.

[Run aktif SBERT + UMAP + DBSCAN](../../outputs/nlp_20261028_coherence_01/summary.json) memakai skema v2,
sebelas artifact dan manifest SHA-256. Empat Parquet: social_data (semua sumber),
sentences (unik), occurrences (kemunculan) dan skipped (alasan dilewati).
8.218 komentar/balasan input menghasilkan 16.178 kemunculan, 15.878 unik, 300
pengulangan dan 1.045 potongan dilewati. 7.944 komentar/balasan terwakili.

Hasil aktif: **52 topik**, coverage kalimat unik 95.11%, silhouette cosine -0.103367, ARI dua seed UMAP 0.825132. DBSCAN eps=0.3, min_samples=10. Noise: 776 kalimat unik dan 802 kemunculan. Fitting run publikasi 19.0 detik (embedding/UMAP dari cache tervalidasi).

Baseline [SBERT/UMAP/DBSCAN sebelum coherence](../../outputs/nlp_20261028_sbert_dbscan_01/summary.json)
dipertahankan utuh. Evaluasi ulang memakai protokol sama memberi c_v **0,4097033012**;
retrain menghasilkan nilai sama dan memenuhi ambang global **0,4**. 31/52 topik masih
<0,4 secara individual. Skor dan hash referensi tersimpan di summary.json run aktif.

Snapshot [v1 sebelumnya](../../outputs/nlp_20261028_02/summary.json) tetap tersedia:
51 topik HDBSCAN/UMAP, 80 sisi graf, coverage 53,1% kalimat unik. Itu hasil historis,
bukan hasil DBSCAN aktif. Loader dan penjelasan mendukung kedua versi tanpa training.

Periode post asal 27 Oktober 2025–26 Oktober 2026, sumber parsial, tanggal komentar
YouTube dapat berupa perkiraan. Penyebut komentar berbeda dari kemunculan kalimat.
Verifier memeriksa checksum seluruh snapshot NLP; output crawler terpisah tidak
dianggap bundle dashboard. Artifact dipublikasikan melalui allowlist Git.

[[Metodologi Machine Learning Social NLP]] · [[Arsitektur BeeSense]] · [[HOME]]
