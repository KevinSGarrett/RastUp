---
id: TD-254
title: "**1.14.1 Roles, gates, and global invariants (recap + expansions)**"
source_doc: "TechDevBlueprint.docx"
source_path: "docs\blueprints\tech\TD-254-1141-roles-gates-and-global-invariants-recap-expansions\TD-254-overview.md"
parent_id: 
anchor: "TD-254"
checksum: "sha256:0eee2b3004ce1ad8433ddd87fa92c66fcde29dab40a117d555678444c248a95f"
last_modified: "2025-11-06T20:40:46Z"
doc_kind: "TD"
h_level: 2
---
<a id="TD-254"></a>
## **1.14.1 Roles, gates, and global invariants (recap + expansions)**

- **Eligibility gates** (server‑enforced before any Fan‑Sub surface or API):

  - **Age**: both creator and fan must have *idv_status=passed* and *age_verified=true* (§1.6).
  - **Trust**: creator must be *ID Verified*; **Trusted Pro** badge is **not** required for Fan‑Sub (optional boost).
  - **Policy clean**: creator not suspended; no unresolved DMCA strike blocking publish.

- Safe‑Mode & visibility:

  - Public pages show **SFW previews only**; finals require explicit entitlement + Safe‑Mode OFF (for adult categories).
  - City/region gates respected if configured by creator or policy.

- **Media storage stance**: we **store only previews**; **finals** live off‑platform (creator‑controlled) and are referenced via **immutable manifests** (with file checksums).

- **Money separation**: Marketplace GMV for Fan‑Sub (subs, PPV, requests, tips) is separate from booking GMV. Platform fees are separate revenue per §1.9.
