---
type: experiment
tags: [beesense, machine-learning, relevansi, rollback]
---

# Relevansi Konteks — 2 November 2026

Eksperimen lokal menggunakan ContextRelevanceFilter dan backend SBERT referensi semantik. Profil keyword: kuliah, kampus, universitas, beasiswa, jurusan. Konteks native root dan parent terverifikasi membantu kalimat ambigu; interaksi umum, pembahasan di luar lingkup dan keputusan meragukan dipisahkan sebelum clustering. Data mentah tetap utuh.


## Hasil eksperimen lokal — 2 November 2026

- Sumber: 34.764 record unik; data asli dan konfigurasi aktif tidak berubah.
- Keputusan: 10,496 relevan, 18,990 interaksi umum, 3,747 di luar lingkup, 20,099 meragukan dari 53,332 kemunculan.
- Kalimat diterima: 10,380 unik dari 6.544 komentar/balasan sumber. Relasi parent terverifikasi tersedia pada 6,633 kemunculan.
- Clustering: 20 topik; mean c_v 0.4733391691; 7/20 topik masih <0,4 individual. Coverage unik 82.1676%, silhouette cosine 0.049654, ARI 0.811814.
- DBSCAN eps 0,25/min_samples 10 menghasilkan 66 kelompok primer, kemudian Ward berbobot menggabungkannya menjadi 20. Embedding SBERT identik digunakan kembali; proyeksi/clustering/evaluasi dijalankan ulang.
- Snapshot dashboard lokal: `outputs/nlp_20261102_relevance_topics20_gemini_02/`. Dataset keputusan: `outputs/relevance_20261102_01/`. Snapshot tanpa narasi `_01` tetap utuh; dipilih untuk publikasi setelah persetujuan pengguna.

Contoh kelompok berlabel negara/rakyat memuat pembahasan LPDP, tanggung jawab penerima beasiswa, biaya kuliah dan pendidikan. Label c-TF-IDF singkat tidak cukup untuk menentukan relevansi; periksa kalimat serta konteks audit. Ada risiko salah seleksi otomatis dan banyak kasus meragukan yang dipisahkan; belum ada pengukuran akurasi berlabel.

[Runbook dan algoritma](../../docs/machine-learning/CONTEXT_RELEVANCE.md) · [Dashboard lokal](http://localhost:8502)

Pilih **Sebelum penyaringan** pada sidebar untuk membandingkan dengan [[Twitter 20 Topik 20261102]]. Default repository kini memakai snapshot tersaring ber-Gemini untuk publikasi ke Streamlit Cloud. Preset `config/social_nlp_twitter_20261102.json` dan snapshot lama dipertahankan untuk rollback. Cadangan kode tersedia pada `output/relevance_experiment_20261102/rollback/`.

Tidak diperlukan migrasi database aplikasi. Format artifact relevansi versi 1 dan cache skor disposable terpisah. Docker belum dibangun karena daemon lokal tidak tersedia. Setelah pengguna meminta Gemini secara eksplisit, 20 kalimat topik dan deskripsi berhasil dibuat dari 10 keyword c-TF-IDF serta 10 kalimat representatif per topik. CSV: `outputs/nlp_20261102_relevance_topics20_gemini_02/topic_narratives.csv`. Dua belas file data/clustering/audit identik dengan snapshot tanpa narasi; coherence tetap 0,4733391691. Dashboard membaca CSV tersimpan tanpa API saat rerun. Narasi adalah sintesis AI dari bukti terpilih, bukan statistik popularitas atau validasi relevansi. Otorisasi eksplisit ini menyelesaikan penolakan otomatis pada tahap sebelumnya.

[[Metodologi Machine Learning Social NLP]] · [[Dataset Dashboard]] · [[Arsitektur BeeSense]]
