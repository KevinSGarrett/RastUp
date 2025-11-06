---
id: TD-322
title: "**1.17.A Canon & invariants**"
source_doc: "TechDevBlueprint.docx"
source_path: "docs\blueprints\tech\TD-322-117a-canon-invariants\TD-322-overview.md"
parent_id: 
anchor: "TD-322"
checksum: "sha256:fd28639b8ca5382ee61641fc0b4fdfa527ab1010827845603ee50d3a36594d5c"
last_modified: "2025-11-06T20:40:46Z"
doc_kind: "TD"
h_level: 2
---
<a id="TD-322"></a>
## **1.17.A Canon & invariants**

1763. **SFW on the open web.** Public pages show *SFW previews only*. Age‑gated/18+ content never leaves the app; no email with 18+ previews.
1764. **Single canonical per concept.** Every profile, studio, case study, and city page has one canonical URL; alternates (share/UTM/tracking) 301 to the canonical.
1765. **Server‑rendered entry, cached at the edge.** We use Next.js **ISR/SSR** with CloudFront caching and smart revalidation (low cost).
1766. **Robots are guests, not owners.** We invite indexing of SFW listings and guides; we set *noindex* on anything gated, duplicated, or ephemeral (drafts, filters, session pages).
1767. **Accessibility improves SEO.** Headings, landmarks, alt text, and readable copy are mandatory—no image‑only text.
