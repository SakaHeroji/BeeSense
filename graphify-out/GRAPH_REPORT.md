# Graph Report - /Users/socs3/Documents/BeeSense  (2026-11-02)

## Corpus Check
- 27 files · ~48,458 words
- Verdict: corpus is large enough that graph structure adds value.

## Summary
- 1945 nodes · 4071 edges · 130 communities (96 shown, 34 thin omitted)
- Extraction: 93% EXTRACTED · 7% INFERRED · 0% AMBIGUOUS · INFERRED: 279 edges (avg confidence: 0.71)
- Token cost: AST 0 LLM tokens; semantic usage unavailable (not a measured zero).

## Graph Freshness
- Built from commit: `c8f5e257`
- Run `git rev-parse HEAD` and compare to check if the graph is stale.
- Run `graphify update .` after code changes (no API cost).

## Community Hubs (Navigation)
- Akuisisi YouTube
- Crawler Selenium
- Worker Instaloader
- Riwayat Sesi Instagram
- Penggabungan Dataset
- Pengujian Client Instagram
- Konteks dan Provenance Gemini
- Pengujian Koordinator Crawler
- Kontrak Record Reddit
- Validasi Konfigurasi Frontend
- Penjadwalan dan Riwayat Akuisisi
- Worker Reddrix
- Alur Dataset Model Dashboard
- Eksekusi dan Ekspor Crawler
- Form Akuisisi dan Survei
- Model dan Pengujian NLP
- Panduan Pipeline BeeSense
- Integrasi X dan Provenans Akuisisi
- Monitor Job dan Dataset
- Koordinator Backend Sosial
- Parsing Identitas Reddit
- Konfigurasi TypeScript
- Pengujian Worker Instaloader
- Batas Akuisisi Reddit
- Encoding dan Penyimpanan Model
- Struktur DOM Reddit
- Pengujian Parser Reddit
- Tipe dan Client API
- Penjelasan Topik Dashboard
- Kontrak API Frontend
- thread_url
- Encoding dan Penyimpanan Model
- Persyaratan Produk Crawler
- Integrasi Default Instaloader
- Dependency Pengembangan Frontend
- app.py
- Pengambilan HTML Reddit
- Capture Reddit Playwright
- Render Dashboard Streamlit
- Pengujian Narasi Gemini
- Panduan Pipeline BeeSense
- Pengambilan HTML Reddit
- Wrapper RedditCrawler
- Pengujian Penjelasan Topik
- Pengambilan HTML Reddit
- Pengambilan HTML Reddit
- Batas Integrasi Produksi
- Dependency Runtime Frontend
- Pengujian Resume Capture
- Panduan Pipeline BeeSense
- Validasi Record Reddit
- Integrasi X dan Provenans Akuisisi
- Interface Layanan Frontend
- Operasi dan Verifikasi BeeSense
- Pengujian UI Streamlit
- Integrasi X dan Provenans Akuisisi
- Panduan Pipeline BeeSense
- Operasi dan Verifikasi BeeSense
- topic_sentence_export.py
- Kampanye Browser Reddit
- Integrasi X dan Provenans Akuisisi
- Integrasi X dan Provenans Akuisisi
- Runtime Docker dan Display
- Integrasi X dan Provenans Akuisisi
- InstaloaderCrawler
- Pengujian Analisis Dashboard
- Skrip Build Frontend
- Rencana Produk dan Survei
- Runtime Docker dan Display
- Integrasi X dan Provenans Akuisisi
- Konfigurasi Trial Reddit
- Validasi Record Reddit
- Pengambilan HTML Reddit
- Bukti Ekstraktif Topik
- build_topic_sentences.mjs
- Integrasi X dan Provenans Akuisisi
- Kontrak Record Reddit
- Router dan Batas Error
- Operasi dan Verifikasi BeeSense
- Operasi dan Verifikasi BeeSense
- Bukti Ekstraktif Topik
- Integrasi X dan Provenans Akuisisi
- Metadata Package Frontend
- .topic_figure
- Operasi dan Verifikasi BeeSense
- Operasi dan Verifikasi BeeSense
- Integrasi X dan Provenans Akuisisi
- Integrasi X dan Provenans Akuisisi
- Integrasi X dan Provenans Akuisisi
- Pengujian Alur Frontend
- Q: ok sekarang training ulang menggunakan /Users/sakaheroji/Documents/BeeSense/outputs/social_20261030_combined_instagram_500_2h_02/social_data.xlsx, clustering. Buat 20 topik dengan coherence minimal 0.4. Lalu buat excel baru dengan tabel dengan kolom: topik, kalimat yang berada dalam cluster topik. lalu model digunakan kembali di dashboard streamlit yang di rebuild ulang, dan di commit dan dipush semuanya ke githubnya untuk di deploy ulang
- Parser Public Post
- Format Kode Frontend
- Rencana Layanan Backend
- Model dan Pengujian NLP
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
- Integrasi X dan Provenans Akuisisi
- Model dan Pengujian NLP
- Panduan Pipeline BeeSense
- Memori Startup Dashboard
- Arsitektur Model dan Dashboard
- BeeSense project
- Panduan Pipeline BeeSense
- Integrasi X dan Provenans Akuisisi
- Integrasi X dan Provenans Akuisisi
- Dependency Backend Instagrapi
- Integrasi Default Instaloader
- Akuisisi X dan Ekspor Scweet

## God Nodes (most connected - your core abstractions)
1. `SocialCrawler` - 97 edges
2. `SocialNLPClusterer` - 91 edges
3. `SocialNLPStreamlitApp` - 57 edges
4. `SocialCrawlerTests` - 42 edges
5. `InstagramCrawlerTests` - 33 edges
6. `file_hash()` - 30 edges
7. `Reddrix-backed RedditCrawler runbook` - 29 edges
8. `NLPTests` - 29 edges
9. `Runbook and historical record for finalized partial crawler campaign` - 27 edges
10. `TwitterCrawlerTests` - 26 edges

## Surprising Connections (you probably didn't know these)
- `Relocated Selenium image preserves included requirements and package modules` --references--> `SocialCrawlerSelenium`  [INFERRED]
  deployment/docker/Dockerfile.selenium → Crawler/Backend/social_crawler_selenium.py
- `CLI/class display overrides and explicit virtual preconditions` --references--> `RedditCrawler`  [EXTRACTED]
  docs/crawler/REDDIT_CRAWLER.md → Crawler/Backend/reddit_crawler.py
- `Three unchanged SocialCrawler methods moved to SocialExportMixin` --references--> `SocialExportMixin`  [EXTRACTED]
  docs/crawler/INSTAGRAM_CRAWLER.md → Crawler/Backend/social_export.py
- `SocialExportMixin` --references--> `SocialExportMixin`  [EXTRACTED]
  docs/PROJECT_STRUCTURE.md → Crawler/Backend/social_export.py
- `Offline tests/context checks do not establish live Instagram trial success` --references--> `InstagramCrawlerTests`  [INFERRED]
  docs/crawler/INSTAGRAM_CRAWLER.md → tests/crawler/test_instagram_crawler.py

## Import Cycles
- None detected.

## Hyperedges (group relationships)
- **Persistent session access lifecycle** — docs_crawler_twitter_crawler_persistent_scweet_worker, docs_crawler_twitter_crawler_persistent_account_state, docs_crawler_twitter_crawler_pool_cooldown_wait, docs_crawler_twitter_crawler_terminal_access_barriers, docs_crawler_twitter_crawler_network_pacing_and_root_cache [EXTRACTED 1.00]
- **Integrated Twitter acquisition** — docs_crawler_social_crawler_socialcrawler, docs_crawler_twitter_crawler_twittercoordinatorworker, docs_crawler_twitter_crawler_persistent_scweet_worker, docs_crawler_twitter_crawler_native_x_identity, docs_crawler_twitter_crawler_beesense_audit_bundle [EXTRACTED 1.00]
- **Semantic clustering pipeline** — docs_machine_learning_social_nlp_multilingual_sbert_encoder, docs_machine_learning_social_nlp_umap_projection, docs_machine_learning_social_nlp_dbscan_clustering, docs_machine_learning_social_nlp_weighted_ward_topic_reduction, docs_machine_learning_social_nlp_c_tf_idf_topic_labels, docs_machine_learning_social_nlp_versioned_model_artifact_contract [EXTRACTED 1.00]
- **Dated historical NLP evidence** — docs_machine_learning_social_nlp_social_nlp_methodology, docs_machine_learning_social_nlp_nlp_snapshot_29_october_2026, docs_machine_learning_social_nlp_nlp_snapshot_30_october_2026_earlier_session, docs_machine_learning_social_nlp_nlp_snapshot_30_october_2026_instagram_500 [EXTRACTED 1.00]
- **End to end verified social pipeline** — readme_socialcrawler, docs_crawler_twitter_acquisition_20261102_combined_social_workbook_20261102, docs_machine_learning_twitter_retrain_20261102_socialnlpclusterer, docs_machine_learning_twitter_retrain_20261102_twitter_model_artifact_manifest, graphify_out_obsidian_arsitektur_beesense_socialnlpstreamlitapp [EXTRACTED 1.00]
- **Semantic clustering and evaluation flow** — docs_machine_learning_twitter_retrain_20261102_multilingual_sbert, docs_machine_learning_twitter_retrain_20261102_dual_seed_umap, docs_machine_learning_twitter_retrain_20261102_dbscan, docs_machine_learning_twitter_retrain_20261102_sentence_weighted_ward_reduction, graphify_out_obsidian_metodologi_machine_learning_social_nlp_coherence_c_v_evaluation_protocol, graphify_out_obsidian_metodologi_machine_learning_social_nlp_candidate_scoring_and_selection [EXTRACTED 1.00]
- **Preserved historical dataset lineage** — graphify_out_obsidian_dataset_dashboard_original_baseline_preservation, graphify_out_obsidian_dataset_dashboard_historical_merged_snapshot_29_october_2026, graphify_out_obsidian_dataset_dashboard_historical_earlier_snapshot_30_october_2026, graphify_out_obsidian_dataset_dashboard_historical_instagram_500_snapshot_30_october_2026, readme_historical_dataset_and_model_archives [EXTRACTED 1.00]
- **Crawler product specification and acceptance** — prd_prd_frontend_prd_frontend_crawler_crawler_product_requirements, prd_prd_frontend_rancangan_layar_crawler_crawler_screen_design, prd_prd_frontend_acceptance_criteria_crawler_crawler_acceptance_criteria [EXTRACTED 1.00]
- **Shared social export contract across crawler backends** — docs_crawler_instagram_crawler_shared_social_export_contract, docs_crawler_instaloader_crawler_instaloader_crawler, docs_crawler_reddit_crawler_reddrix_reddit_crawler, docs_crawler_instagram_crawler_persistent_chrome_worker [EXTRACTED 1.00]
- **Supported Monthly Topic Direction** — docs_machine_learning_explainable_topics_supported_descriptive_trends, docs_machine_learning_explainable_topics_theil_sen, docs_machine_learning_explainable_topics_kendall_tau_b [EXTRACTED 1.00]
- **Verified standalone trial06 GraphQL and comment path** — docs_crawler_instaloader_crawler_runtime_graphql_patch, docs_crawler_instaloader_crawler_same_context_tokens, docs_crawler_instaloader_crawler_persistent_worker_deadline, docs_crawler_instaloader_crawler_legacy_comment_nodeiterator, docs_crawler_instaloader_crawler_trial06_verified_outcome [EXTRACTED 1.00]
- **Stoppedacquisition→auditedfinalcorpus→verified20topics→contextualGeminiCSV** — docs_crawler_instagram_pipeline_20261030_acquisition_user_stop, docs_crawler_instagram_pipeline_20261030_final_native_identity_corpus, docs_crawler_instagram_pipeline_20261030_final_verified_model, docs_crawler_instagram_pipeline_20261030_actual_contextual_gemini_csv [EXTRACTED 1.00]
- **Topicweights,fittedcontext,receiptandCSV2bindoneversionednarrative** — docs_machine_learning_gemini_topic_narratives_weighted_keyword_input, docs_machine_learning_gemini_topic_narratives_fitted_sentence_context_selection, docs_machine_learning_gemini_topic_narratives_receipt_resume_binding, docs_machine_learning_gemini_topic_narratives_extension_validation [EXTRACTED 1.00]
- **VerifiedmodelandCSVsupportread-onlythree-platformDashboard** — docs_dashboard_dashboard_design_verified_model_20261030, docs_dashboard_dashboard_design_three_platform_support, docs_dashboard_dashboard_design_gemini_read_only_narratives [EXTRACTED 1.00]
- **Verified synthetic React delivery remains separate from proposed production worker/API acceptance** — crawler_frontend_readme_react_crawler_implementation, crawler_frontend_docs_delivery_verified_frontend_checks, crawler_frontend_docs_delivery_synthetic_demo_limitations, crawler_frontend_docs_api_contract_expected_api_contract, prd_prd_backend_readme_persistent_acquisition_worker, prd_prd_frontend_acceptance_criteria_crawler_production_acceptance_gates [INFERRED 0.95]

## Communities (130 total, 34 thin omitted)

### Community 0 - "Akuisisi YouTube"
Cohesion: 0.07
Nodes (50): error_code(), load_settings(), main(), parser(), run(), SafeLogger, Settings, video_url() (+42 more)

### Community 1 - "Crawler Selenium"
Cohesion: 0.07
Nodes (19): _barrier(), _create_driver(), main(), Content quoting an error is never used to classify an access barrier., Convert the shared rendered DOM capture without inventing identities., One browser operation. The parent enforces the hard process deadline., Stream evidence before completion; the original supervisor can retain it., Drop-in SocialCrawler with Selenium for both platforms and shared exports. (+11 more)

### Community 2 - "Worker Instaloader"
Cohesion: 0.06
Nodes (37): apply_browser_patch(), browser_graphql_query(), _check(), _cookie(), _hints(), _load_tokens(), main(), _pace() (+29 more)

### Community 3 - "Riwayat Sesi Instagram"
Cohesion: 0.07
Nodes (47): Standalone browser1800-second preset, updated bounded retry, Local session path and explicit360-second/3-retry policy, Instagram-only configured1800-second acquisition budget, instagramDocumentPayload(), instagramNavigate(), instagramRetryAfter(), instagramSourceRateLimit(), Bounded hashtag discovery with authoritative local root filters (+39 more)

### Community 4 - "Penggabungan Dataset"
Cohesion: 0.08
Nodes (17): checksum(), native(), Resolve X conversation roots from audited native IDs, never caption similarity., Read a workbook-bound sidecar, or the original hash-verified crawl audit., twitter_roots(), write_roots(), identity(), main() (+9 more)

### Community 5 - "Pengujian Client Instagram"
Cohesion: 0.07
Nodes (7): Clock, FakeClient, InstagramCrawlerTests, Offline contract/deadline tests; fixture data is always marked synthetic., records(), spawn_fixture(), spawn_hanging()

### Community 6 - "Konteks dan Provenance Gemini"
Cohesion: 0.07
Nodes (41): Active artifacts outputs/nlp_20261030_instagram_topics20_02, Configured33034-record final merged workbook, Active20-topic Instagram-inclusive model configuration, Configured c_v threshold 0.4 with topn 10 and window 110, Current active Gemini enabled; historical disabled state retained, Final Instagram-inclusive20-topic/Gemini configuration, Verified model configuration enables contextual Gemini CSV, Active20-topic Instagram-inclusive model configuration (+33 more)

### Community 7 - "Pengujian Koordinator Crawler"
Cohesion: 0.15
Nodes (6): Exercise Instagram through the combined coordinator, without network access., rd_events(), receipt(), SocialCrawlerTests, spawn_youtube_fixture(), yt_events()

### Community 8 - "Kontrak Record Reddit"
Cohesion: 0.13
Nodes (17): add_readme(), ContentInput, ContractTests, Dataset, digest(), dumps(), main(), parser() (+9 more)

### Community 9 - "Validasi Konfigurasi Frontend"
Cohesion: 0.10
Nodes (32): ConfigReview(), advance(), cap, committed, dataset(), get(), load(), plans (+24 more)

### Community 10 - "Penjadwalan dan Riwayat Akuisisi"
Cohesion: 0.09
Nodes (36): Per-platform bounds: max_posts 4000, max_candidates 6000, Main root reddrix.display_mode=auto, Historical exclusion source outputs/social_20261028_01, Configured global acquisition budget 10800 seconds, Retained Playwright-only CAPTCHA fields:600-second wait and five-second poll, Configured Reddit policy cooldown:360seconds, Configured Reddit retry cap:threeperrun, Current main configuration: platforms.reddit.enabled=true (+28 more)

### Community 11 - "Worker Reddrix"
Cohesion: 0.10
Nodes (22): collect_reddrix(), _config(), _keywords(), normalize_reddrix_item(), _number(), Map Reddrix 1.2.14 dictionaries without inventing identity or dates., Reddrix anti-bot exceptions do not expose an authoritative HTTP status., Virtual displays require Linux and Xvfb; other environments use headless. (+14 more)

### Community 12 - "Alur Dataset Model Dashboard"
Cohesion: 0.07
Nodes (35): Dashboard Python 3.12 and 3.14 runtime matrix, Offline crawler and NLP regression tests, Verify BeeSense CI, Synthetic Reddit post, comment and reply fixture, Reddit browser campaign helpers, User checkpoint audit export and verification, Manual CAPTCHA recovery within global deadline, Reddit Playwright runner (+27 more)

### Community 13 - "Eksekusi dan Ekspor Crawler"
Cohesion: 0.08
Nodes (12): main(), SocialExportMixin, Validate and return the effective plan without browser/network access., Re-export saved Contents without network or modifying the source bundle., Describe the acquisition backend independently of the shared export., Return an explicit target/shortfall report and write one atomic bundle., Compose platform workers with one configuration, scheduler and export bundle., Read roots and all global X IDs; never alter historical workbooks. (+4 more)

### Community 14 - "Form Akuisisi dan Survei"
Cohesion: 0.12
Nodes (27): Automatic(), Baselines(), ConfigFields(), Manual(), ManualUrl(), labels, sample, Survey() (+19 more)

### Community 15 - "Model dan Pengujian NLP"
Cohesion: 0.13
Nodes (6): Encode with SBERT, fit UMAP + DBSCAN and optionally merge to a topic count., SocialNLPClusterer, DashboardTests, encoder(), fixture(), NLPTests

### Community 16 - "Panduan Pipeline BeeSense"
Cohesion: 0.07
Nodes (30): Advanced connected-browser Reddit campaign helpers, Checkpoint export to the eight-sheet contract, Native-ID provenance and bounded public excerpts, Standalone runner stops 429; coordinator 1.3 supports bounded cooldown, Isolated Chrome profile, manual CAPTCHA wait and access-barrier stops, Coordinator waits for manual CAPTCHA without automated clicks, Shared rendered_thread_dom.mjs extraction, Reddit Playwright CLI runner (+22 more)

### Community 17 - "Integrasi X dan Provenans Akuisisi"
Cohesion: 0.08
Nodes (5): hanging_worker(), persistent_worker(), Offline contracts for Twitter/X acquisition; no live credentials required., tweet(), TwitterCrawlerTests

### Community 18 - "Monitor Job dan Dataset"
Cohesion: 0.20
Nodes (24): Shell(), DatasetView(), History(), Composition(), JobDetail(), liveStates, PlatformCard(), ProgressChart() (+16 more)

### Community 19 - "Koordinator Backend Sosial"
Cohesion: 0.11
Nodes (5): InstaloaderSettings, InstaloaderWorker, One subprocess and rate controller, with killable per-operation deadlines., Clock, InstagramIntegrationTests

### Community 20 - "Parsing Identitas Reddit"
Cohesion: 0.13
Nodes (18): bounded_events(), HtmlPage, HtmlSource, LocalHtmlSource, now_iso(), PublicHtmlSource, ABC, Normalize a source event; write only through the shared Dataset/Sink. (+10 more)

### Community 21 - "Konfigurasi TypeScript"
Cohesion: 0.07
Nodes (26): compilerOptions, allowImportingTsExtensions, esModuleInterop, isolatedModules, jsx, lib, module, moduleResolution (+18 more)

### Community 22 - "Pengujian Worker Instaloader"
Cohesion: 0.13
Nodes (5): fixture_post(), hanging_fixture(), InstaloaderCrawlerTests, persistent_fixture(), Offline contracts for the separate Instaloader experiment.

### Community 23 - "Batas Akuisisi Reddit"
Cohesion: 0.10
Nodes (26): Configured 360-second policy and three HTTP 429 retries, Configured new sorting differs from Reddrix capability, Relocated Selenium image preserves included requirements and package modules, Installed Reddrix 1.2.14 and Camoufox 156 browser evidence, Preserved compact SocialCrawler workbook, Hard-deadline subprocess retains streamed records, BeeSense interoperation delay differs from library request retries, Isolated local environment and separately downloaded browser (+18 more)

### Community 24 - "Encoding dan Penyimpanan Model"
Cohesion: 0.12
Nodes (7): Use the same class TF-IDF vocabulary for selection and publication., Macro c_v on ALL non-noise topics and a fixed full-corpus reference.          Un, Derive Indonesian Gemini labels after topic count and coherence pass., Reuse immutable SBERT features only after verifying data/model identity., Preserve explicit zero distances, including identical sentence vectors., Merge entire DBSCAN groups using sentence-weighted Ward linkage.          Minimi, Select DBSCAN parameters on UMAP; evaluate in original SBERT geometry.

### Community 25 - "Struktur DOM Reddit"
Cohesion: 0.12
Nodes (13): assert_accessible(), BoundedDom, content_node(), MemorySink, Node, Small serialised-DOM reader, not a browser or full HTML5 repair engine., rendered_text(), RestrictedRedirect (+5 more)

### Community 26 - "Pengujian Parser Reddit"
Cohesion: 0.22
Nodes (7): first(), fixture_page(), native_fullname(), object_key(), RedditHtmlParser, RedditTests, source_time()

### Community 27 - "Tipe dan Client API"
Cohesion: 0.10
Nodes (20): ApiError, base, httpApi, post(), request(), Baseline, Config, Counts (+12 more)

### Community 28 - "Penjelasan Topik Dashboard"
Cohesion: 0.12
Nodes (23): Count evidence in the filter, keeping sentences/comments/parents distinct., Filters retain model membership and do not recompute c_v, Selected-topic c_v card is separate from the full-model mean, Historical combined snapshot QA; relocated root shim checked offline, Occurrences, unique sentences, comments and source roots have different denominators, Five artifact-backed Streamlit analysis views, Historical combined20 UI/runtime verification retained after relocation, Internal model metrics do not establish accuracy or representativeness (+15 more)

### Community 29 - "Kontrak API Frontend"
Cohesion: 0.10
Nodes (24): Server history pagination, SSE, templates and organizational login remain future, Project-prefixed cookie-session API requires server CORS/CSRF/access controls, Expected typed frontend API contract; backend implementation pending, locatorKey is normalized permalink identity;nativeId may await backend verification, Increasing snapshotVersion and server-owned actions drive reconciliation, Safe structured errors distinguish API429 from worker-platform429, Survey commit binds review to session/project and revalidates conflicts, Typed plan/job requests bind plan IDs, idempotency and safe stop (+16 more)

### Community 30 - "thread_url"
Cohesion: 0.12
Nodes (6): Read-only exploration of completed NLP runs; no training on page reruns., SocialNLPStreamlitApp, DashboardreadsverifiedCSVwithnoAPIortrainingonrerun, Active20-topic/c_v0.4315 artifact andGemini display contract, Historical 28 October 2026 coherence retrain: 52 topics, c_v 0.40970330118194137, Historical fixed top10/window110/all15878-unique macro c_v protocol

### Community 31 - "Encoding dan Penyimpanan Model"
Cohesion: 0.13
Nodes (13): file_hash(), main(), Explain already verified artifacts without encoding or fitting again., Publish a new versioned sidecar; never modify the original run., main(), published_crawl_files(), published_source_files(), Verify published source workbooks and the dashboard artifact bundle. (+5 more)

### Community 32 - "Persyaratan Produk Crawler"
Cohesion: 0.18
Nodes (23): Atomic survey review and idempotent commit, Expected Crawler API contract, NLP schema eligibility gate, Seven-platform capability gating, Server-owned acquisition job lifecycle, Crawler frontend delivery and UX audit, Frontend verification evidence: 50 tests and container checks, BeeSense Crawler React frontend (+15 more)

### Community 33 - "Integrasi Default Instaloader"
Cohesion: 0.20
Nodes (22): Diagnostic and active-data separation, Diagnostic trial deduplication, Instaloader Docker artifact awaiting runtime verification, Standalone experiment caps, InstaloaderCrawler guide and evidence, Historical Instagram resume preset preserved, Historical trials 01–05, InstaloaderCrawler (+14 more)

### Community 34 - "Dependency Pengembangan Frontend"
Cohesion: 0.10
Nodes (21): devDependencies, eslint, @eslint/js, jsdom, prettier, @testing-library/user-event, @types/react, @types/react-dom (+13 more)

### Community 35 - "app.py"
Cohesion: 0.15
Nodes (14): Root Docker context allowlist for relocated dashboard runtime, _explain_filtered(), _load_artifacts(), main(), Streamlit entry point for local and Community Cloud dashboards.  Training lives, Dashboard build context includes root shim and artifact-reader packages, Relocated dashboard image uses root Streamlit shim and runtime-only wheels, Responsive cards, visible keyboard focus and chart/table alternatives verified (+6 more)

### Community 36 - "Pengambilan HTML Reddit"
Cohesion: 0.20
Nodes (18): create_client(), error_receipt(), instagram_worker(), load_client(), login_from_file(), login_local(), login_with_saved_password(), _manual_verification_required() (+10 more)

### Community 37 - "Capture Reddit Playwright"
Cohesion: 0.21
Nodes (12): atomic_json(), barrier_status(), campaign_plan(), find_cli(), PlaywrightCLI, rate_limit_seconds(), run(), save_capture() (+4 more)

### Community 39 - "Pengujian Narasi Gemini"
Cohesion: 0.18
Nodes (5): Nine Gemini offline tests and all20 actual contextual CSV rows validated, GeminiArtifactTests, GeminiTests, response(), topic()

### Community 40 - "Panduan Pipeline BeeSense"
Cohesion: 0.14
Nodes (20): Bounded radius graph, c-TF-IDF topic labels, Candidate quality gate, Coherence c_v protocol, DBSCAN clustering, Gemini topic narratives, Multilingual SBERT encoder, NLP snapshot 29 October 2026 (+12 more)

### Community 41 - "Pengambilan HTML Reddit"
Cohesion: 0.14
Nodes (7): InstagramCrawler, main(), Standalone trial. The production SocialCrawler backend stays unchanged., run_instagram_worker(), run_worker(), InstagramBrowserTests, Offline checks for the Chrome boundary, native identity, and provenance.

### Community 42 - "Wrapper RedditCrawler"
Cohesion: 0.17
Nodes (5): main(), Reddit-only compatibility entry point for the integrated SocialCrawler Reddrix b, Run only Reddit through the shared Reddrix implementation in SocialCrawler., RedditCrawler, RedditCrawlerTests

### Community 43 - "Pengujian Penjelasan Topik"
Cohesion: 0.25
Nodes (3): ExplanationTests, model_from_counts(), profile()

### Community 44 - "Pengambilan HTML Reddit"
Cohesion: 0.17
Nodes (9): browser_configuration(), browser_script(), InstagramBrowserWorker, Serial Chrome acquisition using a persistent profile and manual login.  The same, _configuration(), InstagramSettings, _integer(), decode_cli_output() (+1 more)

### Community 45 - "Pengambilan HTML Reddit"
Cohesion: 0.22
Nodes (11): collect(), InstagramAdapter, media_pk_from_url(), media_url(), native_pk(), normalize_item(), object_key(), Map explicit native IDs/timestamps; do not infer authors or text coverage. (+3 more)

### Community 46 - "Batas Integrasi Produksi"
Cohesion: 0.13
Nodes (17): Final style samples:96desktop/78narrow444px elements,all black and≥13 px, React frontend and simulation verified; production acquisition integration unavailable, Implemented UI flows:automatic/manual, monitor, survey and dataset review, Applied UX fixes:linked errors, step validation, deep links, drawer focus and inertness, Browser actual widths400/444px;requested360px remains unproven, Production release waits for API/worker/access/export and survey adapter integration, Late plan, URL and survey validation is ignored after input changes, Demo IDs, baseline data and downloads are synthetic rather than acquisition evidence (+9 more)

### Community 47 - "Dependency Runtime Frontend"
Cohesion: 0.12
Nodes (17): dependencies, @fontsource-variable/plus-jakarta-sans, lucide-react, papaparse, react, react-dom, react-router-dom, @tanstack/react-query (+9 more)

### Community 49 - "Panduan Pipeline BeeSense"
Cohesion: 0.17
Nodes (16): Baseline identity exclusion, Instaloader 4.16, Platform rate limit policies, Reddrix 1.2.14, Round robin deadline scheduler, Shared root and comment filters, Social campaign 29 October 2026, SocialCrawler (+8 more)

### Community 50 - "Validasi Record Reddit"
Cohesion: 0.19
Nodes (6): KeywordMatcher, Aho-Corasick; offsets refer to Python Unicode code points in source., RecordFactory, utc_datetime(), export_campaign(), load_campaign()

### Community 51 - "Integrasi X dan Provenans Akuisisi"
Cohesion: 0.24
Nodes (14): AccessBarrier, account_cooldown(), auth_material(), create_client(), error_receipt(), guarded_transport(), private_json(), Standalone Twitter/X acquisition with Scweet and BeeSense's Excel contract. (+6 more)

### Community 53 - "Operasi dan Verifikasi BeeSense"
Cohesion: 0.16
Nodes (15): BeeSense architecture note, Extracted evidence and inferred cosine edges, Dataset Dashboard note, Historical earlier snapshot 30 October 2026, Historical Instagram 500 snapshot 30 October 2026, Historical merged snapshot 29 October 2026, Original baseline preservation, BeeSense HOME (+7 more)

### Community 55 - "Integrasi X dan Provenans Akuisisi"
Cohesion: 0.20
Nodes (14): Social crawler guide, Credential and state isolation, Native parent preservation, Network pacing and root cache, Persistent account state, Persistent Scweet worker, Pool cooldown wait, Scweet 5.8.2 (+6 more)

### Community 56 - "Panduan Pipeline BeeSense"
Cohesion: 0.16
Nodes (14): Artifact Only Dashboard Runtime, 30 October Three Platform Model, BeeSense Dashboard Guide, Kendall Tau B Consistency, Maximal Marginal Relevance, Supported Descriptive Topic Trends, Theil Sen Monthly Slope, Explainable Topics Guide (+6 more)

### Community 57 - "Operasi dan Verifikasi BeeSense"
Cohesion: 0.18
Nodes (14): Package rooted path consistency, Dashboard URL state binding, SocialNLPStreamlitApp, Active four platform dataset, Active Twitter NLP snapshot, BeeSense README, Dashboard runtime CI, Dashboard runtime dependency separation (+6 more)

### Community 58 - "topic_sentence_export.py"
Cohesion: 0.26
Nodes (8): json_write(), export_payload(), main(), Prepare an original-sentence export and seal it into a new NLP snapshot., Keep original variants; remove repeated occurrences of the same text., Verify every Excel membership before publishing the complete snapshot., seal(), TopicSentenceExportTests

### Community 59 - "Kampanye Browser Reddit"
Cohesion: 0.27
Nodes (8): classifyCaptureFailure(), enrichBatch(), rateLimitSeconds(), inWindow(), mergeCandidates(), row, source, window

### Community 60 - "Integrasi X dan Provenans Akuisisi"
Cohesion: 0.19
Nodes (13): Comment sentence eligibility, DBSCAN, Dual seed UMAP, Internal evaluation interpretation limits, Sentence preparation provenance, Sentence weighted Ward reduction, SocialNLPClusterer, Verified Twitter twenty topic fit (+5 more)

### Community 61 - "Integrasi X dan Provenans Akuisisi"
Cohesion: 0.27
Nodes (7): main(), SocialExportMixin, Bounded newest-first date windows, shared by both entry points., Scweet-only trial; uses the existing shared sink, filters and Excel format., search_targets(), TwitterCrawler, upstream_version()

### Community 62 - "Runtime Docker dan Display"
Cohesion: 0.18
Nodes (12): Relocated combined crawler image runs package module as UID10001, Actual macOS lifecycle test versus mocked Linux display matrix, Reddrix Docker image unbuilt: local daemon unavailable, No database/model/persistent-contract migration, Reddrix trial preserves existing model and frontend boundaries, Current offline tests pass; actual Linux and reorganized Docker image unverified, Folder moves preserve data paths, artifact bytes and historical crawl results, Reorganized Docker image remains unbuilt while local daemon is unavailable (+4 more)

### Community 63 - "Integrasi X dan Provenans Akuisisi"
Cohesion: 0.29
Nodes (12): Combined social workbook 20261102, Global native X identity, Merged record lineage contract, native_roots.json, Twitter acquisition report 2 November 2026, Stored artifact Twitter dashboard, topic_sentences.xlsx, Twitter model artifact manifest (+4 more)

### Community 64 - "InstaloaderCrawler"
Cohesion: 0.23
Nodes (4): FakeReddrix, item(), Reddrix field/identity boundaries and the real, shared Excel exporter., records()

### Community 66 - "Skrip Build Frontend"
Cohesion: 0.18
Nodes (11): scripts, build, build:demo, check, dev, format, format:check, lint (+3 more)

### Community 67 - "Rencana Produk dan Survei"
Cohesion: 0.20
Nodes (11): Curated two-menu contract with URL/Survey under Manual, Curated immutable dataset selection does not train or change Dashboard, Curated Crawler PRD status:frontend implemented, backend pending, New survey schema must preserve role, question, response, version and permission, Crawler wireframes are illustrative design requirements, not app screenshots, Monitor prioritizes status, units, barriers and next actions over logs, Worker-session CAPTCHA and429 UI offer observation rather than bypass, Responsive drawer/table/focus behavior is a design target (+3 more)

### Community 68 - "Runtime Docker dan Display"
Cohesion: 0.24
Nodes (9): load_reddrix(), Configure initial and refreshed sessions inside an isolated worker module., Adaptive display v1.1.0 auto platform policy, CLI/class display overrides and explicit virtual preconditions, Requested/effective display mode is visible in plan and source metadata, Historical trial 01 ended PARTIAL with zero posts, Reddrix-only Camoufox factory controls initial and refreshed sessions, Historical v1.0.0 module-specific non-Linux Xvfb shim (+1 more)

### Community 69 - "Integrasi X dan Provenans Akuisisi"
Cohesion: 0.29
Nodes (10): Daily request cap overshoot, Deadline bounded pool cooldown, Deadline preserving checkpoint resume, Five batch BeeSense audit outputs, Observed Twitter HTTP telemetry, Scweet, Scweet rate limiting documentation, Twenty five query parity (+2 more)

### Community 70 - "Konfigurasi Trial Reddit"
Cohesion: 0.31
Nodes (9): Read-only historical baseline exclusion, Original date boundary and university-topic query scope, Tracked reddrix.display_mode=auto, Configured root/comment/candidate/time budgets, Trial config now explicitly selects Reddrix; wrapper preserves legacy compatibility, Tracked Reddit trial configuration, Original historical date window, keywords and read-only baseline, Thin Reddit-only wrapper selects shared Reddrix explicitly (+1 more)

### Community 71 - "Validasi Record Reddit"
Cohesion: 0.28
Nodes (5): load_settings(), parsed_number(), Settings, thread_url(), timeout_fixture()

### Community 72 - "Pengambilan HTML Reddit"
Cohesion: 0.28
Nodes (5): Shared root selection and formula-safe Excel projection for social crawlers., Project the full audit rows into one sheet, applying current filters., Requires config, include and exclude matchers; performs no acquisition., Return a local date for display; relative source dates stay estimates., SocialExportMixin

### Community 74 - "build_topic_sentences.mjs"
Cohesion: 0.22
Nodes (6): body, payload, [payloadPath, outputPath, previewDir], sentences, topics, workbook

### Community 75 - "Integrasi X dan Provenans Akuisisi"
Cohesion: 0.25
Nodes (8): Query pendidikan Indonesia jendela tujuh hari, Preset percobaan Twitter 30 menit, Jeda 5 dan 15 detik limiter window per operasi dan cap harian 120, 1.800 detik target 1.000 post 10 balasan, Allowlist Docker tanpa auth dan sesi, Image Twitter Python 3.12 UID 10001, openpyxl 3.1.5, Scweet 5.8.2

### Community 76 - "Kontrak Record Reddit"
Cohesion: 0.36
Nodes (3): BundleSink, Atomic new directory; streaming JSONL + streaming, formula-safe Excel., Preserved eight-sheet audit and checksummed full-text bundle

### Community 77 - "Router dan Batas Error"
Cohesion: 0.25
Nodes (3): client, ErrorBoundary, router

### Community 78 - "Operasi dan Verifikasi BeeSense"
Cohesion: 0.29
Nodes (8): beesense-topic-id:2, Gemini 3.5 Flash Lite, topic_narratives.csv, topic_narratives.py, Verified embedding cache, Narrative CSV schema compatibility, Narrative evidence validation, Narrative request receipt cache

### Community 79 - "Operasi dan Verifikasi BeeSense"
Cohesion: 0.29
Nodes (8): Multilingual SBERT, Twenty topic mean coherence publication gate, Candidate scoring and selection, Coherence c_v evaluation protocol, Gensim CoherenceModel reference, Historical baseline coherence snapshots, Overflow window sentence encoding, Social NLP methodology note

### Community 82 - "Metadata Package Frontend"
Cohesion: 0.29
Nodes (6): engines, node, name, private, type, version

### Community 83 - ".topic_figure"
Cohesion: 0.29
Nodes (4): _graph_positions(), Bounded topic graph: volume from filtered rows, semantic edges from the full mod, Count sentence occurrences; never confuse them with distinct comments., Keep the full-model layout stable while volume and edge filters change.

### Community 84 - "Operasi dan Verifikasi BeeSense"
Cohesion: 0.33
Nodes (7): TwitterCoordinatorWorker, Reddrix subprocess lifecycle, Shared deadline round robin scheduling, InstaloaderCrawler, RedditCrawler, SocialCrawler, TwitterCrawler

### Community 85 - "Operasi dan Verifikasi BeeSense"
Cohesion: 0.29
Nodes (7): BeeSense project structure, Ignored local authentication and browser state, Legacy Instagram browser isolation, Separate training and test environments, SocialExportMixin, Published artifact allowlist, verify_dashboard_data

### Community 87 - "Integrasi X dan Provenans Akuisisi"
Cohesion: 0.33
Nodes (6): 2 November 2026 pipeline integration, 31 October 2026 historical evidence, SocialNLPClusterer, thread_root_key, TwitterCrawler Scweet architecture, Workbook bound root sidecar

### Community 88 - "Integrasi X dan Provenans Akuisisi"
Cohesion: 0.70
Nodes (4): native_id(), normalize_item(), object_key(), Keep native parent IDs; never infer a reply parent from screen position.

### Community 89 - "Pengujian Alur Frontend"
Cohesion: 0.40
Nodes (3): AppContext, demoApi, UrlReview

### Community 90 - "Q: ok sekarang training ulang menggunakan /Users/sakaheroji/Documents/BeeSense/outputs/social_20261030_combined_instagram_500_2h_02/social_data.xlsx, clustering. Buat 20 topik dengan coherence minimal 0.4. Lalu buat excel baru dengan tabel dengan kolom: topik, kalimat yang berada dalam cluster topik. lalu model digunakan kembali di dashboard streamlit yang di rebuild ulang, dan di commit dan dipush semuanya ke githubnya untuk di deploy ulang"
Cohesion: 0.40
Nodes (4): Answer, Outcome, Q: ok sekarang training ulang menggunakan /Users/sakaheroji/Documents/BeeSense/outputs/social_20261030_combined_instagram_500_2h_02/social_data.xlsx, clustering. Buat 20 topik dengan coherence minimal 0.4. Lalu buat excel baru dengan tabel dengan kolom: topik, kalimat yang berada dalam cluster topik. lalu model digunakan kembali di dashboard streamlit yang di rebuild ulang, dan di commit dan dipush semuanya ke githubnya untuk di deploy ulang, Source Nodes

### Community 92 - "Format Kode Frontend"
Cohesion: 0.50
Nodes (3): printWidth, singleQuote, trailingComma

### Community 93 - "Rencana Layanan Backend"
Cohesion: 0.50
Nodes (4): Backend PRD is not written; API/worker services remain proposed, Proposed persistent Python worker and authorized CAPTCHA browser bridge, Proposed server session, role, project isolation and idempotency, Proposed survey transactions, immutable datasets and operational audit

### Community 95 - "CI Container Frontend"
Cohesion: 0.67
Nodes (3): SPA container health and deep-link checks, Crawler frontend CI, BeeSense Crawler SPA document

## Knowledge Gaps
- **201 isolated node(s):** `window`, `source`, `row`, `candidate`, `singleQuote` (+196 more)
  These have ≤1 connection - possible missing edges or undocumented components.
- **34 thin communities (<3 nodes) omitted from report** — run `graphify query` to explore isolated nodes.

## Suggested Questions
_Questions this graph is uniquely positioned to answer:_

- **Bagaimana data X digabung tanpa duplikasi, lalu divalidasi menjadi 20 topik dan deskripsi Gemini?**
  _Akuisisi, native root, penggabungan, gate coherence, CSV dan dashboard memiliki provenance yang terhubung._
- **Why does `SocialCrawler` connect `Eksekusi dan Ekspor Crawler` to `InstaloaderCrawler`, `Crawler Selenium`, `Pengujian Client Instagram`, `Pengujian Koordinator Crawler`, `Wrapper RedditCrawler`, `Worker Reddrix`, `Penjadwalan dan Riwayat Akuisisi`, `Panduan Pipeline BeeSense`, `Panduan Pipeline BeeSense`, `Integrasi X dan Provenans Akuisisi`, `Koordinator Backend Sosial`, `Parsing Identitas Reddit`, `Integrasi X dan Provenans Akuisisi`, `Batas Akuisisi Reddit`, `Runtime Docker dan Display`?**
  _High betweenness centrality (0.281) - this node is a cross-community bridge._
- **Why does `SocialNLPClusterer` connect `Model dan Pengujian NLP` to `app.py`, `Penggabungan Dataset`, `Konteks dan Provenance Gemini`, `Pengujian Narasi Gemini`, `Panduan Pipeline BeeSense`, `Bukti Ekstraktif Topik`, `Pengujian Penjelasan Topik`, `Bukti Ekstraktif Topik`, `Model dan Pengujian NLP`, `Pengujian UI Streamlit`, `Integrasi X dan Provenans Akuisisi`, `Runtime Docker dan Display`, `Encoding dan Penyimpanan Model`, `topic_sentence_export.py`, `Penjelasan Topik Dashboard`, `thread_url`, `Encoding dan Penyimpanan Model`?**
  _High betweenness centrality (0.128) - this node is a cross-community bridge._
- **Why does `Runbook and historical record for finalized partial crawler campaign` connect `Penjadwalan dan Riwayat Akuisisi` to `Alur Dataset Model Dashboard`, `Penjelasan Topik Dashboard`, `Eksekusi dan Ekspor Crawler`?**
  _High betweenness centrality (0.081) - this node is a cross-community bridge._
- **Are the 21 inferred relationships involving `SocialCrawler` (e.g. with `RedditCrawler` and `_SeleniumSource`) actually correct?**
  _`SocialCrawler` has 21 INFERRED edges - model-reasoned connections that need verification._
- **Are the 14 inferred relationships involving `SocialNLPClusterer` (e.g. with `SocialNLPStreamlitApp` and `CloudRuntimeTests`) actually correct?**
  _`SocialNLPClusterer` has 14 INFERRED edges - model-reasoned connections that need verification._
- **Are the 51 inferred relationships involving `ValueError` (e.g. with `browser_configuration()` and `instaloader_options()`) actually correct?**
  _`ValueError` has 51 INFERRED edges - model-reasoned connections that need verification._
- **Are the 3 inferred relationships involving `SocialNLPStreamlitApp` (e.g. with `Platform and top-five source graphs count unique topic comments` and `Term bars show bounded phrase presence in unique filtered sentences`) actually correct?**
  _`SocialNLPStreamlitApp` has 3 INFERRED edges - model-reasoned connections that need verification._
## Integrasi Twitter dan retraining — 2 November 2026

Scoped incremental extraction retains untouched graph sources. The listed commit is the baseline of this modified working tree. Auth, private SQLite, model arrays and acquired raw text are excluded from extraction. Curated Obsidian notes are explicit semantic inputs.

Three public JSON presets produced zero AST nodes in the preflight; they remain represented by explicit documented configuration concepts, not claimed as structurally extracted.

Verification: {"crawl": {"synthetic": false, "new_posts": 333, "new_comments": 187, "new_replies": 104, "duplicate_native_ids": 0, "unresolved_parent_references": 0, "cross_root_parent_edges": 0}, "dataset": {"rows": 34764, "roots": 2526, "comments": 32238, "duplicate_native_ids": 0}, "model": {"topics": 20, "macro_coherence": 0.4243209771786889, "individual_topics_below_threshold": 9, "coverage": 0.9308674928503337, "silhouette_cosine": -0.022359121590852737, "stability_ari": 0.7939739617939582, "gemini_topics": 20, "excel_sentence_rows": 48850}, "tests": {"twitter": "23 PASS", "social": "70 PASS,1 optional SKIP", "nlp": "95 PASS", "cloud": "1 PASS; five views with all platforms and Twitter-only; no training/Gemini runtime"}, "static_checks": "Ruff check/format,compileall,pip check PASS", "docker": "Final Moby 0.6.0 contexts exclude secrets; isolated final crawler dry-run and minimal dashboard imports PASS; image build/start/health UNVERIFIED because daemon unavailable", "database": "No migration required; additive X metadata in versioned artifact snapshots"}

Changed-fragment diagnostic warnings: {"dangling_endpoint_edges": 155, "directed_same_endpoint_collapsed_edges": 1, "undirected_same_endpoint_collapsed_edges": 1}. AST references outside the scoped fragment may be unresolved here; full exported edge endpoints and hyperedge membership are separately verified. These checks do not establish extraction completeness. Semantic token usage is unknown; numeric cumulative totals exclude unknown usage.
Stale cross-document hyperedges referencing replaced nodes were removed: [{"id": "artifact_model_dashboard_flow", "missing_replaced_nodes": ["readme_active_combined_dataset", "readme_artifact_only_dashboard"]}, {"id": "docs_machine_learning_gemini_topic_narratives_verified_publication", "missing_replaced_nodes": ["docs_machine_learning_social_nlp_artifact_contract_v2"]}]. Valid hyperedges were retained; no substitute membership was guessed.
