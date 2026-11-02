# Graph Report - /Users/socs3/Documents/BeeSense  (2026-11-02)

## Corpus Check
- 6 files · ~10,194 words
- Verdict: corpus is large enough that graph structure adds value.

## Summary
- 2062 nodes · 4332 edges · 130 communities (97 shown, 33 thin omitted)
- Extraction: 94% EXTRACTED · 6% INFERRED · 0% AMBIGUOUS · INFERRED: 272 edges (avg confidence: 0.7)
- Token cost: AST 0 LLM tokens; semantic usage unavailable (not a measured zero).

## Graph Freshness
- Built from commit: `3987e049`
- Run `git rev-parse HEAD` and compare to check if the graph is stale.
- Run `graphify update .` after code changes (no API cost).

## Community Hubs (Navigation)
- Panduan Pipeline BeeSense
- Pengambilan HTML Reddit
- Worker Instaloader
- Integrasi X dan Provenans Akuisisi
- Crawler Selenium
- Akuisisi YouTube
- Penyaringan Relevansi dan Narasi Topik
- Penggabungan Dataset
- Riwayat Sesi Instagram
- Penjadwalan dan Riwayat Akuisisi
- Penyaringan Relevansi dan Narasi Topik
- Pengujian Client Instagram
- Pengujian Koordinator Crawler
- Koordinator Backend Sosial
- Validasi Konfigurasi Frontend
- Form Akuisisi dan Survei
- Model dan Pengujian NLP
- Integrasi X dan Provenans Akuisisi
- Monitor Job dan Dataset
- Pengujian Parser Reddit
- Kontrak Record Reddit
- Parsing Identitas Reddit
- Konfigurasi TypeScript
- Pengujian Worker Instaloader
- Tipe dan Client API
- Encoding dan Penyimpanan Model
- Kontrak Record Reddit
- Worker Reddrix
- Kontrak API Frontend
- Persyaratan Produk Crawler
- Pengujian Narasi Gemini
- Integrasi Default Instaloader
- Kontrak Record Reddit
- Dependency Pengembangan Frontend
- Batas Akuisisi Reddit
- Akuisisi YouTube
- Penggabungan Dataset
- Capture Reddit Playwright
- Struktur DOM Reddit
- Wrapper RedditCrawler
- Render Dashboard Streamlit
- Pengujian Penjelasan Topik
- Batas Integrasi Produksi
- Dependency Runtime Frontend
- thread_url
- topic_sentence_export.py
- app.py
- Batas Akuisisi Reddit
- Pengujian Resume Capture
- Interface Layanan Frontend
- Rencana Produk dan Survei
- Pengujian UI Streamlit
- Wrapper RedditCrawler
- Pengujian Narasi Gemini
- Kampanye Browser Reddit
- Panduan Pipeline BeeSense
- Alur Dataset Model Dashboard
- Integrasi X dan Provenans Akuisisi
- Alur Dataset Model Dashboard
- Model dan Pengujian NLP
- Pengujian Analisis Dashboard
- Alur Dataset Model Dashboard
- Koordinator Backend Sosial
- app.py
- Integrasi X dan Provenans Akuisisi
- Integrasi X dan Provenans Akuisisi
- Operasi dan Verifikasi BeeSense
- Pengujian Narasi Gemini
- Skrip Build Frontend
- Batas Akuisisi Reddit
- thread_url
- Panduan Pipeline BeeSense
- Panduan Pipeline BeeSense
- Integrasi X dan Provenans Akuisisi
- build_topic_sentences.mjs
- Integrasi X dan Provenans Akuisisi
- Router dan Batas Error
- Panduan Pipeline BeeSense
- Encoding dan Penyimpanan Model
- Panduan Pipeline BeeSense
- Metadata Package Frontend
- Operasi dan Verifikasi BeeSense
- Integrasi X dan Provenans Akuisisi
- Pengujian Alur Frontend
- Operasi dan Verifikasi BeeSense
- Operasi dan Verifikasi BeeSense
- Q: ok sekarang training ulang menggunakan /Users/sakaheroji/Documents/BeeSense/outputs/social_20261030_combined_instagram_500_2h_02/social_data.xlsx, clustering. Buat 20 topik dengan coherence minimal 0.4. Lalu buat excel baru dengan tabel dengan kolom: topik, kalimat yang berada dalam cluster topik. lalu model digunakan kembali di dashboard streamlit yang di rebuild ulang, dan di commit dan dipush semuanya ke githubnya untuk di deploy ulang
- Parsing Identitas Reddit
- Parser Public Post
- Format Kode Frontend
- Operasi dan Verifikasi BeeSense
- Model dan Pengujian NLP
- CI Container Frontend
- Batas Akuisisi Reddit
- Batas Akuisisi Reddit
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
1. `SocialNLPClusterer` - 101 edges
2. `SocialCrawler` - 97 edges
3. `SocialNLPStreamlitApp` - 49 edges
4. `SocialCrawlerTests` - 42 edges
5. `Cara kerja BeeSense` - 35 edges
6. `InstagramCrawlerTests` - 33 edges
7. `file_hash()` - 32 edges
8. `Reddrix-backed RedditCrawler runbook` - 29 edges
9. `NLPTests` - 29 edges
10. `Class NLP BeeSense: SBERT + UMAP + DBSCAN` - 29 edges

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
- **Artifact-connected acquisition, selection, and topic workflow** — graphify_out_obsidian_peta_cara_kerja_beesense_crawler_backend_social_crawler_py, graphify_out_obsidian_peta_cara_kerja_beesense_crawler_backend_social_export_py, graphify_out_obsidian_peta_cara_kerja_beesense_scripts_merge_social_datasets_py, graphify_out_obsidian_peta_cara_kerja_beesense_scripts_filter_context_relevance_py, graphify_out_obsidian_peta_cara_kerja_beesense_machinelearning_social_nlp_py [EXTRACTED 1.00]
- **Published before/after comparison with verified Cloud radio** — graphify_out_obsidian_peta_cara_kerja_beesense_verified_streamlit_release, docs_machine_learning_context_relevance_config_dashboard_json, docs_machine_learning_context_relevance_outputs_nlp_20261102_relevance_topics20_gemini_02, docs_machine_learning_context_relevance_outputs_nlp_20261102_twitter_topics20_gemini_01, graphify_out_obsidian_peta_cara_kerja_beesense_commit_778cb81, graphify_out_obsidian_peta_cara_kerja_beesense_commit_3987e04 [EXTRACTED 1.00]
- **Semantic reference filtering with verified context and audit** — docs_machine_learning_context_relevance_contextrelevancefilter, docs_machine_learning_context_relevance_localsemanticbackend, docs_machine_learning_context_relevance_config_context_relevance_json, docs_machine_learning_context_relevance_verified_native_context, docs_machine_learning_context_relevance_relevant_only_clustering_and_complete_audit [EXTRACTED 1.00]
- **SBERT to verified final topic artifact** — docs_machine_learning_social_nlp_multilingual_sbert_encoder, docs_machine_learning_social_nlp_umap_projection, docs_machine_learning_social_nlp_dbscan_euclidean_density_clustering, docs_machine_learning_social_nlp_weighted_ward_topic_reduction, docs_machine_learning_social_nlp_c_tf_idf_topic_terms, docs_machine_learning_social_nlp_beesense_sentence_clusters_2 [EXTRACTED 1.00]
- **Persistent session access lifecycle** — docs_crawler_twitter_crawler_persistent_scweet_worker, docs_crawler_twitter_crawler_persistent_account_state, docs_crawler_twitter_crawler_pool_cooldown_wait, docs_crawler_twitter_crawler_terminal_access_barriers, docs_crawler_twitter_crawler_network_pacing_and_root_cache [EXTRACTED 1.00]
- **Integrated Twitter acquisition** — docs_crawler_social_crawler_socialcrawler, docs_crawler_twitter_crawler_twittercoordinatorworker, docs_crawler_twitter_crawler_persistent_scweet_worker, docs_crawler_twitter_crawler_native_x_identity, docs_crawler_twitter_crawler_beesense_audit_bundle [EXTRACTED 1.00]
- **End to end verified social pipeline** — readme_socialcrawler, docs_crawler_twitter_acquisition_20261102_combined_social_workbook_20261102, docs_machine_learning_twitter_retrain_20261102_socialnlpclusterer, docs_machine_learning_twitter_retrain_20261102_twitter_model_artifact_manifest, graphify_out_obsidian_arsitektur_beesense_socialnlpstreamlitapp [EXTRACTED 1.00]
- **Semantic clustering and evaluation flow** — docs_machine_learning_twitter_retrain_20261102_multilingual_sbert, docs_machine_learning_twitter_retrain_20261102_dual_seed_umap, docs_machine_learning_twitter_retrain_20261102_dbscan, docs_machine_learning_twitter_retrain_20261102_sentence_weighted_ward_reduction, graphify_out_obsidian_metodologi_machine_learning_social_nlp_coherence_c_v_evaluation_protocol, graphify_out_obsidian_metodologi_machine_learning_social_nlp_candidate_scoring_and_selection [EXTRACTED 1.00]
- **Crawler product specification and acceptance** — prd_prd_frontend_prd_frontend_crawler_crawler_product_requirements, prd_prd_frontend_rancangan_layar_crawler_crawler_screen_design, prd_prd_frontend_acceptance_criteria_crawler_crawler_acceptance_criteria [EXTRACTED 1.00]
- **Shared social export contract across crawler backends** — docs_crawler_instagram_crawler_shared_social_export_contract, docs_crawler_instaloader_crawler_instaloader_crawler, docs_crawler_reddit_crawler_reddrix_reddit_crawler, docs_crawler_instagram_crawler_persistent_chrome_worker [EXTRACTED 1.00]
- **Supported Monthly Topic Direction** — docs_machine_learning_explainable_topics_supported_descriptive_trends, docs_machine_learning_explainable_topics_theil_sen, docs_machine_learning_explainable_topics_kendall_tau_b [EXTRACTED 1.00]
- **Verified standalone trial06 GraphQL and comment path** — docs_crawler_instaloader_crawler_runtime_graphql_patch, docs_crawler_instaloader_crawler_same_context_tokens, docs_crawler_instaloader_crawler_persistent_worker_deadline, docs_crawler_instaloader_crawler_legacy_comment_nodeiterator, docs_crawler_instaloader_crawler_trial06_verified_outcome [EXTRACTED 1.00]
- **Stoppedacquisition→auditedfinalcorpus→verified20topics→contextualGeminiCSV** — docs_crawler_instagram_pipeline_20261030_acquisition_user_stop, docs_crawler_instagram_pipeline_20261030_final_native_identity_corpus, docs_crawler_instagram_pipeline_20261030_final_verified_model, docs_crawler_instagram_pipeline_20261030_actual_contextual_gemini_csv [EXTRACTED 1.00]
- **Verified synthetic React delivery remains separate from proposed production worker/API acceptance** — crawler_frontend_readme_react_crawler_implementation, crawler_frontend_docs_delivery_verified_frontend_checks, crawler_frontend_docs_delivery_synthetic_demo_limitations, crawler_frontend_docs_api_contract_expected_api_contract, prd_prd_backend_readme_persistent_acquisition_worker, prd_prd_frontend_acceptance_criteria_crawler_production_acceptance_gates [INFERRED 0.95]

## Communities (130 total, 33 thin omitted)

### Community 0 - "Panduan Pipeline BeeSense"
Cohesion: 0.05
Nodes (75): TwitterCoordinatorWorker, Accessible dashboard interactions, Counting units and topic share, Dashboard BeeSense, Dashboard validation, Filters preserve full-model memberships and scores, Five dashboard views, SocialNLPStreamlitApp (Dashboard/app.py) (+67 more)

### Community 1 - "Pengambilan HTML Reddit"
Cohesion: 0.06
Nodes (45): browser_configuration(), browser_script(), InstagramBrowserWorker, Serial Chrome acquisition using a persistent profile and manual login.  The same, collect(), create_client(), error_receipt(), instagram_worker() (+37 more)

### Community 2 - "Worker Instaloader"
Cohesion: 0.06
Nodes (41): apply_browser_patch(), browser_graphql_query(), _check(), _cookie(), _hints(), _load_tokens(), main(), _pace() (+33 more)

### Community 3 - "Integrasi X dan Provenans Akuisisi"
Cohesion: 0.06
Nodes (42): _config(), _keywords(), normalize_reddrix_item(), _number(), Map Reddrix 1.2.14 dictionaries without inventing identity or dates., Virtual displays require Linux and Xvfb; other environments use headless., resolve_reddrix_display(), _url() (+34 more)

### Community 4 - "Crawler Selenium"
Cohesion: 0.07
Nodes (20): _barrier(), _create_driver(), main(), Content quoting an error is never used to classify an access barrier., Convert the shared rendered DOM capture without inventing identities., One browser operation. The parent enforces the hard process deadline., Stream evidence before completion; the original supervisor can retain it., Drop-in SocialCrawler with Selenium for both platforms and shared exports. (+12 more)

### Community 5 - "Akuisisi YouTube"
Cohesion: 0.09
Nodes (34): error_code(), load_settings(), main(), parser(), run(), SafeLogger, Settings, video_url() (+26 more)

### Community 6 - "Penyaringan Relevansi dan Narasi Topik"
Cohesion: 0.07
Nodes (60): beesense-context-relevance:1, config/context_relevance.json, config/dashboard.json, ContextRelevanceFilter (MachineLearning/context_relevance.py), Cosine thresholds and context gates, Explicit Gemini authorization, Explicit relevance_artifact opt-in, Filtered clustering: 20 topics, mean c_v 0.4733391691 (+52 more)

### Community 7 - "Penggabungan Dataset"
Cohesion: 0.07
Nodes (41): Active artifacts outputs/nlp_20261030_instagram_topics20_02, Configured33034-record final merged workbook, Active20-topic Instagram-inclusive model configuration, Configured c_v threshold 0.4 with topn 10 and window 110, Current active Gemini enabled; historical disabled state retained, Final Instagram-inclusive20-topic/Gemini configuration, Verified model configuration enables contextual Gemini CSV, Active20-topic Instagram-inclusive model configuration (+33 more)

### Community 8 - "Riwayat Sesi Instagram"
Cohesion: 0.07
Nodes (47): Standalone browser1800-second preset, updated bounded retry, Local session path and explicit360-second/3-retry policy, Instagram-only configured1800-second acquisition budget, instagramDocumentPayload(), instagramNavigate(), instagramRetryAfter(), instagramSourceRateLimit(), Bounded hashtag discovery with authoritative local root filters (+39 more)

### Community 9 - "Penjadwalan dan Riwayat Akuisisi"
Cohesion: 0.07
Nodes (46): Per-platform bounds: max_posts 4000, max_candidates 6000, Main root reddrix.display_mode=auto, Historical exclusion source outputs/social_20261028_01, Configured global acquisition budget 10800 seconds, Retained Playwright-only CAPTCHA fields:600-second wait and five-second poll, Configured Reddit policy cooldown:360seconds, Configured Reddit retry cap:threeperrun, Current main configuration: platforms.reddit.enabled=true (+38 more)

### Community 10 - "Penyaringan Relevansi dan Narasi Topik"
Cohesion: 0.08
Nodes (17): Keep original audit data intact; escape spreadsheet formulas on export., relevance_csv(), checksum(), ContextRelevanceFilter, digest(), Local, auditable zero-shot relevance decisions before topic clustering.  Model s, Units contain target ``sentence`` and optional audited parent/post text., Resolve roots from native URLs; never match conversations by title. (+9 more)

### Community 11 - "Pengujian Client Instagram"
Cohesion: 0.07
Nodes (7): Clock, FakeClient, InstagramCrawlerTests, Offline contract/deadline tests; fixture data is always marked synthetic., records(), spawn_fixture(), spawn_hanging()

### Community 12 - "Pengujian Koordinator Crawler"
Cohesion: 0.15
Nodes (5): rd_events(), receipt(), SocialCrawlerTests, spawn_youtube_fixture(), yt_events()

### Community 13 - "Koordinator Backend Sosial"
Cohesion: 0.10
Nodes (5): SocialExportMixin, Compose platform workers with one configuration, scheduler and export bundle., SocialCrawler, Clock, InstagramIntegrationTests

### Community 14 - "Validasi Konfigurasi Frontend"
Cohesion: 0.10
Nodes (32): ConfigReview(), advance(), cap, committed, dataset(), get(), load(), plans (+24 more)

### Community 15 - "Form Akuisisi dan Survei"
Cohesion: 0.12
Nodes (27): Automatic(), Baselines(), ConfigFields(), Manual(), ManualUrl(), labels, sample, Survey() (+19 more)

### Community 16 - "Model dan Pengujian NLP"
Cohesion: 0.13
Nodes (5): Encode with SBERT, fit UMAP + DBSCAN and optionally merge to a topic count., SocialNLPClusterer, encoder(), fixture(), NLPTests

### Community 17 - "Integrasi X dan Provenans Akuisisi"
Cohesion: 0.08
Nodes (5): hanging_worker(), persistent_worker(), Offline contracts for Twitter/X acquisition; no live credentials required., tweet(), TwitterCrawlerTests

### Community 18 - "Monitor Job dan Dataset"
Cohesion: 0.20
Nodes (24): Shell(), DatasetView(), History(), Composition(), JobDetail(), liveStates, PlatformCard(), ProgressChart() (+16 more)

### Community 19 - "Pengujian Parser Reddit"
Cohesion: 0.21
Nodes (9): assert_accessible(), content_node(), first(), fixture_page(), RedditHtmlParser, RedditTests, rendered_text(), source_time() (+1 more)

### Community 20 - "Kontrak Record Reddit"
Cohesion: 0.16
Nodes (16): _configuration(), _integer(), ContentInput, KeywordMatcher, native_fullname(), object_key(), Aho-Corasick; offsets refer to Python Unicode code points in source., Only public HTML pages on the canonical host; never auth/API routes. (+8 more)

### Community 21 - "Parsing Identitas Reddit"
Cohesion: 0.13
Nodes (17): bounded_events(), HtmlPage, HtmlSource, load_settings(), LocalHtmlSource, now_iso(), parsed_number(), PublicHtmlSource (+9 more)

### Community 22 - "Konfigurasi TypeScript"
Cohesion: 0.07
Nodes (26): compilerOptions, allowImportingTsExtensions, esModuleInterop, isolatedModules, jsx, lib, module, moduleResolution (+18 more)

### Community 23 - "Pengujian Worker Instaloader"
Cohesion: 0.13
Nodes (5): fixture_post(), hanging_fixture(), InstaloaderCrawlerTests, persistent_fixture(), Offline contracts for the separate Instaloader experiment.

### Community 24 - "Tipe dan Client API"
Cohesion: 0.10
Nodes (20): ApiError, base, httpApi, post(), request(), Baseline, Config, Counts (+12 more)

### Community 25 - "Encoding dan Penyimpanan Model"
Cohesion: 0.13
Nodes (6): Use the same class TF-IDF vocabulary for selection and publication., Macro c_v on ALL non-noise topics and a fixed full-corpus reference.          Un, Reuse immutable SBERT features only after verifying data/model identity., Preserve explicit zero distances, including identical sentence vectors., Merge entire DBSCAN groups using sentence-weighted Ward linkage.          Minimi, Select DBSCAN parameters on UMAP; evaluate in original SBERT geometry.

### Community 26 - "Kontrak Record Reddit"
Cohesion: 0.16
Nodes (13): BundleSink, dumps(), main(), parser(), Validate the embedded contract; an external descriptor is optional., Atomic new directory; streaming JSONL + streaming, formula-safe Excel., run(), run_self_tests() (+5 more)

### Community 27 - "Worker Reddrix"
Cohesion: 0.14
Nodes (12): collect_reddrix(), Reddrix anti-bot exceptions do not expose an authoritative HTTP status., Spawn boundary retains streamed records when the hard deadline expires., reddrix_error_receipt(), reddrix_receipt(), reddrix_version(), reddrix_worker(), run_reddrix_worker() (+4 more)

### Community 28 - "Kontrak API Frontend"
Cohesion: 0.10
Nodes (24): Server history pagination, SSE, templates and organizational login remain future, Project-prefixed cookie-session API requires server CORS/CSRF/access controls, Expected typed frontend API contract; backend implementation pending, locatorKey is normalized permalink identity;nativeId may await backend verification, Increasing snapshotVersion and server-owned actions drive reconciliation, Safe structured errors distinguish API429 from worker-platform429, Survey commit binds review to session/project and revalidates conflicts, Typed plan/job requests bind plan IDs, idempotency and safe stop (+16 more)

### Community 29 - "Persyaratan Produk Crawler"
Cohesion: 0.18
Nodes (23): Atomic survey review and idempotent commit, Expected Crawler API contract, NLP schema eligibility gate, Seven-platform capability gating, Server-owned acquisition job lifecycle, Crawler frontend delivery and UX audit, Frontend verification evidence: 50 tests and container checks, BeeSense Crawler React frontend (+15 more)

### Community 30 - "Pengujian Narasi Gemini"
Cohesion: 0.16
Nodes (7): file_hash(), enrich_run(), main(), Add Gemini descriptions to a verified fitted run, preserving its clustering., Publish a new atomic bundle; never overwrite or refit the source run., GeminiArtifactTests, A visibly synthetic fixture exercising the saved-bundle path.

### Community 31 - "Integrasi Default Instaloader"
Cohesion: 0.20
Nodes (22): Diagnostic and active-data separation, Diagnostic trial deduplication, Instaloader Docker artifact awaiting runtime verification, Standalone experiment caps, InstaloaderCrawler guide and evidence, Historical Instagram resume preset preserved, Historical trials 01–05, InstaloaderCrawler (+14 more)

### Community 32 - "Kontrak Record Reddit"
Cohesion: 0.17
Nodes (6): add_readme(), ContractTests, Dataset, digest(), Shared pipeline; adapters cannot choose their own headers or cell formats., validate_row()

### Community 33 - "Dependency Pengembangan Frontend"
Cohesion: 0.10
Nodes (21): devDependencies, eslint, @eslint/js, jsdom, prettier, @testing-library/user-event, @types/react, @types/react-dom (+13 more)

### Community 34 - "Batas Akuisisi Reddit"
Cohesion: 0.13
Nodes (21): Installed Reddrix 1.2.14 and Camoufox 156 browser evidence, Preserved compact SocialCrawler workbook, Historical trial 01 ended PARTIAL with zero posts, Hard-deadline subprocess retains streamed records, BeeSense interoperation delay differs from library request retries, Historical v1.0.0 module-specific non-Linux Xvfb shim, No database/model/persistent-contract migration, Adaptive display implemented after trial with no new crawl (+13 more)

### Community 35 - "Akuisisi YouTube"
Cohesion: 0.19
Nodes (17): build_prompt(), canonical(), digest(), generate(), load_key(), Gemini narratives grounded in ranked topic keywords and representative sentences, Up to ten unique fitted sentences, cosine rank descending, stable ID ties., One request per topic; restart uses source/prompt/keyword-bound local receipts. (+9 more)

### Community 36 - "Penggabungan Dataset"
Cohesion: 0.10
Nodes (3): NativeDatasetTests, PublishedDataTests, PublishedRelevanceTests

### Community 37 - "Capture Reddit Playwright"
Cohesion: 0.21
Nodes (12): atomic_json(), barrier_status(), campaign_plan(), find_cli(), PlaywrightCLI, rate_limit_seconds(), run(), save_capture() (+4 more)

### Community 38 - "Struktur DOM Reddit"
Cohesion: 0.13
Nodes (9): BoundedDom, MemorySink, Node, Small serialised-DOM reader, not a browser or full HTML5 repair engine., RestrictedRedirect, SourceFailure, Exception, HTMLParser (+1 more)

### Community 39 - "Wrapper RedditCrawler"
Cohesion: 0.17
Nodes (5): main(), Reddit-only compatibility entry point for the integrated SocialCrawler Reddrix b, Run only Reddit through the shared Reddrix implementation in SocialCrawler., RedditCrawler, RedditCrawlerTests

### Community 41 - "Pengujian Penjelasan Topik"
Cohesion: 0.25
Nodes (3): ExplanationTests, model_from_counts(), profile()

### Community 42 - "Batas Integrasi Produksi"
Cohesion: 0.13
Nodes (17): Final style samples:96desktop/78narrow444px elements,all black and≥13 px, React frontend and simulation verified; production acquisition integration unavailable, Implemented UI flows:automatic/manual, monitor, survey and dataset review, Applied UX fixes:linked errors, step validation, deep links, drawer focus and inertness, Browser actual widths400/444px;requested360px remains unproven, Production release waits for API/worker/access/export and survey adapter integration, Late plan, URL and survey validation is ignored after input changes, Demo IDs, baseline data and downloads are synthetic rather than acquisition evidence (+9 more)

### Community 43 - "Dependency Runtime Frontend"
Cohesion: 0.12
Nodes (17): dependencies, @fontsource-variable/plus-jakarta-sans, lucide-react, papaparse, react, react-dom, react-router-dom, @tanstack/react-query (+9 more)

### Community 44 - "thread_url"
Cohesion: 0.15
Nodes (5): Read-only exploration of completed NLP runs; no training on page reruns., Count evidence in the filter, keeping sentences/comments/parents distinct., SocialNLPStreamlitApp, Historical 28 October 2026 coherence retrain: 52 topics, c_v 0.40970330118194137, Historical fixed top10/window110/all15878-unique macro c_v protocol

### Community 45 - "topic_sentence_export.py"
Cohesion: 0.20
Nodes (10): json_write(), main(), Start the local relevance experiment, or its preserved baseline snapshot., export_payload(), main(), Prepare an original-sentence export and seal it into a new NLP snapshot., Keep original variants; remove repeated occurrences of the same text., Verify every Excel membership before publishing the complete snapshot. (+2 more)

### Community 46 - "app.py"
Cohesion: 0.19
Nodes (13): Root Docker context allowlist for relocated dashboard runtime, _explain_filtered(), _load_artifacts(), main(), Streamlit entry point for local and Community Cloud dashboards.  Training lives, Dashboard build context includes root shim and artifact-reader packages, Relocated dashboard image uses root Streamlit shim and runtime-only wheels, Obsidian Cloud runbook: streamlit_apps.py, Python 3.12 and complete artifact publication (+5 more)

### Community 47 - "Batas Akuisisi Reddit"
Cohesion: 0.16
Nodes (16): Read-only historical baseline exclusion, Configured 360-second policy and three HTTP 429 retries, Original date boundary and university-topic query scope, Tracked reddrix.display_mode=auto, Configured root/comment/candidate/time budgets, Configured new sorting differs from Reddrix capability, Trial config now explicitly selects Reddrix; wrapper preserves legacy compatibility, Tracked Reddit trial configuration (+8 more)

### Community 50 - "Rencana Produk dan Survei"
Cohesion: 0.14
Nodes (15): Curated two-menu contract with URL/Survey under Manual, Curated immutable dataset selection does not train or change Dashboard, Curated Crawler PRD status:frontend implemented, backend pending, New survey schema must preserve role, question, response, version and permission, Backend PRD is not written; API/worker services remain proposed, Proposed persistent Python worker and authorized CAPTCHA browser bridge, Proposed server session, role, project isolation and idempotency, Proposed survey transactions, immutable datasets and operational audit (+7 more)

### Community 52 - "Wrapper RedditCrawler"
Cohesion: 0.19
Nodes (4): FakeReddrix, item(), Reddrix field/identity boundaries and the real, shared Excel exporter., records()

### Community 53 - "Pengujian Narasi Gemini"
Cohesion: 0.27
Nodes (3): GeminiTests, response(), topic()

### Community 54 - "Kampanye Browser Reddit"
Cohesion: 0.27
Nodes (8): classifyCaptureFailure(), enrichBatch(), rateLimitSeconds(), inWindow(), mergeCandidates(), row, source, window

### Community 55 - "Panduan Pipeline BeeSense"
Cohesion: 0.17
Nodes (13): Shared rendered_thread_dom.mjs extraction, Relative dates remain calendar estimates, Historical Selenium implementation preset:500roots/platform andonehour, Worker hard deadline preserves streamed partial events, Inherited SocialCrawler filters and Excel exporters, Separate non-root crawler container with Selenium Grid, Fresh Chrome guest session per operation, Official Selenium Manager ChromeDriver selection (+5 more)

### Community 56 - "Alur Dataset Model Dashboard"
Cohesion: 0.22
Nodes (13): InstagramCrawler browser and instagrapi history, Explicit instagrapi backend, Persistent Chrome worker with manual login, Shared compact and eight-sheet social export contract, Stored Indonesian Gemini topic narratives, Instagram acquisition, dataset and training pipeline, Random pacing, batch pauses and exponential 429 backoff, Native-ID deduplication and latest-observation lineage (+5 more)

### Community 57 - "Integrasi X dan Provenans Akuisisi"
Cohesion: 0.26
Nodes (13): Combined social workbook 20261102, Global native X identity, Merged record lineage contract, native_roots.json, Twitter acquisition report 2 November 2026, Comment sentence eligibility, Stored artifact Twitter dashboard, topic_sentences.xlsx (+5 more)

### Community 58 - "Alur Dataset Model Dashboard"
Cohesion: 0.19
Nodes (13): Artifact-only dashboard without Gensim/Torch imports, Obsidian runbook records Python 3.14 failure and dashboard-only packaging fix, BeeSense startup, verification and coherence training runbook, New-corpus native SBERT encoding or exact verified cache reuse, Package module CLIs retain repository-root path semantics, Crawler, MachineLearning and Dashboard packages with grouped supporting folders, Reorganized BeeSense package and supporting-file structure, Training/evaluation-only Gensim coherence requirements (+5 more)

### Community 59 - "Model dan Pengujian NLP"
Cohesion: 0.15
Nodes (4): Identify the parent thread, not the individual comment URL., Extract real sentences using relevance plus MMR diversity., Evidence-grounded topic descriptions and descriptive, source-aware trends., Rule-based segmentation preserving exact offsets in the original text.

### Community 61 - "Alur Dataset Model Dashboard"
Cohesion: 0.18
Nodes (12): Dashboard Python 3.12 and 3.14 runtime matrix, Offline crawler and NLP regression tests, Verify BeeSense CI, Synthetic Reddit post, comment and reply fixture, Reddit browser campaign helpers, User checkpoint audit export and verification, Manual CAPTCHA recovery within global deadline, Reddit Playwright runner (+4 more)

### Community 62 - "Koordinator Backend Sosial"
Cohesion: 0.17
Nodes (6): main(), Validate and return the effective plan without browser/network access., Re-export saved Contents without network or modifying the source bundle., Describe the acquisition backend independently of the shared export., Return an explicit target/shortfall report and write one atomic bundle., Read roots and all global X IDs; never alter historical workbooks.

### Community 64 - "Integrasi X dan Provenans Akuisisi"
Cohesion: 0.23
Nodes (12): Credential and state isolation, Native parent preservation, Network pacing and root cache, Persistent account state, Persistent Scweet worker, Pool cooldown wait, Scweet 5.8.2, Terminal access barriers (+4 more)

### Community 65 - "Integrasi X dan Provenans Akuisisi"
Cohesion: 0.21
Nodes (12): DBSCAN, Dual seed UMAP, Internal evaluation interpretation limits, Sentence preparation provenance, Sentence weighted Ward reduction, SocialNLPClusterer, Verified Twitter twenty topic fit, MMR diverse source evidence (+4 more)

### Community 66 - "Operasi dan Verifikasi BeeSense"
Cohesion: 0.17
Nodes (12): Multilingual SBERT, BeeSense project structure, Ignored local authentication and browser state, Legacy Instagram browser isolation, Package rooted path consistency, Separate training and test environments, SocialExportMixin, topic_narratives.py (+4 more)

### Community 67 - "Pengujian Narasi Gemini"
Cohesion: 0.24
Nodes (11): main(), published_crawl_files(), published_relevance_files(), published_source_files(), Verify published source workbooks and the dashboard artifact bundle., Bind a separately published relevance dataset to the active fitted mask., Verify record identity independently of sentence-text deduplication., A merge report binds its small, explicit audit sidecars to the input. (+3 more)

### Community 68 - "Skrip Build Frontend"
Cohesion: 0.18
Nodes (11): scripts, build, build:demo, check, dev, format, format:check, lint (+3 more)

### Community 69 - "Batas Akuisisi Reddit"
Cohesion: 0.24
Nodes (11): Relocated combined crawler image runs package module as UID10001, Adaptive display v1.1.0 auto platform policy, Actual macOS lifecycle test versus mocked Linux display matrix, CLI/class display overrides and explicit virtual preconditions, Requested/effective display mode is visible in plan and source metadata, Reddrix Docker image unbuilt: local daemon unavailable, Reddrix-only Camoufox factory controls initial and refreshed sessions, Curated adaptive display and isolated factory architecture (+3 more)

### Community 70 - "thread_url"
Cohesion: 0.20
Nodes (4): _graph_positions(), Bounded topic graph: volume from filtered rows, semantic edges from the full mod, Keep the full-model layout stable while volume and edge filters change., DashboardTests

### Community 71 - "Panduan Pipeline BeeSense"
Cohesion: 0.24
Nodes (10): Selenium Rendered DOM, Gensim Coherence Environment, Combined Crawler Environment, Offline Regression and Crawler Environment, Instagram Chrome Worker Environment, Instaloader 4.16 Environment, General NLP Environment, Isolated Reddrix Environment (+2 more)

### Community 72 - "Panduan Pipeline BeeSense"
Cohesion: 0.29
Nodes (10): Instaloader 4.16, Platform rate limit policies, Reddrix 1.2.14, Round robin deadline scheduler, Shared root and comment filters, SocialCrawler, SocialExportMixin, BeeSense audit bundle (+2 more)

### Community 73 - "Integrasi X dan Provenans Akuisisi"
Cohesion: 0.29
Nodes (10): Daily request cap overshoot, Deadline bounded pool cooldown, Deadline preserving checkpoint resume, Five batch BeeSense audit outputs, Observed Twitter HTTP telemetry, Scweet, Scweet rate limiting documentation, Twenty five query parity (+2 more)

### Community 74 - "build_topic_sentences.mjs"
Cohesion: 0.22
Nodes (6): body, payload, [payloadPath, outputPath, previewDir], sentences, topics, workbook

### Community 75 - "Integrasi X dan Provenans Akuisisi"
Cohesion: 0.25
Nodes (8): Query pendidikan Indonesia jendela tujuh hari, Preset percobaan Twitter 30 menit, Jeda 5 dan 15 detik limiter window per operasi dan cap harian 120, 1.800 detik target 1.000 post 10 balasan, Allowlist Docker tanpa auth dan sesi, Image Twitter Python 3.12 UID 10001, openpyxl 3.1.5, Scweet 5.8.2

### Community 76 - "Router dan Batas Error"
Cohesion: 0.25
Nodes (3): client, ErrorBoundary, router

### Community 77 - "Panduan Pipeline BeeSense"
Cohesion: 0.25
Nodes (8): Baseline identity exclusion, Social campaign 29 October 2026, Social crawler guide, merge_social_datasets, native_roots.json, Native X identity, Twitter crawler guide, Verified conversation root provenance

### Community 78 - "Encoding dan Penyimpanan Model"
Cohesion: 0.25
Nodes (4): main(), Explain already verified artifacts without encoding or fitting again., Publish a new versioned sidecar; never modify the original run., Derive Indonesian Gemini labels after topic count and coherence pass.

### Community 79 - "Panduan Pipeline BeeSense"
Cohesion: 0.29
Nodes (7): Advanced connected-browser Reddit campaign helpers, Checkpoint export to the eight-sheet contract, Native-ID provenance and bounded public excerpts, Standalone runner stops 429; coordinator 1.3 supports bounded cooldown, Isolated Chrome profile, manual CAPTCHA wait and access-barrier stops, Coordinator waits for manual CAPTCHA without automated clicks, Reddit Playwright CLI runner

### Community 80 - "Metadata Package Frontend"
Cohesion: 0.29
Nodes (6): engines, node, name, private, type, version

### Community 81 - "Operasi dan Verifikasi BeeSense"
Cohesion: 0.29
Nodes (7): Dataset Dashboard note, Historical earlier snapshot 30 October 2026, Historical Instagram 500 snapshot 30 October 2026, Historical merged snapshot 29 October 2026, Original baseline preservation, Historical Gemini publication 30 October 2026, Topik Gemini note

### Community 82 - "Integrasi X dan Provenans Akuisisi"
Cohesion: 0.33
Nodes (6): 2 November 2026 pipeline integration, 31 October 2026 historical evidence, SocialNLPClusterer, thread_root_key, TwitterCrawler Scweet architecture, Workbook bound root sidecar

### Community 83 - "Pengujian Alur Frontend"
Cohesion: 0.40
Nodes (3): AppContext, demoApi, UrlReview

### Community 84 - "Operasi dan Verifikasi BeeSense"
Cohesion: 0.50
Nodes (5): beesense-topic-id:2, Gemini 3.5 Flash Lite, topic_narratives.csv, Narrative CSV schema compatibility, Narrative evidence validation

### Community 85 - "Operasi dan Verifikasi BeeSense"
Cohesion: 0.50
Nodes (5): Twenty topic mean coherence publication gate, Candidate scoring and selection, Coherence c_v evaluation protocol, Gensim CoherenceModel reference, Historical baseline coherence snapshots

### Community 86 - "Q: ok sekarang training ulang menggunakan /Users/sakaheroji/Documents/BeeSense/outputs/social_20261030_combined_instagram_500_2h_02/social_data.xlsx, clustering. Buat 20 topik dengan coherence minimal 0.4. Lalu buat excel baru dengan tabel dengan kolom: topik, kalimat yang berada dalam cluster topik. lalu model digunakan kembali di dashboard streamlit yang di rebuild ulang, dan di commit dan dipush semuanya ke githubnya untuk di deploy ulang"
Cohesion: 0.40
Nodes (4): Answer, Outcome, Q: ok sekarang training ulang menggunakan /Users/sakaheroji/Documents/BeeSense/outputs/social_20261030_combined_instagram_500_2h_02/social_data.xlsx, clustering. Buat 20 topik dengan coherence minimal 0.4. Lalu buat excel baru dengan tabel dengan kolom: topik, kalimat yang berada dalam cluster topik. lalu model digunakan kembali di dashboard streamlit yang di rebuild ulang, dan di commit dan dipush semuanya ke githubnya untuk di deploy ulang, Source Nodes

### Community 87 - "Parsing Identitas Reddit"
Cohesion: 0.50
Nodes (3): RedditAdapter, RedditRecordFactory, Verified Reddit native identity and parent/root relationships

### Community 89 - "Format Kode Frontend"
Cohesion: 0.50
Nodes (3): printWidth, singleQuote, trailingComma

### Community 90 - "Operasi dan Verifikasi BeeSense"
Cohesion: 0.50
Nodes (4): BeeSense architecture note, Dashboard URL state binding, Extracted evidence and inferred cosine edges, SocialNLPStreamlitApp

### Community 92 - "CI Container Frontend"
Cohesion: 0.67
Nodes (3): SPA container health and deep-link checks, Crawler frontend CI, BeeSense Crawler SPA document

### Community 94 - "Batas Akuisisi Reddit"
Cohesion: 0.67
Nodes (3): Relocated Selenium image preserves included requirements and package modules, Isolated local environment and separately downloaded browser, Isolated Reddrix 1.2.14 crawler dependency pins

## Knowledge Gaps
- **203 isolated node(s):** `window`, `source`, `row`, `candidate`, `singleQuote` (+198 more)
  These have ≤1 connection - possible missing edges or undocumented components.
- **33 thin communities (<3 nodes) omitted from report** — run `graphify query` to explore isolated nodes.

## Suggested Questions
_Questions this graph is uniquely positioned to answer:_

- **Bagaimana konteks terverifikasi menyaring kalimat sebelum clustering, lalu Gemini menjelaskan 20 topik tanpa mengubah cluster?**
  _Keputusan relevansi, parent native, embedding subset terverifikasi, gate coherence, CSV Gemini dan pembandingan snapshot lokal terhubung._
- **Why does `SocialCrawler` connect `Koordinator Backend Sosial` to `Batas Akuisisi Reddit`, `Integrasi X dan Provenans Akuisisi`, `Crawler Selenium`, `Batas Akuisisi Reddit`, `Worker Instaloader`, `Wrapper RedditCrawler`, `Panduan Pipeline BeeSense`, `Penjadwalan dan Riwayat Akuisisi`, `Pengujian Client Instagram`, `Pengujian Koordinator Crawler`, `Panduan Pipeline BeeSense`, `Integrasi X dan Provenans Akuisisi`, `Wrapper RedditCrawler`, `Panduan Pipeline BeeSense`, `Parsing Identitas Reddit`, `Alur Dataset Model Dashboard`, `Worker Reddrix`, `Koordinator Backend Sosial`?**
  _High betweenness centrality (0.325) - this node is a cross-community bridge._
- **Why does `SocialNLPClusterer` connect `Model dan Pengujian NLP` to `Pengujian Narasi Gemini`, `thread_url`, `Penggabungan Dataset`, `Penjadwalan dan Riwayat Akuisisi`, `Penyaringan Relevansi dan Narasi Topik`, `Model dan Pengujian NLP`, `thread_url`, `topic_sentence_export.py`, `Encoding dan Penyimpanan Model`, `Pengujian Penjelasan Topik`, `Integrasi X dan Provenans Akuisisi`, `Pengujian UI Streamlit`, `Pengujian Narasi Gemini`, `Encoding dan Penyimpanan Model`, `Alur Dataset Model Dashboard`, `Model dan Pengujian NLP`, `Pengujian Narasi Gemini`?**
  _High betweenness centrality (0.206) - this node is a cross-community bridge._
- **Why does `BeeSense startup, verification and coherence training runbook` connect `Alur Dataset Model Dashboard` to `Penjadwalan dan Riwayat Akuisisi`, `Alur Dataset Model Dashboard`, `app.py`?**
  _High betweenness centrality (0.111) - this node is a cross-community bridge._
- **Are the 18 inferred relationships involving `SocialNLPClusterer` (e.g. with `LocalSemanticBackend` and `ContextRelevanceFilter`) actually correct?**
  _`SocialNLPClusterer` has 18 INFERRED edges - model-reasoned connections that need verification._
- **Are the 21 inferred relationships involving `SocialCrawler` (e.g. with `RedditCrawler` and `_SeleniumSource`) actually correct?**
  _`SocialCrawler` has 21 INFERRED edges - model-reasoned connections that need verification._
- **Are the 51 inferred relationships involving `ValueError` (e.g. with `browser_configuration()` and `instaloader_options()`) actually correct?**
  _`ValueError` has 51 INFERRED edges - model-reasoned connections that need verification._
- **What connects `window`, `source`, `row` to the rest of the system?**
  _203 weakly-connected nodes found - possible documentation gaps or missing edges._
## Floor plan dan perbaikan pembandingan Cloud — 2 November 2026

Scoped incremental extraction retains untouched graph sources. The listed commit is the baseline of this modified working tree. Auth, private SQLite, model arrays and acquired raw text are excluded from extraction. Curated Obsidian notes are explicit semantic inputs.

This incremental update documents the local floorplan and the verified Streamlit before/after comparison. Generated floorplan files, raw acquired text, auth, and model arrays are excluded from graph extraction. Floorplan is local and git-ignored. All 139 selected files have Indonesian descriptions; 3 guided flows and a tour were browser-verified. Frontend crawler uses a demo adapter; the Python server endpoints for it are not implemented. No high severity item in the floorplan quick health check; a medium warning identifies six large files. This is not a security audit.

Verification: {"commit": "3987e04909328c0f62be04f3948058d20de3b32b", "previous_delivery_commit": "778cb8120327c4fd436e894bf22dcf4077ec2c89", "both_pushed": true, "streamlit_restarted_and_comparison_verified": true, "before": {"occurrences": 53332, "mean_cv": 0.4243209771786889}, "after": {"occurrences": 10496, "mean_cv": 0.4733391691099718}, "regression_tests": {"dashboard_unit_tests": 12, "minimal_cloud_runtime_tests": 2}, "floorplan": {"files_described": 139, "file_description_coverage": "100%", "unassigned": 0, "guided_flows": 3, "tour_stops": 7, "url": "http://127.0.0.1:4378", "git_ignored": true, "high_severity_health_items": 0, "medium_health_items": 1, "large_files_identified": 6, "browser_verified": true}, "database": "No application database migration required", "docker": {"verified": false, "reason": "Local Docker daemon unavailable", "pending_command": "docker build -f deployment/docker/Dockerfile.dashboard -t beesense-dashboard:local ."}}

Changed-fragment diagnostic warnings: {"dangling_endpoint_edges": 38, "undirected_same_endpoint_collapsed_edges": 1}. AST references outside the scoped fragment may be unresolved here; full exported edge endpoints and hyperedge membership are separately verified. These checks do not establish extraction completeness. Semantic token usage is unknown; numeric cumulative totals exclude unknown usage.
Verified source-replacement reduction audit: {"old_nodes": 2034, "new_nodes": 2062, "removed_from_reextracted_sources": 18, "untouched_nodes_and_edges_preserved": true}
Stale cross-document hyperedges referencing replaced nodes were removed: []. Valid hyperedges were retained; no substitute membership was guessed.

Re-extracted document relationships between retained nodes were replaced: {"count": 1, "sources": ["docs/machine-learning/CONTEXT_RELEVANCE.md"]}. All relationships from untouched source files were retained.
