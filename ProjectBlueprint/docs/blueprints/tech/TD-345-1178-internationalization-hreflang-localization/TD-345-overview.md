---
id: TD-345
title: "**1.17.8 Internationalization (hreflang) & Localization**"
source_doc: "TechDevBlueprint.docx"
source_path: "docs\blueprints\tech\TD-345-1178-internationalization-hreflang-localization\TD-345-overview.md"
parent_id: 
anchor: "TD-345"
checksum: "sha256:ae7c1960b1fa438d63a295adf4ca9a028f1d33571f9fe94ee94cc8909643e7d3"
last_modified: "2025-11-06T20:40:46Z"
doc_kind: "TD"
h_level: 2
---
<a id="TD-345"></a>
## **1.17.8 Internationalization (hreflang) & Localization**

- Launch locale: **en‑US**; all public pages must set *\<html lang="en"\>*.
- **Hreflang scaffolding** in head for future locales; keep canonical **without** locale in path; add *\<link rel="alternate" hreflang="…"\>* once translations ship.
- Localize **currency/date/number** rendering server‑side for public pages; keep URLs stable.

**Artifact — hreflang helper**  
*Recommended path:* *web/lib/hreflang.ts*

*export const hreflangLinks = (canonical, alts) =\>*  
*alts.map(a =\> \`\<link rel="alternate" hreflang="\${a.lang}" href="\${a.href}"\>\`).join("\n")*  
* + \`\n\<link rel="alternate" hreflang="x-default" href="\${canonical}"\>\`;*
