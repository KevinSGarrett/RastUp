---
id: TD-317
title: "**1.16-L. ANY/ALL Query Builder — Typesense/OpenSearch spec**"
source_doc: "TechDevBlueprint.docx"
source_path: "docs\blueprints\tech\TD-317-116-l-anyall-query-builder-typesenseopensearch-spec\TD-317-overview.md"
parent_id: 
anchor: "TD-317"
checksum: "sha256:a62f415344c5ec608eab692c3c09c98077c449547ace1a10dd603959b8f0012f"
last_modified: "2025-11-06T20:40:46Z"
doc_kind: "TD"
h_level: 2
---
<a id="TD-317"></a>
## **1.16-L. ANY/ALL Query Builder — Typesense/OpenSearch spec**

**Recommended filename/path:** *search/spec/any_all_query_builder.md*

*Goal*  
*Support saved searches with (ANY OR ALL) filter groups over people/studios while enforcing Safe-Mode.*  
  
*Input*  
*queryJson:*  
*{*  
*"any": \[*  
*{"field":"roleFields.genres","op":"in","value":\["fashion","editorial"\]},*  
*{"field":"verification.id","op":"eq","value":true}*  
*\],*  
*"all": \[*  
*{"field":"city","op":"eq","value":"Houston"},*  
*{"field":"priceFromCents","op":"between","value":\[10000,30000\]}*  
*\]*  
*}*  
  
*Algorithm (Typesense flavor)*  
* - Base filters: city:={{city}} AND isPublished:=true AND safeModeBandMax:\<= {{safeMode?1:2}}*  
* - Build ANY clause:*  
* - Map each criterion to Typesense filter expression:*  
*\* in: field:=\[v1, v2, ...\]*  
*\* eq: field:=value*  
*\* between: field:\>={{lo}} && field:\<={{hi}}*  
* - ANY -\> join with " \|\| "*  
* - Build ALL clause: same mapping, join with " && "*  
* - Combined: base && ( (ANY) \|\| true_if_any_empty ) && (ALL)*  
* - Sorting: text match score, geo distance, repScore, verifyBoost, priceFit*  
* - Pagination: cursor API; record query_hash for analytics and dedupe.*  
  
*OpenSearch variant*  
* - Translate to bool query:*  
*{*  
*"bool": {*  
*"filter": \[*  
*{"term":{"city":"houston"}},*  
*{"term":{"isPublished":true}},*  
*{"range":{"safeModeBandMax":{"lte": safeMode?1:2}}}*  
*\],*  
*"must": \[ ...ALL... \],*  
*"should": \[ ...ANY... \],*  
*"minimum_should_match": {{ANY? 1 : 0}}*  
*}*  
*}*
