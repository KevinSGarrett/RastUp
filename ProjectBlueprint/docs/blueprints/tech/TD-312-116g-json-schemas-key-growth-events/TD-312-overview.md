---
id: TD-312
title: "**1.16‑G. JSON Schemas — Key Growth Events**"
source_doc: "TechDevBlueprint.docx"
source_path: "docs\blueprints\tech\TD-312-116g-json-schemas-key-growth-events\TD-312-overview.md"
parent_id: 
anchor: "TD-312"
checksum: "sha256:584b2fda8612e229776d49a72f72bc964e5d4cf13173d7038cb346887d615362"
last_modified: "2025-11-06T20:40:46Z"
doc_kind: "TD"
h_level: 2
---
<a id="TD-312"></a>
## **1.16‑G. JSON Schemas — Key Growth Events**

**Recommended filename/path:** *data/schemas/growth-events/*

*// search.saved.v1.json*  
*{*  
*"\$id": "*[*https://rastup/schemas/search.saved.v1.json*](https://rastup/schemas/search.saved.v1.json)*",*  
*"\$schema": "*[*https://json-schema.org/draft/2020-12/schema*](https://json-schema.org/draft/2020-12/schema)*",*  
*"type": "object",*  
*"required": \["scope","city","query_hash"\],*  
*"properties": {*  
*"scope": { "type": "string", "enum": \["people","studios"\] },*  
*"city": { "type": "string" },*  
*"query_hash": { "type": "string" }*  
*},*  
*"additionalProperties": false*  
*}*  

*// alert.sent.v1.json*  
*{*  
*"\$id": "*[*https://rastup/schemas/alert.sent.v1.json*](https://rastup/schemas/alert.sent.v1.json)*",*  
*"\$schema": "*[*https://json-schema.org/draft/2020-12/schema*](https://json-schema.org/draft/2020-12/schema)*",*  
*"type": "object",*  
*"required": \["search_id","count","channel"\],*  
*"properties": {*  
*"search_id": { "type": "string" },*  
*"count": { "type": "integer", "minimum": 1 },*  
*"channel": { "type": "string", "enum": \["email","inapp"\] }*  
*},*  
*"additionalProperties": false*  
*}*  

*// referral.invite.v1.json*  
*{*  
*"\$id": "*[*https://rastup/schemas/referral.invite.v1.json*](https://rastup/schemas/referral.invite.v1.json)*",*  
*"\$schema": "*[*https://json-schema.org/draft/2020-12/schema*](https://json-schema.org/draft/2020-12/schema)*",*  
*"type": "object",*  
*"required": \["program_id","inviter_user_id","invitee_email_sha"\],*  
*"properties": {*  
*"program_id": { "type": "string" },*  
*"inviter_user_id": { "type": "string" },*  
*"invitee_email_sha": { "type": "string" },*  
*"source": { "type": "string" }*  
*},*  
*"additionalProperties": false*  
*}*
