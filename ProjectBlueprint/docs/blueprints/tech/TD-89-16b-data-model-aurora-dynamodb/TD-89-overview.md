---
id: TD-89
title: "**1.6.B Data model (Aurora + DynamoDB)**"
source_doc: "TechDevBlueprint.docx"
source_path: "docs\blueprints\tech\TD-89-16b-data-model-aurora-dynamodb\TD-89-overview.md"
parent_id: 
anchor: "TD-89"
checksum: "sha256:985a133111d50b7898ddc305d66731a9ecf174dbdd2982c20284fa54a6db84b6"
last_modified: "2025-11-06T20:40:46Z"
doc_kind: "TD"
h_level: 2
---
<a id="TD-89"></a>
## **1.6.B Data model (Aurora + DynamoDB)**

*-- Identity Verification (IDV) status & metadata*  
*create table idv_status (*  
*idv_id text primary key, -- idv\_...*  
*user_id text not null, -- usr\_...*  
*provider text not null, -- 'persona' or 'stripe_identity' etc.*  
*provider_ref text not null, -- external session/check id*  
*status text not null check (status in ('pending','passed','failed','expired','requires_review')),*  
*checks_json jsonb not null, -- document, selfie, liveness, match scores (non-PII summaries)*  
*age_verified boolean not null default false,*  
*created_at timestamptz not null default now(),*  
*updated_at timestamptz not null default now(),*  
*unique (user_id, provider_ref)*  
*);*  
  
*-- Background Check (FCRA) status*  
*create table bg_status (*  
*bg_id text primary key, -- bg\_...*  
*user_id text not null,*  
*provider text not null, -- 'checkr' etc.*  
*provider_ref text not null,*  
*status text not null check (status in ('invited','in_progress','clear','consider','suspended','disputed','withdrawn','expired')),*  
*package text not null, -- e.g. 'basic_us'*  
*adjudication text, -- provider adjudication summary (non-PII)*  
*report_url text, -- provider-hosted report link (if allowed)*  
*created_at timestamptz not null default now(),*  
*updated_at timestamptz not null default now(),*  
*unique (user_id, provider_ref)*  
*);*  
  
*-- Social verification (per platform)*  
*create table social_verification (*  
*soc_id text primary key, -- soc\_...*  
*user_id text not null,*  
*platform text not null check (platform in ('instagram','tiktok','youtube','x')),*  
*handle text not null,*  
*verified boolean not null default false,*  
*snapshot_json jsonb, -- follower counts, ER, etc. (non-secret)*  
*last_checked_at timestamptz*  
*);*  
  
*-- Trust badges (derived)*  
*create table trust_badge (*  
*badge_id text primary key, -- tbg\_...*  
*user_id text not null,*  
*kind text not null check (kind in ('id_verified','trusted_pro','social_verified')),*  
*source_id text, -- idv_id, bg_id, or soc_id*  
*issued_at timestamptz not null default now(),*  
*expires_at timestamptz -- optional expiry for recert*  
*);*  
  
*-- Risk signals snapshots*  
*create table trust_risk_signal (*  
*signal_id text primary key, -- rsk\_...*  
*user_id text not null,*  
*window daterange not null, -- \[start,end)*  
*disputes_opened int not null default 0,*  
*refunds_asked int not null default 0,*  
*cancellations int not null default 0,*  
*late_delivery int not null default 0,*  
*charge_failures int not null default 0,*  
*bad_clicks int not null default 0,*  
*flags_json jsonb not null default '{}'::jsonb,*  
*score int not null default 0, -- aggregate score (0-100; lower is riskier)*  
*computed_at timestamptz not null default now()*  
*);*  

**DynamoDB (hot path cache):** a small *trust_cache* item per user (IDV passed?, Trusted Pro?, social verified?, risk score) to avoid DB round trips on search and booking.
