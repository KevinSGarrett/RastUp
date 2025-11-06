---
id: TD-392
title: "**1.19.4 Locale detection & routing (no auto‑redirect loop)**"
source_doc: "TechDevBlueprint.docx"
source_path: "docs\blueprints\tech\TD-392-1194-locale-detection-routing-no-autoredirect-loop\TD-392-overview.md"
parent_id: 
anchor: "TD-392"
checksum: "sha256:632c4ae4625ecab427b8980266711b4bdc2c82640646a7f3e9e2fc20249e4d97"
last_modified: "2025-11-06T20:40:46Z"
doc_kind: "TD"
h_level: 2
---
<a id="TD-392"></a>
## **1.19.4 Locale detection & routing (no auto‑redirect loop)**

**Middleware (concept)**  
**Recommended path:** *web/middleware.locale.ts*

*import { NextRequest, NextResponse } from "next/server";*  
*import Negotiator from "negotiator";*  
*const SUPPORTED = \["en-US","es-ES","fr-FR","ar","de-DE"\];*  
  
*export function middleware(req: NextRequest) {*  
*const res = NextResponse.next();*  
*// Honor explicit choice in cookie first*  
*const chosen = req.cookies.get("locale")?.value;*  
*const lang = chosen \|\| new Negotiator({ headers: { "accept-language": req.headers.get("accept-language") \|\| "" } }).language(SUPPORTED) \|\| "en-US";*  
*res.headers.set("x-lang", lang);*  
*res.headers.set("x-dir", lang.startsWith("ar") ? "rtl" : "ltr");*  
*return res;*  
*}*  

**UX:** always offer a visible language switcher; **do not** force redirects based on IP.
