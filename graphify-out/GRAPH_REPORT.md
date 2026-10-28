# Graph Report - /Users/sakaheroji/Documents/BeeSense  (2026-10-28)

## Corpus Check
- 57 files · ~45,293 words
- Verdict: corpus is large enough that graph structure adds value.

## Summary
- 668 nodes · 1520 edges · 33 communities (28 shown, 5 thin omitted)
- Extraction: 94% EXTRACTED · 6% INFERRED · 0% AMBIGUOUS · INFERRED: 88 edges (avg confidence: 0.64)
- Token cost: AST 0; semantic token usage unavailable (not measured).

## Community Hubs (Navigation)
- Pipeline dan Persistensi NLP
- Alur Akuisisi Sosial Terpadu
- Adapter Akuisisi YouTube
- Eksplorasi Dashboard Streamlit
- Crawler Selenium Terisolasi
- Parser dan Runner Reddit
- Identitas dan Kontrak Data
- Akses dan Parsing HTML
- Ekspor Campaign dan Resume
- Bundle Excel dan Provenans
- Coherence dan Quality Gate
- Runner Playwright Reddit
- Pengujian Penjelasan Topik
- Dashboard dan Tren Deskriptif
- Arsitektur Crawler dan Dependensi
- Runbook dan Verifikasi Lokal
- Helper Campaign Browser
- Pengujian UI Streamlit
- Validasi Redirect dan Kesalahan
- Snapshot NLP dan Arsip
- Verifikasi Dataset Berversi
- Parser DOM Terbatas
- Encoder SBERT dan Cache
- Ekstraksi Cuplikan Publik
- Memori Startup Dashboard
- Dependensi NLP dan Dashboard

## God Nodes (most connected - your core abstractions)
1. `SocialNLPClusterer` - 71 edges
2. `SocialCrawler` - 45 edges
3. `SocialNLPStreamlitApp` - 42 edges
4. `SocialCrawlerTests` - 32 edges
5. `NLPTests` - 25 edges
6. `SocialCrawlerSelenium` - 24 edges
7. `file_hash()` - 23 edges
8. `run()` - 21 edges
9. `RedditHtmlParser` - 20 edges
10. `RedditTests` - 20 edges

## Surprising Connections (you probably didn't know these)
- `SocialCrawler` --references--> `Per-platform qualifying-root targets and shortfalls`  [EXTRACTED]
  social_crawler.py → SOCIAL_CRAWLER.md
- `SocialNLPClusterer` --implements--> `Non-noise c-TF-IDF unigram/bigram labels`  [EXTRACTED]
  social_nlp.py → SOCIAL_NLP.md
- `SocialNLPClusterer` --implements--> `Two UMAP 10D projections seeded 42 and 43`  [EXTRACTED]
  social_nlp.py → SOCIAL_NLP.md
- `SocialNLPClusterer` --shares_data_with--> `Additive v2 coherence metadata with v1/v2-compatible loaders`  [EXTRACTED]
  social_nlp.py → SOCIAL_NLP.md
- `Obsidian c_v corpus and token protocol` --semantically_similar_to--> `Gensim c_v protocol: top 10 terms, window 110, phrase tokens`  [INFERRED] [semantically similar]
  graphify-out/obsidian/Metodologi Machine Learning Social NLP.md → SOCIAL_NLP.md

## Import Cycles
- None detected.

## Hyperedges (group relationships)
- **Frozen native SBERT to UMAP, density clustering and c-TF-IDF labels** — social_nlp_native_sbert, social_nlp_overflow_normalization, social_nlp_dual_umap, social_nlp_euclidean_dbscan, social_nlp_ctfidf [EXTRACTED 1.00]
- **Fixed c_v token protocol, full unique reference corpus and unweighted aggregate** — social_nlp_coherence_protocol, social_nlp_coherence_reference, social_nlp_coherence_aggregation, social_nlp_invalid_topic_failure [EXTRACTED 1.00]
- **Passing global c_v with unchanged baseline, individual shortfalls and in-sample limits** — social_nlp_coherence_result, social_nlp_unchanged_baseline, social_nlp_individual_shortfalls, social_nlp_insample_limit, social_nlp_original_space_silhouette [EXTRACTED 1.00]
- **Shared social workbook contract** — selenium_crawler_inherited_export, social_crawler_compact_excel, social_crawler_audit_bundle, graphify_out_obsidian_crawler_selenium_shared_excel [EXTRACTED 1.00]

## Communities (33 total, 5 thin omitted)

### Community 0 - "Pipeline dan Persistensi NLP"
Cohesion: 0.06
Nodes (23): _explain_filtered(), main(), Verify published source workbooks and the dashboard artifact bundle., verify(), file_hash(), json_write(), main(), Identify the parent thread, not the individual comment URL. (+15 more)

### Community 1 - "Alur Akuisisi Sosial Terpadu"
Cohesion: 0.06
Nodes (29): Advanced connected-browser Reddit campaign helpers, Checkpoint export to the eight-sheet contract, Native-ID provenance and bounded public excerpts, Isolated browser profile and access-barrier stops, Shared rendered_thread_dom.mjs extraction, Reddit Playwright CLI runner, Inherited SocialCrawler filters and Excel exporters, JSONL audit, dataset.xlsx and checksum manifest (+21 more)

### Community 2 - "Adapter Akuisisi YouTube"
Cohesion: 0.09
Nodes (34): SourceAdapter, error_code(), load_settings(), main(), parser(), run(), SafeLogger, Settings (+26 more)

### Community 3 - "Eksplorasi Dashboard Streamlit"
Cohesion: 0.08
Nodes (12): _graph_positions(), _load_artifacts(), main(), number(), percent(), Streamlit presentation only. Training lives in SocialNLPClusterer., Read-only exploration of completed NLP runs; no training on page reruns., Bounded topic graph: volume from filtered rows, semantic edges from the full mod (+4 more)

### Community 4 - "Crawler Selenium Terisolasi"
Cohesion: 0.08
Nodes (19): _barrier(), _create_driver(), main(), Content quoting an error is never used to classify an access barrier., Convert the shared rendered DOM capture without inventing identities., One browser operation. The parent enforces the hard process deadline., Stream evidence before completion; the original supervisor can retain it., Drop-in SocialCrawler with Selenium for both platforms and shared exports. (+11 more)

### Community 5 - "Parser dan Runner Reddit"
Cohesion: 0.09
Nodes (23): bounded_events(), HtmlPage, HtmlSource, load_settings(), LocalHtmlSource, native_fullname(), now_iso(), object_key() (+15 more)

### Community 6 - "Identitas dan Kontrak Data"
Cohesion: 0.13
Nodes (12): ContentInput, ContractTests, Dataset, digest(), KeywordMatcher, MemorySink, Aho-Corasick; offsets refer to Python Unicode code points in source., Shared pipeline; adapters cannot choose their own headers or cell formats. (+4 more)

### Community 7 - "Akses dan Parsing HTML"
Cohesion: 0.22
Nodes (9): assert_accessible(), content_node(), first(), fixture_page(), RedditHtmlParser, RedditTests, rendered_text(), source_time() (+1 more)

### Community 8 - "Ekspor Campaign dan Resume"
Cohesion: 0.13
Nodes (3): export_campaign(), load_campaign(), ResumeTests

### Community 9 - "Bundle Excel dan Provenans"
Cohesion: 0.20
Nodes (12): add_readme(), BundleSink, dumps(), main(), parser(), Validate the embedded contract; an external descriptor is optional., Atomic new directory; streaming JSONL + streaming, formula-safe Excel., run() (+4 more)

### Community 10 - "Coherence dan Quality Gate"
Cohesion: 0.12
Nodes (20): Negative original-space silhouette warning remains visible, Coherence mean 0.4097 passes while 31/52 topics remain low, Obsidian c_v corpus and token protocol, Global c_v target met with 31/52 individual shortfalls, Unweighted mean across all 52 non-noise topics, Additional c_v >=0.4 gate preserves earlier eligibility rules, Gensim c_v protocol: top 10 terms, window 110, phrase tokens, Reference corpus: all 15878 unique embedding_text sentences including noise (+12 more)

### Community 11 - "Runner Playwright Reddit"
Cohesion: 0.23
Nodes (12): atomic_json(), barrier_status(), campaign_plan(), decode_cli_output(), find_cli(), PlaywrightCLI, rate_limit_seconds(), run() (+4 more)

### Community 12 - "Pengujian Penjelasan Topik"
Cohesion: 0.26
Nodes (3): ExplanationTests, model_from_counts(), profile()

### Community 13 - "Dashboard dan Tren Deskriptif"
Cohesion: 0.13
Nodes (16): Filters retain model membership and do not recompute c_v, Global c_v on all views and per-topic/baseline table, Sentence occurrences, unique sentences and represented comments differ, Five artifact-backed Streamlit analysis views, On-demand explanations from active coherence run, Historical v1 HDBSCAN directional counts for 51 topics, MMR evidence and guarded Theil-Sen/Kendall directions, Source-bound beesense-topic-explanations:1 sidecar manifest (+8 more)

### Community 14 - "Arsitektur Crawler dan Dependensi"
Cohesion: 0.14
Nodes (15): Bounded native-ID evidence and explicit uncertainty, Obsidian: Crawler Selenium architecture, Shared BundleSink and dual-workbook export path, BeeSense Obsidian architecture and dataset index, Combined locked NLP and crawler installation, Pinned openpyxl and yt-dlp crawler dependencies, Pinned Selenium 4.51.0 plus crawler requirements, Relative dates remain calendar estimates (+7 more)

### Community 15 - "Runbook dan Verifikasi Lokal"
Cohesion: 0.18
Nodes (14): Coherence dependencies and NLP/UI regression verification, Verify BeeSense offline CI, Historical Graphify memory of the native SBERT/UMAP/DBSCAN migration, Artifact-only dashboard without Gensim/Torch imports, BeeSense startup, verification and coherence training runbook, Separate .venv-sbert training with explicit coherence baseline, Active outputs/nlp_20261028_coherence_01 snapshot, Separate archived v1 ONNX/HDBSCAN and pre-coherence v2 DBSCAN runs (+6 more)

### Community 16 - "Helper Campaign Browser"
Cohesion: 0.27
Nodes (8): classifyCaptureFailure(), enrichBatch(), rateLimitSeconds(), inWindow(), mergeCandidates(), row, source, window

### Community 18 - "Validasi Redirect dan Kesalahan"
Cohesion: 0.20
Nodes (5): Exception, HTTPRedirectHandler, Node, RestrictedRedirect, SourceFailure

### Community 19 - "Snapshot NLP dan Arsip"
Cohesion: 0.22
Nodes (10): Active coherence run with eleven v2 artifacts, Same-protocol baseline and retrain c_v approximately 0.4097033012, Obsidian dashboard dataset provenance, Source workbook and multi-snapshot integrity verification, Active 52-topic DBSCAN result at eps 0.3 and min_samples 10, Four Parquet files, UMAP npz and eleven-artifact v2 manifest, Unchanged MMR and source-guarded Theil-Sen/Kendall explanations, Obsidian methodology: SBERT, UMAP, DBSCAN and coherence (+2 more)

### Community 21 - "Parser DOM Terbatas"
Cohesion: 0.38
Nodes (3): HTMLParser, BoundedDom, Small serialised-DOM reader, not a browser or full HTML5 repair engine.

### Community 22 - "Encoder SBERT dan Cache"
Cohesion: 0.40
Nodes (5): Requested DBSCAN clustering, Requested SBERT-based embeddings, Pinned multilingual SentenceTransformer safetensors encoder, Overflow-window averaging and L2-normalized 384D embeddings, Encoder cache bound to immutable revision and text/checksums

## Knowledge Gaps
- **24 isolated node(s):** `window`, `source`, `row`, `candidate`, `Checkpoint export to the eight-sheet contract` (+19 more)
  These have ≤1 connection - possible missing edges or undocumented components.
- **5 thin communities (<3 nodes) omitted from report** — run `graphify query` to explore isolated nodes.

## Suggested Questions
_Questions this graph is uniquely positioned to answer:_

- **Why does `file_hash()` connect `Pipeline dan Persistensi NLP` to `Bundle Excel dan Provenans`, `Adapter Akuisisi YouTube`, `Eksplorasi Dashboard Streamlit`, `Alur Akuisisi Sosial Terpadu`?**
  _High betweenness centrality (0.421) - this node is a cross-community bridge._
- **Why does `SocialNLPClusterer` connect `Pipeline dan Persistensi NLP` to `Eksplorasi Dashboard Streamlit`, `Coherence dan Quality Gate`, `Pengujian Penjelasan Topik`, `Dashboard dan Tren Deskriptif`, `Runbook dan Verifikasi Lokal`, `Pengujian UI Streamlit`, `Snapshot NLP dan Arsip`, `Encoder SBERT dan Cache`?**
  _High betweenness centrality (0.276) - this node is a cross-community bridge._
- **Why does `SocialCrawler` connect `Alur Akuisisi Sosial Terpadu` to `Crawler Selenium Terisolasi`, `Arsitektur Crawler dan Dependensi`?**
  _High betweenness centrality (0.264) - this node is a cross-community bridge._
- **Are the 8 inferred relationships involving `SocialNLPClusterer` (e.g. with `SocialNLPStreamlitApp` and `DashboardTests`) actually correct?**
  _`SocialNLPClusterer` has 8 INFERRED edges - model-reasoned connections that need verification._
- **Are the 6 inferred relationships involving `SocialCrawler` (e.g. with `_SeleniumSource` and `SocialCrawlerSelenium`) actually correct?**
  _`SocialCrawler` has 6 INFERRED edges - model-reasoned connections that need verification._
- **Are the 4 inferred relationships involving `SocialNLPStreamlitApp` (e.g. with `SocialNLPClusterer` and `AnalysisTests`) actually correct?**
  _`SocialNLPStreamlitApp` has 4 INFERRED edges - model-reasoned connections that need verification._
- **Are the 2 inferred relationships involving `NLPTests` (e.g. with `SocialNLPStreamlitApp` and `SocialNLPClusterer`) actually correct?**
  _`NLPTests` has 2 INFERRED edges - model-reasoned connections that need verification._
## Extraction limitations

AST token cost: 0. Semantic token usage is unavailable from the delegated tool; displayed 0 counters are placeholders, not measured zero cost.

Raw extraction diagnostics: {"dangling_endpoint_edges": 49, "undirected_same_endpoint_collapsed_edges": 10}. These include external/unresolved symbols and same-endpoint relationship collapse in the undirected view. The exported graph has been checked separately for dangling endpoints.

The changed social_nlp.json configuration produces no AST symbols; its retained configuration node and current code/document relationships remain available. All changed Python/test files are structurally indexed. The active model uses SBERT, UMAP, DBSCAN and c-TF-IDF; negative original-space silhouette remains an explicit limitation.
