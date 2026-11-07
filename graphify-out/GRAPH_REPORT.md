# Graph Report - .  (2026-11-07)

## Corpus Check
- 3 files · ~314,493 words
- Verdict: corpus is large enough that graph structure adds value.

## Summary
- 2411 nodes · 5313 edges · 156 communities (118 shown, 38 thin omitted)
- Extraction: 93% EXTRACTED · 7% INFERRED · 0% AMBIGUOUS · INFERRED: 398 edges (avg confidence: 0.66)
- Token cost: 0 input · 0 output

## Community Hubs (Navigation)
- SocialNLPClusterer
- crawl_youtube.py
- SocialCrawlerSelenium
- BeeSense Crawler Frontend PRD
- TransactionMigration.tsx
- ContextRelevanceFilter
- InstagramCrawlerTests
- TikTokTests
- domain.ts
- InstaloaderCrawlerTests
- instagram_crawler.py
- crawl_reddit_playwright.py
- SocialCrawlerTests
- SourceBarrier
- NLPTests
- types.ts
- TwitterCrawlerTests
- tiktok_crawler.py
- file_hash
- SocialCrawler
- .row
- Active TikTokCrawler2.6.1 / NativeTikTokClient / BeeSenseNative1.3.0 with Playwright1.62.0
- read_config
- organize
- .error
- Conversation Parallel Execution Plan
- social_crawler.py
- crawl_reddit_single.py
- compilerOptions
- architecture.json
- twitter_crawler.py
- NativeTikTokClient
- Desain dan verifikasi Sidebar TikTok Connector 1.4.0
- Optimasi YouTube dan Reddit — 6 November 2026
- instaloader_crawler.py
- SocialExportMixin
- demo.ts
- Clock
- worker
- .thread
- manifest.json
- api.ts
- Api
- topic_narratives.py
- ChromeBridgeTests
- PublishedDataTests
- devDependencies
- instaloader_browser_patch.py
- stream
- TwitterCrawler
- Audit dan optimasi X / Instagram — 6 November 2026
- RedditCrawlerTests
- ExplanationTests
- BoundedDom
- background.mjs
- SocialNLPStreamlitApp
- test_unlimited_crawling.py
- scripts
- ConversationWorkspace.tsx
- number
- Panduan output per platform dan tanggal WIB
- AnalysisTests
- Graphify memory: parallel crawling campaign proposal
- Panduan sesi per sosmed — 6 November 2026
- dependencies
- json_write
- StreamlitTests
- TwitterCoordinatorWorker
- ChromeLiveWorker
- core.mjs
- SidePanelTests
- GeminiTests
- InstagramBrowserWorker
- browser_campaign_detail.mjs
- item
- MergeTests
- AuthSettings.tsx
- App.tsx
- .render
- Dashboard BeeSense: verified artifacts, caption source labels and topic evidence
- CommentDomTests
- app.py
- SocialNLPClusterer:SBERT→L2→UMAP→DBSCAN→weightedWard→c-TF-IDF→verified artifacts
- PRD Machine Learning
- InstaloaderWorker
- source_records
- November5TikTok combined retraining:both local fits20topics/mean c_v>=0.4,40authorized Gemini narratives complete,activepair updated
- sidepanel.mjs
- .response
- BeeSense: separate crawler, NLP and artifact-reading Streamlit dashboard
- build_topic_sentences.mjs
- YouTubePerformanceTests
- KeywordMatcher
- BundleSink
- Settings
- benchmark_youtube_reddit.py
- InstaloaderCrawler
- package.json
- .parent_post_key
- ContextRelevanceFilter/LocalSemanticBackend: local pinned-SBERT reference-based occurrence filtering,not human-labeled classifier or per-comment API
- instagram_browser_capture.mjs
- TikTokWorker
- Active native provenance:CLI2.6.1 / NativeTikTokClient / BeeSenseNative1.3.0
- Historical map: before and after relevance-filtered clustering
- Uji backend aktif TikTok-Api 3 November 2026
- TikTok existing-Chrome observation and offline import — 3 November 2026
- SBERT, UMAP, DBSCAN, and c-TF-IDF pipeline
- SPA container health and deep-link verification
- sync-config.mjs
- .topic_figure
- Single config/social_nlp.json for SocialNLPClusterer;five dated presets removed,history retained in summaries
- public_web_post.test.mjs
- NetworkPacing
- Provenance dfreelon/Pyktok — historis
- .prettierrc.json
- InstaloaderCrawler dan patch GraphQL web
- Dua uji live native 3 November 2026 — keduanya gagal target
- Uji TikTok 3 November 2026
- Memori historis delivery X/Instagram dan sidebar TikTok
- test_relevance_runtime.py
- pageOperation
- Provenance PyTok historis, dependency sudah tidak aktif
- BeeSense App Icon
- Shared crawler dependency bundle
- Backend/__init__.py
- .legacy_comments
- Nested Reddit comment hierarchy
- rendered_thread_dom.mjs
- Provenance TikTok-Api langsung — historis
- Youtube/__init__.py
- eslint-plugin-react-hooks
- @testing-library/jest-dom
- @testing-library/user-event
- @types/react
- @types/react-dom
- Crawler/__init__.py
- Dashboard/__init__.py
- Historical migration implementation later corrected
- Memori penjelasan Peta Topik dan TikTok sedang berjalan
- Memori historis delivery panduan sesi frontend
- Independent Instagram Chrome-worker Python environment
- tests/__init__.py
- eslint.config.js
- Community 150
- Community 151
- Community 152
- Community 153
- Community 154

## God Nodes (most connected - your core abstractions)
1. `SocialCrawler` - 121 edges
2. `SocialNLPClusterer` - 116 edges
3. `SocialNLPStreamlitApp` - 49 edges
4. `TikTokTests` - 46 edges
5. `SocialCrawlerTests` - 42 edges
6. `file_hash()` - 35 edges
7. `InstaloaderCrawlerTests` - 35 edges
8. `NativeTikTokClient` - 32 edges
9. `InstagramCrawlerTests` - 32 edges
10. `TwitterCrawlerTests` - 32 edges

## Surprising Connections (you probably didn't know these)
- `Stagnasi native ID 75 detik diperiksa pada batas request` --rationale_for--> `RedditRequestGate`  [INFERRED]
  docs/crawler/PERFORMANCE_YOUTUBE_REDDIT_20261106.md → Crawler/Backend/crawler_network.py
- `Native TikTok dependencies: Playwright 1.62.0 and openpyxl 3.1.5` --conceptually_related_to--> `NativeTikTokClient`  [INFERRED]
  requirements/tiktok.txt → Crawler/Backend/tiktok_crawler.py
- `Hitungan setelah bridge mengakui batch, dedup native ID` --rationale_for--> `flush()`  [INFERRED]
  docs/crawler/TIKTOK_SIDEBAR_20261106.md → Crawler/Backend/Tiktok/chrome_extension/background.mjs
- `Source pagination replaces idle completion` --conceptually_related_to--> `runTask()`  [INFERRED]
  graphify-out/memory/query_20261103_101600_ambil_semua_komentar_tiktok__berhenti_setelah_perb.md → Crawler/Backend/Tiktok/chrome_extension/background.mjs
- `Synthetic counts are not live TikTok results` --conceptually_related_to--> `runTask()`  [INFERRED]
  graphify-out/memory/query_20261105_043203_perbaiki_semua_komentar_tiktok_dan_pilih_comments.md → Crawler/Backend/Tiktok/chrome_extension/background.mjs

## Import Cycles
- None detected.

## Hyperedges (group relationships)
- **Transaction-Owned Publication Range Boundary** — graphify_out_memory_query_20261107_044403_ubah_frontend_conversation__untuk_rentang_publikas_config, graphify_out_memory_query_20261107_044403_ubah_frontend_conversation__untuk_rentang_publikas_platformworkspace, graphify_out_memory_query_20261107_044403_ubah_frontend_conversation__untuk_rentang_publikas_parallelworkspace, graphify_out_memory_query_20261107_044403_ubah_frontend_conversation__untuk_rentang_publikas_applyconversation, graphify_out_memory_query_20261107_044403_ubah_frontend_conversation__untuk_rentang_publikas_frozen_conversation_snapshot [EXTRACTED 1.00]
- **Conversation-First Research Context Flow** — prd_prd_frontend_prd_frontend_crawler_conversation_first_product_model, crawler_frontend_readme_conversation_first_workflow, crawler_frontend_docs_api_contract_conversation_api, crawler_frontend_docs_delivery_conversation_first_delivery, graphify_out_memory_query_20261107_040159_update_frontend_crawler_menjadi_conversation_first_conversationworkspace [INFERRED 0.95]
- **Publication Dates Belong to Crawling Transactions** — crawler_frontend_readme_transaction_publication_range, crawler_frontend_docs_api_contract_transaction_publication_range_contract, crawler_frontend_docs_delivery_transaction_date_correction, prd_prd_frontend_prd_frontend_crawler_research_context_and_operation_separation [INFERRED 0.95]
- **Parallel Execution with Failure and Recovery Isolation** — docs_crawler_plan_conversation_paralel_conversation_runner, docs_crawler_plan_conversation_paralel_per_platform_process_isolation, docs_crawler_plan_conversation_paralel_platform_failure_isolation, docs_crawler_plan_conversation_paralel_checkpoint_and_resume, docs_crawler_plan_conversation_paralel_resource_ownership_lock [EXTRACTED 1.00]
- **Sumber sesi berbeda menurut platform** — crawler_frontend_docs_session_guide_instagram_sessionid, crawler_frontend_docs_session_guide_x_auth_token_alias, crawler_frontend_docs_session_guide_tiktok_chrome_session, crawler_frontend_docs_session_guide_threads_facebook_pending, crawler_frontend_docs_session_guide_youtube_reddit_no_session [EXTRACTED 1.00]
- **Panduan dan hint memakai metadata sesi yang sama** — crawler_frontend_src_shared_sessionguide_sessionguide, crawler_frontend_src_shared_auth_sessioncookies, crawler_frontend_src_shared_authsettings_authsettings, crawler_frontend_src_features_tiktokconnector_tiktokchromepreparation [EXTRACTED 1.00]
- **Penghematan request sambil mempertahankan proteksi akses** — docs_crawler_performance_x_instagram_20261106_calendar_windows, docs_crawler_performance_x_instagram_20261106_root_preflight, docs_crawler_performance_x_instagram_20261106_lazy_replies, docs_crawler_performance_x_instagram_20261106_remaining_cap [EXTRACTED 1.00]
- **Batas request yang mempertahankan progres dan pacing** — docs_crawler_performance_youtube_reddit_20261106_root_preflight, docs_crawler_performance_youtube_reddit_20261106_metadata_only, docs_crawler_performance_youtube_reddit_20261106_serialized_requests, docs_crawler_performance_youtube_reddit_20261106_native_id_stagnation, docs_crawler_performance_youtube_reddit_20261106_latched_barriers [EXTRACTED 1.00]
- **Fixture mempertahankan ID tanpa klaim throughput live** — docs_crawler_performance_youtube_reddit_20261106_youtube_fixture, docs_crawler_performance_youtube_reddit_20261106_reddit_fixture, docs_crawler_performance_youtube_reddit_20261106_timeout_fixture, docs_crawler_performance_youtube_reddit_20261106_offline_validation [EXTRACTED 1.00]
- **Siklus kontrol dan progres sidebar** — crawler_backend_tiktok_chrome_extension_sidepanel_sidebar_ui, docs_crawler_tiktok_sidebar_20261106_connector_session_state, docs_crawler_tiktok_sidebar_20261106_acknowledged_counts [EXTRACTED 1.00]
- **Validasi offline tanpa klaim hasil live** — docs_crawler_tiktok_sidebar_20261106_sidebar_verification, docs_crawler_tiktok_sidebar_20261106_native_api_verification, docs_crawler_tiktok_sidebar_20261106_release_limitations [EXTRACTED 1.00]
- **Audited semantic relevance selection** — docs_machine_learning_proses_penyaringan_kalimat_reference_examples, docs_machine_learning_proses_penyaringan_kalimat_local_semantic_scores, docs_machine_learning_proses_penyaringan_kalimat_threshold_decisions, docs_machine_learning_proses_penyaringan_kalimat_verified_conversation_context, docs_machine_learning_proses_penyaringan_kalimat_occurrence_audit [EXTRACTED 1.00]
- **BeeSense Icon Composition** — crawler_frontend_public_beesense_beesense_app_icon, crawler_frontend_public_beesense_black_isometric_cube_mark, crawler_frontend_public_beesense_orange_rounded_square_background [EXTRACTED 1.00]
- **Frontend CI and SPA verification flow** — _github_workflows_crawler_frontend_verify_crawler_frontend, _github_workflows_crawler_frontend_frontend_quality_gate, _github_workflows_crawler_frontend_spa_container_verification, crawler_frontend_index_crawler_spa_document, crawler_frontend_index_frontend_entry_module [INFERRED 0.95]
- **NLP embedding, clustering, and dashboard lifecycle** — docs_notes_note_sbert_dbscan_note, docs_notes_note_sbert, docs_notes_note_dbscan, graphify_out_memory_query_20261028_153533_update_social_nlp_py_ke_embedding_sbert__umap_sesu_sbert_umap_dbscan_ctfidf_pipeline, graphify_out_memory_query_20261028_132041_jalankan_dashboard_streamlitnya_dashboard_startup_query [INFERRED 0.85]
- **Crawler architecture, optimization, and campaign evolution** — graphify_out_memory_query_20261028_135700_buat_versi_socialcrawler_dalam_file_baru_memakai_s_selenium_architecture_memory, graphify_out_memory_query_20261106_091620_analisa_dan_percepat_crawler_youtube_dan_reddit_de_crawler_performance_memory, graphify_out_memory_query_20261106_091620_analisa_dan_percepat_crawler_youtube_dan_reddit_de_low_risk_crawler_acceleration, graphify_out_memory_query_20261106_094009_brainstorm_satu_perintah_crawling_campaign_dengan_parallel_campaign_proposal, graphify_out_memory_query_20261106_094009_brainstorm_satu_perintah_crawling_campaign_dengan_campaign_runner [INFERRED 0.75]
- **Machine Learning Dataset Handoff Contract** — prd_prd_machine_learning_readme_versioned_dataset_handoff, prd_prd_machine_learning_readme_source_and_role_separation, prd_prd_machine_learning_readme_survey_dataset_contract, prd_prd_machine_learning_readme_social_schema_normalization, prd_prd_machine_learning_readme_corpus_normalization_and_deduplication, prd_prd_machine_learning_readme_training_snapshot_separation [EXTRACTED 1.00]

## Communities (156 total, 38 thin omitted)

### Community 0 - "SocialNLPClusterer"
Cohesion: 0.09
Nodes (37): Exception, SourceBarrier, error_code(), load_settings(), main(), parser(), run(), SafeLogger (+29 more)

### Community 1 - "crawl_youtube.py"
Cohesion: 0.06
Nodes (21): _barrier(), _create_driver(), main(), Content quoting an error is never used to classify an access barrier., Convert the shared rendered DOM capture without inventing identities., One browser operation. The parent enforces the hard process deadline., Stream evidence before completion; the original supervisor can retain it., Drop-in SocialCrawler with Selenium for both platforms and shared exports. (+13 more)

### Community 2 - "SocialCrawlerSelenium"
Cohesion: 0.06
Nodes (53): AuthStatus Contract, Conversation API, ConversationDraft, Conversation Snapshot Contract, Crawling and Dataset API, Frontend Crawler API Contract 1.3, Local Excel Browser Contract, Server-Side Secret Containment (+45 more)

### Community 3 - "BeeSense Crawler Frontend PRD"
Cohesion: 0.08
Nodes (6): comment(), hanging_worker(), source_comment(), source_video(), TikTokTests, video()

### Community 4 - "TransactionMigration.tsx"
Cohesion: 0.08
Nodes (18): Historical relevance results from 2 November 2026, Per-occurrence decisions, source checksums and preserved provenance, Ordered relevance decisions and short-sentence uncertainty gate, Verified root and parent context for short uncertain sentences, checksum(), ContextRelevanceFilter, digest(), Local, auditable zero-shot relevance decisions before topic clustering.  Model s (+10 more)

### Community 5 - "ContextRelevanceFilter"
Cohesion: 0.10
Nodes (6): fixture_post(), hanging_fixture(), InstaloaderCrawlerTests, persistent_fixture(), Offline contracts for the separate Instaloader experiment., server_fault_fixture()

### Community 6 - "InstagramCrawlerTests"
Cohesion: 0.15
Nodes (6): Exercise Instagram through the combined coordinator, without network access., rd_events(), receipt(), SocialCrawlerTests, spawn_youtube_fixture(), yt_events()

### Community 7 - "TikTokTests"
Cohesion: 0.08
Nodes (13): atomic_json(), campaign_plan(), find_cli(), PlaywrightCLI, run(), save_capture(), utcnow(), valid_candidate() (+5 more)

### Community 8 - "domain.ts"
Cohesion: 0.07
Nodes (10): BeeSense application package., load_config(), Resolve one editable NLP config and optional legacy partial overrides.      Expl, main(), Start the local relevance experiment, or its preserved baseline snapshot., No model/network calls: policy, provenance and integration regressions., DashboardTests, encoder() (+2 more)

### Community 9 - "InstaloaderCrawlerTests"
Cohesion: 0.08
Nodes (6): FakeClient, InstagramCrawlerTests, Offline contract/deadline tests; fixture data is always marked synthetic., records(), spawn_fixture(), spawn_hanging()

### Community 10 - "instagram_crawler.py"
Cohesion: 0.08
Nodes (16): _explain_filtered(), Historical 28 October 2026 coherence retrain: 52 topics, c_v 0.40970330118194137, Historical fixed top10/window110/all15878-unique macro c_v protocol, Historical topic training, 30 October 2026, Coherence is not domain relevance, Encode with SBERT, fit UMAP + DBSCAN and optionally merge to a topic count., Identify the parent thread, not the individual comment URL., Evidence-grounded topic descriptions and descriptive, source-aware trends. (+8 more)

### Community 11 - "crawl_reddit_playwright.py"
Cohesion: 0.10
Nodes (18): file_hash(), json_write(), main(), Publish a new versioned sidecar; never modify the original run., Derive Indonesian Gemini labels after topic count and coherence pass., enrich_run(), main(), Add Gemini descriptions to a verified fitted run, preserving its clustering. (+10 more)

### Community 12 - "SocialCrawlerTests"
Cohesion: 0.07
Nodes (30): changeDemoConnection(), connections, demoConnection(), validateStorage(), connectorStates, accounts, completed, migrations (+22 more)

### Community 13 - "SourceBarrier"
Cohesion: 0.14
Nodes (22): DatasetView(), TikTokConnector(), TransactionMigration(), AppContext, FieldErrorsContext, useApp(), csvCell(), download() (+14 more)

### Community 14 - "NLPTests"
Cohesion: 0.13
Nodes (12): ContentInput, ContractTests, Dataset, digest(), dumps(), MemorySink, Shared pipeline; adapters cannot choose their own headers or cell formats., RecordFactory (+4 more)

### Community 15 - "types.ts"
Cohesion: 0.06
Nodes (5): hanging_worker(), persistent_worker(), Offline contracts for Twitter/X acquisition; no live credentials required., tweet(), TwitterCrawlerTests

### Community 16 - "TwitterCrawlerTests"
Cohesion: 0.09
Nodes (9): Validate and return the effective plan without browser/network access., Re-export saved Contents without network or modifying the source bundle., Describe the acquisition backend independently of the shared export., Compose platform workers with one configuration, scheduler and export bundle., SocialCrawler, Universal crawler configuration consolidation, WIB archive and native identity deduplication, Nullable crawl limits and complete comment intent (+1 more)

### Community 17 - "tiktok_crawler.py"
Cohesion: 0.11
Nodes (22): bounded_events(), HtmlPage, HtmlSource, load_settings(), LocalHtmlSource, native_fullname(), now_iso(), object_key() (+14 more)

### Community 18 - "file_hash"
Cohesion: 0.13
Nodes (24): install_browser(), Install the browser required by the native TikTok backend., Live, loopback-only task/result bridge for an already-connected Chrome agent.  T, ChromeCaptureWorker, live_chrome_plan(), main(), metric_number(), native_id() (+16 more)

### Community 19 - "SocialCrawler"
Cohesion: 0.14
Nodes (21): emptyParallelConfig(), ParallelWorkspace(), PlatformPage(), httpApi, ConversationPicker(), applyConversation(), initialConfig(), isoWib() (+13 more)

### Community 20 - ".row"
Cohesion: 0.11
Nodes (4): StreamlitTests, ExplanationTests, model_from_counts(), profile()

### Community 21 - "Active TikTokCrawler2.6.1 / NativeTikTokClient / BeeSenseNative1.3.0 with Playwright1.62.0"
Cohesion: 0.09
Nodes (8): Use the same class TF-IDF vocabulary for selection and publication., Macro c_v on ALL non-noise topics and a fixed full-corpus reference.          Un, Extract real sentences using relevance plus MMR diversity., Rule-based segmentation preserving exact offsets in the original text., Reuse immutable SBERT features only after verifying data/model identity., Preserve explicit zero distances, including identical sentence vectors., Merge entire DBSCAN groups using sentence-weighted Ward linkage.          Minimi, Select DBSCAN parameters on UMAP; evaluate in original SBERT geometry.

### Community 22 - "read_config"
Cohesion: 0.13
Nodes (16): expand_config(), One editable crawler configuration, expanded before adapter validation., Read a bounded JSON object without touching authentication or runtime state., Apply shared defaults; an explicit platform value always wins, even []., Project the versioned universal file to a legacy standalone adapter contract., read_config(), standalone_config(), Reddit-only compatibility entry point for the integrated SocialCrawler Reddrix b (+8 more)

### Community 23 - "organize"
Cohesion: 0.06
Nodes (32): CLI2.6.1/native1.3.0/live1.2.1/extension1.2.1 retains same business configuration and permissions;auth unchanged, Chrome live follows global deadline;timeout_seconds90 audit field does not prove90second truncation;Stop/CAPTCHA/login/rate limits remain, Single social_crawler.json business configuration across all runners and Chrome transports, Five enabled platforms,target1000each,null duration/count caps,preserved comment context and root filters;source access/coverage not guaranteed, Instagram backend browser Chrome/Playwright, Instagram browser: thread tersedia pada dokumen, kelengkapan tidak dijamin, Instagram: 1000 post, semua komentar tersedia tanpa cap, InstagramCrawler instagrapi atau browser (+24 more)

### Community 24 - ".error"
Cohesion: 0.11
Nodes (16): main(), native_id(), normalize_item(), object_key(), post_url(), Bounded newest-first date windows, shared by both entry points., Use the shared record contract without changing native X identity., Adapt a persistent Scweet worker to SocialCrawler's five-argument protocol. (+8 more)

### Community 25 - "Conversation Parallel Execution Plan"
Cohesion: 0.14
Nodes (24): create_client(), error_receipt(), instagram_worker(), InstagramAdapter, InstagramCrawler, load_client(), login_from_file(), login_local() (+16 more)

### Community 26 - "social_crawler.py"
Cohesion: 0.11
Nodes (16): cap(), deadline_after(), Nullable application limits; network timeouts and pacing stay independent., reached(), remaining(), remaining_seconds(), browser_configuration(), browser_script() (+8 more)

### Community 27 - "crawl_reddit_single.py"
Cohesion: 0.13
Nodes (21): retry_after_seconds(), Storage settings shared with the frontend; DSNs stay in server environment., require_excel_storage(), storage_config(), AccessBarrier, account_cooldown(), auth_material(), configuration() (+13 more)

### Community 28 - "compilerOptions"
Cohesion: 0.21
Nodes (9): assert_accessible(), content_node(), first(), fixture_page(), RedditHtmlParser, RedditTests, rendered_text(), source_time() (+1 more)

### Community 29 - "architecture.json"
Cohesion: 0.20
Nodes (23): Composition(), JobDetail(), liveStates, PlatformCard(), ProgressChart(), JobStatistics(), PlatformResults(), TransactionPreview() (+15 more)

### Community 30 - "twitter_crawler.py"
Cohesion: 0.07
Nodes (26): compilerOptions, allowImportingTsExtensions, esModuleInterop, isolatedModules, jsx, lib, module, moduleResolution (+18 more)

### Community 31 - "NativeTikTokClient"
Cohesion: 0.07
Nodes (26): annotations, audience, edges, flows, ignore, include, nodes, project (+18 more)

### Community 32 - "Desain dan verifikasi Sidebar TikTok Connector 1.4.0"
Cohesion: 0.14
Nodes (20): http_barrier(), barrier_status(), rate_limit_seconds(), collect_reddrix(), load_reddrix(), normalize_reddrix_item(), Map Reddrix 1.2.14 dictionaries without inventing identity or dates., Reddrix anti-bot exceptions do not expose an authoritative HTTP status. (+12 more)

### Community 33 - "Optimasi YouTube dan Reddit — 6 November 2026"
Cohesion: 0.19
Nodes (5): NativeTikTokClient, One ordinary Playwright session; observe public UI traffic, never forge APIs., Pause automation until the human confirms in the local control channel., Native client live failure versus fixture success, TikWM probe dead end

### Community 34 - "instaloader_crawler.py"
Cohesion: 0.10
Nodes (25): Optimasi YouTube dan Reddit — 6 November 2026, Cooldown YouTube/Reddit belum persisten lintas restart, Delivery tanpa migrasi; Docker dan performa live belum terverifikasi, Barrier 401/403/429/5xx melekat pada worker, max_comments nol berarti metadata-only; null tanpa cap, Stagnasi native ID 75 detik diperiksa pada batas request, Validasi: 96 tes, 94 lulus dan 2 SDK opsional skip, Hook internal SDK dipin dan versi tak dikenal ditolak (+17 more)

### Community 35 - "SocialExportMixin"
Cohesion: 0.16
Nodes (7): controlled_reddrix(), Small access barriers shared by the bounded YouTube and Reddit workers., Inspect HTTP status before Reddrix discards it as an anti-bot error., Serialize requests, wait after responses and latch the first barrier.      Reddr, RedditClientGuard, RedditRequestGate, RequestGateTests

### Community 36 - "demo.ts"
Cohesion: 0.12
Nodes (24): connectorState, Riwayat Connector 1.3.0 throughput-v6, BeeSense TikTok Connector 1.4.0 sidebar, Alur operator Reload, pilih tab, pairing dan kontrol, Akses dibatasi tab TikTok pilihan dan loopback, Sidebar native BeeSense: formulir, monitor dan kontrol, Form dan status sidebar aksesibel, Data terkirim sesi dibedakan dari ekspor Python (+16 more)

### Community 37 - "Clock"
Cohesion: 0.13
Nodes (20): advance(), cap, conversationSeed(), dataset(), generatedConversation(), get(), load(), loadConversations() (+12 more)

### Community 38 - "worker"
Cohesion: 0.11
Nodes (17): Shared root selection and formula-safe Excel projection for social crawlers., Project the full audit rows into one sheet, applying current filters., Requires config, include and exclude matchers; performs no acquisition., Return a local date for display; relative source dates stay estimates., SocialExportMixin, AccessBarrier, auth_material(), AuthError (+9 more)

### Community 40 - "manifest.json"
Cohesion: 0.19
Nodes (11): crawl_day(), historical_records(), organize(), Upsert observations, retain latest values and assign each ID its first WIB day., Read every exported row back; fail on repeated IDs, wrong days or lost rows., Recover a verified merge's source range with honest day-only precision., sha(), verify() (+3 more)

### Community 41 - "api.ts"
Cohesion: 0.09
Nodes (21): action, default_title, background, service_worker, type, description, host_permissions, key (+13 more)

### Community 43 - "topic_narratives.py"
Cohesion: 0.23
Nodes (3): ChromeBridgeTests, post(), Task isolation, real loopback transport and streamed export contracts.

### Community 44 - "ChromeBridgeTests"
Cohesion: 0.15
Nodes (14): configure_web_graphql(), instaloader_worker(), InstaloaderAdapter, InstaloaderSettings, _json(), observe_requests(), Standalone Instaloader experiment using BeeSense's shared Excel contract., Load JSON cookies only; never unpickle a session or replay a password. (+6 more)

### Community 45 - "PublishedDataTests"
Cohesion: 0.18
Nodes (12): add_readme(), BundleSink, main(), parser(), Validate the embedded contract; an external descriptor is optional., Atomic new directory; streaming JSONL + streaming, formula-safe Excel., run(), run_self_tests() (+4 more)

### Community 46 - "devDependencies"
Cohesion: 0.10
Nodes (21): devDependencies, eslint, @eslint/js, prettier, @testing-library/jest-dom, @testing-library/react, typescript, typescript-eslint (+13 more)

### Community 47 - "instaloader_browser_patch.py"
Cohesion: 0.14
Nodes (4): Read-only exploration of completed NLP runs; no training on page reruns., Count evidence in the filter, keeping sentences/comments/parents distinct., SocialNLPStreamlitApp, Saved Gemini narratives, 30 October 2026

### Community 48 - "stream"
Cohesion: 0.16
Nodes (18): Audit dan optimasi X / Instagram — 6 November 2026, Jendela tanggal X tanpa hari berulang, Balasan Instagram lazy dan reuse first_data, Fixture Instagram: dua menjadi satu request simulasi, Fixture X: 32 menjadi 29 kunjungan hari, Komentar utama sebelum balasan Instagram, Cooldown Instagram antarrun schema v1, Cap nol dan payload sesuai sisa (+10 more)

### Community 49 - "TwitterCrawler"
Cohesion: 0.14
Nodes (8): BoundedDom, Node, Exception, Small serialised-DOM reader, not a browser or full HTML5 repair engine., RestrictedRedirect, SourceFailure, HTMLParser, HTTPRedirectHandler

### Community 50 - "Audit dan optimasi X / Instagram — 6 November 2026"
Cohesion: 0.15
Nodes (4): main(), Run only Reddit through the shared Reddrix implementation in SocialCrawler., RedditCrawler, RedditCrawlerTests

### Community 51 - "RedditCrawlerTests"
Cohesion: 0.14
Nodes (6): configure_daily_quotas(), Optional daily quotas for the pinned Scweet account repository.  Scweet's public, Clock, Offline evidence for target-based runs and nullable comment/daily limits., ScweetQuotaTests, UnlimitedCrawlingTests

### Community 52 - "ExplanationTests"
Cohesion: 0.22
Nodes (6): FakeReddrix, item(), Reddrix field/identity boundaries and the real, shared Excel exporter., records(), Offline SDK boundaries; no social network requests are made here., RedditPerformanceTests

### Community 53 - "BoundedDom"
Cohesion: 0.27
Nodes (17): bridge(), cdp(), delay(), expired(), flush(), inFlight(), inspect(), page() (+9 more)

### Community 54 - "background.mjs"
Cohesion: 0.12
Nodes (17): scripts, build, build:demo, check, dev, format, format:check, lint (+9 more)

### Community 55 - "SocialNLPStreamlitApp"
Cohesion: 0.12
Nodes (17): outputs/crawling/<platform>/<YYYY-MM-DD>/social_data.xlsx, --output-dir mempertahankan bundle eksplisit legacy, Hari pertama akuisisi dengan nilai observasi terbaru, Native ID unik global lintas seluruh tanggal, Konsolidasi awal: 34785 native ID, empat platform, sembilan partisi, Relokasi bundle belum terbit dan relocation map, Publikasi partisi dengan lock dan rollback, native_roots.json mempertahankan root Twitter (+9 more)

### Community 56 - "test_unlimited_crawling.py"
Cohesion: 0.26
Nodes (16): build_prompt(), canonical(), digest(), generate(), load_key(), Gemini narratives grounded in ranked topic keywords and representative sentences, Up to ten unique fitted sentences, cosine rank descending, stable ID ties., One request per topic; restart uses source/prompt/keyword-bound local receipts. (+8 more)

### Community 58 - "ConversationWorkspace.tsx"
Cohesion: 0.28
Nodes (13): collect(), media_pk_from_url(), media_url(), native_pk(), normalize_item(), object_key(), ValueError, Map explicit native IDs/timestamps; do not infer authors or text coverage. (+5 more)

### Community 60 - "Panduan output per platform dan tanggal WIB"
Cohesion: 0.15
Nodes (16): Graphify memory: Selenium crawler preserving the Excel contract, Access-barrier and stagnation safeguards, Graphify memory: low-risk YouTube and Reddit crawler optimization, Low-risk crawler acceleration, Reddit response-paced request serialization, YouTube native-comment streaming and deduplication, CampaignRunner parallel process launcher, Stable campaign snapshot and output contract (+8 more)

### Community 61 - "AnalysisTests"
Cohesion: 0.28
Nodes (13): checksum(), native(), Resolve X conversation roots from audited native IDs, never caption similarity., Read a workbook-bound sidecar, or the original hash-verified crawl audit., twitter_roots(), write_roots(), main(), merge() (+5 more)

### Community 62 - "Graphify memory: parallel crawling campaign proposal"
Cohesion: 0.28
Nodes (10): sessionCookies menjadi metadata bersama panduan dan hint, TikTokChromePreparation(), sessionCookies, sessionPlatforms, validateAuth(), AuthSettings(), SessionGuide(), AuthInput (+2 more)

### Community 63 - "Panduan sesi per sosmed — 6 November 2026"
Cohesion: 0.13
Nodes (15): dependencies, @fontsource-variable/plus-jakarta-sans, lucide-react, react, react-dom, react-router-dom, @tanstack/react-query, xlsx (+7 more)

### Community 64 - "dependencies"
Cohesion: 0.23
Nodes (15): Audited Social Crawler Output Bundle, DataDwip Instagram Scraping Reference, 29 October 2026 Campaign Result, Instagram Instaloader Integration, Native Identity Deduplication, HTTP 429 Cooldown and Retry Policy, Reddit Reddrix Integration, RFC 6585 Section 4 (+7 more)

### Community 65 - "json_write"
Cohesion: 0.22
Nodes (12): CI memeriksa boundary performa YouTube dan Reddit, GitHub Actions Verify BeeSense, One shared root policy, usable before fetching expensive child pages., root_rejection(), Pinned yt-dlp hooks: stream native comments without buffering a full list., root_filter(), root_projection(), baseline_function() (+4 more)

### Community 66 - "StreamlitTests"
Cohesion: 0.14
Nodes (6): ChromeLiveWorker, One pending operation at a time, with streamed batches and stale-task rejection., Local Chrome bridge introduction, Extension installation and pairing contract, Pairing timeout is separate from crawl time, Queued keywords are not executed queries

### Community 67 - "TwitterCoordinatorWorker"
Cohesion: 0.31
Nodes (12): commentPaginationExhausted(), metric(), nativeId(), parsePublicJson(), retryAfter(), sourceComments(), sourceHasMore(), sourceVideo() (+4 more)

### Community 68 - "ChromeLiveWorker"
Cohesion: 0.19
Nodes (9): Shell(), ApiError, base, connection(), connectorPath(), jobPath(), post(), request() (+1 more)

### Community 69 - "core.mjs"
Cohesion: 0.20
Nodes (11): main(), published_crawl_files(), published_relevance_files(), published_source_files(), Verify published source workbooks and the dashboard artifact bundle., Bind a separately published relevance dataset to the active fitted mask., Verify record identity independently of sentence-text deduplication., A merge report binds its small, explicit audit sidecars to the input. (+3 more)

### Community 71 - "GeminiTests"
Cohesion: 0.30
Nodes (3): GeminiTests, response(), topic()

### Community 72 - "InstagramBrowserWorker"
Cohesion: 0.27
Nodes (8): classifyCaptureFailure(), enrichBatch(), rateLimitSeconds(), inWindow(), mergeCandidates(), row, source, window

### Community 73 - "browser_campaign_detail.mjs"
Cohesion: 0.29
Nodes (11): _audit_key(), _lock(), _native(), Publish one globally unique social dataset partitioned by platform and crawl day, Bind compact rows to real acquisition timestamps and native roots., source_records(), stamp(), consolidate() (+3 more)

### Community 77 - "App.tsx"
Cohesion: 0.32
Nodes (11): apply_browser_patch(), browser_graphql_query(), _check(), _cookie(), _hints(), _load_tokens(), main(), _pace() (+3 more)

### Community 78 - ".render"
Cohesion: 0.26
Nodes (5): instaloader_options(), InstaloaderWorker, One subprocess and rate controller, with killable per-operation deadlines., Validate shared Instaloader settings without loading credentials or networking., upstream_version()

### Community 79 - "Dashboard BeeSense: verified artifacts, caption source labels and topic evidence"
Cohesion: 0.21
Nodes (12): Tempel Value cookie, bukan label Session pada Expires, Operator memilih origin, Name dan Value pada Chrome DevTools, Panduan tidak mengubah auth nyata, database atau deployment, Validasi panduan: 50 Vitest, 2 sinkronisasi dan UI lokal, Instagram: cookie sessionid dari instagram.com, Membuka panduan menjaga input masked tanpa auto-save/start, Panduan details/summary native di samping input dan persiapan Chrome, Panduan sesi per sosmed — 6 November 2026 (+4 more)

### Community 80 - "CommentDomTests"
Cohesion: 0.17
Nodes (7): client, ConversationWorkspace, ErrorBoundary, JobDetail, ParallelWorkspace, PlatformWorkspace, router

### Community 81 - "app.py"
Cohesion: 0.23
Nodes (12): Active filtered 20 topics / c_v 0.4666033620 with 20 stored narratives; before 20 topics / c_v 0.4346102845, five supported platforms; old dated metrics remain history, Occurrences, sentences, comments and roots differ; source identity keeps same-title posts separate, c_v is in-sample lexical coherence, not accuracy; root dates / trend gaps and source dominance disclosed, Dashboard BeeSense: verified artifacts, caption source labels and topic evidence, Five views expose summary, stable topic map, selected-topic explanation, sentences / sources and methods; counts / evidence read verified artifacts, not hardcoded or refitted, Oct 29 / 30 model and Docker healthy-image results are history; new image unverified because daemon unavailable; publication target main / Streamlit is workflow, not evidence push / redeploy completed, Legacy artifact schemas and snapshots without narrative CSV remain readable; UI filter changes evidence / counts, not model scores or memberships; Gemini CSV read without runtime API, Enrichment changes only occurrence copy for UI; contributing-post graph, source table and sentence evidence share caption labels, two-line graph labels / full hover and table text, All 25 TikTok posts have caption in teks on jenis=post rows; judul_post is empty because no separate source title exists (+4 more)

### Community 83 - "PRD Machine Learning"
Cohesion: 0.24
Nodes (8): AccessBarrier, error_receipt(), PaginationStalled, RuntimeError, The source claims more pages without advancing native identities., KeywordMatcher, Aho-Corasick; offsets refer to Python Unicode code points in source., Contextual relevance design remains unimplemented

### Community 84 - "InstaloaderWorker"
Cohesion: 0.18
Nodes (11): Current36,233record corpus,filtered20topics/c_v0.4666033620 and before20/c_v0.4346102845;11,185occurrences/10,795unique filtered,6individualtopics<0.4, Gensim4.4 c_v uses top10positive c-TF-IDFterms,window110 and all run-unique embedding_text includingnoise;unweighted mean of20topics,invalid/nonfinite topic invalidates aggregate, Only normalized target text forms embeddings;c-TF-IDFlabels count unigram/bigram features,MMR diversifies originalquotes,Theil–Sen/Kendall trends have source/platform/support guards;centroidgraph edges INFERRED, DatedOct29/30model metrics and Dockerhealthy claims are historical;originalfitted/Gemini snapshots preserved,noDBmigration orproductionDocker/Coolifychanges, MultilingualMiniLM-L12-v2 immutable revision,384dimensions CPU,safetensors;128token windows/stride24 averaged thenL2normalized,cache binds encoder/text/checksums;no neural fine-tuning, WeightedWard on originalSBERT group sums merges whole DBSCANgroups to20,does not split groups or absorbnoise;bothseeds reduced before evaluation,mapping/cost retained, SocialNLPClusterer:SBERT→L2→UMAP→DBSCAN→weightedWard→c-TF-IDF→verified artifacts, SocialNLP2.6.1TikTok video/photo HTTPS native ID survives username change;X roots use checksum-bound Contents/native_roots audit,not title/date guessing;metadata not embedding features (+3 more)

### Community 85 - "source_records"
Cohesion: 0.25
Nodes (11): Corpus Normalization and Deduplication, PRD Frontend Crawler, Obsidian Machine Learning Notes, PRD Machine Learning, Social NLP Methodology, Cross-Platform Social Schema Normalization, Source and Respondent Role Separation, Survey Dataset Contract (+3 more)

### Community 86 - "November5TikTok combined retraining:both local fits20topics/mean c_v>=0.4,40authorized Gemini narratives complete,activepair updated"
Cohesion: 0.27
Nodes (10): Current afterfilter20topics,c_v0.4666033620;10,795unique/11,185occurrences,81.81%coverage,silhouette0.062782,ARI0.641173,DBSCAN154groups→Ward20, Current beforefilter20topics,c_v0.4346102845;53,967unique/55,257occurrences,95.75%coverage,silhouette-0.011752,ARI0.803763,DBSCAN508groups→Ward20, After localfit and payloadpreview,explicit permission sent400keywords+400representative sentences to GoogleGemini gemini-3.5-flash-lite;40narratives saved20perpair,prompthashes match approved payload, Nov5stored7posts492comments537replies=1,036unique;last16:00segmentaccepted0records because2rootsout-of-period/1withoutinclude;115comments196replies observed311not stored or modeled, Combinedsource totals:YouTube25,158,Reddit4,514,Instagram4,444,X669,TikTok1,448;TikTokallarchive25posts617comments806replies differs from today’s7/492/537, 12sourceworkbooks/11platform-date partitions merge to36,233unique IDs:2,552roots+33,681comments/replies;34,764interfile repeats removed,0native duplicates/0orphans;firstoccurrence order/latestprovided values retained, Newmask55,257decisions:11,185relevant/19,739general/3,833out/20,500uncertain;verifiedsubsetreuse only aftersource/model/text/sentenceID checks,then projection/clustering/evaluation refitted, Native dashboard8502,productionDocker/envunchanged,noDBmigration;newDockerimage unverified because daemon unavailable;requestedcommit/fast-forwardmain/push is not proof remoteCI/productiondeployment (+2 more)

### Community 87 - "sidepanel.mjs"
Cohesion: 0.38
Nodes (10): applyConversation, Config, Conversation, ConversationWorkspace.tsx, Documented and Tested Date Boundary, Frozen Conversation Snapshot, ParallelWorkspace.tsx, PlatformWorkspace.tsx (+2 more)

### Community 89 - "BeeSense: separate crawler, NLP and artifact-reading Streamlit dashboard"
Cohesion: 0.28
Nodes (7): clock, fieldError(), numbers, refresh(), render(), showTabError(), state

### Community 90 - "build_topic_sentences.mjs"
Cohesion: 0.25
Nodes (6): embedded_videos(), Missing pagination metadata never proves that all comments were loaded., Find video objects in hydration and browser response JSON., Honor server seconds or an HTTP date; never put headers in receipts., retry_after(), source_has_more()

### Community 91 - "YouTubePerformanceTests"
Cohesion: 0.36
Nodes (6): conversationPrompt(), parseConversationWorkbook(), promptFilename(), text(), unique(), WorkbookRow

### Community 92 - "KeywordMatcher"
Cohesion: 0.25
Nodes (5): _load_artifacts(), main(), Streamlit entry point for local and Community Cloud dashboards.  Training lives, Resolve display captions from verified roots, leaving fitted files intact., Streamlit Community Cloud entry point; UI implementation lives in Dashboard.

### Community 93 - "BundleSink"
Cohesion: 0.22
Nodes (9): Active36,233unique five-platform records; before/after models20topics,c_v0.4346102845/0.4666033620; filtered11,185occurrences/10,795unique sentences,81.81%coverage,6topics individually below0.4, Explicitly authorized400keywords+400representative sentences sent to GoogleGemini for40stored narratives; UI reruns read verifiedCSV without API or refitting, BeeSense: separate crawler, NLP and artifact-reading Streamlit dashboard, StreamlitCloud main/streamlit_apps.py uses repository-relative active snapshot and complete allowlist/checksums; no runtime secrets/model download/training required, Earlier baseline8,449,29,099,33,034,34,095 and34,764record sources/models are retained with original checksums; their scores and trials remain dated history, DashboardPython3.12/3.14 installs artifact/UI dependencies only,without Torch/UMAP/Gensim/ONNX/Numba/crawler;PyArrow24pinned for reader stability,training environment separate, Data verifier/check-git,offline tests,CI and Docker checks are distinct;dashboard reads artifacts,noDBmigration;old local Docker validation is historical,remoteCI not inferred from local passes, New corpus is encoded with pinned pretrainedSBERT;UMAP/DBSCAN/weightedWard refit to20topics;reuse requires checksum/model/sentence-order compatibility and never changes encoder weights (+1 more)

### Community 94 - "Settings"
Cohesion: 0.22
Nodes (6): body, payload, [payloadPath, outputPath, previewDir], sentences, topics, workbook

### Community 96 - "InstaloaderCrawler"
Cohesion: 0.43
Nodes (4): BrowserPatchTests, context(), Verify the supplied browser-style patch without sending network requests., response()

### Community 97 - "package.json"
Cohesion: 0.48
Nodes (3): InstaloaderCrawler, main(), Separate backend; preserves the existing export and native-ID dedup logic.

### Community 98 - ".parent_post_key"
Cohesion: 0.33
Nodes (4): identity(), Native social record identity shared by merge and organized crawler outputs., Return global native object ID plus its root; text never defines identity., Offline integration and failure contracts for the native TikTok browser crawler.

### Community 99 - "ContextRelevanceFilter/LocalSemanticBackend: local pinned-SBERT reference-based occurrence filtering,not human-labeled classifier or per-comment API"
Cohesion: 0.29
Nodes (6): engines, node, name, private, type, version

### Community 100 - "instagram_browser_capture.mjs"
Cohesion: 0.29
Nodes (7): 36,233records produce55,257decisions:11,185relevant,19,739general interaction,3,833out-of-scope,20,500uncertain;10,795unique accepted sentences, Authorized Gemini uses10weighted keywords/10centroid-near sentences per topic;new narrative bundle copies fitted files identically,validates before/after checksums and publishes atomically;UI reads without API, Every occurrence receives one decision;mask/artifacts bind source checksum,ID/text/model/normalization checks allow subset embedding reuse;UMAP/DBSCAN/Ward/evaluation still refit, Different reference corpora prevent direct before/after quality claims;example tests are not precision/recall,lightNLI rejected;old snapshots/configs retained,SQLitecache disposable,noDBmigration, ContextRelevanceFilter/LocalSemanticBackend: local pinned-SBERT reference-based occurrence filtering,not human-labeled classifier or per-comment API, Maximum cosine against category examples:direct>=0.42/margin0.035,short<=14word targets may need context;context>=0.50/margin0.035 afterdirect>=0.22;onlyrelevant enters clustering, URL/native roots and checksum-verified parent relations supply context;missing/conflicting parents are not guessed;only original target sentence is clustering feature

### Community 101 - "TikTokWorker"
Cohesion: 0.47
Nodes (3): instagramNavigate(), instagramRetryAfter(), instagramSourceRateLimit()

### Community 103 - "Historical map: before and after relevance-filtered clustering"
Cohesion: 0.40
Nodes (6): Active native provenance:CLI2.6.1 / NativeTikTokClient / BeeSenseNative1.3.0, Current Playwright1.62.0 and OpenPyXL3.1.5;no third-party TikTok SDK or canceled Chinel0 code, Ordinary browser UI responses/hydration/native IDs feed shared Dataset/Excel;unknown metadata not synthesized,private local auth unchanged,pacing/Retry-After/partial output retained, Combined crawler environment pins Playwright1.62.0 for Camoufox0.5.8<1.63;Chrome plugin protocol and dashboard requirements unchanged, Offline saved capture,agent-driven live transport,installed-extension live transport and owned Chromium manual preflight are distinct;dated trial versions/partial counts remain history, Uncapped comments need source/parent pagination-end evidence,runtime build/policy handshake precedes clock;old-protocolHTTP409/incomplete batches preserve partial data,never claim global completeness

### Community 104 - "Uji backend aktif TikTok-Api 3 November 2026"
Cohesion: 0.33
Nodes (6): Historical architecture snapshot exported 2 November 2026, Historical map: before and after relevance-filtered clustering, Self-contained BeeSense architecture map export, Stored-data sentence relevance filter before topic clustering, Local pretrained SBERT with per-category maximum cosine scores, Three groups of semantic reference examples

### Community 105 - "TikTok existing-Chrome observation and offline import — 3 November 2026"
Cohesion: 0.33
Nodes (6): TikTok-Api: 0/500, PARTIAL ACCESS_BLOCKED setelah 33,27 detik, Tiga HTTP200, pencarian kosong; bukan bukti token kedaluwarsa, Uji backend aktif TikTok-Api 3 November 2026, PyTok historis: 0/500, PARTIAL CAPTCHA_REQUIRED, 159,81 detik, Riwayat uji PyTok 3 November 2026, PyTok: timeout pertama, CAPTCHA worker kedua, telemetry HTTP tidak lengkap

### Community 106 - "SBERT, UMAP, DBSCAN, and c-TF-IDF pipeline"
Cohesion: 0.33
Nodes (6): Owned Chromium trial at 14:49:43 WIB cancelled; already-open logged-in Chrome used without restart or profile copying, TikTok existing-Chrome observation and offline import — 3 November 2026, Original-post metadata ID matched; 10 observed comment IDs, relative comment dates unknown, unobserved replies omitted, ChromeCaptureWorker offline import produces 11 content rows in common Excel/day archive; native IDs unique across dates, Observed and imported 1 post, 10 comments, 0 replies; target 500 not achieved and comments incomplete, 33 focused tests passed; auth unchanged, no PostgreSQL migration; Docker unverified because daemon unavailable

### Community 107 - "SPA container health and deep-link verification"
Cohesion: 0.47
Nodes (6): DBSCAN clustering, Sentence-BERT embedding, SBERT and DBSCAN method note, Graphify memory: Streamlit dashboard startup, Graphify memory: SBERT, UMAP, DBSCAN, and c-TF-IDF migration, SBERT, UMAP, DBSCAN, and c-TF-IDF pipeline

### Community 108 - "sync-config.mjs"
Cohesion: 0.40
Nodes (5): Frontend format, lint, test, and build quality gate, SPA container health and deep-link verification, Verify Crawler Frontend workflow, BeeSense Crawler SPA document, Frontend main.tsx entry module

### Community 109 - ".topic_figure"
Cohesion: 0.50
Nodes (3): publicDefaults(), source, target

### Community 111 - "public_web_post.test.mjs"
Cohesion: 0.40
Nodes (3): _graph_positions(), Bounded topic graph: volume from filtered rows, semantic edges from the full mod, Keep the full-model layout stable while volume and edge filters change.

### Community 112 - "NetworkPacing"
Cohesion: 0.40
Nodes (5): Narrative-only bundle may retain source output_dir in config;opened bundle+manifest identify result;old data/fits/container settings preserved,no migration, Relevance config and dashboard before/after pair remain separate;mask must match source checksum,custom corpus cannot inherit old mask/baseline silently, Dry-run validates without workbook/model/fitting/credentials;nested partial overrides merge and unknown fields reject;effective summaryconfig reproduces into new directory,not copied presets, Single config/social_nlp.json for SocialNLPClusterer;five dated presets removed,history retained in summaries, Default20topics,mean c_v>=0.4,Gemini enabled,filtered active snapshot;gate never automatically lowered and local API key stays outside tracked config

### Community 115 - "InstaloaderCrawler dan patch GraphQL web"
Cohesion: 0.50
Nodes (4): Provenance dfreelon/Pyktok — historis, Pyktok dan TikTokApi tidak lagi requirements aktif, Pyktok historis: HTTP200 hydration tanpa video pada satu halaman keyword, Riwayat Pyktok: 0/500, 2,69 detik, CLIENT_UPGRADE_REQUIRED

### Community 116 - "Dua uji live native 3 November 2026 — keduanya gagal target"
Cohesion: 0.50
Nodes (3): printWidth, singleQuote, trailingComma

### Community 118 - "Memori historis delivery X/Instagram dan sidebar TikTok"
Cohesion: 0.50
Nodes (4): Penolakan Instagram menghentikan crawl, Uji Instagram historis trial06: 1 post / 20 komentar, Worker Instaloader 4.16 persisten, InstaloaderCrawler dan patch GraphQL web

### Community 119 - "test_relevance_runtime.py"
Cohesion: 0.50
Nodes (4): Headed: 0/500, 11,05 detik, PARTIAL / ACCESS_BLOCKED, Headless: 0/500, 4,79 detik, PARTIAL / ACCESS_BLOCKED, Dua uji live native 3 November 2026 — keduanya gagal target, Fixture browser dicegat: post komentar reply dan statistik berhasil, bukan live

### Community 120 - "pageOperation"
Cohesion: 0.50
Nodes (4): Trial PARTIAL ACCESS_BLOCKED: 0/500 post, 0 komentar/balasan, Satu HTTP200 tanpa bootstrap terbaca; berhenti setelah 0,61 detik, Run kosong menyimpan audit tanpa TikTok harian; 34785 ID lama tetap, Uji TikTok 3 November 2026

### Community 121 - "Provenance PyTok historis, dependency sudah tidak aktif"
Cohesion: 0.50
Nodes (4): Memori historis delivery X/Instagram dan sidebar TikTok, Delivery historis sidebar 1.4.0 sidebar-v7, Uji TikTok sebelum panduan: 10 post / 1348 komentar / 481 balasan, Delivery historis X/Instagram: request efisien dengan pacing tetap

### Community 122 - "BeeSense App Icon"
Cohesion: 1.00
Nodes (3): pageOperation(), Reply control starvation and forced scrolling, Clipped reply controls require visibility checks

### Community 123 - "Shared crawler dependency bundle"
Cohesion: 0.67
Nodes (3): Riwayat PyTok 0.3.0: PolyForm Noncommercial 1.0.0 AND MIT, Provenance PyTok historis, dependency sudah tidak aktif, Pengguna kembali ke TikTok-Api; PyTok tidak lagi aktif

### Community 124 - "Backend/__init__.py"
Cohesion: 0.67
Nodes (3): BeeSense App Icon, Black Isometric Cube Mark, Orange Rounded Square Background

### Community 125 - ".legacy_comments"
Cohesion: 0.67
Nodes (3): Shared crawler dependency bundle, Python 3.12 offline regression and crawler tooling environment, Native TikTok dependencies: Playwright 1.62.0 and openpyxl 3.1.5

## Knowledge Gaps
- **296 isolated node(s):** `window`, `source`, `row`, `candidate`, `requests` (+291 more)
  These have ≤1 connection - possible missing edges or undocumented components.
- **38 thin communities (<3 nodes) omitted from report** — run `graphify query` to explore isolated nodes.

## Suggested Questions
_Questions this graph is uniquely positioned to answer:_

- **Why does `Panduan sesi per sosmed — 6 November 2026` connect `Dashboard BeeSense: verified artifacts, caption source labels and topic evidence` to `Graphify memory: parallel crawling campaign proposal`?**
  _High betweenness centrality (0.200) - this node is a cross-community bridge._
- **Why does `sessionCookies menjadi metadata bersama panduan dan hint` connect `Graphify memory: parallel crawling campaign proposal` to `Dashboard BeeSense: verified artifacts, caption source labels and topic evidence`?**
  _High betweenness centrality (0.142) - this node is a cross-community bridge._
- **Why does `SocialCrawler` connect `TwitterCrawlerTests` to `SocialNLPClusterer`, `crawl_youtube.py`, `InstagramCrawlerTests`, `InstaloaderCrawlerTests`, `types.ts`, `read_config`, `.error`, `Conversation Parallel Execution Plan`, `social_crawler.py`, `Desain dan verifikasi Sidebar TikTok Connector 1.4.0`, `instaloader_crawler.py`, `SocialExportMixin`, `worker`, `.thread`, `manifest.json`, `ChromeBridgeTests`, `Audit dan optimasi X / Instagram — 6 November 2026`, `RedditCrawlerTests`, `ExplanationTests`, `ConversationWorkspace.tsx`, `.render`, `Active native provenance:CLI2.6.1 / NativeTikTokClient / BeeSenseNative1.3.0`?**
  _High betweenness centrality (0.128) - this node is a cross-community bridge._
- **Are the 37 inferred relationships involving `SocialCrawler` (e.g. with `RedditCrawler` and `_SeleniumSource`) actually correct?**
  _`SocialCrawler` has 37 INFERRED edges - model-reasoned connections that need verification._
- **Are the 26 inferred relationships involving `SocialNLPClusterer` (e.g. with `SocialNLPStreamlitApp` and `LocalSemanticBackend`) actually correct?**
  _`SocialNLPClusterer` has 26 INFERRED edges - model-reasoned connections that need verification._
- **What connects `window`, `source`, `row` to the rest of the system?**
  _296 weakly-connected nodes found - possible documentation gaps or missing edges._
- **Should `SocialNLPClusterer` be split into smaller, more focused modules?**
  _Cohesion score 0.08578088578088579 - nodes in this community are weakly interconnected._