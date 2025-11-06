---
id: TD-96
title: "**1.6.I Webhooks → normalized events**"
source_doc: "TechDevBlueprint.docx"
source_path: "docs\blueprints\tech\TD-96-16i-webhooks-normalized-events\TD-96-overview.md"
parent_id: 
anchor: "TD-96"
checksum: "sha256:e0a8f27e23b7fb926de2e9b11010d938815575b9dfb2394d4ee6451aa940324e"
last_modified: "2025-11-06T20:40:46Z"
doc_kind: "TD"
h_level: 2
---
<a id="TD-96"></a>
## **1.6.I Webhooks → normalized events**

- idv.started\|passed\|failed\|expired
- bg.invited\|in_progress\|clear\|consider\|suspended\|disputed\|expired
- social.connected\|verified\|revoked
- *risk.score.updated*  
  Each event includes *user_id*, provider_ref, and relevant timestamps.

**Idempotency:** dedupe by *(provider, provider_event_id)*; keep last processed id per provider.
