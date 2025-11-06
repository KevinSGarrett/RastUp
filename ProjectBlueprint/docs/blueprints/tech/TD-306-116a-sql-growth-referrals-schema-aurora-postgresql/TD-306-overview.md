---
id: TD-306
title: "**1.16‑A. SQL — Growth & Referrals schema (Aurora PostgreSQL)**"
source_doc: "TechDevBlueprint.docx"
source_path: "docs\blueprints\tech\TD-306-116a-sql-growth-referrals-schema-aurora-postgresql\TD-306-overview.md"
parent_id: 
anchor: "TD-306"
checksum: "sha256:8141f6b0df915148071baffc32d09d9e7277f99a608b2a88cb2870ff6f45aa2b"
last_modified: "2025-11-06T20:40:46Z"
doc_kind: "TD"
h_level: 2
---
<a id="TD-306"></a>
## **1.16‑A. SQL — Growth & Referrals schema (Aurora PostgreSQL)**

**Recommended filename/path:** *db/migrations/016_growth_referrals.sql*

*-- 016_growth_referrals.sql*  
*-- Saved searches (ANY/ALL filters), alert sends, follow graph, feed posts,*  
*-- referrals & credits (ledger), with sensible indexes.*  
  
*begin;*  
  
*create table if not exists saved_search (*  
*search_id text primary key, -- ssv\_...*  
*user_id text not null, -- usr\_...*  
*scope text not null check (scope in ('people','studios')),*  
*query_json jsonb not null, -- normalized ANY/ALL filters*  
*city text not null,*  
*paused_until date,*  
*last_alert_dt date,*  
*created_at timestamptz not null default now(),*  
*updated_at timestamptz not null default now()*  
*);*  
*create index if not exists idx_saved_search_user on saved_search(user_id);*  
*create index if not exists idx_saved_search_city on saved_search(city);*  
  
*create table if not exists saved_search_alert (*  
*alert_id text primary key, -- ssa\_...*  
*search_id text not null references saved_search(search_id) on delete cascade,*  
*alert_dt date not null,*  
*match_count int not null,*  
*email_sent boolean not null default false,*  
*inapp_created boolean not null default false,*  
*created_at timestamptz not null default now(),*  
*unique (search_id, alert_dt)*  
*);*  
  
*create table if not exists follow (*  
*follower_user_id text not null, -- usr\_...*  
*target_id text not null, -- usr\_... \| fsc\_...*  
*target_kind text not null check (target_kind in ('service_profile','fansub_creator')),*  
*created_at timestamptz not null default now(),*  
*primary key (follower_user_id, target_id, target_kind)*  
*);*  
  
*create table if not exists feed_post (*  
*feed_id text primary key, -- fdp\_...*  
*author_id text not null,*  
*role_tags text\[\] not null,*  
*kind text not null check (kind in ('case_study','availability','touring','studio_slot','influence')),*  
*title text not null,*  
*body_md text,*  
*media_preview jsonb not null default '\[\]'::jsonb, -- SFW previews only*  
*nsfw_band int not null default 0, -- 0 allow,1 blur,2 block*  
*city text,*  
*verified_chip boolean not null default false,*  
*is_published boolean not null default false,*  
*created_at timestamptz not null default now(),*  
*updated_at timestamptz not null default now()*  
*);*  
*create index if not exists idx_feed_post_pub on feed_post(is_published, created_at desc);*  
*create index if not exists idx_feed_post_city on feed_post(city);*  
  
*create table if not exists referral_program (*  
*program_id text primary key, -- rpr\_...*  
*kind text not null check (kind in ('provider_invites_provider','buyer_invites_buyer','cross_side')),*  
*reward_bips int not null default 0,*  
*reward_fixed_cents int not null default 0,*  
*credit_scope text not null, -- e.g., 'buyer_fee_only'*  
*monthly_cap int not null default 5,*  
*active boolean not null default true,*  
*created_at timestamptz not null default now()*  
*);*  
  
*create table if not exists referral_invite (*  
*invite_id text primary key, -- rfi\_...*  
*program_id text not null references referral_program(program_id),*  
*inviter_user_id text not null,*  
*invitee_user_id text,*  
*invitee_email_sha text not null,*  
*source text, -- 'sharecard','linkinbio', etc.*  
*device_fp text,*  
*ip_addr_sha text,*  
*created_at timestamptz not null default now(),*  
*accepted_at timestamptz*  
*);*  
*create index if not exists idx_rfi_inviter on referral_invite(inviter_user_id, created_at desc);*  
*create index if not exists idx_rfi_email on referral_invite(invitee_email_sha);*  
  
*create table if not exists credit_ledger (*  
*entry_id text primary key, -- crl\_...*  
*user_id text not null,*  
*kind text not null check (kind in ('award','clawback','redeem')),*  
*program_id text,*  
*amount_cents int not null,*  
*currency text not null default 'USD',*  
*reason text not null,*  
*related_id text,*  
*created_at timestamptz not null default now()*  
*);*  
*create index if not exists idx_credit_user on credit_ledger(user_id, created_at desc);*  
  
*commit;*
