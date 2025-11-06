---
id: TD-210
title: "**1.13.A Canon & invariants**"
source_doc: "TechDevBlueprint.docx"
source_path: "docs\blueprints\tech\TD-210-113a-canon-invariants\TD-210-overview.md"
parent_id: 
anchor: "TD-210"
checksum: "sha256:dc47f484284e7dd9edff2a9ae25a5652046556c16b4e95077e7fa4fd20b20fd4"
last_modified: "2025-11-06T20:40:46Z"
doc_kind: "TD"
h_level: 2
---
<a id="TD-210"></a>
## **1.13.A Canon & invariants**

1260. **Single event canon.** Every user/system action emits an immutable, versioned event to a central bus with stable keys (*user_id*, *anon_id*, *lbg_id*, *leg_id*, etc.).

1261. Bronze → Silver → Gold.

      177. **Bronze**: raw, append‑only JSON in S3 (immutable).
      178. **Silver**: curated, typed Parquet tables (facts/dimensions).
      179. **Gold**: business‑ready marts (dashboards/KPIs).

1262. **Privacy‑by‑design.** No raw PII (email/phone/images) in events or indexes. Emails/phones appear only as **stable hashes** where needed for dedupe.

1263. **Money correctness.** Finance facts derive from source‑of‑record tables in Aurora (§§1.3, 1.9) and from Stripe/tax webhooks; checks ensure sums reconcile (ties into daily close gates).

1264. **Cost‑efficient first.** S3 + Glue Catalog + **Athena** for querying; **QuickSight SPICE** or **Metabase** for BI; optional **Redshift Serverless** only when we outgrow Athena latency.

1265. **Experimentation guardrails.** Sticky bucketing, exposure logging, predefined guardrails (refund/complaint ceilings), and sequential/CUPED‑ready metrics.
