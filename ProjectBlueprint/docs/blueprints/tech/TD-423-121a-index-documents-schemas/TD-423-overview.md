---
id: TD-423
title: "**1.21.A Index documents & schemas**"
source_doc: "TechDevBlueprint.docx"
source_path: "docs\blueprints\tech\TD-423-121a-index-documents-schemas\TD-423-overview.md"
parent_id: 
anchor: "TD-423"
checksum: "sha256:bcf8d7e6d1dc18d4d6b631aecc5b689ea3f240b67d891e00e030ab3cbeacd4b3"
last_modified: "2025-11-06T20:40:46Z"
doc_kind: "TD"
h_level: 2
---
<a id="TD-423"></a>
## **1.21.A Index documents & schemas**

We maintain two primary collections: *people_v1* and *studios_v1*. All public fields are **SFW‑only** (no 18+ media or attributes). Private/sensitive fields never enter search docs.

**Recommended path:** *search/schemas/typesense.json*

*{*  
*"collections": \[*  
*{*  
*"name": "people_v1",*  
*"fields": \[*  
*{"name":"id","type":"string"},*  
*{"name":"handle","type":"string"},*  
*{"name":"displayName","type":"string"},*  
*{"name":"roles","type":"string\[\]","facet":true},*  
*{"name":"genres","type":"string\[\]","facet":true},*  
*{"name":"city","type":"string","facet":true},*  
*{"name":"region","type":"string","facet":true},*  
*{"name":"country","type":"string","facet":true},*  
*{"name":"lat","type":"float"},*  
*{"name":"lon","type":"float"},*  
*{"name":"verified","type":"bool","facet":true},*  
*{"name":"trusted","type":"bool","facet":true},*  
*{"name":"nsfw_band","type":"int32","facet":true},*  
*{"name":"priceFromCents","type":"int64","facet":true},*  
*{"name":"priceToCents","type":"int64","facet":true},*  
*{"name":"amenities","type":"string\[\]","facet":true},*  
*{"name":"packagesCount","type":"int32"},*  
*{"name":"repScore","type":"float"},*  
*{"name":"recencyScore","type":"float"},*  
*{"name":"engagementScore","type":"float"},*  
*{"name":"availabilityScore","type":"float"},*  
*{"name":"completenessScore","type":"float"},*  
*{"name":"updatedAt","type":"int64"},*  
*{"name":"createdAt","type":"int64"}*  
*\],*  
*"default_sorting_field": "updatedAt"*  
*},*  
*{*  
*"name":"studios_v1",*  
*"fields":\[*  
*{"name":"id","type":"string"},*  
*{"name":"slug","type":"string"},*  
*{"name":"name","type":"string"},*  
*{"name":"city","type":"string","facet":true},*  
*{"name":"region","type":"string","facet":true},*  
*{"name":"country","type":"string","facet":true},*  
*{"name":"lat","type":"float"},*  
*{"name":"lon","type":"float"},*  
*{"name":"verified","type":"bool","facet":true},*  
*{"name":"nsfw_band","type":"int32","facet":true},*  
*{"name":"amenities","type":"string\[\]","facet":true},*  
*{"name":"priceFromCents","type":"int64","facet":true},*  
*{"name":"priceToCents","type":"int64","facet":true},*  
*{"name":"sizeSqFt","type":"int32","facet":true},*  
*{"name":"recencyScore","type":"float"},*  
*{"name":"engagementScore","type":"float"},*  
*{"name":"bookingScore","type":"float"},*  
*{"name":"updatedAt","type":"int64"},*  
*{"name":"createdAt","type":"int64"}*  
*\],*  
*"default_sorting_field": "updatedAt"*  
*}*  
*\]*  
*}*
