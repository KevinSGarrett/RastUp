---
id: TD-22
title: "**1.3.C State machines (per leg and for LBG)**"
source_doc: "TechDevBlueprint.docx"
source_path: "docs\blueprints\tech\TD-22-13c-state-machines-per-leg-and-for-lbg\TD-22-overview.md"
parent_id: 
anchor: "TD-22"
checksum: "sha256:c33fced7a2a495bf0a2e9d41b28595d0568b45b1c972e95f0e0721243e9534f6"
last_modified: "2025-11-06T20:40:46Z"
doc_kind: "TD"
h_level: 2
---
<a id="TD-22"></a>
## **1.3.C State machines (per leg and for LBG)**

**Leg state:**  
*draft → awaiting_docs → awaiting_payment → confirmed → in_progress → completed*  
Failures: *cancelled*, *failed*

**LBG state:**

- Derived from legs: *draft* if any leg *draft/awaiting\_\**; *confirmed* if **both** legs *confirmed*; *in_progress* if any leg *in_progress*; *completed* if **both** *completed*; *cancelled* if both cancelled (or group cancelled prior to start); *failed* on atomicity failure pre‑confirm.

**Transitions (high‑level)**

171. **startCheckout** → create LBG + one leg (Talent) in *awaiting_docs*.
172. **attachStudioInFlow** (optional) → add Studio leg; both legs now *awaiting_docs*.
173. **createDocPack & sign** → both legs *awaiting_payment*.
174. **authorize & capture LBG charge** (PaymentIntent) → *confirmed* if both legs funded; else rollback.
175. **before start_at**: allow **amendments** (extras), re‑quote tax, adjust charge (incremental capture or second charge).
176. **at start_at**: move legs to *in_progress*.
177. **completion**: buyer acceptance or window expiry → queue **payouts**; auto‑void unused deposit holds.
178. **dispute/refund**: flows do not alter leg status but affect payout/finance ledgers; receipts amended.

**Studio deposit** lives outside the main charge and is captured only on approved claim within a policy window.

We implement these as an **AWS Step Functions** saga for LBG with per‑leg substates, plus outbox events to keep UI in sync.
