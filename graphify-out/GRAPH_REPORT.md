# Graph Report - BeeSense  (2026-10-30)

## Corpus Check
- 129 files · ~120,719 words
- Verdict: corpus is large enough that graph structure adds value.

## Summary
- 1857 nodes · 4197 edges · 119 communities (99 shown, 20 thin omitted)
- Extraction: 91% EXTRACTED · 9% INFERRED · 0% AMBIGUOUS · INFERRED: 394 edges (avg confidence: 0.76)
- Token cost: 0 input · 0 output

## Graph Freshness
- Built from commit: `984f8f87`
- Run `git rev-parse HEAD` and compare to check if the graph is stale.
- Run `graphify update .` after code changes (no API cost).

## Community Hubs (Navigation)
- Instagram Client dan Ekspor
- Penjadwalan dan Riwayat Akuisisi
- Akuisisi YouTube
- Crawler Selenium
- Worker Instaloader
- Panduan Pipeline BeeSense
- Integrasi Default Instaloader
- Pengujian Client Instagram
- Pengujian Koordinator Crawler
- Koordinator Backend Sosial
- Kontrak Record Reddit
- Validasi Konfigurasi Frontend
- Penggabungan Dataset
- Model dan Pengujian NLP
- Render Dashboard Streamlit
- Form Akuisisi dan Survei
- Riwayat Sesi Instagram
- Worker Reddrix
- Monitor Job dan Dataset
- Konfigurasi TypeScript
- Encoding dan Penyimpanan Model
- Pengujian Worker Instaloader
- Batas Akuisisi Reddit
- Tipe dan Client API
- Pengujian Parser Reddit
- Kontrak API Frontend
- Generator Narasi Gemini
- Struktur Runtime Dashboard
- Pemilihan Topik dan Coherence
- Persyaratan Produk Crawler
- Konfigurasi Model Aktif
- Parsing Identitas Reddit
- Dependency Pengembangan Frontend
- Capture Reddit Playwright
- Wrapper RedditCrawler
- Penjelasan Topik Dashboard
- Validasi Record Reddit
- Format Grafik Dashboard
- Pengujian Penjelasan Topik
- Pengujian Narasi Gemini
- Pengambilan HTML Reddit
- Batas Integrasi Produksi
- Dependency Runtime Frontend
- Verifikasi Artefak Dataset
- Ekspor dan Provenance Reddit
- Pengujian Resume Capture
- Bukti Ekstraktif Topik
- Lingkungan Training SBERT
- Riwayat Pacing Instagram
- Interface Layanan Frontend
- Arsitektur Model dan Dashboard
- Fixture dan Pengujian Reddit
- Worker Chrome Instagram
- Runtime Docker dan Display
- Konteks dan Provenance Gemini
- Eksekusi dan Ekspor Crawler
- Alur Dataset Model Dashboard
- Riwayat Dataset dan Metodologi
- Pengujian UI Streamlit
- CI dan Verifikasi Backend
- Kampanye Browser Reddit
- Riwayat Evaluasi Coherence
- Audit Akuisisi Instagram
- Struktur DOM Reddit
- Skrip Build Frontend
- Rencana Produk dan Survei
- Pengujian Analisis Dashboard
- Pengujian Integrasi Reddrix
- Default Backend Reddit
- Konfigurasi Trial Reddit
- Router dan Batas Error
- Metadata Package Frontend
- Pengujian Alur Frontend
- Transport GraphQL Instaloader
- Parser Public Post
- Format Kode Frontend
- Kontrak Ekspor Instagram
- Rencana Layanan Backend
- CI Container Frontend
- Package Backend Python
- Package YouTube Python
- Aturan React Hooks
- Matcher DOM Pengujian
- Testing Library React
- Tipe Parser CSV
- Compiler TypeScript
- Bundler Vite
- Identitas Visual BeeSense
- Package Crawler Python
- Package Dashboard Python
- Memori Startup Dashboard
- Dependency Backend Instagrapi
- thread_url
- build_topic_sentences.mjs
- topic_sentence_export.py
- InstaloaderCrawler
- .score_coherence
- .topic_figure
- BeeSense project
- config/social_crawler.json
- Read-only native/canonical index excludes 50 YouTube and 181 Reddit roots
- Round Robin Shared Deadline
- .render
- app.py
- Reddit Playwright CLI runner
- Historical Reddit continuations preserve bundles and original deadline
- instagram_browser_capture.mjs
- Q: ok sekarang training ulang menggunakan /Users/sakaheroji/Documents/BeeSense/outputs/social_20261030_combined_instagram_500_2h_02/social_data.xlsx, clustering. Buat 20 topik dengan coherence minimal 0.4. Lalu buat excel baru dengan tabel dengan kolom: topik, kalimat yang berada dalam cluster topik. lalu model digunakan kembali di dashboard streamlit yang di rebuild ulang, dan di commit dan dipush semuanya ke githubnya untuk di deploy ulang

## God Nodes (most connected - your core abstractions)
1. `SocialCrawler` - 111 edges
2. `SocialNLPClusterer` - 98 edges
3. `SocialNLPStreamlitApp` - 58 edges
4. `SocialCrawlerTests` - 42 edges
5. `InstagramCrawlerTests` - 33 edges
6. `Reddrix-backed RedditCrawler runbook` - 32 edges
7. `file_hash()` - 29 edges
8. `Runbook and historical record for finalized partial crawler campaign` - 29 edges
9. `NLPTests` - 28 edges
10. `IntegratedInstagram1.5.2 pacing after verified dashboard release` - 27 edges

## Surprising Connections (you probably didn't know these)
- `Relocated Selenium image preserves included requirements and package modules` --references--> `SocialCrawlerSelenium`  [INFERRED]
  deployment/docker/Dockerfile.selenium → Crawler/Backend/social_crawler_selenium.py
- `Documented regression coverage for shared backend contracts` --references--> `SocialCrawlerReddrixTests`  [INFERRED]
  docs/crawler/SOCIAL_CRAWLER.md → tests/crawler/test_social_crawler_reddrix.py
- `Configured Reddit policy cooldown:360seconds` --conceptually_related_to--> `Reddit bounded 429 policy introduced in version 1.3`  [INFERRED]
  config/social_crawler.json → docs/crawler/SOCIAL_CRAWLER.md
- `Configured Reddit retry cap:threeperrun` --conceptually_related_to--> `Reddit bounded 429 policy introduced in version 1.3`  [INFERRED]
  config/social_crawler.json → docs/crawler/SOCIAL_CRAWLER.md
- `Preserved eight-sheet audit and checksummed full-text bundle` --conceptually_related_to--> `BundleSink`  [EXTRACTED]
  docs/crawler/REDDIT_CRAWLER.md → Crawler/Backend/Reddit/crawl_reddit_single.py

## Import Cycles
- None detected.

## Hyperedges (group relationships)
- **Crawler product specification and acceptance** — prd_prd_frontend_prd_frontend_crawler_crawler_product_requirements, prd_prd_frontend_rancangan_layar_crawler_crawler_screen_design, prd_prd_frontend_acceptance_criteria_crawler_crawler_acceptance_criteria [EXTRACTED 1.00]
- **Shared social export contract across crawler backends** — docs_crawler_instagram_crawler_shared_social_export_contract, docs_crawler_instaloader_crawler_instaloader_crawler, docs_crawler_reddit_crawler_reddrix_reddit_crawler, docs_crawler_instagram_crawler_persistent_chrome_worker [EXTRACTED 1.00]
- **Immutable dataset to trained model to artifact dashboard** — readme_active_combined_dataset, docs_crawler_instagram_pipeline_20261030_verified_20261030_model, docs_crawler_instagram_pipeline_20261030_gemini_topic_narratives, readme_artifact_only_dashboard [EXTRACTED 1.00]
- **SBERT UMAP DBSCAN Ward Topic Pipeline** — docs_machine_learning_social_nlp_sbert, docs_machine_learning_social_nlp_umap, docs_machine_learning_social_nlp_dbscan, docs_machine_learning_social_nlp_weighted_ward, docs_machine_learning_social_nlp_c_tf_idf [EXTRACTED 1.00]
- **Supported Monthly Topic Direction** — docs_machine_learning_explainable_topics_supported_descriptive_trends, docs_machine_learning_explainable_topics_theil_sen, docs_machine_learning_explainable_topics_kendall_tau_b [EXTRACTED 1.00]
- **Verified Model Narratives and Dashboard** — docs_machine_learning_social_nlp_artifact_contract_v2, docs_machine_learning_gemini_topic_narratives_topic_narratives_csv, docs_dashboard_dashboard_design_artifact_only_runtime, docs_machine_learning_gemini_topic_narratives_post_clustering_synthesis [INFERRED 0.85]
- **Verified standalone trial06 GraphQL and comment path** — docs_crawler_instaloader_crawler_runtime_graphql_patch, docs_crawler_instaloader_crawler_same_context_tokens, docs_crawler_instaloader_crawler_persistent_worker_deadline, docs_crawler_instaloader_crawler_legacy_comment_nodeiterator, docs_crawler_instaloader_crawler_trial06_verified_outcome [EXTRACTED 1.00]
- **Filtered acquisition, identity exclusion, audit export and merge** — docs_crawler_social_crawler_coordinator_filters_and_scheduler, docs_crawler_social_crawler_baseline_identity_exclusion, docs_crawler_social_crawler_audit_bundle_and_excel, docs_crawler_social_crawler_native_id_merge_integrity [EXTRACTED 1.00]
- **Saved NLP snapshot, narrative CSV and dashboard delivery** — readme_nlp_training_and_reuse, readme_active_dataset_and_snapshot, readme_gemini_narratives, readme_streamlit_cloud_deployment, readme_artifact_and_ci_gate [EXTRACTED 1.00]
- **Stoppedacquisition→auditedfinalcorpus→verified20topics→contextualGeminiCSV** — docs_crawler_instagram_pipeline_20261030_acquisition_user_stop, docs_crawler_instagram_pipeline_20261030_final_native_identity_corpus, docs_crawler_instagram_pipeline_20261030_final_verified_model, docs_crawler_instagram_pipeline_20261030_actual_contextual_gemini_csv [EXTRACTED 1.00]
- **Topicweights,fittedcontext,receiptandCSV2bindoneversionednarrative** — docs_machine_learning_gemini_topic_narratives_weighted_keyword_input, docs_machine_learning_gemini_topic_narratives_fitted_sentence_context_selection, docs_machine_learning_gemini_topic_narratives_receipt_resume_binding, docs_machine_learning_gemini_topic_narratives_extension_validation [EXTRACTED 1.00]
- **VerifiedmodelandCSVsupportread-onlythree-platformDashboard** — docs_dashboard_dashboard_design_verified_model_20261030, docs_dashboard_dashboard_design_three_platform_support, docs_dashboard_dashboard_design_gemini_read_only_narratives [EXTRACTED 1.00]
- **Root shim, UI implementation, package CLIs and ROOT resolution preserve application entry contracts** — docs_project_structure_component_layout, docs_project_structure_streamlit_root_shim, docs_project_structure_repository_root_resolution, docs_project_structure_package_module_cli, docs_project_structure_runtime_requirements_layout [EXTRACTED 1.00]
- **Relocation preserves artifacts while runtime packaging and publication remain distinct verification stages** — docs_project_structure_data_preservation, docs_project_structure_docker_root_context, readme_reorganization_publication_pending, readme_active_coherence, config_social_nlp_active_output_dir [INFERRED 0.95]
- **All three declared images retain module/config layout under root build contexts** — deployment_docker_dockerfile_dashboard_wheels_python_version, deployment_docker_dockerfile_reddrix_one_shot_worker, deployment_docker_dockerfile_selenium_included_reddrix_manifest, deployment_docker_dockerfile_dashboard_context_allowlist, docs_project_structure_docker_root_context [INFERRED 0.95]
- **Verified synthetic React delivery remains separate from proposed production worker/API acceptance** — crawler_frontend_readme_react_crawler_implementation, crawler_frontend_docs_delivery_verified_frontend_checks, crawler_frontend_docs_delivery_synthetic_demo_limitations, crawler_frontend_docs_api_contract_expected_api_contract, prd_prd_backend_readme_persistent_acquisition_worker, prd_prd_frontend_acceptance_criteria_crawler_production_acceptance_gates [INFERRED 0.95]

## Communities (119 total, 20 thin omitted)

### Community 0 - "Instagram Client dan Ekspor"
Cohesion: 0.29
Nodes (11): collect(), media_pk_from_url(), media_url(), native_pk(), normalize_item(), object_key(), Map explicit native IDs/timestamps; do not infer authors or text coverage., Accept only Instagram post/reel permalinks; strip tracking parameters. (+3 more)

### Community 1 - "Penjadwalan dan Riwayat Akuisisi"
Cohesion: 0.24
Nodes (19): Historical user-authorized version-1.3 continuation 04, Historical active-campaign state; acquisition now finalized PARTIAL, Before segment 03: qualified YouTube6/Reddit17; exported evidence8/31, Before 04 cumulative qualified YouTube77/Reddit26; evidence325/47, Campaign descriptor records finalized PARTIAL status and five-segment accounting, Historical descriptor-based monitoring now resolves final campaign counters, Historical user request for fifteen-minute updates during active acquisition monitoring, Historical preparation restriction: cooldown implemented without restarting segment 03 (+11 more)

### Community 2 - "Akuisisi YouTube"
Cohesion: 0.09
Nodes (34): error_code(), load_settings(), main(), parser(), run(), SafeLogger, Settings, video_url() (+26 more)

### Community 3 - "Crawler Selenium"
Cohesion: 0.07
Nodes (19): _barrier(), _create_driver(), main(), Content quoting an error is never used to classify an access barrier., Convert the shared rendered DOM capture without inventing identities., One browser operation. The parent enforces the hard process deadline., Stream evidence before completion; the original supervisor can retain it., Drop-in SocialCrawler with Selenium for both platforms and shared exports. (+11 more)

### Community 4 - "Worker Instaloader"
Cohesion: 0.08
Nodes (24): AccessBarrier, configure_web_graphql(), error_receipt(), instaloader_worker(), InstaloaderAdapter, InstaloaderCrawler, InstaloaderSettings, InstaloaderWorker (+16 more)

### Community 5 - "Panduan Pipeline BeeSense"
Cohesion: 0.06
Nodes (53): Shared rendered_thread_dom.mjs extraction, Relative dates remain calendar estimates, Historical Selenium implementation preset:500roots/platform andonehour, Separate non-root crawler container with Selenium Grid, Fresh Chrome guest session per operation, Official Selenium Manager ChromeDriver selection, Selenium Rendered DOM, SocialCrawlerSelenium Guide (+45 more)

### Community 6 - "Integrasi Default Instaloader"
Cohesion: 0.09
Nodes (49): Diagnostic and active-data separation, Diagnostic trial deduplication, Instaloader Docker artifact awaiting runtime verification, Standalone experiment caps, InstaloaderCrawler guide and evidence, Historical Instagram resume preset preserved, Historical trials 01–05, InstaloaderCrawler (+41 more)

### Community 7 - "Pengujian Client Instagram"
Cohesion: 0.07
Nodes (7): Clock, FakeClient, InstagramCrawlerTests, Offline contract/deadline tests; fixture data is always marked synthetic., records(), spawn_fixture(), spawn_hanging()

### Community 8 - "Pengujian Koordinator Crawler"
Cohesion: 0.15
Nodes (5): rd_events(), receipt(), SocialCrawlerTests, spawn_youtube_fixture(), yt_events()

### Community 9 - "Koordinator Backend Sosial"
Cohesion: 0.09
Nodes (6): InstagramSettings, Compose platform workers with one configuration, scheduler and export bundle., SocialCrawler, Clock, InstagramIntegrationTests, SocialCrawlerReddrixTests

### Community 10 - "Kontrak Record Reddit"
Cohesion: 0.13
Nodes (17): add_readme(), ContractTests, Dataset, digest(), dumps(), main(), parser(), Validate the embedded contract; an external descriptor is optional. (+9 more)

### Community 11 - "Validasi Konfigurasi Frontend"
Cohesion: 0.10
Nodes (32): ConfigReview(), advance(), cap, committed, dataset(), get(), load(), plans (+24 more)

### Community 12 - "Penggabungan Dataset"
Cohesion: 0.08
Nodes (12): Native-ID baseline-then-new workbook merge with provenance, identity(), main(), merge(), merge_unique(), Merge compact crawl workbooks, rejecting repeated native content identities., Keep the latest supplied observation per native ID, with full row lineage., Return global native object ID plus its root; text never defines identity. (+4 more)

### Community 13 - "Model dan Pengujian NLP"
Cohesion: 0.09
Nodes (9): BeeSense application package., Rule-based segmentation preserving exact offsets in the original text., Encode with SBERT, fit UMAP + DBSCAN and optionally merge to a topic count., SocialNLPClusterer, CloudRuntimeTests, Run in an isolated Cloud environment, using only root requirements.txt., encoder(), fixture() (+1 more)

### Community 15 - "Form Akuisisi dan Survei"
Cohesion: 0.12
Nodes (27): Automatic(), Baselines(), ConfigFields(), Manual(), ManualUrl(), labels, sample, Survey() (+19 more)

### Community 16 - "Riwayat Sesi Instagram"
Cohesion: 0.23
Nodes (19): One LoginRequired recovery with verification-code preservation, CAAHTTP200 without session;legacyHTTP400 needs_upgrade, Cookie accepted for login/account read; trial02 firsthashtag LOGIN_REQUIRED, Explicit auto/password/sessionid login selection, Historical initial password rejection and trial01 LOGIN_REQUIRED/zero, Historical real-cookie header-patch validation fails SDKAttributeError, Instaloader preflight fails before discovery;zero acquired data, Future Instaloader worker must retain one run-wide context/rate controller (+11 more)

### Community 17 - "Worker Reddrix"
Cohesion: 0.10
Nodes (30): browser_configuration(), _configuration(), _integer(), instaloader_options(), Validate shared Instaloader settings without loading credentials or networking., thread_url(), collect_reddrix(), _config() (+22 more)

### Community 18 - "Monitor Job dan Dataset"
Cohesion: 0.20
Nodes (24): Shell(), DatasetView(), History(), Composition(), JobDetail(), liveStates, PlatformCard(), ProgressChart() (+16 more)

### Community 19 - "Konfigurasi TypeScript"
Cohesion: 0.07
Nodes (26): compilerOptions, allowImportingTsExtensions, esModuleInterop, isolatedModules, jsx, lib, module, moduleResolution (+18 more)

### Community 20 - "Encoding dan Penyimpanan Model"
Cohesion: 0.11
Nodes (8): main(), Use the same class TF-IDF vocabulary for selection and publication., Macro c_v on ALL non-noise topics and a fixed full-corpus reference.          Un, Extract real sentences using relevance plus MMR diversity., Publish a new versioned sidecar; never modify the original run., Reuse immutable SBERT features only after verifying data/model identity., Preserve explicit zero distances, including identical sentence vectors., Select DBSCAN parameters on UMAP; evaluate in original SBERT geometry.

### Community 21 - "Pengujian Worker Instaloader"
Cohesion: 0.13
Nodes (5): fixture_post(), hanging_fixture(), InstaloaderCrawlerTests, persistent_fixture(), Offline contracts for the separate Instaloader experiment.

### Community 22 - "Batas Akuisisi Reddit"
Cohesion: 0.11
Nodes (25): Configured 360-second policy and three HTTP 429 retries, Configured new sorting differs from Reddrix capability, Preserved eight-sheet audit and checksummed full-text bundle, Installed Reddrix 1.2.14 and Camoufox 156 browser evidence, Preserved compact SocialCrawler workbook, Historical trial 01 ended PARTIAL with zero posts, Hard-deadline subprocess retains streamed records, BeeSense interoperation delay differs from library request retries (+17 more)

### Community 23 - "Tipe dan Client API"
Cohesion: 0.10
Nodes (20): ApiError, base, httpApi, post(), request(), Baseline, Config, Counts (+12 more)

### Community 24 - "Pengujian Parser Reddit"
Cohesion: 0.24
Nodes (6): bounded_events(), fixture_page(), Whole-post comment budget includes replies; nested replies share thread cap., RedditHtmlParser, RedditTests, worker()

### Community 25 - "Kontrak API Frontend"
Cohesion: 0.10
Nodes (24): Server history pagination, SSE, templates and organizational login remain future, Project-prefixed cookie-session API requires server CORS/CSRF/access controls, Expected typed frontend API contract; backend implementation pending, locatorKey is normalized permalink identity;nativeId may await backend verification, Increasing snapshotVersion and server-owned actions drive reconciliation, Safe structured errors distinguish API429 from worker-platform429, Survey commit binds review to session/project and revalidates conflicts, Typed plan/job requests bind plan IDs, idempotency and safe stop (+16 more)

### Community 26 - "Generator Narasi Gemini"
Cohesion: 0.20
Nodes (18): One request per topic:top10weights plus10 fitted original sentences, Derive Indonesian Gemini labels after topic count and coherence pass., build_prompt(), canonical(), digest(), generate(), load_key(), Gemini narratives grounded in ranked topic keywords and representative sentences (+10 more)

### Community 27 - "Struktur Runtime Dashboard"
Cohesion: 0.19
Nodes (15): Saved-model dashboard uses a separate runtime;full refitting stays Python 3.12, Artifact-only dashboard without Gensim/Torch imports, Obsidian Cloud runbook: streamlit_apps.py, Python 3.12 and complete artifact publication, Obsidian runbook records Python 3.14 failure and dashboard-only packaging fix, BeeSense startup, verification and coherence training runbook, Root streamlit_apps.py delegates to Dashboard.app, Package module CLIs retain repository-root path semantics, Crawler, MachineLearning and Dashboard packages with grouped supporting folders (+7 more)

### Community 28 - "Pemilihan Topik dan Coherence"
Cohesion: 0.11
Nodes (22): Configured c_v threshold 0.4 with topn 10 and window 110, Configured final topic target: 20, Stored protocol, reference hash, baseline identity and per-topic scores, Additional c_v >=0.4 gate preserves earlier eligibility rules, Gensim c_v protocol: top 10 terms, window 110, phrase tokens, Historical46143-sentence reference; current corpus remains separately bound, DBSCAN core points and noise without membership probabilities, Non-noise c-TF-IDF unigram/bigram labels (+14 more)

### Community 29 - "Persyaratan Produk Crawler"
Cohesion: 0.18
Nodes (23): Atomic survey review and idempotent commit, Expected Crawler API contract, NLP schema eligibility gate, Seven-platform capability gating, Server-owned acquisition job lifecycle, Crawler frontend delivery and UX audit, Frontend verification evidence: 50 tests and container checks, BeeSense Crawler React frontend (+15 more)

### Community 30 - "Konfigurasi Model Aktif"
Cohesion: 0.20
Nodes (14): Active artifacts outputs/nlp_20261030_instagram_topics20_02, Configured33034-record final merged workbook, Active20-topic Instagram-inclusive model configuration, Current active Gemini enabled; historical disabled state retained, Component-oriented repository layout after SocialCrawler integration, Reorganization preserves data bytes and requires no migration, Relocated Dockerfiles preserve package/config layout from repository root, Module CLIs and worker spawn import relocated packages (+6 more)

### Community 31 - "Parsing Identitas Reddit"
Cohesion: 0.17
Nodes (14): assert_accessible(), content_node(), first(), HtmlSource, LocalHtmlSource, native_fullname(), Node, object_key() (+6 more)

### Community 32 - "Dependency Pengembangan Frontend"
Cohesion: 0.10
Nodes (21): devDependencies, eslint, @eslint/js, jsdom, prettier, @testing-library/user-event, @types/react, @types/react-dom (+13 more)

### Community 33 - "Capture Reddit Playwright"
Cohesion: 0.21
Nodes (12): atomic_json(), barrier_status(), campaign_plan(), find_cli(), PlaywrightCLI, rate_limit_seconds(), run(), save_capture() (+4 more)

### Community 34 - "Wrapper RedditCrawler"
Cohesion: 0.16
Nodes (5): main(), Reddit-only compatibility entry point for the integrated SocialCrawler Reddrix b, Run only Reddit through the shared Reddrix implementation in SocialCrawler., RedditCrawler, RedditCrawlerTests

### Community 35 - "Penjelasan Topik Dashboard"
Cohesion: 0.14
Nodes (19): Count evidence in the filter, keeping sentences/comments/parents distinct., Filters retain model membership and do not recompute c_v, Selected-topic c_v card is separate from the full-model mean, Occurrences, unique sentences, comments and source roots have different denominators, Five artifact-backed Streamlit analysis views, Historical combined20 UI/runtime verification retained after relocation, Platform and top-five source graphs count unique topic comments, Responsive cards, visible keyboard focus and chart/table alternatives verified (+11 more)

### Community 36 - "Validasi Record Reddit"
Cohesion: 0.16
Nodes (8): ContentInput, KeywordMatcher, load_settings(), parsed_number(), Aho-Corasick; offsets refer to Python Unicode code points in source., RecordFactory, Settings, timeout_fixture()

### Community 37 - "Format Grafik Dashboard"
Cohesion: 0.18
Nodes (15): apply_browser_patch(), browser_graphql_query(), _check(), _cookie(), _hints(), _load_tokens(), main(), _pace() (+7 more)

### Community 38 - "Pengujian Penjelasan Topik"
Cohesion: 0.25
Nodes (3): ExplanationTests, model_from_counts(), profile()

### Community 39 - "Pengujian Narasi Gemini"
Cohesion: 0.19
Nodes (4): GeminiArtifactTests, GeminiTests, response(), topic()

### Community 40 - "Pengambilan HTML Reddit"
Cohesion: 0.11
Nodes (11): error_receipt(), instagram_worker(), InstagramCrawler, main(), Standalone trial. The production SocialCrawler backend stays unchanged., Classify by exception type/status; never write exception text or sessions., run_instagram_worker(), upstream_version() (+3 more)

### Community 41 - "Batas Integrasi Produksi"
Cohesion: 0.13
Nodes (17): Final style samples:96desktop/78narrow444px elements,all black and≥13 px, React frontend and simulation verified; production acquisition integration unavailable, Implemented UI flows:automatic/manual, monitor, survey and dataset review, Applied UX fixes:linked errors, step validation, deep links, drawer focus and inertness, Browser actual widths400/444px;requested360px remains unproven, Production release waits for API/worker/access/export and survey adapter integration, Late plan, URL and survey validation is ignored after input changes, Demo IDs, baseline data and downloads are synthetic rather than acquisition evidence (+9 more)

### Community 42 - "Dependency Runtime Frontend"
Cohesion: 0.12
Nodes (17): dependencies, @fontsource-variable/plus-jakarta-sans, lucide-react, papaparse, react, react-dom, react-router-dom, @tanstack/react-query (+9 more)

### Community 43 - "Verifikasi Artefak Dataset"
Cohesion: 0.20
Nodes (8): file_hash(), main(), published_source_files(), Verify published source workbooks and the dashboard artifact bundle., Verify record identity independently of sentence-text deduplication., A merge report binds its small, explicit audit sidecars to the input., verify(), verify_native_dataset()

### Community 44 - "Ekspor dan Provenance Reddit"
Cohesion: 0.18
Nodes (8): BundleSink, Atomic new directory; streaming JSONL + streaming, formula-safe Excel., RedditRecordFactory, utc_datetime(), export_campaign(), load_campaign(), Verified Reddit native identity and parent/root relationships, Async Reddrix to validated records to existing Excel pipeline

### Community 46 - "Bukti Ekstraktif Topik"
Cohesion: 0.22
Nodes (4): _explain_filtered(), Identify the parent thread, not the individual comment URL., Evidence-grounded topic descriptions and descriptive, source-aware trends., Explain already verified artifacts without encoding or fitting again.

### Community 47 - "Lingkungan Training SBERT"
Cohesion: 0.24
Nodes (11): Relocated Selenium image preserves included requirements and package modules, Isolated local environment and separately downloaded browser, New-corpus native SBERT encoding or exact verified cache reuse, Separate SBERT training and artifact-only dashboard environments, Training/evaluation-only Gensim coherence requirements, NLP, Streamlit and Plotly dependency ranges, Frozen full NLP and offline development environment, Isolated Reddrix 1.2.14 crawler dependency pins (+3 more)

### Community 48 - "Riwayat Pacing Instagram"
Cohesion: 0.17
Nodes (15): Current Instagram bounded retry configuration; historical execution chronology, Chrome remains available for operator inspection, Bounded Instagram recovery does not override user stop, Verifieddashboard publication precedes offlinecrawlerpacing, User-provided DataDwip Instagram pacing reference, Historical Instagram run:248 posts and 2,128 comments, Historical version-1.5.1 fixed Instagram recovery policy, Documented local exponential cooldown respects longer Retry-After (+7 more)

### Community 50 - "Arsitektur Model dan Dashboard"
Cohesion: 0.17
Nodes (15): Nine Gemini offline tests and all20 actual contextual CSV rows validated, Verified current model and20context-grounded narratives, Current20-topic macro c_v0.4315219014 model, Active33034-record three-platform corpus, Producer2.4 contextual Gemini stage after verified model gate, Prior Graphify memory: Selenium crawler preserves Excel contract, BeeSense crawler, NLP and dashboard class architecture, React host/container addition preserves existing acquisition/model artifacts (+7 more)

### Community 51 - "Fixture dan Pengujian Reddit"
Cohesion: 0.29
Nodes (5): browser_script(), InstagramBrowserWorker, Serial Chrome acquisition using a persistent profile and manual login.  The same, decode_cli_output(), RuntimeError

### Community 52 - "Worker Chrome Instagram"
Cohesion: 0.31
Nodes (9): Standalone browser1800-second preset, updated bounded retry, instagramDocumentPayload(), Browser discovery follows InstagramUI order withlocaleligibilitychecks, Bind document-script comments by native DOM permalink andsame shortcode, macOS headed trial andLinuxprepared-profile requirements, One dedicated persistentprofile andpinnedCLI/session perrun, Chrome backend selected by same standalone InstagramCrawler class, Historical Chrome trial02 INTERRUPTED76posts/910comments (+1 more)

### Community 53 - "Runtime Docker dan Display"
Cohesion: 0.21
Nodes (13): Relocated combined crawler image runs package module as UID10001, Adaptive display v1.1.0 auto platform policy, Actual macOS lifecycle test versus mocked Linux display matrix, CLI/class display overrides and explicit virtual preconditions, Requested/effective display mode is visible in plan and source metadata, Reddrix Docker image unbuilt: local daemon unavailable, Reddrix-only Camoufox factory controls initial and refreshed sessions, Historical integrated test scope and unverified Docker runtime (+5 more)

### Community 54 - "Konteks dan Provenance Gemini"
Cohesion: 0.20
Nodes (14): Verified model configuration enables contextual Gemini CSV, Complete contextual20-row Gemini CSV passes bundle gate, Boundedtransientretryandfail-closedpublication, Prompt2/CSV2 with preserved keyword-only version1, Atomic20-row contextual CSV with per-topic provenance, ContextualCSVextension2 binds Parquet; legacyextension1 supported, Deterministic fitted-sentence context ranking, Gemini GenerateContent APIreference (+6 more)

### Community 55 - "Eksekusi dan Ekspor Crawler"
Cohesion: 0.15
Nodes (5): main(), Describe the acquisition backend independently of the shared export., Validate and return the effective plan without browser/network access., Re-export saved Contents without network or modifying the source bundle., Mixed bundles retain backend-specific provenance

### Community 56 - "Alur Dataset Model Dashboard"
Cohesion: 0.13
Nodes (21): Dashboard Python 3.12 and 3.14 runtime matrix, Offline crawler and NLP regression tests, Verify BeeSense CI, Synthetic Reddit post, comment and reply fixture, Reddit browser campaign helpers, User checkpoint audit export and verification, Manual CAPTCHA recovery within global deadline, Reddit Playwright runner (+13 more)

### Community 57 - "Riwayat Dataset dan Metodologi"
Cohesion: 0.13
Nodes (16): Internal model metrics do not establish accuracy or representativeness, Historical v 1 HDBSCAN directional counts for 51 topics, Historical7/20 shortfalls; current model has8/20, Training-corpus coherence is not holdout or labeled accuracy, Historical29October original-space silhouette -0.000279, ImmutableolderNLPsnapshots including29Octobercombinedrun, Historicalcorporaandscoresarenotcurrentqualitycomparators, Obsidian dashboard dataset provenance (+8 more)

### Community 59 - "CI dan Verifikasi Backend"
Cohesion: 0.28
Nodes (14): create_client(), load_client(), login_from_file(), login_local(), login_with_saved_password(), _manual_verification_required(), _raise_exception(), Bounded Instagram acquisition through instagrapi, with the shared Excel contract (+6 more)

### Community 60 - "Kampanye Browser Reddit"
Cohesion: 0.27
Nodes (8): classifyCaptureFailure(), enrichBatch(), rateLimitSeconds(), inWindow(), mergeCandidates(), row, source, window

### Community 61 - "Riwayat Evaluasi Coherence"
Cohesion: 0.21
Nodes (13): Historical combined snapshot QA; relocated root shim checked offline, Unweighted mean across all 20 final non-noise topics, Historical29October macro c_v0.4720034334, Invalid or nonfinite topic coherence cancels the aggregate, Pinned multilingual SentenceTransformer safetensors encoder, Historical29October exact-corpus SBERT/UMAP cache evidence, Overflow-window averaging and L 2-normalized 384 D embeddings, Historical old-corpus baselines retained; no cross-corpus quality comparison (+5 more)

### Community 62 - "Audit Akuisisi Instagram"
Cohesion: 0.18
Nodes (17): Final Instagram-inclusive20-topic/Gemini configuration, Active20-topic Instagram-inclusive model configuration, RetainedSBERTrevision,UMAP/DBSCANbudget andexplanationgates, 27–30October inclusiverefers tosourceacquisitiondate,notpostdate, User stopped Instagram acquisition; no subsequent crawl, All20 actual contextual Gemini narratives validated, Final audited33034-record Instagram-inclusive corpus, Verified20-topic Instagram-inclusive model:macro c_v0.4315219014 (+9 more)

### Community 63 - "Struktur DOM Reddit"
Cohesion: 0.22
Nodes (4): BoundedDom, MemorySink, Small serialised-DOM reader, not a browser or full HTML5 repair engine., HTMLParser

### Community 64 - "Skrip Build Frontend"
Cohesion: 0.18
Nodes (11): scripts, build, build:demo, check, dev, format, format:check, lint (+3 more)

### Community 65 - "Rencana Produk dan Survei"
Cohesion: 0.20
Nodes (11): Curated two-menu contract with URL/Survey under Manual, Curated immutable dataset selection does not train or change Dashboard, Curated Crawler PRD status:frontend implemented, backend pending, New survey schema must preserve role, question, response, version and permission, Crawler wireframes are illustrative design requirements, not app screenshots, Monitor prioritizes status, units, barriers and next actions over logs, Worker-session CAPTCHA and429 UI offer observation rather than bypass, Responsive drawer/table/focus behavior is a design target (+3 more)

### Community 67 - "Pengujian Integrasi Reddrix"
Cohesion: 0.18
Nodes (11): HtmlPage, now_iso(), PublicHtmlSource, Only public HTML pages on the canonical host; never auth/API routes., RestrictedRedirect, safe_web_url(), SourceFailure, thread_id() (+3 more)

### Community 68 - "Default Backend Reddit"
Cohesion: 0.33
Nodes (7): No database/model/persistent-contract migration, Default Reddit Reddrix with YouTube yt-dlp since SocialCrawler 1.4, Explicit legacy HTML, Playwright and checkpoint selections, RedditCrawler wrapper delegates to the shared coordinator, Reddrix trial preserves existing model and frontend boundaries, Integrated SocialCrawler Reddrix with thin Reddit-only wrapper, Folder moves preserve data paths, artifact bytes and historical crawl results

### Community 69 - "Konfigurasi Trial Reddit"
Cohesion: 0.27
Nodes (10): Read-only historical baseline exclusion, Original date boundary and university-topic query scope, Tracked reddrix.display_mode=auto, Configured root/comment/candidate/time budgets, Trial config now explicitly selects Reddrix; wrapper preserves legacy compatibility, Tracked Reddit trial configuration, Original historical date window, keywords and read-only baseline, Thin Reddit-only wrapper selects shared Reddrix explicitly (+2 more)

### Community 70 - "Router dan Batas Error"
Cohesion: 0.25
Nodes (3): client, ErrorBoundary, router

### Community 71 - "Metadata Package Frontend"
Cohesion: 0.29
Nodes (6): engines, node, name, private, type, version

### Community 72 - "Pengujian Alur Frontend"
Cohesion: 0.40
Nodes (3): AppContext, demoApi, UrlReview

### Community 73 - "Transport GraphQL Instaloader"
Cohesion: 0.22
Nodes (6): InstagramAdapter, Shared root selection and formula-safe Excel projection for social crawlers., Project the full audit rows into one sheet, applying current filters., Requires config, include and exclude matchers; performs no acquisition., Return a local date for display; relative source dates stay estimates., SocialExportMixin

### Community 75 - "Format Kode Frontend"
Cohesion: 0.50
Nodes (3): printWidth, singleQuote, trailingComma

### Community 76 - "Kontrak Ekspor Instagram"
Cohesion: 0.15
Nodes (15): Local session path and explicit360-second/3-retry policy, Instagram-only configured1800-second acquisition budget, Bounded hashtag discovery with authoritative local root filters, Spawned operations,global deadline and bounded retry policy, Explicit local login and session reuse with no automatic password replay, Historical Instagram-only campaign start and unchanged three-hour targets, Offline tests/context checks do not establish live Instagram trial success, Cookie login briefly accepted; private acquisition/reuse still rejected (+7 more)

### Community 77 - "Rencana Layanan Backend"
Cohesion: 0.50
Nodes (4): Backend PRD is not written; API/worker services remain proposed, Proposed persistent Python worker and authorized CAPTCHA browser bridge, Proposed server session, role, project isolation and idempotency, Proposed survey transactions, immutable datasets and operational audit

### Community 78 - "CI Container Frontend"
Cohesion: 0.67
Nodes (3): SPA container health and deep-link checks, Crawler frontend CI, BeeSense Crawler SPA document

### Community 103 - "thread_url"
Cohesion: 0.19
Nodes (4): Read-only exploration of completed NLP runs; no training on page reruns., SocialNLPStreamlitApp, DashboardreadsverifiedCSVwithnoAPIortrainingonrerun, Active20-topic/c_v0.4315 artifact andGemini display contract

### Community 104 - "build_topic_sentences.mjs"
Cohesion: 0.22
Nodes (6): body, payload, [payloadPath, outputPath, previewDir], sentences, topics, workbook

### Community 105 - "topic_sentence_export.py"
Cohesion: 0.28
Nodes (8): json_write(), export_payload(), main(), Prepare an original-sentence export and seal it into a new NLP snapshot., Keep original variants; remove repeated occurrences of the same text., Verify every Excel membership before publishing the complete snapshot., seal(), TopicSentenceExportTests

### Community 106 - "InstaloaderCrawler"
Cohesion: 0.17
Nodes (4): FakeReddrix, item(), Reddrix field/identity boundaries and the real, shared Excel exporter., records()

### Community 107 - ".score_coherence"
Cohesion: 0.23
Nodes (13): Return an explicit target/shortfall report and write one atomic bundle., Round robin lets YouTube run while Reddit cools down, Reddit bounded 429 policy introduced in version 1.3, Keep the same failed operation through cooldown, Native root duplicate guard within export, 429 timestamps, cooldown deadline and retry-decision audit, Recovery report interval 331.315 seconds is not a server minimum, Skip old roots before requests and check returned identity before export (+5 more)

### Community 108 - ".topic_figure"
Cohesion: 0.20
Nodes (4): _graph_positions(), Bounded topic graph: volume from filtered rows, semantic edges from the full mod, Keep the full-model layout stable while volume and edge filters change., DashboardTests

### Community 109 - "BeeSense project"
Cohesion: 0.23
Nodes (14): Stored Indonesian Gemini topic narratives, Instagram acquisition, dataset and training pipeline, Random pacing, batch pauses and exponential 429 backoff, Native-ID deduplication and latest-observation lineage, Verified 30 October 20-topic model, BeeSense project structure and root-relative paths, Separate dashboard, crawler and training runtimes, Historical Graphify memory of the native SBERT/UMAP/DBSCAN migration (+6 more)

### Community 110 - "config/social_crawler.json"
Cohesion: 0.18
Nodes (11): Per-platform bounds: max_posts 4000, max_candidates 6000, Main root reddrix.display_mode=auto, Configured Reddit policy cooldown:360seconds, Configured Reddit retry cap:threeperrun, Main config now selects Reddit backend=reddrix, Configured per-platform min_posts=1000 and min_comments_per_post=10, Target 1,000 qualified roots with bounded attempts and candidates, Root publication dates and literal keyword selection (+3 more)

### Community 111 - "Read-only native/canonical index excludes 50 YouTube and 181 Reddit roots"
Cohesion: 0.22
Nodes (11): Historical exclusion source outputs/social_20261028_01, Worker hard deadline preserves streamed partial events, Inherited SocialCrawler filters and Excel exporters, JSONL audit, dataset.xlsx and checksum manifest, Historical PARTIAL: YouTube 1,188/300 qualified; Reddit 98/58, social_data.xlsx ten-column Data worksheet, Five retained segments consolidate apart from the baseline, Read-only native/canonical index excludes 50 YouTube and 181 Reddit roots (+3 more)

### Community 112 - "Round Robin Shared Deadline"
Cohesion: 0.20
Nodes (9): Configured global acquisition budget 10800 seconds, Retained Playwright-only CAPTCHA fields:600-second wait and five-second poll, Configured platform_execution=round_robin, Coordinator waits for manual CAPTCHA without automated clicks, Atomic sibling .progress.json acquisition snapshots, Original deadline ends acquisition before final workbook publication, Historical or explicitly selected Playwright CAPTCHA wait, Round Robin Shared Deadline (+1 more)

### Community 114 - "app.py"
Cohesion: 0.31
Nodes (7): Root Docker context allowlist for relocated dashboard runtime, _load_artifacts(), main(), Streamlit entry point for local and Community Cloud dashboards.  Training lives, Dashboard build context includes root shim and artifact-reader packages, Relocated dashboard image uses root Streamlit shim and runtime-only wheels, Streamlit Community Cloud entry point; UI implementation lives in Dashboard.

### Community 115 - "Reddit Playwright CLI runner"
Cohesion: 0.33
Nodes (6): Advanced connected-browser Reddit campaign helpers, Checkpoint export to the eight-sheet contract, Native-ID provenance and bounded public excerpts, Standalone runner stops 429; coordinator 1.3 supports bounded cooldown, Isolated Chrome profile, manual CAPTCHA wait and access-barrier stops, Reddit Playwright CLI runner

### Community 116 - "Historical Reddit continuations preserve bundles and original deadline"
Cohesion: 0.70
Nodes (5): Current main configuration: platforms.reddit.enabled=true, Historical user-requested Reddit pause after 429, Historical Reddit continuations preserve bundles and original deadline, Historical Reddit pause: ten qualified and seventeen exported evidence posts, Historical platforms.reddit.enabled=false during requested pause

### Community 117 - "instagram_browser_capture.mjs"
Cohesion: 0.60
Nodes (3): instagramNavigate(), instagramRetryAfter(), instagramSourceRateLimit()

### Community 118 - "Q: ok sekarang training ulang menggunakan /Users/sakaheroji/Documents/BeeSense/outputs/social_20261030_combined_instagram_500_2h_02/social_data.xlsx, clustering. Buat 20 topik dengan coherence minimal 0.4. Lalu buat excel baru dengan tabel dengan kolom: topik, kalimat yang berada dalam cluster topik. lalu model digunakan kembali di dashboard streamlit yang di rebuild ulang, dan di commit dan dipush semuanya ke githubnya untuk di deploy ulang"
Cohesion: 0.40
Nodes (4): Answer, Outcome, Q: ok sekarang training ulang menggunakan /Users/sakaheroji/Documents/BeeSense/outputs/social_20261030_combined_instagram_500_2h_02/social_data.xlsx, clustering. Buat 20 topik dengan coherence minimal 0.4. Lalu buat excel baru dengan tabel dengan kolom: topik, kalimat yang berada dalam cluster topik. lalu model digunakan kembali di dashboard streamlit yang di rebuild ulang, dan di commit dan dipush semuanya ke githubnya untuk di deploy ulang, Source Nodes

## Knowledge Gaps
- **169 isolated node(s):** `window`, `source`, `row`, `candidate`, `singleQuote` (+164 more)
  These have ≤1 connection - possible missing edges or undocumented components.
- **20 thin communities (<3 nodes) omitted from report** — run `graphify query` to explore isolated nodes.

## Work-memory lessons

**Preferred sources** — corroborated by past sessions; start here.
- `SocialNLPStreamlitApp` (4× useful, score=3.861366614)
- `SocialNLPClusterer` (3× useful, score=2.909066527)
- `SocialCrawler` (2× useful, score=1.941443562)

## Suggested Questions
_Questions this graph is uniquely positioned to answer:_

- **Why does `SocialCrawler` connect `Koordinator Backend Sosial` to `Instagram Client dan Ekspor`, `Penjadwalan dan Riwayat Akuisisi`, `Crawler Selenium`, `Worker Instaloader`, `Panduan Pipeline BeeSense`, `Pengujian Client Instagram`, `Pengujian Koordinator Crawler`, `Worker Reddrix`, `Batas Akuisisi Reddit`, `Struktur Runtime Dashboard`, `Konfigurasi Model Aktif`, `Wrapper RedditCrawler`, `Ekspor dan Provenance Reddit`, `Riwayat Pacing Instagram`, `Arsitektur Model dan Dashboard`, `Fixture dan Pengujian Reddit`, `Runtime Docker dan Display`, `Eksekusi dan Ekspor Crawler`, `Default Backend Reddit`, `Transport GraphQL Instaloader`, `InstaloaderCrawler`, `.score_coherence`, `config/social_crawler.json`, `Read-only native/canonical index excludes 50 YouTube and 181 Reddit roots`, `Round Robin Shared Deadline`, `Reddit Playwright CLI runner`, `Historical Reddit continuations preserve bundles and original deadline`?**
  _High betweenness centrality (0.235) - this node is a cross-community bridge._
- **Why does `SocialNLPClusterer` connect `Model dan Pengujian NLP` to `Encoding dan Penyimpanan Model`, `Generator Narasi Gemini`, `Struktur Runtime Dashboard`, `Pemilihan Topik dan Coherence`, `Konfigurasi Model Aktif`, `Penjelasan Topik Dashboard`, `Pengujian Penjelasan Topik`, `Pengujian Narasi Gemini`, `Verifikasi Artefak Dataset`, `Bukti Ekstraktif Topik`, `Arsitektur Model dan Dashboard`, `Konteks dan Provenance Gemini`, `Riwayat Dataset dan Metodologi`, `Pengujian UI Streamlit`, `Riwayat Evaluasi Coherence`, `Audit Akuisisi Instagram`, `thread_url`, `topic_sentence_export.py`, `.topic_figure`, `app.py`?**
  _High betweenness centrality (0.148) - this node is a cross-community bridge._
- **Why does `BeeSense crawler, NLP and dashboard class architecture` connect `Arsitektur Model dan Dashboard` to `Rencana Produk dan Survei`, `Riwayat Pacing Instagram`, `Riwayat Sesi Instagram`, `Kontrak API Frontend`, `Struktur Runtime Dashboard`?**
  _High betweenness centrality (0.077) - this node is a cross-community bridge._
- **Are the 24 inferred relationships involving `SocialCrawler` (e.g. with `RedditCrawler` and `_SeleniumSource`) actually correct?**
  _`SocialCrawler` has 24 INFERRED edges - model-reasoned connections that need verification._
- **Are the 15 inferred relationships involving `SocialNLPClusterer` (e.g. with `SocialNLPStreamlitApp` and `Historical29October bounded15-candidate grid; shared budget retained`) actually correct?**
  _`SocialNLPClusterer` has 15 INFERRED edges - model-reasoned connections that need verification._
- **Are the 87 inferred relationships involving `ValueError` (e.g. with `browser_configuration()` and `instaloader_options()`) actually correct?**
  _`ValueError` has 87 INFERRED edges - model-reasoned connections that need verification._
- **Are the 3 inferred relationships involving `SocialNLPStreamlitApp` (e.g. with `Platform and top-five source graphs count unique topic comments` and `Term bars show bounded phrase presence in unique filtered sentences`) actually correct?**
  _`SocialNLPStreamlitApp` has 3 INFERRED edges - model-reasoned connections that need verification._