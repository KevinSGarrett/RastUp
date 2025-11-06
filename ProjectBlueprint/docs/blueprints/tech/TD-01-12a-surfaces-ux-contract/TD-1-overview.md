---
id: TD-1
title: "**1.2.A Surfaces & UX contract**"
source_doc: "TechDevBlueprint.docx"
source_path: "docs\blueprints\tech\TD-01-12a-surfaces-ux-contract\TD-1-overview.md"
parent_id: 
anchor: "TD-1"
checksum: "sha256:2dc2cfce129e1de9df522bd2cfcc7d536bf84211654a2c77da33ed374c4d8ca2"
last_modified: "2025-11-06T20:40:46Z"
doc_kind: "TD"
h_level: 2
---
<a id="TD-1"></a>
## **1.2.A Surfaces & UX contract**

**Where search appears**

47. **Search home** (role picker + location field + date and budget quick filters).
48. **Role‑scoped search** (tabs): *Models*, *Photographers*, *Videographers*, *Creators*.
49. **Studios search** (separate surface; can be “attached in flow” during checkout).
50. **Saved searches & alerts** (optional for MVP; schema below).
51. **Admin**: Reindex, synonyms, density caps, city gates, invalid‑click dashboard.

**Non‑negotiable behaviors**

- Clicking a search card **always** deep‑links to the **role canonical page** (*/u/{handle}/{role}*) or **studio page** (*/studio/{slug}*), never the account shell alone.
- Safe‑Mode ON by default for guests; public thumbnails follow NSFW rules.
- **Studios are listings (places)**; role results never mix studio ratings or badges.
- Social metrics appear *only when verified*; otherwise show “Unverified”.
