---
id: TD-351
title: "**1.17.14 Risk Register & Mitigations**"
source_doc: "TechDevBlueprint.docx"
source_path: "docs\blueprints\tech\TD-351-11714-risk-register-mitigations\TD-351-overview.md"
parent_id: 
anchor: "TD-351"
checksum: "sha256:67ddc5f17cc57580c1d3ee801a9d84cc8fac8dd69fabeb2d148a6d7d3585f4d4"
last_modified: "2025-11-06T20:40:46Z"
doc_kind: "TD"
h_level: 2
---
<a id="TD-351"></a>
## **1.17.14 Risk Register & Mitigations**

- **Duplicate content** via tracking params → mitigated by canonical middleware + 301.
- **Faceted crawl bloat** → *noindex, follow* + allowlist + self‑canonical.
- **Accidental 18+ leakage** → centralized SFW image service for OG/JSON‑LD; tests in CI.
- **Thin pages** (empty profiles) → hold *noindex* until profile meets completeness threshold.
- **CLS regressions** → enforce width/height on images; block unstyled font flashes.
