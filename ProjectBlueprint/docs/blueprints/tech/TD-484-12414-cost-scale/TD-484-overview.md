---
id: TD-484
title: "**1.24.14 Cost & Scale**"
source_doc: "TechDevBlueprint.docx"
source_path: "docs\blueprints\tech\TD-484-12414-cost-scale\TD-484-overview.md"
parent_id: 
anchor: "TD-484"
checksum: "sha256:f405647f062502f37dc026cf0f45a864dcfae2429a464e5359847e7ea218af63"
last_modified: "2025-11-06T20:40:46Z"
doc_kind: "TD"
h_level: 2
---
<a id="TD-484"></a>
## **1.24.14 Cost & Scale**

- **Aurora Postgres** (serverless v2) autoscaling; keep read replicas off at launch; aggressive connection pooling via Data API.
- **Typesense**: shared cluster (same as §1.21) with capped fields; background reindex on publish/update.
- **S3/CloudFront** for gallery assets; image transforms cached; lifecycle to IA after 90 days.
- **Stripe** deposit holds auth‑only (no capture unless violation).
- **AppSync** on‑demand; resolvers primarily Data API + Lambda; no long‑polling jobs.
