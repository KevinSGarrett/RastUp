---
id: TD-249
title: "**1.14.M Performance & cost**"
source_doc: "TechDevBlueprint.docx"
source_path: "docs\blueprints\tech\TD-249-114m-performance-cost\TD-249-overview.md"
parent_id: 
anchor: "TD-249"
checksum: "sha256:0dfec87ebd42b1d1c657e77938bc81576c70ea76b395b7ed09c299695ab0ccf5"
last_modified: "2025-11-06T20:40:46Z"
doc_kind: "TD"
h_level: 2
---
<a id="TD-249"></a>
## **1.14.M Performance & cost**

- **Storage**: previews only; lifecycle to Intelligent‑Tiering after 30 days.
- **Bandwidth**: HLS previews limited (10–20 s); CloudFront caching; signed cookies for private previews when needed.
- **Compute**: watermarking/transcode via Lambda on demand; no always‑on media servers.
- **Stripe**: use **billing thresholds** & retries for subs; dunning emails via Stripe to reduce send costs.
- **Search**: PPV/creator discovery in Typesense with lean fields (no captions in index).
