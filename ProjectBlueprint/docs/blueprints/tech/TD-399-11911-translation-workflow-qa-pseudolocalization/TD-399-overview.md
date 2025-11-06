---
id: TD-399
title: "**1.19.11 Translation workflow, QA & pseudolocalization**"
source_doc: "TechDevBlueprint.docx"
source_path: "docs\blueprints\tech\TD-399-11911-translation-workflow-qa-pseudolocalization\TD-399-overview.md"
parent_id: 
anchor: "TD-399"
checksum: "sha256:ee934eb5b499b96504f557fb85b68a926586d29126b551cf259f3989066e73e4"
last_modified: "2025-11-06T20:40:46Z"
doc_kind: "TD"
h_level: 2
---
<a id="TD-399"></a>
## **1.19.11 Translation workflow, QA & pseudolocalization**

**Workflow**

2020. Devs mark strings with *t('key')*.
2021. Extract → *messages.pot* (CI).
2022. Translate in Git (JSON catalogs), not in CMS; PR review by language owners.
2023. **Pseudolocalization** stage (*\[!! Ŧêxţ ẽłôñĝąţęđ !!\]*) to catch truncation/overflow.
2024. Screenshot diff QA for top pages per locale (Crowd‑shots optional later).
2025. Version catalogs; invalidate CDN on merge.

**Pseudolocalizer script**  
**Recommended path:** *i18n/tools/pseudo.ts*

*export function pseudo(s: string){ return s.replace(/\[aAeEiIoOuUc\]/g, m =\> ({a:"á",e:"ë",i:"ï",o:"ø",u:"ü",c:"ç"}\[m.toLowerCase()\] \|\| m)).replace(/(\[a-z\])/gi,"\$1\u0301"); }*
