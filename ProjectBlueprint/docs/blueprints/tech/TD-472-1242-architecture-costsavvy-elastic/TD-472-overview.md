---
id: TD-472
title: "**1.24.2 Architecture (cost‑savvy, elastic)**"
source_doc: "TechDevBlueprint.docx"
source_path: "docs\blueprints\tech\TD-472-1242-architecture-costsavvy-elastic\TD-472-overview.md"
parent_id: 
anchor: "TD-472"
checksum: "sha256:176866eaf3a81012a8b7cb226b6920999a1bf2f02e5fa85f18f838036973409d"
last_modified: "2025-11-06T20:40:46Z"
doc_kind: "TD"
h_level: 2
---
<a id="TD-472"></a>
## **1.24.2 Architecture (cost‑savvy, elastic)**

- **Frontend (web + RN):** Next.js + Amplify Gen 2 (SSR for listing pages for SEO), React Native screens for mobile booking & host ops.
- **API layer:** AppSync GraphQL.
- **Canonical data store:** **Aurora PostgreSQL** for listings, rules, pricing tiers, schedules, and reviews (we need rich filtering/sorting and transactional edits).
- **Search:** **Typesense** index (title, neighborhood, amenity facets, price ranges, availability summaries, rating).
- **Media:** S3 + CloudFront; image transforms via Lambda (thumbs), with guidelines for minimum gallery set.

NonTechBlueprint

- **Availability & booking:** use the same booking/order pipeline defined in §1.12/§1.13 and payments in §1.22; widget emits a **space‑line item** with min‑hours and fee components.
- **Docs:** Smart Docs service (Property/Space Release, House Rules) injected at checkout and stored with the order.

NonTechBlueprint

- **Deposit holds:** Stripe authorization only, as labeled in the widget; captured only if a post‑booking violation is logged.

NonTechBlueprint

- **Location:** AWS Location Service for geocoding + approximate map render; precise address gated to post‑booking.

NonTechBlueprint

- **Calendars:** ICS export for host calendars; inbound full two‑way sync is Phase 2 (optional).

NonTechBlueprint
