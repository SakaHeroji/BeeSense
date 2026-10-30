---
source_file: "deployment/docker/Dockerfile.dashboard"
type: "rationale"
community: "Community None"
location: "L1-L23"
tags:
  - graphify/rationale
  - graphify/EXTRACTED
  - community/Community_None
---

# Relocated dashboard image uses root Streamlit shim and runtime-only wheels

## Connections
- [[Dashboard build context includes root shim and artifact-reader packages]] - `references` [EXTRACTED]
- [[Dashboard-only artifactexplanationUI dependency boundary]] - `references` [EXTRACTED]
- [[Root Docker context allowlist for relocated dashboard runtime]] - `references` [EXTRACTED]
- [[app.py]] - `references` [EXTRACTED]
- [[streamlit_apps.py]] - `references` [EXTRACTED]

#graphify/rationale #graphify/EXTRACTED #community/Community_None