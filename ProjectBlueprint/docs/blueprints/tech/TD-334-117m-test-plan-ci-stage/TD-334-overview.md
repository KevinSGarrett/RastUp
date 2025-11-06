---
id: TD-334
title: "**1.17.M Test plan (CI + stage)**"
source_doc: "TechDevBlueprint.docx"
source_path: "docs\blueprints\tech\TD-334-117m-test-plan-ci-stage\TD-334-overview.md"
parent_id: 
anchor: "TD-334"
checksum: "sha256:0a970966f296c9f4f1e4e3591c82f75cec2349dbc6d1d148ebc38e57e8e66dc3"
last_modified: "2025-11-06T20:40:46Z"
doc_kind: "TD"
h_level: 2
---
<a id="TD-334"></a>
## **1.17.M Test plan (CI + stage)**

1821. **Lighthouse CI** on PRs for */*, */city/{city}*, */p/{handle}*, */s/{slug}*, */stories/{slug}*; budgets enforced.
1822. **Structured data** validates (Person/Product/LocalBusiness/Article) with schema validator; image URLs SFW.
1823. **Canonical/redirects**: UTM/ref variants 301 to canonical; no duplicate indexation.
1824. **Robots/noindex**: drafts, filters, admin, checkout and DMCA pages return *x-robots-tag: noindex*.
1825. **Sitemaps**: contain only published SFW pages; child sitemaps \< 50k URLs; index lists all children.
1826. **Hreflang** (when enabled): alternates present and correct.
1827. **A11y**: axe/Pa11y suite passes; keyboard nav end‑to‑end on public pages.
1828. **Perf**: p75 CWV targets met under synthetic 3G.
