---
id: TD-393
title: "**1.19.5 Numbers, currency, dates & time zones**"
source_doc: "TechDevBlueprint.docx"
source_path: "docs\blueprints\tech\TD-393-1195-numbers-currency-dates-time-zones\TD-393-overview.md"
parent_id: 
anchor: "TD-393"
checksum: "sha256:066fbd46175da31d7e6a313daafd5222ed82a25d7e333d77342c6179cc5d53a7"
last_modified: "2025-11-06T20:40:46Z"
doc_kind: "TD"
h_level: 2
---
<a id="TD-393"></a>
## **1.19.5 Numbers, currency, dates & time zones**

**Utility**  
**Recommended path:** *i18n/format.ts*

*export function money(amountCents: number, currency: string, locale: string) {*  
*return new Intl.NumberFormat(locale, { style: "currency", currency }).format(amountCents / 100);*  
*}*  
*export function dateFmt(dtISO: string, locale: string, tz: string) {*  
*return new Intl.DateTimeFormat(locale, { dateStyle: "medium", timeStyle: "short", timeZone: tz }).format(new Date(dtISO));*  
*}*  

**Rules:**

- Always format **server‑side** for SEO pages.
- Respect *prefers_24h* and *timezone*.
- For booking availability, display both **provider local time** and **viewer time** when they differ.
