---
type: "query"
date: "2026-10-28T15:35:33.877282+00:00"
question: "Update social_nlp.py ke embedding SBERT, UMAP sesuai pilihan pengguna, DBSCAN dan c-TF-IDF; latih ulang social_20261028_01, simpan Parquet dan rebuild dashboard."
contributor: "graphify"
outcome: "useful"
source_nodes: ["SocialNLPClusterer", "SocialNLPStreamlitApp"]
---

# Q: Update social_nlp.py ke embedding SBERT, UMAP sesuai pilihan pengguna, DBSCAN dan c-TF-IDF; latih ulang social_20261028_01, simpan Parquet dan rebuild dashboard.

## Answer

Graph vocabulary: nlp embedding encode clustering fit save artifact dashboard. Implemented native SentenceTransformer multilingual SBERT safetensors, frozen pretrained encoder with token overflow, two seeded UMAP projections and Euclidean DBSCAN; c-TF-IDF describes topics. Refit source8449rows into15878unique/16178occurrences,52clusters,95.11percent unique coverage,eps0.3,min_samples10. Original-space silhouette -0.103367 explicitly warns of semantic overlap; ARI0.825132. Four Parquet files and UMAP npz published atomically in outputs/nlp_20261028_sbert_dbscan_01, v2 loader compatible with v1, 24published file checksums verified, originals preserved.49NLP/UI tests passed in both training and dashboard runtimes; all5real-data views and live Chrome dashboard verified at127.0.0.1:8501. Docker daemon inaccessible; no database migration or production configuration changes.

## Outcome

- Signal: useful

## Source Nodes

- SocialNLPClusterer
- SocialNLPStreamlitApp