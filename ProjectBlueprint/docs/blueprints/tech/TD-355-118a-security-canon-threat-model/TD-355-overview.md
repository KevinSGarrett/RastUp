---
id: TD-355
title: "**1.18.A Security canon & threat model**"
source_doc: "TechDevBlueprint.docx"
source_path: "docs\blueprints\tech\TD-355-118a-security-canon-threat-model\TD-355-overview.md"
parent_id: 
anchor: "TD-355"
checksum: "sha256:7c19232c38eac62f981ab966a3b82581778e78db7e0a63bdea11ecfafda508ec"
last_modified: "2025-11-06T20:40:46Z"
doc_kind: "TD"
h_level: 2
---
<a id="TD-355"></a>
## **1.18.A Security canon & threat model**

1915. **Least privilege & zero trust.** Every call is authenticated and authorized; no “trusted subnet.”
1916. **Default‑deny at edges.** WAF blocks obvious bad traffic; API throttles by identity.
1917. **PII minimization.** Only store what we must; tokenize or hash where possible; keep PII out of logs.
1918. **Compartmentalization.** Separate AWS accounts per env (dev/stage/prod) and per blast radius (prod‑data, prod‑ops).
1919. **Tamper‑evident audit.** Immutable trails for money/IDV/policy actions.
1920. **Idempotence everywhere.** All webhooks & money operations idempotent (no double charges).
1921. **Cost aware.** Prefer managed services (Amplify, Cognito, AppSync, WAF, Security Hub) over self‑hosted appliances.
