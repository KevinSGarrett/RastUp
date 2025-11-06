---
id: TD-490
title: "**1.26.4 Data model (Aurora) — cases, actions, audit**"
source_doc: "TechDevBlueprint.docx"
source_path: "docs\blueprints\tech\TD-490-1264-data-model-aurora-cases-actions-audit\TD-490-overview.md"
parent_id: 
anchor: "TD-490"
checksum: "sha256:dd767887711239bf411580c403d641dd3b448e011a47cf60d8e1988448885af1"
last_modified: "2025-11-06T20:40:46Z"
doc_kind: "TD"
h_level: 2
---
<a id="TD-490"></a>
## **1.26.4 Data model (Aurora) — cases, actions, audit**

**Recommended path:** *db/migrations/026_admin_core.sql*

*begin;*  
  
*create table admin_case (*  
*case_id text primary key, -- cas\_...*  
*kind text not null check (kind in ('report','dmca','dispute','appeal','fraud')),*  
*status text not null check (status in ('new','triage','investigating','awaiting_user','resolved','closed')),*  
*priority int not null default 3, -- 1 .. 5*  
*opened_by text not null, -- usr\_... or system*  
*subject_user text, -- user primarily involved*  
*order_id text, -- optional link*  
*thread_id text, -- optional link*  
*listing_id text, -- person/studio id*  
*summary text not null,*  
*sla_due_at timestamptz,*  
*created_at timestamptz default now(),*  
*updated_at timestamptz default now()*  
*);*  
  
*create table admin_action (*  
*action_id text primary key, -- act\_...*  
*case_id text references admin_case(case_id) on delete cascade,*  
*actor_admin text not null, -- admin user id (oidc subject)*  
*action text not null, -- 'suspend','refund','request_evidence','note','close',...*  
*payload jsonb,*  
*created_at timestamptz default now()*  
*);*  
  
*create table admin_audit (*  
*audit_id text primary key, -- aud\_...*  
*actor_admin text not null,*  
*resource text not null, -- 'user:usr\_...','order:ord\_...'*  
*action text not null,*  
*payload jsonb,*  
*ip inet,*  
*user_agent text,*  
*created_at timestamptz default now()*  
*);*  
  
*commit;*  

**Immutable stream.** All *admin_audit* rows also appended to S3 with **Object Lock** (WORM).
