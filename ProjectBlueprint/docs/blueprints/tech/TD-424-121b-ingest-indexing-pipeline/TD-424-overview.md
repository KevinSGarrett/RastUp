---
id: TD-424
title: "**1.21.B Ingest & indexing pipeline**"
source_doc: "TechDevBlueprint.docx"
source_path: "docs\blueprints\tech\TD-424-121b-ingest-indexing-pipeline\TD-424-overview.md"
parent_id: 
anchor: "TD-424"
checksum: "sha256:a0529b0e48a3b2fb5a3631d647ce44c451e5db31fcb0aa46b2876541c1ba58d9"
last_modified: "2025-11-06T20:40:46Z"
doc_kind: "TD"
h_level: 2
---
<a id="TD-424"></a>
## **1.21.B Ingest & indexing pipeline**

**Sources:** Aurora (entities), S3 (SFW previews/derived tags), computed‑signals service.

**Flow:** publish/edit/booking → **Kinesis change topic** → **Indexer Lambda** → Typesense *upsert*.

**Recommended path:** *search/events/entity-change.json*

*{ "kind":"entity.updated", "entity":"person\|studio", "id":"sp\_...\|st\_...", "reason":"publish\|edit\|review\|booking\|availability", "ts":"2025-11-06T15:10:01Z" }*  

**Recommended path:** *search/indexer/indexer.ts*

*for (const evt of stream) {*  
*const base = await loadEntity(evt.entity, evt.id);*  
*const signals = await computeSignals(evt.entity, evt.id);*  
*const doc = toSearchDocument(base, signals); // SFW-only*  
*await typesense.collections(coll(evt.entity)).documents().upsert(doc, { 'dirty_values':'coerce_or_drop' });*  
*}*  

**Reindex runbook** (alias flip, dual‑write, shadow compare): *search/runbooks/reindex.md*.
