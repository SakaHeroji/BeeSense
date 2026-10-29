# Graph Report - /Users/socs3/Documents/BeeSense  (2026-10-29)

## Corpus Check
- 40 files · ~31,541 words
- Verdict: corpus is large enough that graph structure adds value.

## Summary
- 1168 nodes · 2577 edges · 82 communities (69 shown, 13 thin omitted)
- Extraction: 93% EXTRACTED · 7% INFERRED · 0% AMBIGUOUS · INFERRED: 178 edges (avg confidence: 0.82)
- Token cost: 0 input · 0 output

## Graph Freshness
- Built from commit: `cd29d710`
- Run `git rev-parse HEAD` and compare to check if the graph is stale.
- Run `graphify update .` after code changes (no API cost).

## Community Hubs (Navigation)
- Eksplorasi Dashboard Streamlit
- Adapter Akuisisi YouTube
- Crawler Selenium Terisolasi
- Alur Akuisisi Sosial Terpadu
- Konfigurasi Tujuh Sumber
- Monitor Akuisisi Sintetis
- Pipeline dan Persistensi NLP
- Alur Akuisisi Sosial Terpadu
- Workspace React Crawler
- Pipeline dan Persistensi NLP
- Bundle Excel dan Provenans
- Akses dan Parsing HTML
- Monitor Akuisisi Sintetis
- Topik dan Verifikasi NLP
- Parser dan Runner Reddit
- Ekspor Campaign dan Resume
- Workspace React Crawler
- Monitor Akuisisi Sintetis
- Identitas dan Kontrak Data
- Konfigurasi SocialCrawler
- Runner Playwright Reddit
- Topik dan Verifikasi NLP
- Identitas dan Kontrak Data
- Workspace React Crawler
- Parser DOM Terbatas
- Pipeline dan Persistensi NLP
- Pengujian Penjelasan Topik
- Snapshot NLP dan Arsip
- PRD Workspace Crawler
- Workspace React Crawler
- PRD Workspace Crawler
- PRD Workspace Crawler
- Validasi Redirect dan Kesalahan
- Pengujian UI Streamlit
- Kontrak API Crawler
- Alur Akuisisi Sosial Terpadu
- Helper Campaign Browser
- Verifikasi Dataset Berversi
- Snapshot NLP dan Arsip
- Runbook dan Verifikasi Lokal
- Arsitektur Crawler dan Dependensi
- Workspace React Crawler
- Validasi Respons Survei
- Coherence dan Quality Gate
- Arsitektur Crawler dan Dependensi
- Coherence dan Quality Gate
- PRD Workspace Crawler
- Coherence dan Quality Gate
- Pipeline dan Persistensi NLP
- Alur Akuisisi Sosial Terpadu
- PRD Workspace Crawler
- Workspace React Crawler
- Eksplorasi Dashboard Streamlit
- Alur Akuisisi Sosial Terpadu
- PRD Workspace Crawler
- Workspace React Crawler
- Alur Akuisisi Sosial Terpadu
- Coherence dan Quality Gate
- Pipeline dan Persistensi NLP
- Snapshot NLP dan Arsip
- Coherence dan Quality Gate
- Workspace React Crawler
- Ekstraksi Cuplikan Publik
- Pipeline dan Persistensi NLP
- Workspace React Crawler
- Workspace React Crawler
- Workspace React Crawler
- Workspace React Crawler
- Workspace React Crawler
- Workspace React Crawler
- Memori Startup Dashboard

## God Nodes (most connected - your core abstractions)
1. `SocialNLPClusterer` - 79 edges
2. `SocialCrawler` - 58 edges
3. `SocialNLPStreamlitApp` - 52 edges
4. `SocialCrawlerTests` - 41 edges
5. `Runbook and historical record for finalized partial crawler campaign` - 30 edges
6. `NLPTests` - 26 edges
7. `SocialCrawlerSelenium` - 24 edges
8. `file_hash()` - 23 edges
9. `Crawler frontend PRD v1.1 with implemented seven-source UI and pending backend` - 22 edges
10. `run()` - 21 edges

## Surprising Connections (you probably didn't know these)
- `Configured coordinator 1.3 Reddit policy cooldown:360 seconds` --conceptually_related_to--> `SocialCrawler 1.3 bounded HTTP 429 cooldown policy`  [INFERRED]
  social_crawler.json → SOCIAL_CRAWLER.md
- `Configured coordinator 1.3 Reddit retry cap:3 per run` --conceptually_related_to--> `SocialCrawler 1.3 bounded HTTP 429 cooldown policy`  [INFERRED]
  social_crawler.json → SOCIAL_CRAWLER.md
- `Configured c_v threshold 0.4 with topn 10 and window 110` --conceptually_related_to--> `Additional c_v >=0.4 gate preserves earlier eligibility rules`  [INFERRED]
  social_nlp.json → SOCIAL_NLP.md
- `Historical fixed top10/window110/all15878-unique macro c_v protocol` --semantically_similar_to--> `Gensim c_v protocol: top 10 terms, window 110, phrase tokens`  [INFERRED] [semantically similar]
  graphify-out/memory/query_20261028_155746_hitung_coherence_minimal_0_4__retrain_sbert_umap_d.md → SOCIAL_NLP.md
- `SocialNLPClusterer` --implements--> `Two UMAP 10 D projections seeded 42 and 43`  [EXTRACTED]
  social_nlp.py → SOCIAL_NLP.md

## Import Cycles
- None detected.

## Hyperedges (group relationships)
- **Verified synthetic React delivery remains separate from proposed production worker/API acceptance** — crawler_frontend_readme_react_crawler_implementation, crawler_frontend_docs_delivery_verified_frontend_checks, crawler_frontend_docs_delivery_synthetic_demo_limitations, crawler_frontend_docs_api_contract_expected_api_contract, prd_prd_backend_readme_persistent_acquisition_worker, prd_prd_frontend_acceptance_criteria_crawler_production_acceptance_gates [INFERRED 0.95]
- **Complete survey/native-source provenance and validated schema gates protect immutable NLP selection** — prd_prd_frontend_prd_frontend_crawler_complete_response_survey_contract, prd_prd_frontend_prd_frontend_crawler_native_identity_provenance_rules, prd_prd_frontend_prd_frontend_crawler_immutable_dataset_nlp_selection, crawler_frontend_docs_api_contract_server_bound_survey_validation_commit, prd_prd_machine_learning_readme_survey_schema_adapter_requirement, crawler_frontend_readme_preview_export_and_schema_gate, prd_prd_machine_learning_readme_new_social_source_adapter_gate [INFERRED 0.95]
- **Bounded qualifying-root campaign with shared scheduler and manual CAPTCHA** — social_crawler_round_robin_deadline, social_crawler_campaign_qualified_targets, social_crawler_manual_captcha_wait, social_crawler_partial_bundle_reporting [EXTRACTED 1.00]
- **Historical identity exclusion with pre-request and export duplicate guards** — social_crawler_historical_root_identity, social_crawler_root_identity_guards, social_crawler_per_run_root_deduplication, social_crawler_atomic_live_progress [INFERRED 0.85]
- **Coordinator 1.3 retry contract: policy, same operation, readiness, deadline and audit** — social_crawler_next_run_bounded_cooldown, social_crawler_pending_failed_operation_retry, social_crawler_cooldown_ready_scheduler, social_crawler_rate_limit_timing_audit, social_crawler_round_robin_deadline [EXTRACTED 1.00]
- **Frozen native SBERT, UMAP, DBSCAN, sentence-weighted Ward and final c-TF-IDF labels** — social_nlp_native_sbert, social_nlp_overflow_normalization, social_nlp_dual_umap, social_nlp_euclidean_dbscan, social_nlp_sentence_weighted_ward, social_nlp_ctfidf [EXTRACTED 1.00]
- **Fixed c_v token protocol, full unique reference corpus and unweighted aggregate** — social_nlp_coherence_protocol, social_nlp_coherence_reference, social_nlp_coherence_aggregation, social_nlp_invalid_topic_failure [EXTRACTED 1.00]
- **Combined-corpus global coherence with historical incomparable baselines,individual shortfalls and in-sample limits** — social_nlp_coherence_result, social_nlp_unchanged_baseline, social_nlp_individual_shortfalls, social_nlp_insample_limit, social_nlp_original_space_silhouette [EXTRACTED 1.00]
- **Dashboard-only dependencies,Docker wheels and isolated dual-Python regression** — requirements_dashboard_ui_artifact_dependencies, requirements_dashboard_python_numpy_markers, dockerfile_dashboard_wheels_python_version, _github_workflows_ci_dashboard_runtime_isolation, _github_workflows_ci_shipped_artifact_cloud_regression [INFERRED 0.95]
- **Shared social workbook contract** — selenium_crawler_inherited_export, social_crawler_compact_excel, social_crawler_audit_bundle, graphify_out_obsidian_crawler_selenium_shared_excel [EXTRACTED 1.00]

## Communities (82 total, 13 thin omitted)

### Community 0 - "Eksplorasi Dashboard Streamlit"
Cohesion: 0.05
Nodes (27): Filters retain model membership and do not recompute c_v, Selected-topic c_v card is separate from the full-model mean, Occurrences, unique sentences, comments and source roots have different denominators, Five artifact-backed Streamlit analysis views, Platform and top-five source graphs count unique topic comments, Responsive cards, visible keyboard focus and chart/table alternatives verified, Four selected-topic cards: unique comments, share, source roots and topic c_v, Term bars show bounded phrase presence in unique filtered sentences (+19 more)

### Community 1 - "Adapter Akuisisi YouTube"
Cohesion: 0.09
Nodes (34): SourceAdapter, error_code(), load_settings(), main(), parser(), run(), SafeLogger, Settings (+26 more)

### Community 2 - "Crawler Selenium Terisolasi"
Cohesion: 0.07
Nodes (19): _barrier(), _create_driver(), main(), Content quoting an error is never used to classify an access barrier., Convert the shared rendered DOM capture without inventing identities., One browser operation. The parent enforces the hard process deadline., Stream evidence before completion; the original supervisor can retain it., Drop-in SocialCrawler with Selenium for both platforms and shared exports. (+11 more)

### Community 3 - "Alur Akuisisi Sosial Terpadu"
Cohesion: 0.12
Nodes (7): Return a local date for display; relative source dates stay estimates., Clock, rd_events(), receipt(), SocialCrawlerTests, spawn_youtube_fixture(), yt_events()

### Community 4 - "Konfigurasi Tujuh Sumber"
Cohesion: 0.15
Nodes (26): Automatic(), Baselines(), ConfigFields(), ConfigReview(), ManualUrl(), useApp(), csvCell(), initialConfig() (+18 more)

### Community 5 - "Monitor Akuisisi Sintetis"
Cohesion: 0.21
Nodes (24): Shell(), DatasetView(), History(), Composition(), JobDetail(), liveStates, PlatformCard(), ProgressChart() (+16 more)

### Community 6 - "Pipeline dan Persistensi NLP"
Cohesion: 0.14
Nodes (5): Encode with SBERT, fit UMAP + DBSCAN and optionally merge to a topic count., SocialNLPClusterer, encoder(), fixture(), NLPTests

### Community 7 - "Alur Akuisisi Sosial Terpadu"
Cohesion: 0.10
Nodes (10): Atomic sibling .progress.json snapshots during acquisition, main(), Describe the acquisition backend independently of the shared export., Compose the original adapters and workers; one JSON configuration and bundle., Validate and return the effective plan without browser/network access., Project the full audit rows into one sheet, applying current filters., Re-export saved Contents without network or modifying the source bundle., Root-publication date and literal keyword selection (+2 more)

### Community 8 - "Workspace React Crawler"
Cohesion: 0.07
Nodes (26): compilerOptions, allowImportingTsExtensions, esModuleInterop, isolatedModules, jsx, lib, module, moduleResolution (+18 more)

### Community 9 - "Pipeline dan Persistensi NLP"
Cohesion: 0.17
Nodes (8): main(), Verify published source workbooks and the dashboard artifact bundle., verify(), file_hash(), json_write(), main(), Publish a new versioned sidecar; never modify the original run., Reuse immutable SBERT features only after verifying data/model identity.

### Community 10 - "Bundle Excel dan Provenans"
Cohesion: 0.17
Nodes (13): add_readme(), BundleSink, dumps(), main(), now_iso(), parser(), Validate the embedded contract; an external descriptor is optional., Atomic new directory; streaming JSONL + streaming, formula-safe Excel. (+5 more)

### Community 11 - "Akses dan Parsing HTML"
Cohesion: 0.22
Nodes (8): bounded_events(), first(), fixture_page(), Whole-post comment budget includes replies; nested replies share thread cap., RedditHtmlParser, RedditTests, source_time(), worker()

### Community 12 - "Monitor Akuisisi Sintetis"
Cohesion: 0.11
Nodes (19): AppContext, FieldErrorsContext, demoApi, Baseline, Capabilities, Counts, DatasetDetail, DatasetFile (+11 more)

### Community 13 - "Topik dan Verifikasi NLP"
Cohesion: 0.20
Nodes (22): Historical active-campaign state; acquisition now finalized PARTIAL, Before segment 03: qualified YouTube6/Reddit17; exported evidence8/31, Before 04 cumulative qualified YouTube77/Reddit26; evidence325/47, Campaign descriptor records finalized PARTIAL status and five-segment accounting, Historical descriptor-based monitoring now resolves final campaign counters, Historical user request for fifteen-minute updates during active acquisition monitoring, Historical preparation restriction: cooldown implemented without restarting segment 03, New user authorization supersedes historical preparation-only restriction (+14 more)

### Community 14 - "Parser dan Runner Reddit"
Cohesion: 0.13
Nodes (11): HtmlSource, load_settings(), LocalHtmlSource, parsed_number(), ABC, Normalize a source event; write only through the shared Dataset/Sink., run_worker(), Settings (+3 more)

### Community 15 - "Ekspor Campaign dan Resume"
Cohesion: 0.13
Nodes (3): export_campaign(), load_campaign(), ResumeTests

### Community 16 - "Workspace React Crawler"
Cohesion: 0.10
Nodes (21): devDependencies, eslint, @eslint/js, jsdom, prettier, @testing-library/user-event, @types/react, @types/react-dom (+13 more)

### Community 17 - "Monitor Akuisisi Sintetis"
Cohesion: 0.13
Nodes (18): advance(), cap, committed, dataset(), get(), load(), plans, reviews (+10 more)

### Community 18 - "Identitas dan Kontrak Data"
Cohesion: 0.18
Nodes (5): ContractTests, digest(), RecordFactory, utc_datetime(), validate_row()

### Community 19 - "Konfigurasi SocialCrawler"
Cohesion: 0.18
Nodes (18): 1000 qualified-root targets per platform within shared three-hour budget, Historical Reddit pause: ten qualified and seventeen exported evidence posts, Configured 1000 new posts per platform, shared three-hour campaign, Original deadline stopped acquisition; no operation started afterward, Target 1000 qualified new roots per platform, bounded attempts and candidates, Per-platform bounds: max_posts 4000, max_candidates 6000, Configured global acquisition budget 10800 seconds, Configured coordinator 1.3 Reddit policy cooldown:360 seconds (+10 more)

### Community 20 - "Runner Playwright Reddit"
Cohesion: 0.23
Nodes (12): atomic_json(), barrier_status(), campaign_plan(), decode_cli_output(), find_cli(), PlaywrightCLI, rate_limit_seconds(), run() (+4 more)

### Community 21 - "Topik dan Verifikasi NLP"
Cohesion: 0.20
Nodes (10): Merged corpus: 29, 099 rows, 1, 517 roots and 27, 582 comments/replies, Combined workbook provenance PASS with immutable source hashes and row lineage, identity(), main(), merge(), Merge compact crawl workbooks, rejecting repeated native content identities., Return global native object ID plus its root; text never defines identity., sha() (+2 more)

### Community 22 - "Identitas dan Kontrak Data"
Cohesion: 0.18
Nodes (10): ContentInput, Dataset, KeywordMatcher, MemorySink, native_fullname(), object_key(), Aho-Corasick; offsets refer to Python Unicode code points in source., Shared pipeline; adapters cannot choose their own headers or cell formats. (+2 more)

### Community 23 - "Workspace React Crawler"
Cohesion: 0.12
Nodes (17): dependencies, @fontsource-variable/plus-jakarta-sans, lucide-react, papaparse, react, react-dom, react-router-dom, @tanstack/react-query (+9 more)

### Community 24 - "Parser DOM Terbatas"
Cohesion: 0.18
Nodes (8): HTMLParser, assert_accessible(), BoundedDom, content_node(), Node, Small serialised-DOM reader, not a browser or full HTML5 repair engine., rendered_text(), walk()

### Community 25 - "Pipeline dan Persistensi NLP"
Cohesion: 0.13
Nodes (5): Use the same class TF-IDF vocabulary for selection and publication., Macro c_v on ALL non-noise topics and a fixed full-corpus reference.          Un, Preserve explicit zero distances, including identical sentence vectors., Merge entire DBSCAN groups using sentence-weighted Ward linkage.          Minimi, Select DBSCAN parameters on UMAP; evaluate in original SBERT geometry.

### Community 26 - "Pengujian Penjelasan Topik"
Cohesion: 0.26
Nodes (3): ExplanationTests, model_from_counts(), profile()

### Community 27 - "Snapshot NLP dan Arsip"
Cohesion: 0.15
Nodes (16): Prior Graphify memory: Selenium crawler preserves Excel contract, BeeSense crawler, NLP and dashboard class architecture, React host/container addition preserves existing acquisition/model artifacts, Saved-artifact Dashboard packages and full training/dev environment remain separate, EXTRACTED source quotations versus INFERRED topic interpretations, Existing Python data/model pipeline and new React workspace remain separate, Curated demo storage and API-mode failure boundaries, Curated React Crawler implementation with synthetic/API separation (+8 more)

### Community 28 - "PRD Workspace Crawler"
Cohesion: 0.17
Nodes (15): Final style samples:96desktop/78narrow444px elements,all black and≥13 px, React frontend and simulation verified; production acquisition integration unavailable, Applied UX fixes:linked errors, step validation, deep links, drawer focus and inertness, Browser actual widths400/444px;requested360px remains unproven, Production release waits for API/worker/access/export and survey adapter integration, Demo IDs, baseline data and downloads are synthetic rather than acquisition evidence, Production build defaults API mode;missing backend fails explicitly, Implemented adapter polls snapshots every five seconds;worker state stays server-owned (+7 more)

### Community 30 - "PRD Workspace Crawler"
Cohesion: 0.19
Nodes (14): locatorKey is normalized permalink identity;nativeId may await backend verification, Survey commit binds review to session/project and revalidates conflicts, Implemented UI flows:automatic/manual, monitor, survey and dataset review, Frontend URL review and minat-studi-v1 survey form/CSV/XLSX workflows, Proposed server-owned monitor separates units and finalization states, Automatic four-step source/filter/baseline/review workflow, Proposed survey schema preserves declared roles, questions, permission and whole responses, Crawler frontend PRD v1.1 with implemented seven-source UI and pending backend (+6 more)

### Community 31 - "PRD Workspace Crawler"
Cohesion: 0.16
Nodes (14): Late plan, URL and survey validation is ignored after input changes, Draft acceptance criteria are release requirements, not a React test report, Acceptance: plan invalidation, field errors and idempotent job creation, Acceptance: complete consented survey responses and conflict-safe import, Acceptance: authoritative snapshots, stale recovery and worker barriers, Crawler wireframes are illustrative design requirements, not app screenshots, Monitor prioritizes status, units, barriers and next actions over logs, Worker-session CAPTCHA and429 UI offer observation rather than bypass (+6 more)

### Community 32 - "Validasi Redirect dan Kesalahan"
Cohesion: 0.21
Nodes (9): Exception, HTTPRedirectHandler, HtmlPage, PublicHtmlSource, Only public HTML pages on the canonical host; never auth/API routes., RestrictedRedirect, safe_web_url(), SourceFailure (+1 more)

### Community 34 - "Kontrak API Crawler"
Cohesion: 0.19
Nodes (9): ApiError, base, httpApi, post(), request(), Config, Job, Plan (+1 more)

### Community 35 - "Alur Akuisisi Sosial Terpadu"
Cohesion: 0.26
Nodes (12): Cooldown verification:50 crawler tests, 49pass/1skip;12 Reddit runner tests pass, Obsidian records bounded retry policy and chronological authorization, Round-robin advances YouTube while Reddit waits for readiness, SocialCrawler 1.3 bounded HTTP 429 cooldown policy, Retain the same failed Reddit operation until cooldown expires, Per-run canonical root duplicate guard, Persist actual 429 finish timestamps, cooldown deadline and retry decisions, Return an explicit target/shortfall report and write one atomic bundle. (+4 more)

### Community 36 - "Helper Campaign Browser"
Cohesion: 0.27
Nodes (8): classifyCaptureFailure(), enrichBatch(), rateLimitSeconds(), inWindow(), mergeCandidates(), row, source, window

### Community 38 - "Snapshot NLP dan Arsip"
Cohesion: 0.20
Nodes (12): Active combined 20-topic run with eleven artifacts and manifest, Historical scores are not directly comparable with combined-corpus c_v, Obsidian dashboard dataset provenance, Artifact-only dashboard without Gensim/Torch imports, Obsidian Cloud runbook:main.py, Python 3.12 and complete artifact publication, BeeSense startup, verification and coherence training runbook, Active combined 20-topic result:DBSCAN eps0.2/min_samples 10, Four Parquet files, UMAP npz and eleven-artifact v 2 manifest (+4 more)

### Community 39 - "Runbook dan Verifikasi Lokal"
Cohesion: 0.24
Nodes (11): Full Python 3.12 NLP/UI/crawler regressions use requirements-dev.txt, CI verifies full Python 3.12 tooling separately from dashboard-only Python 3.12/3.14 matrix, New-corpus native SBERT encoding or exact verified cache reuse, Separate SBERT training and artifact-only dashboard environments, Training/evaluation-only Gensim coherence requirements, Pinned openpyxl and yt-dlp crawler dependencies, Separate Python 3.12 development/training regression dependency entry, NLP, Streamlit and Plotly dependency ranges (+3 more)

### Community 40 - "Arsitektur Crawler dan Dependensi"
Cohesion: 0.27
Nodes (11): Isolated dashboard-runtime matrix for Python 3.12 and3.14, Cloud AppTest regression opens all five views/T04 without installed or imported training libraries, Docker runtime ARG selects Python 3.12 or3.14 and installs only root wheels, Obsidian runbook records Python 3.14 failure and dashboard-only packaging fix, Historical Python 3.14.10 Cloud install failure:ONNX cp314 wheels and Numba support, PyArrow 24.0.0 matches Cloud guard for Arrow/mimalloc threaded-import compatibility, Cloud root requirements now install dashboard-only dependencies, Root Community Cloud requirements include only dashboard runtime (+3 more)

### Community 41 - "Workspace React Crawler"
Cohesion: 0.18
Nodes (11): scripts, build, build:demo, check, dev, format, format:check, lint (+3 more)

### Community 42 - "Validasi Respons Survei"
Cohesion: 0.20
Nodes (9): labels, sample, Survey(), WorkbookData, download(), SurveyField, surveyFields, Field() (+1 more)

### Community 43 - "Coherence dan Quality Gate"
Cohesion: 0.25
Nodes (11): Combined20 runtime and desktop/narrow-screen topic QA verified, Combined-corpus training completed:20topics, c_v 0.4720034333858867, Requested DBSCAN clustering, Requested SBERT-based embeddings, Combined-corpus mean c_v 0.4720034333858867 meets 0.4, Pinned multilingual SentenceTransformer safetensors encoder, New combined-corpus SBERT and dual-UMAP features reused only through exact verified caches, Overflow-window averaging and L 2-normalized 384 D embeddings (+3 more)

### Community 44 - "Arsitektur Crawler dan Dependensi"
Cohesion: 0.20
Nodes (11): Bounded native-ID evidence and explicit uncertainty, Obsidian: Crawler Selenium architecture, Shared BundleSink and dual-workbook export path, Shared rendered_thread_dom.mjs extraction, Relative dates remain calendar estimates, Full crawl: 500 roots per platform within one hour, Worker hard deadline preserves streamed partial events, Separate non-root crawler container with Selenium Grid (+3 more)

### Community 45 - "Coherence dan Quality Gate"
Cohesion: 0.25
Nodes (11): Obsidian method: weighted Ward to 20 final topics, Additional c_v >=0.4 gate preserves earlier eligibility rules, DBSCAN core points and noise without membership probabilities, Two UMAP 10 D projections seeded 42 and 43, Euclidean DBSCAN with reusable bounded radius graphs, Published 15-candidate DBSCAN grid preserves 8 million-edge guard, Evaluate final topic partitions before candidate selection, Combined-corpus two-seed final-topic ARI 0.7642290252255706 (+3 more)

### Community 46 - "PRD Workspace Crawler"
Cohesion: 0.22
Nodes (10): Dataset.nlpSupported requires tested schema and every included source adapter, Versioned datasets provide50-row pages, authorized files and selection-only NLP handoff, Demo preview-only downloads and validated-source NLP gate, Curated available UI flows retain worker authority and survey metadata, New survey schema must preserve role, question, response, version and permission, Version/checksum handoff requires partial acceptance and supported schema, Machine Learning PRD remains unwritten; Crawler handoff dependencies listed, 20 topics/coherence≥0.4 belong to future model criteria, not Crawler success (+2 more)

### Community 47 - "Coherence dan Quality Gate"
Cohesion: 0.20
Nodes (10): Historical 28 October 2026 coherence retrain: 52 topics, c_v 0.40970330118194137, Historical fixed top10/window110/all15878-unique macro c_v protocol, Obsidian c_v corpus and token protocol, Unweighted mean across all 20 final non-noise topics, Stored protocol, reference hash, baseline identity and per-topic scores, Gensim c_v protocol: top 10 terms, window 110, phrase tokens, Reference corpus: all 46143 unique embedding_text sentences including noise, Original DBSCAN IDs and full reduction mapping survive final topic IDs (+2 more)

### Community 48 - "Pipeline dan Persistensi NLP"
Cohesion: 0.20
Nodes (4): _explain_filtered(), Identify the parent thread, not the individual comment URL., Evidence-grounded topic descriptions and descriptive, source-aware trends., Explain already verified artifacts without encoding or fitting again.

### Community 49 - "Alur Akuisisi Sosial Terpadu"
Cohesion: 0.27
Nodes (6): _config(), _keywords(), Omitted retry config defaults to zero retries for existing callers, _number(), Read root identities only; never alter the historical workbooks., _url()

### Community 50 - "PRD Workspace Crawler"
Cohesion: 0.22
Nodes (9): Increasing snapshotVersion and server-owned actions drive reconciliation, Delivery records 50 passing tests, lint/format and production API build, Curated PRD 1.1 theme and seven-source UI distinguish planned backend adapters, Backend PRD is not written; API/worker services remain proposed, Proposed persistent Python worker and authorized CAPTCHA browser bridge, Proposed server session, role, project isolation and idempotency, Proposed survey transactions, immutable datasets and operational audit, Proposed worker survives tab close; reconnect reconciles snapshots (+1 more)

### Community 51 - "Workspace React Crawler"
Cohesion: 0.22
Nodes (4): client, ErrorBoundary, router, Manual()

### Community 52 - "Eksplorasi Dashboard Streamlit"
Cohesion: 0.25
Nodes (9): Verified local runtime now reads combined 20-topic artifacts, On-demand explanations from active combined 20-topic artifacts, Historical v 1 HDBSCAN directional counts for 51 topics, Healthy combined 20 local Docker runtime serves the new model, MMR evidence and guarded Theil-Sen/Kendall directions, Source-bound beesense-topic-explanations:1 sidecar manifest, Traceable extractive topic explanations, Four immutable older NLP snapshots including baseline 20-topic run (+1 more)

### Community 53 - "Alur Akuisisi Sosial Terpadu"
Cohesion: 0.22
Nodes (9): Advanced connected-browser Reddit campaign helpers, Checkpoint export to the eight-sheet contract, Native-ID provenance and bounded public excerpts, Standalone runner stops 429; coordinator 1.3 supports bounded cooldown, Isolated Chrome profile, manual CAPTCHA wait and access-barrier stops, Coordinator waits for manual CAPTCHA without automated clicks, Reddit Playwright CLI runner, Reddit CAPTCHA wait 600 seconds, poll 5 seconds (+1 more)

### Community 54 - "PRD Workspace Crawler"
Cohesion: 0.25
Nodes (8): Server history pagination, SSE, templates and organizational login remain future, Project-prefixed cookie-session API requires server CORS/CSRF/access controls, Expected typed frontend API contract; backend implementation pending, Safe structured errors distinguish API429 from worker-platform429, Typed plan/job requests bind plan IDs, idempotency and safe stop, Backend wrapper must translate local WIB dates and TypeScript field names, Survey answers avoid URL/localStorage;safe text and CSV formula handling, Fresh server validation and one idempotency key precede job start

### Community 55 - "Workspace React Crawler"
Cohesion: 0.29
Nodes (6): engines, node, name, private, type, version

### Community 56 - "Alur Akuisisi Sosial Terpadu"
Cohesion: 0.33
Nodes (7): Historical audit workbook: 50 YouTube and 181 Reddit root identities, Inherited SocialCrawler filters and Excel exporters, JSONL audit, dataset.xlsx and checksum manifest, social_data.xlsx ten-column Data worksheet, Historical exclusion source outputs/social_20261028_01, Five verified segments consolidate with zero duplicate roots and zero baseline overlap, Read-only canonical/native identity index excludes 50 old YouTube and 181 Reddit roots

### Community 57 - "Coherence dan Quality Gate"
Cohesion: 0.52
Nodes (6): Cloud publication includes model code, config and complete checksummed active snapshot, Community Cloud entry point:root main.py, repo SakaHeroji/BeeSense, branch main, Python 3.12, Cloud uses relative artifacts and platform-controlled bind; local loopback stays explicit, Active artifact directory outputs/nlp_20261029_combined_topics20_01, Configured merged workbook identity and SHA-256, Configured c_v threshold 0.4 with topn 10 and window 110

### Community 59 - "Snapshot NLP dan Arsip"
Cohesion: 0.33
Nodes (6): Historical Graphify memory of the native SBERT/UMAP/DBSCAN migration, Four retained prior NLP snapshots, including old-corpus 20-topic run, BeeSense project and dashboard runbook, Local main.py runtime documented healthy, non-root and read-only, Documented coordinator 1.3 cooldown 360 seconds with at most 3 retries, Unchanged compact source and eight-sheet audit workbooks

### Community 60 - "Coherence dan Quality Gate"
Cohesion: 0.40
Nodes (5): Internal model metrics do not establish accuracy or representativeness, Combined-corpus c_v 0.4720034334 passes with7/20 individual shortfalls, 7 of 20 combined-corpus topics remain below c_v 0.4, Training-corpus coherence is not holdout or labeled accuracy, Combined-corpus original-space silhouette -0.00027895558741874993

### Community 61 - "Workspace React Crawler"
Cohesion: 0.50
Nodes (3): printWidth, singleQuote, trailingComma

## Knowledge Gaps
- **118 isolated node(s):** `window`, `source`, `row`, `candidate`, `Checkpoint export to the eight-sheet contract` (+113 more)
  These have ≤1 connection - possible missing edges or undocumented components.
- **13 thin communities (<3 nodes) omitted from report** — run `graphify query` to explore isolated nodes.

## Suggested Questions
_Questions this graph is uniquely positioned to answer:_

- **Why does `file_hash()` connect `Pipeline dan Persistensi NLP` to `Eksplorasi Dashboard Streamlit`, `Adapter Akuisisi YouTube`, `Pipeline dan Persistensi NLP`, `Alur Akuisisi Sosial Terpadu`, `Bundle Excel dan Provenans`, `Pipeline dan Persistensi NLP`?**
  _High betweenness centrality (0.235) - this node is a cross-community bridge._
- **Why does `SocialCrawler` connect `Alur Akuisisi Sosial Terpadu` to `Crawler Selenium Terisolasi`, `Alur Akuisisi Sosial Terpadu`, `Alur Akuisisi Sosial Terpadu`, `Arsitektur Crawler dan Dependensi`, `Topik dan Verifikasi NLP`, `Alur Akuisisi Sosial Terpadu`, `Konfigurasi SocialCrawler`, `Alur Akuisisi Sosial Terpadu`, `Alur Akuisisi Sosial Terpadu`?**
  _High betweenness centrality (0.229) - this node is a cross-community bridge._
- **Why does `SocialNLPClusterer` connect `Pipeline dan Persistensi NLP` to `Eksplorasi Dashboard Streamlit`, `Pengujian UI Streamlit`, `Pengujian Penjelasan Topik`, `Snapshot NLP dan Arsip`, `Arsitektur Crawler dan Dependensi`, `Pipeline dan Persistensi NLP`, `Coherence dan Quality Gate`, `Coherence dan Quality Gate`, `Coherence dan Quality Gate`, `Pipeline dan Persistensi NLP`, `Coherence dan Quality Gate`, `Pipeline dan Persistensi NLP`, `Snapshot NLP dan Arsip`, `Pipeline dan Persistensi NLP`, `Pipeline dan Persistensi NLP`?**
  _High betweenness centrality (0.140) - this node is a cross-community bridge._
- **Are the 8 inferred relationships involving `SocialNLPClusterer` (e.g. with `Published 15-candidate DBSCAN grid preserves 8 million-edge guard` and `New combined-corpus SBERT and dual-UMAP features reused only through exact verified caches`) actually correct?**
  _`SocialNLPClusterer` has 8 INFERRED edges - model-reasoned connections that need verification._
- **Are the 4 inferred relationships involving `SocialCrawler` (e.g. with `_SeleniumSource` and `SocialCrawlerSelenium`) actually correct?**
  _`SocialCrawler` has 4 INFERRED edges - model-reasoned connections that need verification._
- **Are the 3 inferred relationships involving `SocialNLPStreamlitApp` (e.g. with `Cloud AppTest regression opens all five views/T04 without installed or imported training libraries` and `Platform and top-five source graphs count unique topic comments`) actually correct?**
  _`SocialNLPStreamlitApp` has 3 INFERRED edges - model-reasoned connections that need verification._
- **What connects `window`, `source`, `row` to the rest of the system?**
  _118 weakly-connected nodes found - possible documentation gaps or missing edges._
## Frontend scope and verification


Incremental scope: 26 frontend structural files and 14 PRD/delivery/curated Obsidian documents. Existing crawler, NLP, historical dataset and Cloud deployment mappings are preserved. CSS, Nginx, Docker and the SVG logo are described through delivery/PRD notes; they are not claimed as AST-extracted code. Working-tree implementation is ahead of built_at_commit; this map does not claim a GitHub publication.


Frontend implements automatic and manual URL/survey acquisition UI, typed API transport and an explicitly synthetic adapter. Python SocialCrawler currently has YouTube/Reddit adapters only. Instagram, TikTok, Threads, Facebook and X/Twitter are UI/demo options; production adapters are planned and capability-gated. Backend HTTP/worker is not implemented. The seven-source monitor, series and filters are dynamic. Locator normalization is distinct from verified native IDs. NLP handoff for surveys and the five new sources is blocked pending schema adapters.


PRD 1.1 requires white/orange surfaces and accents, all text black #000000, actual text minimum 13px. Body/input 15px, labels/buttons 14px. No green theme, logo, status or chart. HTML chart labels avoid SVG scaling below the minimum. Desktop computed-style audit: 96 visible text/input elements, minimum 13px, no non-black text. Actual narrow layouts 400px and 444px were inspected; requested override 360px mapped to actual 400px, so actual 360px is not claimed.


Validation: 50 frontend tests pass (domain, API and workflow); formatting, lint, TypeScript and production API build pass. Demo Docker image builds and serves localhost:4174 as UID101; health 200 and SPA deep link 200. Unconfigured API returns JSON503. Existing Streamlit localhost:8501 remains healthy. No database/model changes: No migration required. Tests do not prove real platform access, worker recovery, data acquisition or 1000-post targets.

## Extraction limitations and cost

AST uses 0 LLM tokens. Semantic work used the delegated host agent; input/output token accounting is unavailable. Generated zero counters above are placeholders, not measured zero semantic cost. Cost tracker records null values and excludes this unknown usage from known cumulative totals.

Raw changed-source diagnostics: {"dangling_endpoint_edges": 80, "undirected_same_endpoint_collapsed_edges": 14}. These include external AST symbols and relationships collapsed by the existing undirected graph. The exported graph separately passes endpoint and hyperedge-membership checks; raw limitations remain visible.
