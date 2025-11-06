---
id: TD-191
title: "**1.12.A Canon & invariants**"
source_doc: "TechDevBlueprint.docx"
source_path: "docs\blueprints\tech\TD-191-112a-canon-invariants\TD-191-overview.md"
parent_id: 
anchor: "TD-191"
checksum: "sha256:a26f6f17595cdd0c11ab4842285a0e8c4ac8df5cc1632fd6c48889ed7e9135b1"
last_modified: "2025-11-06T20:40:46Z"
doc_kind: "TD"
h_level: 2
---
<a id="TD-191"></a>
## **1.12.A Canon & invariants**

1142. **Amplify Gen 2 only (code‑first)**: infrastructure expressed in CDK within the repo; no Amplify Classic “console‑first” projects. We add guardrails to prevent accidental Classic usage (see §1.12.D).
1143. **Serverless by default** for elasticity and cost: Aurora Serverless v2 for relational, DynamoDB for hot‑path messaging, Lambda/AppSync for compute, S3/CloudFront for media, Step Functions for sagas.
1144. **One source of truth (IaC)**: every resource is created via CDK/Amplify Gen 2 stacks in Git; no click‑ops in prod.
1145. **Multi‑environment** (dev, stage, prod) with separate AWS accounts, least privilege, and per‑env DNS.
1146. **Security & privacy by design**: KMS, WAF, VPC boundaries, least‑priv IAM, PII minimization, age‑gate/safe‑mode enforcement server‑side.
1147. **Cost controls baked in**: budgets/alerts, right‑sized defaults, lifecycle policies, OCU/RCU caps, and CI step gates when a change increases spend.
