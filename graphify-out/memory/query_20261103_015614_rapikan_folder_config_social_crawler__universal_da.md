---
type: "query"
date: "2026-11-03T01:56:14.692478+00:00"
question: "Rapikan folder config social crawler: universal dari satu file, hapus JSON yang tidak diperlukan, dan perbarui Obsidian"
contributor: "graphify"
outcome: "useful"
source_nodes: ["SocialCrawler", "RedditCrawler", "InstagramCrawler", "InstaloaderCrawler", "TwitterCrawler"]
---

# Q: Rapikan folder config social crawler: universal dari satu file, hapus JSON yang tidak diperlukan, dan perbarui Obsidian

## Answer

Expanded from graph vocabulary: config configuration social crawler instagram twitter reddit youtube instaloader. The graph identified SocialCrawler plus standalone runner defaults as the consolidation boundary. Implemented schema_version 1 in config/social_crawler.json with shared queries and platform_defaults, validated by existing platform parsers. Added crawler_config.read_config, expand_config and standalone_config; all six CLIs use the same file. Removed eight duplicate crawler presets. Twitter accepts shared audit workbooks as baselines while preserving native ID and URL consistency checks. Legacy caller dictionaries remain supported. The combined default keeps YouTube and Reddit enabled; Instagram and Twitter are configured but disabled. Verified 175 crawler tests with 174 passes and one optional browser skip, twelve Reddit runner tests, lint, format, six dry-runs and a clean release guard. Graph and Obsidian maps updated. Docker daemon unavailable. No migration required.

## Outcome

- Signal: useful

## Source Nodes

- SocialCrawler
- RedditCrawler
- InstagramCrawler
- InstaloaderCrawler
- TwitterCrawler