---
id: TD-389
title: "**1.19.1 Canon & invariants**"
source_doc: "TechDevBlueprint.docx"
source_path: "docs\blueprints\tech\TD-389-1191-canon-invariants\TD-389-overview.md"
parent_id: 
anchor: "TD-389"
checksum: "sha256:96ddf02c5c8a18996bf7a5121642d0ff07cfa70b0f37ec7101cfbcb503a94676"
last_modified: "2025-11-06T20:40:46Z"
doc_kind: "TD"
h_level: 2
---
<a id="TD-389"></a>
## **1.19.1 Canon & invariants**

2005. **Locale‑agnostic canonicals.** Canonical URLs **don’t** contain locale; we add *hreflang* alternates (ties to §1.17).
2006. **Server‑rendered locale content** for public/SEO pages; client hydration matches server strings.
2007. **ICU MessageFormat** everywhere (plural, select, number/currency, dates).
2008. **RTL** supported from day one (Arabic/Hebrew): directional CSS, logical properties, bidi‑safe UI.
2009. **WCAG 2.2 AA**: keyboard, contrast, focus, forms, motion.
2010. **Cost**: catalogs in S3 (versioned), CDN‑cached; no per‑string paid APIs.
2011. **Safe‑Mode** rules: no 18+ previews in public pages/emails; localized strings **must not** bypass gating.
