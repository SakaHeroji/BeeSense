# Graph Report - /Users/socs3/Documents/BeeSense  (2026-10-28)

## Corpus Check
- Corpus is ~35,722 words - fits in a single context window. You may not need a graph.

## Summary
- 565 nodes · 1299 edges · 28 communities (24 shown, 4 thin omitted)
- Extraction: 96% EXTRACTED · 4% INFERRED · 0% AMBIGUOUS · INFERRED: 55 edges (avg confidence: 0.58)
- Token cost: deterministic AST 0; semantic agent usage unknown (not exposed)

## Community Hubs (Navigation)
- [[_COMMUNITY_Parser dan Runner Reddit|Parser dan Runner Reddit]]
- [[_COMMUNITY_Orkestrasi SocialCrawler|Orkestrasi SocialCrawler]]
- [[_COMMUNITY_Eksplorasi Dashboard Streamlit|Eksplorasi Dashboard Streamlit]]
- [[_COMMUNITY_Clustering dan Penjelasan NLP|Clustering dan Penjelasan NLP]]
- [[_COMMUNITY_Parser dan Runner Reddit 2|Parser dan Runner Reddit 2]]
- [[_COMMUNITY_Adapter dan Kontrak YouTube|Adapter dan Kontrak YouTube]]
- [[_COMMUNITY_Pengujian dan Regresi|Pengujian dan Regresi]]
- [[_COMMUNITY_Parser dan Runner Reddit 3|Parser dan Runner Reddit 3]]
- [[_COMMUNITY_Pengujian dan Regresi 2|Pengujian dan Regresi 2]]
- [[_COMMUNITY_Metodologi Machine Learning|Metodologi Machine Learning]]
- [[_COMMUNITY_Parser dan Runner Reddit 4|Parser dan Runner Reddit 4]]
- [[_COMMUNITY_Pengujian dan Regresi 3|Pengujian dan Regresi 3]]
- [[_COMMUNITY_Dokumentasi dan Konfigurasi|Dokumentasi dan Konfigurasi]]
- [[_COMMUNITY_Metodologi Machine Learning 2|Metodologi Machine Learning 2]]
- [[_COMMUNITY_Metodologi Machine Learning 3|Metodologi Machine Learning 3]]
- [[_COMMUNITY_Parser dan Runner Reddit 5|Parser dan Runner Reddit 5]]
- [[_COMMUNITY_Pengujian dan Regresi 4|Pengujian dan Regresi 4]]
- [[_COMMUNITY_Dokumentasi dan Konfigurasi 2|Dokumentasi dan Konfigurasi 2]]
- [[_COMMUNITY_Parser dan Runner Reddit 6|Parser dan Runner Reddit 6]]
- [[_COMMUNITY_Metodologi Machine Learning 4|Metodologi Machine Learning 4]]
- [[_COMMUNITY_Metodologi Machine Learning 5|Metodologi Machine Learning 5]]

## God Nodes (most connected - your core abstractions)
1. `SocialNLPClusterer` - 57 edges
2. `SocialNLPStreamlitApp` - 53 edges
3. `SocialCrawler` - 34 edges
4. `SocialCrawlerTests` - 32 edges
5. `Metodologi Machine Learning Social NLP` - 31 edges
6. `run()` - 21 edges
7. `RedditHtmlParser` - 20 edges
8. `RedditTests` - 20 edges
9. `file_hash()` - 19 edges
10. `import_pilot()` - 17 edges

## Surprising Connections (you probably didn't know these)
- `SocialCrawler` --implements--> `Compact Excel and verified reexport`  [EXTRACTED]
  social_crawler.py → SOCIAL_CRAWLER.md
- `SocialCrawler` --references--> `Reddit backend selection`  [EXTRACTED]
  social_crawler.py → SOCIAL_CRAWLER.md
- `SocialNLPStreamlitApp` --implements--> `Occurrence, sentence and comment units`  [EXTRACTED]
  nlp_dashboard.py → DASHBOARD_DESIGN.md
- `SocialNLPClusterer` --implements--> `Sentence and occurrence provenance`  [EXTRACTED]
  social_nlp.py → SOCIAL_NLP.md
- `SocialCrawler` --references--> `social_crawler.json`  [EXTRACTED]
  social_crawler.py → SOCIAL_CRAWLER.md

## Import Cycles
- None detected.

## Hyperedges (group relationships)
- **Common-space comparison of candidate families** — graphify_out_obsidian_metodologi_machine_learning_social_nlp_umap_hdbscan, graphify_out_obsidian_metodologi_machine_learning_social_nlp_semantic_kmeans, graphify_out_obsidian_metodologi_machine_learning_social_nlp_lexical_baseline, graphify_out_obsidian_metodologi_machine_learning_social_nlp_eligibility_silhouette, graphify_out_obsidian_metodologi_machine_learning_social_nlp_noise_ari, graphify_out_obsidian_metodologi_machine_learning_social_nlp_selection_policy [EXTRACTED 1.00]
- **Frozen inference, corpus fitting and saved exploration** — graphify_out_obsidian_metodologi_machine_learning_social_nlp_encoder_fitting, graphify_out_obsidian_metodologi_machine_learning_social_nlp_function_pipeline, graphify_out_obsidian_metodologi_machine_learning_social_nlp_snapshot_not_estimator, social_nlp_socialnlpclusterer, nlp_dashboard_socialnlpstreamlitapp [EXTRACTED 1.00]
- **Supported snapshot explanation** — explainable_topics_extractive_mmr, explainable_topics_comment_topic_share, explainable_topics_temporal_direction, explainable_topics_support_and_platform_mix, explainable_topics_phrase_change [EXTRACTED 1.00]

## Communities (28 total, 4 thin omitted)

### Community 0 - "Parser dan Runner Reddit"
Cohesion: 0.07
Nodes (36): add_readme(), BundleSink, ContentInput, ContractTests, Dataset, digest(), dumps(), KeywordMatcher (+28 more)

### Community 1 - "Orkestrasi SocialCrawler"
Cohesion: 0.06
Nodes (24): Offline CI validation suite, Verify BeeSense workflow, Pinned crawler dependency group, Combined installation requirements, _config(), Literal source filtering and bounded acquisition, _keywords(), main() (+16 more)

### Community 2 - "Eksplorasi Dashboard Streamlit"
Cohesion: 0.06
Nodes (20): Accessible and safe dashboard rendering, Native URL state and bounded controls, Filtered explanation lifecycle, _explain_filtered(), _graph_positions(), _load_artifacts(), main(), number() (+12 more)

### Community 3 - "Clustering dan Penjelasan NLP"
Cohesion: 0.07
Nodes (18): main(), Verify published source workbooks and the dashboard artifact bundle., verify(), file_hash(), json_write(), main(), Evidence-grounded topic descriptions and descriptive, source-aware trends., Explain already verified artifacts without encoding or fitting again. (+10 more)

### Community 4 - "Parser dan Runner Reddit 2"
Cohesion: 0.07
Nodes (28): Exception, HTMLParser, HTTPRedirectHandler, assert_accessible(), bounded_events(), BoundedDom, content_node(), first() (+20 more)

### Community 5 - "Adapter dan Kontrak YouTube"
Cohesion: 0.09
Nodes (34): SourceAdapter, error_code(), load_settings(), main(), parser(), run(), SafeLogger, Settings (+26 more)

### Community 6 - "Pengujian dan Regresi"
Cohesion: 0.13
Nodes (3): export_campaign(), load_campaign(), ResumeTests

### Community 7 - "Parser dan Runner Reddit 3"
Cohesion: 0.23
Nodes (12): atomic_json(), barrier_status(), campaign_plan(), decode_cli_output(), find_cli(), PlaywrightCLI, rate_limit_seconds(), run() (+4 more)

### Community 8 - "Pengujian dan Regresi 2"
Cohesion: 0.26
Nodes (3): ExplanationTests, model_from_counts(), profile()

### Community 9 - "Metodologi Machine Learning"
Cohesion: 0.18
Nodes (16): Represented-comment trend denominator, Metodologi Machine Learning Social NLP, Embedding cache identity and validation, In-sample candidate evaluation, Excel input and population guards, TF-IDF, SVD and KMeans baseline, Pinned local multilingual ONNX encoder, Overflow windows and equal-window pooling (+8 more)

### Community 10 - "Parser dan Runner Reddit 4"
Cohesion: 0.27
Nodes (8): classifyCaptureFailure(), enrichBatch(), rateLimitSeconds(), inWindow(), mergeCandidates(), row, source, window

### Community 12 - "Dokumentasi dan Konfigurasi"
Cohesion: 0.20
Nodes (10): Five dashboard views, Semantic similarity map interpretation, Occurrence, sentence and comment units, Represented-comment topic share, Extractive MMR descriptions, Support and platform-mixture sensitivity, Calendar-aware descriptive direction, Traceable topic explanations (+2 more)

### Community 13 - "Metodologi Machine Learning 2"
Cohesion: 0.25
Nodes (8): Within-topic phrase change, Eligibility gates and original-space silhouette, Frozen encoder versus corpus fitting, Explicit fit and explanation lifecycle, Noise-aware two-seed ARI, Composite score and tolerance policy, Heuristic model-selection tradeoff, Local multilingual topic-modeling pipeline

### Community 14 - "Metodologi Machine Learning 3"
Cohesion: 0.29
Nodes (7): BERTopic c-TF-IDF reference, Sparse class TF-IDF weighting, Automatic labels and centroid representatives, Extractive relevance and MMR, Carbonell and Goldstein MMR (1998), Sentence-level lexical vocabulary, Centroid graph and unused node cap

### Community 15 - "Parser dan Runner Reddit 5"
Cohesion: 0.33
Nodes (7): Snapshot artifacts without prediction estimators, Connected-browser campaign helpers, Checkpoint export and evidence limits, User-supplied checkpoint integrity, Reddit Playwright runner, Reddit backend selection, Validated clustering storage contract

### Community 17 - "Dokumentasi dan Konfigurasi 2"
Cohesion: 0.33
Nodes (6): Preserved full audit workbook, BeeSense, Twelve-file data allowlist, BeeSense README, Retained dashboard Excel input, Compact Excel and verified reexport

### Community 19 - "Metodologi Machine Learning 4"
Cohesion: 0.67
Nodes (3): Deduplicated fitting and occurrence units, Embedding text and deterministic identities, Sentence and occurrence provenance

## Knowledge Gaps
- **10 isolated node(s):** `social_crawler.json`, `NLP and dashboard dependency group`, `window`, `source`, `row` (+5 more)
  These have ≤1 connection - possible missing edges or undocumented components.
- **4 thin communities (<3 nodes) omitted from report** — run `graphify query` to explore isolated nodes.

## Suggested Questions
_Questions this graph is uniquely positioned to answer:_

- **Why does `file_hash()` connect `Clustering dan Penjelasan NLP` to `Parser dan Runner Reddit`, `Orkestrasi SocialCrawler`, `Eksplorasi Dashboard Streamlit`, `Adapter dan Kontrak YouTube`?**
  _High betweenness centrality (0.330) - this node is a cross-community bridge._
- **Why does `SocialNLPClusterer` connect `Clustering dan Penjelasan NLP` to `Orkestrasi SocialCrawler`, `Eksplorasi Dashboard Streamlit`, `Pengujian dan Regresi 2`, `Pengujian dan Regresi 3`, `Dokumentasi dan Konfigurasi`, `Metodologi Machine Learning 2`, `Parser dan Runner Reddit 5`, `Dokumentasi dan Konfigurasi 2`, `Metodologi Machine Learning 4`, `Metodologi Machine Learning 5`?**
  _High betweenness centrality (0.289) - this node is a cross-community bridge._
- **Why does `SocialCrawler` connect `Orkestrasi SocialCrawler` to `Dokumentasi dan Konfigurasi 2`, `Parser dan Runner Reddit 5`?**
  _High betweenness centrality (0.191) - this node is a cross-community bridge._
- **Are the 6 inferred relationships involving `SocialNLPClusterer` (e.g. with `SocialNLPStreamlitApp` and `DashboardTests`) actually correct?**
  _`SocialNLPClusterer` has 6 INFERRED edges - model-reasoned connections that need verification._
- **Are the 4 inferred relationships involving `SocialNLPStreamlitApp` (e.g. with `SocialNLPClusterer` and `AnalysisTests`) actually correct?**
  _`SocialNLPStreamlitApp` has 4 INFERRED edges - model-reasoned connections that need verification._
- **Are the 2 inferred relationships involving `SocialCrawler` (e.g. with `Clock` and `SocialCrawlerTests`) actually correct?**
  _`SocialCrawler` has 2 INFERRED edges - model-reasoned connections that need verification._
- **What connects `social_crawler.json`, `NLP and dashboard dependency group`, `window` to the rest of the system?**
  _10 weakly-connected nodes found - possible documentation gaps or missing edges._
## Preserved full audit workbook

The curated Obsidian vault now includes `Metodologi Machine Learning Social NLP.md` with the actual source hash, preprocessing and sentence provenance, frozen multilingual encoder, UMAP/HDBSCAN/KMeans comparison, internal evaluation and selection policy, c-TF-IDF topic extraction, descriptive trend explanations, training limits, all 47 JSON configuration fields, hardcoded parameters and test coverage. README, SOCIAL_NLP and the architecture canvas link to it. Documentation changes do not rerun acquisition, embedding or clustering.

The published data allowlist now contains twelve files: the full eight-sheet audit workbook `outputs/social_20261028_01/dataset.xlsx`, the unchanged compact NLP input `social_data.xlsx`, and ten files under `outputs/nlp_20261028_02`. The audit workbook is 6,480,303 bytes; SHA-256 ccfc77dc136ed8e98bce5c2c11d6243d22ff9e2a3082d9e299847b8b5aec74b3. Contents has 8,449 records: 6,167 comments, 2,051 replies and 231 root posts/videos. Relations has 16,436 relationship records, a different unit from comments. The saved NLP run has 16,178 sentence occurrences. Input and all nine artifact hashes still pass. No NLP class, input configuration, model weights or cluster result was changed. The verifier accepts both source workbooks, ignores temporary Excel owner files and still rejects missing or unlisted datasets; four regression tests cover these boundaries.

Graph extraction: 224 raw unresolved endpoint edges and 22 collapsed pairs. These structural extraction gaps are distinct from final graph integrity: zero dangling endpoints and zero self-loops. Six JSON configurations without AST symbols retain their file nodes. No raw conversation quotes or historical Reddit post nodes were introduced.

Obsidian remains a curated set of five notes and a canvas; the complete code map is in JSON/HTML. Deterministic AST token use is zero; semantic token use is unavailable from the agent API and is not reported as zero. Local NLP/UI/data-verifier tests and lint pass. The preceding main commit passed GitHub Actions. This upload triggers a new remote workflow. Docker build/runtime remain unverified because the local daemon is unavailable; there is no database migration.
