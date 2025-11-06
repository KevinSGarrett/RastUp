---
id: TD-582
title: "**1.4.B Inbox search syntax & Typesense mapping**"
source_doc: "TechDevBlueprint.docx"
source_path: "docs\blueprints\tech\TD-582-14b-inbox-search-syntax-typesense-mapping\TD-582-overview.md"
parent_id: 
anchor: "TD-582"
checksum: "sha256:e8881212754fe406bc8fbf442479d188593f22369e604739c23643cd97e10156"
last_modified: "2025-11-06T20:40:46Z"
doc_kind: "TD"
h_level: 2
---
<a id="TD-582"></a>
## **1.4.B Inbox search syntax & Typesense mapping**

**Query syntax (user‑facing):**

- Free‑text across sender names, message body, and **card titles**.
- Filters: *from:@handle*, *to:@handle*, *role:model\|photographer\|videographer\|creator*, *type:booking\|inquiry\|invite\|support*, *has:file\|image\|card*, *card:reschedule\|extras\|proofs\|expense\|complete\|dispute\|safety*, *date:2025-11*, *city:"Los Angeles"*.

NonTechBlueprint

**Typesense collection** ***inbox_index*** **(flattened per message)**:

*{*  
*"name": "inbox_index",*  
*"fields": \[*  
*{"name":"userId","type":"string"},*  
*{"name":"threadId","type":"string"},*  
*{"name":"kind","type":"string"}, // inquiry\|booking\|invite\|support*  
*{"name":"participants","type":"string\[\]"},*  
*{"name":"role","type":"string"}, // Model/Photographer/...*  
*{"name":"city","type":"string"},*  
*{"name":"has","type":"string\[\]"}, // file\|image\|card*  
*{"name":"card","type":"string\[\]"}, // reschedule\|extras\|...*  
*{"name":"text","type":"string"},*  
*{"name":"ts","type":"int64", "optional": false}*  
*\],*  
*"default_sorting_field": "ts"*  
*}*  

**Indexing rules**

- Every new message produces one doc per **recipient** (for personal inbox views).
- *text* contains message body **or** card summary (e.g., “Reschedule from 2–5pm → 3–6pm”).
- *has* is derived from attachments/card presence.
- **Data minimization:** do **not** index PII (addresses, phone) or full proofs; index only file names and user‑provided titles.

NonTechBlueprint

**Examples**

- *card:extras role:photographer* → threads with extras proposals to you from photographers.
- *has:file date:2025-11* → threads with docs shared this month.
