---
id: TD-335
title: "**1.17.N Cost posture**"
source_doc: "TechDevBlueprint.docx"
source_path: "docs\blueprints\tech\TD-335-117n-cost-posture\TD-335-overview.md"
parent_id: 
anchor: "TD-335"
checksum: "sha256:be06915650229514443149dee53622a0441a8b66607520b528439e3c56ba1113"
last_modified: "2025-11-06T20:40:46Z"
doc_kind: "TD"
h_level: 2
---
<a id="TD-335"></a>
## **1.17.N Cost posture**

- **Edge caching** with ISR keeps SSR compute near‑zero for stable pages.
- **Static image transforms** for SFW previews; avoid runtime transformations for public pages when possible.
- **No third‑party SEO SaaS** at launch; rely on Search Console/Bing free tools; Lighthouse CI self‑hosted runner.
- **Sharecard worker** concurrency capped; aggressively cache results.
