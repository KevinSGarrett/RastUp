---
id: TD-198
title: "**1.12.H API shape (AppSync)**"
source_doc: "TechDevBlueprint.docx"
source_path: "docs\blueprints\tech\TD-198-112h-api-shape-appsync\TD-198-overview.md"
parent_id: 
anchor: "TD-198"
checksum: "sha256:255b56e40fc0a04c2ab1ed7cb307be5489996396c54de89f3a6638d27b5c4f2f"
last_modified: "2025-11-06T20:40:46Z"
doc_kind: "TD"
h_level: 2
---
<a id="TD-198"></a>
## **1.12.H API shape (AppSync)**

- **Schema‑first** in repo; codegen to TS types.

- **Auth modes**: Cognito JWT (primary) + API key (dev only) + IAM (admin tools).

- **Pipeline resolvers** enforce:

  - input validation & normalization
  - rate limits (token bucket per IP/user)
  - role/age gates (e.g., Fan‑sub)

- **Subscriptions** for messaging & notifications.

**Limits**: page sizes capped; cursors opaque; error taxonomy standardized per prior sections.
