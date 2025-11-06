---
id: TD-386
title: "**1.19.A Canon & invariants**"
source_doc: "TechDevBlueprint.docx"
source_path: "docs\blueprints\tech\TD-386-119a-canon-invariants\TD-386-overview.md"
parent_id: 
anchor: "TD-386"
checksum: "sha256:f449b7e2d0618c9f24d5000f7faa9485047198e24ae3ef2ff61c2f54a6303cd8"
last_modified: "2025-11-06T20:40:46Z"
doc_kind: "TD"
h_level: 2
---
<a id="TD-386"></a>
## **1.19.A Canon & invariants**

- **Locale‑agnostic URLs** (canonical without locale; hreflang alternates in head).
- **Server‑rendered locale content** for SEO; dynamic strings pulled from versioned catalogs.
- **Currency, date, number** formats localized server‑side.
- **Right‑to‑left (RTL)** support from day one (dir=rtl).
- **Accessibility first**: WCAG 2.2 AA; keyboard‑first nav; SFW previews always carry alt text.
- **Cost**: use message catalogs + ICU; avoid heavy third‑party i18n SaaS; translations stored in S3/JSON and cached.
