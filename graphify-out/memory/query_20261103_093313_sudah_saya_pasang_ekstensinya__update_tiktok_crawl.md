---
type: "query"
date: "2026-11-03T09:33:13.200267+00:00"
question: "sudah saya pasang ekstensinya, update tiktok_crawler.py dan uji ulang 500 post 30 menit"
contributor: "graphify"
outcome: "useful"
source_nodes: ["ChromeLiveWorker", "TikTokCrawler", "SocialCrawler"]
---

# Q: sudah saya pasang ekstensinya, update tiktok_crawler.py dan uji ulang 500 post 30 menit

## Answer

Expanded trace ChromeLiveWorker wait_for_extension -> TikTokCrawler main -> SocialCrawler shared Excel. Updated TikTokCrawler2.4.1 actual extension plan/version, connected-before-run event,15s waiting heartbeat, explicit scoped pairing timeout and reuse --manual-wait-seconds for1..3600s pairing independently of1800s crawl.36Python crawler+10HTTP bridge+8Node tests pass, Ruff/pip/release guard pass. User confirms extension installed; automated browser rejects private all-tab listing and blocks internal chrome://extensions protocol. User must pair via popup. First600s wait timed out without starting crawler or new posts; retrylocalhost58698 waiting3600s then authorized500posts/1800s. No new TikTok data yet; old2posts/30comments/13replies are historical. Auth unchanged, no DB migration, Docker unverified. Graph refreshed2280nodes4727edges160communities,87unresolved AST references and3collapsed undirected edges remain documented.

## Outcome

- Signal: useful

## Source Nodes

- ChromeLiveWorker
- TikTokCrawler
- SocialCrawler