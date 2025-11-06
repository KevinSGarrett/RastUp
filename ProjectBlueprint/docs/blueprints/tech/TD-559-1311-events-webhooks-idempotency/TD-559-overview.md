---
id: TD-559
title: "**1.3.11 Events, webhooks & idempotency**"
source_doc: "TechDevBlueprint.docx"
source_path: "docs\blueprints\tech\TD-559-1311-events-webhooks-idempotency\TD-559-overview.md"
parent_id: 
anchor: "TD-559"
checksum: "sha256:6552b41e9ec8e718f589bbc13af216bb7884e6e7ede5ac30adbe9e2b02afced7"
last_modified: "2025-11-06T20:40:46Z"
doc_kind: "TD"
h_level: 2
---
<a id="TD-559"></a>
## **1.3.11 Events, webhooks & idempotency**

**Event taxonomy (emits to Kinesis/SNS):**

- booking.request.sent\|accepted\|declined\|countered\|expired
- booking.confirmed\|calendar.blocked\|chat.opened
- booking.milestone.delivered\|approved
- booking.completed\|payout.scheduled\|payout.released
- booking.cancelled.buyer\|provider
- booking.dispute.opened\|resolved

**Webhooks (Stripe Connect):**

- *payment_intent.succeeded*, *payment_intent.payment_failed*, *charge.refunded*, *charge.dispute.created\|closed*, *transfer.created\|paid\|reversed*.

**Idempotency**: all webhook handlers accept *event.id* and store in DynamoDB to prevent duplicate processing.
