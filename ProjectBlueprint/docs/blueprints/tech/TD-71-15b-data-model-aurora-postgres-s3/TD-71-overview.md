---
id: TD-71
title: "**1.5.B Data model (Aurora Postgres + S3)**"
source_doc: "TechDevBlueprint.docx"
source_path: "docs\blueprints\tech\TD-71-15b-data-model-aurora-postgres-s3\TD-71-overview.md"
parent_id: 
anchor: "TD-71"
checksum: "sha256:8381947ece2cd4cf7443b240b0e9fb1ca197d5a1bf63b329374652e7f68cb517"
last_modified: "2025-11-06T20:40:46Z"
doc_kind: "TD"
h_level: 2
---
<a id="TD-71"></a>
## **1.5.B Data model (Aurora Postgres + S3)**

*-- Clause library (atomic building blocks)*  
*create table doc_clause (*  
*clause_id text primary key, -- cls\_...*  
*name text not null, -- "SOW: Base Terms", "Model Release: Adult", "House Rules: Standard"*  
*version int not null, -- semantic versions across edits*  
*city_gate text\[\], -- list of allowed city codes (null = global)*  
*role_gate text\[\], -- \['model','photographer','studio'\] filter*  
*is_active boolean default true,*  
*body_markdown text not null, -- authoring format*  
*variables_json jsonb not null, -- schema of variables required*  
*created_by text not null,*  
*created_at timestamptz not null default now(),*  
*published_at timestamptz,*  
*unique (name, version)*  
*);*  
  
*-- Document templates (ordered lists of clauses + layout & signers)*  
*create table doc_template (*  
*template_id text primary key, -- tpl\_...*  
*name text not null, -- "Talent SOW v3", "Studio House Rules v2"*  
*version int not null,*  
*city_gate text\[\],*  
*role_gate text\[\],*  
*clauses_ordered jsonb not null, -- e.g., \[{clause_id, version, order}\]*  
*layout_json jsonb not null, -- header/footer/logo, page breaks*  
*signer_roles jsonb not null, -- e.g., \[{role:'buyer'},{role:'talent'},{role:'witness'?}\]*  
*is_active boolean default true,*  
*created_by text not null,*  
*created_at timestamptz not null default now(),*  
*published_at timestamptz,*  
*unique (name, version)*  
*);*  
  
*-- Doc pack (generated for each leg at checkout)*  
*create table doc_pack (*  
*pack_id text primary key, -- dpk\_...*  
*leg_id text not null references booking_leg(leg_id) on delete cascade,*  
*status text not null check (status in ('draft','issued','signed','voided','superseded')),*  
*generator_ver text not null, -- codegen version hash*  
*city text not null,*  
*created_at timestamptz not null default now(),*  
*updated_at timestamptz not null default now(),*  
*unique (leg_id, status) deferrable initially deferred*  
*);*  
  
*-- Documents within a pack*  
*create table doc_instance (*  
*doc_id text primary key, -- doc\_...*  
*pack_id text not null references doc_pack(pack_id) on delete cascade,*  
*template_id text not null references doc_template(template_id),*  
*template_version int not null,*  
*variables_filled jsonb not null, -- resolved values at generate time*  
*render_pdf_s3 text, -- s3://bucket/key.pdf*  
*render_pdf_sha256 text, -- SHA-256 of PDF bytes*  
*envelope_id text, -- e-sign envelope id*  
*envelope_status text check (envelope_status in ('none','sent','completed','voided','expired')) default 'none',*  
*signer_map_json jsonb not null, -- mapping of signer roles -\> users/emails*  
*created_at timestamptz not null default now(),*  
*updated_at timestamptz not null default now()*  
*);*  
  
*-- Signer evidence log*  
*create table doc_sign_event (*  
*sign_event_id text primary key, -- dse\_...*  
*doc_id text not null references doc_instance(doc_id) on delete cascade,*  
*actor_role text not null, -- 'buyer','talent','studio_owner','witness'*  
*actor_user_id text,*  
*actor_email text,*  
*event text not null check (event in ('envelope_sent','viewed','signed','declined','voided','expired')),*  
*provider_payload jsonb not null,*  
*created_at timestamptz not null default now()*  
*);*  

**S3 layout**

*s3://docs/prod/packs/{pack_id}/*  
*doc\_{doc_id}\_v1.pdf \# immutable versioned PDF*  
*envelope\_{doc_id}.json \# e-sign provider metadata*  
*hash\_{doc_id}.txt \# SHA-256 digest*  

**Retention & legal hold**

- Bucket policy applies **7‑year retention**; legal hold flag per doc if Support/Legal initiates a hold.
