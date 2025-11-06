---
id: TD-208
title: "**1.12.R Acceptance criteria (mark §1.12 FINAL only when ALL true)**"
source_doc: "TechDevBlueprint.docx"
source_path: "docs\blueprints\tech\TD-208-112r-acceptance-criteria-mark-112-final-only-when-all-true\TD-208-overview.md"
parent_id: 
anchor: "TD-208"
checksum: "sha256:ff8aefb7003adb0a61a07177dbf37d63a4031655c64cc2a936a1d2a3bdfcd9c8"
last_modified: "2025-11-06T20:40:46Z"
doc_kind: "TD"
h_level: 2
---
<a id="TD-208"></a>
## **1.12.R Acceptance criteria (mark §1.12 FINAL only when ALL true)**

1246. **Amplify Gen 2** stacks synth and deploy cleanly; CI fails any PR that introduces Classic artifacts.
1247. **Three environments** live with separate accounts, DNS, certs, and secrets; branch mapping works; previews auto‑expire.
1248. **Security**: WAF enabled, IAM least‑priv, KMS on RDS/DDB/S3, no public RDS, TLS enforced, Secrets Manager used.
1249. **Data**: Aurora + Dynamo tables created; backups & retention policies; migrations framework in place.
1250. **Observability**: dashboards/alerts deployed; traces flow end‑to‑end; PII scrubbing verified.
1251. **Cost**: budgets & alarms active; lifecycle policies in place; OCU/ACU/RCU caps; NAT egress minimal.
1252. **DR**: PITR validated; restore drill passes in stage within RTO.
1253. **DX**: local mocks, seed data, and codegen working; CI green; cost‑diff gate functional.
