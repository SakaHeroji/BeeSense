---
source_file: "requirements/dashboard.txt"
type: "rationale"
community: "app.py"
location: "L1-L14"
tags:
  - graphify/rationale
  - graphify/EXTRACTED
  - community/apppy
---

# Dashboard-only artifact/explanation/UI dependency boundary

## Connections
- [[NumPy 2.2.6 below Python 3.14;2.3.5 on Python 3.14 and later]] - `references` [EXTRACTED]
- [[Relocated dashboard image uses root Streamlit shim and runtime-only wheels]] - `references` [EXTRACTED]
- [[Root Cloud requirements include relocated dashboard-only runtime]] - `references` [EXTRACTED]
- [[Root streamlit_apps.py delegates to Dashboard.app]] - `references` [EXTRACTED]

#graphify/rationale #graphify/EXTRACTED #community/apppy