---
id: TD-213
title: "**1.13.D Bronze → Silver → Gold modeling**"
source_doc: "TechDevBlueprint.docx"
source_path: "docs\blueprints\tech\TD-213-113d-bronze-silver-gold-modeling\TD-213-overview.md"
parent_id: 
anchor: "TD-213"
checksum: "sha256:c1174d0fd5a098c921ecf516f7e7da1078e6a70ec7f1cf4e87ee3882864834fc"
last_modified: "2025-11-06T20:40:46Z"
doc_kind: "TD"
h_level: 2
---
<a id="TD-213"></a>
## **1.13.D Bronze → Silver → Gold modeling**

**Bronze (raw):**  
*s3://data/bronze/events/dt=YYYY‑MM‑DD/hour=HH/\*.json*

- Append‑only; immutable.
- Glue Catalog table *bronze_events* with partitions (*dt*, *hour*).

**Silver (typed/curated):** primary tables

- *fact_search_impressions*, *fact_search_clicks* (joinable via *impression_id*).
- *fact_booking_legs* (one row per leg status change with snapshots).
- *fact_payments*, *fact_refunds*, *fact_payouts*, *fact_disputes*.
- *fact_promotions_events* (impressions/clicks/invalids), *fact_promotions_spend*.
- *fact_messages*, *fact_action_cards*, *fact_notifications*.
- *fact_docs*, *fact_idv_bg*, *fact_reviews*.
- **Dimensions**: *dim_user_public* (no PII), *dim_service_profile*, *dim_studio*, *dim_city*, *dim_device*, *dim_campaign*.

**Gold (marts/KPIs):**

- **Marketplace**: *kpi_gmv_daily*, *kpi_take_rate*, *kpi_conversion_funnel* (search→profile→checkout→confirm), *kpi_cancellations*, *kpi_refunds*, *kpi_disputes*.
- **Supply**: *kpi_seller_activation*, *kpi_studio_verification_rate*, *kpi_acceptance_window_hist*.
- **Trust**: *kpi_idv_pass_rate*, *kpi_bg_clear_rate*, *kpi_risk_buckets*.
- **Promotions**: *kpi_promo_ctr*, *kpi_invalid_rate*, *kpi_spend_vs_budget*.
- **Comms**: *kpi_delivery*, *kpi_bounce*, *kpi_complaint*, *kpi_open_click* (non‑sensitive).
- **SRE**: *kpi_api_latency_p95*, *kpi_error_rates*, *kpi_waf_blocks*.

**Build strategy**

- Glue/CTAS jobs materialize Silver to Parquet partitioned by *dt* (and sometimes *city*).
- Gold uses **dbt models** (on Athena) with tests (unique keys, not null, referential integrity), incremental by *dt*.
