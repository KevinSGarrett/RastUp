---
id: TD-97
title: "**1.6.J Privacy & retention**"
source_doc: "TechDevBlueprint.docx"
source_path: "docs\blueprints\tech\TD-97-16j-privacy-retention\TD-97-overview.md"
parent_id: 
anchor: "TD-97"
checksum: "sha256:8f18219f87ba47ff1da1e2b708992703fcf83b6fefd3dc69aaf1062c70f2c56a"
last_modified: "2025-11-06T20:40:46Z"
doc_kind: "TD"
h_level: 2
---
<a id="TD-97"></a>
## **1.6.J Privacy & retention**

- **Store only** provider refs/state and non-PII summaries (age-verified boolean, adjudication summaries).
- No images/scans of IDs at rest in our DB/S3.
- Retention windows: IDV and BG statuses kept for 7 years or as required by policy; social snapshots roll daily with 30–90 day retention.

**Access control:**

- Trust data visible to user (their statuses) and Admin roles only; not exposed to other users.
- Audit logs for every access by Admin with reason.
