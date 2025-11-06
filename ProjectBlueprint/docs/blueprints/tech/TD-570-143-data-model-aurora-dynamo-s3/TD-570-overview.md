---
id: TD-570
title: "**1.4.3 Data model (Aurora + Dynamo + S3)**"
source_doc: "TechDevBlueprint.docx"
source_path: "docs\blueprints\tech\TD-570-143-data-model-aurora-dynamo-s3\TD-570-overview.md"
parent_id: 
anchor: "TD-570"
checksum: "sha256:6cbb371c630445dbfa7bce6af6125338e800dfc86d914ed8f880d4331470dbd3"
last_modified: "2025-11-06T20:40:46Z"
doc_kind: "TD"
h_level: 2
---
<a id="TD-570"></a>
## **1.4.3 Data model (Aurora + Dynamo + S3)**

**Recommended path:** *db/migrations/014_messaging_inbox.sql*

*begin;*  
  
*create type thread_kind as enum ('inquiry','booking','studio','invite','support');*  
*create type request_status as enum ('pending','accepted','declined','blocked','expired');*  
*create type message_kind as enum ('text','image','file','card');*  
  
*create table thread (*  
*thread_id text primary key, -- thr\_...*  
*kind thread_kind not null,*  
*subject text,*  
*owner_order_id text, -- nullable; booking/studio link*  
*opened_by_user text not null,*  
*created_at timestamptz default now(),*  
*updated_at timestamptz default now(),*  
*last_msg_ts timestamptz*  
*);*  
  
*create table thread_participant (*  
*thread_id text references thread(thread_id) on delete cascade,*  
*user_id text not null,*  
*role text, -- buyer\|provider\|host\|support*  
*status text not null check (status in ('active','left','blocked')),*  
*last_read_ts timestamptz,*  
*muted_until timestamptz,*  
*primary key (thread_id, user_id)*  
*);*  
  
*create table message (*  
*message_id text primary key, -- msg\_...*  
*thread_id text not null references thread(thread_id) on delete cascade,*  
*sender_user text not null,*  
*kind message_kind not null,*  
*body_text text, -- for kind='text'*  
*card_type text, -- for kind='card' (reschedule, extras, proofs, expense, complete, dispute, safety)*  
*card_payload jsonb,*  
*attachment_meta jsonb, -- for images/files*  
*created_at timestamptz default now(),*  
*edited_at timestamptz*  
*);*  
  
*create table message_request_gate (*  
*gate_id text primary key, -- rqt\_...*  
*thread_id text not null,*  
*target_user text not null, -- the recipient who must accept/decline*  
*status request_status not null default 'pending',*  
*expires_at timestamptz, -- auto-expire if no action*  
*reason text -- spam heuristic reason*  
*);*  
  
*create table user_block (*  
*blocker_user text not null,*  
*blocked_user text not null,*  
*created_at timestamptz default now(),*  
*primary key (blocker_user, blocked_user)*  
*);*  
  
*-- Inbox indexing for fast lists*  
*create table inbox_index (*  
*user_id text not null,*  
*thread_id text not null,*  
*last_msg_ts timestamptz not null,*  
*folder text not null check (folder in ('all','action','bookings','offers','archived','spam')),*  
*unread_count int not null default 0,*  
*pinned boolean not null default false,*  
*primary key (user_id, thread_id)*  
*);*  
  
*commit;*  

**DynamoDB (ephemeral & rate‑limit)**

- *msg_typing* (*pk=thread_id*, *sk=user_id*, TTL 10s).
- *msg_rate* (*pk=user_id*, counters for message starts/hour; burst windows).
- *request_pending* (gate caches with TTL for quick pending checks).

**S3 prefixes**

- *threads/{threadId}/attachments/\** (images/proofs/receipts; virus scan lambda on upload).
- *threads/{threadId}/cards/\** (rendered PDFs if a card generates a doc preview).
