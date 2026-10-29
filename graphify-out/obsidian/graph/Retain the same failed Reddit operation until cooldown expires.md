---
source_file: "SOCIAL_CRAWLER.md"
type: "rationale"
community: "Community None"
location: "## Cooldown HTTP 429 untuk crawl berikutnya"
tags:
  - graphify/rationale
  - graphify/INFERRED
  - community/Community_None
---

# Retain the same failed Reddit operation until cooldown expires

## Connections
- [[.run()_1]] - `implements` [INFERRED]
- [[Per-run canonical root duplicate guard]] - `references` [EXTRACTED]
- [[SocialCrawler 1.3 bounded HTTP 429 cooldown policy]] - `references` [EXTRACTED]
- [[Unrepresentable or deadline-exceeding source wait forbids retry and preserves partial data]] - `conceptually_related_to` [INFERRED]

#graphify/rationale #graphify/INFERRED #community/Community_None