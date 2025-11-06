---
id: TD-171
title: "**1.10.Y Full test matrix (Part 2)**"
source_doc: "TechDevBlueprint.docx"
source_path: "docs\blueprints\tech\TD-171-110y-full-test-matrix-part-2\TD-171-overview.md"
parent_id: 
anchor: "TD-171"
checksum: "sha256:ca5429b2152b188a96caa3d84c8829c693febbdeafab86dd8aad49af3db07107"
last_modified: "2025-11-06T20:40:46Z"
doc_kind: "TD"
h_level: 2
---
<a id="TD-171"></a>
## **1.10.Y Full test matrix (Part 2)**

**Deliverability**

1040. SPF/DKIM/DMARC pass; BIMI optional path.
1041. Shared IP warm sends; dedicated IP warmup plan verified (if enabled).
1042. From/Reply‑To policies applied; DMARC alignment OK.

**Suppression**  
4) Hard bounce → suppression; retry rules for soft bounces; complaint → global suppression.  
5) One‑click unsubscribe toggles correct categories; re‑permission requires explicit user action.

**In‑app**  
6) Pagination, grouping, unread counts, pinning; accessibility roles/labels.

**Experiments**  
7) Stable bucketing; hold‑out analyses; guardrail auto‑rollback triggers.

**Localization**  
8) Locale fallback path; pluralization; timezone formatting.

**Tracking & privacy**  
9) Link wrapper logs click; no tracking for security/legal; UTM only on allowed templates; DNT honored.

**Admin**  
10) Template versioning diff + dual approval; test sends whitelisted only; suppression viewer actions audited.

**Performance & cost**  
11) Event→send SLOs met under synthetic load; SMS cost gates observed; SES cost within envelope.
