---
id: TD-321
title: "**1.16-P. Cost & SLO Guardrails (growth jobs)**"
source_doc: "TechDevBlueprint.docx"
source_path: "docs\blueprints\tech\TD-321-116-p-cost-slo-guardrails-growth-jobs\TD-321-overview.md"
parent_id: 
anchor: "TD-321"
checksum: "sha256:d6b3f009ccf0888ccf157267e4e1394717ea7b049d2ddca3dfc9e9b1898ff307"
last_modified: "2025-11-06T20:40:46Z"
doc_kind: "TD"
h_level: 2
---
<a id="TD-321"></a>
## **1.16-P. Cost & SLO Guardrails (growth jobs)**

**Recommended filename/path:** *observability/slo/growth-jobs.md*

*SLOs*  
* - Saved-search alert job completes \< 10 min p95; per-user dedupe strictly 1/day/search.*  
* - Weekly digest job \< 20 min p95 per city cohort.*  
* - Book-again jobs \< 5 min p95 each run.*  
  
*Alarms*  
* - SES bounce/complaint spikes \> 0.3% rolling 24h -\> pause digest/alerts, in-app only.*  
* - Lambda errors \> 1% or duration p95 \> SLO -\> investigate search query shapes or batch sizes.*  
* - Dynamo TTL dead-letter \> 100/day -\> inspect dedupe miswrites.*  
  
*Cost*  
* - Prefer in-app notifications when SES threshold near daily cap.*  
* - Batch Typesense/OpenSearch queries for alerts by grouping identical filters.*

# **§1.17 — SEO, Web Performance & Content Discovery**

*(URL topology · metadata & canonicalization · JSON‑LD · robots/noindex & Safe‑Mode · sitemaps · hreflang · ISR/SSR caching · Core Web Vitals budgets · a11y synergy · admin content ops · telemetry · tests · cost)*

**Purpose.** Make the marketplace discoverable while keeping costs down and content safe. This section defines *exactly* how we structure URLs, metadata, structured data, crawlers access, internationalization signals, build & caching strategy, performance budgets, admin workflows, and monitoring—plus copy‑pasteable artifacts for your Word plan.
