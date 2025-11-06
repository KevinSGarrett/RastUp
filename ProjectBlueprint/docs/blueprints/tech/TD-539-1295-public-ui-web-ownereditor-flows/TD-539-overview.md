---
id: TD-539
title: "**1.29.5 Public UI (web) & owner/editor flows**"
source_doc: "TechDevBlueprint.docx"
source_path: "docs\blueprints\tech\TD-539-1295-public-ui-web-ownereditor-flows\TD-539-overview.md"
parent_id: 
anchor: "TD-539"
checksum: "sha256:5f6c693d80d7f36d87e352fa18b984f086398618ff7a92590895be832b574e20"
last_modified: "2025-11-06T20:40:46Z"
doc_kind: "TD"
h_level: 2
---
<a id="TD-539"></a>
## **1.29.5 Public UI (web) & owner/editor flows**

**Profile → Portfolio tab (public):**

- Grid (masonry) of **Portfolio Items**; hover shows title, city, genres; Safe‑Mode ensures **SFW only** on public surfaces.

NonTechBlueprint

- Case‑study page (optional route */p/{handle}/work/{slug}*) with hero media, story, deliverables, “**Request a similar shoot**” CTA, collaborators row (only **approved** chips click to profiles), and “**Studio used**” chip linking to the studio page.

NonTechBlueprint

**Owner editor (dashboard):**

- Sections: **Portfolio** (media upload, order, cover pick), **Case Study** (story/results/deliverables), **Collaborators** (invite → pending → approve/decline UI), **Studio used** (search/link). These tools are called out in the non‑technical owner editor scope.

NonTechBlueprint

**Boards (public/private):**

- From any People/Studio/Portfolio card: **Add to Board** → picker (create new or choose existing); fires *board.add* telemetry.

NonTechBlueprint

- Board page lists items (mixed types) with notes; can be **private** (default), **unlisted** (share link), or **public** (SEO‑light; SFW only).

**“Request a similar shoot”**

- On case‑study pages and Board pages, a CTA opens a **pre‑filled RFP** (city, genres, budget band from case study). On submit, it creates an inquiry thread to the owner (or a marketplace RFP if configured).
