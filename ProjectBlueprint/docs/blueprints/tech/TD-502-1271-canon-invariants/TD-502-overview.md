---
id: TD-502
title: "**1.27.1 Canon & invariants**"
source_doc: "TechDevBlueprint.docx"
source_path: "docs\blueprints\tech\TD-502-1271-canon-invariants\TD-502-overview.md"
parent_id: 
anchor: "TD-502"
checksum: "sha256:259bdaec29e37e1f846b9d6386d5f5bf883147bcd743f69349a5e2e0b9135949"
last_modified: "2025-11-06T20:40:46Z"
doc_kind: "TD"
h_level: 2
---
<a id="TD-502"></a>
## **1.27.1 Canon & invariants**

2445. **SFW‑only indexing.** Public pages (profiles, studios, city pages) must render SFW previews and **noindex** any page that would expose 18+ content or paid assets. Safe‑Mode OFF areas are never indexed.
2446. **Stable URLs & canonical rules.** We allow a small, controlled set of query params to be indexed; everything else is **canonicalized** to a base URL to avoid duplicate content and crawl traps.
2447. **SSR/ISR.** City & directory pages use **Next.js SSR + Incremental Static Regeneration (ISR)** for speed and freshness; profiles/studios use SSR with short revalidation.
2448. **Lightweight structured data.** We publish JSON‑LD for **Person** (People profiles), **Place** (Studios), and **BreadcrumbList** on directories; never include exact addresses on public Studio pages (privacy).
2449. **Crawl budget control.** We pre‑render and surface only “thin‑spine” pages (Cities × Roles/Genres), not combinatorial facets.
2450. **Performance first.** Core Web Vitals (CWV) budgets are enforced at build and runtime (LCP, INP, CLS).
