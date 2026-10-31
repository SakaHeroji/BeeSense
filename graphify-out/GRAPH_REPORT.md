# Graph Report - /Users/socs3/Documents/BeeSense  (2026-10-31)

## Corpus Check
- 8 files · ~5,830 words
- Verdict: corpus is large enough that graph structure adds value.

## Summary
- 1942 nodes · 4344 edges · 120 communities (100 shown, 20 thin omitted)
- Extraction: 91% EXTRACTED · 9% INFERRED · 0% AMBIGUOUS · INFERRED: 400 edges (avg confidence: 0.76)
- Token cost: AST 0 LLM tokens; semantic usage unavailable (not a measured zero).

## Graph Freshness
- Built from commit: `ea3b9d61`
- Run `git rev-parse HEAD` and compare to check if the graph is stale.
- Run `graphify update .` after code changes (no API cost).

## Community Hubs (Navigation)
- Pengambilan HTML Reddit
- Penjadwalan dan Riwayat Akuisisi
- Akuisisi X dan Ekspor Scweet
- Akuisisi YouTube
- Crawler Selenium
- Pengujian Client Instagram
- Worker Instaloader
- Pengujian Koordinator Crawler
- Penggabungan Dataset
- Model dan Pengujian NLP
- Validasi Konfigurasi Frontend
- Koordinator Backend Sosial
- Form Akuisisi dan Survei
- Riwayat Sesi Instagram
- Worker Reddrix
- Monitor Job dan Dataset
- Validasi Record Reddit
- Konfigurasi TypeScript
- Pengujian Worker Instaloader
- Tipe dan Client API
- Generator Narasi Gemini
- Kontrak API Frontend
- Akuisisi X dan Ekspor Scweet
- Batas Akuisisi Reddit
- Persyaratan Produk Crawler
- thread_url
- Integrasi Default Instaloader
- Pengujian Parser Reddit
- app.py
- Parsing Identitas Reddit
- Kontrak Record Reddit
- Dependency Pengembangan Frontend
- Encoding dan Penyimpanan Model
- Format Grafik Dashboard
- Capture Reddit Playwright
- Kontrak Record Reddit
- Wrapper RedditCrawler
- Render Dashboard Streamlit
- Penjelasan Topik Dashboard
- Pengujian Narasi Gemini
- Pengujian Integrasi Reddrix
- Audit Akuisisi Instagram
- Pengujian Penjelasan Topik
- Alur Dataset Model Dashboard
- Batas Integrasi Produksi
- Dependency Runtime Frontend
- Pengujian Resume Capture
- Eksekusi dan Ekspor Crawler
- Bukti Ekstraktif Topik
- Riwayat Pacing Instagram
- Interface Layanan Frontend
- BeeSense project
- Panduan Pipeline BeeSense
- Panduan Pipeline BeeSense
- Pemilihan Topik dan Coherence
- Arsitektur Model dan Dashboard
- InstaloaderCrawler
- Pengujian UI Streamlit
- Worker Chrome Instagram
- Konfigurasi Model Aktif
- Konteks dan Provenance Gemini
- Runtime Docker dan Display
- Encoding dan Penyimpanan Model
- Kampanye Browser Reddit
- Panduan Pipeline BeeSense
- Pemilihan Topik dan Coherence
- Integrasi Default Instaloader
- Riwayat Dataset dan Metodologi
- topic_sentence_export.py
- Pengujian Analisis Dashboard
- Skrip Build Frontend
- Lingkungan Training SBERT
- Riwayat Evaluasi Coherence
- Rencana Produk dan Survei
- Integrasi Default Instaloader
- Default Backend Reddit
- Struktur DOM Reddit
- Penjelasan Topik Dashboard
- Konfigurasi Trial Reddit
- build_topic_sentences.mjs
- Koordinator Backend Sosial
- Router dan Batas Error
- Panduan Pipeline BeeSense
- Verifikasi Artefak Dataset
- Validasi Record Reddit
- Metadata Package Frontend
- Pengujian Alur Frontend
- .topic_figure
- Q: ok sekarang training ulang menggunakan /Users/sakaheroji/Documents/BeeSense/outputs/social_20261030_combined_instagram_500_2h_02/social_data.xlsx, clustering. Buat 20 topik dengan coherence minimal 0.4. Lalu buat excel baru dengan tabel dengan kolom: topik, kalimat yang berada dalam cluster topik. lalu model digunakan kembali di dashboard streamlit yang di rebuild ulang, dan di commit dan dipush semuanya ke githubnya untuk di deploy ulang
- Parser Public Post
- Format Kode Frontend
- Alur Dataset Model Dashboard
- Integrasi Default Instaloader
- Rencana Layanan Backend
- CI Container Frontend
- Struktur Runtime Dashboard
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
- `CLI/class display overrides and explicit virtual preconditions` --references--> `RedditCrawler`  [EXTRACTED]
  docs/crawler/REDDIT_CRAWLER.md → Crawler/Backend/reddit_crawler.py
- `Adaptive display v1.1.0 auto platform policy` --conceptually_related_to--> `resolve_reddrix_display()`  [INFERRED]
  docs/crawler/REDDIT_CRAWLER.md → Crawler/Backend/social_crawler.py
- `Reddrix-only Camoufox factory controls initial and refreshed sessions` --conceptually_related_to--> `load_reddrix()`  [INFERRED]
  docs/crawler/REDDIT_CRAWLER.md → Crawler/Backend/social_crawler.py

## Import Cycles
- None detected.

## Hyperedges (group relationships)
- **Identitas dan keterlacakan ekspor Twitter** — docs_crawler_twitter_crawler_native_id_dedup, docs_crawler_twitter_crawler_native_parent_relations, docs_crawler_twitter_crawler_audit_bundle [EXTRACTED 1.00]
- **Lifecycle akses dengan state dan barrier** — docs_crawler_twitter_crawler_persistent_worker, docs_crawler_twitter_crawler_persistent_private_state, docs_crawler_twitter_crawler_access_barrier [EXTRACTED 1.00]
- **Verifikasi identitas dan parent hasil live** — docs_crawler_twitter_crawler_live_trial_results, docs_crawler_twitter_crawler_native_id_dedup, docs_crawler_twitter_crawler_native_parent_relations, docs_crawler_twitter_crawler_trial_verification [EXTRACTED 1.00]
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

## Communities (120 total, 20 thin omitted)

### Community 0 - "Pengambilan HTML Reddit"
Cohesion: 0.05
Nodes (50): browser_configuration(), browser_script(), InstagramBrowserWorker, Serial Chrome acquisition using a persistent profile and manual login.  The same, collect(), _configuration(), create_client(), error_receipt() (+42 more)

### Community 1 - "Penjadwalan dan Riwayat Akuisisi"
Cohesion: 0.05
Nodes (70): Per-platform bounds: max_posts 4000, max_candidates 6000, Main root reddrix.display_mode=auto, Historical exclusion source outputs/social_20261028_01, Configured global acquisition budget 10800 seconds, Retained Playwright-only CAPTCHA fields:600-second wait and five-second poll, Configured Reddit policy cooldown:360seconds, Configured Reddit retry cap:threeperrun, Current main configuration: platforms.reddit.enabled=true (+62 more)

### Community 2 - "Akuisisi X dan Ekspor Scweet"
Cohesion: 0.06
Nodes (51): Query pendidikan Indonesia jendela tujuh hari, Preset percobaan Twitter 30 menit, Jeda 5 dan 15 detik limiter window per operasi dan cap harian 120, 1.800 detik target 1.000 post 10 balasan, AccessBarrier, account_cooldown(), auth_material(), configuration() (+43 more)

### Community 3 - "Akuisisi YouTube"
Cohesion: 0.09
Nodes (34): error_code(), load_settings(), main(), parser(), run(), SafeLogger, Settings, video_url() (+26 more)

### Community 4 - "Crawler Selenium"
Cohesion: 0.07
Nodes (19): _barrier(), _create_driver(), main(), Content quoting an error is never used to classify an access barrier., Convert the shared rendered DOM capture without inventing identities., One browser operation. The parent enforces the hard process deadline., Stream evidence before completion; the original supervisor can retain it., Drop-in SocialCrawler with Selenium for both platforms and shared exports. (+11 more)

### Community 5 - "Pengujian Client Instagram"
Cohesion: 0.08
Nodes (7): Clock, FakeClient, InstagramCrawlerTests, Offline contract/deadline tests; fixture data is always marked synthetic., records(), spawn_fixture(), spawn_hanging()

### Community 6 - "Worker Instaloader"
Cohesion: 0.08
Nodes (24): AccessBarrier, configure_web_graphql(), error_receipt(), instaloader_options(), instaloader_worker(), InstaloaderAdapter, InstaloaderCrawler, InstaloaderWorker (+16 more)

### Community 7 - "Pengujian Koordinator Crawler"
Cohesion: 0.15
Nodes (5): rd_events(), receipt(), SocialCrawlerTests, spawn_youtube_fixture(), yt_events()

### Community 8 - "Penggabungan Dataset"
Cohesion: 0.08
Nodes (12): Native-ID baseline-then-new workbook merge with provenance, identity(), main(), merge(), merge_unique(), Merge compact crawl workbooks, rejecting repeated native content identities., Keep the latest supplied observation per native ID, with full row lineage., Return global native object ID plus its root; text never defines identity. (+4 more)

### Community 9 - "Model dan Pengujian NLP"
Cohesion: 0.11
Nodes (9): BeeSense application package., Encode with SBERT, fit UMAP + DBSCAN and optionally merge to a topic count., SocialNLPClusterer, CloudRuntimeTests, Run in an isolated Cloud environment, using only root requirements.txt., DashboardTests, encoder(), fixture() (+1 more)

### Community 10 - "Validasi Konfigurasi Frontend"
Cohesion: 0.10
Nodes (32): ConfigReview(), advance(), cap, committed, dataset(), get(), load(), plans (+24 more)

### Community 11 - "Koordinator Backend Sosial"
Cohesion: 0.11
Nodes (7): InstagramSettings, InstaloaderSettings, Compose platform workers with one configuration, scheduler and export bundle., SocialCrawler, Clock, InstagramIntegrationTests, Exercise Instagram through the combined coordinator, without network access.

### Community 12 - "Form Akuisisi dan Survei"
Cohesion: 0.12
Nodes (27): Automatic(), Baselines(), ConfigFields(), Manual(), ManualUrl(), labels, sample, Survey() (+19 more)

### Community 13 - "Riwayat Sesi Instagram"
Cohesion: 0.13
Nodes (32): Local session path and explicit360-second/3-retry policy, Instagram-only configured1800-second acquisition budget, Bounded hashtag discovery with authoritative local root filters, One LoginRequired recovery with verification-code preservation, CAAHTTP200 without session;legacyHTTP400 needs_upgrade, Cookie accepted for login/account read; trial02 firsthashtag LOGIN_REQUIRED, Spawned operations,global deadline and bounded retry policy, Explicit local login and session reuse with no automatic password replay (+24 more)

### Community 14 - "Worker Reddrix"
Cohesion: 0.14
Nodes (24): thread_url(), collect_reddrix(), _config(), _keywords(), load_reddrix(), normalize_reddrix_item(), _number(), Map Reddrix 1.2.14 dictionaries without inventing identity or dates. (+16 more)

### Community 15 - "Monitor Job dan Dataset"
Cohesion: 0.20
Nodes (24): Shell(), DatasetView(), History(), Composition(), JobDetail(), liveStates, PlatformCard(), ProgressChart() (+16 more)

### Community 16 - "Validasi Record Reddit"
Cohesion: 0.13
Nodes (14): _timestamp(), ContentInput, Dataset, KeywordMatcher, MemorySink, Aho-Corasick; offsets refer to Python Unicode code points in source., Shared pipeline; adapters cannot choose their own headers or cell formats., RecordFactory (+6 more)

### Community 17 - "Konfigurasi TypeScript"
Cohesion: 0.07
Nodes (26): compilerOptions, allowImportingTsExtensions, esModuleInterop, isolatedModules, jsx, lib, module, moduleResolution (+18 more)

### Community 18 - "Pengujian Worker Instaloader"
Cohesion: 0.13
Nodes (5): fixture_post(), hanging_fixture(), InstaloaderCrawlerTests, persistent_fixture(), Offline contracts for the separate Instaloader experiment.

### Community 19 - "Tipe dan Client API"
Cohesion: 0.10
Nodes (20): ApiError, base, httpApi, post(), request(), Baseline, Config, Counts (+12 more)

### Community 20 - "Generator Narasi Gemini"
Cohesion: 0.19
Nodes (18): One request per topic:top10weights plus10 fitted original sentences, Derive Indonesian Gemini labels after topic count and coherence pass., build_prompt(), canonical(), digest(), generate(), load_key(), Gemini narratives grounded in ranked topic keywords and representative sentences (+10 more)

### Community 21 - "Kontrak API Frontend"
Cohesion: 0.10
Nodes (24): Server history pagination, SSE, templates and organizational login remain future, Project-prefixed cookie-session API requires server CORS/CSRF/access controls, Expected typed frontend API contract; backend implementation pending, locatorKey is normalized permalink identity;nativeId may await backend verification, Increasing snapshotVersion and server-owned actions drive reconciliation, Safe structured errors distinguish API429 from worker-platform429, Survey commit binds review to session/project and revalidates conflicts, Typed plan/job requests bind plan IDs, idempotency and safe stop (+16 more)

### Community 22 - "Akuisisi X dan Ekspor Scweet"
Cohesion: 0.10
Nodes (5): hanging_worker(), persistent_worker(), Offline contracts for Twitter/X acquisition; no live credentials required., tweet(), TwitterCrawlerTests

### Community 23 - "Batas Akuisisi Reddit"
Cohesion: 0.12
Nodes (23): Configured 360-second policy and three HTTP 429 retries, Configured new sorting differs from Reddrix capability, Installed Reddrix 1.2.14 and Camoufox 156 browser evidence, Preserved compact SocialCrawler workbook, Historical trial 01 ended PARTIAL with zero posts, BeeSense interoperation delay differs from library request retries, Historical v1.0.0 module-specific non-Linux Xvfb shim, Adaptive display implemented after trial with no new crawl (+15 more)

### Community 24 - "Persyaratan Produk Crawler"
Cohesion: 0.18
Nodes (23): Atomic survey review and idempotent commit, Expected Crawler API contract, NLP schema eligibility gate, Seven-platform capability gating, Server-owned acquisition job lifecycle, Crawler frontend delivery and UX audit, Frontend verification evidence: 50 tests and container checks, BeeSense Crawler React frontend (+15 more)

### Community 25 - "thread_url"
Cohesion: 0.13
Nodes (4): Read-only exploration of completed NLP runs; no training on page reruns., SocialNLPStreamlitApp, DashboardreadsverifiedCSVwithnoAPIortrainingonrerun, Active20-topic/c_v0.4315 artifact andGemini display contract

### Community 26 - "Integrasi Default Instaloader"
Cohesion: 0.20
Nodes (23): Diagnostic and active-data separation, Diagnostic trial deduplication, Instaloader Docker artifact awaiting runtime verification, Standalone experiment caps, InstaloaderCrawler guide and evidence, Historical Instagram resume preset preserved, Historical trials 01–05, InstaloaderCrawler (+15 more)

### Community 27 - "Pengujian Parser Reddit"
Cohesion: 0.25
Nodes (6): bounded_events(), fixture_page(), Whole-post comment budget includes replies; nested replies share thread cap., RedditHtmlParser, RedditTests, worker()

### Community 28 - "app.py"
Cohesion: 0.15
Nodes (18): Root Docker context allowlist for relocated dashboard runtime, _load_artifacts(), main(), Streamlit entry point for local and Community Cloud dashboards.  Training lives, Dashboard build context includes root shim and artifact-reader packages, Relocated dashboard image uses root Streamlit shim and runtime-only wheels, Saved-model dashboard uses a separate runtime;full refitting stays Python 3.12, Root streamlit_apps.py delegates to Dashboard.app (+10 more)

### Community 29 - "Parsing Identitas Reddit"
Cohesion: 0.17
Nodes (14): assert_accessible(), content_node(), first(), HtmlSource, LocalHtmlSource, native_fullname(), Node, object_key() (+6 more)

### Community 30 - "Kontrak Record Reddit"
Cohesion: 0.22
Nodes (4): ContractTests, digest(), dumps(), validate_row()

### Community 31 - "Dependency Pengembangan Frontend"
Cohesion: 0.10
Nodes (21): devDependencies, eslint, @eslint/js, jsdom, prettier, @testing-library/user-event, @types/react, @types/react-dom (+13 more)

### Community 32 - "Encoding dan Penyimpanan Model"
Cohesion: 0.21
Nodes (5): file_hash(), json_write(), main(), Publish a new versioned sidecar; never modify the original run., Reuse immutable SBERT features only after verifying data/model identity.

### Community 33 - "Format Grafik Dashboard"
Cohesion: 0.18
Nodes (15): apply_browser_patch(), browser_graphql_query(), _check(), _cookie(), _hints(), _load_tokens(), main(), _pace() (+7 more)

### Community 34 - "Capture Reddit Playwright"
Cohesion: 0.21
Nodes (12): atomic_json(), barrier_status(), campaign_plan(), find_cli(), PlaywrightCLI, rate_limit_seconds(), run(), save_capture() (+4 more)

### Community 35 - "Kontrak Record Reddit"
Cohesion: 0.18
Nodes (12): add_readme(), BundleSink, main(), parser(), Validate the embedded contract; an external descriptor is optional., Atomic new directory; streaming JSONL + streaming, formula-safe Excel., run(), run_self_tests() (+4 more)

### Community 36 - "Wrapper RedditCrawler"
Cohesion: 0.16
Nodes (5): main(), Reddit-only compatibility entry point for the integrated SocialCrawler Reddrix b, Run only Reddit through the shared Reddrix implementation in SocialCrawler., RedditCrawler, RedditCrawlerTests

### Community 38 - "Penjelasan Topik Dashboard"
Cohesion: 0.17
Nodes (13): percent(), Count evidence in the filter, keeping sentences/comments/parents distinct., Filters retain model membership and do not recompute c_v, Selected-topic c_v card is separate from the full-model mean, Occurrences, unique sentences, comments and source roots have different denominators, Five artifact-backed Streamlit analysis views, Platform and top-five source graphs count unique topic comments, Responsive cards, visible keyboard focus and chart/table alternatives verified (+5 more)

### Community 39 - "Pengujian Narasi Gemini"
Cohesion: 0.19
Nodes (4): GeminiArtifactTests, GeminiTests, response(), topic()

### Community 40 - "Pengujian Integrasi Reddrix"
Cohesion: 0.17
Nodes (12): HtmlPage, now_iso(), PublicHtmlSource, Only public HTML pages on the canonical host; never auth/API routes., RestrictedRedirect, safe_web_url(), SourceFailure, thread_id() (+4 more)

### Community 41 - "Audit Akuisisi Instagram"
Cohesion: 0.12
Nodes (18): 27–30October inclusiverefers tosourceacquisitiondate,notpostdate, User stopped Instagram acquisition; no subsequent crawl, Final audited33034-record Instagram-inclusive corpus, Fiveintegrationtests plus76NLP andoneisolateddashboardtestpassed, Bounded Instagram recovery does not override user stop, Latestnative-ID observation dedupwithrootconflict rejection, Versionedmergepublishesrecordlineage/duplicateauditandchecksums, 20-topic/coherence gate passed; active configuration switched (+10 more)

### Community 42 - "Pengujian Penjelasan Topik"
Cohesion: 0.25
Nodes (3): ExplanationTests, model_from_counts(), profile()

### Community 43 - "Alur Dataset Model Dashboard"
Cohesion: 0.15
Nodes (17): Dashboard Python 3.12 and 3.14 runtime matrix, Offline crawler and NLP regression tests, Verify BeeSense CI, Synthetic Reddit post, comment and reply fixture, Reddit browser campaign helpers, User checkpoint audit export and verification, Manual CAPTCHA recovery within global deadline, Reddit Playwright runner (+9 more)

### Community 44 - "Batas Integrasi Produksi"
Cohesion: 0.13
Nodes (17): Final style samples:96desktop/78narrow444px elements,all black and≥13 px, React frontend and simulation verified; production acquisition integration unavailable, Implemented UI flows:automatic/manual, monitor, survey and dataset review, Applied UX fixes:linked errors, step validation, deep links, drawer focus and inertness, Browser actual widths400/444px;requested360px remains unproven, Production release waits for API/worker/access/export and survey adapter integration, Late plan, URL and survey validation is ignored after input changes, Demo IDs, baseline data and downloads are synthetic rather than acquisition evidence (+9 more)

### Community 45 - "Dependency Runtime Frontend"
Cohesion: 0.12
Nodes (17): dependencies, @fontsource-variable/plus-jakarta-sans, lucide-react, papaparse, react, react-dom, react-router-dom, @tanstack/react-query (+9 more)

### Community 47 - "Eksekusi dan Ekspor Crawler"
Cohesion: 0.15
Nodes (5): main(), Describe the acquisition backend independently of the shared export., Validate and return the effective plan without browser/network access., Re-export saved Contents without network or modifying the source bundle., Mixed bundles retain backend-specific provenance

### Community 48 - "Bukti Ekstraktif Topik"
Cohesion: 0.12
Nodes (6): _explain_filtered(), Identify the parent thread, not the individual comment URL., Extract real sentences using relevance plus MMR diversity., Evidence-grounded topic descriptions and descriptive, source-aware trends., Explain already verified artifacts without encoding or fitting again., Rule-based segmentation preserving exact offsets in the original text.

### Community 49 - "Riwayat Pacing Instagram"
Cohesion: 0.17
Nodes (16): Current Instagram bounded retry configuration; historical execution chronology, Chrome remains available for operator inspection, Browser response429 and private-header boundary, Verifieddashboard publication precedes offlinecrawlerpacing, User-provided DataDwip Instagram pacing reference, Historical Instagram run:248 posts and 2,128 comments, Historical version-1.5.1 fixed Instagram recovery policy, Documented local exponential cooldown respects longer Retry-After (+8 more)

### Community 51 - "BeeSense project"
Cohesion: 0.21
Nodes (15): Stored Indonesian Gemini topic narratives, Instagram acquisition, dataset and training pipeline, Random pacing, batch pauses and exponential 429 backoff, Native-ID deduplication and latest-observation lineage, Verified 30 October 20-topic model, BeeSense project structure and root-relative paths, Separate dashboard, crawler and training runtimes, Historical Graphify memory of the native SBERT/UMAP/DBSCAN migration (+7 more)

### Community 52 - "Panduan Pipeline BeeSense"
Cohesion: 0.15
Nodes (15): Instagram Pacing and Backoff, Artifact Only Dashboard Runtime, 30 October Three Platform Model, BeeSense Dashboard Guide, Kendall Tau B Consistency, Maximal Marginal Relevance, Supported Descriptive Topic Trends, Theil Sen Monthly Slope (+7 more)

### Community 53 - "Panduan Pipeline BeeSense"
Cohesion: 0.23
Nodes (15): Native ID Workbook Consolidation, BeeSense Topic Prompt Version 2, Class Based TF IDF Labels, Gensim C V Coherence Protocol, Euclidean DBSCAN Clustering, Topic Model Quality Gate, Multilingual SBERT Embeddings, Social NLP Methodology (+7 more)

### Community 54 - "Pemilihan Topik dan Coherence"
Cohesion: 0.13
Nodes (15): Internal model metrics do not establish accuracy or representativeness, Unweighted mean across all 20 final non-noise topics, Stored protocol, reference hash, baseline identity and per-topic scores, Gensim c_v protocol: top 10 terms, window 110, phrase tokens, Historical46143-sentence reference; current corpus remains separately bound, Original DBSCAN IDs and full reduction mapping survive final topic IDs, Historical7/20 shortfalls; current model has8/20, Training-corpus coherence is not holdout or labeled accuracy (+7 more)

### Community 55 - "Arsitektur Model dan Dashboard"
Cohesion: 0.17
Nodes (15): Nine Gemini offline tests and all20 actual contextual CSV rows validated, Verified current model and20context-grounded narratives, Current20-topic macro c_v0.4315219014 model, Active33034-record three-platform corpus, Producer2.4 contextual Gemini stage after verified model gate, Prior Graphify memory: Selenium crawler preserves Excel contract, BeeSense crawler, NLP and dashboard class architecture, React host/container addition preserves existing acquisition/model artifacts (+7 more)

### Community 56 - "InstaloaderCrawler"
Cohesion: 0.17
Nodes (4): FakeReddrix, item(), Reddrix field/identity boundaries and the real, shared Excel exporter., records()

### Community 58 - "Worker Chrome Instagram"
Cohesion: 0.20
Nodes (12): Standalone browser1800-second preset, updated bounded retry, instagramDocumentPayload(), instagramNavigate(), instagramRetryAfter(), instagramSourceRateLimit(), Browser discovery follows InstagramUI order withlocaleligibilitychecks, Bind document-script comments by native DOM permalink andsame shortcode, macOS headed trial andLinuxprepared-profile requirements (+4 more)

### Community 59 - "Konfigurasi Model Aktif"
Cohesion: 0.26
Nodes (14): Active artifacts outputs/nlp_20261030_instagram_topics20_02, Configured33034-record final merged workbook, Active20-topic Instagram-inclusive model configuration, Current active Gemini enabled; historical disabled state retained, Final Instagram-inclusive20-topic/Gemini configuration, Active20-topic Instagram-inclusive model configuration, RetainedSBERTrevision,UMAP/DBSCANbudget andexplanationgates, All20 actual contextual Gemini narratives validated (+6 more)

### Community 60 - "Konteks dan Provenance Gemini"
Cohesion: 0.20
Nodes (14): Verified model configuration enables contextual Gemini CSV, Complete contextual20-row Gemini CSV passes bundle gate, Boundedtransientretryandfail-closedpublication, Prompt2/CSV2 with preserved keyword-only version1, Atomic20-row contextual CSV with per-topic provenance, ContextualCSVextension2 binds Parquet; legacyextension1 supported, Deterministic fitted-sentence context ranking, Gemini GenerateContent APIreference (+6 more)

### Community 61 - "Runtime Docker dan Display"
Cohesion: 0.19
Nodes (14): Relocated combined crawler image runs package module as UID10001, Adaptive display v1.1.0 auto platform policy, Actual macOS lifecycle test versus mocked Linux display matrix, CLI/class display overrides and explicit virtual preconditions, Requested/effective display mode is visible in plan and source metadata, Reddrix Docker image unbuilt: local daemon unavailable, Reddrix-only Camoufox factory controls initial and refreshed sessions, Historical integrated test scope and unverified Docker runtime (+6 more)

### Community 62 - "Encoding dan Penyimpanan Model"
Cohesion: 0.16
Nodes (5): Use the same class TF-IDF vocabulary for selection and publication., Macro c_v on ALL non-noise topics and a fixed full-corpus reference.          Un, Preserve explicit zero distances, including identical sentence vectors., Merge entire DBSCAN groups using sentence-weighted Ward linkage.          Minimi, Select DBSCAN parameters on UMAP; evaluate in original SBERT geometry.

### Community 63 - "Kampanye Browser Reddit"
Cohesion: 0.27
Nodes (8): classifyCaptureFailure(), enrichBatch(), rateLimitSeconds(), inWindow(), mergeCandidates(), row, source, window

### Community 64 - "Panduan Pipeline BeeSense"
Cohesion: 0.17
Nodes (13): Shared rendered_thread_dom.mjs extraction, Relative dates remain calendar estimates, Historical Selenium implementation preset:500roots/platform andonehour, Separate non-root crawler container with Selenium Grid, Fresh Chrome guest session per operation, Official Selenium Manager ChromeDriver selection, SocialCrawlerSelenium Guide, Shared SocialExportMixin Contract (+5 more)

### Community 65 - "Pemilihan Topik dan Coherence"
Cohesion: 0.23
Nodes (12): Configured c_v threshold 0.4 with topn 10 and window 110, Configured final topic target: 20, Additional c_v >=0.4 gate preserves earlier eligibility rules, DBSCAN core points and noise without membership probabilities, Two UMAP 10 D projections seeded 42 and 43, Euclidean DBSCAN with reusable bounded radius graphs, Historical29October bounded15-candidate grid; shared budget retained, Evaluate final topic partitions before candidate selection (+4 more)

### Community 66 - "Integrasi Default Instaloader"
Cohesion: 0.35
Nodes (12): SocialCrawler Excel and audit bundle, Read-only native-ID baseline exclusion, Shared filters and round-robin campaign scheduler, SocialCrawler guide, Historical29October campaign PARTIAL outcome, Historical Instagram 1.5 recovery and1.5.2 pacing, SocialCrawler historical test and current container guidance, Native-ID workbook merge and provenance (+4 more)

### Community 67 - "Riwayat Dataset dan Metodologi"
Cohesion: 0.20
Nodes (12): Historical audit workbook: 50 YouTube and 181 Reddit root identities, Historicalcorporaandscoresarenotcurrentqualitycomparators, Obsidian dashboard dataset provenance, FinalnativeIDauditwithpreservedhistoricalchecksums, Artifact-only dashboard without Gensim/Torch imports, BeeSense startup, verification and coherence training runbook, Four Parquet files, UMAP npz and eleven-artifact v 2 manifest, Obsidian method: verify embeddings then refit UMAP/DBSCAN (+4 more)

### Community 68 - "topic_sentence_export.py"
Cohesion: 0.29
Nodes (7): export_payload(), main(), Prepare an original-sentence export and seal it into a new NLP snapshot., Keep original variants; remove repeated occurrences of the same text., Verify every Excel membership before publishing the complete snapshot., seal(), TopicSentenceExportTests

### Community 70 - "Skrip Build Frontend"
Cohesion: 0.18
Nodes (11): scripts, build, build:demo, check, dev, format, format:check, lint (+3 more)

### Community 71 - "Lingkungan Training SBERT"
Cohesion: 0.24
Nodes (11): Relocated Selenium image preserves included requirements and package modules, Isolated local environment and separately downloaded browser, New-corpus native SBERT encoding or exact verified cache reuse, Separate SBERT training and artifact-only dashboard environments, Training/evaluation-only Gensim coherence requirements, NLP, Streamlit and Plotly dependency ranges, Frozen full NLP and offline development environment, Isolated Reddrix 1.2.14 crawler dependency pins (+3 more)

### Community 72 - "Riwayat Evaluasi Coherence"
Cohesion: 0.25
Nodes (11): Historical combined snapshot QA; relocated root shim checked offline, Historical29October macro c_v0.4720034334, Pinned multilingual SentenceTransformer safetensors encoder, Historical29October exact-corpus SBERT/UMAP cache evidence, Overflow-window averaging and L 2-normalized 384 D embeddings, Historical old-corpus baselines retained; no cross-corpus quality comparison, Encoder cache bound to immutable revision and text/checksums, Checksum-verified reuse of immutable SBERT embeddings (+3 more)

### Community 73 - "Rencana Produk dan Survei"
Cohesion: 0.20
Nodes (11): Curated two-menu contract with URL/Survey under Manual, Curated immutable dataset selection does not train or change Dashboard, Curated Crawler PRD status:frontend implemented, backend pending, New survey schema must preserve role, question, response, version and permission, Crawler wireframes are illustrative design requirements, not app screenshots, Monitor prioritizes status, units, barriers and next actions over logs, Worker-session CAPTCHA and429 UI offer observation rather than bypass, Responsive drawer/table/focus behavior is a design target (+3 more)

### Community 74 - "Integrasi Default Instaloader"
Cohesion: 0.40
Nodes (11): Published30October active corpus and20-topic snapshot, Artifact checksum, Git allowlist and CI gates, Separated crawler, NLP and dashboard architecture, Dashboard/training dependency isolation, Gemini topic narrative artifacts, Retained historical workbooks and NLP snapshots, README historical dashboard Docker verification, SBERT/UMAP/DBSCAN training and verified embedding reuse (+3 more)

### Community 75 - "Default Backend Reddit"
Cohesion: 0.22
Nodes (10): Main config now selects Reddit backend=reddrix, Hard-deadline subprocess retains streamed records, No database/model/persistent-contract migration, Default Reddit Reddrix with YouTube yt-dlp since SocialCrawler 1.4, Explicit legacy HTML, Playwright and checkpoint selections, RedditCrawler wrapper delegates to the shared coordinator, Reddrix trial preserves existing model and frontend boundaries, Integrated SocialCrawler Reddrix with thin Reddit-only wrapper (+2 more)

### Community 76 - "Struktur DOM Reddit"
Cohesion: 0.24
Nodes (3): BoundedDom, Small serialised-DOM reader, not a browser or full HTML5 repair engine., HTMLParser

### Community 77 - "Penjelasan Topik Dashboard"
Cohesion: 0.24
Nodes (10): Historical combined20 UI/runtime verification retained after relocation, On-demand explanations from active combined 20-topic artifacts, Historical v 1 HDBSCAN directional counts for 51 topics, Historical combined 20-topic local Docker verification; reorganized image unbuilt, MMR evidence and guarded Theil-Sen/Kendall directions, Module API creates source-bound explanation sidecars without retraining, Source-bound beesense-topic-explanations:1 sidecar manifest, Traceable extractive topic explanations (+2 more)

### Community 78 - "Konfigurasi Trial Reddit"
Cohesion: 0.31
Nodes (9): Read-only historical baseline exclusion, Original date boundary and university-topic query scope, Tracked reddrix.display_mode=auto, Configured root/comment/candidate/time budgets, Trial config now explicitly selects Reddrix; wrapper preserves legacy compatibility, Tracked Reddit trial configuration, Original historical date window, keywords and read-only baseline, Thin Reddit-only wrapper selects shared Reddrix explicitly (+1 more)

### Community 79 - "build_topic_sentences.mjs"
Cohesion: 0.22
Nodes (6): body, payload, [payloadPath, outputPath, previewDir], sentences, topics, workbook

### Community 81 - "Router dan Batas Error"
Cohesion: 0.25
Nodes (3): client, ErrorBoundary, router

### Community 82 - "Panduan Pipeline BeeSense"
Cohesion: 0.32
Nodes (8): Selenium Rendered DOM, Instaloader Instagram Backend, Combined Crawler Environment, Offline Regression and Crawler Environment, Instagram Chrome Worker Environment, Instaloader 4.16 Environment, Isolated Reddrix Environment, Selenium 4.51.0 Environment

### Community 83 - "Verifikasi Artefak Dataset"
Cohesion: 0.36
Nodes (7): main(), published_source_files(), Verify published source workbooks and the dashboard artifact bundle., Verify record identity independently of sentence-text deduplication., A merge report binds its small, explicit audit sidecars to the input., verify(), verify_native_dataset()

### Community 84 - "Validasi Record Reddit"
Cohesion: 0.38
Nodes (4): load_settings(), parsed_number(), Settings, timeout_fixture()

### Community 85 - "Metadata Package Frontend"
Cohesion: 0.29
Nodes (6): engines, node, name, private, type, version

### Community 86 - "Pengujian Alur Frontend"
Cohesion: 0.40
Nodes (3): AppContext, demoApi, UrlReview

### Community 87 - ".topic_figure"
Cohesion: 0.40
Nodes (3): _graph_positions(), Bounded topic graph: volume from filtered rows, semantic edges from the full mod, Keep the full-model layout stable while volume and edge filters change.

### Community 88 - "Q: ok sekarang training ulang menggunakan /Users/sakaheroji/Documents/BeeSense/outputs/social_20261030_combined_instagram_500_2h_02/social_data.xlsx, clustering. Buat 20 topik dengan coherence minimal 0.4. Lalu buat excel baru dengan tabel dengan kolom: topik, kalimat yang berada dalam cluster topik. lalu model digunakan kembali di dashboard streamlit yang di rebuild ulang, dan di commit dan dipush semuanya ke githubnya untuk di deploy ulang"
Cohesion: 0.40
Nodes (4): Answer, Outcome, Q: ok sekarang training ulang menggunakan /Users/sakaheroji/Documents/BeeSense/outputs/social_20261030_combined_instagram_500_2h_02/social_data.xlsx, clustering. Buat 20 topik dengan coherence minimal 0.4. Lalu buat excel baru dengan tabel dengan kolom: topik, kalimat yang berada dalam cluster topik. lalu model digunakan kembali di dashboard streamlit yang di rebuild ulang, dan di commit dan dipush semuanya ke githubnya untuk di deploy ulang, Source Nodes

### Community 90 - "Format Kode Frontend"
Cohesion: 0.50
Nodes (3): printWidth, singleQuote, trailingComma

### Community 91 - "Alur Dataset Model Dashboard"
Cohesion: 0.83
Nodes (4): InstagramCrawler browser and instagrapi history, Explicit instagrapi backend, Persistent Chrome worker with manual login, Shared compact and eight-sheet social export contract

### Community 92 - "Integrasi Default Instaloader"
Cohesion: 0.50
Nodes (4): Vault architecture and audit flow, Frontend React simulation and planned API architecture, HOME attributed historical release/model evidence, BeeSense HOME index

### Community 93 - "Rencana Layanan Backend"
Cohesion: 0.50
Nodes (4): Backend PRD is not written; API/worker services remain proposed, Proposed persistent Python worker and authorized CAPTCHA browser bridge, Proposed server session, role, project isolation and idempotency, Proposed survey transactions, immutable datasets and operational audit

### Community 94 - "CI Container Frontend"
Cohesion: 0.67
Nodes (3): SPA container health and deep-link checks, Crawler frontend CI, BeeSense Crawler SPA document

### Community 95 - "Struktur Runtime Dashboard"
Cohesion: 0.67
Nodes (3): Package module CLIs retain repository-root path semantics, Crawler, MachineLearning and Dashboard packages with grouped supporting folders, Reorganized BeeSense package and supporting-file structure

## Knowledge Gaps
- **173 isolated node(s):** `window`, `source`, `row`, `candidate`, `singleQuote` (+168 more)
  These have ≤1 connection - possible missing edges or undocumented components.
- **20 thin communities (<3 nodes) omitted from report** — run `graphify query` to explore isolated nodes.

## Suggested Questions
_Questions this graph is uniquely positioned to answer:_

- **Bagaimana TwitterCrawler mempertahankan format Excel dan audit yang sama dengan crawler Reddit dan Instagram?**
  _Dokumen dan kode menghubungkan ScweetWorker dengan RecordFactory, Dataset, BundleSink dan SocialExportMixin yang dipakai bersama._
- **Why does `SocialCrawler` connect `Koordinator Backend Sosial` to `Pengambilan HTML Reddit`, `Penjadwalan dan Riwayat Akuisisi`, `Crawler Selenium`, `Pengujian Client Instagram`, `Worker Instaloader`, `Pengujian Koordinator Crawler`, `Worker Reddrix`, `Validasi Record Reddit`, `Batas Akuisisi Reddit`, `Wrapper RedditCrawler`, `Audit Akuisisi Instagram`, `Eksekusi dan Ekspor Crawler`, `Riwayat Pacing Instagram`, `Arsitektur Model dan Dashboard`, `InstaloaderCrawler`, `Runtime Docker dan Display`, `Panduan Pipeline BeeSense`, `Default Backend Reddit`, `Koordinator Backend Sosial`, `Struktur Runtime Dashboard`?**
  _High betweenness centrality (0.272) - this node is a cross-community bridge._
- **Why does `SocialNLPClusterer` connect `Model dan Pengujian NLP` to `Generator Narasi Gemini`, `thread_url`, `app.py`, `Encoding dan Penyimpanan Model`, `Penjelasan Topik Dashboard`, `Pengujian Narasi Gemini`, `Audit Akuisisi Instagram`, `Pengujian Penjelasan Topik`, `Bukti Ekstraktif Topik`, `Pemilihan Topik dan Coherence`, `Arsitektur Model dan Dashboard`, `Pengujian UI Streamlit`, `Konfigurasi Model Aktif`, `Konteks dan Provenance Gemini`, `Encoding dan Penyimpanan Model`, `Pemilihan Topik dan Coherence`, `Riwayat Dataset dan Metodologi`, `topic_sentence_export.py`, `Riwayat Evaluasi Coherence`, `Penjelasan Topik Dashboard`, `Verifikasi Artefak Dataset`, `Struktur Runtime Dashboard`?**
  _High betweenness centrality (0.147) - this node is a cross-community bridge._
- **Why does `SocialCrawler guide` connect `Integrasi Default Instaloader` to `Panduan Pipeline BeeSense`, `Penjadwalan dan Riwayat Akuisisi`, `Integrasi Default Instaloader`, `Panduan Pipeline BeeSense`, `Panduan Pipeline BeeSense`, `Panduan Pipeline BeeSense`, `Integrasi Default Instaloader`?**
  _High betweenness centrality (0.078) - this node is a cross-community bridge._
- **Are the 24 inferred relationships involving `SocialCrawler` (e.g. with `RedditCrawler` and `_SeleniumSource`) actually correct?**
  _`SocialCrawler` has 24 INFERRED edges - model-reasoned connections that need verification._
- **Are the 15 inferred relationships involving `SocialNLPClusterer` (e.g. with `SocialNLPStreamlitApp` and `Historical29October bounded15-candidate grid; shared budget retained`) actually correct?**
  _`SocialNLPClusterer` has 15 INFERRED edges - model-reasoned connections that need verification._
- **Are the 87 inferred relationships involving `ValueError` (e.g. with `browser_configuration()` and `instaloader_options()`) actually correct?**
  _`ValueError` has 87 INFERRED edges - model-reasoned connections that need verification._
- **Are the 3 inferred relationships involving `SocialNLPStreamlitApp` (e.g. with `Platform and top-five source graphs count unique topic comments` and `Term bars show bounded phrase presence in unique filtered sentences`) actually correct?**
  _`SocialNLPStreamlitApp` has 3 INFERRED edges - model-reasoned connections that need verification._
## TwitterCrawler delivery — 31 October 2026

Scoped incremental update: eight Twitter-related sources were extracted; the pre-existing graph was retained. The listed commit is the baseline of this modified working tree, not a claim that these changes were committed. Auth, SQLite state and raw acquisition data were excluded from graph input.

Verification: {"implementation": "Standalone TwitterCrawler Scweet5.8.2 with shared Excel contract; library cooldown waits preserve state; actual HTTP429 stops", "aggregate": "/Users/socs3/Documents/BeeSense/outputs/twitter_scweet_20261031_30m_combined", "mode": "compact_projection_of_two_verified_audit_bundles", "records": 45, "unique_native_ids": 45, "duplicate_native_ids": 0, "counts": {"post": 33, "comment": 11, "reply": 1}, "unresolved_native_parents": 0, "sources": [{"path": "/Users/socs3/Documents/BeeSense/outputs/twitter_scweet_20261031_30m_01", "manifest_sha256": "7dbb33266ad108602155552bf57bdd50764aab876de6e383e6dff796605a4577", "records": 30, "status": "PARTIAL", "stop_reason": "ACCOUNT_UNAVAILABLE", "elapsed_seconds": 864.74, "configured_seconds": 1800, "live_access_verified": true, "network": {"requests": 65, "http_status_counts": {"200": 65}}}, {"path": "/Users/socs3/Documents/BeeSense/outputs/twitter_scweet_20261031_30m_02", "manifest_sha256": "164a27a20f04e418e8bf2782b413c72dc4700c4cca7e5212d86441d5098f986c", "records": 15, "status": "PARTIAL", "stop_reason": "TIME_BUDGET_EXHAUSTED", "elapsed_seconds": 755.01, "configured_seconds": 755, "live_access_verified": true, "network": {"requests": 59, "http_status_counts": {"200": 59}}}], "compact": {"file": "social_data.xlsx", "sheets": ["Data"], "columns": ["platform", "jenis", "judul_post", "tanggal_post_wib", "akurasi_tanggal_post", "tanggal_konten_wib", "akurasi_tanggal_konten", "teks", "url", "teks_dipotong"], "timezone": "Asia/Jakarta", "rows": 45, "counts": {"twitter:post": 33, "twitter:comment": 11, "twitter:reply": 1}, "date_accuracy_counts": {"pasti": 45}, "truncated_texts": 0, "filtered_roots": 0, "filtered_comments": 0, "date_estimate_anchor": "source_observed_at", "relative_date_precision": "calendar_date_not_exact_timestamp"}, "full_audit_location": "dataset.xlsx and all eight JSONL tables remain in each source run", "target_posts": 1000, "target_met": false, "configured_trial_window_seconds": 1800, "database_migration_required": false, "docker_build_verified": false, "offline_tests_passed": 17, "social_regression_tests": 71, "social_regression_skipped": 1, "trial_wall_seconds": 1803.57, "acquisition_run_seconds": 1619.75, "trial_note": "30-minute wall-clock trial including one library cooldown and adapter update/resume; acquisition runs total fewer active seconds. Actual HTTP429 responses were not observed.", "all_manifest_hashes_valid": true, "all_excel_headers_valid": true, "excel_formula_cells": 0, "local_session_material_in_exports": false, "docker_context_secret_exclusion": true, "isolated_context_dry_run": true, "docker_remaining_command": "docker build -f deployment/docker/Dockerfile.twitter -t beesense-twitter:local .", "social_regression_passed": 70, "cross_root_parent_edges": 0, "actual_http_429_responses": 0, "library_cooldown_events": 1}

Changed-fragment health warnings: {"dangling_endpoint_edges": 38}. AST references outside the scoped fragment may not resolve in its diagnostics. Exported edge endpoints and hyperedge membership are verified; these checks do not establish completeness of extraction. Semantic usage is unmeasured; historical cumulative numeric totals exclude unknown usage.
