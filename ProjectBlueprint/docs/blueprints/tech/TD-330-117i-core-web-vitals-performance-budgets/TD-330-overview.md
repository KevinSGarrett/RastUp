---
id: TD-330
title: "**1.17.I Core Web Vitals & performance budgets**"
source_doc: "TechDevBlueprint.docx"
source_path: "docs\blueprints\tech\TD-330-117i-core-web-vitals-performance-budgets\TD-330-overview.md"
parent_id: 
anchor: "TD-330"
checksum: "sha256:b8174ec4acd2f6b0d3bc1a589a941047c7d8e9b5edbde9c95da0e956c186730f"
last_modified: "2025-11-06T20:40:46Z"
doc_kind: "TD"
h_level: 2
---
<a id="TD-330"></a>
## **1.17.I Core Web Vitals & performance budgets**

**Targets (P75 on mobile):**

- **LCP ≤ 2.5s**, **CLS ≤ 0.10**, **INP ≤ 200ms**, **TTFB ≤ 800ms**.

**Levers:**

- Use Next/Image for responsive SFW previews; WebP/AVIF; lazy + priority on hero.
- Inline **critical CSS** for above‑the‑fold; remove unused CSS via CSS‑in‑JS extraction.
- Code‑split heavy modules (editor, charts) behind dynamic import.
- Preconnect to our CDN and Stripe (checkout pages only).
- Ship system fonts or 1 local WOFF2 with *font-display: swap*.
- Avoid blocking analytics; send beacons via *navigator.sendBeacon* to our */collect* endpoint.
- Only 1 external script allowed on public pages: the consented analytics shim (first‑party). No ad trackers.

**Lighthouse CI budget (inline)**  
**Recommended path:** *observability/budgets/lighthouse-budget.json*

*{*  
*"resourceSizes": \[*  
*{"resourceType": "script", "budget": 160},*  
*{"resourceType": "total", "budget": 900}*  
*\],*  
*"resourceCounts": \[*  
*{"resourceType": "third-party", "budget": 2},*  
*{"resourceType": "total", "budget": 90}*  
*\],*  
*"timings": \[*  
*{"metric": "interactive", "budget": 3500},*  
*{"metric": "first-contentful-paint", "budget": 1800}*  
*\]*  
*}*
