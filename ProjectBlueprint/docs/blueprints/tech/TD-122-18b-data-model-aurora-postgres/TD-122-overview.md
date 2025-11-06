---
id: TD-122
title: "**1.8.B Data model (Aurora Postgres)**"
source_doc: "TechDevBlueprint.docx"
source_path: "docs\blueprints\tech\TD-122-18b-data-model-aurora-postgres\TD-122-overview.md"
parent_id: 
anchor: "TD-122"
checksum: "sha256:c72529df5a6ebc6fbd2f6071e4fd8344b469d9384d7cb4d116cda10abd4b5e3f"
last_modified: "2025-11-06T20:40:46Z"
doc_kind: "TD"
h_level: 2
---
<a id="TD-122"></a>
## **1.8.B Data model (Aurora Postgres)**

*-- Reviews are scoped to either a Service Profile (person) or a Studio (place)*  
*create table review (*  
*review_id text primary key, -- rev\_...*  
*target_type text not null check (target_type in ('service_profile','studio')),*  
*target_id text not null, -- srv\_\* or std\_\**  
*author_user_id text not null, -- usr\_\* (buyer on the leg)*  
*leg_id text not null, -- leg\_\* (used to enforce 1:1 and eligibility)*  
*rating smallint not null check (rating between 1 and 5),*  
*title text,*  
*body text,*  
*facets_json jsonb not null default '{}'::jsonb, -- {communication:1-5, quality:1-5, ...}*  
*photos_json jsonb not null default '\[\]'::jsonb, -- review photos (previews only)*  
*status text not null check (status in ('published','hidden','removed','pending')),*  
*policy_flags jsonb not null default '{}'::jsonb, -- {toxicity:0-1, nsfw:0-1, fraud_score:0-1}*  
*source text not null default 'first_party', -- reserved for future imports*  
*created_at timestamptz not null default now(),*  
*updated_at timestamptz not null default now(),*  
*unique (leg_id, author_user_id)*  
*);*  
  
*-- Aggregates per entity (denormalized for fast reads)*  
*create table reputation_aggregate (*  
*agg_id text primary key, -- rag\_...*  
*target_type text not null, -- 'service_profile' \| 'studio'*  
*target_id text not null,*  
*rating_avg numeric(3,2) not null default 0,*  
*rating_count int not null default 0,*  
*rating_recent_avg numeric(3,2) not null default 0, -- time-decayed*  
*last_review_at timestamptz,*  
*facet_avgs_json jsonb not null default '{}'::jsonb, -- per-facet averages*  
*fraud_signal numeric(3,2) not null default 0, -- 0-1*  
*updated_at timestamptz not null default now(),*  
*unique (target_type, target_id)*  
*);*  
  
*-- Moderation decisions (immutable)*  
*create table review_moderation_audit (*  
*audit_id text primary key, -- rma\_...*  
*review_id text not null references review(review_id) on delete cascade,*  
*action text not null check (action in ('hide','remove','restore','edit_mask')),*  
*reason_code text not null, -- 'hate_speech','doxxing','fraud_ring','by_request', etc.*  
*actor_user_id text not null, -- admin*  
*details_json jsonb not null default '{}'::jsonb,*  
*created_at timestamptz not null default now()*  
*);*  
  
*-- Reports (user flags)*  
*create table review_report (*  
*report_id text primary key, -- rr\_...*  
*review_id text not null references review(review_id) on delete cascade,*  
*reporter_user_id text not null,*  
*reason_code text not null,*  
*details text,*  
*created_at timestamptz not null default now()*  
*);*  

**Indexes**

- *review(target_type, target_id, status)* for listing.
- *review(author_user_id, created_at)* to detect bursts.
- *reputation_aggregate(target_type, rating_recent_avg desc)* for search surfacing.
