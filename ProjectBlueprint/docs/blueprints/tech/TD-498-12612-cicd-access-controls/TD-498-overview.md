---
id: TD-498
title: "**1.26.12 CI/CD & access controls**"
source_doc: "TechDevBlueprint.docx"
source_path: "docs\blueprints\tech\TD-498-12612-cicd-access-controls\TD-498-overview.md"
parent_id: 
anchor: "TD-498"
checksum: "sha256:efceb139af58f3a8a64ff6739e104c333eacc81d307bade9b6ccc5a5458a39f0"
last_modified: "2025-11-06T20:40:46Z"
doc_kind: "TD"
h_level: 2
---
<a id="TD-498"></a>
## **1.26.12 CI/CD & access controls**

- Admin app deploys to a separate Amplify environment / CloudFront distribution.
- SSO required for any access; WAF blocks public traffic; IP allowlist; rate‑limits.
- Secrets in AWS Secrets Manager; no admin credentials in code.
