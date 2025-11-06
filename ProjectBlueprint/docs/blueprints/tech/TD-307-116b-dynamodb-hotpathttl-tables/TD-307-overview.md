---
id: TD-307
title: "**1.16‑B. DynamoDB — hot‑path/TTL tables**"
source_doc: "TechDevBlueprint.docx"
source_path: "docs\blueprints\tech\TD-307-116b-dynamodb-hotpathttl-tables\TD-307-overview.md"
parent_id: 
anchor: "TD-307"
checksum: "sha256:5f353edf014153a10cde92d5af1c67eafcc1c0c87e2618191c58257af2282661"
last_modified: "2025-11-06T20:40:46Z"
doc_kind: "TD"
h_level: 2
---
<a id="TD-307"></a>
## **1.16‑B. DynamoDB — hot‑path/TTL tables**

**Recommended filename/path:** *infra/dynamodb/016_growth_ttl_tables.md* *(doc note for infra CDK)*

*Table: saved_search_dedupe*  
*Key: PK = search_id, SK = alert_date (YYYY-MM-DD)*  
*Attributes: ttl_epoch (Number)*  
*Purpose: ensure ≤1 alert/day/search; items auto-expire via TTL.*  
  
*Table: feed_fanout_cursor*  
*Key: PK = user_id, SK = 'cursor'*  
*Attributes: last_seen_created_at (ISO), last_seen_id*  
*Purpose: incremental paging for unified feed.*  
  
*Table: referral_device_daily*  
*Key: PK = device_fp#YYYY-MM-DD, SK = program_id*  
*Attributes: ip_hash, count*  
*TTL: next day*  
*Purpose: rate-limit & fraud signal for invites/accepts.*
