---
id: TD-512
title: "**1.27.11 Core Web Vitals budgets & enforcements**"
source_doc: "TechDevBlueprint.docx"
source_path: "docs\blueprints\tech\TD-512-12711-core-web-vitals-budgets-enforcements\TD-512-overview.md"
parent_id: 
anchor: "TD-512"
checksum: "sha256:c711e8844b512011d4c54c4e9949d2f8a6f03a529fe640b21e2a3be8aaa66a20"
last_modified: "2025-11-06T20:40:46Z"
doc_kind: "TD"
h_level: 2
---
<a id="TD-512"></a>
## **1.27.11 Core Web Vitals budgets & enforcements**

**Budgets (mobile P75):** LCP ≤ 2.5s, INP ≤ 200ms, CLS ≤ 0.1.  
**Build gate:** Lighthouse CI must pass budgets on key templates (home, city listing, profile, studio).  
**Runtime beacons:** send CWV field data via *web-vitals* to our analytics (§1.13).  
**Tactics:**

- Preconnect DNS for Typesense/AppSync endpoints; lazyload below‑fold images; use *fetchpriority="high"* for LCP media; defer non‑critical JS; no third‑party tag bloat.

**Recommended path:** *observability/budgets/web.json*

*{"lcpMs": 2500, "inpMs": 200, "cls": 0.1, "maxScriptKb": 160, "maxFirstLoadKb": 900}*
