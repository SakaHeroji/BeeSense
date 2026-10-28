---
type: community
cohesion: 0.38
members: 7
---

# Parser DOM Terbatas

**Cohesion:** 0.38 - loosely connected
**Members:** 7 nodes

## Members
- [[.handle_data()]] - code - Reddit/crawl_reddit_single.py
- [[.handle_endtag()]] - code - Reddit/crawl_reddit_single.py
- [[.handle_startendtag()]] - code - Reddit/crawl_reddit_single.py
- [[.handle_starttag()]] - code - Reddit/crawl_reddit_single.py
- [[BoundedDom]] - code - Reddit/crawl_reddit_single.py
- [[HTMLParser]] - code
- [[Small serialised-DOM reader, not a browser or full HTML5 repair engine.]] - rationale - Reddit/crawl_reddit_single.py

## Live Query (requires Dataview plugin)

```dataview
TABLE source_file, type FROM #community/Parser_DOM_Terbatas
SORT file.name ASC
```

## Connections to other communities
- 3 edges to [[_COMMUNITY_Validasi Redirect dan Kesalahan]]
- 1 edge to [[_COMMUNITY_Parser dan Runner Reddit]]
- 1 edge to [[_COMMUNITY_Akses dan Parsing HTML]]

## Top bridge nodes
- [[BoundedDom]] - degree 9, connects to 3 communities
- [[.handle_starttag()]] - degree 4, connects to 1 community