---
id: TD-188
title: "**1.11.P Test plan (CI + sandbox)**"
source_doc: "TechDevBlueprint.docx"
source_path: "docs\blueprints\tech\TD-188-111p-test-plan-ci-sandbox\TD-188-overview.md"
parent_id: 
anchor: "TD-188"
checksum: "sha256:d2789fab230b5f605d02f1c8a3ae00f3ed914122b6ab582129deb2c0b4ea9da5"
last_modified: "2025-11-06T20:40:46Z"
doc_kind: "TD"
h_level: 2
---
<a id="TD-188"></a>
## **1.11.P Test plan (CI + sandbox)**

**Onboarding & verification**

1129. Create studio with mandatory fields; cannot publish until media + house rules present.
1130. Submit verification; approve → badge appears; reject → reasons surfaced; revoke path.

**Pricing & quotes**  
3) Hourly/slot/day quotes across DOW windows; min/max duration rules; buffers enforced.  
4) Overtime quote appended via amendment flow.  
5) Tax quote correct per city; deposit auth amount surfaced but not included in GMV.

**Availability & conflicts**  
6) Blackout block; buffer conflicts on adjacent bookings; ICS feed integrity.

**Search & facets**  
7) Amenity filters; deposit required toggle; verified badge facet; ranking respects verified + rating.

**Media & safety**  
8) NSFW scan blocks unsafe previews; blur for band=1; ordering respected.

**Checkout & deposit**  
9) Attach‑in‑flow: atomic confirm (Studio+Talent) succeeds/fails together.  
10) Deposit claim flow: claim within window; capture or deny; receipts updated.

**Admin**  
11) Verification audit trail; policy editor; taxonomy updates push to search analyzer.

**Performance**  
12) Quote engine p95 \< 120 ms; search p95 unchanged with facets; media upload pipeline cost within limits.
