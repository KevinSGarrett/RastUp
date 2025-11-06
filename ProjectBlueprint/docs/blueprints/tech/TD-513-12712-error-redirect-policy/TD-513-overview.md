---
id: TD-513
title: "**1.27.12 Error & redirect policy**"
source_doc: "TechDevBlueprint.docx"
source_path: "docs\blueprints\tech\TD-513-12712-error-redirect-policy\TD-513-overview.md"
parent_id: 
anchor: "TD-513"
checksum: "sha256:9c25c8d0d87e13da9fd9748da462f3cb27f1550d8e3cad2d759bb3a15d509170"
last_modified: "2025-11-06T20:40:46Z"
doc_kind: "TD"
h_level: 2
---
<a id="TD-513"></a>
## **1.27.12 Error & redirect policy**

- **4xx:** custom 404 with search module; return *404* (not soft).

- **5xx:** friendly error page; *Retry-After* when under maintenance.

- Redirects:

  - Legacy slugs preserved via *301*; maintain a *slug_redirects* table (source → target).
  - Force canonical host (*www* vs apex) and HTTPS.
  - Trailing slashes normalized.

**Recommended path:** *web/next.config.mjs* (excerpt)

*async redirects() { return \[*  
*{ source: '/profile/:handle', destination: '/p/:handle', permanent: true },*  
*{ source: '/studio/:slug', destination: '/s/:slug', permanent: true }*  
*\];}*
