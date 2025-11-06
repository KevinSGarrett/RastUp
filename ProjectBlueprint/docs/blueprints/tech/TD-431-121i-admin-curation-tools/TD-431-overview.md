---
id: TD-431
title: "**1.21.I Admin & curation tools**"
source_doc: "TechDevBlueprint.docx"
source_path: "docs\blueprints\tech\TD-431-121i-admin-curation-tools\TD-431-overview.md"
parent_id: 
anchor: "TD-431"
checksum: "sha256:5f96df1bd58470c434d05940d78c8f7febe5e01f985030ad5f68c491f1f2b9ae"
last_modified: "2025-11-06T20:40:46Z"
doc_kind: "TD"
h_level: 2
---
<a id="TD-431"></a>
## **1.21.I Admin & curation tools**

- **Pins** per city/query; TTL; stored in *search_curation* (DDL below).
- **Synonym editor** (admin UI) persisted in Aurora and synced to Typesense.
- **Bad queries** dashboard for zero‑results & low CTR.

**Recommended path:** *db/migrations/021_search_curations.sql*

*create table if not exists search_curation (*  
*cur_id text primary key, -- scu\_...*  
*scope text not null check (scope in ('people','studios')),*  
*city text not null,*  
*query text,*  
*pin_ids text\[\] not null,*  
*expires_at timestamptz,*  
*created_at timestamptz not null default now()*  
*);*
