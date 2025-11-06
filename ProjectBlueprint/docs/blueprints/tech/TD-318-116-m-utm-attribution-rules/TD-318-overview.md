---
id: TD-318
title: "**1.16-M. UTM & Attribution Rules**"
source_doc: "TechDevBlueprint.docx"
source_path: "docs\blueprints\tech\TD-318-116-m-utm-attribution-rules\TD-318-overview.md"
parent_id: 
anchor: "TD-318"
checksum: "sha256:099c55eb97cea8845065cc8574d303a1dc5b803a3504a226524e6dd79bd6093d"
last_modified: "2025-11-06T20:40:46Z"
doc_kind: "TD"
h_level: 2
---
<a id="TD-318"></a>
## **1.16-M. UTM & Attribution Rules**

**Recommended filename/path:** *growth/utm_attribution_rules.md*

*UTM structure*  
*utm_source = one of: lib (link-in-bio), sharecard, digest, alert*  
*utm_medium = email \| inapp \| web*  
*utm_campaign = pkg \| avail \| city_digest \| book_again_7 \| book_again_30 \| book_again_90 \| referral*  
  
*Click tokens*  
*token = HMAC(k, user_id \| ts \| target) \# 5-minute TTL*  
*Store click event -\> attribute conversion to last non-expired click within 7 days.*  
  
*Attribution in §1.13*  
* - fact_clicks (Silver) join to fact_conversions (checkout.confirmed) by user_id within window.*  
* - Gold KPI: by (utm_source, utm_campaign), city, role.*
