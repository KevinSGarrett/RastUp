---
id: TD-123
title: "**1.8.C Write rules & lifecycle**"
source_doc: "TechDevBlueprint.docx"
source_path: "docs\blueprints\tech\TD-123-18c-write-rules-lifecycle\TD-123-overview.md"
parent_id: 
anchor: "TD-123"
checksum: "sha256:daed522fc4939c3dae3ccadb7694c85880ccc80f99e28e4bf447f1cd7dac6c19"
last_modified: "2025-11-06T20:40:46Z"
doc_kind: "TD"
h_level: 2
---
<a id="TD-123"></a>
## **1.8.C Write rules & lifecycle**

740. **Eligibility check** on *createReview*:

     88. *leg.status ∈ {completed}* and *leg.buyer_user_id = author_user_id*.
     89. No prior review by the same author for this *leg_id*.

741. **Edit window**: author may update title/body/facets within 24 h (config), but not the **rating** (to prevent score gaming).

742. **Photos**: preview-size only; NSFW scan; Safe-Mode on public surfaces.

743. **Status transitions**: *published → hidden/removed* (moderation), *removed → restored* (appeal).

744. **Deletion**: no hard delete—use *removed* + audit.
