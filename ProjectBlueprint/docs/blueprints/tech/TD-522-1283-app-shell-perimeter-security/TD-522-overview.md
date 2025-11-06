---
id: TD-522
title: "**1.28.3 App shell & perimeter security**"
source_doc: "TechDevBlueprint.docx"
source_path: "docs\blueprints\tech\TD-522-1283-app-shell-perimeter-security\TD-522-overview.md"
parent_id: 
anchor: "TD-522"
checksum: "sha256:399cdbbc45ed1e3008e069d4660699cc3466ebe7c4d5aee5faee0fb0ca09da72"
last_modified: "2025-11-06T20:40:46Z"
doc_kind: "TD"
h_level: 2
---
<a id="TD-522"></a>
## **1.28.3 App shell & perimeter security**

- **Network:** CloudFront → WAF (bot/rate) → Admin API Gateway (JWT from SSO) → AppSync/Lambda.
- **IP allowlist** for office/VPN subnets; break‑glass path requires ticket id + reason and auto‑revokes after TTL.
- **No SSR** for admin pages (client‑side only) to minimize accidental PII caching.
