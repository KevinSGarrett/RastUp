---
id: TD-140
title: "**1.9.E Wallet (buyer credits) — rules & flows**"
source_doc: "TechDevBlueprint.docx"
source_path: "docs\blueprints\tech\TD-140-19e-wallet-buyer-credits-rules-flows\TD-140-overview.md"
parent_id: 
anchor: "TD-140"
checksum: "sha256:43e7e02c05da179403d8d89b4e9bb08d94763d006829304e305d9b81b50a0076"
last_modified: "2025-11-06T20:40:46Z"
doc_kind: "TD"
h_level: 2
---
<a id="TD-140"></a>
## **1.9.E Wallet (buyer credits) — rules & flows**

**Use cases:** residuals from partial refunds, goodwill credits, referral bonuses.  
**Important:** wallet *reduces* the **PaymentIntent** amount at checkout; it is never auto‑withdrawn to bank/card.

**Flows**

- **Credit**: create *wallet_txn(kind='credit', source='refund_residual'\|'goodwill'\|'referral')*; increase balance.
- **Apply at checkout**: before creating PI, debit wallet up to available balance (*kind='debit', source='checkout_apply'*) and reduce charge amount; store the applied amount on the LBG for receipts.
- **Reversal**: if a checkout fails post‑debit, write *reversal* credit with same idempotency key to restore balance.

**GraphQL**

*type Wallet { balanceCents: Int!, currency: String! }*  
*type WalletTxn { walletTxnId: ID!, kind: String!, source: String!, amountCents: Int!, createdAt: AWSDateTime! }*  
  
*type Query { myWallet: Wallet!, myWalletTxns(limit:Int=50, cursor:String): \[WalletTxn!\]! }*  
*type Mutation {*  
*applyWalletToCheckout(draftId: ID!, maxCents: Int!): ApplyWalletResult! \# returns appliedCents*  
*}*  

**Constraints**

- One wallet per user per currency (USD MVP).
- Wallet cannot go negative.
- Expiry on promo/referral credits optional (tracked in *note* or extended field later).
