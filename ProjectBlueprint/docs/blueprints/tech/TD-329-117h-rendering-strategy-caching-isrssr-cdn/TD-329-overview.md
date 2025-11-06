---
id: TD-329
title: "**1.17.H Rendering strategy & caching (ISR/SSR + CDN)**"
source_doc: "TechDevBlueprint.docx"
source_path: "docs\blueprints\tech\TD-329-117h-rendering-strategy-caching-isrssr-cdn\TD-329-overview.md"
parent_id: 
anchor: "TD-329"
checksum: "sha256:442711fcdeee828daae7db3696b996c5b6b18c477d23e1d97226d30117e93e96"
last_modified: "2025-11-06T20:40:46Z"
doc_kind: "TD"
h_level: 2
---
<a id="TD-329"></a>
## **1.17.H Rendering strategy & caching (ISR/SSR + CDN)**

- **People/Studios pages**: ISR with *revalidate: 86400* (24h) on low‑change fields; **on‑demand revalidation** when profile edits publish.
- **City pages**: ISR, *revalidate: 21600* (6h) at launch → 24h later.
- **Stories**: static at publish; republish on edit.
- **Edge cache**: CloudFront cache policy keyed by *Accept‑Language* and *Cookie* *only for Safe‑Mode* flag (avoid leaking modes).
- **Stale‑while‑revalidate** for instant TTFB.
- **ETag** for JSON APIs used by static props.
