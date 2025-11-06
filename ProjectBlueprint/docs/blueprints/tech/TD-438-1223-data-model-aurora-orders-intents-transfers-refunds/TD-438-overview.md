---
id: TD-438
title: "**1.22.3 Data model (Aurora) — orders, intents, transfers, refunds**"
source_doc: "TechDevBlueprint.docx"
source_path: "docs\blueprints\tech\TD-438-1223-data-model-aurora-orders-intents-transfers-refunds\TD-438-overview.md"
parent_id: 
anchor: "TD-438"
checksum: "sha256:b2234017507ad99d630d1479d2e95f849ae720ec54401d5f00ed09b3f66a2340"
last_modified: "2025-11-06T20:40:46Z"
doc_kind: "TD"
h_level: 2
---
<a id="TD-438"></a>
## **1.22.3 Data model (Aurora) — orders, intents, transfers, refunds**

**Recommended path:** *db/migrations/022_payments_core.sql*

*begin;*  
  
*create table "order" (*  
*order_id text primary key, -- ord\_...*  
*buyer_user_id text not null,*  
*provider_user_id text not null, -- seller*  
*service_profile_id text not null, -- sp\_...*  
*studio_id text, -- optional, st\_...*  
*currency text not null default 'USD',*  
*subtotal_cents int not null,*  
*buyer_fee_cents int not null, -- platform fee charged to buyer*  
*tax_cents int not null default 0,*  
*credit_applied_cents int not null default 0, -- credits applied to buyer_fee*  
*status text not null check (status in ('draft','authorized','captured','completed','refunded','voided','disputed')),*  
*booking_dt timestamptz,*  
*created_at timestamptz not null default now(),*  
*updated_at timestamptz not null default now()*  
*);*  
  
*create table payment_intent (*  
*pi_id text primary key, -- pi\_...*  
*order_id text not null references "order"(order_id),*  
*stripe_pi text not null, -- PaymentIntent id*  
*client_secret text not null,*  
*method text not null, -- 'card','ach','wallet'*  
*capture_method text not null check (capture_method in ('automatic','manual')) default 'automatic',*  
*amount_cents int not null,*  
*currency text not null,*  
*status text not null, -- 'requires_payment_method','succeeded','requires_capture','canceled'*  
*last_error text,*  
*created_at timestamptz not null default now(),*  
*updated_at timestamptz not null default now(),*  
*unique (order_id, stripe_pi)*  
*);*  
  
*create table transfer_ledger (*  
*xfer_id text primary key, -- xfr\_...*  
*order_id text not null references "order"(order_id),*  
*provider_account text not null, -- acct\_... (Stripe Connect)*  
*amount_cents int not null,*  
*currency text not null,*  
*stripe_transfer text, -- tr\_...*  
*status text not null check (status in ('pending','paid','reversed','canceled')),*  
*created_at timestamptz not null default now()*  
*);*  
  
*create table refund_ledger (*  
*refund_id text primary key, -- rfd\_...*  
*order_id text not null,*  
*stripe_refund text,*  
*amount_cents int not null,*  
*reason text not null,*  
*initiator text not null, -- 'buyer','provider','platform','dispute'*  
*created_at timestamptz not null default now()*  
*);*  
  
*commit;*  

Separate from the **credit_ledger** in §1.16 (promos/referrals). Card numbers are never stored—only Stripe ids.
