---
id: TD-401
title: "**1.19.13 Performance & bundle budgets for i18n**"
source_doc: "TechDevBlueprint.docx"
source_path: "docs\blueprints\tech\TD-401-11913-performance-bundle-budgets-for-i18n\TD-401-overview.md"
parent_id: 
anchor: "TD-401"
checksum: "sha256:29765f7f2155a84690def1acf1f2acae870be20bf3f0f91743f9ee252310b1e2"
last_modified: "2025-11-06T20:40:46Z"
doc_kind: "TD"
h_level: 2
---
<a id="TD-401"></a>
## **1.19.13 Performance & bundle budgets for i18n**

- **Do not** ship all catalogs to every user: load on demand from CDN.
- Tree‑shake i18n runtime; rely on browser *Intl*; **Node with full‑icu** in SSR.
- Pre‑render top locales for city/role pages to hit SEO.

**Bundle budget (public pages)**  
**Recommended path:** *observability/budgets/i18n-budget.json*

*{ "resourceSizes":\[{"resourceType":"script","budget":150},{"resourceType":"total","budget":850}\] }*
