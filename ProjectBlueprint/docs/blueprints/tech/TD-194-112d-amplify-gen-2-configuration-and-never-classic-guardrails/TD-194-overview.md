---
id: TD-194
title: "**1.12.D Amplify Gen 2 configuration (and “never Classic” guardrails)**"
source_doc: "TechDevBlueprint.docx"
source_path: "docs\blueprints\tech\TD-194-112d-amplify-gen-2-configuration-and-never-classic-guardrails\TD-194-overview.md"
parent_id: 
anchor: "TD-194"
checksum: "sha256:83de65de1b438795d9e6fb9bdb9f906db7db7a7ab70d25c53d9de6614be5545b"
last_modified: "2025-11-06T20:40:46Z"
doc_kind: "TD"
h_level: 2
---
<a id="TD-194"></a>
## **1.12.D Amplify Gen 2 configuration (and “never Classic” guardrails)**

**Repo structure (illustrative):**

*/amplify/*  
*stack.ts \# CDK app entry for Amplify Gen 2*  
*backend/*  
*auth/ (Cognito)*  
*api/ (AppSync schema & functions)*  
*storage/ (S3, Dynamo)*  
*functions/ (Lambdas)*  
*observability/ (CW dashboards, alarms)*  
*search/ (Typesense/OpenSearch stack)*  
*cdk.json*  
*/bin/infra.ts \# CDK app bootstrap for non-Amplify stacks (optionally)*  
*/packages/ (web, bff libs, shared types)*  
*/apps/web (Next.js)*  
*/apps/indexer (indexing worker)*  
*/apps/renderer (docs/pdf)*  

**Guardrails to avoid Classic:**

- CI check: **fail build** if an *amplify/cli.json* or *team-provider-info.json* (Classic) is introduced.
- Only accept PRs that modify CDK stacks under */amplify/backend/\*\**.
- Run *amplify status* (Gen 2) and diff in CI; deny merge if detected drift or unmanaged resources.

**Stacks (high-level CDK):**

- **AuthStack** (Cognito pools, Hosted UI, OAuth providers).
- **ApiStack** (AppSync, GraphQL schema, Lambda functions, role policies).
- **DataStack** (Aurora cluster, Dynamo tables, Secrets, Subnets).
- **SearchStack** (Typesense ECS/Fargate or managed option; or OpenSearch Serverless w/ OCU cap).
- **MediaStack** (S3 buckets, CloudFront, Lambda@Edge image resizer, WAF).
- **WorkflowStack** (SQS, EventBridge, Step Functions).
- **ObservabilityStack** (CloudWatch dashboards, alarms, X‑Ray, logs retention).
- **CommsStack** (SES identities, SNS/SQS for bounces, in‑app store).
- **AdminStack** (Amplify Admin UI access scopes, RBAC seeds).
