---
id: TD-23
title: "**1.3.D Checkout & payment flows**"
source_doc: "TechDevBlueprint.docx"
source_path: "docs\blueprints\tech\TD-23-13d-checkout-payment-flows\TD-23-overview.md"
parent_id: 
anchor: "TD-23"
checksum: "sha256:d26c33c5adfdfd78618b81539fbb35de0c7b618b9f00f6d1212296c4c7559ae6"
last_modified: "2025-11-06T20:40:46Z"
doc_kind: "TD"
h_level: 2
---
<a id="TD-23"></a>
## **1.3.D Checkout & payment flows**

**Payment providers:** Stripe only at launch (cards + ACH via Financial Connections). Adapter makes it swappable later.

**Strategy (escrow mimic):**

- **Capture the LBG charge at confirmation** (no long holds). Funds sit in platform/connected accounts.
- **Delay payouts** until completion/acceptance window.
- **Deposits** for Studio are handled via **SetupIntent** authorization (separate from GMV) and captured only if a valid claim is approved.

**Stripe objects**

- **PaymentIntent** (one per LBG) with **separate transfers** to legs on payout; metadata contains *lbg_id*, *leg_ids\[\]* and split details.
- **SetupIntent** for Studio deposit with *payment_method_options\[card\]\[capture_method\]=manual* semantics at claim time.
- **Transfers** at payout time per leg to the seller’s Connect account.
- **Refunds** per leg (partial allowed).

**ACH specifics**

- ACH debit is **captured** when *succeeded*; we hold payouts until enough settlement confidence or policy window.

**3DS / SCA**

- Use Stripe’s Payment Element; handle *requires_action* client‑side; webhook transitions keep our state machine consistent.

**Idempotency**

- All create/confirm/refund/payout calls carry an *Idempotency-Key* (persisted), and webhooks are verified (HMAC) + deduped.
