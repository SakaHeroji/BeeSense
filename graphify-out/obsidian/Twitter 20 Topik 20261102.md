---
type: pipeline-result
tags: [beesense, twitter, nlp, gemini, dashboard]
---

# Twitter dan 20 topik — 2 November 2026

[[TwitterCrawler Scweet]] kini terhubung ke SocialCrawler 1.7.0. Hasil baru **333 post/187 komentar/104 balasan**; target konfigurasi 1.000 post dalam batas tiga jam belum tercapai. [Audit lima batch](../../docs/crawler/TWITTER_ACQUISITION_20261102.md) membedakan cooldown pool dari HTTP429 dan mencatat stop reason sebenarnya.

[[Dataset Dashboard]] aktif: **34.764 record unik**, **0 duplikasi native ID**, dari empat platform. Root X tersimpan dalam native_roots.json yang terikat checksum workbook. Komentar/balasan menjadi kalimat training; post/video asal menjadi konteks. [Workbook gabungan](../../outputs/social_20261102_combined_twitter_01/social_data.xlsx).

[[Metodologi Machine Learning Social NLP]]: **20 topik**, rata-rata **c_v 0.4243209772**, coverage **93.09%**, silhouette **-0.022359**, ARI **0.793974**. 9/20 skor individual masih di bawah 0,4; gate berlaku pada rata-rata. Evaluasi in-sample, bukan akurasi populasi/holdout.

[[Topik Gemini]]: [CSV 20 kalimat/deskripsi](../../outputs/nlp_20261102_twitter_topics20_gemini_01/topic_narratives.csv), masing-masing dari 10 keyword c-TF-IDF dan hingga 10 kalimat representatif. Excel memuat 48.850 pasangan topik–kalimat asli. Snapshot `outputs/nlp_20261102_twitter_topics20_gemini_01` dibaca dashboard tanpa request API atau training pada rerun.

[Metode dan hasil terverifikasi](../../docs/machine-learning/TWITTER_RETRAIN_20261102.md) · [[Arsitektur BeeSense]] · [[HOME]]
