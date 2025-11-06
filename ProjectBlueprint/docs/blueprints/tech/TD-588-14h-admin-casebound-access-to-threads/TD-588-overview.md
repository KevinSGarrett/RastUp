---
id: TD-588
title: "**1.4.H Admin case‑bound access to threads**"
source_doc: "TechDevBlueprint.docx"
source_path: "docs\blueprints\tech\TD-588-14h-admin-casebound-access-to-threads\TD-588-overview.md"
parent_id: 
anchor: "TD-588"
checksum: "sha256:8c46e05ffe29497c2378bd8b0336aceada7c95079aec67f37192767ef2e19e0a"
last_modified: "2025-11-06T20:40:46Z"
doc_kind: "TD"
h_level: 2
---
<a id="TD-588"></a>
## **1.4.H Admin case‑bound access to threads**

- **Case scope**: Admin sees only the threads tied to the case (dispute/safety).
- **JIT tokens**: time‑boxed read access; all views/actions written to the **audit trail** with reason codes.
- **PII redaction**: transient secrets (door codes, phone, emails) masked unless escalation level requires full view.
- **Actions**: mark as reviewed, apply holds, unblock, redact messages (legal), export evidence pack for chargeback.
