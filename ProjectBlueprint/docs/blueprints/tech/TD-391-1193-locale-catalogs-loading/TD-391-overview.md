---
id: TD-391
title: "**1.19.3 Locale catalogs & loading**"
source_doc: "TechDevBlueprint.docx"
source_path: "docs\blueprints\tech\TD-391-1193-locale-catalogs-loading\TD-391-overview.md"
parent_id: 
anchor: "TD-391"
checksum: "sha256:482ceda73320560340dae83cb22423056f20e4cfdfaa60baf6182b3ac0253545"
last_modified: "2025-11-06T20:40:46Z"
doc_kind: "TD"
h_level: 2
---
<a id="TD-391"></a>
## **1.19.3 Locale catalogs & loading**

**Catalog structure (ICU MessageFormat)**  
**Recommended path:** *i18n/catalogs/en-US.json*

*{*  
*"nav.home": "Home",*  
*"nav.city": "{city} creatives",*  
*"cta.book": "Book now",*  
*"price.perHour": "{amount, number, ::currency/USD} per hour",*  
*"availability.slots": "{count, plural, one {# slot} other {# slots}} available",*  
*"a11y.skip": "Skip to main content",*  
*"safeMode.disclaimer": "Public previews are SFW. Some content requires Safe-Mode OFF and age verification."*  
*}*  

**Other locales** (create *es-ES.json*, *fr-FR.json*, *ar.json*, etc.) with identical keys; avoid string concatenation—always parametrize.

**Loader (server & client)**  
**Recommended path:** *i18n/loader.ts*

*export async function loadLocaleCatalog(lang: string) {*  
*const url = \`https://cdn.rastup.com/i18n/\${lang}.json\`;*  
*const res = await fetch(url, { cache: "force-cache" });*  
*if (!res.ok) throw new Error("CATALOG_MISSING");*  
*return res.json();*  
*}*  

**Extraction config**  
**Recommended path:** *i18n/extract.config.json*

*{*  
*"src": \["web/\*\*/\*.{ts,tsx}","apps/\*\*/\*.{ts,tsx}"\],*  
*"funcs": \["t","fmt.t","i18n.t"\],*  
*"output": "i18n/messages.pot"*  
*}*
