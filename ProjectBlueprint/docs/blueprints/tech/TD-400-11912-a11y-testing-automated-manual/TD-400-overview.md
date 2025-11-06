---
id: TD-400
title: "**1.19.12 A11y testing (automated + manual)**"
source_doc: "TechDevBlueprint.docx"
source_path: "docs\blueprints\tech\TD-400-11912-a11y-testing-automated-manual\TD-400-overview.md"
parent_id: 
anchor: "TD-400"
checksum: "sha256:97cf0a26c522d264277f815bd342dfff00d0d772b2ff53a759bbdda09bc60ac7"
last_modified: "2025-11-06T20:40:46Z"
doc_kind: "TD"
h_level: 2
---
<a id="TD-400"></a>
## **1.19.12 A11y testing (automated + manual)**

**Automated (CI):** axe + pa11y on */*, */city/{city}*, */p/{handle}*, */s/{slug}*, */checkout*.  
**Manual matrix:** keyboard‑only; screen readers (NVDA/Windows, VoiceOver/macOS), zoom 200%, high‑contrast mode, reduced‑motion, RTL reading order.  
**Defect SLAs:** A11y blockers = P1 (fix before release to prod); contrast/label issues = P2 (fix within 2 sprints).
