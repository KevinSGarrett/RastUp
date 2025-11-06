---
id: TD-341
title: "**1.17.4 Structured Data (JSON‑LD) — Full Coverage**"
source_doc: "TechDevBlueprint.docx"
source_path: "docs\blueprints\tech\TD-341-1174-structured-data-jsonld-full-coverage\TD-341-overview.md"
parent_id: 
anchor: "TD-341"
checksum: "sha256:47b096757d9e2d26413c0c8b41fbf30150f6830de967482139eed5ddb8570687"
last_modified: "2025-11-06T20:40:46Z"
doc_kind: "TD"
h_level: 2
---
<a id="TD-341"></a>
## **1.17.4 Structured Data (JSON‑LD) — Full Coverage**

**Entity → schema.org type map**

- **People (Service Profiles)**: *Person* + *Offer*(s) for packages; optional *AggregateRating* when policy allows.
- **Studios**: *LocalBusiness* with *amenityFeature*; optional *AggregateRating*.
- **Case Studies/Guides**: *Article*/*CreativeWork*.
- **Breadcrumbs**: *BreadcrumbList* on all public pages.
- **Search results** (optional enhancement): *ItemList* on landing pages.

**Artifacts**

**A) BreadcrumbList**  
*Recommended path:* *web/lib/ldjson/breadcrumb.ts*

*export const breadcrumbLd = (trail) =\> ({*  
*"@context": "*[*https://schema.org*](https://schema.org)*",*  
*"@type": "BreadcrumbList",*  
*"itemListElement": trail.map((item, i) =\> ({*  
*"@type": "ListItem", "position": i+1, "name": item.name, "item": item.url*  
*}))*  
*});*  

**B) Service Profile with Offers & rating**  
*Recommended path:* *web/lib/ldjson/personOffers.ts*

*export const personWithOffersLd = (p) =\> ({*  
*"@context": "*[*https://schema.org*](https://schema.org)*",*  
*"@type": "Person",*  
*"name": p.displayName,*  
*"image": p.og_image_sfw_url,*  
*"url": \`https://rastup.com/\${p.role}/\${p.slug}\`,*  
*"jobTitle": p.roleTitle,*  
*"address": {"@type":"PostalAddress","addressLocality": p.city},*  
*"makesOffer": p.packages.map(pkg =\> ({*  
*"@type":"Offer",*  
*"priceCurrency": pkg.currency,*  
*"price": (pkg.priceCents/100).toFixed(2),*  
*"url": \`https://rastup.com/\${p.role}/\${p.slug}/packages/\${pkg.slug}\`,*  
*"availability":"https://schema.org/InStock"*  
*})),*  
*...(p.ratingCount \>= 5 ? {*  
*"aggregateRating": {*  
*"@type":"AggregateRating",*  
*"ratingValue": p.rating.toFixed(1),*  
*"reviewCount": p.ratingCount*  
*}*  
*} : {})*  
*});*  

**C) Studio with amenity features**  
*(already covered earlier—kept here for completeness; ensure SFW images)*
