---
id: TD-426
title: "**1.21.D Autocomplete & suggestions**"
source_doc: "TechDevBlueprint.docx"
source_path: "docs\blueprints\tech\TD-426-121d-autocomplete-suggestions\TD-426-overview.md"
parent_id: 
anchor: "TD-426"
checksum: "sha256:9321877f0183c2295e9e0f6944a1adf482ac12af1e46912c930fc64d4198f81e"
last_modified: "2025-11-06T20:40:46Z"
doc_kind: "TD"
h_level: 2
---
<a id="TD-426"></a>
## **1.21.D Autocomplete & suggestions**

2108. **Prefix autocomplete** across *displayName/handle/genres/city* with typo tolerance.
2109. **Query suggestions** materialized from analytics (last 30 days), ranked by CTR and deduped; cached.

**Recommended path:** *search/api/autocomplete.ts*

*export async function autocomplete({ q, scope, city }) {*  
*const params = {*  
*q,*  
*query_by: scope==='people' ? 'displayName,handle,genres,city' : 'name,amenities,city',*  
*filter_by: \[\`city:=\${city}\`, 'nsfw_band:\<=1'\].join(' && '),*  
*per_page: 8,*  
*prefix: true,*  
*num_typos: 2*  
*};*  
*return typesense.collections(coll(scope)).documents().search(params);*  
*}*  

**Materialization SQL:** *search/suggestions/materialize.sql* (CTR@30d, thresholds, limit 2k).
