---
type: "query"
date: "2026-11-03T07:33:01.801544+00:00"
question: "ok, coba buat sendiri deh Friday untuk Tiktok crawlernya, cari akal agar gak diblok"
contributor: "graphify"
outcome: "useful"
source_nodes: ["NativeTikTokClient", "TikTokCrawler", "SocialCrawler", "SocialExportMixin"]
---

# Q: ok, coba buat sendiri deh Friday untuk Tiktok crawlernya, cari akal agar gak diblok

## Answer

Expanded from original question via graph vocabulary: [tiktok, crawler, client, worker, normalize, export, config, auth, identity, dataset, docker, comment]. Implemented native BeeSense Playwright backend in TikTokCrawler 2.0.0, without TikTok SDKs or Chinel0 code. Native UI/hydration/network acquisition, request pacing, persistent Retry-After, terminal access barriers, partial exports, verified IDs and shared Excel/WIB archive are in place. Live access remains unsuccessful: headless 0/500 after4.79s, headed 0/500 after11.05s, PARTIAL/ACCESS_BLOCKED; headed reason native_api_empty_or_invalid_json despiteHTTP200. Ordinary browser fixture succeeded separately with synthetic responses.219 crawler tests ran successfully with1skip. Auth unchanged,34785 archiveIDs and0duplicates. No migration required. Docker daemon unavailable; image unbuilt. Graph2156nodes4484edges155communities,32unresolved targeted AST/import refs and6collapsed raw edges; do not claim complete graph integrity or unblocked live access.

## Outcome

- Signal: useful

## Source Nodes

- NativeTikTokClient
- TikTokCrawler
- SocialCrawler
- SocialExportMixin