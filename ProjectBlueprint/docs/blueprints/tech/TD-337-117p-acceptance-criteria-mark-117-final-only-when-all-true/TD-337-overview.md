---
id: TD-337
title: "**1.17.P Acceptance criteria — mark §1.17 FINAL only when ALL true**"
source_doc: "TechDevBlueprint.docx"
source_path: "docs\blueprints\tech\TD-337-117p-acceptance-criteria-mark-117-final-only-when-all-true\TD-337-overview.md"
parent_id: 
anchor: "TD-337"
checksum: "sha256:d8c96328403890f78ebfdb1f20335d62ad40ba0dccd5f36e85bb9998c13fa90a"
last_modified: "2025-11-06T20:40:46Z"
doc_kind: "TD"
h_level: 2
---
<a id="TD-337"></a>
## **1.17.P Acceptance criteria — mark §1.17 FINAL only when ALL true**

1833. Canonical URL policy implemented; UTM/ref routes 301 correctly.
1834. JSON‑LD present on People, Packages, Studios, and Stories with SFW images only.
1835. robots/noindex enforced for drafts, gated/NSFW, filters, admin, and checkout routes.
1836. Segmented sitemaps generate & auto‑submit; include only indexable pages; refresh cadence set.
1837. Hreflang in place when we enable additional locales; default *en* with *x-default*.
1838. ISR/SSR caching + CloudFront policies deliver p75 **LCP ≤ 2.5s**, **CLS ≤ 0.10**, **INP ≤ 200ms** on top routes.
1839. a11y checks pass (axe/Pa11y) on public routes; alt text coverage ≥ 99%.
1840. Dashboards show CWV trends, crawl health, and the SEO funnel; alerts configured for regressions.
1841. Costs stay within budgets (no third‑party bloat; edge cache hit ratio ≥ 90%).

# **§1.17 — SEO & On‑Site Optimization Deep‑Dive (Expanded)**
