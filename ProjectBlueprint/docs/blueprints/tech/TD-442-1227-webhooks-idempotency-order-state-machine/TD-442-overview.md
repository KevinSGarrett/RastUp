---
id: TD-442
title: "**1.22.7 Webhooks, idempotency & order state machine**"
source_doc: "TechDevBlueprint.docx"
source_path: "docs\blueprints\tech\TD-442-1227-webhooks-idempotency-order-state-machine\TD-442-overview.md"
parent_id: 
anchor: "TD-442"
checksum: "sha256:4352fb9db8e631d5e492dc2f2367ed1d4022bfe7e8b8363cc5c05f928ad635c8"
last_modified: "2025-11-06T20:40:46Z"
doc_kind: "TD"
h_level: 2
---
<a id="TD-442"></a>
## **1.22.7 Webhooks, idempotency & order state machine**

**Listen to:**  
*payment_intent.succeeded*, *payment_intent.payment_failed*, *charge.refunded*, *charge.dispute.created\|closed*, *account.updated*, *transfer.paid\|reversed*, *payout.paid\|failed*.

**Order states:** *draft → authorized? → captured → completed → (refunded\|disputed)*.

**Artifact — webhook handler skeleton**  
**Recommended path:** *apps/functions/stripeWebhook.ts*

*import { verifyStripe } from '../../security/webhooks/verify'; // §1.18.E*  
  
*export const handler = async (evt) =\> {*  
*const sig = evt.headers\['stripe-signature'\];*  
*const raw = Buffer.from(evt.body, 'utf8');*  
*const event = stripe.webhooks.constructEvent(raw, sig, process.env.STRIPE_WEBHOOK_SECRET);*  
  
*switch (event.type) {*  
*case 'payment_intent.succeeded': await onPiSucceeded(event.data.object); break;*  
*case 'payment_intent.payment_failed': await onPiFailed(event.data.object); break;*  
*case 'charge.refunded': await onRefund(event.data.object); break;*  
*case 'charge.dispute.created': await onDispute(event.data.object); break;*  
*case 'charge.dispute.closed': await onDisputeClosed(event.data.object); break;*  
*case 'transfer.paid': await onTransferPaid(event.data.object); break;*  
*}*  
*return { statusCode: 200, body: '{}' };*  
*};*  

**Idempotency store:** record processed *event.id* in Dynamo with TTL; duplicates are no‑ops.
