---
id: TD-358
title: "**1.18.D Secrets & key management**"
source_doc: "TechDevBlueprint.docx"
source_path: "docs\blueprints\tech\TD-358-118d-secrets-key-management\TD-358-overview.md"
parent_id: 
anchor: "TD-358"
checksum: "sha256:81155fcc3ded2029251a93eb975ad27f8a9a5185454186fbc31441fce04f3760"
last_modified: "2025-11-06T20:40:46Z"
doc_kind: "TD"
h_level: 2
---
<a id="TD-358"></a>
## **1.18.D Secrets & key management**

- **AWS Secrets Manager**: Stripe keys, Plaid (if adopted), e‑sign provider tokens, SMTP creds (if not SES), third‑party API tokens.
- **SSM Parameter Store**: non‑secret config (feature flags, limits).
- **KMS**: dedicated CMKs per data domain (*pii*, *finance*, *legal*) with **key policies** bound to minimal roles; automatic rotation enabled.

**Inline artifact — Secrets naming convention**  
**Path:** *security/secrets/naming.md*

*/prod/stripe/secret_key*  
*/prod/stripe/webhook_secret*  
*/prod/plaid/client_id*  
*/prod/plaid/secret*  
*/prod/esign/api_key*  
*/stage/...*
