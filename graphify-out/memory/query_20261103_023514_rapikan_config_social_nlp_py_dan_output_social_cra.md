---
type: "query"
date: "2026-11-03T02:35:14.875563+00:00"
question: "Rapikan config social_nlp.py dan output social_crawler.py per sosmed per tanggal crawling WIB, tanpa ID duplikat"
contributor: "graphify"
outcome: "useful"
source_nodes: ["SocialNLPClusterer", "SocialCrawler", "organize", "identity"]
---

# Q: Rapikan config social_nlp.py dan output social_crawler.py per sosmed per tanggal crawling WIB, tanpa ID duplikat

## Answer

Expanded from original query via graph vocab: social, nlp, configuration, config, dashboard, relevance, model, merge, dataset, provenance. Crawler config uses config/social_crawler.json and NLP config uses config/social_nlp.json. Default SocialCrawler runs publish outputs/crawling/<platform>/<YYYY-MM-DD>/social_data.xlsx, with immutable raw audits under output/crawler_runs. Global native identity dedup retains first observed WIB day and latest values. Consolidation yielded 34785 unique IDs across 4 platforms and 9 partitions, zero duplicate native IDs; 47 workbooks checked with zero missing IDs. Historical recovery has 1058 Instagram records with campaign-day-only precision and null exact observation times. The existing dashboard corpus remains 34764 records and 20 topics, unchanged. NLP 117 tests and crawler 180 tests passed, one optional browser test skipped; dashboard 2 tests passed. Graph health has zero missing, dangling, collapsed or self-loop edges. No database migration required. Docker runtime verification unavailable because daemon inactive.

## Outcome

- Signal: useful

## Source Nodes

- SocialNLPClusterer
- SocialCrawler
- organize
- identity