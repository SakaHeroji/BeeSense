---
type: "query"
date: "2026-11-06T09:16:20.431587+00:00"
question: "Analisa dan percepat crawler YouTube dan Reddit dengan Graphify dan Obsidian tanpa meningkatkan risiko blokir"
contributor: "graphify"
outcome: "useful"
source_nodes: ["crawler_backend_social_export_root_rejection", "crawler_backend_social_crawler_collect_reddrix", "crawler_backend_social_crawler_socialcrawler"]
---

# Q: Analisa dan percepat crawler YouTube dan Reddit dengan Graphify dan Obsidian tanpa meningkatkan risiko blokir

## Answer

YouTube/Reddit optimized in SocialCrawler 1.11.0 and YouTube 0.2.0. Shared root_rejection runs before comments. YouTube streams/deduplicates native comments, lazy-searches, and passes extractor request delay. Reddrix closes capped/rejected iterators, serializes response-paced requests, bypasses hidden retry/refresh and limits initialization to one attempt. HTTP 401/403/429/5xx latch barriers, Retry-After survives, and 75-second no-native-ID stagnation stops before the next request as PARTIAL. Offline benchmark against d896cade2719d77b0498e87d5c79504cbf483894: YouTube synthetic comment pages 20 to 10 with same 101 IDs; Reddit 20 to 1 with same 11 IDs; timeout retains two previously lost comments. 96 tests: 94 passed, 2 optional SDK skips; 21 new boundary tests. Lint, format, compile, dry runs, CLI and CI YAML passed. No new live social crawl or live throughput claim. Docker daemon unavailable; image unbuilt. No migration required. Internal SDK hooks pinned, Reddit browser startup and cross-restart cooldown remain limitations. See docs/crawler/PERFORMANCE_YOUTUBE_REDDIT_20261106.md and graphify-out/obsidian/Optimasi Crawler YouTube dan Reddit 20261106.md. Graph 2710 nodes/5485 edges/202 communities; semantic tokens unavailable.

## Outcome

- Signal: useful

## Source Nodes

- crawler_backend_social_export_root_rejection
- crawler_backend_social_crawler_collect_reddrix
- crawler_backend_social_crawler_socialcrawler