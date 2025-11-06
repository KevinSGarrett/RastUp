---
id: TD-526
title: "**1.28.7 JIT access & privacy guardrails**"
source_doc: "TechDevBlueprint.docx"
source_path: "docs\blueprints\tech\TD-526-1287-jit-access-privacy-guardrails\TD-526-overview.md"
parent_id: 
anchor: "TD-526"
checksum: "sha256:b5f3e67a096e760847e3c6f772b6224d6cc2ee5fe0110ca36479b897335a086f"
last_modified: "2025-11-06T20:40:46Z"
doc_kind: "TD"
h_level: 2
---
<a id="TD-526"></a>
## **1.28.7 JIT access & privacy guardrails**

- Case‑bound scopes grant temporary read (and limited reply where policy allows) to specific threads/media.
- Sensitive artifacts (IDs, invoices, door codes) are served only by short‑TTL, single‑use signed URLs; downloads counted and audited.
- All access writes an *admin_audit* record with case id, IP, UA, and reason.
