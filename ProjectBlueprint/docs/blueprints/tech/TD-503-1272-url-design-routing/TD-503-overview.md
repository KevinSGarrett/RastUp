---
id: TD-503
title: "**1.27.2 URL design & routing**"
source_doc: "TechDevBlueprint.docx"
source_path: "docs\blueprints\tech\TD-503-1272-url-design-routing\TD-503-overview.md"
parent_id: 
anchor: "TD-503"
checksum: "sha256:16d5b7961fc112d03d76fab33c92c4193808a7a3f7b680e4e4d915c8da8d17bb"
last_modified: "2025-11-06T20:40:46Z"
doc_kind: "TD"
h_level: 2
---
<a id="TD-503"></a>
## **1.27.2 URL design & routing**

**Pages (examples):**

- City directory: */tx/houston/models* (*/state/city/role*)
- Genre slice: */tx/houston/models/editorial*
- Studio directory: */tx/houston/studios*
- Profile: */p/{handle}* (SFW profile)
- Studio: */s/{slug}* (SFW listing; exact address hidden)
- Content hubs / guides (optional): */guides/houston-photography-studios*

**Canonical param whitelist:** *?page=*, *?sort=* limited to *best\|new\|price_low\|price_high\|distance* when an origin exists. All other params are dropped in canonicals. Deep facet queries (ANY/ALL filters) **do not** get indexable canonicals.
