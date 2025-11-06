---
id: TD-518
title: "**1.27.17 Test plan**"
source_doc: "TechDevBlueprint.docx"
source_path: "docs\blueprints\tech\TD-518-12717-test-plan\TD-518-overview.md"
parent_id: 
anchor: "TD-518"
checksum: "sha256:f06be0aa4302ca3a96dc646ebe87ec024d299d1b49bfb80b0506ee18c69fc975"
last_modified: "2025-11-06T20:40:46Z"
doc_kind: "TD"
h_level: 2
---
<a id="TD-518"></a>
## **1.27.17 Test plan**

2495. **Indexability matrix:** verify *index,follow* on city listings, SFW profiles/studios; verify *noindex,nofollow* on any page with NSFW risks, Safe‑Mode OFF, or paid content.
2496. **Canonicals:** for facet URLs, canonical points to base; for allowed sorts/pagination, canonical preserves them; prev/next present for paginated listings.
2497. **Sitemaps:** validate XML; GSC fetch succeeds; sitemaps list only indexable URLs; updated on publish/unpublish.
2498. **JSON‑LD:** Person/Place/Breadcrumb validate in Rich Results; studios never leak exact address pre‑booking.
2499. **OG/Twitter:** correct images and titles; images update on asset change; cached at edge.
2500. **CWV:** Lighthouse CI passes budgets on templates; field beacons report within targets after deploy.
2501. **Redirects:** legacy slugs 301 to current; no redirect loops; canonical host enforced.
2502. **Error handling:** 404 returns hard 404; maintenance returns Retry‑After; robots obeys disallows.
2503. **Security:** no PII or paid asset URLs in page source; signed URLs never appear in HTML.
