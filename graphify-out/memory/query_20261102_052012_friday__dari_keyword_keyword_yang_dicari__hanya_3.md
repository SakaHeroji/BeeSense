---
type: "query"
date: "2026-11-02T05:20:12.259154+00:00"
question: "Friday, dari keyword-keyword yang dicari, hanya 3-5 topik saja yang menyangkut menyerempet ke keywordnya. apakah ini hal yang lumrah?"
contributor: "graphify"
outcome: "useful"
source_nodes: ["SocialNLPClusterer", "Weighted Ward topic reduction", "Coherence c_v evaluation protocol"]
---

# Q: Friday, dari keyword-keyword yang dicari, hanya 3-5 topik saja yang menyangkut menyerempet ke keywordnya. apakah ini hal yang lumrah?

## Answer

Expanded from original query via vocab: [keyword, query, sentence, clustering, coherence, relevance, comment, root, filter, ward, topic]. Graph traversal located SocialNLPClusterer, Weighted Ward topic reduction, and the current retraining report. Verified source: MachineLearning/social_nlp.py:274 prepares eligible comments/replies and segments/length-cleans them without a domain relevance gate. The acquisition preset uses kuliah, kampus, universitas, beasiswa, jurusan, but these are not topic seed constraints. Current topics include family, politics, entertainment and generic reactions; T03 kuliah/kerja/kampus contains 15902 sentence occurrences. Exploratory unsupervised topics can drift from acquisition keywords; the user observation is plausible but no manual relevance percentage has been measured. Mean c_v 0.4243 measures word association, not domain relevance; 20 is a topic count constraint. Topic count share is not sentence/record share. Recommend context-aware education relevance screening before clustering, human sample validation, and relevance alongside coherence; Gemini naming cannot fix off-domain cluster membership. No source code, model, or deployment changes requested or performed.

## Outcome

- Signal: useful

## Source Nodes

- SocialNLPClusterer
- Weighted Ward topic reduction
- Coherence c_v evaluation protocol