---
id: TD-531
title: "**1.28.12 CI/CD & access controls**"
source_doc: "TechDevBlueprint.docx"
source_path: "docs\blueprints\tech\TD-531-12812-cicd-access-controls\TD-531-overview.md"
parent_id: 
anchor: "TD-531"
checksum: "sha256:bcdc53c1530249069b5a710d4785520c4aef8ca4b8698b60d9d4c4c26b6f47ef"
last_modified: "2025-11-06T20:40:46Z"
doc_kind: "TD"
h_level: 2
---
<a id="TD-531"></a>
## **1.28.12 CI/CD & access controls**

- Admin app deployed to a dedicated Amplify/CloudFront stack; WAF and IP allowlist required.
- SSO enforced for all routes; break‑glass elevation requires ticket id; logs routed to centralized logging with retention.
