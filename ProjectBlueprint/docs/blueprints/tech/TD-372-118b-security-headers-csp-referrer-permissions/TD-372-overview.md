---
id: TD-372
title: "**1.18.B Security Headers (CSP, Referrer, Permissions)**"
source_doc: "TechDevBlueprint.docx"
source_path: "docs\blueprints\tech\TD-372-118b-security-headers-csp-referrer-permissions\TD-372-overview.md"
parent_id: 
anchor: "TD-372"
checksum: "sha256:7567dc05226c87b363ae8609e62b5ee30eb3a2775681f5483e790c472265eae2"
last_modified: "2025-11-06T20:40:46Z"
doc_kind: "TD"
h_level: 2
---
<a id="TD-372"></a>
## **1.18.B Security Headers (CSP, Referrer, Permissions)**

**Recommended path:** *security/headers/response-headers.json*

*{*  
*"Content-Security-Policy": "default-src 'self'; img-src 'self'* [*https://cdn.rastup.com*](https://cdn.rastup.com) *data:; media-src 'self'* [*https://cdn.rastup.com*](https://cdn.rastup.com)*; script-src 'self'; style-src 'self' 'unsafe-inline'; font-src 'self' data:; connect-src 'self'* [*https://api.rastup.com*](https://api.rastup.com)*; frame-ancestors 'none'; base-uri 'self'; form-action 'self'",*  
*"Referrer-Policy": "strict-origin-when-cross-origin",*  
*"Permissions-Policy": "camera=(), microphone=(), geolocation=()",*  
*"Strict-Transport-Security": "max-age=63072000; includeSubDomains; preload",*  
*"X-Content-Type-Options": "nosniff",*  
*"X-Frame-Options": "DENY",*  
*"X-XSS-Protection": "0"*  
*}*  

Apply via **CloudFront Response Headers Policy**; for checkout pages add Stripe to *connect-src*/*frame-src*.
