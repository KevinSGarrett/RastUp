---
id: TD-342
title: "**1.17.5 Content Templates & On‑Page Optimization**"
source_doc: "TechDevBlueprint.docx"
source_path: "docs\blueprints\tech\TD-342-1175-content-templates-onpage-optimization\TD-342-overview.md"
parent_id: 
anchor: "TD-342"
checksum: "sha256:86fb383cb1dafd05434f8cd5499cf9caf5aa16be10e4674a8bf00b89fa4a0305"
last_modified: "2025-11-06T20:40:46Z"
doc_kind: "TD"
h_level: 2
---
<a id="TD-342"></a>
## **1.17.5 Content Templates & On‑Page Optimization**

**Title & Description formulas**  
*Recommended path:* *web/seo/title-desc-formulas.md*

*Service Profile (People):*  
*\<title\> {DisplayName} — {RoleTitle} in {City} \| RastUp \</title\>*  
*\<meta name="description" content="{Short role tagline}. Packages, availability, reviews, and verified badges." /\>*  
  
*Studio:*  
*\<title\> {StudioName} — {City} Studio Rental (Amenities & Rates) \| RastUp \</title\>*  
*\<meta name="description" content="{Short studio pitch}. Amenities: {Top 3}. From {Price}/hr." /\>*  
  
*City/Role landing:*  
*\<title\> {RolePlural} in {City} — Verified & Bookable \| RastUp \</title\>*  
*\<meta name="description" content="Explore {City} {rolePlural}. Verified portfolios, packages, and studios." /\>*  

**Heading & module order (to reduce CLS + maximize relevance)**  
*Recommended path:* *web/seo/page-templates.md*

*Service Profile:*  
*H1: {DisplayName} — {RoleTitle} in {City}*  
*Intro block (50–80 words, SFW)*  
*Modules (in order): Packages → Portfolio (SFW grid) → Availability → Reviews → Badges/Verification → Location (city-only hint) → FAQs*  
*Internal links: "Similar {rolePlural} in {City}" (3–8 cards), "Studios with {top amenity}" (2–4 cards)*  
  
*Studio Detail:*  
*H1: {StudioName} — {City}*  
*Intro (amenity-rich; SFW)*  
*Modules: Gallery (SFW) → Rates & Rules → Amenities → Availability/Slots → Host → Location (area only) → FAQs*  
*Internal links: "People recently booked here" cards*  
  
*City/Role Landing:*  
*H1: {RolePlural} in {City}*  
*Intro paragraph (~120–160 words, unique)*  
*Modules: Top Verified → New this week → Budget filters → Case Studies carousel (SFW)*  

**Internal linking rules**

- Every profile and studio page should expose **two blocks** of curated internal links: “Similar in {City}” and a cross‑entity block (People↔Studios).
- Keep links **crawlable** (no *nofollow*), descriptive anchor text, and **stable** across rebuilds (deterministic selection).
