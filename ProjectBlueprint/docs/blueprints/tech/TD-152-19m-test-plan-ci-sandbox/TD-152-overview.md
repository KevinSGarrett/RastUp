---
id: TD-152
title: "**1.9.M Test plan (CI + sandbox)**"
source_doc: "TechDevBlueprint.docx"
source_path: "docs\blueprints\tech\TD-152-19m-test-plan-ci-sandbox\TD-152-overview.md"
parent_id: 
anchor: "TD-152"
checksum: "sha256:907fd6b224ea462c823abbbd21579fab0b50a2f0523818e0f8f8a23f1c23d7bc"
last_modified: "2025-11-06T20:40:46Z"
doc_kind: "TD"
h_level: 2
---
<a id="TD-152"></a>
## **1.9.M Test plan (CI + sandbox)**

**Fees & taxes**

915. Compute per‑leg fees & fee tax for different cities/roles; verify rounding; receipts show lines.
916. Earn revenue on completion; deferral → earned; reverse on refund both pre‑ and post‑earn.

**Wallet**  
3) Credit on refund residual; apply to checkout; reversal on failed PI; double‑debit prevented by idempotency key.

**GL & recon**  
4) GL entries written at capture, completion, payout, refund, dispute; sums balance.  
5) Recon: Σcharges == Cash delta ± Stripe fees; Σtransfers == Seller Payable delta; variance gates payouts when off.

**MoR switch**  
6) Service tax to Seller Payable vs Tax Payable toggles correctly and flows to statements/reports.

**Seller/Buyer statements**  
7) Generate period statements; totals tie to underlying legs/payouts/charges.

**Performance**  
8) Fee compute p95 \< 100 ms; wallet apply p95 \< 75 ms under load.
