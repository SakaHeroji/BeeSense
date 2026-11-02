---
type: "query"
date: "2026-11-02T05:23:52.016484+00:00"
question: "coba jelaskan ini bagaimana caranya? apakah setidaknya pas crawling proses ini dilakukan?: penyaringan relevansi berdasarkan konteks sebelum clustering"
contributor: "graphify"
outcome: "useful"
source_nodes: ["KeywordMatcher", "SocialNLPClusterer", "SocialCrawler"]
---

# Q: coba jelaskan ini bagaimana caranya? apakah setidaknya pas crawling proses ini dilakukan?: penyaringan relevansi berdasarkan konteks sebelum clustering

## Answer

Expanded query via graph vocabulary: [keyword, filter, comment, root, relevance, sentence]. Graph traversal located KeywordMatcher, Comment sentence eligibility, SocialNLPClusterer and BundleSink. Verified source Crawler/Backend/social_export.py:243: _select checks root date and literal include/exclude matches on root title/text; related nonempty comments/replies are retained unless literal excluded terms match. Shared compact export at line185 also checks literal excludes for child text. KeywordMatcher at Crawler/Backend/Reddit/crawl_reddit_single.py:169 is casefolded literal matching, not semantic relevance classification. MachineLearning/social_nlp.py:274 prepares comment/reply sentences with length and cleanliness checks, not a contextual education-domain gate. Thus contextual relevance is currently not implemented even though acquisition keyword/date/exclusion filtering exists. Recommended design only: define the research scope; screen candidate roots during acquisition before costly comment retrieval when metadata is available; classify each comment/reply using its own text plus limited parent/root context without blindly inheriting relevance; retain relevant, irrelevant, generic-interaction and uncertain labels plus reasons/model version in an audit sidecar and preserve raw records. Separate contextual relevance eligibility from sentence topic embedding; contextual yes/no classifier is different from embedding the whole parent into every child. Before clustering, reassess existing corpus and segment mixed comments, retain relevant sentences, route uncertainty to review, calibrate thresholds on manually labeled examples, evaluate precision/recall separately from coherence. No code implementation or rerun requested.

## Outcome

- Signal: useful

## Source Nodes

- KeywordMatcher
- SocialNLPClusterer
- SocialCrawler