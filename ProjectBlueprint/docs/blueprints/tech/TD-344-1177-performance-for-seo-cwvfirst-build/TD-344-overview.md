---
id: TD-344
title: "**1.17.7 Performance for SEO (CWV‑first Build)**"
source_doc: "TechDevBlueprint.docx"
source_path: "docs\blueprints\tech\TD-344-1177-performance-for-seo-cwvfirst-build\TD-344-overview.md"
parent_id: 
anchor: "TD-344"
checksum: "sha256:f7e42cfbd58c807ecf1be44644bf010f2682789b2f9b71d6def20cd88adcd4b5"
last_modified: "2025-11-06T20:40:46Z"
doc_kind: "TD"
h_level: 2
---
<a id="TD-344"></a>
## **1.17.7 Performance for SEO (CWV‑first Build)**

**Budgets (mobile P75):** LCP ≤ 2.5s, CLS ≤ 0.10, INP ≤ 200ms, TTFB ≤ 800ms.

**Tactics**

- Pick an **LCP element** (hero image) per template; preload it with *as=image* and *fetchpriority="high"*.
- Inline **critical CSS**; defer the rest; no blocking fonts (local WOFF2 + *font-display: swap*).
- **Code‑split** heavy widgets; ship minimal JS on public pages.
- Preconnect only to **our CDN** and **Stripe** (checkout only).
- Serve **stale‑while‑revalidate** via ISR + CloudFront.
- Use **first‑party analytics** via *sendBeacon* (no third‑party bloat).

**Artifact — Lighthouse CI budget**  
*Recommended path:* *observability/budgets/lighthouse.json*

*{*  
*"resourceSizes": \[*  
*{"resourceType":"total", "budget": 900},*  
*{"resourceType":"script", "budget": 160}*  
*\],*  
*"timings": \[*  
*{"metric": "interactive", "budget": 3500},*  
*{"metric": "first-contentful-paint", "budget": 1800}*  
*\]*  
*}*
