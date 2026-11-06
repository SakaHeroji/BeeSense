---
type: "query"
date: "2026-11-06T02:44:24.454073+00:00"
question: "[$graphify](/Users/socs3/.codex/skills/graphify/SKILL.md) obsidian yang menu peta topik di dashboard. Jelaskan ke saya menghubungkannya dengan cara apa step by step"
contributor: "graphify"
outcome: "useful"
source_nodes: ["SocialNLPClusterer", "SocialNLPStreamlitApp", ".build_topic_graph()", ".topic_figure()", "_graph_positions()"]
---

# Q: [$graphify](/Users/socs3/.codex/skills/graphify/SKILL.md) obsidian yang menu peta topik di dashboard. Jelaskan ke saya menghubungkannya dengan cara apa step by step

## Answer

Expanded exact graph vocabulary: topic graph centroid cosine similarity dashboard. Graph navigation verified build_topic_graph at MachineLearning/social_nlp.py:L1347, describe_topics call at L1344, topic_figure at Dashboard/app.py:L239, _network call at L1350 and _graph_positions at L85. Current source and manifest-verified local artifacts confirm: unique sentence SBERT embeddings are L2-normalized; each final topic centroid is their mean renormalized to unit length (social_nlp.py:L1303). Graph similarity is centroids @ centroids.T (L1350), choosing three closest non-self neighbors per topic, retaining cosine >=0.55 and deduplicating undirected pairs (L1363-1383). Incoming choices mean a node can have degree greater than three. Graph uses original SBERT space, not UMAP plot distance, topic-name overlap or generated Gemini narrative. Graph saved during fitting to graph.json (L2391); dashboard reads verified artifacts and filters saved edges (Dashboard/app.py:L255). The configured after-filter snapshot outputs/nlp_20261105_relevance_topics20_gemini_01 has20topics,38edges,centroids shape20x384. Every saved edge cosine recomputed within1e-6 from verified centroids. Actual example T01 kampus/kuliah/mahasiswa to T07 jurusan/ijazah/kuliah cosine0.843081; T01-T05 swasta/pendidikan/kampus0.826123; T05-T07 0.799943. With all topics visible, saved edges remaining at thresholds .55/.65/.75/.85 are38/26/10/0. Slider only removes saved edges, cannot add discarded pairs. Layout uses weighted NetworkX spring_layout seed42 on full graph and label-separation adjustment; positions remain stable across filters, visual distance is not calibrated cosine. Node size uses filtered sentence occurrences; color shows platform composition or dominant platform. Cosine is inferred semantic similarity, not probability, accuracy or social-account relation. No application change or retraining performed. Prior authorized TikTok test is now truly running: verified Connector1.3.0/build20261106-throughput-v6, run social_20261106T023450Z_12916634 started09:34:50WIB, deadline10:34:50WIB. Keep live session6670 running; no premature completion claim.

## Outcome

- Signal: useful

## Source Nodes

- SocialNLPClusterer
- SocialNLPStreamlitApp
- .build_topic_graph()
- .topic_figure()
- _graph_positions()