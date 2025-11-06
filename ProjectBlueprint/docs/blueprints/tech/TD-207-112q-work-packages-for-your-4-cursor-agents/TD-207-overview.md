---
id: TD-207
title: "**1.12.Q Work packages (for your 4 Cursor agents)**"
source_doc: "TechDevBlueprint.docx"
source_path: "docs\blueprints\tech\TD-207-112q-work-packages-for-your-4-cursor-agents\TD-207-overview.md"
parent_id: 
anchor: "TD-207"
checksum: "sha256:bc880bb6e786e016b644bbdbc02982e4907c8a7cb3adf8a8d28179022de8ea3c"
last_modified: "2025-11-06T20:40:46Z"
doc_kind: "TD"
h_level: 2
---
<a id="TD-207"></a>
## **1.12.Q Work packages (for your 4 Cursor agents)**

**Agent B — Infra/IaC**

- WP‑INF‑01: Amplify Gen 2 CDK stacks (Auth, API, Data, Media, Workflow, Observability).
- WP‑INF‑02: Multi‑account bootstrap, DNS, ACM certs, WAF.
- WP‑INF‑03: Budgets/alerts; cost gate in CI; cdk‑nag rules.

**Agent C — Data/Runtime**

- WP‑DATA‑01: Aurora cluster + migrations framework; Dynamo tables with TTL/RCU/WCU.
- WP‑DATA‑02: Search stack (Typesense baseline + adapter to OpenSearch Serverless).
- WP‑DATA‑03: Step Functions templates & EventBridge buses.

**Agent A — Web/Hosting**

- WP‑WEB‑INF‑01: Amplify Hosting setup w/ branch mapping, ISR/SSR config, edge rewrites.
- WP‑WEB‑INF‑02: Signed S3 uploads with scoped IAM; image proxy/resizer at edge.

**Agent D — SecOps/Observability**

- WP‑SEC‑01: WAF managed rules + custom IP rate limits; Secrets Manager + rotation.
- WP‑OBS‑01: CloudWatch dashboards/alarms; X‑Ray traces; log scrubbing; audit sinks.
- WP‑DR‑01: DR runbook & drill scripts; snapshot retention; restore tests.
