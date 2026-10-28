---
type: architecture
tags: [beesense, crawler, nlp, streamlit]
---

# Arsitektur BeeSense

SocialCrawler → Excel → SocialNLPClusterer → artifact terverifikasi → SocialNLPStreamlitApp.

- [SocialCrawler](../../social_crawler.py) memakai adapter YouTube/Reddit dan satu social_crawler.json untuk rentang tanggal, jeda, keyword serta batas post/komentar.
- [SocialNLPClusterer](../../social_nlp.py) memisahkan preparasi kalimat, embedding multilingual ONNX, perbandingan clustering, c-TF-IDF, graf dan persistensi. Tidak mengimpor Streamlit.
- [SocialNLPStreamlitApp](../../nlp_dashboard.py) membaca hasil tersimpan. Lima tampilan: ringkasan, peta topik, penjelasan topik, kalimat/sumber dan metode/data. UI tidak training saat rerun.
- MMR memilih bukti kalimat beragam. Theil–Sen/Kendall dan dua jendela waktu menyusun arah deskriptif dengan pemeriksaan sumber/platform/dukungan. Ini bukan sebab, ramalan atau tren populasi.
- Binding URL menyimpan filter/pilihan. Slider peta menyesuaikan nilai tersimpan saat hasil pencarian mengecil.

Kutipan sumber EXTRACTED; interpretasi pola dan edge cosine INFERRED. Lihat [metode NLP](../../SOCIAL_NLP.md), [penjelasan](../../EXPLAINABLE_TOPICS.md) dan [desain](../../DASHBOARD_DESIGN.md).

[[Dataset Dashboard]] · [[Menjalankan BeeSense]] · [[HOME]]

Metodologi lengkap, parameter dan pemilihan algoritma: [[Metodologi Machine Learning Social NLP]].
