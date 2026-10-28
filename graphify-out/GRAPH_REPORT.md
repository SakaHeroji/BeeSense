# Graph Report - /Users/socs3/Documents/BeeSense  (2026-10-28)

## Corpus Check
- Corpus is ~35,458 words - fits in a single context window. You may not need a graph.

## Summary
- 557 nodes · 1292 edges · 21 communities (19 shown, 2 thin omitted)
- Extraction: 96% EXTRACTED · 4% INFERRED · 0% AMBIGUOUS · INFERRED: 55 edges (avg confidence: 0.58)
- Token cost: deterministic AST 0; semantic agent usage unknown (not exposed)

## Community Hubs (Navigation)
- [[_COMMUNITY_Parser dan Runner Reddit|Parser dan Runner Reddit]]
- [[_COMMUNITY_Eksplorasi Dashboard Streamlit|Eksplorasi Dashboard Streamlit]]
- [[_COMMUNITY_Clustering dan Penjelasan NLP|Clustering dan Penjelasan NLP]]
- [[_COMMUNITY_Adapter dan Kontrak YouTube|Adapter dan Kontrak YouTube]]
- [[_COMMUNITY_Parser dan Runner Reddit 2|Parser dan Runner Reddit 2]]
- [[_COMMUNITY_Orkestrasi SocialCrawler|Orkestrasi SocialCrawler]]
- [[_COMMUNITY_Metodologi Machine Learning|Metodologi Machine Learning]]
- [[_COMMUNITY_Pengujian dan Regresi|Pengujian dan Regresi]]
- [[_COMMUNITY_Pengujian dan Regresi 2|Pengujian dan Regresi 2]]
- [[_COMMUNITY_Parser dan Runner Reddit 3|Parser dan Runner Reddit 3]]
- [[_COMMUNITY_Pengujian dan Regresi 3|Pengujian dan Regresi 3]]
- [[_COMMUNITY_Parser dan Runner Reddit 4|Parser dan Runner Reddit 4]]
- [[_COMMUNITY_Pengujian dan Regresi 4|Pengujian dan Regresi 4]]
- [[_COMMUNITY_Parser dan Runner Reddit 5|Parser dan Runner Reddit 5]]

## God Nodes (most connected - your core abstractions)
1. `SocialNLPClusterer` - 58 edges
2. `SocialNLPStreamlitApp` - 53 edges
3. `SocialCrawler` - 34 edges
4. `SocialCrawlerTests` - 32 edges
5. `Metodologi Machine Learning Social NLP` - 31 edges
6. `run()` - 21 edges
7. `RedditHtmlParser` - 20 edges
8. `RedditTests` - 20 edges
9. `file_hash()` - 20 edges
10. `import_pilot()` - 17 edges

## Surprising Connections (you probably didn't know these)
- `SocialNLPStreamlitApp` --implements--> `Occurrence, sentence and comment units`  [EXTRACTED]
  nlp_dashboard.py → DASHBOARD_DESIGN.md
- `SocialNLPClusterer` --implements--> `Sentence and occurrence provenance`  [EXTRACTED]
  social_nlp.py → SOCIAL_NLP.md
- `SocialCrawler` --references--> `social_crawler.json`  [EXTRACTED]
  social_crawler.py → SOCIAL_CRAWLER.md
- `SocialCrawler` --implements--> `Literal source filtering and bounded acquisition`  [EXTRACTED]
  social_crawler.py → SOCIAL_CRAWLER.md
- `SocialCrawler` --implements--> `Compact Excel and verified reexport`  [EXTRACTED]
  social_crawler.py → SOCIAL_CRAWLER.md

## Import Cycles
- None detected.

## Hyperedges (group relationships)
- **Common-space comparison of candidate families** — graphify_out_obsidian_metodologi_machine_learning_social_nlp_umap_hdbscan, graphify_out_obsidian_metodologi_machine_learning_social_nlp_semantic_kmeans, graphify_out_obsidian_metodologi_machine_learning_social_nlp_lexical_baseline, graphify_out_obsidian_metodologi_machine_learning_social_nlp_eligibility_silhouette, graphify_out_obsidian_metodologi_machine_learning_social_nlp_noise_ari, graphify_out_obsidian_metodologi_machine_learning_social_nlp_selection_policy [EXTRACTED 1.00]
- **Frozen inference, corpus fitting and saved exploration** — graphify_out_obsidian_metodologi_machine_learning_social_nlp_encoder_fitting, graphify_out_obsidian_metodologi_machine_learning_social_nlp_function_pipeline, graphify_out_obsidian_metodologi_machine_learning_social_nlp_snapshot_not_estimator, social_nlp_socialnlpclusterer, nlp_dashboard_socialnlpstreamlitapp [EXTRACTED 1.00]
- **Supported snapshot explanation** — explainable_topics_extractive_mmr, explainable_topics_comment_topic_share, explainable_topics_temporal_direction, explainable_topics_support_and_platform_mix, explainable_topics_phrase_change [EXTRACTED 1.00]

## Communities (21 total, 2 thin omitted)

### Community 0 - "Parser dan Runner Reddit"
Cohesion: 0.06
Nodes (40): Exception, HTMLParser, HTTPRedirectHandler, assert_accessible(), bounded_events(), BoundedDom, content_node(), first() (+32 more)

### Community 1 - "Eksplorasi Dashboard Streamlit"
Cohesion: 0.06
Nodes (21): Accessible and safe dashboard rendering, Native URL state and bounded controls, Filtered explanation lifecycle, _explain_filtered(), _graph_positions(), _load_artifacts(), main(), number() (+13 more)

### Community 2 - "Clustering dan Penjelasan NLP"
Cohesion: 0.08
Nodes (17): main(), Verify the single published dataset and the dashboard artifact bundle., verify(), file_hash(), json_write(), main(), Evidence-grounded topic descriptions and descriptive, source-aware trends., Explain already verified artifacts without encoding or fitting again. (+9 more)

### Community 3 - "Adapter dan Kontrak YouTube"
Cohesion: 0.09
Nodes (34): SourceAdapter, error_code(), load_settings(), main(), parser(), run(), SafeLogger, Settings (+26 more)

### Community 4 - "Parser dan Runner Reddit 2"
Cohesion: 0.09
Nodes (24): add_readme(), BundleSink, ContentInput, ContractTests, Dataset, digest(), dumps(), KeywordMatcher (+16 more)

### Community 5 - "Orkestrasi SocialCrawler"
Cohesion: 0.06
Nodes (28): Offline CI validation suite, Verify BeeSense workflow, Snapshot artifacts without prediction estimators, Eleven-file data allowlist, Retained dashboard Excel input, Connected-browser campaign helpers, Checkpoint export and evidence limits, User-supplied checkpoint integrity (+20 more)

### Community 6 - "Metodologi Machine Learning"
Cohesion: 0.06
Nodes (48): Five dashboard views, Semantic similarity map interpretation, Occurrence, sentence and comment units, Represented-comment topic share, Extractive MMR descriptions, Within-topic phrase change, Support and platform-mixture sensitivity, Calendar-aware descriptive direction (+40 more)

### Community 7 - "Pengujian dan Regresi"
Cohesion: 0.16
Nodes (6): Clock, rd_events(), receipt(), SocialCrawlerTests, spawn_youtube_fixture(), yt_events()

### Community 8 - "Pengujian dan Regresi 2"
Cohesion: 0.13
Nodes (3): export_campaign(), load_campaign(), ResumeTests

### Community 9 - "Parser dan Runner Reddit 3"
Cohesion: 0.23
Nodes (12): atomic_json(), barrier_status(), campaign_plan(), decode_cli_output(), find_cli(), PlaywrightCLI, rate_limit_seconds(), run() (+4 more)

### Community 10 - "Pengujian dan Regresi 3"
Cohesion: 0.26
Nodes (3): ExplanationTests, model_from_counts(), profile()

### Community 11 - "Parser dan Runner Reddit 4"
Cohesion: 0.27
Nodes (8): classifyCaptureFailure(), enrichBatch(), rateLimitSeconds(), inWindow(), mergeCandidates(), row, source, window

## Knowledge Gaps
- **10 isolated node(s):** `social_crawler.json`, `NLP and dashboard dependency group`, `window`, `source`, `row` (+5 more)
  These have ≤1 connection - possible missing edges or undocumented components.
- **2 thin communities (<3 nodes) omitted from report** — run `graphify query` to explore isolated nodes.

## Suggested Questions
_Questions this graph is uniquely positioned to answer:_

- **Why does `file_hash()` connect `Clustering dan Penjelasan NLP` to `Eksplorasi Dashboard Streamlit`, `Adapter dan Kontrak YouTube`, `Parser dan Runner Reddit 2`, `Orkestrasi SocialCrawler`?**
  _High betweenness centrality (0.339) - this node is a cross-community bridge._
- **Why does `SocialNLPClusterer` connect `Clustering dan Penjelasan NLP` to `Eksplorasi Dashboard Streamlit`, `Orkestrasi SocialCrawler`, `Metodologi Machine Learning`, `Pengujian dan Regresi 3`, `Pengujian dan Regresi 4`?**
  _High betweenness centrality (0.298) - this node is a cross-community bridge._
- **Why does `SocialCrawler` connect `Orkestrasi SocialCrawler` to `Pengujian dan Regresi`?**
  _High betweenness centrality (0.196) - this node is a cross-community bridge._
- **Are the 6 inferred relationships involving `SocialNLPClusterer` (e.g. with `SocialNLPStreamlitApp` and `DashboardTests`) actually correct?**
  _`SocialNLPClusterer` has 6 INFERRED edges - model-reasoned connections that need verification._
- **Are the 4 inferred relationships involving `SocialNLPStreamlitApp` (e.g. with `SocialNLPClusterer` and `AnalysisTests`) actually correct?**
  _`SocialNLPStreamlitApp` has 4 INFERRED edges - model-reasoned connections that need verification._
- **Are the 2 inferred relationships involving `SocialCrawler` (e.g. with `Clock` and `SocialCrawlerTests`) actually correct?**
  _`SocialCrawler` has 2 INFERRED edges - model-reasoned connections that need verification._
- **What connects `social_crawler.json`, `NLP and dashboard dependency group`, `window` to the rest of the system?**
  _10 weakly-connected nodes found - possible documentation gaps or missing edges._
## Methodology documentation update

The curated Obsidian vault now includes `Metodologi Machine Learning Social NLP.md` with the actual source hash, preprocessing and sentence provenance, frozen multilingual encoder, UMAP/HDBSCAN/KMeans comparison, internal evaluation and selection policy, c-TF-IDF topic extraction, descriptive trend explanations, training limits, all 47 JSON configuration fields, hardcoded parameters and test coverage. README, SOCIAL_NLP and the architecture canvas link to it. Documentation changes do not rerun acquisition, embedding or clustering.

The dashboard input remains `outputs/social_20261028_01/social_data.xlsx`: 8,449 rows including 8,218 comments/replies. Its SHA-256 matches the fitted run. The published data allowlist contains this one-sheet Excel and the ten files under `outputs/nlp_20261028_02`; all nine run artifact hashes pass. The eight-sheet acquisition workbook `dataset.xlsx` is a separate, unavailable source bundle and must not be confused with this retained input.

Graph extraction: 214 raw unresolved endpoint edges and 22 collapsed pairs. These structural extraction gaps are distinct from final graph integrity: zero dangling endpoints and zero self-loops. Six JSON configurations without AST symbols retain their file nodes. No raw conversation quotes or historical Reddit post nodes were introduced.

Obsidian remains a curated set of five notes and a canvas; the complete code map is in JSON/HTML. Deterministic AST token use is zero; semantic token use is unavailable from the agent API and is not reported as zero. Local NLP/UI tests pass; remote GitHub Actions and Docker build/runtime remain separate validation steps.
