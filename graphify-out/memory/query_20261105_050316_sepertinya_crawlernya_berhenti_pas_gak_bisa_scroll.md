---
type: "query"
date: "2026-11-05T05:03:16.850165+00:00"
question: "sepertinya crawlernya berhenti pas gak bisa scrolling komentar lanjutan dibawah gak?"
contributor: "graphify"
outcome: "useful"
source_nodes: ["pageOperation()", "runTask()", "ChromeLiveWorker"]
---

# Q: sepertinya crawlernya berhenti pas gak bisa scrolling komentar lanjutan dibawah gak?

## Answer

Expanded from original query via graph vocabulary: [tiktok, comment, scroll, pagination, reply, expand, idle, page, operation]. Traversal identified pageOperation core.mjs L214 and runTask background.mjs. Source and offline tests reproduced reply-control starvation: clearing all blocked controls every3idle rounds can repeat unresponsive controls before scrolling; same-label controls can inherit wrongparentkey; broad wrappers can win over actual comment list. Prepared and tested Connector1.2.2 build20261105-reply-scroll-v4: per-control retry plus guaranteed scroll after3unproductive clicks, correct parent/position key, prefer actual list, rewind only afterbottom. This UI action cadence does not cap comments or terminate collection. 11Node,6offlineDOM,53Python tests pass. UserReloaded and actualbridgeverified1.2.2/protocolsource-pagination-v3 around11:56WIB on sameactive run6cd0ad73/deadline14:25. Manualclick earlier restored live91comments51replies to155comments81replies on source239;236doesnotproveeverylistedcommentavailable. At11:55completedoperations4posts302comments363replies;ongoingnot1000success. Graph2331nodes4784edges,2500Obsidian notes;31ASTreferences unresolved aftermerge.

## Outcome

- Signal: useful

## Source Nodes

- pageOperation()
- runTask()
- ChromeLiveWorker