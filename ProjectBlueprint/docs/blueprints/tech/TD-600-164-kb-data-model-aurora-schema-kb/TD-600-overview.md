---
id: TD-600
title: "**1.6.4 KB data model (Aurora schema** ***kb*****)**"
source_doc: "TechDevBlueprint.docx"
source_path: "docs\blueprints\tech\TD-600-164-kb-data-model-aurora-schema-kb\TD-600-overview.md"
parent_id: 
anchor: "TD-600"
checksum: "sha256:6d8ba563e9c0176d6020977f8cb39b334fecb167c9d14612d7bf3c86dd9d6d55"
last_modified: "2025-11-06T20:40:46Z"
doc_kind: "TD"
h_level: 2
---
<a id="TD-600"></a>
## **1.6.4 KB data model (Aurora schema** ***kb*****)**

**DDL — paste into your doc** ***db/migrations/016_kb.sql*****:**

*begin;*  
  
*create table kb_category (*  
*category_id serial primary key,*  
*slug text unique not null,*  
*title text not null,*  
*ordinal int not null default 0,*  
*visible boolean not null default true*  
*);*  
  
*create table kb_article (*  
*article_id uuid primary key,*  
*category_id int references kb_category(category_id),*  
*slug text unique not null,*  
*title text not null,*  
*summary text not null, -- "At-a-glance"*  
*body_md text not null, -- Markdown*  
*role_audience text\[\], -- \["buyer","provider","studio"\]*  
*locale text not null default 'en-US',*  
*status text not null check (status in ('draft','review','published','archived')),*  
*published_at timestamptz,*  
*updated_at timestamptz default now()*  
*);*  
  
*create table kb_article_version (*  
*version_id uuid primary key,*  
*article_id uuid references kb_article(article_id) on delete cascade,*  
*editor_user_id text not null,*  
*body_md text not null,*  
*changelog text,*  
*created_at timestamptz default now()*  
*);*  
  
*create table kb_tag (*  
*tag text primary key*  
*);*  
  
*create table kb_article_tag (*  
*article_id uuid references kb_article(article_id) on delete cascade,*  
*tag text references kb_tag(tag),*  
*primary key (article_id, tag)*  
*);*  
  
*create table kb_redirect (*  
*from_slug text primary key,*  
*to_slug text not null*  
*);*  
  
*create table kb_feedback (*  
*article_id uuid references kb_article(article_id) on delete cascade,*  
*user_id text,*  
*helpful boolean,*  
*comment text,*  
*created_at timestamptz default now()*  
*);*  
  
*create table kb_relation (*  
*source_article_id uuid references kb_article(article_id) on delete cascade,*  
*target_kind text not null, -- 'action'\|'article'*  
*target_ref text not null, -- e.g., "app://orders/ord_123/refund" or article slug*  
*label text,*  
*ordinal int default 0*  
*);*  
  
*commit;*  

**S3 prefixes**: *kb/images/{articleId}/\** (webp, svg), *kb/downloads/{articleId}/\** (pdf templates).  
**SEO**: static routes */help/{category}/{slug}*; JSON‑LD *FAQPage* when an article has FAQs.
