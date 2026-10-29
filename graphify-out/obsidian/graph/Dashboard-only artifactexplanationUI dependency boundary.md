---
source_file: "requirements-dashboard.txt"
type: "rationale"
community: "Community None"
location: "L1-L14"
tags:
  - graphify/rationale
  - graphify/EXTRACTED
  - community/Community_None
---

# Dashboard-only artifact/explanation/UI dependency boundary

## Connections
- [[Cloud root requirements now install dashboard-only dependencies]] - `references` [EXTRACTED]
- [[Docker runtime ARG selects Python 3.12 or3.14 and installs only root wheels]] - `references` [EXTRACTED]
- [[Historical Python 3.14.10 Cloud install failureONNX cp314 wheels and Numba support]] - `references` [EXTRACTED]
- [[Isolated dashboard-runtime matrix for Python 3.12 and3.14]] - `references` [EXTRACTED]
- [[NumPy 2.2.6 below Python 3.14;2.3.5 on Python 3.14 and later]] - `references` [EXTRACTED]
- [[PyArrow 24.0.0 matches Cloud guard for Arrowmimalloc threaded-import compatibility]] - `references` [EXTRACTED]
- [[Root Community Cloud requirements include only dashboard runtime]] - `references` [EXTRACTED]
- [[Saved-model dashboard uses a separate runtime;full refitting stays Python 3.12]] - `references` [EXTRACTED]

#graphify/rationale #graphify/EXTRACTED #community/Community_None