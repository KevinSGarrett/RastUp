---
id: TD-240
title: "**1.14.D Payment flows (Stripe) & taxes**"
source_doc: "TechDevBlueprint.docx"
source_path: "docs\blueprints\tech\TD-240-114d-payment-flows-stripe-taxes\TD-240-overview.md"
parent_id: 
anchor: "TD-240"
checksum: "sha256:68338941dbbb32307d0f85a282479c974742dc0d1fb666debee349733b97bf87"
last_modified: "2025-11-06T20:40:46Z"
doc_kind: "TD"
h_level: 2
---
<a id="TD-240"></a>
## **1.14.D Payment flows (Stripe) & taxes**

- **Subscriptions:** Stripe Billing **subscriptions** (monthly).

  - Create product per creator with *price_month_cents*; or use one product with **price per creator** (more scalable).
  - Webhooks: *invoice.payment_succeeded/failed*, *customer.subscription.updated\|deleted*.
  - We record *fansub_subscription* and entitlement (active period).

- **Tips:** one‑time **PaymentIntent** with **Connect destination** to the creator account (less platform float). Platform fee (if any) handled as application fee on Connect.

- **PPV:** one‑time **PaymentIntent**; after success, create *fansub_ppv_access* row to grant entitlement.

- Requests:

  - Creator issues **quote** (action card in thread).
  - Buyer pays **PaymentIntent**; on success, order → *succeeded*; request status *paid*.
  - Deliverable posted via action card; buyer **approves** or **requests revisions**.
  - Refunds follow §1.3 policy; disputes → §1.9 D.5.

- Taxes:

  - **Subscription/PPV/Requests** are **digital services**; compute **buyer tax** via tax adapter (Stripe Tax/Avalara/TaxJar) using buyer location.
  - We separately compute **platform fee taxes** per §1.9 for any fee we charge.
  - Receipts show line items: content price, tax, platform fee (if present), platform fee tax.

- **Payouts:** per creator via Stripe Connect scheduled payouts; we record *payout.queued\|paid* events into analytics (see §1.13).
