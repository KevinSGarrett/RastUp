---
id: TD-598
title: "**1.6.2 Architecture & cost posture**"
source_doc: "TechDevBlueprint.docx"
source_path: "docs\blueprints\tech\TD-598-162-architecture-cost-posture\TD-598-overview.md"
parent_id: 
anchor: "TD-598"
checksum: "sha256:e11ca2edb68607c9eacd420c19cbcdf51ee58d2a44223d5de2a0bdb3feafe6b5"
last_modified: "2025-11-06T20:40:46Z"
doc_kind: "TD"
h_level: 2
---
<a id="TD-598"></a>
## **1.6.2 Architecture & cost posture**

**Decision (MVP):**

- **Help Center & KB**: build **in‑house** (Next.js SSR/ISR) backed by Aurora Postgres + S3 for images, with **Typesense** for search. (Keeps content on our domain, full control over SEO, and low unit cost.)
- **Ticketing**: integrate **Zendesk Support (Team plan)** for 3–5 agent seats at launch (macros, views, SLAs, automations, deflection APIs). Provide **Zammad** as a drop‑in **open‑source alternative** if we later need vendor‑free hosting; we maintain a thin adapter layer so the product APIs don’t change.

**Why this split?** Your plan needs heavy **custom context, deflection, and product deep links**; we move fast by owning the KB + widget and **renting** ticketing where it’s cheap and battle‑tested. If seat cost ever outweighs benefits, we can switch to Zammad with the same product contracts.

**Core components**

- **Frontend**: Next.js Help Center (*/help/\**), embeddable React **Support Widget**.
- **API**: AppSync GraphQL for KB, guided flows, ticket prefill, and **context capture**; Lambda resolvers for Zendesk/Zammad adapters.
- **Data**: Aurora (articles, versions, feedback), S3 (images/attachments), Typesense (KB search).
- **Email/Push**: SES for transactional, Pinpoint for digests/alerts.
- **Events**: Kinesis/SNS (*support.contact*, *ticket.created*, *sla.breach*, *kb.view*, *kb.search*) → dashboards.
