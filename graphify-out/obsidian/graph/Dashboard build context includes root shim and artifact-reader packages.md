---
source_file: "deployment/docker/Dockerfile.dashboard.dockerignore"
type: "rationale"
community: "app.py"
location: "L1-L18"
tags:
  - graphify/rationale
  - graphify/EXTRACTED
  - community/apppy
---

# Dashboard build context includes root shim and artifact-reader packages

## Connections
- [[Relocated dashboard image uses root Streamlit shim and runtime-only wheels]] - `references` [EXTRACTED]
- [[streamlit_apps.py]] - `references` [EXTRACTED]
- [[topic_narratives.py]] - `references` [EXTRACTED]

#graphify/rationale #graphify/EXTRACTED #community/apppy