---
type: community
cohesion: 0.15
members: 14
---

# PRD Workspace Crawler

**Cohesion:** 0.15 - loosely connected
**Members:** 14 nodes

## Members
- [[Backend PRD is not written; APIworker services remain proposed]] - document - PRD/PRD Backend/README.md
- [[Backend wrapper must translate local WIB dates and TypeScript field names]] - rationale - Crawler/Frontend/docs/API_CONTRACT.md
- [[Expected typed frontend API contract; backend implementation pending]] - document - Crawler/Frontend/docs/API_CONTRACT.md
- [[Fresh server validation and one idempotency key precede job start]] - rationale - PRD/PRD Frontend/PRD Frontend Crawler.md
- [[Increasing snapshotVersion and server-owned actions drive reconciliation]] - rationale - Crawler/Frontend/docs/API_CONTRACT.md
- [[Project-prefixed cookie-session API requires server CORSCSRFaccess controls]] - rationale - Crawler/Frontend/docs/API_CONTRACT.md
- [[Proposed persistent Python worker and authorized CAPTCHA browser bridge]] - rationale - PRD/PRD Backend/README.md
- [[Proposed server session, role, project isolation and idempotency]] - rationale - PRD/PRD Backend/README.md
- [[Proposed survey transactions, immutable datasets and operational audit]] - rationale - PRD/PRD Backend/README.md
- [[Proposed worker survives tab close; reconnect reconciles snapshots]] - rationale - PRD/PRD Frontend/PRD Frontend Crawler.md
- [[Safe structured errors distinguish API429 from worker-platform429]] - rationale - Crawler/Frontend/docs/API_CONTRACT.md
- [[Server history pagination, SSE, templates and organizational login remain future]] - concept - Crawler/Frontend/docs/API_CONTRACT.md
- [[Survey answers avoid URLlocalStorage;safe text and CSV formula handling]] - rationale - Crawler/Frontend/README.md
- [[Typed planjob requests bind plan IDs, idempotency and safe stop]] - concept - Crawler/Frontend/docs/API_CONTRACT.md

## Live Query (requires Dataview plugin)

```dataview
TABLE source_file, type FROM #community/PRD_Workspace_Crawler
SORT file.name ASC
```

## Connections to other communities
- 5 edges to [[_COMMUNITY_PRD Workspace Crawler_3]]
- 3 edges to [[_COMMUNITY_PRD Workspace Crawler_1]]
- 2 edges to [[_COMMUNITY_Snapshot NLP dan Arsip_4]]
- 2 edges to [[_COMMUNITY_PRD Workspace Crawler_4]]
- 1 edge to [[_COMMUNITY_PRD Workspace Crawler]]

## Top bridge nodes
- [[Expected typed frontend API contract; backend implementation pending]] - degree 14, connects to 4 communities
- [[Backend PRD is not written; APIworker services remain proposed]] - degree 6, connects to 2 communities
- [[Proposed persistent Python worker and authorized CAPTCHA browser bridge]] - degree 3, connects to 1 community
- [[Proposed worker survives tab close; reconnect reconciles snapshots]] - degree 3, connects to 1 community
- [[Survey answers avoid URLlocalStorage;safe text and CSV formula handling]] - degree 2, connects to 1 community