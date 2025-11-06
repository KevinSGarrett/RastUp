---
id: TD-25
title: "**1.3.F Amendments, extras & overtime**"
source_doc: "TechDevBlueprint.docx"
source_path: "docs\blueprints\tech\TD-25-13f-amendments-extras-overtime\TD-25-overview.md"
parent_id: 
anchor: "TD-25"
checksum: "sha256:6ad3898cfa86b6c60a15a24ae3dbbb070715b92a74699d2ec0f95d4af51fa8b3"
last_modified: "2025-11-06T20:40:46Z"
doc_kind: "TD"
h_level: 2
---
<a id="TD-25"></a>
## **1.3.F Amendments, extras & overtime**

- **Change Orders** produce *amendment* rows with deltas; tax re‑quoted; receipts updated.
- **Overtime**: triggered from thread/project during/after the session; priced per policy; may generate an extra **PaymentIntent** or **incremental capture** (cards) if allowed; for ACH, create a second charge.
