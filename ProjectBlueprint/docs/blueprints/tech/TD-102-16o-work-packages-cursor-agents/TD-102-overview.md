---
id: TD-102
title: "**1.6.O Work packages (Cursor agents)**"
source_doc: "TechDevBlueprint.docx"
source_path: "docs\blueprints\tech\TD-102-16o-work-packages-cursor-agents\TD-102-overview.md"
parent_id: 
anchor: "TD-102"
checksum: "sha256:077aefec8d689ce340468c2b026a81341b6abebdde6ac2ce90a08027b422b109"
last_modified: "2025-11-06T20:40:46Z"
doc_kind: "TD"
h_level: 2
---
<a id="TD-102"></a>
## **1.6.O Work packages (Cursor agents)**

- **Agent C — Trust Integrations**  
  WP-TRUST-IDV-01: Provider adapter (Persona or Stripe Identity) + webhooks + HMAC + normalized events.  
  WP-TRUST-BG-01: FCRA BG adapter (Checkr) + invite/status + adverse-action scaffolding.  
  WP-TRUST-SOC-01: OAuth connections for IG/TT/YT/X; nightly snapshot job.
- **Agent B — Domain/API**  
  WP-API-TRUST-01: GraphQL resolvers for *startIdv*, *startBackgroundCheck*, *trustStatus*; trust cache.  
  WP-RISK-01: Risk rollups & score compute jobs; throttles integration.
- **Agent A — Web**  
  WP-WEB-TRUST-01: Trust center UI (badges, flows, status); IDV/BG wizards; social connect pages.  
  WP-WEB-IB-01: Wire Instant Book gate; age gate for Fan-sub surfaces.
- **Agent D — Admin & QA**  
  WP-ADM-TRUST-01: Trust dashboard, IDV review queue, BG adverse-action tools, overrides with dual approval.  
  WP-QA-TRUST-01: Full test matrix above; webhooks idempotency; privacy audits.
