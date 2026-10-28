---
type: "query"
date: "2026-10-28T15:57:46.647861+00:00"
question: "Hitung coherence minimal 0.4, retrain SBERT UMAP DBSCAN c-TF-IDF dan rebuild dashboard BeeSense"
contributor: "graphify"
outcome: "useful"
source_nodes: ["SocialNLPClusterer", "SocialNLPStreamlitApp"]
---

# Q: Hitung coherence minimal 0.4, retrain SBERT UMAP DBSCAN c-TF-IDF dan rebuild dashboard BeeSense

## Answer

Baseline dan hasil retrain c_v sama 0.40970330118194137; target rata-rata 0.4 tercapai untuk 52 topik. Sebanyak 31 topik masih di bawah 0.4 individual. Protokol tetap top10 istilah c-TF-IDF unigram/bigram single tokens, window110, semua15878 kalimat unik termasuk noise, macro mean tanpa bobot dan tanpa membuang topik invalid. Ambang tambahan saat training mempertahankan quality gate sebelumnya. Run baru outputs/nlp_20261028_coherence_01 menyimpan empat Parquet dan metadata coherence; sumber dan dua arsip lama terverifikasi. Dashboard lokal port8501 diperbarui;55 tes lulus pada dua environment, kelima tampilan data asli lulus, recomputation c_v independen sama. Docker daemon tidak tersedia; tidak ada migrasi database atau perubahan Coolify.

## Outcome

- Signal: useful

## Source Nodes

- SocialNLPClusterer
- SocialNLPStreamlitApp