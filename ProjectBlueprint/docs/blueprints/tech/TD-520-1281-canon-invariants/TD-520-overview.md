---
id: TD-520
title: "**1.28.1 Canon & invariants**"
source_doc: "TechDevBlueprint.docx"
source_path: "docs\blueprints\tech\TD-520-1281-canon-invariants\TD-520-overview.md"
parent_id: 
anchor: "TD-520"
checksum: "sha256:ba16f446162c0451225772b180686872fefca112c1946fbf7c70e46ed560f5af"
last_modified: "2025-11-06T20:40:46Z"
doc_kind: "TD"
h_level: 2
---
<a id="TD-520"></a>
## **1.28.1 Canon & invariants**

2510. **Least privilege + JIT access.** Roles narrowly scoped; message/media viewing requires **case‑bound** time‑boxed access.
2511. **Immutable audit.** Every admin action is recorded in Aurora **and** appended to S3 with **Object Lock (WORM)**.
2512. **Separation of duties.** Finance vs Trust & Safety (T&S) vs Support vs Content Ops vs Search Curation vs Docs Admin.
2513. **Privacy by design.** Sensitive artifacts only via short‑TTL, single‑use signed URLs; all access audited.
2514. **Cost posture.** One Next.js Admin app behind CloudFront + WAF + IP allowlist; serverless APIs (AppSync/Lambda/Data API).
