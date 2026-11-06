---
type: "query"
date: "2026-11-06T09:40:09.836663+00:00"
question: "Brainstorm satu perintah crawling campaign dengan folder outputs/crawling/id-nama campaign, konfigurasi teks bersama dan setiap platform berjalan paralel"
contributor: "graphify"
outcome: "useful"
source_nodes: ["socialexportmixin", "crawler_backend_social_crawler_py_socialexportmixin", "crawler_backend_twitter_crawler_py_socialexportmixin", "crawler_backend_instagram_crawler_py_socialexportmixin", "crawler_backend_tiktok_crawler_py_socialexportmixin", "crawler_frontend_src_shared_types_config", "machinelearning_context_relevance_contextrelevancefilter", "crawler_backend_social_export_socialexportmixin", "crawler_backend_social_crawler_socialcrawler"]
---

# Q: Brainstorm satu perintah crawling campaign dengan folder outputs/crawling/id-nama campaign, konfigurasi teks bersama dan setiap platform berjalan paralel

## Answer

BRAINSTORM / PROPOSED ONLY; no implementation authorized or performed. Expanded graph vocab: crawler config shared archive storage filter relevance query session scheduler campaign. User explicitly clarified one execution command must launch each selected platform truly in parallel, not a scheduler or round-robin workflow. Proposed CampaignRunner parent launches one isolated process per enabled platform at once using the existing SocialCrawler restricted to that platform. A stable campaign_id owns outputs/crawling/<id>-<slug>/ with campaign/config snapshot, progress/events, platform child folders, immutable attempts/checkpoints, combined export and relevance results. Freeze shared keywords, excludes, queries, hashtags, date scope and relevance references/model/thresholds in one campaign snapshot; adapt discovery syntax only to supported platform capabilities, with clear preview. Credentials and plugin/session binding remain platform-specific references outside output; ready platform processes run while another waits for login/connector. Parent aggregates progress and owns shared manifest/final export; workers write only their own platform data. Stop/pause/resume preserves partial records and the same campaign ID; new executions create new IDs unless explicitly resuming. Access barriers and pacing remain per platform/account, with one active owner of each session. Raw records remain available; relevance is classified in batches under the same policy. Deduplicate within campaign by native identity; cross-campaign baseline exclusion is explicit. Campaign status can become PARTIAL when one platform fails while others complete. Existing backend run() at social_crawler.py L1922 creates one bundle and round_robin at L2522 alternates blocking operations; true parallel launcher and campaign-aware frontend HTTP backend still need implementation. Relevance engine ContextRelevanceFilter at context_relevance.py L42 supports shared reference examples and batch classification. Suggested build order: campaign schema/folder + snapshot; parallel process launcher and partial recovery; one campaign form and monitoring; failure/concurrency/export tests. This is an executable research workflow, not a promise of database ACID rollback for external requests.

## Outcome

- Signal: useful

## Source Nodes

- socialexportmixin
- crawler_backend_social_crawler_py_socialexportmixin
- crawler_backend_twitter_crawler_py_socialexportmixin
- crawler_backend_instagram_crawler_py_socialexportmixin
- crawler_backend_tiktok_crawler_py_socialexportmixin
- crawler_frontend_src_shared_types_config
- machinelearning_context_relevance_contextrelevancefilter
- crawler_backend_social_export_socialexportmixin
- crawler_backend_social_crawler_socialcrawler
## Dokumen rencana

Rencana rinci dicatat di [PLAN_CAMPAIGN_PARALEL.md](../../docs/crawler/PLAN_CAMPAIGN_PARALEL.md). Status tetap planned; penyimpanan dokumen ini tidak mengimplementasikan atau menjalankan campaign paralel.
