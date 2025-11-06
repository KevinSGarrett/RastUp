---
id: TD-359
title: "**1.18.E Encryption (in transit & at rest)**"
source_doc: "TechDevBlueprint.docx"
source_path: "docs\blueprints\tech\TD-359-118e-encryption-in-transit-at-rest\TD-359-overview.md"
parent_id: 
anchor: "TD-359"
checksum: "sha256:2bcf3124c53b5c19e002ad0c5b2fb762b1e4626fe65543d1298dc18ec9bde067"
last_modified: "2025-11-06T20:40:46Z"
doc_kind: "TD"
h_level: 2
---
<a id="TD-359"></a>
## **1.18.E Encryption (in transit & at rest)**

- **TLS 1.2+** everywhere (CloudFront, ALB, AppSync). HSTS on apex.
- **At rest**: S3 SSE‑KMS; DynamoDB SSE‑KMS; Aurora **encrypted**; CloudWatch Logs encrypted; Athena workgroup encryption enforced.
- **Field‑level**: hash emails (*sha256(email.lower().trim())*), store last‑4 only for phone if needed; avoid plaintext PII in events.
- **Tokenization**: use surrogate keys (*usr\_*, *sp\_*, *fsc\_*) across domains.
