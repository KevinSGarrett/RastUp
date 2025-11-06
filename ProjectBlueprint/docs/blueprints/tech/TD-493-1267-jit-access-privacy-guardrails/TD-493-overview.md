---
id: TD-493
title: "**1.26.7 JIT access & privacy guardrails**"
source_doc: "TechDevBlueprint.docx"
source_path: "docs\blueprints\tech\TD-493-1267-jit-access-privacy-guardrails\TD-493-overview.md"
parent_id: 
anchor: "TD-493"
checksum: "sha256:ed81c12da52a4f8b53c6fe56b0af2ad0cf6d94756a7c4ae181d22a734e300cf8"
last_modified: "2025-11-06T20:40:46Z"
doc_kind: "TD"
h_level: 2
---
<a id="TD-493"></a>
## **1.26.7 JIT access & privacy guardrails**

- **Case‑bound scopes**: to open any message or attachment, an admin must attach it to an **open case**; access grants are time‑boxed (e.g., 2 hours) and **auto‑revoked** when case status changes.
- View/download of sensitive artifacts (IDs, invoices, door codes) uses **signed, single‑use URLs** with short TTL.
- All views generate *admin_audit* entries with IP/UA and the case id.
