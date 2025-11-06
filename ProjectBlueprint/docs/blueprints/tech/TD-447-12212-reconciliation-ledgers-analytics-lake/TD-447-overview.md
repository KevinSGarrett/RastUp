---
id: TD-447
title: "**1.22.12 Reconciliation — ledgers & analytics lake**"
source_doc: "TechDevBlueprint.docx"
source_path: "docs\blueprints\tech\TD-447-12212-reconciliation-ledgers-analytics-lake\TD-447-overview.md"
parent_id: 
anchor: "TD-447"
checksum: "sha256:d033cfbbead89e087a7353f984c4dd3516689b31604fab58cde91fd93cac7db7"
last_modified: "2025-11-06T20:40:46Z"
doc_kind: "TD"
h_level: 2
---
<a id="TD-447"></a>
## **1.22.12 Reconciliation — ledgers & analytics lake**

**Bronze**: raw webhook dumps + Stripe balance transactions → S3.  
**Silver**: normalized facts: *fact_payments*, *fact_transfers*, *fact_refunds*, *fact_payouts* joined by *order_id*/*transfer_group*.  
**Gold**: revenue dashboards (by city/role), take‑rate, dispute rate, net provider earnings.

**Artifact — reconciliation SQL (Silver build)**  
**Recommended path:** *data/sql/recon_build.sql*

*CREATE OR REPLACE TABLE fact_payments AS*  
*SELECT o.order_id, p.stripe_pi, bt.id as balance_tx, bt.amount, bt.fee, bt.net, bt.created*  
*FROM stripe_balance_tx bt*  
*JOIN payment_intent p ON bt.source = p.stripe_pi*  
*JOIN "order" o ON o.order_id = p.order_id;*  
  
*CREATE OR REPLACE TABLE fact_transfers AS*  
*SELECT t.order_id, t.stripe_transfer, bt.amount, bt.fee, bt.net, bt.created*  
*FROM stripe_balance_tx bt*  
*JOIN transfer_ledger t ON bt.source = t.stripe_transfer;*  

**Dashboards:** revenue by city/role, average booking value, platform take‑rate, refunds %, disputes %, payout SLA compliance.
