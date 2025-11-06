---
id: TD-407
title: "**1.20.C PWA configuration (manifest, SW, caching, offline)**"
source_doc: "TechDevBlueprint.docx"
source_path: "docs\blueprints\tech\TD-407-120c-pwa-configuration-manifest-sw-caching-offline\TD-407-overview.md"
parent_id: 
anchor: "TD-407"
checksum: "sha256:ebd97aac92d69b955bdeff2b8f3b0439ff0f2df5bbe9f7cc931eacbd5cff114e"
last_modified: "2025-11-06T20:40:46Z"
doc_kind: "TD"
h_level: 2
---
<a id="TD-407"></a>
## **1.20.C PWA configuration (manifest, SW, caching, offline)**

**Recommended path:** *web/public/manifest.webmanifest*

*{*  
*"name": "RastUp",*  
*"short_name": "RastUp",*  
*"start_url": "/?source=pwa",*  
*"display": "standalone",*  
*"background_color": "#0e1116",*  
*"theme_color": "#0e1116",*  
*"icons": \[*  
*{"src": "/icons/icon-192.png", "sizes": "192x192", "type": "image/png"},*  
*{"src": "/icons/icon-512.png", "sizes": "512x512", "type": "image/png"}*  
*\]*  
*}*  

**Service Worker** (Workbox‑style pseudocode)  
**Recommended path:** *web/public/sw.js*

*self.addEventListener('install', e =\> {*  
*e.waitUntil(caches.open('rastup-precache-v1').then(c =\> c.addAll(\[*  
*'/', '/city', '/styles.css', '/manifest.webmanifest'*  
*\])));*  
*});*  
*self.addEventListener('fetch', e =\> {*  
*const url = new URL(e.request.url);*  
*// HTML: NetworkFirst with fallback to cache*  
*if (e.request.mode === 'navigate') {*  
*e.respondWith(fetch(e.request).then(r =\> {*  
*const copy = r.clone(); caches.open('rastup-pages').then(c =\> c.put(e.request, copy));*  
*return r;*  
*}).catch(() =\> caches.match(e.request) \|\| caches.match('/')));*  
*return;*  
*}*  
*// Images: Stale-While-Revalidate*  
*if (url.pathname.startsWith('/\_next/image') \|\| url.pathname.startsWith('/images/')) {*  
*e.respondWith(caches.open('img').then(async c =\> {*  
*const cached = await c.match(e.request);*  
*const fresh = fetch(e.request).then(r =\> { c.put(e.request, r.clone()); return r; });*  
*return cached \|\| fresh;*  
*}));*  
*}*  
*});*  

**Offline scope:** home, city pages, profile/studio detail (last viewed), messages list (last page cached), compose drafts.
