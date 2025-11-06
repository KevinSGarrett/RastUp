---
id: TD-425
title: "**1.21.C Query model (ANY/ALL, Safe‑Mode, geo/price)**"
source_doc: "TechDevBlueprint.docx"
source_path: "docs\blueprints\tech\TD-425-121c-query-model-anyall-safemode-geoprice\TD-425-overview.md"
parent_id: 
anchor: "TD-425"
checksum: "sha256:3c4d985697687b39341c6ebc74e77f2fe644281f7fc27dae89aa22be529f8013"
last_modified: "2025-11-06T20:40:46Z"
doc_kind: "TD"
h_level: 2
---
<a id="TD-425"></a>
## **1.21.C Query model (ANY/ALL, Safe‑Mode, geo/price)**

Input mirrors §1.16’s saved‑search format:

*{*  
*"scope":"people\|studios",*  
*"city":"houston",*  
*"any":\[{"field":"genres","op":"in","value":\["fashion","editorial"\]}\],*  
*"all":\[{"field":"priceFromCents","op":"between","value":\[10000,30000\]},{"field":"verified","op":"eq","value":true}\],*  
*"safeMode":true,*  
*"sort":"best\|new\|distance\|price_low\|price_high",*  
*"origin":{"lat":29.7604,"lon":-95.3698}*  
*}*  

- **Safe‑Mode ON:** filter *nsfw_band \<= 1*.
- **Distance:** add *\_distance(lat,lon)* for sort and expose *distanceKm* in results.
- **Price:** hard filter via ranges; soft fitness in ranking (below).
