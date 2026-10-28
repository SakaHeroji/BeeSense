---
type: "query"
date: "2026-10-28T13:57:00.625766+00:00"
question: "Buat versi SocialCrawler dalam file baru memakai Selenium dengan kontrak Excel sama, gunakan Graphify dan Obsidian, lalu jalankan konfigurasi penuh."
contributor: "graphify"
outcome: "useful"
source_nodes: ["SocialCrawler", "SocialCrawlerSelenium", "BundleSink"]
---

# Q: Buat versi SocialCrawler dalam file baru memakai Selenium dengan kontrak Excel sama, gunakan Graphify dan Obsidian, lalu jalankan konfigurasi penuh.

## Answer

Graph vocabulary: social crawler export excel workbook browser reddit youtube config. Architectural path: SocialCrawlerSelenium inherits SocialCrawler filters, targets and Excel exporters; Selenium worker streams public YouTube/Reddit DOM events through the existing hard-deadline supervisor, normalizes native records, and uses BundleSink. The only base extension is _source_metadata for truthful Selenium provenance. All 40 crawler tests passed including real Chrome DOM fixtures. Graph has 637 nodes and 1455 edges, generated Obsidian vault has 662 notes. Full configuration crawl started at 2026-10-28 20:43:45 WIB, up to one hour, output outputs/social_selenium_20261028_01 and log .cache/selenium-full-20261028-01.log. Still running at last check with at least 86 selected rows in staging; Excel is published atomically on stop. Docker daemon unavailable; canonical tracked dataset checksums preserved.

## Outcome

- Signal: useful

## Source Nodes

- SocialCrawler
- SocialCrawlerSelenium
- BundleSink