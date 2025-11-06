---
id: TD-91
title: "**1.6.D Badge logic, gates & expiration**"
source_doc: "TechDevBlueprint.docx"
source_path: "docs\blueprints\tech\TD-91-16d-badge-logic-gates-expiration\TD-91-overview.md"
parent_id: 
anchor: "TD-91"
checksum: "sha256:8f09d87be45e991d5073d99845c5396763f157e06234b4a7e2010036f3933371"
last_modified: "2025-11-06T20:40:46Z"
doc_kind: "TD"
h_level: 2
---
<a id="TD-91"></a>
## **1.6.D Badge logic, gates & expiration**

- **ID Verified (badge)** → issued when IDV status transitions to *passed* and *age_verified = true*.
- **Trusted Pro (badge)** → issued when BG status == *clear* with no pending adverse action.
- **Social Verified (badge)** → issued when OAuth verified AND snapshot passes thresholds (e.g., follower minimum or platform verification).

**Expiration / recert (configurable):**

- IDV: re-verify after 24 months (or upon provider signal).
- BG: re-check annually or upon key incidents (dispute rate spike).
- Social: nightly refresh; badge revoked if OAuth disconnects or signals stale \> N days.

**Gates driven by badges:**

- **Instant Book** requires **ID Verified** (+ optionally minimum reputation).
- **Fan-sub role visibility** requires **age_verified** and Safe-Mode OFF by adult viewers.
- **Search boosts**: ID Verified \> Social Verified \> Trusted Pro (configurable weights); Trusted Pro may also unlock promotions eligibility.
