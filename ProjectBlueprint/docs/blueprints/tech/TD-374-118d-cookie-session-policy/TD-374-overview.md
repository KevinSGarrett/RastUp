---
id: TD-374
title: "**1.18.D Cookie & Session Policy**"
source_doc: "TechDevBlueprint.docx"
source_path: "docs\blueprints\tech\TD-374-118d-cookie-session-policy\TD-374-overview.md"
parent_id: 
anchor: "TD-374"
checksum: "sha256:922e28eb41b3c146ddee0ba45f2d026a560533db79a5c90af3745f1da3271832"
last_modified: "2025-11-06T20:40:46Z"
doc_kind: "TD"
h_level: 2
---
<a id="TD-374"></a>
## **1.18.D Cookie & Session Policy**

**Recommended path:** *security/cookies/policy.md*

*Cookies*  
*- \_\_Host-rastup: session JWT reference; SameSite=Lax; Secure; HttpOnly; Path=/; Domain=\<none\>; Prefix=\_\_Host*  
*- consent: preference state; SameSite=Lax; Secure; HttpOnly=false*  
*- cfduid/edge: none (avoid third-party identifiers)*  
  
*Rules*  
*- No third-party trackers on public pages.*  
*- Analytics via first-party beacon only; respect consent.*  
*- JWTs not stored in localStorage; refresh via secure cookie.*
