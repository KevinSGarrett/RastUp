---
id: TD-276
title: "**1.15.E Data model (Aurora + S3)**"
source_doc: "TechDevBlueprint.docx"
source_path: "docs\blueprints\tech\TD-276-115e-data-model-aurora-s3\TD-276-overview.md"
parent_id: 
anchor: "TD-276"
checksum: "sha256:5b4447734268b588fd4e72aabea4959dc97fe7f78247aeea1a2dcfb4f521e1ed"
last_modified: "2025-11-06T20:40:46Z"
doc_kind: "TD"
h_level: 2
---
<a id="TD-276"></a>
## **1.15.E Data model (Aurora + S3)**

*create table support_case (*  
*case_id text primary key, -- sca\_...*  
*type text not null check (type in ('booking','payment','product','dmca','policy','chargeback')),*  
*subtype text, -- e.g., 'no_show','quality','duplicate_charge'*  
*status text not null check (status in ('open','awaiting_customer','awaiting_seller','investigating','decision_pending','refunded','denied','goodwill','escalated','closed')),*  
*severity text not null check (severity in ('low','normal','high','urgent')),*  
*opened_by_user text not null, -- usr\_...*  
*owner_user_id text, -- agent assigned*  
*watchers text\[\] not null default '{}',*  
*lbg_id text, -- booking group*  
*leg_id text,*  
*order_id text, -- fansub order (PPV/tip/request)*  
*studio_id text,*  
*creator_id text, -- fansub_creator*  
*payout_id text, -- if payout hold/release*  
*reason_code text, -- normalized reason taxonomy*  
*sla_first_resp_at timestamptz,*  
*sla_due_at timestamptz,*  
*created_at timestamptz not null default now(),*  
*updated_at timestamptz not null default now()*  
*);*  
  
*create table support_message (*  
*msg_id text primary key, -- smg\_...*  
*case_id text not null references support_case(case_id) on delete cascade,*  
*author_role text not null check (author_role in ('buyer','seller','studio_owner','creator','agent','system')),*  
*author_user_id text,*  
*body_md text not null, -- markdown (sanitized)*  
*attachments_json jsonb not null default '\[\]'::jsonb, -- \[{s3_key, hash, bytes, mime}\]*  
*created_at timestamptz not null default now()*  
*);*  
  
*create table support_event (*  
*evt_id text primary key, -- sev\_...*  
*case_id text not null references support_case(case_id) on delete cascade,*  
*action text not null, -- 'status_change','refund_issued','deposit_captured','evidence_attached','hold_applied','hold_released','chargeback_represented','dmca_hide','dmca_restore'*  
*actor_user_id text,*  
*details_json jsonb not null default '{}'::jsonb,*  
*created_at timestamptz not null default now()*  
*);*  
  
*-- Calculated refund/goodwill outcomes (mirror §1.9 fee/tax logic)*  
*create table support_refund (*  
*refund_id text primary key, -- srf\_...*  
*case_id text not null references support_case(case_id) on delete cascade,*  
*leg_id text,*  
*order_id text,*  
*amount_cents int not null,*  
*platform_fee_cents int not null,*  
*platform_fee_tax_cents int not null,*  
*reason text not null,*  
*processor_ref text, -- refund id on Stripe*  
*status text not null check (status in ('proposed','processing','succeeded','failed')),*  
*created_at timestamptz not null default now()*  
*);*  
  
*-- Payout holds (linked to legs/orders)*  
*create table payout_hold (*  
*hold_id text primary key, -- sph\_...*  
*case_id text not null references support_case(case_id),*  
*leg_id text,*  
*order_id text,*  
*amount_cents int not null, -- up to the payable amount*  
*status text not null check (status in ('applied','released','expired')),*  
*created_at timestamptz not null default now()*  
*);*  

**S3**:

- *support-evidence/* (immutable, WORM‑like via object‑lock if enabled) stores attachments (photos, manifests, logs PDF). Lifecycle → Intelligent‑Tiering @30d; Glacier @180d.
