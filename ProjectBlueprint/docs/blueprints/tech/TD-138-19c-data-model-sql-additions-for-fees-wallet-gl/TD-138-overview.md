---
id: TD-138
title: "**1.9.C Data model (SQL additions for fees, wallet & GL)**"
source_doc: "TechDevBlueprint.docx"
source_path: "docs\blueprints\tech\TD-138-19c-data-model-sql-additions-for-fees-wallet-gl\TD-138-overview.md"
parent_id: 
anchor: "TD-138"
checksum: "sha256:0ed3627180763b647c9db764ad2b718d2f7af5041c5edc17410942e3aaf4d689"
last_modified: "2025-11-06T20:40:46Z"
doc_kind: "TD"
h_level: 2
---
<a id="TD-138"></a>
## **1.9.C Data model (SQL additions for fees, wallet & GL)**

Extends §1.3 schema.

*-- Per-leg fee snapshot (immutable after confirm; amendments add new rows)*  
*alter table booking_leg*  
*add column platform_fee_cents int not null default 0,*  
*add column platform_fee_tax_cents int not null default 0;*  
  
*-- Wallet for BUYERS (not advertisers)*  
*create table wallet_account (*  
*wallet_id text primary key, -- wlt\_...*  
*user_id text unique not null, -- usr\_...*  
*currency text not null default 'USD',*  
*balance_cents int not null default 0,*  
*created_at timestamptz not null default now(),*  
*updated_at timestamptz not null default now()*  
*);*  
  
*create table wallet_txn (*  
*wallet_txn_id text primary key, -- wtx\_...*  
*wallet_id text not null references wallet_account(wallet_id) on delete cascade,*  
*kind text not null check (kind in ('credit','debit','adjustment')),*  
*source text not null check (source in ('refund_residual','goodwill','referral','checkout_apply','reversal')),*  
*lbg_id text,*  
*leg_id text,*  
*amount_cents int not null, -- positive; sign inferred by kind*  
*note text,*  
*idempotency_key text not null,*  
*created_at timestamptz not null default now()*  
*);*  
*create index on wallet_txn(wallet_id, created_at desc);*  
*create unique index on wallet_txn(idempotency_key);*  
  
*-- Platform fee ledger (deferrals→earned)*  
*create table fee_ledger (*  
*fee_entry_id text primary key, -- fle\_...*  
*leg_id text not null,*  
*stage text not null check (stage in ('deferred','earned','reversed')),*  
*platform_fee_cents int not null,*  
*platform_fee_tax_cents int not null,*  
*reason text not null, -- 'confirm','complete','refund','dispute'*  
*created_at timestamptz not null default now()*  
*);*  
  
*-- GL journal (exportable to accounting)*  
*create table gl_entry (*  
*gl_id text primary key, -- gl\_...*  
*occurred_at timestamptz not null,*  
*lbg_id text,*  
*leg_id text,*  
*account_dr text not null, -- e.g., 'Cash:Stripe', 'Deferred:PlatformFees'*  
*account_cr text not null, -- e.g., 'Liability:SellerPayable'*  
*amount_cents int not null,*  
*memo text,*  
*ext_ref text, -- stripe bal_txn id, charge id, payout id*  
*created_at timestamptz not null default now()*  
*);*  
*create index on gl_entry(occurred_at);*  
*create index on gl_entry(lbg_id, leg_id);*  

**Note:** Advertiser **ads credits** ledger from §1.7 remains separate (*promo_budget_ledger*). Buyer wallet and promo credits **never** touch each other.
