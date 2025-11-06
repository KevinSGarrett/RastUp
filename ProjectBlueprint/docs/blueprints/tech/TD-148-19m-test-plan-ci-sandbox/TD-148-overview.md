---
id: TD-148
title: "**1.9.M Test plan (CI + sandbox)**"
source_doc: "TechDevBlueprint.docx"
source_path: "docs\blueprints\tech\TD-148-19m-test-plan-ci-sandbox\TD-148-overview.md"
parent_id: 
anchor: "TD-148"
checksum: "sha256:e665e5c5d986cc0dcc97970c79381a3d8bf83cd894482b73857c190c45077208"
last_modified: "2025-11-06T20:40:46Z"
doc_kind: "TD"
h_level: 2
---
<a id="TD-148"></a>
## **1.9.M Test plan (CI + sandbox)**

**Fees & taxes**

852. Compute per‑leg fees & fee tax for different cities/roles; verify rounding; receipts show lines.
853. Earn revenue on completion; deferral → earned; reverse on refund both pre‑ and post‑earn.

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
