---
id: TD-601
title: "**1.6.5 KB search (Typesense)**"
source_doc: "TechDevBlueprint.docx"
source_path: "docs\blueprints\tech\TD-601-165-kb-search-typesense\TD-601-overview.md"
parent_id: 
anchor: "TD-601"
checksum: "sha256:29994f25676f8eea5ccb279123f0656ca32e54c2255122b33008b24dd629f66c"
last_modified: "2025-11-06T20:40:46Z"
doc_kind: "TD"
h_level: 2
---
<a id="TD-601"></a>
## **1.6.5 KB search (Typesense)**

**Collection** ***kb_index*****:**

*{*  
*"name":"kb_index",*  
*"fields":\[*  
*{"name":"articleId","type":"string"},*  
*{"name":"slug","type":"string"},*  
*{"name":"title","type":"string"},*  
*{"name":"summary","type":"string"},*  
*{"name":"body","type":"string"},*  
*{"name":"category","type":"string"},*  
*{"name":"role","type":"string\[\]"},*  
*{"name":"locale","type":"string"},*  
*{"name":"updatedAt","type":"int64"}*  
*\],*  
*"default_sorting_field": "updatedAt"*  
*}*  

**Indexing rules**: strip code blocks, preserve headings; boost **title \> summary \> body**; filter by *role* and *locale*.  
**Query tokens**: free text + *category:*, *role:buyer\|provider\|studio*, *type:faq\|steps*, *updated:\<days\>*.
