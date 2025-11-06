---
id: TD-201
title: "**1.12.K Security posture**"
source_doc: "TechDevBlueprint.docx"
source_path: "docs\blueprints\tech\TD-201-112k-security-posture\TD-201-overview.md"
parent_id: 
anchor: "TD-201"
checksum: "sha256:b76f5576fe14a976ccf26e7d8c4b3ecffcd3514c32847a2676b64213a1a06c9f"
last_modified: "2025-11-06T20:40:46Z"
doc_kind: "TD"
h_level: 2
---
<a id="TD-201"></a>
## **1.12.K Security posture**

- **Least‑privilege IAM** for each Lambda.
- **Secrets** in Secrets Manager; rotation policies; no secrets in env vars.
- **WAF** with bot control & rate limits (different thresholds for search, auth, checkout).
- **Abuse** mitigations: captcha challenges for signup bursts; email domain denylist; phone verification for payouts.
- **Backups & keys**: scheduled audits for restore drills and KMS key rotations.
