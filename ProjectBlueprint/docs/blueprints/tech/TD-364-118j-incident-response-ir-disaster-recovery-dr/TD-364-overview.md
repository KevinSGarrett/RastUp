---
id: TD-364
title: "**1.18.J Incident response (IR) & disaster recovery (DR)**"
source_doc: "TechDevBlueprint.docx"
source_path: "docs\blueprints\tech\TD-364-118j-incident-response-ir-disaster-recovery-dr\TD-364-overview.md"
parent_id: 
anchor: "TD-364"
checksum: "sha256:ca9a6bb08e549bf1e9fcd8347354f3ed35fbabfd17eec621f5ade3046cf6b413"
last_modified: "2025-11-06T20:40:46Z"
doc_kind: "TD"
h_level: 2
---
<a id="TD-364"></a>
## **1.18.J Incident response (IR) & disaster recovery (DR)**

- **IR team & runbooks**: security@ group, Slack \#secur‑incidents (private), paging via SNS.

- **Playbooks**: credential leak, PII exposure, DDOS, data corruption, provider breach.

- **Forensics**: isolate role credentials; retrieve CloudTrail & app logs; snapshot affected S3 prefixes with Write Once retention.

- **DR**:

  - **Backups**: Aurora PITR, daily snapshots; Dynamo PITR; S3 versioning + Object Lock for evidence.
  - **RPO/RTO**: core web ≤ 15m RPO / ≤ 60m RTO; payments webhooks ≤ 5m / 15m.
  - **Regional**: consider cross‑region S3 replication for evidence vault; Aurora global DB if required later.

**Inline artifact — IR ticket template**  
**Path:** *security/ir/ticket-template.md*

*- Summary:*  
*- Detected by:*  
*- Impacted data/classes:*  
*- Timeline:*  
*- Containment:*  
*- Eradication:*  
*- Recovery:*  
*- Customer comms needed? Y/N*  
*- Follow-up CAPA items:*
