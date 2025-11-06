---
id: TD-551
title: "**1.3.3 Data model (Aurora, schema** ***booking*****)**"
source_doc: "TechDevBlueprint.docx"
source_path: "docs\blueprints\tech\TD-551-133-data-model-aurora-schema-booking\TD-551-overview.md"
parent_id: 
anchor: "TD-551"
checksum: "sha256:d46881291c1cd21b9700270693a4dee91b14545822233926396aecfcea0669a6"
last_modified: "2025-11-06T20:40:46Z"
doc_kind: "TD"
h_level: 2
---
<a id="TD-551"></a>
## **1.3.3 Data model (Aurora, schema** ***booking*****)**

**Recommended path:** *db/migrations/013_booking_core.sql*

*begin;*  
  
*create type booking_mode as enum ('IB','RTB','INVITE');*  
*create type booking_status as enum (*  
*'initiated','pending_accept','countered','accepted','declined',*  
*'confirmed','in_progress','delivered','completed',*  
*'cancelled_buyer','cancelled_provider','disputed','resolved'*  
*);*  
  
*-- Core order*  
*create table booking.order (*  
*order_id text primary key, -- ord\_...*  
*buyer_user_id text not null,*  
*provider_user_id text not null, -- owner of Service Profile*  
*service_profile_id text not null,*  
*package_id text, -- null when base rate*  
*mode booking_mode not null,*  
*status booking_status not null default 'initiated',*  
*city text, -- normalized city for search/seo*  
*start_ts timestamptz not null,*  
*end_ts timestamptz not null,*  
*location_kind text not null check (location_kind in ('buyer','provider_studio','rented_studio','remote')),*  
*location_address text, -- revealed to parties post-confirm*  
*travel_miles numeric, -- for travel fee calc*  
*license_tier text, -- 'commercial','ads','exclusive','buyout'...*  
*subtotal_cents int not null default 0,*  
*platform_fee_cents int not null default 0,*  
*tax_cents int not null default 0,*  
*tip_cents int not null default 0,*  
*total_cents int not null default 0, -- money charged to buyer*  
*currency text not null default 'usd',*  
*stripe_payment_intent_id text,*  
*connect_transfer_group text,*  
*chat_thread_id text, -- opens on confirm*  
*created_at timestamptz default now(),*  
*updated_at timestamptz default now()*  
*);*  
  
*-- Line items (packages, extras, travel, license)*  
*create table booking.line_item (*  
*id text primary key,*  
*order_id text references booking.order(order_id) on delete cascade,*  
*kind text not null check (kind in ('package','extra','travel','license','adjustment','refund')),*  
*title text not null,*  
*qty numeric not null default 1,*  
*unit_cents int not null,*  
*total_cents int not null*  
*);*  
  
*-- Auto-accept rules (owned by provider)*  
*create table booking.autoaccept_rule (*  
*rule_id text primary key,*  
*service_profile_id text not null,*  
*min_price_cents int,*  
*weekday_mask int, -- bitmask; e.g., Mon..Sun*  
*max_distance_mi numeric,*  
*allow_ib boolean not null default false*  
*);*  
  
*-- Request → Accept / Decline / Counter (Custom Offer)*  
*create table booking.request (*  
*request_id text primary key, -- req\_...*  
*mode booking_mode not null,*  
*order_id text not null, -- binds to a draft order*  
*buyer_user_id text not null,*  
*provider_user_id text not null,*  
*status text not null check (status in ('pending','accepted','declined','countered','expired')),*  
*message text,*  
*expires_at timestamptz,*  
*created_at timestamptz default now()*  
*);*  
  
*-- Smart Invite fan-out recipients*  
*create table booking.invite_recipient (*  
*invite_id text,*  
*recipient_user_id text,*  
*status text not null check (status in ('new','responded','awarded','not_awarded')),*  
*primary key (invite_id, recipient_user_id)*  
*);*  
  
*-- Milestones (deliverable-based jobs)*  
*create table booking.milestone (*  
*milestone_id text primary key,*  
*order_id text not null,*  
*title text not null,*  
*due_ts timestamptz,*  
*amount_cents int not null, -- portion of subtotal*  
*status text not null check (status in ('open','delivered','approved','disputed','refunded'))*  
*);*  
  
*-- Disputes*  
*create table booking.dispute (*  
*dispute_id text primary key, -- dsp\_...*  
*order_id text not null,*  
*opened_by text not null, -- buyer or provider*  
*reason text not null,*  
*description text,*  
*status text not null check (status in ('open','awaiting_evidence','under_review','resolved_buyer','resolved_provider','split','chargeback')),*  
*created_at timestamptz default now(),*  
*updated_at timestamptz default now()*  
*);*  
  
*commit;*  

**Studio damage deposits** (auth‑only holds) live in §1.24 schema; talent bookings do not use deposit holds at launch. (Cross‑ref only; no duplication here.)
