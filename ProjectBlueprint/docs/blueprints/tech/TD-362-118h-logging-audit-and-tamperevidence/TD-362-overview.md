---
id: TD-362
title: "**1.18.H Logging, audit, and tamper‑evidence**"
source_doc: "TechDevBlueprint.docx"
source_path: "docs\blueprints\tech\TD-362-118h-logging-audit-and-tamperevidence\TD-362-overview.md"
parent_id: 
anchor: "TD-362"
checksum: "sha256:537763012ab31c04b241e3faedc4c862514bb624b0f83c9a514ac10e4d1cf221"
last_modified: "2025-11-06T20:40:46Z"
doc_kind: "TD"
h_level: 2
---
<a id="TD-362"></a>
## **1.18.H Logging, audit, and tamper‑evidence**

- **CloudTrail** to dedicated **log‑archive account** (S3 with **Object Lock** + Glacier).
- **App logs**: JSON, structured, **no PII**. Correlation IDs propagate (*x‑corr‑id*).
- **Admin actions** (refunds, holds, DMCA, representment) write to an **immutable audit table** (Aurora) and **append‑only** S3 log (WORM).
- **Webhook idempotency**: record *event_id* + response; on duplicate → 200 OK no‑op.

**Inline artifact — audit event shape**  
**Path:** *security/audit/event-envelope.json*

*{*  
*"ts":"2025-11-06T12:34:56Z",*  
*"actor":"usr_abc \| sys_lambda \| admin@rastup",*  
*"action":"refund.issued \| payout.hold.apply \| dmca.hide",*  
*"target":"leg\_... \| order\_... \| content\_...",*  
*"details":{ "reason":"...", "amount_cents":1234 },*  
*"corrId":"abc123"*  
*}*
