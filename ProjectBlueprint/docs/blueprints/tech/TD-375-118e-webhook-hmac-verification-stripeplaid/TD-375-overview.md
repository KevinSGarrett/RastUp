---
id: TD-375
title: "**1.18.E Webhook HMAC Verification (Stripe/Plaid)**"
source_doc: "TechDevBlueprint.docx"
source_path: "docs\blueprints\tech\TD-375-118e-webhook-hmac-verification-stripeplaid\TD-375-overview.md"
parent_id: 
anchor: "TD-375"
checksum: "sha256:8bef1ae23f456c2547f2b838d5cb8bdb84551579f0ea4cec1cd7fc317fc3ecd8"
last_modified: "2025-11-06T20:40:46Z"
doc_kind: "TD"
h_level: 2
---
<a id="TD-375"></a>
## **1.18.E Webhook HMAC Verification (Stripe/Plaid)**

**Recommended path:** *security/webhooks/verify.ts*

*import crypto from 'crypto';*  
  
*export function verifyStripe(rawBody: Buffer, sigHeader: string, secret: string) {*  
*// Prefer Stripe SDK constructEvent; fallback HMAC check:*  
*const \[tPart, v1Part\] = sigHeader.split(',').map(s =\> s.trim());*  
*const t = tPart.split('=')\[1\]; const v1 = v1Part.split('=')\[1\];*  
*const payload = \`\${t}.\${rawBody.toString()}\`;*  
*const hmac = crypto.createHmac('sha256', secret).update(payload).digest('hex');*  
*if (!crypto.timingSafeEqual(Buffer.from(hmac), Buffer.from(v1))) throw new Error('INVALID_SIGNATURE');*  
*}*  

Store last **event_id** in an idempotency table; on duplicate, return 200 OK without re‑execution.
