---
id: TD-489
title: "**1.26.3 App shell & security**"
source_doc: "TechDevBlueprint.docx"
source_path: "docs\blueprints\tech\TD-489-1263-app-shell-security\TD-489-overview.md"
parent_id: 
anchor: "TD-489"
checksum: "sha256:f73e5c370ecdb7969cf30e37b284053c733b203d84317c8b1eaee726543a9e8c"
last_modified: "2025-11-06T20:40:46Z"
doc_kind: "TD"
h_level: 2
---
<a id="TD-489"></a>
## **1.26.3 App shell & security**

- **Admin app**: Next.js, SSR disabled (pure client + APIs) to minimize PII leakage.
- **Network**: CloudFront → WAF (bot/rate rules) → Admin API Gateway (JWT from SSO).
- **IP allowlist** for office/VPN; optional hardware key (WebAuthn) step‑up for finance/disputes.
- **Break‑glass**: short‑lived *super_admin* elevations require a ticket id + reason; auto‑revoked after TTL.
