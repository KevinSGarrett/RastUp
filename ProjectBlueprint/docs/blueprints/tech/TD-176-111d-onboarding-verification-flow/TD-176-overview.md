---
id: TD-176
title: "**1.11.D Onboarding & verification flow**"
source_doc: "TechDevBlueprint.docx"
source_path: "docs\blueprints\tech\TD-176-111d-onboarding-verification-flow\TD-176-overview.md"
parent_id: 
anchor: "TD-176"
checksum: "sha256:c6bbf67eb5b1786d247f6e2789e938a5e468cafcc8dd874713c00485e487f089"
last_modified: "2025-11-06T20:40:46Z"
doc_kind: "TD"
h_level: 2
---
<a id="TD-176"></a>
## **1.11.D Onboarding & verification flow**

**Owner tasks**

1067. Create listing (title, description, address, city/geo).
1068. Add **amenities**, **capacity**, **pricing schedules**, **buffers**, **house rules**, and **deposit policy**.
1069. Upload **previews** (scanned; SFW).
1070. Submit **verification**: proof of control/ownership (lease/utility), IDV match to owner (see §1.6), optional insurance cert.

**Admin verification**

- Review docs; optional video call or geo‑code match.
- **Approve** → *verified_studio=true* and studio gets badge; **Reject** → return reasons.
- **Revoke** when reports or insurance lapse; all actions audited in *studio_verification_audit*.

**Publishing gate**

- Cannot publish unless required fields + minimum media count met and **house rules** present. Verification not required to publish, but required for some placements/promotions.
