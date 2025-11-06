---
id: TD-328
title: "**1.17.G Hreflang & locale routing**"
source_doc: "TechDevBlueprint.docx"
source_path: "docs\blueprints\tech\TD-328-117g-hreflang-locale-routing\TD-328-overview.md"
parent_id: 
anchor: "TD-328"
checksum: "sha256:6fbec4dee572ce68cbafc7a255ad931f9614e6bfdd84497dc3e7ea6c26494837"
last_modified: "2025-11-06T20:40:46Z"
doc_kind: "TD"
h_level: 2
---
<a id="TD-328"></a>
## **1.17.G Hreflang & locale routing**

- Default locale *en-US*. Add hreflang alternates when we add translations:

  - *\<link rel="alternate" hreflang="en" href="…"\>*, *\<link rel="alternate" hreflang="es" href="…"\>*, plus *x-default*.

- URL policy: keep canonical paths without locale prefix; inject *hreflang* only (simplifies link sharing).

- Next.js middleware detects *Accept‑Language*, sets *lang* and *dir* on *\<html\>*, and formats dates/currency per locale.

**Snippet (Next.js, concept)**  
**Recommended path:** *web/middleware.ts* *(doc block)*

*export function middleware(req: NextRequest) {*  
*const locale = negotiateLocale(req.headers.get('accept-language'));*  
*const res = NextResponse.next();*  
*res.headers.set('x-lang', locale.lang);*  
*res.headers.set('x-dir', locale.dir); // ltr/rtl*  
*return res;*  
*}*
