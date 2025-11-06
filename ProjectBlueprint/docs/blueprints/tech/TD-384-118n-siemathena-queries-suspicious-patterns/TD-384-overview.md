---
id: TD-384
title: "**1.18.N SIEM/Athena Queries (suspicious patterns)**"
source_doc: "TechDevBlueprint.docx"
source_path: "docs\blueprints\tech\TD-384-118n-siemathena-queries-suspicious-patterns\TD-384-overview.md"
parent_id: 
anchor: "TD-384"
checksum: "sha256:3bd5dcdff545ae1655d4f43319fa239ec9848bfee4490b0f68d60c634a8ad791"
last_modified: "2025-11-06T20:40:46Z"
doc_kind: "TD"
h_level: 2
---
<a id="TD-384"></a>
## **1.18.N SIEM/Athena Queries (suspicious patterns)**

**Recommended path:** *security/siem/queries.sql*

*-- Excessive GraphQL POSTs per IP in 5 min*  
*SELECT ip, count(\*) AS c*  
*FROM cf_logs*  
*WHERE cs_method='POST' AND cs_uri_stem LIKE '%/graphql%' AND date=CAST(current_date AS varchar)*  
*GROUP BY ip HAVING count(\*) \> 500;*  
  
*-- Admin OIDC logins outside office hours*  
*SELECT user, ts FROM admin_auth_logs*  
*WHERE hour(ts) NOT BETWEEN 8 AND 20 AND result='SUCCESS';*
