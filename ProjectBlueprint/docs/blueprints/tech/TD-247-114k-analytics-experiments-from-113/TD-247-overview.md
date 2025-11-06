---
id: TD-247
title: "**1.14.K Analytics & experiments (from §1.13)**"
source_doc: "TechDevBlueprint.docx"
source_path: "docs\blueprints\tech\TD-247-114k-analytics-experiments-from-113\TD-247-overview.md"
parent_id: 
anchor: "TD-247"
checksum: "sha256:e7e83dc53d118219000307140327776a62caf4b5bf296316f256ab06251fe172"
last_modified: "2025-11-06T20:40:46Z"
doc_kind: "TD"
h_level: 2
---
<a id="TD-247"></a>
## **1.14.K Analytics & experiments (from §1.13)**

- Events: *fansub.subscribe.start\|success\|fail*, *fansub.tip*, *fansub.ppv.buy*, *fansub.request.quote\|paid\|delivered\|approved\|revision*, *fansub.preview.view*, *fansub.final.view*.
- Funnels: profile → subscribe; preview → PPV buy; request quote → paid → approved.
- Guardrails: refund rate, complaint rate, moderation flags.
- Experiments: pricing A/B, preview length, watermark density, digest timing.
- NRT ops: creator earnings today, MTD, subscriber churn, request backlog, invoice failures.
