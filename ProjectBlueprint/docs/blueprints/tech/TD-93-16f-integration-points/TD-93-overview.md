---
id: TD-93
title: "**1.6.F Integration points**"
source_doc: "TechDevBlueprint.docx"
source_path: "docs\blueprints\tech\TD-93-16f-integration-points\TD-93-overview.md"
parent_id: 
anchor: "TD-93"
checksum: "sha256:3849ba6cea3415ac3fe9a0246abaeb8cbbe2fd6b77f68753e000dca45942aaaf"
last_modified: "2025-11-06T20:40:46Z"
doc_kind: "TD"
h_level: 2
---
<a id="TD-93"></a>
## **1.6.F Integration points**

- **Search (§1.2)**: include *verification.id*, *trustedPro*, *socialVerified* in index docs; apply **verified-only** filter when toggled; ranking boosts as configured.

- **Booking & Checkout (§1.3)**:

  - **Instant Book** path checks *idVerified=true* before allowing.
  - For Fan-sub or 18+ toggles, ensure **age_verified=true** before exposing surfaces.

- **Messaging (§1.4)**: show badges on thread headers; anticircumvention policies apply regardless of badges.

- **Admin**: trust tiles show IDV/BG status; overrides require reasons and are flagged for later audit.
