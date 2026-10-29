---
type: architecture
tags: [beesense, crawler, nlp, streamlit]
---

# Arsitektur BeeSense

SocialCrawler → Excel → SocialNLPClusterer → artifact terverifikasi → SocialNLPStreamlitApp.

[[Frontend React Crawler]] menambahkan workspace React terpisah di `Crawler/Frontend`, berdasarkan [[PRD Frontend Crawler]]. Typed adapter memisahkan demo sintetis dari API/worker yang masih perlu diimplementasikan; aplikasi React tidak menjalankan crawler dari tab. UI mencakup tujuh sumber (YouTube, Reddit, Instagram, TikTok, Threads, Facebook, X/Twitter), dengan capability gating untuk lima adapter baru yang belum diimplementasikan. Survei memakai kontrak baru, sementara alur workbook sosial dan Dashboard Streamlit tetap terpisah.

[[Crawler Selenium|SocialCrawlerSelenium]] menyediakan pengambilan Chrome melalui Selenium untuk kedua platform, dengan filter dan exporter SocialCrawler yang sama.

- [SocialCrawler](../../social_crawler.py) memakai adapter YouTube/Reddit dan satu social_crawler.json untuk rentang tanggal, jeda, keyword serta batas post/komentar.
- [SocialNLPClusterer](../../social_nlp.py) memisahkan preparasi kalimat, embedding SBERT native multilingual, UMAP → DBSCAN Euclidean pada ruang UMAP → penggabungan Ward berbobot menjadi 20 topik, c-TF-IDF, evaluasi coherence c_v, graf dan persistensi. Tidak mengimpor Streamlit.
- [SocialNLPStreamlitApp](../../main.py) membaca hasil tersimpan. Lima tampilan: ringkasan, peta topik, penjelasan topik, kalimat/sumber dan metode/data. UI tidak training saat rerun.
- MMR memilih bukti kalimat beragam. Theil–Sen/Kendall dan dua jendela waktu menyusun arah deskriptif dengan pemeriksaan sumber/platform/dukungan. Ini bukan sebab, ramalan atau tren populasi.
- Binding URL menyimpan filter/pilihan. Slider peta menyesuaikan nilai tersimpan saat hasil pencarian mengecil.

Kutipan sumber EXTRACTED; interpretasi pola dan edge cosine INFERRED. Lihat [metode NLP](../../SOCIAL_NLP.md), [penjelasan](../../EXPLAINABLE_TOPICS.md) dan [desain](../../DASHBOARD_DESIGN.md).

[[Dataset Dashboard]] · [[Menjalankan BeeSense]] · [[HOME]]

Metodologi lengkap, parameter dan pemilihan algoritma: [[Metodologi Machine Learning Social NLP]].

Run aktif `outputs/nlp_20261029_combined_topics20_01`: 20 topik, rata-rata c_v 0,4720. Workbook gabungan baseline + akuisisi baru diperiksa ID/checksum melalui scripts/merge_social_datasets.py. Embedding baru dihitung untuk seluruh korpus, diikuti fitting UMAP/DBSCAN dan Ward; dbscan_cluster_id dan mapping tetap disimpan.

[[Crawling 1000 Post Baru]] memakai scheduler round robin dengan satu deadline, indeks ID post historis read-only dan penantian CAPTCHA manual. Ekspor baru tetap memakai kontrak delapan sheet serta workbook ringkas; crawler host tidak mengubah artifact dashboard aktif.

Panel topik terpilih memisahkan komentar, porsi, post asal dan coherence; grafik istilah/platform/sumber serta bukti bertautan mempertahankan konteks filter URL. Lihat [desain](../../DASHBOARD_DESIGN.md).

Runtime deployment dipisahkan: `requirements.txt` → `requirements-dashboard.txt` untuk UI/penjelasan dengan artifact tersimpan pada Python 3.12/3.14. Dependency ONNX, Numba/llvmlite, UMAP, Torch dan Gensim hanya berada di environment training/dev terpisah. `Dockerfile.nlp` memakai daftar runtime yang sama dan ARG `PYTHON_VERSION`; CI membuka snapshot asli pada kedua versi agar ketidakcocokan ABI seperti cp314 terdeteksi sebelum deploy. Lihat [[Menjalankan BeeSense]].
