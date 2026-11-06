---
type: "query"
date: "2026-11-06T02:26:10.536500+00:00"
question: "Upgrade TikTok crawler: stagnasi per post, komentar utama sebelum replies, backoff terbatas; lalu uji 50 post 1 jam"
contributor: "graphify"
outcome: "useful"
source_nodes: ["ChromeLiveWorker", "SocialCrawler", "TikTokCrawler", "runTask()", "NetworkPacing"]
---

# Q: Upgrade TikTok crawler: stagnasi per post, komentar utama sebelum replies, backoff terbatas; lalu uji 50 post 1 jam

## Answer

Expanded graph vocabulary: tiktok chrome comment replies pagination partial retry delay background bridge. Implemented Connector 1.3.0/build 20261106-throughput-v6: 75s native-comment-ID stagnation gives PARTIAL; new candidates precede one deferred retry; retry queue persists with manifest checksum and merges only new native IDs; top-level comments precede reply clicks; bounded 5/10/15s 5xx backoff, 30s shared pause and reset on successful HTTP; bounded response-body waiting with loadingFailed cleanup and foreign-post isolation. 114 relevant Python tests,13 Node tests,7 frontend tests and production frontend build pass. Broader Selenium tests unavailable in TikTok environment due missing selenium; Docker daemon inactive so image unbuilt. No database migration. Graph2510nodes/5005edges and generated Obsidian updated; health no dangling or missing endpoints. User authorized actual50post/max3600s test. CLI currently waiting on http://127.0.0.1:49968 for connector1.3.0 pairing; crawl timer has not begun and no new live data is claimed. Browser control failed to access tab/popup, so user must reload/pair locally. Live process session6670 writes output/tiktok_throughput_20261106/live.log; after pairing verify handshake then monitor and verify final export.

## Outcome

- Signal: useful

## Source Nodes

- ChromeLiveWorker
- SocialCrawler
- TikTokCrawler
- runTask()
- NetworkPacing