---
id: TD-112
title: "**1.7.I Billing & credits (cost‑conscious MVP)**"
source_doc: "TechDevBlueprint.docx"
source_path: "docs\blueprints\tech\TD-112-17i-billing-credits-costconscious-mvp\TD-112-overview.md"
parent_id: 
anchor: "TD-112"
checksum: "sha256:6eea802565140c0731023d1ec0b5342351c2eacb49eb83cab0c14108d0ac1350"
last_modified: "2025-11-06T20:40:46Z"
doc_kind: "TD"
h_level: 2
---
<a id="TD-112"></a>
## **1.7.I Billing & credits (cost‑conscious MVP)**

**MVP billing model: Prepaid credits (lowest complexity)**

- Advertiser tops up credits via **Stripe** (platform customer).
- Spend ledger debits for each **valid click** at campaign’s *cpc_cents*.
- When balance low (\< threshold), show in‑product **“low balance”** banner; auto‑recharge (optional).
- **Make‑good credits** issued on invalid‑click findings as positive ledger entries.
- Monthly statements available (CSV/PDF) with impressions, clicks, CPC, charges, credits, net spend.

**Phase‑up (optional): Stripe Billing metered**

- Create a metered product *promoted_click*; report usage daily; Stripe invoices monthly (postpaid).
- Keep **internal ledger** regardless for exact traceability and fraud credits.

**Tax on ad fees**

- If applicable by jurisdiction, apply sales tax to **ad purchases/top‑ups** (separate from marketplace taxes). Use the same tax adapter.

**Accounting separation**

- Ad revenue is **non‑GMV**; in analytics, keep separate revenue streams and costs to avoid inflating marketplace take.
