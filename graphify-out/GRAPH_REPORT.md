# Graph Report - /Users/socs3/Documents/BeeSense  (2026-10-29)

## Corpus Check
- 58 files · ~54,422 words
- Verdict: corpus is large enough that graph structure adds value.

## Summary
- 830 nodes · 1910 edges · 42 communities (34 shown, 8 thin omitted)
- Extraction: 92% EXTRACTED · 8% INFERRED · 0% AMBIGUOUS · INFERRED: 150 edges (avg confidence: 0.8)
- Token cost: 0 input · 0 output

## Graph Freshness
- Built from commit: `6fd6dc92`
- Run `git rev-parse HEAD` and compare to check if the graph is stale.
- Run `graphify update .` after code changes (no API cost).

## Community Hubs (Navigation)
- Pipeline dan Persistensi NLP
- Alur Akuisisi Sosial Terpadu
- Alur Akuisisi Sosial Terpadu
- Adapter Akuisisi YouTube
- Crawler Selenium Terisolasi
- Bundle Excel dan Provenans
- Akses dan Parsing HTML
- Snapshot NLP dan Arsip
- Parser dan Runner Reddit
- Ekspor Campaign dan Resume
- Identitas dan Kontrak Data
- Eksplorasi Dashboard Streamlit
- Runner Playwright Reddit
- Eksplorasi Dashboard Streamlit
- Topik dan Verifikasi NLP
- Identitas dan Kontrak Data
- Parser DOM Terbatas
- Pengujian Penjelasan Topik
- Coherence dan Quality Gate
- Validasi Redirect dan Kesalahan
- Eksplorasi Dashboard Streamlit
- Pengujian UI Streamlit
- Coherence dan Quality Gate
- Coherence dan Quality Gate
- Arsitektur Crawler dan Dependensi
- Helper Campaign Browser
- Verifikasi Dataset Berversi
- Arsitektur Crawler dan Dependensi
- Eksplorasi Dashboard Streamlit
- Eksplorasi Dashboard Streamlit
- Runbook dan Verifikasi Lokal
- Eksplorasi Dashboard Streamlit
- Eksplorasi Dashboard Streamlit
- Coherence dan Quality Gate
- Snapshot NLP dan Arsip
- Ekstraksi Cuplikan Publik
- Memori Startup Dashboard

## God Nodes (most connected - your core abstractions)
1. `SocialNLPClusterer` - 80 edges
2. `SocialCrawler` - 58 edges
3. `SocialNLPStreamlitApp` - 53 edges
4. `SocialCrawlerTests` - 41 edges
5. `Runbook and historical record for finalized partial crawler campaign` - 32 edges
6. `NLPTests` - 26 edges
7. `SocialCrawlerSelenium` - 24 edges
8. `file_hash()` - 23 edges
9. `run()` - 21 edges
10. `RedditHtmlParser` - 20 edges

## Surprising Connections (you probably didn't know these)
- `Historical fixed top10/window110/all15878-unique macro c_v protocol` --semantically_similar_to--> `Gensim c_v protocol: top 10 terms, window 110, phrase tokens`  [INFERRED] [semantically similar]
  graphify-out/memory/query_20261028_155746_hitung_coherence_minimal_0_4__retrain_sbert_umap_d.md → SOCIAL_NLP.md
- `SocialNLPClusterer` --implements--> `Two UMAP 10 D projections seeded 42 and 43`  [EXTRACTED]
  social_nlp.py → SOCIAL_NLP.md
- `SocialNLPClusterer` --implements--> `Published 15-candidate DBSCAN grid preserves 8 million-edge guard`  [INFERRED]
  social_nlp.py → SOCIAL_NLP.md
- `SocialNLPClusterer` --implements--> `New combined-corpus SBERT and dual-UMAP features reused only through exact verified caches`  [INFERRED]
  social_nlp.py → SOCIAL_NLP.md
- `SocialNLPClusterer` --references--> `Saved-model dashboard uses a separate runtime;full refitting stays Python 3.12`  [EXTRACTED]
  social_nlp.py → SOCIAL_NLP.md

## Import Cycles
- None detected.

## Hyperedges (group relationships)
- **Bounded qualifying-root campaign with shared scheduler and manual CAPTCHA** — social_crawler_round_robin_deadline, social_crawler_campaign_qualified_targets, social_crawler_manual_captcha_wait, social_crawler_partial_bundle_reporting [EXTRACTED 1.00]
- **Historical identity exclusion with pre-request and export duplicate guards** — social_crawler_historical_root_identity, social_crawler_root_identity_guards, social_crawler_per_run_root_deduplication, social_crawler_atomic_live_progress [INFERRED 0.85]
- **Coordinator 1.3 retry contract: policy, same operation, readiness, deadline and audit** — social_crawler_next_run_bounded_cooldown, social_crawler_pending_failed_operation_retry, social_crawler_cooldown_ready_scheduler, social_crawler_rate_limit_timing_audit, social_crawler_round_robin_deadline [EXTRACTED 1.00]
- **Frozen native SBERT, UMAP, DBSCAN, sentence-weighted Ward and final c-TF-IDF labels** — social_nlp_native_sbert, social_nlp_overflow_normalization, social_nlp_dual_umap, social_nlp_euclidean_dbscan, social_nlp_sentence_weighted_ward, social_nlp_ctfidf [EXTRACTED 1.00]
- **Fixed c_v token protocol, full unique reference corpus and unweighted aggregate** — social_nlp_coherence_protocol, social_nlp_coherence_reference, social_nlp_coherence_aggregation, social_nlp_invalid_topic_failure [EXTRACTED 1.00]
- **Combined-corpus global coherence with historical incomparable baselines,individual shortfalls and in-sample limits** — social_nlp_coherence_result, social_nlp_unchanged_baseline, social_nlp_individual_shortfalls, social_nlp_insample_limit, social_nlp_original_space_silhouette [EXTRACTED 1.00]
- **Dashboard-only dependencies,Docker wheels and isolated dual-Python regression** — requirements_dashboard_ui_artifact_dependencies, requirements_dashboard_python_numpy_markers, dockerfile_dashboard_wheels_python_version, _github_workflows_ci_dashboard_runtime_isolation, _github_workflows_ci_shipped_artifact_cloud_regression [INFERRED 0.95]
- **Shared social workbook contract** — selenium_crawler_inherited_export, social_crawler_compact_excel, social_crawler_audit_bundle, graphify_out_obsidian_crawler_selenium_shared_excel [EXTRACTED 1.00]

## Communities (42 total, 8 thin omitted)

### Community 0 - "Pipeline dan Persistensi NLP"
Cohesion: 0.05
Nodes (25): main(), Verify published source workbooks and the dashboard artifact bundle., verify(), file_hash(), json_write(), main(), Use the same class TF-IDF vocabulary for selection and publication., Macro c_v on ALL non-noise topics and a fixed full-corpus reference.          Un (+17 more)

### Community 1 - "Alur Akuisisi Sosial Terpadu"
Cohesion: 0.06
Nodes (21): _config(), _keywords(), Omitted retry config defaults to zero retries for existing callers, main(), _number(), Describe the acquisition backend independently of the shared export., Compose the original adapters and workers; one JSON configuration and bundle., Validate and return the effective plan without browser/network access. (+13 more)

### Community 2 - "Alur Akuisisi Sosial Terpadu"
Cohesion: 0.05
Nodes (70): Host crawler campaign preserves independent dashboard artifacts, Historical active-campaign state; acquisition now finalized PARTIAL, Before segment 03: qualified YouTube6/Reddit17; exported evidence8/31, Before 04 cumulative qualified YouTube77/Reddit26; evidence325/47, 1000 qualified-root targets per platform within shared three-hour budget, Campaign descriptor records finalized PARTIAL status and five-segment accounting, Cooldown verification:50 crawler tests, 49pass/1skip;12 Reddit runner tests pass, Historical descriptor-based monitoring now resolves final campaign counters (+62 more)

### Community 3 - "Adapter Akuisisi YouTube"
Cohesion: 0.09
Nodes (34): SourceAdapter, error_code(), load_settings(), main(), parser(), run(), SafeLogger, Settings (+26 more)

### Community 4 - "Crawler Selenium Terisolasi"
Cohesion: 0.08
Nodes (19): _barrier(), _create_driver(), main(), Content quoting an error is never used to classify an access barrier., Convert the shared rendered DOM capture without inventing identities., One browser operation. The parent enforces the hard process deadline., Stream evidence before completion; the original supervisor can retain it., Drop-in SocialCrawler with Selenium for both platforms and shared exports. (+11 more)

### Community 5 - "Bundle Excel dan Provenans"
Cohesion: 0.17
Nodes (13): add_readme(), BundleSink, dumps(), main(), now_iso(), parser(), Validate the embedded contract; an external descriptor is optional., Atomic new directory; streaming JSONL + streaming, formula-safe Excel. (+5 more)

### Community 6 - "Akses dan Parsing HTML"
Cohesion: 0.22
Nodes (8): bounded_events(), first(), fixture_page(), Whole-post comment budget includes replies; nested replies share thread cap., RedditHtmlParser, RedditTests, source_time(), worker()

### Community 7 - "Snapshot NLP dan Arsip"
Cohesion: 0.12
Nodes (23): Historical v 1 HDBSCAN directional counts for 51 topics, Prior Graphify memory: Selenium crawler preserves Excel contract, BeeSense crawler, NLP and dashboard class architecture, EXTRACTED source quotations versus INFERRED topic interpretations, Crawler Excel to independent NLP/coherence artifacts to Streamlit, Historical audit workbook: 50 YouTube and 181 Reddit root identities, Active combined 20-topic run with eleven artifacts and manifest, Four immutable older NLP snapshots including baseline 20-topic run (+15 more)

### Community 8 - "Parser dan Runner Reddit"
Cohesion: 0.13
Nodes (11): HtmlSource, load_settings(), LocalHtmlSource, parsed_number(), ABC, Normalize a source event; write only through the shared Dataset/Sink., run_worker(), Settings (+3 more)

### Community 9 - "Ekspor Campaign dan Resume"
Cohesion: 0.13
Nodes (3): export_campaign(), load_campaign(), ResumeTests

### Community 10 - "Identitas dan Kontrak Data"
Cohesion: 0.18
Nodes (5): ContractTests, digest(), RecordFactory, utc_datetime(), validate_row()

### Community 12 - "Runner Playwright Reddit"
Cohesion: 0.23
Nodes (12): atomic_json(), barrier_status(), campaign_plan(), decode_cli_output(), find_cli(), PlaywrightCLI, rate_limit_seconds(), run() (+4 more)

### Community 13 - "Eksplorasi Dashboard Streamlit"
Cohesion: 0.17
Nodes (17): Filters retain model membership and do not recompute c_v, Selected-topic c_v card is separate from the full-model mean, Occurrences, unique sentences, comments and source roots have different denominators, Five artifact-backed Streamlit analysis views, Verified local runtime now reads combined 20-topic artifacts, Platform and top-five source graphs count unique topic comments, Four selected-topic cards: unique comments, share, source roots and topic c_v, Term bars show bounded phrase presence in unique filtered sentences (+9 more)

### Community 14 - "Topik dan Verifikasi NLP"
Cohesion: 0.20
Nodes (10): Merged corpus: 29, 099 rows, 1, 517 roots and 27, 582 comments/replies, Combined workbook provenance PASS with immutable source hashes and row lineage, identity(), main(), merge(), Merge compact crawl workbooks, rejecting repeated native content identities., Return global native object ID plus its root; text never defines identity., sha() (+2 more)

### Community 15 - "Identitas dan Kontrak Data"
Cohesion: 0.18
Nodes (10): ContentInput, Dataset, KeywordMatcher, MemorySink, native_fullname(), object_key(), Aho-Corasick; offsets refer to Python Unicode code points in source., Shared pipeline; adapters cannot choose their own headers or cell formats. (+2 more)

### Community 16 - "Parser DOM Terbatas"
Cohesion: 0.18
Nodes (8): HTMLParser, assert_accessible(), BoundedDom, content_node(), Node, Small serialised-DOM reader, not a browser or full HTML5 repair engine., rendered_text(), walk()

### Community 17 - "Pengujian Penjelasan Topik"
Cohesion: 0.26
Nodes (3): ExplanationTests, model_from_counts(), profile()

### Community 18 - "Coherence dan Quality Gate"
Cohesion: 0.17
Nodes (15): Obsidian method: weighted Ward to 20 final topics, Stored protocol, reference hash, baseline identity and per-topic scores, Additional c_v >=0.4 gate preserves earlier eligibility rules, Configured c_v threshold 0.4 with topn 10 and window 110, DBSCAN core points and noise without membership probabilities, Original DBSCAN IDs and full reduction mapping survive final topic IDs, Two UMAP 10 D projections seeded 42 and 43, Euclidean DBSCAN with reusable bounded radius graphs (+7 more)

### Community 19 - "Validasi Redirect dan Kesalahan"
Cohesion: 0.21
Nodes (9): Exception, HTTPRedirectHandler, HtmlPage, PublicHtmlSource, Only public HTML pages on the canonical host; never auth/API routes., RestrictedRedirect, safe_web_url(), SourceFailure (+1 more)

### Community 22 - "Coherence dan Quality Gate"
Cohesion: 0.21
Nodes (13): Combined20 runtime and desktop/narrow-screen topic QA verified, Combined-corpus training completed:20topics, c_v 0.4720034333858867, Combined 20 topics:mean c_v 0.4720 passes;7/20 individually below 0.4, Requested DBSCAN clustering, Requested SBERT-based embeddings, Local main.py runtime documented healthy, non-root and read-only, Combined-corpus mean c_v 0.4720034333858867 meets 0.4, Pinned multilingual SentenceTransformer safetensors encoder (+5 more)

### Community 23 - "Coherence dan Quality Gate"
Cohesion: 0.15
Nodes (13): Internal model metrics do not establish accuracy or representativeness, Historical 28 October 2026 coherence retrain: 52 topics, c_v 0.40970330118194137, Historical fixed top10/window110/all15878-unique macro c_v protocol, Obsidian c_v corpus and token protocol, Combined-corpus c_v 0.4720034334 passes with7/20 individual shortfalls, Unweighted mean across all 20 final non-noise topics, Gensim c_v protocol: top 10 terms, window 110, phrase tokens, Reference corpus: all 46143 unique embedding_text sentences including noise (+5 more)

### Community 24 - "Arsitektur Crawler dan Dependensi"
Cohesion: 0.17
Nodes (13): Bounded native-ID evidence and explicit uncertainty, Obsidian: Crawler Selenium architecture, Shared BundleSink and dual-workbook export path, Shared rendered_thread_dom.mjs extraction, Pinned openpyxl and yt-dlp crawler dependencies, Pinned Selenium 4.51.0 plus crawler requirements, Relative dates remain calendar estimates, Full crawl: 500 roots per platform within one hour (+5 more)

### Community 25 - "Helper Campaign Browser"
Cohesion: 0.27
Nodes (8): classifyCaptureFailure(), enrichBatch(), rateLimitSeconds(), inWindow(), mergeCandidates(), row, source, window

### Community 27 - "Arsitektur Crawler dan Dependensi"
Cohesion: 0.25
Nodes (11): Isolated dashboard-runtime matrix for Python 3.12 and3.14, Cloud AppTest regression opens all five views/T04 without installed or imported training libraries, Docker runtime ARG selects Python 3.12 or3.14 and installs only root wheels, Architecture separates saved-artifact deployment from full training/dev packages, Obsidian runbook records Python 3.14 failure and dashboard-only packaging fix, Historical Python 3.14.10 Cloud install failure:ONNX cp314 wheels and Numba support, Cloud root requirements now install dashboard-only dependencies, Root Community Cloud requirements include only dashboard runtime (+3 more)

### Community 30 - "Runbook dan Verifikasi Lokal"
Cohesion: 0.31
Nodes (9): Full Python 3.12 NLP/UI/crawler regressions use requirements-dev.txt, CI verifies full Python 3.12 tooling separately from dashboard-only Python 3.12/3.14 matrix, New-corpus native SBERT encoding or exact verified cache reuse, Separate SBERT training and artifact-only dashboard environments, Training/evaluation-only Gensim coherence requirements, Separate Python 3.12 development/training regression dependency entry, NLP, Streamlit and Plotly dependency ranges, Platform-specific macOS Intel Torch and numerical compatibility (+1 more)

### Community 31 - "Eksplorasi Dashboard Streamlit"
Cohesion: 0.32
Nodes (5): Responsive cards, visible keyboard focus and chart/table alternatives verified, _explain_filtered(), _load_artifacts(), main(), Streamlit entry point for local and Community Cloud dashboards.  Training lives

### Community 32 - "Eksplorasi Dashboard Streamlit"
Cohesion: 0.33
Nodes (4): _graph_positions(), Bounded topic graph: volume from filtered rows, semantic edges from the full mod, Keep the full-model layout stable while volume and edge filters change., DashboardTests

### Community 33 - "Coherence dan Quality Gate"
Cohesion: 0.67
Nodes (5): Cloud publication includes model code, config and complete checksummed active snapshot, Community Cloud entry point:root main.py, repo SakaHeroji/BeeSense, branch main, Python 3.12, Cloud uses relative artifacts and platform-controlled bind; local loopback stays explicit, Active artifact directory outputs/nlp_20261029_combined_topics20_01, Configured merged workbook identity and SHA-256

### Community 34 - "Snapshot NLP dan Arsip"
Cohesion: 0.40
Nodes (5): Historical Graphify memory of the native SBERT/UMAP/DBSCAN migration, Four retained prior NLP snapshots, including old-corpus 20-topic run, BeeSense project and dashboard runbook, Documented coordinator 1.3 cooldown 360 seconds with at most 3 retries, Unchanged compact source and eight-sheet audit workbooks

## Knowledge Gaps
- **21 isolated node(s):** `window`, `source`, `row`, `candidate`, `Checkpoint export to the eight-sheet contract` (+16 more)
  These have ≤1 connection - possible missing edges or undocumented components.
- **8 thin communities (<3 nodes) omitted from report** — run `graphify query` to explore isolated nodes.

## Suggested Questions
_Questions this graph is uniquely positioned to answer:_

- **Why does `SocialCrawler` connect `Alur Akuisisi Sosial Terpadu` to `Arsitektur Crawler dan Dependensi`, `Alur Akuisisi Sosial Terpadu`, `Crawler Selenium Terisolasi`?**
  _High betweenness centrality (0.327) - this node is a cross-community bridge._
- **Why does `file_hash()` connect `Pipeline dan Persistensi NLP` to `Alur Akuisisi Sosial Terpadu`, `Adapter Akuisisi YouTube`, `Bundle Excel dan Provenans`, `Eksplorasi Dashboard Streamlit`?**
  _High betweenness centrality (0.322) - this node is a cross-community bridge._
- **Why does `SocialNLPClusterer` connect `Pipeline dan Persistensi NLP` to `Coherence dan Quality Gate`, `Snapshot NLP dan Arsip`, `Snapshot NLP dan Arsip`, `Pengujian Penjelasan Topik`, `Coherence dan Quality Gate`, `Pengujian UI Streamlit`, `Coherence dan Quality Gate`, `Coherence dan Quality Gate`, `Arsitektur Crawler dan Dependensi`, `Eksplorasi Dashboard Streamlit`?**
  _High betweenness centrality (0.222) - this node is a cross-community bridge._
- **Are the 8 inferred relationships involving `SocialNLPClusterer` (e.g. with `Published 15-candidate DBSCAN grid preserves 8 million-edge guard` and `New combined-corpus SBERT and dual-UMAP features reused only through exact verified caches`) actually correct?**
  _`SocialNLPClusterer` has 8 INFERRED edges - model-reasoned connections that need verification._
- **Are the 4 inferred relationships involving `SocialCrawler` (e.g. with `_SeleniumSource` and `SocialCrawlerSelenium`) actually correct?**
  _`SocialCrawler` has 4 INFERRED edges - model-reasoned connections that need verification._
- **Are the 3 inferred relationships involving `SocialNLPStreamlitApp` (e.g. with `Cloud AppTest regression opens all five views/T04 without installed or imported training libraries` and `Platform and top-five source graphs count unique topic comments`) actually correct?**
  _`SocialNLPStreamlitApp` has 3 INFERRED edges - model-reasoned connections that need verification._
- **What connects `window`, `source`, `row` to the rest of the system?**
  _21 weakly-connected nodes found - possible documentation gaps or missing edges._
## Extraction limitations

AST token cost: 0. Semantic extraction ran through the delegated host agent; token accounting is unavailable. Displayed zero semantic counters are placeholders, not measured zero cost.

Raw changed-source diagnostics (including unresolved external AST symbols): {"dangling_endpoint_edges": 152, "missing_endpoint_edges": 0, "self_loop_edges": 0, "undirected_same_endpoint_collapsed_edges": 8}. Exported graph endpoints and hyperedge membership were checked separately and are valid.

Cloud dependency repair: the user log showed Python 3.14.10 failing before UI startup on ONNX 1.23.2 cp314 wheels and Numba 0.61.2. Root requirements now install the artifact/UI runtime only; Python 3.12/3.14 use compatible NumPy wheels, while the full Python 3.12 development/training lock is preserved separately. Docker installs wheels only and CI opens all five shipped-artifact views without any training libraries on both versions. Validation results are recorded separately in output/cloudfix_verification.json; no Cloud success is assumed by this graph. The dashboard entry point has been renamed from nlp_dashboard.py to main.py for Streamlit Community Cloud (Python 3.12); Docker, CI, test imports, documentation and Obsidian links use main.py. Graph identifiers and source paths were migrated before fresh AST extraction to preserve incoming references. The existing undirected graph is preserved. Same-endpoint relationships may collapse in this view; call direction is not a rollout dependency claim. Configuration JSON and curated Obsidian notes are mapped explicitly. The crawler campaign has a shared three-hour acquisition deadline, round-robin scheduling, canonical/native historical exclusions, manual CAPTCHA wait and atomic progress. Targets are distinct from collected totals. Acquisition is finalized PARTIAL: YouTube 1188 exported/300 qualified and Reddit 98/58. Baseline plus acquisition yields 29099 rows with no duplicate native IDs. The active combined snapshot has 20 topics and mean c_v 0.4720034333858867 (7 individual topics below 0.4), four new Parquets and verified non-root/read-only local dashboard runtime. Desktop, actual 433px narrow layout and keyboard focus were verified; 68 NLP/UI tests passed. Historical snapshots remain intact and their different-corpus scores are not direct comparisons.
