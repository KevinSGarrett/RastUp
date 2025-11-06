---
id: TD-519
title: "**1.27.18 Acceptance criteria — mark §1.27 FINAL only when ALL true**"
source_doc: "TechDevBlueprint.docx"
source_path: "docs\blueprints\tech\TD-519-12718-acceptance-criteria-mark-127-final-only-when-all-true\TD-519-overview.md"
parent_id: 
anchor: "TD-519"
checksum: "sha256:95fc610d2c326275ed0bf94206985a73335ca2a6d263e0e22b8204d8365e1bdc"
last_modified: "2025-11-06T20:40:46Z"
doc_kind: "TD"
h_level: 2
---
<a id="TD-519"></a>
## **1.27.18 Acceptance criteria — mark §1.27 FINAL only when ALL true**

2504. Robots, canonicals, and sitemaps are live; only SFW, complete pages are indexable; combinatorial facets are non‑indexable.
2505. Profiles (Person) and Studios (Place) emit valid JSON‑LD; city/role directories emit BreadcrumbList; no exact studio address is exposed.
2506. SSR/ISR strategy implemented; paginated HTML for bots; prev/next and canonical tags correct.
2507. OG/Twitter images render with correct caching; redirect rules cover legacy paths.
2508. Core Web Vitals budgets enforced (build & field); dashboards and alerts wired; GSC is clean of soft‑404 or duplicate‑content warnings.
2509. Costs remain within launch budgets; no third‑party SEO tool lock‑ins.

# **§1.28 — Admin Console, Ops & Support (Back‑Office) — Full Technical Spec**

*(RBAC & SSO · immutable audit/WORM · user/listing moderation · Trust & Safety casework (reports, DMCA, disputes) · finance ops & reconciliation · search curation tools · Smart Docs admin · CMS (help/announcements) · feature flags & risk knobs · observability & SLAs · tests · acceptance)*

**Purpose.** Provide safe, efficient operational tooling to run the marketplace—moderate users/listings, handle reports/DMCA/disputes, operate refunds/payouts, curate search, manage Smart Docs templates, publish help/announcements, tune risk/rate‑limits, and observe SLOs—while enforcing least‑privilege, case‑bound access, and immutable audit.
