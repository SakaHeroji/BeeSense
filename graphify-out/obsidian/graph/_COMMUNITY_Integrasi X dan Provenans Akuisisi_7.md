---
type: community
cohesion: 0.25
members: 8
---

# Integrasi X dan Provenans Akuisisi

**Cohesion:** 0.25 - loosely connected
**Members:** 8 nodes

## Members
- [[1.800 detik target 1.000 post 10 balasan]] - concept - config/twitter_crawler.json
- [[Allowlist Docker tanpa auth dan sesi]] - rationale - deployment/docker/Dockerfile.twitter.dockerignore
- [[Image Twitter Python 3.12 UID 10001]] - concept - deployment/docker/Dockerfile.twitter
- [[Jeda 5 dan 15 detik limiter window per operasi dan cap harian 120]] - concept - config/twitter_crawler.json
- [[Preset percobaan Twitter 30 menit]] - concept - config/twitter_crawler.json
- [[Query pendidikan Indonesia jendela tujuh hari]] - concept - config/twitter_crawler.json
- [[Scweet 5.8.2]] - concept - requirements/twitter.txt
- [[openpyxl 3.1.5]] - concept - requirements/twitter.txt

## Live Query (requires Dataview plugin)

```dataview
TABLE source_file, type FROM #community/Integrasi_X_dan_Provenans_Akuisisi
SORT file.name ASC
```
