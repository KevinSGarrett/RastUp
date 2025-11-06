---
id: TD-487
title: "**1.26.1 Canon & invariants**"
source_doc: "TechDevBlueprint.docx"
source_path: "docs\blueprints\tech\TD-487-1261-canon-invariants\TD-487-overview.md"
parent_id: 
anchor: "TD-487"
checksum: "sha256:379e0dcbd69edaa70a240c0507691bad6cb09088da9b663b2a8c11dd79b1b3f9"
last_modified: "2025-11-06T20:40:46Z"
doc_kind: "TD"
h_level: 2
---
<a id="TD-487"></a>
## **1.26.1 Canon & invariants**

2371. **Least privilege + JIT access.** Role‑based access (RBAC), per‑action checks, and **just‑in‑time case access** for message/content review.
2372. **Immutable audit.** Every admin action writes to an append‑only audit table and an object‑locked S3 stream (see §1.18).
2373. **Separation of duties.** Finance permissions are distinct from Trust & Safety (T&S) and Content Ops.
2374. **Privacy.** Admins view PII only when case‑bound and time‑boxed; all access is logged.
2375. **Cost.** One lightweight **Admin Next.js app** behind CloudFront + IP allowlist + SSO; serverless APIs (AppSync/Lambda), pay‑per‑use data access.
