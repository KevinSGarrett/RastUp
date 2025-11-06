---
id: TD-189
title: "**1.11.Q Work packages (Cursor 4‑agent lanes)**"
source_doc: "TechDevBlueprint.docx"
source_path: "docs\blueprints\tech\TD-189-111q-work-packages-cursor-4agent-lanes\TD-189-overview.md"
parent_id: 
anchor: "TD-189"
checksum: "sha256:6d0dab0fc7a900078e456c9b01600d3bd8790cf285cc1e8f4031985fbaf5231a"
last_modified: "2025-11-06T20:40:46Z"
doc_kind: "TD"
h_level: 2
---
<a id="TD-189"></a>
## **1.11.Q Work packages (Cursor 4‑agent lanes)**

- **Agent B — Domain/API**  
  WP‑STD‑01: SQL migrations (*studio*, *studio_rate*, *studio_policy*, *studio_blackout*, *studio_media*, *studio_verification_audit*).  
  WP‑STD‑02: GraphQL resolvers for Studio CRUD, rates, media, blackouts, verification.  
  WP‑STD‑03: Quote engine + buffer/conflict checks; ICS feed generator.
- **Agent C — Integrations**  
  WP‑STD‑INT‑01: Media scan + transform Lambdas; NSFW + antivirus; S3 lifecycle.  
  WP‑STD‑INT‑02: Tax quoting for studio services; deposit auth via SetupIntent (already in §1.3).
- **Agent A — Web**  
  WP‑STD‑WEB‑01: Studio create/edit wizard (amenities, pricing, rules, deposit).  
  WP‑STD‑WEB‑02: Public Studio page; search facet UI; attach‑in‑flow picker in checkout.
- **Agent D — Admin & QA**  
  WP‑STD‑ADM‑01: Verification queue; policy editor; taxonomy manager; pricing inspector.  
  WP‑STD‑QA‑01: Full test matrix automation + synthetic data fixtures.
