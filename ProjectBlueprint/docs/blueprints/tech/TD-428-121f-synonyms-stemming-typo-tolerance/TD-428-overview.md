---
id: TD-428
title: "**1.21.F Synonyms, stemming & typo tolerance**"
source_doc: "TechDevBlueprint.docx"
source_path: "docs\blueprints\tech\TD-428-121f-synonyms-stemming-typo-tolerance\TD-428-overview.md"
parent_id: 
anchor: "TD-428"
checksum: "sha256:1c2d8967825768de3459e197caca0d59d9b88fc16704fdd86f4b8b7b3cab15f5"
last_modified: "2025-11-06T20:40:46Z"
doc_kind: "TD"
h_level: 2
---
<a id="TD-428"></a>
## **1.21.F Synonyms, stemming & typo tolerance**

- Domain synonyms (e.g., *“cyclorama” ⇄ “cyc wall”*), city nicknames (*“NYC” ⇄ “New York City”*).
- Typos: **2** for terms \>5 chars, **1** for 3–5 chars, exact for ≤2 chars.
- **Recommended path:** *search/schemas/synonyms.json*.
