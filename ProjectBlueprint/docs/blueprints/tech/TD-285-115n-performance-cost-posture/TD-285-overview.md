---
id: TD-285
title: "**1.15.N Performance & cost posture**"
source_doc: "TechDevBlueprint.docx"
source_path: "docs\blueprints\tech\TD-285-115n-performance-cost-posture\TD-285-overview.md"
parent_id: 
anchor: "TD-285"
checksum: "sha256:f271859a46ee650881a7ef0eef63da0e98feff11638dadaf8beb8b0f752b2c50"
last_modified: "2025-11-06T20:40:46Z"
doc_kind: "TD"
h_level: 2
---
<a id="TD-285"></a>
## **1.15.N Performance & cost posture**

- **Ticketing** in Aurora (no external SaaS at launch).
- **Email bridge** via SES (inbound + outbound) to avoid Twilio SendGrid costs.
- **Storage**: S3 evidence with lifecycle; avoid storing large videos—store **manifests** and small screenshots.
- **Compute**: Lambda for parsers and automations; Step Functions for chargeback deadlines; no provisioned concurrency unless needed.
