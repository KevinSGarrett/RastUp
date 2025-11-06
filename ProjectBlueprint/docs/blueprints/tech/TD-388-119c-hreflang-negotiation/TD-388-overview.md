---
id: TD-388
title: "**1.19.C Hreflang & negotiation**"
source_doc: "TechDevBlueprint.docx"
source_path: "docs\blueprints\tech\TD-388-119c-hreflang-negotiation\TD-388-overview.md"
parent_id: 
anchor: "TD-388"
checksum: "sha256:5ba23ac8985ad385a5e5cbad0175369c5b2692b7a4d49c8023bb188bf7859c96"
last_modified: "2025-11-06T20:40:46Z"
doc_kind: "TD"
h_level: 2
---
<a id="TD-388"></a>
## **1.19.C Hreflang & negotiation**

**Recommended path:** *web/lib/hreflang.ts* (complements §1.17)

*export const locales = \["en-US","es-ES","fr-FR","ar","de-DE"\];*  
*export function linksFor(canonical: string, map: Record\<string,string\>) {*  
*return Object.entries(map).map((\[lang, href\]) =\> \`\<link rel="alternate" hreflang="\${lang}" href="\${href}"\>\`).join("\n")*  
* + \`\n\<link rel="alternate" hreflang="x-default" href="\${canonical}"\>\`;*  
*}*  

# **§1.19 — Internationalization (I18n), Localization (L10n) & Accessibility (A11y) — Full Spec**

**Goal:** Ship a multilingual, accessible marketplace that preserves SEO, Safe‑Mode rules, and performance budgets. Everything below is **text‑only** for your Word doc and includes **Recommended filename/path** tags for later lift into the repo. We keep costs low (no heavy SaaS): JSON catalogs in S3, *Intl.\** APIs server/client, and automated extraction/QA.
