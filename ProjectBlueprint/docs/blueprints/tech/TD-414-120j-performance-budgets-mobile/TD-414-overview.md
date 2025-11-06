---
id: TD-414
title: "**1.20.J Performance budgets (mobile)**"
source_doc: "TechDevBlueprint.docx"
source_path: "docs\blueprints\tech\TD-414-120j-performance-budgets-mobile\TD-414-overview.md"
parent_id: 
anchor: "TD-414"
checksum: "sha256:21e1b7d555659db02aa812cb48e0ae214689dfd30f52739a2017776aadaad31c"
last_modified: "2025-11-06T20:40:46Z"
doc_kind: "TD"
h_level: 2
---
<a id="TD-414"></a>
## **1.20.J Performance budgets (mobile)**

**Targets (mobile P75):** LCP ≤ 2.5s (PWA), INP ≤ 200ms, TTI ≤ 3.5s, bundle ≤ 900KB total on first load (GZIP).

**Tactics:**

- Code‑split heavy editors/maps; prefetch next screens on tap‑down; image lazy‑load with low‑quality placeholders; *fetchpriority="high"* for LCP hero; local fonts with *font-display: swap*.
- For RN: Hermes engine, RAM bundles, Flipper disabled in prod, animation worklets only where needed.

**Budget file**  
**Recommended path:** *observability/budgets/mobile.json*

*{ "pwaFirstLoadKB": 900, "pwaScriptKB": 160, "pwaImgPolicy": "webp/avif", "rnBundleKB": 420 }*
