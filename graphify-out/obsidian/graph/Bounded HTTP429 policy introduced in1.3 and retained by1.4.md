---
source_file: "docs/crawler/SOCIAL_CRAWLER.md"
type: "rationale"
community: "Community None"
location: "## Cooldown HTTP 429 untuk crawl berikutnya"
tags:
  - graphify/rationale
  - graphify/EXTRACTED
  - community/Community_None
---

# Bounded HTTP429 policy introduced in1.3 and retained by1.4

## Connections
- [[.run()]] - `implements` [INFERRED]
- [[Bounded 1.3 cooldown applied to user-authorized continuation 04]] - `references` [EXTRACTED]
- [[Configured Reddit policy cooldown360seconds]] - `conceptually_related_to` [INFERRED]
- [[Configured Reddit retry capthreeperrun]] - `conceptually_related_to` [INFERRED]
- [[Documented coordinator 1.3 cooldown 360 seconds with at most 3 retries]] - `references` [EXTRACTED]
- [[Explicit partial export and qualified-post shortfall after acquisition]] - `references` [EXTRACTED]
- [[Historical continuation 04 applied 1.3 cooldown after explicit user instruction]] - `references` [EXTRACTED]
- [[Observed recovery-notice interval≈331.315 seconds is not a server minimum]] - `references` [EXTRACTED]
- [[Obsidian records bounded retry policy and chronological authorization]] - `semantically_similar_to` [INFERRED]
- [[Omitted retry config defaults to zero retries for existing callers]] - `references` [EXTRACTED]
- [[One-operation round-robin scheduler with shared 10800-second deadline]] - `references` [EXTRACTED]
- [[Persist actual 429 finish timestamps, cooldown deadline and retry decisions]] - `references` [EXTRACTED]
- [[Receipt retry_after_seconds60 may be Chrome parser fallback]] - `references` [EXTRACTED]
- [[Retain the same failed Reddit operation until cooldown expires]] - `references` [EXTRACTED]
- [[Round-robin advances YouTube while Reddit waits for readiness]] - `references` [EXTRACTED]
- [[Standalone runner stops 429; coordinator 1.3 supports bounded cooldown]] - `references` [EXTRACTED]
- [[Unrepresentable or deadline-exceeding source wait forbids retry and preserves partial data]] - `conceptually_related_to` [INFERRED]

#graphify/rationale #graphify/EXTRACTED #community/Community_None