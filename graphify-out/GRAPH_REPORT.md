# Graph Report - /Users/socs3/Documents/BeeSense  (2026-10-30)

## Corpus Check
- 135 files · ~111,916 words
- Verdict: corpus is large enough that graph structure adds value.

## Summary
- 1625 nodes · 3667 edges · 114 communities (90 shown, 24 thin omitted)
- Extraction: 91% EXTRACTED · 9% INFERRED · 0% AMBIGUOUS · INFERRED: 340 edges (avg confidence: 0.78)
- Token cost: AST 0 LLM tokens; semantic usage unavailable (not a measured zero).

## Graph Freshness
- Built from commit: `e58a9bad`
- Run `git rev-parse HEAD` and compare to check if the graph is stale.
- Run `graphify update .` after code changes (no API cost).

## Community Hubs (Navigation)
- Adapter Akuisisi YouTube
- Crawler Selenium Terisolasi
- Akuisisi Instagram Terintegrasi
- Ekspor Campaign dan Resume
- Alur Akuisisi Sosial Terpadu
- Topik dan Verifikasi NLP
- Monitor Akuisisi Sintetis
- Pipeline dan Persistensi NLP
- Monitor Akuisisi Sintetis
- Akuisisi Reddit Reddrix
- Akuisisi Reddit Reddrix
- Alur Akuisisi Sosial Terpadu
- Alur Akuisisi Sosial Terpadu
- Identitas dan Kontrak Data
- Monitor Akuisisi Sintetis
- Eksplorasi Dashboard Streamlit
- Parser dan Runner Reddit
- Akses dan Parsing HTML
- Workspace React Crawler
- Ringkasan Topik Gemini
- Monitor Akuisisi Sintetis
- Pipeline dan Persistensi NLP
- Eksplorasi Dashboard Streamlit
- Topik dan Verifikasi NLP
- Akuisisi Instagram Terintegrasi
- Bundle Excel dan Provenans
- Workspace React Crawler
- Akuisisi Instagram Terintegrasi
- Ringkasan Topik Gemini
- Parser DOM Terbatas
- Snapshot NLP dan Arsip
- Eksplorasi Dashboard Streamlit
- Snapshot NLP dan Arsip
- Pengujian Penjelasan Topik
- Akuisisi Instagram Terintegrasi
- PRD Workspace Crawler
- Workspace React Crawler
- Konfigurasi SocialCrawler
- Coherence dan Quality Gate
- Pipeline dan Persistensi NLP
- Akuisisi Reddit Reddrix
- Snapshot NLP dan Arsip
- Ringkasan Topik Gemini
- PRD Workspace Crawler
- Workspace React Crawler
- Arsitektur Crawler dan Dependensi
- PRD Workspace Crawler
- PRD Workspace Crawler
- Eksplorasi Dashboard Streamlit
- Pengujian UI Streamlit
- Runbook dan Verifikasi Lokal
- Akuisisi Instagram Terintegrasi
- Helper Campaign Browser
- Validasi Redirect dan Kesalahan
- Akuisisi Reddit Reddrix
- Akuisisi Instagram Terintegrasi
- Konfigurasi SocialCrawler
- Akuisisi Instagram Terintegrasi
- Coherence dan Quality Gate
- Akuisisi Instagram Terintegrasi
- Alur Akuisisi Sosial Terpadu
- Akuisisi Instagram Terintegrasi
- Coherence dan Quality Gate
- Workspace React Crawler
- Akuisisi Instagram Terintegrasi
- PRD Workspace Crawler
- Snapshot NLP dan Arsip
- Akuisisi Instagram Terintegrasi
- Operasi dan Verifikasi BeeSense
- Akuisisi Reddit Reddrix
- Workspace React Crawler
- Pipeline dan Persistensi NLP
- Alur Akuisisi Sosial Terpadu
- Snapshot NLP dan Arsip
- Workspace React Crawler
- Akuisisi Reddit Reddrix
- Eksplorasi Dashboard Streamlit
- Pipeline dan Persistensi NLP
- Alur Akuisisi Sosial Terpadu
- Snapshot NLP dan Arsip
- Akuisisi Instagram Terintegrasi
- Identitas dan Kontrak Data
- Monitor Akuisisi Sintetis
- Eksplorasi Dashboard Streamlit
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
- Akuisisi Instagram Terintegrasi
- Akuisisi Reddit Reddrix
- Adapter Akuisisi YouTube

## God Nodes (most connected - your core abstractions)
1. `SocialCrawler` - 104 edges
2. `SocialNLPClusterer` - 98 edges
3. `SocialNLPStreamlitApp` - 59 edges
4. `SocialCrawlerTests` - 42 edges
5. `InstagramCrawlerTests` - 33 edges
6. `Reddrix-backed RedditCrawler runbook` - 32 edges
7. `Runbook and historical record for finalized partial crawler campaign` - 30 edges
8. `NLPTests` - 27 edges
9. `file_hash()` - 26 edges
10. `IntegratedInstagram1.5.1 withhistoricalprivate-API/Chrome trials` - 26 edges

## Surprising Connections (you probably didn't know these)
- `Configured Reddit policy cooldown:360seconds` --conceptually_related_to--> `Bounded HTTP429 policy introduced in1.3 and retained by1.4`  [INFERRED]
  config/social_crawler.json → docs/crawler/SOCIAL_CRAWLER.md
- `Configured Reddit retry cap:threeperrun` --conceptually_related_to--> `Bounded HTTP429 policy introduced in1.3 and retained by1.4`  [INFERRED]
  config/social_crawler.json → docs/crawler/SOCIAL_CRAWLER.md
- `Browserworker context permitscode/config whileexcludingauth/profiles` --references--> `InstagramBrowserWorker`  [INFERRED]
  deployment/docker/Dockerfile.instagram-browser.dockerignore → Crawler/Backend/instagram_browser.py
- `Fiveintegrationtests plus76NLP andoneisolateddashboardtestpassed` --conceptually_related_to--> `InstagramIntegrationTests`  [INFERRED]
  docs/crawler/INSTAGRAM_PIPELINE_20261030.md → tests/crawler/test_social_crawler_instagram.py
- `Historical fixed top10/window110/all15878-unique macro c_v protocol` --semantically_similar_to--> `Gensim c_v protocol: top 10 terms, window 110, phrase tokens`  [INFERRED] [semantically similar]
  graphify-out/memory/query_20261028_155746_hitung_coherence_minimal_0_4__retrain_sbert_umap_d.md → docs/machine-learning/SOCIAL_NLP.md

## Import Cycles
- None detected.

## Hyperedges (group relationships)
- **Stoppedacquisition→auditedfinalcorpus→verified20topics→contextualGeminiCSV** — docs_crawler_instagram_pipeline_20261030_acquisition_user_stop, docs_crawler_instagram_pipeline_20261030_final_native_identity_corpus, docs_crawler_instagram_pipeline_20261030_final_verified_model, docs_crawler_instagram_pipeline_20261030_actual_contextual_gemini_csv [EXTRACTED 1.00]
- **Topicweights,fittedcontext,receiptandCSV2bindoneversionednarrative** — docs_machine_learning_gemini_topic_narratives_weighted_keyword_input, docs_machine_learning_gemini_topic_narratives_fitted_sentence_context_selection, docs_machine_learning_gemini_topic_narratives_receipt_resume_binding, docs_machine_learning_gemini_topic_narratives_extension_validation [EXTRACTED 1.00]
- **VerifiedmodelandCSVsupportread-onlythree-platformDashboard** — docs_dashboard_dashboard_design_verified_model_20261030, docs_dashboard_dashboard_design_three_platform_support, docs_dashboard_dashboard_design_gemini_read_only_narratives [EXTRACTED 1.00]
- **Root shim, UI implementation, package CLIs and ROOT resolution preserve application entry contracts** — docs_project_structure_component_layout, docs_project_structure_streamlit_root_shim, docs_project_structure_repository_root_resolution, docs_project_structure_package_module_cli, docs_project_structure_runtime_requirements_layout [EXTRACTED 1.00]
- **Relocation preserves artifacts while runtime packaging and publication remain distinct verification stages** — docs_project_structure_data_preservation, docs_project_structure_docker_root_context, readme_reorganization_publication_pending, readme_active_coherence, config_social_nlp_active_output_dir [INFERRED 0.95]
- **All three declared images retain module/config layout under root build contexts** — deployment_docker_dockerfile_dashboard_wheels_python_version, deployment_docker_dockerfile_reddrix_one_shot_worker, deployment_docker_dockerfile_selenium_included_reddrix_manifest, deployment_docker_dockerfile_dashboard_context_allowlist, docs_project_structure_docker_root_context [INFERRED 0.95]
- **Verified synthetic React delivery remains separate from proposed production worker/API acceptance** — crawler_frontend_readme_react_crawler_implementation, crawler_frontend_docs_delivery_verified_frontend_checks, crawler_frontend_docs_delivery_synthetic_demo_limitations, crawler_frontend_docs_api_contract_expected_api_contract, prd_prd_backend_readme_persistent_acquisition_worker, prd_prd_frontend_acceptance_criteria_crawler_production_acceptance_gates [INFERRED 0.95]
- **Complete survey/native-source provenance and validated schema gates protect immutable NLP selection** — prd_prd_frontend_prd_frontend_crawler_complete_response_survey_contract, prd_prd_frontend_prd_frontend_crawler_native_identity_provenance_rules, prd_prd_frontend_prd_frontend_crawler_immutable_dataset_nlp_selection, crawler_frontend_docs_api_contract_server_bound_survey_validation_commit, prd_prd_machine_learning_readme_survey_schema_adapter_requirement, crawler_frontend_readme_preview_export_and_schema_gate, prd_prd_machine_learning_readme_new_social_source_adapter_gate [INFERRED 0.95]

## Communities (114 total, 24 thin omitted)

### Community 0 - "Adapter Akuisisi YouTube"
Cohesion: 0.09
Nodes (34): error_code(), load_settings(), main(), parser(), run(), SafeLogger, Settings, video_url() (+26 more)

### Community 1 - "Crawler Selenium Terisolasi"
Cohesion: 0.07
Nodes (19): _barrier(), _create_driver(), main(), Content quoting an error is never used to classify an access barrier., Convert the shared rendered DOM capture without inventing identities., One browser operation. The parent enforces the hard process deadline., Stream evidence before completion; the original supervisor can retain it., Drop-in SocialCrawler with Selenium for both platforms and shared exports. (+11 more)

### Community 2 - "Akuisisi Instagram Terintegrasi"
Cohesion: 0.07
Nodes (7): Clock, FakeClient, InstagramCrawlerTests, Offline contract/deadline tests; fixture data is always marked synthetic., records(), spawn_fixture(), spawn_hanging()

### Community 3 - "Ekspor Campaign dan Resume"
Cohesion: 0.08
Nodes (16): atomic_json(), barrier_status(), campaign_plan(), decode_cli_output(), find_cli(), PlaywrightCLI, rate_limit_seconds(), run() (+8 more)

### Community 4 - "Alur Akuisisi Sosial Terpadu"
Cohesion: 0.14
Nodes (5): rd_events(), receipt(), SocialCrawlerTests, spawn_youtube_fixture(), yt_events()

### Community 5 - "Topik dan Verifikasi NLP"
Cohesion: 0.08
Nodes (14): Atomic baseline-then-new workbook merge preserves native identity and provenance, Merged corpus: 29, 099 rows, 1, 517 roots and 27, 582 comments/replies, Combined workbook provenance PASS with immutable source hashes and row lineage, identity(), main(), merge(), merge_unique(), Merge compact crawl workbooks, rejecting repeated native content identities. (+6 more)

### Community 6 - "Monitor Akuisisi Sintetis"
Cohesion: 0.10
Nodes (32): ConfigReview(), advance(), cap, committed, dataset(), get(), load(), plans (+24 more)

### Community 7 - "Pipeline dan Persistensi NLP"
Cohesion: 0.12
Nodes (8): Encode with SBERT, fit UMAP + DBSCAN and optionally merge to a topic count., SocialNLPClusterer, CloudRuntimeTests, Run in an isolated Cloud environment, using only root requirements.txt., DashboardTests, encoder(), fixture(), NLPTests

### Community 8 - "Monitor Akuisisi Sintetis"
Cohesion: 0.12
Nodes (27): Automatic(), Baselines(), ConfigFields(), Manual(), ManualUrl(), labels, sample, Survey() (+19 more)

### Community 9 - "Akuisisi Reddit Reddrix"
Cohesion: 0.09
Nodes (33): Configured 360-second policy and three HTTP 429 retries, Configured new sorting differs from Reddrix capability, Installed Reddrix 1.2.14 and Camoufox 156 browser evidence, Preserved compact SocialCrawler workbook, Historical trial 01 ended PARTIAL with zero posts, Hard-deadline subprocess retains streamed records, BeeSense interoperation delay differs from library request retries, Historical v1.0.0 module-specific non-Linux Xvfb shim (+25 more)

### Community 10 - "Akuisisi Reddit Reddrix"
Cohesion: 0.10
Nodes (9): main(), Reddit-only compatibility entry point for the integrated SocialCrawler Reddrix b, Run only Reddit through the shared Reddrix implementation in SocialCrawler., RedditCrawler, FakeReddrix, item(), Reddrix field/identity boundaries and the real, shared Excel exporter., records() (+1 more)

### Community 11 - "Alur Akuisisi Sosial Terpadu"
Cohesion: 0.10
Nodes (9): main(), Describe the acquisition backend independently of the shared export., Compose platform workers with one configuration, scheduler and export bundle., Validate and return the effective plan without browser/network access., Re-export saved Contents without network or modifying the source bundle., SocialCrawler, Mixed bundle retains source-specific backend provenance, InstagramIntegrationTests (+1 more)

### Community 12 - "Alur Akuisisi Sosial Terpadu"
Cohesion: 0.13
Nodes (23): collect_reddrix(), _config(), _keywords(), load_reddrix(), normalize_reddrix_item(), _number(), Map Reddrix 1.2.14 dictionaries without inventing identity or dates., Reddrix anti-bot exceptions do not expose an authoritative HTTP status. (+15 more)

### Community 13 - "Identitas dan Kontrak Data"
Cohesion: 0.15
Nodes (9): add_readme(), ContentInput, ContractTests, Dataset, digest(), Shared pipeline; adapters cannot choose their own headers or cell formats., RecordFactory, utc_datetime() (+1 more)

### Community 14 - "Monitor Akuisisi Sintetis"
Cohesion: 0.20
Nodes (24): Shell(), DatasetView(), History(), Composition(), JobDetail(), liveStates, PlatformCard(), ProgressChart() (+16 more)

### Community 15 - "Eksplorasi Dashboard Streamlit"
Cohesion: 0.13
Nodes (4): Read-only exploration of completed NLP runs; no training on page reruns., Count sentence occurrences; never confuse them with distinct comments., SocialNLPStreamlitApp, Keyboard dropdown and URL-bound topic/explanation navigation

### Community 16 - "Parser dan Runner Reddit"
Cohesion: 0.12
Nodes (16): bounded_events(), HtmlSource, load_settings(), LocalHtmlSource, parsed_number(), PublicHtmlSource, ABC, Normalize a source event; write only through the shared Dataset/Sink. (+8 more)

### Community 17 - "Akses dan Parsing HTML"
Cohesion: 0.19
Nodes (10): first(), fixture_page(), native_fullname(), object_key(), RedditAdapter, RedditHtmlParser, RedditRecordFactory, RedditTests (+2 more)

### Community 18 - "Workspace React Crawler"
Cohesion: 0.07
Nodes (26): compilerOptions, allowImportingTsExtensions, esModuleInterop, isolatedModules, jsx, lib, module, moduleResolution (+18 more)

### Community 19 - "Ringkasan Topik Gemini"
Cohesion: 0.17
Nodes (18): Derive Indonesian Gemini labels after topic count and coherence pass., Merge entire DBSCAN groups using sentence-weighted Ward linkage.          Minimi, build_prompt(), canonical(), digest(), generate(), load_key(), Gemini narratives grounded in ranked topic keywords and representative sentences (+10 more)

### Community 20 - "Monitor Akuisisi Sintetis"
Cohesion: 0.10
Nodes (20): ApiError, base, httpApi, post(), request(), Baseline, Config, Counts (+12 more)

### Community 21 - "Pipeline dan Persistensi NLP"
Cohesion: 0.17
Nodes (7): file_hash(), json_write(), main(), Publish a new versioned sidecar; never modify the original run., Reuse immutable SBERT features only after verifying data/model identity., Preserve explicit zero distances, including identical sentence vectors., Select DBSCAN parameters on UMAP; evaluate in original SBERT geometry.

### Community 22 - "Eksplorasi Dashboard Streamlit"
Cohesion: 0.11
Nodes (9): Root Docker context allowlist for relocated dashboard runtime, _explain_filtered(), _load_artifacts(), main(), Streamlit entry point for local and Community Cloud dashboards.  Training lives, Dashboard build context includes root shim and artifact-reader packages, Relocated dashboard image uses root Streamlit shim and runtime-only wheels, Streamlit Community Cloud entry point; UI implementation lives in Dashboard. (+1 more)

### Community 23 - "Topik dan Verifikasi NLP"
Cohesion: 0.19
Nodes (22): Final PARTIAL: YouTube 1, 188 exported/300 qualified; Reddit 98/58, Bounded 1.3 cooldown applied to user-authorized continuation 04, YouTube date hint aids discovery; exact coordinator timestamp filter decides eligibility, Historical active-campaign state; acquisition now finalized PARTIAL, Before segment 03: qualified YouTube6/Reddit17; exported evidence8/31, Before 04 cumulative qualified YouTube77/Reddit26; evidence325/47, Campaign descriptor records finalized PARTIAL status and five-segment accounting, Historical descriptor-based monitoring now resolves final campaign counters (+14 more)

### Community 24 - "Akuisisi Instagram Terintegrasi"
Cohesion: 0.20
Nodes (20): collect(), create_client(), error_receipt(), instagram_worker(), load_client(), login_from_file(), login_local(), login_with_saved_password() (+12 more)

### Community 25 - "Bundle Excel dan Provenans"
Cohesion: 0.19
Nodes (12): BundleSink, dumps(), main(), parser(), Validate the embedded contract; an external descriptor is optional., Atomic new directory; streaming JSONL + streaming, formula-safe Excel., run(), run_self_tests() (+4 more)

### Community 26 - "Workspace React Crawler"
Cohesion: 0.10
Nodes (21): devDependencies, eslint, @eslint/js, jsdom, prettier, @testing-library/user-event, @types/react, @types/react-dom (+13 more)

### Community 27 - "Akuisisi Instagram Terintegrasi"
Cohesion: 0.22
Nodes (20): One LoginRequired recovery with verification-code preservation, CAAHTTP200 without session;legacyHTTP400 needs_upgrade, Cookie accepted for login/account read; trial02 firsthashtag LOGIN_REQUIRED, Explicit auto/password/sessionid login selection, Historical initial password rejection and trial01 LOGIN_REQUIRED/zero, Historical real-cookie header-patch validation fails SDKAttributeError, Instaloader preflight fails before discovery;zero acquired data, Future Instaloader worker must retain one run-wide context/rate controller (+12 more)

### Community 28 - "Ringkasan Topik Gemini"
Cohesion: 0.18
Nodes (5): Nine Gemini offline tests and all20 actual contextual CSV rows validated, GeminiArtifactTests, GeminiTests, response(), topic()

### Community 29 - "Parser DOM Terbatas"
Cohesion: 0.16
Nodes (9): assert_accessible(), BoundedDom, content_node(), MemorySink, Node, Small serialised-DOM reader, not a browser or full HTML5 repair engine., rendered_text(), walk() (+1 more)

### Community 30 - "Snapshot NLP dan Arsip"
Cohesion: 0.15
Nodes (19): DashboardreadsverifiedCSVwithnoAPIortrainingonrerun, Active20-topic/c_v0.4315 artifact andGemini display contract, Verified current model and20context-grounded narratives, Current20-topic macro c_v0.4315219014 model, Active33034-record three-platform corpus, Producer2.4 contextual Gemini stage after verified model gate, Prior Graphify memory: Selenium crawler preserves Excel contract, BeeSense crawler, NLP and dashboard class architecture (+11 more)

### Community 31 - "Eksplorasi Dashboard Streamlit"
Cohesion: 0.16
Nodes (16): Count evidence in the filter, keeping sentences/comments/parents distinct., Filters retain model membership and do not recompute c_v, Selected-topic c_v card is separate from the full-model mean, Occurrences, unique sentences, comments and source roots have different denominators, Five artifact-backed Streamlit analysis views, Platform and top-five source graphs count unique topic comments, Responsive cards, visible keyboard focus and chart/table alternatives verified, Four selected-topic cards: unique comments, share, source roots and topic c_v (+8 more)

### Community 32 - "Snapshot NLP dan Arsip"
Cohesion: 0.14
Nodes (18): Historical v 1 HDBSCAN directional counts for 51 topics, ImmutableolderNLPsnapshots including29Octobercombinedrun, Historicalcorporaandscoresarenotcurrentqualitycomparators, Obsidian dashboard dataset provenance, FinalnativeIDauditwithpreservedhistoricalchecksums, Artifact-only dashboard without Gensim/Torch imports, Obsidian Cloud runbook: streamlit_apps.py, Python 3.12 and complete artifact publication, BeeSense startup, verification and coherence training runbook (+10 more)

### Community 33 - "Pengujian Penjelasan Topik"
Cohesion: 0.25
Nodes (3): ExplanationTests, model_from_counts(), profile()

### Community 34 - "Akuisisi Instagram Terintegrasi"
Cohesion: 0.21
Nodes (11): InstagramAdapter, media_pk_from_url(), media_url(), native_pk(), normalize_item(), object_key(), Map explicit native IDs/timestamps; do not infer authors or text coverage., Accept only Instagram post/reel permalinks; strip tracking parameters. (+3 more)

### Community 35 - "PRD Workspace Crawler"
Cohesion: 0.15
Nodes (17): Late plan, URL and survey validation is ignored after input changes, Curated two-menu contract with URL/Survey under Manual, Curated immutable dataset selection does not train or change Dashboard, Curated Crawler PRD status:frontend implemented, backend pending, Draft acceptance criteria are release requirements, not a React test report, Acceptance: plan invalidation, field errors and idempotent job creation, Acceptance: complete consented survey responses and conflict-safe import, Acceptance: authoritative snapshots, stale recovery and worker barriers (+9 more)

### Community 36 - "Workspace React Crawler"
Cohesion: 0.12
Nodes (17): dependencies, @fontsource-variable/plus-jakarta-sans, lucide-react, papaparse, react, react-dom, react-router-dom, @tanstack/react-query (+9 more)

### Community 37 - "Konfigurasi SocialCrawler"
Cohesion: 0.15
Nodes (13): Main root reddrix.display_mode=auto, Configured global acquisition budget 10800 seconds, Retained Playwright-only CAPTCHA fields:600-second wait and five-second poll, Configured Reddit policy cooldown:360seconds, Configured Reddit retry cap:threeperrun, Main config now selects Reddit backend=reddrix, Configured platform_execution=round_robin, Coordinator waits for manual CAPTCHA without automated clicks (+5 more)

### Community 38 - "Coherence dan Quality Gate"
Cohesion: 0.12
Nodes (16): Internal model metrics do not establish accuracy or representativeness, Unweighted mean across all 20 final non-noise topics, Stored protocol, reference hash, baseline identity and per-topic scores, Gensim c_v protocol: top 10 terms, window 110, phrase tokens, Historical46143-sentence reference; current corpus remains separately bound, Non-noise c-TF-IDF unigram/bigram labels, Original DBSCAN IDs and full reduction mapping survive final topic IDs, Historical7/20 shortfalls; current model has8/20 (+8 more)

### Community 39 - "Pipeline dan Persistensi NLP"
Cohesion: 0.12
Nodes (5): Identify the parent thread, not the individual comment URL., Extract real sentences using relevance plus MMR diversity., Evidence-grounded topic descriptions and descriptive, source-aware trends., Explain already verified artifacts without encoding or fitting again., Rule-based segmentation preserving exact offsets in the original text.

### Community 40 - "Akuisisi Reddit Reddrix"
Cohesion: 0.18
Nodes (15): Read-only historical baseline exclusion, Original date boundary and university-topic query scope, Tracked reddrix.display_mode=auto, Configured root/comment/candidate/time budgets, Trial config now explicitly selects Reddrix; wrapper preserves legacy compatibility, Tracked Reddit trial configuration, Adaptive display v1.1.0 auto platform policy, CLI/class display overrides and explicit virtual preconditions (+7 more)

### Community 41 - "Snapshot NLP dan Arsip"
Cohesion: 0.24
Nodes (15): Active artifacts outputs/nlp_20261030_instagram_topics20_02, Configured33034-record final merged workbook, Active20-topic Instagram-inclusive model configuration, Current active Gemini enabled; historical disabled state retained, Final Instagram-inclusive20-topic/Gemini configuration, Active20-topic Instagram-inclusive model configuration, RetainedSBERTrevision,UMAP/DBSCANbudget andexplanationgates, All20 actual contextual Gemini narratives validated (+7 more)

### Community 42 - "Ringkasan Topik Gemini"
Cohesion: 0.19
Nodes (15): Verified model configuration enables contextual Gemini CSV, Complete contextual20-row Gemini CSV passes bundle gate, Boundedtransientretryandfail-closedpublication, Prompt2/CSV2 with preserved keyword-only version1, Atomic20-row contextual CSV with per-topic provenance, ContextualCSVextension2 binds Parquet; legacyextension1 supported, Deterministic fitted-sentence context ranking, Gemini GenerateContent APIreference (+7 more)

### Community 43 - "PRD Workspace Crawler"
Cohesion: 0.17
Nodes (15): Final style samples:96desktop/78narrow444px elements,all black and≥13 px, React frontend and simulation verified; production acquisition integration unavailable, Applied UX fixes:linked errors, step validation, deep links, drawer focus and inertness, Browser actual widths400/444px;requested360px remains unproven, Production release waits for API/worker/access/export and survey adapter integration, Demo IDs, baseline data and downloads are synthetic rather than acquisition evidence, Production build defaults API mode;missing backend fails explicitly, Implemented adapter polls snapshots every five seconds;worker state stays server-owned (+7 more)

### Community 45 - "Arsitektur Crawler dan Dependensi"
Cohesion: 0.15
Nodes (14): Shared rendered_thread_dom.mjs extraction, Relative dates remain calendar estimates, Historical Selenium implementation preset:500roots/platform andonehour, Worker hard deadline preserves streamed partial events, Inherited SocialCrawler filters and Excel exporters, Separate non-root crawler container with Selenium Grid, Fresh Chrome guest session per operation, Official Selenium Manager ChromeDriver selection (+6 more)

### Community 46 - "PRD Workspace Crawler"
Cohesion: 0.15
Nodes (14): Server history pagination, SSE, templates and organizational login remain future, Project-prefixed cookie-session API requires server CORS/CSRF/access controls, Expected typed frontend API contract; backend implementation pending, Increasing snapshotVersion and server-owned actions drive reconciliation, Safe structured errors distinguish API429 from worker-platform429, Typed plan/job requests bind plan IDs, idempotency and safe stop, Backend wrapper must translate local WIB dates and TypeScript field names, Survey answers avoid URL/localStorage;safe text and CSV formula handling (+6 more)

### Community 47 - "PRD Workspace Crawler"
Cohesion: 0.19
Nodes (14): locatorKey is normalized permalink identity;nativeId may await backend verification, Survey commit binds review to session/project and revalidates conflicts, Implemented UI flows:automatic/manual, monitor, survey and dataset review, Frontend URL review and minat-studi-v1 survey form/CSV/XLSX workflows, Proposed server-owned monitor separates units and finalization states, Automatic four-step source/filter/baseline/review workflow, Proposed survey schema preserves declared roles, questions, permission and whole responses, Crawler frontend PRD v1.1 with implemented seven-source UI and pending backend (+6 more)

### Community 50 - "Runbook dan Verifikasi Lokal"
Cohesion: 0.26
Nodes (13): Full Python3.12 tooling uses requirements/dev.txt and relocated package paths, Declared Reddrix lint/format and offline contract test step, CI verifies full Python 3.12 tooling separately from dashboard-only Python 3.12/3.14 matrix, Saved-model dashboard uses a separate runtime;full refitting stays Python 3.12, New-corpus native SBERT encoding or exact verified cache reuse, Separate SBERT training and artifact-only dashboard environments, Training/evaluation-only Gensim coherence requirements, Separate Python 3.12 development/training regression dependency entry (+5 more)

### Community 51 - "Akuisisi Instagram Terintegrasi"
Cohesion: 0.18
Nodes (13): Ignoredlocalcredentials/profiles;explicitnewmodelandGemininoteallowlist, Local session path and explicit360-second/3-retry policy, Instagram-only configured1800-second acquisition budget, Bounded hashtag discovery with authoritative local root filters, Spawned operations,global deadline and bounded retry policy, Explicit local login and session reuse with no automatic password replay, Offline tests/context checks do not establish live Instagram trial success, Cookie login briefly accepted; private acquisition/reuse still rejected (+5 more)

### Community 52 - "Helper Campaign Browser"
Cohesion: 0.27
Nodes (8): classifyCaptureFailure(), enrichBatch(), rateLimitSeconds(), inWindow(), mergeCandidates(), row, source, window

### Community 53 - "Validasi Redirect dan Kesalahan"
Cohesion: 0.23
Nodes (8): HtmlPage, now_iso(), Only public HTML pages on the canonical host; never auth/API routes., RestrictedRedirect, safe_web_url(), SourceFailure, Exception, HTTPRedirectHandler

### Community 55 - "Akuisisi Instagram Terintegrasi"
Cohesion: 0.21
Nodes (12): Standalone browser1800-second preset, updated bounded retry, instagramDocumentPayload(), Browserworker context permitscode/config whileexcludingauth/profiles, Declared Node/Chrome/Python browserworker atUID10001, Browser discovery follows InstagramUI order withlocaleligibilitychecks, Bind document-script comments by native DOM permalink andsame shortcode, macOS headed trial andLinuxprepared-profile requirements, One dedicated persistentprofile andpinnedCLI/session perrun (+4 more)

### Community 56 - "Konfigurasi SocialCrawler"
Cohesion: 0.26
Nodes (12): Per-platform bounds: max_posts 4000, max_candidates 6000, Current main configuration: platforms.reddit.enabled=true, Configured per-platform min_posts=1000 and min_comments_per_post=10, Target 1000 qualified new roots per platform, bounded attempts and candidates, Explicit partial export and qualified-post shortfall after acquisition, Historical Reddit pause after HTTP 429, superseded by user-authorized resume, Root-publication date and literal keyword selection, Per-platform qualifying-root targets and shortfalls (+4 more)

### Community 57 - "Akuisisi Instagram Terintegrasi"
Cohesion: 0.18
Nodes (12): Read-onlyhistoricalbaselineandbothInstagramtrialexclusions, Instagram-only10800-second browser preset; bounded429 retry, Historical6065-second/870-root Instagram resume preset, Current Instagram bounded retry configuration; historical execution chronology, Historical Instagram-only campaign start and unchanged three-hour targets, Chrome remains available for operator inspection, Browser response429 and private-header boundary, Historical Instagram run01:248 posts and2128 comments (+4 more)

### Community 58 - "Coherence dan Quality Gate"
Cohesion: 0.23
Nodes (12): Configured c_v threshold 0.4 with topn 10 and window 110, Configured final topic target: 20, Additional c_v >=0.4 gate preserves earlier eligibility rules, DBSCAN core points and noise without membership probabilities, Two UMAP 10 D projections seeded 42 and 43, Euclidean DBSCAN with reusable bounded radius graphs, Historical29October bounded15-candidate grid; shared budget retained, Evaluate final topic partitions before candidate selection (+4 more)

### Community 59 - "Akuisisi Instagram Terintegrasi"
Cohesion: 0.24
Nodes (7): browser_configuration(), browser_script(), InstagramBrowserWorker, Serial Chrome acquisition using a persistent profile and manual login.  The same, _configuration(), InstagramSettings, _integer()

### Community 60 - "Alur Akuisisi Sosial Terpadu"
Cohesion: 0.27
Nodes (11): Return an explicit target/shortfall report and write one atomic bundle., Round-robin advances YouTube while Reddit waits for readiness, Bounded HTTP429 policy introduced in1.3 and retained by1.4, Retain the same failed Reddit operation until cooldown expires, Per-run canonical root duplicate guard, Persist actual 429 finish timestamps, cooldown deadline and retry decisions, Observed recovery-notice interval≈331.315 seconds is not a server minimum, Receipt retry_after_seconds60 may be Chrome parser fallback (+3 more)

### Community 61 - "Akuisisi Instagram Terintegrasi"
Cohesion: 0.18
Nodes (12): 27–30October inclusiverefers tosourceacquisitiondate,notpostdate, User stopped Instagram acquisition; no subsequent crawl, Final audited33034-record Instagram-inclusive corpus, Fiveintegrationtests plus76NLP andoneisolateddashboardtestpassed, Bounded Instagram recovery does not override user stop, Latestnative-ID observation dedupwithrootconflict rejection, Versionedmergepublishesrecordlineage/duplicateauditandchecksums, 20-topic/coherence gate passed; active configuration switched (+4 more)

### Community 62 - "Coherence dan Quality Gate"
Cohesion: 0.23
Nodes (12): Historical combined snapshot QA; relocated root shim checked offline, Historical29October macro c_v0.4720034334, Pinned multilingual SentenceTransformer safetensors encoder, Historical29October exact-corpus SBERT/UMAP cache evidence, Overflow-window averaging and L 2-normalized 384 D embeddings, Historical old-corpus baselines retained; no cross-corpus quality comparison, Encoder cache bound to immutable revision and text/checksums, Checksum-verified reuse of immutable SBERT embeddings (+4 more)

### Community 63 - "Workspace React Crawler"
Cohesion: 0.18
Nodes (11): scripts, build, build:demo, check, dev, format, format:check, lint (+3 more)

### Community 65 - "PRD Workspace Crawler"
Cohesion: 0.22
Nodes (10): Dataset.nlpSupported requires tested schema and every included source adapter, Versioned datasets provide50-row pages, authorized files and selection-only NLP handoff, Demo preview-only downloads and validated-source NLP gate, Curated available UI flows retain worker authority and survey metadata, New survey schema must preserve role, question, response, version and permission, Version/checksum handoff requires partial acceptance and supported schema, Machine Learning PRD remains unwritten; Crawler handoff dependencies listed, 20 topics/coherence≥0.4 belong to future model criteria, not Crawler success (+2 more)

### Community 66 - "Snapshot NLP dan Arsip"
Cohesion: 0.36
Nodes (9): Isolated dashboard-runtime matrix for Python 3.12 and3.14, Cloud AppTest regression opens all five views/T04 without installed or imported training libraries, Obsidian runbook records Python 3.14 failure and dashboard-only packaging fix, Historical Python 3.14.10 Cloud install failure:ONNX cp314 wheels and Numba support, PyArrow 24.0.0 matches Cloud guard for Arrow/mimalloc threaded-import compatibility, Cloud root requirements now install dashboard-only dependencies, Root Cloud requirements include relocated dashboard-only runtime, NumPy 2.2.6 below Python 3.14;2.3.5 on Python 3.14 and later (+1 more)

### Community 67 - "Akuisisi Instagram Terintegrasi"
Cohesion: 0.28
Nodes (5): InstagramCrawler, main(), Standalone trial. The production SocialCrawler backend stays unchanged., run_instagram_worker(), Offline checks for the Chrome boundary, native identity, and provenance.

### Community 68 - "Operasi dan Verifikasi BeeSense"
Cohesion: 0.28
Nodes (5): Shared root selection and formula-safe Excel projection for social crawlers., Project the full audit rows into one sheet, applying current filters., Requires config, include and exclude matchers; performs no acquisition., Return a local date for display; relative source dates stay estimates., SocialExportMixin

### Community 69 - "Akuisisi Reddit Reddrix"
Cohesion: 0.32
Nodes (8): CI discovers shared-core Reddrix integration regressions, Actual macOS lifecycle test versus mocked Linux display matrix, Reddrix Docker image unbuilt: local daemon unavailable, Integrated offline tests and macOS lifecycle scope, Seven regression cases verify shared default backend contracts, Current offline tests pass; actual Linux and reorganized Docker image unverified, Reorganized Docker image remains unbuilt while local daemon is unavailable, Historical 16 adapter/export/display tests; current crawler suite 72 pass and 1 skip

### Community 70 - "Workspace React Crawler"
Cohesion: 0.25
Nodes (3): client, ErrorBoundary, router

### Community 71 - "Pipeline dan Persistensi NLP"
Cohesion: 0.36
Nodes (7): main(), published_source_files(), Verify published source workbooks and the dashboard artifact bundle., Verify record identity independently of sentence-text deduplication., A merge report binds its small, explicit audit sidecars to the input., verify(), verify_native_dataset()

### Community 72 - "Alur Akuisisi Sosial Terpadu"
Cohesion: 0.38
Nodes (7): Historical exclusion source outputs/social_20261028_01, JSONL audit, dataset.xlsx and checksum manifest, Five verified segments consolidate with zero duplicate roots and zero baseline overlap, Read-only canonical/native identity index excludes 50 old YouTube and 181 Reddit roots, Historical root skip before request and returned-identity check before export, Historical audit workbook: 50 YouTube and 181 Reddit root identities, Each continuation excludes original dataset and every prior campaign segment

### Community 73 - "Snapshot NLP dan Arsip"
Cohesion: 0.29
Nodes (7): Delivery records 50 passing tests, lint/format and production API build, Curated demo storage and API-mode failure boundaries, Curated React Crawler implementation with synthetic/API separation, Curated local React dev/Nginx runtime is distinct from Dashboard, Curated PRD 1.1 theme and seven-source UI distinguish planned backend adapters, Curated delivery evidence separates UX audit from real backend readiness, Seven implemented UI/demo sources;only two Python adapters exist

### Community 74 - "Workspace React Crawler"
Cohesion: 0.29
Nodes (6): engines, node, name, private, type, version

### Community 75 - "Akuisisi Reddit Reddrix"
Cohesion: 0.43
Nodes (7): Crawler root-context allowlist preserves package/config/dependency layout, Relocated combined crawler image runs package module as UID10001, Selenium build context allows the newly included dependency manifest, Relocated Selenium image preserves included requirements and package modules, Isolated local environment and separately downloaded browser, Shared crawler pins include yt-dlp and isolated Reddrix manifest, Isolated Reddrix 1.2.14 crawler dependency pins

### Community 76 - "Eksplorasi Dashboard Streamlit"
Cohesion: 0.29
Nodes (7): Historical combined20 UI/runtime verification retained after relocation, Historical Graphify memory of the native SBERT/UMAP/DBSCAN migration, Active Instagram-inclusive 20-topic snapshot: macro c_v 0.4315219014, Retained historical NLP snapshots and changed-corpus score limits, BeeSense project and dashboard runbook, Documented coordinator 1.3 cooldown 360 seconds with at most 3 retries, Preserved baseline, versioned merged source and complete active artifacts

### Community 78 - "Alur Akuisisi Sosial Terpadu"
Cohesion: 0.33
Nodes (6): Advanced connected-browser Reddit campaign helpers, Checkpoint export to the eight-sheet contract, Native-ID provenance and bounded public excerpts, Standalone runner stops 429; coordinator 1.3 supports bounded cooldown, Isolated Chrome profile, manual CAPTCHA wait and access-barrier stops, Reddit Playwright CLI runner

### Community 79 - "Snapshot NLP dan Arsip"
Cohesion: 0.33
Nodes (6): Component-oriented repository layout after SocialCrawler integration, Reorganization preserves data bytes and requires no migration, Relocated Dockerfiles preserve package/config layout from repository root, Module CLIs and worker spawn import relocated packages, Package ROOT preserves repository-relative configuration and artifact paths, Runtime manifests live under requirements with relative includes

### Community 80 - "Akuisisi Instagram Terintegrasi"
Cohesion: 0.60
Nodes (3): instagramNavigate(), instagramRetryAfter(), instagramSourceRateLimit()

### Community 82 - "Monitor Akuisisi Sintetis"
Cohesion: 0.40
Nodes (3): AppContext, demoApi, UrlReview

### Community 83 - "Eksplorasi Dashboard Streamlit"
Cohesion: 0.40
Nodes (3): _graph_positions(), Bounded topic graph: volume from filtered rows, semantic edges from the full mod, Keep the full-model layout stable while volume and edge filters change.

### Community 85 - "Workspace React Crawler"
Cohesion: 0.50
Nodes (3): printWidth, singleQuote, trailingComma

## Knowledge Gaps
- **125 isolated node(s):** `window`, `source`, `row`, `candidate`, `Graphify memory: Streamlit dashboard startup` (+120 more)
  These have ≤1 connection - possible missing edges or undocumented components.
- **24 thin communities (<3 nodes) omitted from report** — run `graphify query` to explore isolated nodes.

## Suggested Questions
_Questions this graph is uniquely positioned to answer:_

- **Why does `SocialCrawler` connect `Alur Akuisisi Sosial Terpadu` to `Crawler Selenium Terisolasi`, `Akuisisi Instagram Terintegrasi`, `Alur Akuisisi Sosial Terpadu`, `Akuisisi Reddit Reddrix`, `Akuisisi Reddit Reddrix`, `Alur Akuisisi Sosial Terpadu`, `Akses dan Parsing HTML`, `Topik dan Verifikasi NLP`, `Snapshot NLP dan Arsip`, `Snapshot NLP dan Arsip`, `Akuisisi Instagram Terintegrasi`, `Konfigurasi SocialCrawler`, `Arsitektur Crawler dan Dependensi`, `Akuisisi Reddit Reddrix`, `Akuisisi Instagram Terintegrasi`, `Konfigurasi SocialCrawler`, `Akuisisi Instagram Terintegrasi`, `Akuisisi Instagram Terintegrasi`, `Alur Akuisisi Sosial Terpadu`, `Operasi dan Verifikasi BeeSense`, `Alur Akuisisi Sosial Terpadu`, `Akuisisi Reddit Reddrix`, `Alur Akuisisi Sosial Terpadu`, `Snapshot NLP dan Arsip`?**
  _High betweenness centrality (0.231) - this node is a cross-community bridge._
- **Why does `SocialNLPClusterer` connect `Pipeline dan Persistensi NLP` to `Eksplorasi Dashboard Streamlit`, `Ringkasan Topik Gemini`, `Pipeline dan Persistensi NLP`, `Eksplorasi Dashboard Streamlit`, `Ringkasan Topik Gemini`, `Snapshot NLP dan Arsip`, `Eksplorasi Dashboard Streamlit`, `Snapshot NLP dan Arsip`, `Pengujian Penjelasan Topik`, `Coherence dan Quality Gate`, `Pipeline dan Persistensi NLP`, `Snapshot NLP dan Arsip`, `Ringkasan Topik Gemini`, `Pengujian UI Streamlit`, `Runbook dan Verifikasi Lokal`, `Coherence dan Quality Gate`, `Akuisisi Instagram Terintegrasi`, `Coherence dan Quality Gate`, `Pipeline dan Persistensi NLP`, `Eksplorasi Dashboard Streamlit`, `Pipeline dan Persistensi NLP`, `Snapshot NLP dan Arsip`?**
  _High betweenness centrality (0.149) - this node is a cross-community bridge._
- **Why does `BeeSense Obsidian architecture and dataset index` connect `Snapshot NLP dan Arsip` to `Snapshot NLP dan Arsip`, `PRD Workspace Crawler`, `Snapshot NLP dan Arsip`, `Akuisisi Reddit Reddrix`, `Eksplorasi Dashboard Streamlit`, `Arsitektur Crawler dan Dependensi`, `Topik dan Verifikasi NLP`, `Akuisisi Instagram Terintegrasi`, `Akuisisi Instagram Terintegrasi`?**
  _High betweenness centrality (0.077) - this node is a cross-community bridge._
- **Are the 23 inferred relationships involving `SocialCrawler` (e.g. with `RedditCrawler` and `_SeleniumSource`) actually correct?**
  _`SocialCrawler` has 23 INFERRED edges - model-reasoned connections that need verification._
- **Are the 15 inferred relationships involving `SocialNLPClusterer` (e.g. with `SocialNLPStreamlitApp` and `Historical29October bounded15-candidate grid; shared budget retained`) actually correct?**
  _`SocialNLPClusterer` has 15 INFERRED edges - model-reasoned connections that need verification._
- **Are the 4 inferred relationships involving `SocialNLPStreamlitApp` (e.g. with `Cloud AppTest regression opens all five views/T04 without installed or imported training libraries` and `Platform and top-five source graphs count unique topic comments`) actually correct?**
  _`SocialNLPStreamlitApp` has 4 INFERRED edges - model-reasoned connections that need verification._
- **Are the 47 inferred relationships involving `ValueError` (e.g. with `browser_configuration()` and `collect_reddrix()`) actually correct?**
  _`ValueError` has 47 INFERRED edges - model-reasoned connections that need verification._
## Current delivery evidence

SocialCrawler 1.5 integrates InstagramCrawler through the shared export contract. Instagram-only crawling was stopped by the user after HTTP 429. The latest nonempty partial run yielded 248 posts and 2,128 comments; 1,000 posts/3 hours were not achieved. The recovery run verified HTTP 429 with a 360-second cooldown and was interrupted before its first retry; no crawler is running.

The final acquisition-window merge (27–30 October) contains 33,034 unique records: 1,859 roots and 31,175 comments/replies. Native-ID checks find zero duplicates; 49,952 repeated observations were removed and audited. Instagram totals are 324 posts and 3,038 comments including earlier trials.

The fitted model has exactly 20 topics, macro coherence c_v 0.4315219014, coverage 94.67%, silhouette cosine -0.057864 and two-seed ARI 0.820417. Eight individual topics remain below c_v 0.4; the gate applies to the macro mean. These are in-sample metrics, not labeled accuracy. Core training is unchanged by narrative revisions.

Gemini receives the 10 highest weighted c-TF-IDF keywords plus up to 10 fitted sentences per topic ranked by centroid cosine similarity, stable sentence-ID ties. Prompt beesense-topic-id:2 asks for natural connected Indonesian sentences and descriptions, avoids forced keyword lists, treats source instructions as data, and limits claims to supplied evidence. CSV extension gemini-topic-narratives:2 binds sentence text/IDs/scores to Parquet as well as source/prompt/keyword provenance. Legacy keyword-only version 1 remains readable. Per-topic receipts prevent replay unless context, prompt or source changes. API credentials remain ignored and absent from artifacts.

Dashboard exposes the narratives, downloadable CSV, weighted keywords and the exact representative sentences sent to Gemini. All three platforms remain filterable; reruns neither train nor call Gemini. Nine focused narrative tests pass, including ranking/isolation, context cache invalidation, legacy compatibility, tamper rejection, bounded retries and UI evidence. Prior baseline verification passed 83 NLP/dashboard tests, Cloud runtime 1 test and 117 crawler tests (one optional skip); refreshed release results are recorded in the current status. Docker daemon is unavailable, so image build/startup is unverified. No migration required.

The active configuration points at the verified model. The user authorized GitHub push/Streamlit deployment after context-grounded CSV validation; the current status below records what has actually finished. The DataDwip-inspired acquisition pacing follow-up is ordered after deployment and is not a guarantee of zero HTTP 429.

Current pipeline status:

```json
{
  "phase": "RELEASE_VALIDATED_AWAITING_GRAPH",
  "at": "2026-10-30T08:39:59.782766+00:00",
  "pid": 56718,
  "crawl": {
    "enabled": true,
    "min_posts": 870,
    "min_comments_per_post": 10,
    "posts_attempted": 1,
    "posts_exported": 0,
    "qualified_posts": 0,
    "comments": 0,
    "replies": 0,
    "filtered_roots": {
      "root_not_verified": 1
    },
    "insufficient_comment_posts": 0,
    "invalid_rows": 0,
    "target_met": false,
    "stop_reason": "INTERRUPTED",
    "rate_limit_events": 1,
    "rate_limit_retries": 0,
    "existing_posts_skipped": 0,
    "duplicate_posts_skipped": 0,
    "last_rate_limited_at": "2026-10-30T07:47:19.383831+00:00",
    "rate_limit_cooldown_seconds": 360,
    "rate_limit_cooldown_until": "2026-10-30T07:53:19.383831+00:00",
    "posts_shortfall": 870
  },
  "merged_rows": 33034,
  "duplicates_removed": 49952,
  "topics": 20,
  "coherence_cv": 0.4315219013547426,
  "input_file": "outputs/social_20261030_combined_3days_02/social_data.xlsx",
  "output_dir": "outputs/nlp_20261030_instagram_topics20_02",
  "oversized_artifacts": [],
  "gemini_topics": 20,
  "gemini_model": "gemini-3.5-flash-lite",
  "active_config_changed": true,
  "git_pushed": false,
  "deployment_held_by_user": false,
  "gemini_prompt_version": "beesense-topic-id:2",
  "gemini_extension": "gemini-topic-narratives:2",
  "gemini_sentences_per_topic": 10,
  "nlp_tests_passed": 85,
  "narrative_tests_passed": 9,
  "model_core_unchanged": true,
  "cloud_runtime_tests_passed": 1,
  "data_verifier": "PASS",
  "native_duplicate_records": 0,
  "docker_verified": false,
  "docker_reason": "daemon unavailable"
}
```

## Extraction integrity and cost

Raw changed-fragment diagnostics: {"dangling_endpoint_edges": 313, "directed_same_endpoint_collapsed_edges": 5, "undirected_same_endpoint_collapsed_edges": 7}. Exported endpoints and hyperedge memberships all validate. External/other-file AST references may be outside the changed fragment; endpoint-pair relation collapse can occur in an undirected graph. These are extraction limitations, not verified application failures. Semantic token accounting is unavailable; cost.json records null, never a measured zero. This map describes the working tree above the listed baseline commit.
