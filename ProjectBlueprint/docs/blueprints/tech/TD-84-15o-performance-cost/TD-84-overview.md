---
id: TD-84
title: "**1.5.O Performance & cost**"
source_doc: "TechDevBlueprint.docx"
source_path: "docs\blueprints\tech\TD-84-15o-performance-cost\TD-84-overview.md"
parent_id: 
anchor: "TD-84"
checksum: "sha256:b36a19055e374768126ad191206a5d33f45cbda8a4ed28ea23dfa7c96e07739d"
last_modified: "2025-11-06T20:40:46Z"
doc_kind: "TD"
h_level: 2
---
<a id="TD-84"></a>
## **1.5.O Performance & cost**

- Rendering happens in Lambda with **concurrency caps**; fall back to a headless render service if pages \> threshold.
- E‑sign costs are **per envelope**; we minimize packs to one Talent pack and one Studio pack at MVP.
- S3 + lifecycle rules keep storage costs low; PDFs are compacted (fonts embedded once) and gzipped for transport.
