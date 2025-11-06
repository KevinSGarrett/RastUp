---
id: TD-523
title: "**1.28.4 Data model (cases, actions, audit)**"
source_doc: "TechDevBlueprint.docx"
source_path: "docs\blueprints\tech\TD-523-1284-data-model-cases-actions-audit\TD-523-overview.md"
parent_id: 
anchor: "TD-523"
checksum: "sha256:0e981fdb65aa856f9186510aee0dc88caed2f9d7ecc9d232520b067d1d5bfecc"
last_modified: "2025-11-06T20:40:46Z"
doc_kind: "TD"
h_level: 2
---
<a id="TD-523"></a>
## **1.28.4 Data model (cases, actions, audit)**

**Recommended path:** *db/migrations/028_admin_core.sql*

*begin;*  
  
*create table admin_case (*  
*case_id text primary key, -- cas\_...*  
*kind text not null check (kind in ('report','dmca','dispute','appeal','fraud')),*  
*status text not null check (status in ('new','triage','investigating','awaiting_user','resolved','closed')),*  
*priority int not null default 3, -- 1..5*  
*opened_by text not null, -- usr\_... or system*  
*subject_user text,*  
*order_id text,*  
*thread_id text,*  
*listing_id text,*  
*summary text not null,*  
*sla_due_at timestamptz,*  
*created_at timestamptz default now(),*  
*updated_at timestamptz default now()*  
*);*  
  
*create table admin_action (*  
*action_id text primary key, -- act\_...*  
*case_id text references admin_case(case_id) on delete cascade,*  
*actor_admin text not null, -- OIDC subject*  
*action text not null, -- 'suspend','refund','request_evidence','note','close',...*  
*payload jsonb,*  
*created_at timestamptz default now()*  
*);*  
  
*create table admin_audit (*  
*audit_id text primary key, -- aud\_...*  
*actor_admin text not null,*  
*resource text not null, -- 'user:usr\_...','order:ord\_...','doc:doc\_...'*  
*action text not null,*  
*payload jsonb,*  
*ip inet,*  
*user_agent text,*  
*created_at timestamptz default now()*  
*);*  
  
*commit;*  

**Immutable stream:** all *admin_audit* rows mirrored to S3 bucket with **Object Lock (WORM)**; lifecycle and retention per §1.18.
