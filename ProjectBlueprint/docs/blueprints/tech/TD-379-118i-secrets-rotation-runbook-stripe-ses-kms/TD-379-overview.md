---
id: TD-379
title: "**1.18.I Secrets Rotation Runbook (Stripe, SES, KMS)**"
source_doc: "TechDevBlueprint.docx"
source_path: "docs\blueprints\tech\TD-379-118i-secrets-rotation-runbook-stripe-ses-kms\TD-379-overview.md"
parent_id: 
anchor: "TD-379"
checksum: "sha256:9697ac3aeb2dc7208bbce24743709e53410155c0062b3197ce8b43841a9e3f94"
last_modified: "2025-11-06T20:40:46Z"
doc_kind: "TD"
h_level: 2
---
<a id="TD-379"></a>
## **1.18.I Secrets Rotation Runbook (Stripe, SES, KMS)**

**Recommended path:** *security/secrets/rotation-runbook.md*

*Cadence*  
*- Stripe API/Webhook: 90 days*  
*- SES SMTP creds: 180 days*  
*- KMS key rotation: yearly (auto)*  
  
*Steps (Stripe)*  
*1) Create new restricted key (write: charges, read: events).*  
*2) Deploy to stage via Secrets Manager (/stage/stripe/secret_key).*  
*3) Run stage smoke tests (webhooks).*  
*4) In prod, add new key alongside old; rotate webhooks secret.*  
*5) Flip AppSync/Lambdas to new secret; verify live.*  
*6) Disable old key; update runbook timestamps.*  
  
*Verification*  
*- CloudWatch alarm if Stripe auth errors \> 0.1% after rotation.*
