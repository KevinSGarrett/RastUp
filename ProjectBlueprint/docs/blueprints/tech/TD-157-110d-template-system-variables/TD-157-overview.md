---
id: TD-157
title: "**1.10.D Template system & variables**"
source_doc: "TechDevBlueprint.docx"
source_path: "docs\blueprints\tech\TD-157-110d-template-system-variables\TD-157-overview.md"
parent_id: 
anchor: "TD-157"
checksum: "sha256:bcda557c5b943aa90ad02c54820515848d5b81d5deab05feb5eb9f08c39747ab"
last_modified: "2025-11-06T20:40:46Z"
doc_kind: "TD"
h_level: 2
---
<a id="TD-157"></a>
## **1.10.D Template system & variables**

- **Authoring**: Email uses **MJML** → compiled to inline‑styled HTML. SMS uses strict text length (truncate & link to in‑app). Push uses *{title, body, data}*. In‑app stores *{title, body, deep_link}*.
- **Variables**: Declared in *variables_json* with type, description, and required flag. Types: *string*, *int*, *money_cents*, *date*, *datetime*, *duration*, *enum{…}*, *url*.
- **Localization**: Templates can exist per *locale* (start with *en-US*). Fallback: *en-US* if no locale‑specific template.

**Core templates (MVP, examples)**

- Booking lifecycle: *booking_confirmed_buyer*, *booking_confirmed_seller*, *booking_rescheduled*, *booking_cancellation_outcome*.
- Docs: *doc_sign_request*, *doc_sign_reminder*, *doc_complete*.
- Payments: *charge_receipt*, *refund_receipt*, *payout_queued*, *payout_paid*, *statement_ready*.
- Messaging: *new_message_digest*, *deliverable_posted*, *review_reminder*.
- Trust: *idv_start*, *idv_reminder*, *bg_invited*, *badge_awarded*.
- Promotions: *promo_low_balance*, *promo_statement_ready*.

*(I can include full MJML bodies upon request; they’re verbose.)*

**Variable resolution**

- Resolver library maps domain objects → template variables (e.g., leg dates in local timezone, names, amounts with currency formatting, doc links with signed URLs).
- Hard **PII minimization**: SMS never includes full names + addresses + money in the same text; use in‑app deep links.
