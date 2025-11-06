---
id: TD-54
title: "**1.4.A Canon & invariants**"
source_doc: "TechDevBlueprint.docx"
source_path: "docs\blueprints\tech\TD-54-14a-canon-invariants\TD-54-overview.md"
parent_id: 
anchor: "TD-54"
checksum: "sha256:573018f2d0114630a5a6d1397c3cc9dcc9a400c111c62c4c026d214c8fa1d32e"
last_modified: "2025-11-06T20:40:46Z"
doc_kind: "TD"
h_level: 2
---
<a id="TD-54"></a>
## **1.4.A Canon & invariants**

- Thread kinds.

  - **Inquiry thread** (pre‑booking; can transition into a project on accept).
  - **Project thread** (post‑accept; bound to a **leg** or an **LBG**; unlocks Project Panel + action cards).

- **Project Panel anchors the contract.** It exposes structured tabs *inside* the conversation: **Brief**, **Moodboard**, **Shot list**, **Files**, **Docs & e‑sign**, **Expenses/Adjustments**, **Actions**.

- **Action cards** are typed, stateful message objects that **invoke domain flows** (reschedule, extras, overtime, deliverables accept/changes, cancellations/refunds, deposit claim, dispute). All are idempotent and audit‑friendly.

- **Files: “storage‑sane.”** Public previews only in S3; final deliverables stay external (Drive/Dropbox/S3 owner links) captured as **immutable manifests** (name, size, checksum, URL).

- **Safety & policy.** Safe‑Mode thumbnails; NSFW scanning; anti‑circumvention nudges; role‑scoped moderation; report/block tools.
