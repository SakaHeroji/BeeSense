# Graph Report - /Users/socs3/Documents/BeeSense  (2026-10-30)

## Corpus Check
- 80 files · ~63,883 words
- Verdict: corpus is large enough that graph structure adds value.

## Summary
- 1338 nodes · 2972 edges · 96 communities (74 shown, 22 thin omitted)
- Extraction: 92% EXTRACTED · 8% INFERRED · 0% AMBIGUOUS · INFERRED: 248 edges (avg confidence: 0.8)
- Token cost: 0 input · 0 output

## Graph Freshness
- Built from commit: `8cd561dc`
- Run `git rev-parse HEAD` and compare to check if the graph is stale.
- Run `graphify update .` after code changes (no API cost).

## Community Hubs (Navigation)
- Adapter Akuisisi YouTube
- Crawler Selenium Terisolasi
- Ekspor Campaign dan Resume
- Pipeline dan Persistensi NLP
- Alur Akuisisi Sosial Terpadu
- Akuisisi Reddit Reddrix
- Alur Akuisisi Sosial Terpadu
- Eksplorasi Dashboard Streamlit
- Monitor Akuisisi Sintetis
- Identitas dan Kontrak Data
- Alur Akuisisi Sosial Terpadu
- Monitor Akuisisi Sintetis
- Parser dan Runner Reddit
- Coherence dan Quality Gate
- Akses dan Parsing HTML
- Workspace React Crawler
- Eksplorasi Dashboard Streamlit
- Monitor Akuisisi Sintetis
- PRD Workspace Crawler
- Topik dan Verifikasi NLP
- Konfigurasi SocialCrawler
- Bundle Excel dan Provenans
- Workspace React Crawler
- Monitor Akuisisi Sintetis
- Snapshot NLP dan Arsip
- Parser DOM Terbatas
- Topik dan Verifikasi NLP
- Akuisisi Reddit Reddrix
- Workspace React Crawler
- Pengujian Penjelasan Topik
- Akuisisi Reddit Reddrix
- Snapshot NLP dan Arsip
- PRD Workspace Crawler
- Workspace React Crawler
- Pipeline dan Persistensi NLP
- Snapshot NLP dan Arsip
- Coherence dan Quality Gate
- PRD Workspace Crawler
- Eksplorasi Dashboard Streamlit
- Pipeline dan Persistensi NLP
- Pengujian UI Streamlit
- Helper Campaign Browser
- Validasi Redirect dan Kesalahan
- Alur Akuisisi Sosial Terpadu
- Monitor Akuisisi Sintetis
- Verifikasi Dataset Berversi
- Runbook dan Verifikasi Lokal
- Arsitektur Crawler dan Dependensi
- Pipeline dan Persistensi NLP
- Pipeline dan Persistensi NLP
- Eksplorasi Dashboard Streamlit
- Workspace React Crawler
- Konfigurasi Tujuh Sumber
- Eksplorasi Dashboard Streamlit
- PRD Workspace Crawler
- Akuisisi Reddit Reddrix
- Snapshot NLP dan Arsip
- Alur Akuisisi Sosial Terpadu
- Workspace React Crawler
- PRD Workspace Crawler
- Akuisisi Reddit Reddrix
- Akuisisi Reddit Reddrix
- Akuisisi Reddit Reddrix
- Alur Akuisisi Sosial Terpadu
- Workspace React Crawler
- Akuisisi Reddit Reddrix
- Akuisisi Reddit Reddrix
- Identitas dan Kontrak Data
- Ekstraksi Cuplikan Publik
- Workspace React Crawler
- Kontrak dan Operasi Crawler
- Kontrak dan Operasi Crawler
- Workspace React Crawler
- Workspace React Crawler
- Workspace React Crawler
- Workspace React Crawler
- Workspace React Crawler
- Workspace React Crawler
- Kontrak dan Operasi Crawler
- Kontrak dan Operasi Crawler
- Kontrak dan Operasi Crawler
- Memori Startup Dashboard
- Parser dan Runner Reddit
- Akuisisi Reddit Reddrix
- Adapter Akuisisi YouTube

## God Nodes (most connected - your core abstractions)
1. `SocialNLPClusterer` - 88 edges
2. `SocialCrawler` - 85 edges
3. `SocialNLPStreamlitApp` - 54 edges
4. `SocialCrawlerTests` - 42 edges
5. `Reddrix-backed RedditCrawler runbook` - 32 edges
6. `Runbook and historical record for finalized partial crawler campaign` - 30 edges
7. `NLPTests` - 27 edges
8. `RedditCrawler` - 25 edges
9. `SocialCrawlerSelenium` - 25 edges
10. `file_hash()` - 23 edges

## Surprising Connections (you probably didn't know these)
- `Configured Reddit policy cooldown:360seconds` --conceptually_related_to--> `Bounded HTTP429 policy introduced in1.3 and retained by1.4`  [INFERRED]
  config/social_crawler.json → docs/crawler/SOCIAL_CRAWLER.md
- `Configured Reddit retry cap:threeperrun` --conceptually_related_to--> `Bounded HTTP429 policy introduced in1.3 and retained by1.4`  [INFERRED]
  config/social_crawler.json → docs/crawler/SOCIAL_CRAWLER.md
- `Historical fixed top10/window110/all15878-unique macro c_v protocol` --semantically_similar_to--> `Gensim c_v protocol: top 10 terms, window 110, phrase tokens`  [INFERRED] [semantically similar]
  graphify-out/memory/query_20261028_155746_hitung_coherence_minimal_0_4__retrain_sbert_umap_d.md → docs/machine-learning/SOCIAL_NLP.md
- `Combined workbook provenance PASS with immutable source hashes and row lineage` --conceptually_related_to--> `Atomic baseline-then-new workbook merge preserves native identity and provenance`  [INFERRED]
  output/combined_dataset_20261029.json → docs/crawler/SOCIAL_CRAWLER.md
- `Campaign FINISHED_PARTIAL, no active PID and exact stop timestamp` --conceptually_related_to--> `Original deadline stopped acquisition; no operation started afterward`  [INFERRED]
  output/campaign_20261029_1000_3h.json → docs/crawler/SOCIAL_CRAWLER.md

## Import Cycles
- None detected.

## Hyperedges (group relationships)
- **Root shim, UI implementation, package CLIs and ROOT resolution preserve application entry contracts** — docs_project_structure_component_layout, docs_project_structure_streamlit_root_shim, docs_project_structure_repository_root_resolution, docs_project_structure_package_module_cli, docs_project_structure_runtime_requirements_layout [EXTRACTED 1.00]
- **Relocation preserves artifacts while runtime packaging and publication remain distinct verification stages** — docs_project_structure_data_preservation, docs_project_structure_docker_root_context, readme_reorganization_publication_pending, readme_active_coherence, config_social_nlp_active_output_dir [INFERRED 0.95]
- **All three declared images retain module/config layout under root build contexts** — deployment_docker_dockerfile_dashboard_wheels_python_version, deployment_docker_dockerfile_reddrix_one_shot_worker, deployment_docker_dockerfile_selenium_included_reddrix_manifest, deployment_docker_dockerfile_dashboard_context_allowlist, docs_project_structure_docker_root_context [INFERRED 0.95]
- **Frozen native SBERT, UMAP, DBSCAN, sentence-weighted Ward and final c-TF-IDF labels** — docs_machine_learning_social_nlp_native_sbert, docs_machine_learning_social_nlp_overflow_normalization, docs_machine_learning_social_nlp_dual_umap, docs_machine_learning_social_nlp_euclidean_dbscan, docs_machine_learning_social_nlp_sentence_weighted_ward, docs_machine_learning_social_nlp_ctfidf [EXTRACTED 1.00]
- **Fixed c_v token protocol, full unique reference corpus and unweighted aggregate** — docs_machine_learning_social_nlp_coherence_protocol, docs_machine_learning_social_nlp_coherence_reference, docs_machine_learning_social_nlp_coherence_aggregation, docs_machine_learning_social_nlp_invalid_topic_failure [EXTRACTED 1.00]
- **Combined-corpus global coherence with historical incomparable baselines,individual shortfalls and in-sample limits** — docs_machine_learning_social_nlp_coherence_result, docs_machine_learning_social_nlp_unchanged_baseline, docs_machine_learning_social_nlp_individual_shortfalls, docs_machine_learning_social_nlp_insample_limit, docs_machine_learning_social_nlp_original_space_silhouette [EXTRACTED 1.00]
- **Verified synthetic React delivery remains separate from proposed production worker/API acceptance** — crawler_frontend_readme_react_crawler_implementation, crawler_frontend_docs_delivery_verified_frontend_checks, crawler_frontend_docs_delivery_synthetic_demo_limitations, crawler_frontend_docs_api_contract_expected_api_contract, prd_prd_backend_readme_persistent_acquisition_worker, prd_prd_frontend_acceptance_criteria_crawler_production_acceptance_gates [INFERRED 0.95]
- **Complete survey/native-source provenance and validated schema gates protect immutable NLP selection** — prd_prd_frontend_prd_frontend_crawler_complete_response_survey_contract, prd_prd_frontend_prd_frontend_crawler_native_identity_provenance_rules, prd_prd_frontend_prd_frontend_crawler_immutable_dataset_nlp_selection, crawler_frontend_docs_api_contract_server_bound_survey_validation_commit, prd_prd_machine_learning_readme_survey_schema_adapter_requirement, crawler_frontend_readme_preview_export_and_schema_gate, prd_prd_machine_learning_readme_new_social_source_adapter_gate [INFERRED 0.95]

## Communities (96 total, 22 thin omitted)

### Community 0 - "Adapter Akuisisi YouTube"
Cohesion: 0.09
Nodes (34): error_code(), load_settings(), main(), parser(), run(), SafeLogger, Settings, video_url() (+26 more)

### Community 1 - "Crawler Selenium Terisolasi"
Cohesion: 0.08
Nodes (19): _barrier(), _create_driver(), main(), Content quoting an error is never used to classify an access barrier., Convert the shared rendered DOM capture without inventing identities., One browser operation. The parent enforces the hard process deadline., Stream evidence before completion; the original supervisor can retain it., Drop-in SocialCrawler with Selenium for both platforms and shared exports. (+11 more)

### Community 2 - "Ekspor Campaign dan Resume"
Cohesion: 0.08
Nodes (16): atomic_json(), barrier_status(), campaign_plan(), decode_cli_output(), find_cli(), PlaywrightCLI, rate_limit_seconds(), run() (+8 more)

### Community 3 - "Pipeline dan Persistensi NLP"
Cohesion: 0.11
Nodes (7): Encode with SBERT, fit UMAP + DBSCAN and optionally merge to a topic count., SocialNLPClusterer, CloudRuntimeTests, Run in an isolated Cloud environment, using only root requirements.txt., encoder(), fixture(), NLPTests

### Community 4 - "Alur Akuisisi Sosial Terpadu"
Cohesion: 0.16
Nodes (5): rd_events(), receipt(), SocialCrawlerTests, spawn_youtube_fixture(), yt_events()

### Community 5 - "Akuisisi Reddit Reddrix"
Cohesion: 0.09
Nodes (10): Declared Reddrix lint/format and offline contract test step, main(), Reddit-only compatibility entry point for the integrated SocialCrawler Reddrix b, Run only Reddit through the shared Reddrix implementation in SocialCrawler., RedditCrawler, FakeReddrix, item(), Reddrix field/identity boundaries and the real, shared Excel exporter. (+2 more)

### Community 6 - "Alur Akuisisi Sosial Terpadu"
Cohesion: 0.09
Nodes (11): main(), Re-export saved Contents without network or modifying the source bundle., Describe the acquisition backend independently of the shared export., Compose YouTube and Reddrix Reddit workers with one configuration and bundle., Validate and return the effective plan without browser/network access., Return a local date for display; relative source dates stay estimates., Project the full audit rows into one sheet, applying current filters., SocialCrawler (+3 more)

### Community 7 - "Eksplorasi Dashboard Streamlit"
Cohesion: 0.13
Nodes (4): number(), percent(), Read-only exploration of completed NLP runs; no training on page reruns., SocialNLPStreamlitApp

### Community 8 - "Monitor Akuisisi Sintetis"
Cohesion: 0.15
Nodes (26): Automatic(), Baselines(), ConfigFields(), ConfigReview(), ManualUrl(), useApp(), csvCell(), initialConfig() (+18 more)

### Community 9 - "Identitas dan Kontrak Data"
Cohesion: 0.15
Nodes (10): ContentInput, ContractTests, Dataset, digest(), dumps(), MemorySink, Shared pipeline; adapters cannot choose their own headers or cell formats., RecordFactory (+2 more)

### Community 10 - "Alur Akuisisi Sosial Terpadu"
Cohesion: 0.12
Nodes (25): collect_reddrix(), _config(), _keywords(), load_reddrix(), normalize_reddrix_item(), _number(), Map Reddrix 1.2.14 dictionaries without inventing identity or dates., Reddrix anti-bot exceptions do not expose an authoritative HTTP status. (+17 more)

### Community 11 - "Monitor Akuisisi Sintetis"
Cohesion: 0.21
Nodes (24): Shell(), DatasetView(), History(), Composition(), JobDetail(), liveStates, PlatformCard(), ProgressChart() (+16 more)

### Community 12 - "Parser dan Runner Reddit"
Cohesion: 0.12
Nodes (16): bounded_events(), HtmlSource, load_settings(), LocalHtmlSource, parsed_number(), PublicHtmlSource, ABC, Normalize a source event; write only through the shared Dataset/Sink. (+8 more)

### Community 13 - "Coherence dan Quality Gate"
Cohesion: 0.09
Nodes (28): Historical combined snapshot QA; relocated root shim checked offline, Internal model metrics do not establish accuracy or representativeness, Unweighted mean across all 20 final non-noise topics, Stored protocol, reference hash, baseline identity and per-topic scores, Gensim c_v protocol: top 10 terms, window 110, phrase tokens, Reference corpus: all 46143 unique embedding_text sentences including noise, Combined-corpus mean c_v 0.4720034333858867 meets 0.4, Non-noise c-TF-IDF unigram/bigram labels (+20 more)

### Community 14 - "Akses dan Parsing HTML"
Cohesion: 0.19
Nodes (10): first(), fixture_page(), native_fullname(), object_key(), RedditAdapter, RedditHtmlParser, RedditRecordFactory, RedditTests (+2 more)

### Community 15 - "Workspace React Crawler"
Cohesion: 0.07
Nodes (26): compilerOptions, allowImportingTsExtensions, esModuleInterop, isolatedModules, jsx, lib, module, moduleResolution (+18 more)

### Community 16 - "Eksplorasi Dashboard Streamlit"
Cohesion: 0.10
Nodes (25): Count evidence in the filter, keeping sentences/comments/parents distinct., Filters retain model membership and do not recompute c_v, Selected-topic c_v card is separate from the full-model mean, Occurrences, unique sentences, comments and source roots have different denominators, Five artifact-backed Streamlit analysis views, Historical combined20 UI/runtime verification retained after relocation, Responsive cards, visible keyboard focus and chart/table alternatives verified, Four selected-topic cards: unique comments, share, source roots and topic c_v (+17 more)

### Community 17 - "Monitor Akuisisi Sintetis"
Cohesion: 0.11
Nodes (19): AppContext, FieldErrorsContext, demoApi, Baseline, Capabilities, Counts, DatasetDetail, DatasetFile (+11 more)

### Community 18 - "PRD Workspace Crawler"
Cohesion: 0.12
Nodes (22): Project-prefixed cookie-session API requires server CORS/CSRF/access controls, Final style samples:96desktop/78narrow444px elements,all black and≥13 px, React frontend and simulation verified; production acquisition integration unavailable, Applied UX fixes:linked errors, step validation, deep links, drawer focus and inertness, Browser actual widths400/444px;requested360px remains unproven, Production release waits for API/worker/access/export and survey adapter integration, Late plan, URL and survey validation is ignored after input changes, Demo IDs, baseline data and downloads are synthetic rather than acquisition evidence (+14 more)

### Community 19 - "Topik dan Verifikasi NLP"
Cohesion: 0.20
Nodes (22): Final PARTIAL: YouTube 1, 188 exported/300 qualified; Reddit 98/58, Bounded 1.3 cooldown applied to user-authorized continuation 04, Historical active-campaign state; acquisition now finalized PARTIAL, Before segment 03: qualified YouTube6/Reddit17; exported evidence8/31, Before 04 cumulative qualified YouTube77/Reddit26; evidence325/47, Campaign descriptor records finalized PARTIAL status and five-segment accounting, Historical descriptor-based monitoring now resolves final campaign counters, Historical user request for fifteen-minute updates during active acquisition monitoring (+14 more)

### Community 20 - "Konfigurasi SocialCrawler"
Cohesion: 0.15
Nodes (20): Per-platform bounds: max_posts 4000, max_candidates 6000, Configured global acquisition budget 10800 seconds, Configured Reddit policy cooldown:360seconds, Configured Reddit retry cap:threeperrun, Current main configuration: platforms.reddit.enabled=true, Main config now selects Reddit backend=reddrix, Configured platform_execution=round_robin, Configured per-platform min_posts=1000 and min_comments_per_post=10 (+12 more)

### Community 21 - "Bundle Excel dan Provenans"
Cohesion: 0.18
Nodes (12): add_readme(), BundleSink, main(), parser(), Validate the embedded contract; an external descriptor is optional., Atomic new directory; streaming JSONL + streaming, formula-safe Excel., run(), run_self_tests() (+4 more)

### Community 22 - "Workspace React Crawler"
Cohesion: 0.10
Nodes (21): devDependencies, eslint, @eslint/js, jsdom, prettier, @testing-library/user-event, @types/react, @types/react-dom (+13 more)

### Community 23 - "Monitor Akuisisi Sintetis"
Cohesion: 0.13
Nodes (18): advance(), cap, committed, dataset(), get(), load(), plans, reviews (+10 more)

### Community 24 - "Snapshot NLP dan Arsip"
Cohesion: 0.12
Nodes (20): Prior Graphify memory: Selenium crawler preserves Excel contract, BeeSense crawler, NLP and dashboard class architecture, React host/container addition preserves existing acquisition/model artifacts, Saved-artifact Dashboard packages and full training/dev environment remain separate, EXTRACTED source quotations versus INFERRED topic interpretations, Integrated SocialCrawler owns Reddrix acquisition and shared export, Existing Python data/model pipeline and new React workspace remain separate, Curated demo storage and API-mode failure boundaries (+12 more)

### Community 25 - "Parser DOM Terbatas"
Cohesion: 0.17
Nodes (8): assert_accessible(), BoundedDom, content_node(), Node, Small serialised-DOM reader, not a browser or full HTML5 repair engine., rendered_text(), walk(), HTMLParser

### Community 26 - "Topik dan Verifikasi NLP"
Cohesion: 0.18
Nodes (10): Atomic baseline-then-new workbook merge preserves native identity and provenance, Merged corpus: 29, 099 rows, 1, 517 roots and 27, 582 comments/replies, Combined workbook provenance PASS with immutable source hashes and row lineage, identity(), main(), merge(), Merge compact crawl workbooks, rejecting repeated native content identities., Return global native object ID plus its root; text never defines identity. (+2 more)

### Community 27 - "Akuisisi Reddit Reddrix"
Cohesion: 0.15
Nodes (17): Configured 360-second policy and three HTTP 429 retries, Configured new sorting differs from Reddrix capability, Preserved compact SocialCrawler workbook, Historical trial 01 ended PARTIAL with zero posts, BeeSense interoperation delay differs from library request retries, Historical v1.0.0 module-specific non-Linux Xvfb shim, No CAPTCHA solver, stealth or alternate-crawler fallback, Empty or blocked trials publish explicit partial evidence (+9 more)

### Community 28 - "Workspace React Crawler"
Cohesion: 0.12
Nodes (17): dependencies, @fontsource-variable/plus-jakarta-sans, lucide-react, papaparse, react, react-dom, react-router-dom, @tanstack/react-query (+9 more)

### Community 29 - "Pengujian Penjelasan Topik"
Cohesion: 0.26
Nodes (3): ExplanationTests, model_from_counts(), profile()

### Community 31 - "Snapshot NLP dan Arsip"
Cohesion: 0.15
Nodes (16): Platform and top-five source graphs count unique topic comments, Active combined 20-topic run with eleven artifacts and manifest, Historical scores are not directly comparable with combined-corpus c_v, Obsidian dashboard dataset provenance, Source workbook and multi-snapshot integrity verification, Artifact-only dashboard without Gensim/Torch imports, Obsidian Cloud runbook: streamlit_apps.py, Python 3.12 and complete artifact publication, BeeSense startup, verification and coherence training runbook (+8 more)

### Community 32 - "PRD Workspace Crawler"
Cohesion: 0.14
Nodes (15): Server history pagination, SSE, templates and organizational login remain future, Expected typed frontend API contract; backend implementation pending, Increasing snapshotVersion and server-owned actions drive reconciliation, Safe structured errors distinguish API429 from worker-platform429, Typed plan/job requests bind plan IDs, idempotency and safe stop, Backend wrapper must translate local WIB dates and TypeScript field names, Delivery records 50 passing tests, lint/format and production API build, Curated PRD 1.1 theme and seven-source UI distinguish planned backend adapters (+7 more)

### Community 34 - "Pipeline dan Persistensi NLP"
Cohesion: 0.13
Nodes (5): Identify the parent thread, not the individual comment URL., Extract real sentences using relevance plus MMR diversity., Evidence-grounded topic descriptions and descriptive, source-aware trends., Explain already verified artifacts without encoding or fitting again., Rule-based segmentation preserving exact offsets in the original text.

### Community 35 - "Snapshot NLP dan Arsip"
Cohesion: 0.21
Nodes (13): Active artifact directory outputs/nlp_20261029_combined_topics20_01, Configured merged workbook identity and SHA-256, Component-oriented repository layout after SocialCrawler integration, Reorganization preserves data bytes and requires no migration, Relocated Dockerfiles preserve package/config layout from repository root, Module CLIs and worker spawn import relocated packages, Package ROOT preserves repository-relative configuration and artifact paths, Runtime manifests live under requirements with relative includes (+5 more)

### Community 36 - "Coherence dan Quality Gate"
Cohesion: 0.19
Nodes (13): Configured c_v threshold 0.4 with topn 10 and window 110, Configured final topic target: 20, Additional c_v >=0.4 gate preserves earlier eligibility rules, DBSCAN core points and noise without membership probabilities, Two UMAP 10 D projections seeded 42 and 43, Euclidean DBSCAN with reusable bounded radius graphs, Published 15-candidate DBSCAN grid preserves 8 million-edge guard, Evaluate final topic partitions before candidate selection (+5 more)

### Community 37 - "PRD Workspace Crawler"
Cohesion: 0.19
Nodes (14): locatorKey is normalized permalink identity;nativeId may await backend verification, Survey commit binds review to session/project and revalidates conflicts, Implemented UI flows:automatic/manual, monitor, survey and dataset review, Frontend URL review and minat-studi-v1 survey form/CSV/XLSX workflows, Proposed server-owned monitor separates units and finalization states, Automatic four-step source/filter/baseline/review workflow, Proposed survey schema preserves declared roles, questions, permission and whole responses, Crawler frontend PRD v1.1 with implemented seven-source UI and pending backend (+6 more)

### Community 38 - "Eksplorasi Dashboard Streamlit"
Cohesion: 0.14
Nodes (5): _graph_positions(), Bounded topic graph: volume from filtered rows, semantic edges from the full mod, Count sentence occurrences; never confuse them with distinct comments., Keep the full-model layout stable while volume and edge filters change., DashboardTests

### Community 39 - "Pipeline dan Persistensi NLP"
Cohesion: 0.30
Nodes (4): json_write(), main(), Publish a new versioned sidecar; never modify the original run., Reuse immutable SBERT features only after verifying data/model identity.

### Community 41 - "Helper Campaign Browser"
Cohesion: 0.27
Nodes (8): classifyCaptureFailure(), enrichBatch(), rateLimitSeconds(), inWindow(), mergeCandidates(), row, source, window

### Community 42 - "Validasi Redirect dan Kesalahan"
Cohesion: 0.23
Nodes (8): HtmlPage, now_iso(), Only public HTML pages on the canonical host; never auth/API routes., RestrictedRedirect, safe_web_url(), SourceFailure, Exception, HTTPRedirectHandler

### Community 43 - "Alur Akuisisi Sosial Terpadu"
Cohesion: 0.26
Nodes (12): Return an explicit target/shortfall report and write one atomic bundle., Round-robin advances YouTube while Reddit waits for readiness, Bounded HTTP429 policy introduced in1.3 and retained by1.4, Retain the same failed Reddit operation until cooldown expires, Per-run canonical root duplicate guard, Persist actual 429 finish timestamps, cooldown deadline and retry decisions, Observed recovery-notice interval≈331.315 seconds is not a server minimum, Historical root skip before request and returned-identity check before export (+4 more)

### Community 44 - "Monitor Akuisisi Sintetis"
Cohesion: 0.19
Nodes (9): ApiError, base, httpApi, post(), request(), Config, Job, Plan (+1 more)

### Community 46 - "Runbook dan Verifikasi Lokal"
Cohesion: 0.29
Nodes (12): Full Python3.12 tooling uses requirements/dev.txt and relocated package paths, CI verifies full Python 3.12 tooling separately from dashboard-only Python 3.12/3.14 matrix, Saved-model dashboard uses a separate runtime;full refitting stays Python 3.12, New-corpus native SBERT encoding or exact verified cache reuse, Separate SBERT training and artifact-only dashboard environments, Training/evaluation-only Gensim coherence requirements, Separate Python 3.12 development/training regression dependency entry, NLP, Streamlit and Plotly dependency ranges (+4 more)

### Community 47 - "Arsitektur Crawler dan Dependensi"
Cohesion: 0.18
Nodes (12): Shared rendered_thread_dom.mjs extraction, Relative dates remain calendar estimates, Historical Selenium implementation preset:500roots/platform andonehour, Worker hard deadline preserves streamed partial events, Separate non-root crawler container with Selenium Grid, Fresh Chrome guest session per operation, Official Selenium Manager ChromeDriver selection, SocialCrawlerSelenium class (+4 more)

### Community 48 - "Pipeline dan Persistensi NLP"
Cohesion: 0.26
Nodes (4): file_hash(), main(), Verify published source workbooks and the dashboard artifact bundle., verify()

### Community 49 - "Pipeline dan Persistensi NLP"
Cohesion: 0.20
Nodes (4): Use the same class TF-IDF vocabulary for selection and publication., Macro c_v on ALL non-noise topics and a fixed full-corpus reference.          Un, Preserve explicit zero distances, including identical sentence vectors., Select DBSCAN parameters on UMAP; evaluate in original SBERT geometry.

### Community 50 - "Eksplorasi Dashboard Streamlit"
Cohesion: 0.31
Nodes (8): Root Docker context allowlist for relocated dashboard runtime, _explain_filtered(), _load_artifacts(), main(), Streamlit entry point for local and Community Cloud dashboards.  Training lives, Dashboard build context includes root shim and artifact-reader packages, Relocated dashboard image uses root Streamlit shim and runtime-only wheels, Streamlit Community Cloud entry point; UI implementation lives in Dashboard.

### Community 51 - "Workspace React Crawler"
Cohesion: 0.18
Nodes (11): scripts, build, build:demo, check, dev, format, format:check, lint (+3 more)

### Community 52 - "Konfigurasi Tujuh Sumber"
Cohesion: 0.20
Nodes (9): labels, sample, Survey(), WorkbookData, download(), SurveyField, surveyFields, Field() (+1 more)

### Community 54 - "PRD Workspace Crawler"
Cohesion: 0.22
Nodes (10): Dataset.nlpSupported requires tested schema and every included source adapter, Versioned datasets provide50-row pages, authorized files and selection-only NLP handoff, Demo preview-only downloads and validated-source NLP gate, Curated available UI flows retain worker authority and survey metadata, New survey schema must preserve role, question, response, version and permission, Version/checksum handoff requires partial acceptance and supported schema, Machine Learning PRD remains unwritten; Crawler handoff dependencies listed, 20 topics/coherence≥0.4 belong to future model criteria, not Crawler success (+2 more)

### Community 55 - "Akuisisi Reddit Reddrix"
Cohesion: 0.24
Nodes (10): Hard-deadline subprocess retains streamed records, No database/model/persistent-contract migration, SocialCrawler1.4 default Reddit Reddrix plus YouTube yt-dlp, Legacy HTML/Playwright/checkpoint are explicit,never automatic fallback, RedditCrawler compatibility wrapper delegates to shared core, Index links default integrated Reddrix and retained historical trial, Reddrix trial preserves existing model and frontend boundaries, Integrated SocialCrawler Reddrix with thin Reddit-only wrapper (+2 more)

### Community 56 - "Snapshot NLP dan Arsip"
Cohesion: 0.36
Nodes (9): Isolated dashboard-runtime matrix for Python 3.12 and3.14, Cloud AppTest regression opens all five views/T04 without installed or imported training libraries, Obsidian runbook records Python 3.14 failure and dashboard-only packaging fix, Historical Python 3.14.10 Cloud install failure:ONNX cp314 wheels and Numba support, PyArrow 24.0.0 matches Cloud guard for Arrow/mimalloc threaded-import compatibility, Cloud root requirements now install dashboard-only dependencies, Root Cloud requirements include relocated dashboard-only runtime, NumPy 2.2.6 below Python 3.14;2.3.5 on Python 3.14 and later (+1 more)

### Community 57 - "Alur Akuisisi Sosial Terpadu"
Cohesion: 0.22
Nodes (9): Retained Playwright-only CAPTCHA fields:600-second wait and five-second poll, Advanced connected-browser Reddit campaign helpers, Checkpoint export to the eight-sheet contract, Native-ID provenance and bounded public excerpts, Standalone runner stops 429; coordinator 1.3 supports bounded cooldown, Isolated Chrome profile, manual CAPTCHA wait and access-barrier stops, Coordinator waits for manual CAPTCHA without automated clicks, Reddit Playwright CLI runner (+1 more)

### Community 58 - "Workspace React Crawler"
Cohesion: 0.22
Nodes (4): client, ErrorBoundary, router, Manual()

### Community 59 - "PRD Workspace Crawler"
Cohesion: 0.25
Nodes (9): Crawler wireframes are illustrative design requirements, not app screenshots, Monitor prioritizes status, units, barriers and next actions over logs, Worker-session CAPTCHA and429 UI offer observation rather than bypass, Responsive drawer/table/focus behavior is a design target, History and dataset detail are supporting views under two menus, Frontend PRD index:Crawler detailed; NLP and Dashboard PRDs remain future, React/demo implementation exists while web acquisition backend is still required, BeeSense PRDs separate frontend, backend and machine-learning responsibility (+1 more)

### Community 60 - "Akuisisi Reddit Reddrix"
Cohesion: 0.32
Nodes (8): CI discovers shared-core Reddrix integration regressions, Actual macOS lifecycle test versus mocked Linux display matrix, Reddrix Docker image unbuilt: local daemon unavailable, Integrated offline tests and macOS lifecycle scope, Seven regression cases verify shared default backend contracts, Current offline tests pass; actual Linux and reorganized Docker image unverified, Reorganized Docker image remains unbuilt while local daemon is unavailable, Historical 16 adapter/export/display tests; current crawler suite 72 pass and 1 skip

### Community 61 - "Akuisisi Reddit Reddrix"
Cohesion: 0.36
Nodes (8): Read-only historical baseline exclusion, Original date boundary and university-topic query scope, Configured root/comment/candidate/time budgets, Trial config now explicitly selects Reddrix; wrapper preserves legacy compatibility, Tracked Reddit trial configuration, Original historical date window, keywords and read-only baseline, Thin Reddit-only wrapper selects shared Reddrix explicitly, Thirty-minute bounded trial with non-guaranteed target

### Community 62 - "Akuisisi Reddit Reddrix"
Cohesion: 0.29
Nodes (8): Tracked reddrix.display_mode=auto, Main root reddrix.display_mode=auto, Adaptive display v1.1.0 auto platform policy, CLI/class display overrides and explicit virtual preconditions, Requested/effective display mode is visible in plan and source metadata, Reddrix-only Camoufox factory controls initial and refreshed sessions, Curated adaptive display and isolated factory architecture, SocialCrawler default Reddrix plus thin Reddit-only compatibility entry

### Community 63 - "Alur Akuisisi Sosial Terpadu"
Cohesion: 0.33
Nodes (7): Historical exclusion source outputs/social_20261028_01, Inherited SocialCrawler filters and Excel exporters, JSONL audit, dataset.xlsx and checksum manifest, social_data.xlsx ten-column Data worksheet, Five verified segments consolidate with zero duplicate roots and zero baseline overlap, Read-only canonical/native identity index excludes 50 old YouTube and 181 Reddit roots, Historical audit workbook: 50 YouTube and 181 Reddit root identities

### Community 64 - "Workspace React Crawler"
Cohesion: 0.29
Nodes (6): engines, node, name, private, type, version

### Community 65 - "Akuisisi Reddit Reddrix"
Cohesion: 0.43
Nodes (7): Crawler root-context allowlist preserves package/config/dependency layout, Relocated combined crawler image runs package module as UID10001, Selenium build context allows the newly included dependency manifest, Relocated Selenium image preserves included requirements and package modules, Isolated local environment and separately downloaded browser, Shared crawler pins include yt-dlp and isolated Reddrix manifest, Isolated Reddrix 1.2.14 crawler dependency pins

### Community 66 - "Akuisisi Reddit Reddrix"
Cohesion: 0.40
Nodes (6): Installed Reddrix 1.2.14 and Camoufox 156 browser evidence, Adaptive display implemented after trial with no new crawl, Completed trial 02: PARTIAL with 25 qualified posts, Final trial bundle passes identity, baseline and Excel integrity checks, Integration changes code/config without new live acquisition, Trial chronology separates v1.0.0 results from post-trial v1.1.0 display

### Community 69 - "Workspace React Crawler"
Cohesion: 0.50
Nodes (3): printWidth, singleQuote, trailingComma

## Knowledge Gaps
- **118 isolated node(s):** `window`, `source`, `row`, `candidate`, `Graphify memory: Streamlit dashboard startup` (+113 more)
  These have ≤1 connection - possible missing edges or undocumented components.
- **22 thin communities (<3 nodes) omitted from report** — run `graphify query` to explore isolated nodes.

## Suggested Questions
_Questions this graph is uniquely positioned to answer:_

- **Why does `SocialCrawler` connect `Alur Akuisisi Sosial Terpadu` to `Crawler Selenium Terisolasi`, `Akuisisi Reddit Reddrix`, `Snapshot NLP dan Arsip`, `Alur Akuisisi Sosial Terpadu`, `Akuisisi Reddit Reddrix`, `Alur Akuisisi Sosial Terpadu`, `Alur Akuisisi Sosial Terpadu`, `Akses dan Parsing HTML`, `Arsitektur Crawler dan Dependensi`, `Topik dan Verifikasi NLP`, `Konfigurasi SocialCrawler`, `Akuisisi Reddit Reddrix`, `Snapshot NLP dan Arsip`, `Alur Akuisisi Sosial Terpadu`, `Akuisisi Reddit Reddrix`, `Akuisisi Reddit Reddrix`, `Alur Akuisisi Sosial Terpadu`?**
  _High betweenness centrality (0.257) - this node is a cross-community bridge._
- **Why does `SocialNLPClusterer` connect `Pipeline dan Persistensi NLP` to `Pipeline dan Persistensi NLP`, `Snapshot NLP dan Arsip`, `Coherence dan Quality Gate`, `Eksplorasi Dashboard Streamlit`, `Eksplorasi Dashboard Streamlit`, `Pipeline dan Persistensi NLP`, `Pengujian UI Streamlit`, `Coherence dan Quality Gate`, `Runbook dan Verifikasi Lokal`, `Eksplorasi Dashboard Streamlit`, `Pipeline dan Persistensi NLP`, `Eksplorasi Dashboard Streamlit`, `Pipeline dan Persistensi NLP`, `Snapshot NLP dan Arsip`, `Pengujian Penjelasan Topik`, `Snapshot NLP dan Arsip`?**
  _High betweenness centrality (0.123) - this node is a cross-community bridge._
- **Why does `BeeSense Obsidian architecture and dataset index` connect `Snapshot NLP dan Arsip` to `Arsitektur Crawler dan Dependensi`, `Eksplorasi Dashboard Streamlit`, `Topik dan Verifikasi NLP`, `Akuisisi Reddit Reddrix`, `PRD Workspace Crawler`, `Snapshot NLP dan Arsip`?**
  _High betweenness centrality (0.070) - this node is a cross-community bridge._
- **Are the 12 inferred relationships involving `SocialNLPClusterer` (e.g. with `SocialNLPStreamlitApp` and `Published 15-candidate DBSCAN grid preserves 8 million-edge guard`) actually correct?**
  _`SocialNLPClusterer` has 12 INFERRED edges - model-reasoned connections that need verification._
- **Are the 14 inferred relationships involving `SocialCrawler` (e.g. with `RedditCrawler` and `_SeleniumSource`) actually correct?**
  _`SocialCrawler` has 14 INFERRED edges - model-reasoned connections that need verification._
- **Are the 4 inferred relationships involving `SocialNLPStreamlitApp` (e.g. with `Cloud AppTest regression opens all five views/T04 without installed or imported training libraries` and `Platform and top-five source graphs count unique topic comments`) actually correct?**
  _`SocialNLPStreamlitApp` has 4 INFERRED edges - model-reasoned connections that need verification._
- **What connects `window`, `source`, `row` to the rest of the system?**
  _118 weakly-connected nodes found - possible documentation gaps or missing edges._
## Reorganized project and Streamlit entry point

Reddrix was integrated into SocialCrawler1.4.0 and verified BEFORE folder moves.56 maintained files were moved without deleting dataset/model artifacts. Backend code is now Crawler/Backend, NLP MachineLearning/social_nlp.py, UI Dashboard/app.py. Config is config/, dependency manifests requirements/, guides docs/, Docker deployment/docker/, crawler tests tests/crawler/. Frontend remains Crawler/Frontend. Latest user instruction supersedes main.py retention:Streamlit entry is root streamlit_apps.py;main.py is absent and reserved for a future backend. Root requirements.txt includes requirements/dashboard.txt.

Python imports, worker spawn module paths, project ROOT constants, config/resource paths, relative Markdown links, module CLI commands, dependency includes, Docker COPY and entrypoints, and GitHub Actions discovery were reconciled. Package CLI is python -m Crawler.Backend.social_crawler. Primary config keeps10800seconds/YouTube+Reddit, trial1800seconds/Reddit, backendreddrix/displayauto. Relative data paths resolve against projectroot. No new live crawl, corpus merge, embedding or retraining. Historical partial33post/769row Reddrix trial and existing20topic/coherence0.4720 dashboard snapshot are preserved.

Before extraction,751 moved-source node IDs/source references were rebased from the previous graph WITHOUT node/edge loss. Structural sources were re-extracted at new package paths. Semantic shared-source/historical evidence is reconciled by delegated chunks, not discarded. Existing frontend and historical data evidence remains. Root JSON/runtime manifests are mapped semantically. This report describes local working-tree validation; GitHub publication and Cloud redeployment must be verified independently afterward.

Verification after moves and final entry rename:73 crawler tests(72pass,1optionalbrowser skip),68NLP/Streamlit tests pass,1Cloud test passes in an isolated Python3.12 dashboard-only environment,12legacyReddit runner tests pass,10JavaScript parser tests pass. CI-scoped Ruff lint/format, compileall, published data verifier(61files) and dependency consistency pass. The initial Cloud test was intentionally rerun in the correct clean environment after detecting training packages in the full NLP environment; final isolated result passes and no assertions were weakened.

All included requirements paths exist. Three clean context copies(dashboard/crawler/Selenium) pass actual package import/dry-run and Docker COPY path checks. No migration required. Docker image build/runtime remain NOT verified because local daemon is unavailable. Pending commands:docker build -f deployment/docker/Dockerfile.dashboard -t beesense-dashboard:local . and docker build -f deployment/docker/Dockerfile.crawler -t beesense-social-crawler:local . . Data/model/workbook bytes remain unchanged; original audit baseline and all61shipped data files pass verification.


## Extraction limitations and cost

AST LLM cost is 0. Delegated semantic input/output token accounting is unavailable; generated zero counters are placeholders rather than measured zero cost, and cost.json stores null usage for this run. Raw changed-source diagnostics: {"dangling_endpoint_edges": 316, "directed_same_endpoint_collapsed_edges": 36, "undirected_same_endpoint_collapsed_edges": 44}. Existing-base endpoints may be absent from the extraction fragment, and external AST symbols may be unresolved. Exported endpoints and hyperedge membership are validated separately. The undirected graph can collapse multiple relations on the same endpoint pair.

Final integrity: all maintained Markdown targets and exported graph endpoints validate. Raw fragment references outside fragment:316,resolved againstfullgraph:23,unmapped externalreferences:293. The undirected build collapses44 same-endpoint relations. Benchmark~89,200naivetokens vs~10,163averagequerytokens(~8.8x). Embedded Reddit self-test additionally29pass. Total validation192pass/1optional skip across Python and JS.
