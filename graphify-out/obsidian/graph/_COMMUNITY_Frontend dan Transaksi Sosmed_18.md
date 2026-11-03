---
type: community
cohesion: 0.67
members: 3
---

# Frontend dan Transaksi Sosmed

**Cohesion:** 0.67 - moderately connected
**Members:** 3 nodes

## Members
- [[Default publik 1000 post, durasi dan cap komentar null]] - concept - Crawler/Frontend/src/shared/crawler-defaults.json
- [[Snapshot publik crawler-defaults.json]] - document - Crawler/Frontend/src/shared/crawler-defaults.json
- [[Snapshot storage Excel, hostport dan nama env tanpa DSN]] - concept - Crawler/Frontend/src/shared/crawler-defaults.json

## Live Query (requires Dataview plugin)

```dataview
TABLE source_file, type FROM #community/Frontend_dan_Transaksi_Sosmed
SORT file.name ASC
```
