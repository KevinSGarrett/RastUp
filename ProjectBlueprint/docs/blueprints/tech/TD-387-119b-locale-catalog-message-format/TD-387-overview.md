---
id: TD-387
title: "**1.19.B Locale catalog & message format**"
source_doc: "TechDevBlueprint.docx"
source_path: "docs\blueprints\tech\TD-387-119b-locale-catalog-message-format\TD-387-overview.md"
parent_id: 
anchor: "TD-387"
checksum: "sha256:ba21ec9779339bab90d192a3f92eca5f4feb1c19f0657a7a068ab852b2e98398"
last_modified: "2025-11-06T20:40:46Z"
doc_kind: "TD"
h_level: 2
---
<a id="TD-387"></a>
## **1.19.B Locale catalog & message format**

**Recommended path:** *i18n/catalog/en-US.json* (example)

*{*  
*"nav.home": "Home",*  
*"nav.city": "{city} creatives",*  
*"profile.title": "{displayName} — {role} in {city}",*  
*"studio.amenities": "Amenities",*  
*"checkout.pay": "Pay {amount, number, ::currency/USD}",*  
*"a11y.skip": "Skip to main content"*  
*}*  

**Loader (pseudocode)**  
**Path:** *i18n/loader.ts*

*export async function loadLocale(lang: string) {*  
*const res = await fetch(\`https://cdn.rastup.com/i18n/\${lang}.json\`, { cache: 'force-cache' });*  
*return res.json();*  
*}*
