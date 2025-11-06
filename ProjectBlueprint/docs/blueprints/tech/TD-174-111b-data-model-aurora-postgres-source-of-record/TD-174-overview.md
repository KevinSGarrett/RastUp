---
id: TD-174
title: "**1.11.B Data model (Aurora Postgres, source of record)**"
source_doc: "TechDevBlueprint.docx"
source_path: "docs\blueprints\tech\TD-174-111b-data-model-aurora-postgres-source-of-record\TD-174-overview.md"
parent_id: 
anchor: "TD-174"
checksum: "sha256:c16badd2205fe879e9af66d9c904ed0c36824b751e49fb6b3320d86b9d99e71a"
last_modified: "2025-11-06T20:40:46Z"
doc_kind: "TD"
h_level: 2
---
<a id="TD-174"></a>
## **1.11.B Data model (Aurora Postgres, source of record)**

*create table studio (*  
*studio_id text primary key, -- std\_...*  
*owner_user_id text not null, -- usr\_...*  
*title text not null,*  
*slug text not null unique, -- /studio/{slug}*  
*description text not null,*  
*city text not null,*  
*region text not null, -- state/province*  
*country text not null default 'US',*  
*geo_lat numeric(9,6) not null,*  
*geo_lon numeric(9,6) not null,*  
*address_json jsonb not null, -- {line1,line2,city,region,postal,country}; private UI*  
*is_published boolean not null default false,*  
*verified_studio boolean not null default false,*  
*verification_json jsonb not null default '{}'::jsonb, -- docs summary (no images)*  
*deposit_required boolean not null default false,*  
*deposit_auth_cents int not null default 0, -- default auth amount (can be 0)*  
*capacity_people int not null default 0,*  
*size_sqft int, -- optional*  
*house_rules_json jsonb not null default '\[\]'::jsonb,*  
*amenities_json jsonb not null default '\[\]'::jsonb, -- string\[\] canonical keys*  
*insurance_confirmed boolean not null default false,*  
*rating_avg numeric(3,2) not null default 0.00,*  
*rating_count int not null default 0,*  
*price_from_cents int not null default 0, -- normalized floor*  
*currency text not null default 'USD',*  
*created_at timestamptz not null default now(),*  
*updated_at timestamptz not null default now()*  
*);*  
  
*-- Pricing schedules (hourly, slot, or day rates with peak/off-peak)*  
*create type studio_rate_kind as enum ('hourly','slot','day');*  
  
*create table studio_rate (*  
*rate_id text primary key, -- srt\_...*  
*studio_id text not null references studio(studio_id) on delete cascade,*  
*kind studio_rate_kind not null,*  
*name text not null, -- "Weekday Hourly", "Weekend Slot"*  
*dow int\[\] not null, -- 0=Sun..6=Sat*  
*start_local time not null, -- for 'hourly' window or slot start*  
*end_local time not null, -- for 'hourly' window or slot end*  
*slot_minutes int, -- required for 'slot'*  
*price_cents int not null, -- per hour/slot/day depending on kind*  
*overtime_cents_per_30m int not null default 0,*  
*min_booking_minutes int not null default 60,*  
*max_booking_minutes int, -- optional cap*  
*tax_inclusive boolean not null default false, -- rarely true; standard is false*  
*active boolean not null default true,*  
*created_at timestamptz not null default now()*  
*);*  
  
*-- Blackouts and buffers*  
*create table studio_blackout (*  
*blackout_id text primary key, -- sbo\_...*  
*studio_id text not null references studio(studio_id) on delete cascade,*  
*start_at timestamptz not null,*  
*end_at timestamptz not null,*  
*reason text*  
*);*  
  
*-- Default buffers & cleanup windows (applies to all bookings unless overridden)*  
*create table studio_policy (*  
*studio_id text primary key references studio(studio_id) on delete cascade,*  
*buffer_before_min int not null default 30,*  
*buffer_after_min int not null default 30,*  
*cleaning_min int not null default 0,*  
*cancellation_policy jsonb not null default '{}'::jsonb -- bands like §1.3.L*  
*);*  
  
*-- Media (previews only; S3 keys; NSFW band)*  
*create table studio_media (*  
*media_id text primary key, -- smd\_...*  
*studio_id text not null references studio(studio_id) on delete cascade,*  
*kind text not null check (kind in ('image','video')),*  
*s3_key text not null,*  
*width int,*  
*height int,*  
*nsfw_band int not null default 0, -- 0 allow, 1 blur, 2 block*  
*position int not null default 0,*  
*created_at timestamptz not null default now()*  
*);*  
*create index on studio_media(studio_id, position);*  
  
*-- Studio verification audit trail*  
*create table studio_verification_audit (*  
*sva_id text primary key, -- sva\_...*  
*studio_id text not null references studio(studio_id) on delete cascade,*  
*action text not null check (action in ('submitted','approved','rejected','revoked')),*  
*actor_user_id text not null, -- admin*  
*reason text,*  
*created_at timestamptz not null default now()*  
*);*  

**Indices**

- *studio(city, is_published)* for city listing.
- *studio(owner_user_id, updated_at desc)* for owner dashboards.
- Partial index: *studio(is_published and verified_studio)* for search gating.
