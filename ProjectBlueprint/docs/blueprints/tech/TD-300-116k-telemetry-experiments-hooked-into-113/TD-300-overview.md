---
id: TD-300
title: "**1.16.K Telemetry & experiments (hooked into §1.13)**"
source_doc: "TechDevBlueprint.docx"
source_path: "docs\blueprints\tech\TD-300-116k-telemetry-experiments-hooked-into-113\TD-300-overview.md"
parent_id: 
anchor: "TD-300"
checksum: "sha256:f5fb26ff545e3d7e979364af3f41bbbd2a9924510830eea056afc6d9f913740d"
last_modified: "2025-11-06T20:40:46Z"
doc_kind: "TD"
h_level: 2
---
<a id="TD-300"></a>
## **1.16.K Telemetry & experiments (hooked into §1.13)**

- **Events**: *search.saved\|alert.sent\|alert.click*, *feed.post.publish\|impression\|click*, *sharecard.create\|click*, *lib.microsite.visit*, *book_again.sent\|clicked\|converted*, *referral.invite\|accepted\|qualified\|clawback*.
- **Gold KPIs**: alert CTR, digest CTR, follow growth, feed engagement, book‑again conversion, referral qualification rate, fraud/clawback rate.
- **Guardrails**: unsubscribe/complaint rates; Safe‑Mode breaches (should be zero for emails).
- **NRT** ops tiles: today’s alerts/digests volume, referral awards vs caps, clawbacks.
