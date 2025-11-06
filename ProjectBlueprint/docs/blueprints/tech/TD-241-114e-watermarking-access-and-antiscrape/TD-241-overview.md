---
id: TD-241
title: "**1.14.E Watermarking, access, and anti‑scrape**"
source_doc: "TechDevBlueprint.docx"
source_path: "docs\blueprints\tech\TD-241-114e-watermarking-access-and-antiscrape\TD-241-overview.md"
parent_id: 
anchor: "TD-241"
checksum: "sha256:460b58d6ac362d1ec87f128a35ff4740d296082d3e8472f2443ace8ed92111ca"
last_modified: "2025-11-06T20:40:46Z"
doc_kind: "TD"
h_level: 2
---
<a id="TD-241"></a>
## **1.14.E Watermarking, access, and anti‑scrape**

- Previews:

  - Images: server watermark (creator handle + order id) diagonally; max 1600 px; JPEG/WebP.
  - Video snippets: 10–20 s HLS preview; burned watermark.
  - NSFW banding: if *nsfw_band=1*, blur until hovered & age‑gate OK; *=2* blocked on public.

- Finals (external manifests):

  - Manifest includes per‑file SHA‑256, filename, size, URL, optional watermark seed.
  - If using cloud providers that support transforms (e.g., Cloudflare R2/Stream), creators can host DRM; we just store references and checksums.

- Access control:

  - Entitlement check before revealing **final manifest URLs** (fetched on demand and short‑lived).
  - Per‑request signed redirects; **tokenized** fragment in querystring that expires.

- Rate limits & anti‑abuse:

  - Per‑user/view throttles; hotlink protection via CF **signed cookies** if we proxy some assets.
  - Download logs linked to user id for evidence in disputes.
