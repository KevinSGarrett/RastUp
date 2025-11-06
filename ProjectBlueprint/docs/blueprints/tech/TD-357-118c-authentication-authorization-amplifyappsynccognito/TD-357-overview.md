---
id: TD-357
title: "**1.18.C Authentication & authorization (Amplify/AppSync/Cognito)**"
source_doc: "TechDevBlueprint.docx"
source_path: "docs\blueprints\tech\TD-357-118c-authentication-authorization-amplifyappsynccognito\TD-357-overview.md"
parent_id: 
anchor: "TD-357"
checksum: "sha256:5f57656525323b5a2dffac6bc61b22cee5b924b973f104e118463572108ac3e4"
last_modified: "2025-11-06T20:40:46Z"
doc_kind: "TD"
h_level: 2
---
<a id="TD-357"></a>
## **1.18.C Authentication & authorization (Amplify/AppSync/Cognito)**

**AuthN**

- **Cognito User Pool** for end‑users (buyers/sellers/creators/studio owners) with email+password and optional social IdPs (Apple/Google).
- **Cognito Identity Pool** for federated access to limited S3 (signed uploads of previews only).
- **Admin/agent** access via **OIDC** (IdP such as Google Workspace/Okta) → separate AppSync auth mode.

**AuthZ (AppSync multi‑auth)**

- **Cognito JWT** for user operations; **IAM** for server‑to‑server; **OIDC** for internal tooling.
- Use **@auth** rules + VTL/JS resolvers to enforce **row‑level** constraints (e.g., user can access only their threads, creator their own Fan‑Sub pages, admin by role claims).
- **Fine‑grained**: deny by default; allow by ownership (*ownerId == \$ctx.identity.sub*), role claim (*has("admin")*), or entitlement check (Dynamo cache read).

**Inline artifact — AppSync auth modes**  
**Path:** *security/appsync/multi-auth.md*

*- Default Authorization: AMAZON_COGNITO_USER_POOLS*  
*- Additional:*  
* - AWS_IAM (trusted Lambdas + batch jobs)*  
* - OPENID_CONNECT (Admin console only)*  
*- API Key: \*\*disabled\*\* in prod*
