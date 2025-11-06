---
id: TD-134
title: "**1.8.N Work packages (Cursor agents)**"
source_doc: "TechDevBlueprint.docx"
source_path: "docs\blueprints\tech\TD-134-18n-work-packages-cursor-agents\TD-134-overview.md"
parent_id: 
anchor: "TD-134"
checksum: "sha256:3364489b5a93b100760c9635a6e2ea8369feb76ff030c0008f81b755355805fa"
last_modified: "2025-11-06T20:40:46Z"
doc_kind: "TD"
h_level: 2
---
<a id="TD-134"></a>
## **1.8.N Work packages (Cursor agents)**

- **Agent B — Domain/API**  
  WP-REV-01: SQL tables + GraphQL resolvers (create, edit, list, reputation).  
  WP-REV-02: Aggregation jobs (real-time & nightly full), cache invalidation.
- **Agent C — Integrity**  
  WP-REV-FRD-01: Fraud heuristics, classifiers integration, auto-hide queue.  
  WP-REV-FRD-02: Rate limiter; ring detection; report intake.
- **Agent A — Web**  
  WP-WEB-REV-01: UI components for stars, distributions, facets, highlights, replies; review composer.  
  WP-WEB-REV-02: Nudges & inbox cards; moderation states in UI.
- **Agent D — Admin & QA**  
  WP-ADM-REV-01: Moderation console, audits, appeals.  
  WP-QA-REV-01: Full test matrix automation; golden datasets for aggregation math.
