---
id: TD-356
title: "**1.18.B Identity & access management (IAM) boundaries**"
source_doc: "TechDevBlueprint.docx"
source_path: "docs\blueprints\tech\TD-356-118b-identity-access-management-iam-boundaries\TD-356-overview.md"
parent_id: 
anchor: "TD-356"
checksum: "sha256:66e7bc9dde184636cd0bc325cd3a26fe3568b3924567d5e726485e1020252d57"
last_modified: "2025-11-06T20:40:46Z"
doc_kind: "TD"
h_level: 2
---
<a id="TD-356"></a>
## **1.18.B Identity & access management (IAM) boundaries**

**Recommended path:** *security/policies/iam-boundaries.md*

- Accounts & org

  - AWS **Organizations** with SCPs: deny *\*:\** at root, deny public S3 unless explicitly allowed, deny KMS key deletion.
  - Separate accounts: *rastup-dev*, *rastup-stage*, *rastup-prod*, plus *rastup-shared* (log archive) and *rastup-security*.

- Roles

  - **Workload roles**: per Lambda/service with minimal permissions (AppSync resolver roles; S3 prefixes; DynamoDB tables).
  - **Human roles**: *AdminLimited* (break‑glass), *OpsReadOnly*, *Analyst*, *SecurityEngineer*. MFA enforced; session limits (1–4h).
  - **JIT elevation** via IAM Identity Center (formerly SSO) with approval; all admin actions audited.

**Inline artifact — example least‑priv Dynamo policy**  
**Path:** *security/iam/policies/dynamo-least-priv.json*

*{*  
*"Version":"2012-10-17",*  
*"Statement":\[*  
*{"Effect":"Allow","Action":\["dynamodb:PutItem","dynamodb:GetItem","dynamodb:UpdateItem"\],*  
*"Resource":"arn:aws:dynamodb:us-east-1:{{account}}:table/fansub_entitlement_cache",*  
*"Condition":{"ForAllValues:StringEquals":{"dynamodb:LeadingKeys":\["USER#"\]}}}*  
*\]*  
*}*
