---
id: TD-546
title: "**1.29.12 Test plan**"
source_doc: "TechDevBlueprint.docx"
source_path: "docs\blueprints\tech\TD-546-12912-test-plan\TD-546-overview.md"
parent_id: 
anchor: "TD-546"
checksum: "sha256:4baa0de36bc3f3c460669b1d235aa48849c7c0516a2eee8a8a0897a90a55afce"
last_modified: "2025-11-06T20:40:46Z"
doc_kind: "TD"
h_level: 2
---
<a id="TD-546"></a>
## **1.29.12 Test plan**

2628. **Owner editor**: upload, reorder, set cover, write case‑study, publish → renders on profile.
2629. **Collaborator tags**: request → collaborator approves/declines → public chips render only on approve; decline hides.

NonTechBlueprint

2630. **Safe‑Mode**: with Safe‑Mode ON, any beyond‑allowed tier media is hidden/blurred; public page remains SFW.

NonTechBlueprint

2631. **Boards**: add/remove/reorder across mixed entities; private vs unlisted vs public behaviors; telemetry *board.add* fires.

NonTechBlueprint

2632. **Studio chip**: link on case study opens the studio page; telemetry *studio.link.click* fires.

NonTechBlueprint

2633. **Request similar shoot**: CTA pre‑fills RFP and creates thread/RFP; edge cases (missing city/budget).
2634. **DMCA**: report → Admin case created → item blocked → unblock on resolution.
2635. **SEO**: JSON‑LD validates; only SFW case‑study URLs appear in sitemaps.
2636. **Perf**: LCP/INP within budgets on portfolio and case‑study templates (ties to §1.27 CWV budgets).
