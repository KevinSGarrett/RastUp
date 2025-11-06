---
id: TD-324
title: "**1.17.C Metadata & canonicalization**"
source_doc: "TechDevBlueprint.docx"
source_path: "docs\blueprints\tech\TD-324-117c-metadata-canonicalization\TD-324-overview.md"
parent_id: 
anchor: "TD-324"
checksum: "sha256:14aa1234563a7528a3d52540b8cb8d60691abe27c25d0a86e8eca68950cb745e"
last_modified: "2025-11-06T20:40:46Z"
doc_kind: "TD"
h_level: 2
---
<a id="TD-324"></a>
## **1.17.C Metadata & canonicalization**

- **Required** ***\<head\>*** **tags per page:**

  - *\<title\>* unique, ≤60 chars; *\<meta name="description"\>* ≤160 chars.
  - \<link rel="canonical" href="…"\>
  - OpenGraph (*og:title*, *og:description*, *og:image* SFW, *og:url*, *og:type*)
  - Twitter Card (*summary_large_image*)
  - Preconnect only to first‑party + Stripe (at checkout), never to ad CDNs.

- **Tracking query params** (*utm\_\**, *ref*) are stripped by a Next.js middleware and 301 to canonical (no duplicate content).

- **Case studies** use Article OG tags (*article:published_time*, *article:tag*).
