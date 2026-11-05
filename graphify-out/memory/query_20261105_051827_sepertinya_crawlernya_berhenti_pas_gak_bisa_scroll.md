---
type: "query"
date: "2026-11-05T05:18:27.173025+00:00"
question: "sepertinya crawlernya berhenti pas gak bisa scrolling komentar lanjutan dibawah gak?"
contributor: "graphify"
outcome: "corrected"
correction: "Per-control retry/forcedscroll alone does not solve offscreen reply controls: getClientRects remains nonempty when clipped.1.2.3 adds viewport plus ancestor-clipping checks. Offlinepass does not establish live success; require actual1.2.3handshake and liveprogress."
source_nodes: ["pageOperation()", "runTask()", "ChromeLiveWorker"]
---

# Q: sepertinya crawlernya berhenti pas gak bisa scrolling komentar lanjutan dibawah gak?

## Answer

Expanded via graph vocabulary: [tiktok, comment, scroll, pagination, reply, expand, idle, page, operation]. Follow-up corrects prior incomplete diagnosis.1.2.2 has per-control retries and guaranteed scrolling, but offline viewport regression still selects old offscreen reply control and scrollIntoView jumpsbacktop.1.2.3 fixes by intersecting buttonrectangle withwindow andclipping ancestors; popup displayscounts/navigation.7offlineDOM/11Node/53Python tests pass. UseraskedtoReload1.2.3;actualbridge lastverified1.2.2at12:10WIB. Active3hdeadline14:25 unchanged. Fourcompletedposts302comments363replies,current19comments74repliesonsource273 arepartial,not1000successorallcomments. Graph2340nodes4799edges2504Obsidian notes;31ASTreferences unresolved. No migration required; Docker/native image notrebuilt, noStreamlitdeploy.

## Outcome

- Signal: corrected
- Correction: Per-control retry/forcedscroll alone does not solve offscreen reply controls: getClientRects remains nonempty when clipped.1.2.3 adds viewport plus ancestor-clipping checks. Offlinepass does not establish live success; require actual1.2.3handshake and liveprogress.

## Source Nodes

- pageOperation()
- runTask()
- ChromeLiveWorker