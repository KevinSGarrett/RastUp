---
id: TD-197
title: "**1.12.G Identity & access (Cognito)**"
source_doc: "TechDevBlueprint.docx"
source_path: "docs\blueprints\tech\TD-197-112g-identity-access-cognito\TD-197-overview.md"
parent_id: 
anchor: "TD-197"
checksum: "sha256:41ec63010c608f9effa8409e4f8dc117d2660e1fabc1c22eb49abd0f454c85db"
last_modified: "2025-11-06T20:40:46Z"
doc_kind: "TD"
h_level: 2
---
<a id="TD-197"></a>
## **1.12.G Identity & access (Cognito)**

- **User Pool** with hosted UI (email, Apple/Google OAuth).
- **Groups/Roles:** *buyer*, *seller*, *studio_owner*, *admin*, *trust*, *support*, *finance*.
- **MFA** optional at signup; required for Admin roles.
- **Age‑gate** attribute on user (*\>18*) linked to IDV status (§1.6).
- **Identity Pool** for S3 direct uploads (scoped IAM policies per bucket/prefix).
- **Session length** tuned per role; refresh token rotation.
