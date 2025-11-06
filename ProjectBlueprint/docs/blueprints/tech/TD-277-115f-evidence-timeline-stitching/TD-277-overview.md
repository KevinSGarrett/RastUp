---
id: TD-277
title: "**1.15.F Evidence & timeline stitching**"
source_doc: "TechDevBlueprint.docx"
source_path: "docs\blueprints\tech\TD-277-115f-evidence-timeline-stitching\TD-277-overview.md"
parent_id: 
anchor: "TD-277"
checksum: "sha256:b67189357638556bffff5cbf2cef47e8c82165a0b81c9b5b7f5e354b723ac0dd"
last_modified: "2025-11-06T20:40:46Z"
doc_kind: "TD"
h_level: 2
---
<a id="TD-277"></a>
## **1.15.F Evidence & timeline stitching**

When a case opens or moves to **Investigating**, the system auto‑collects:

- **Messages & action cards** (from §1.4) for the thread(s) related to *leg_id* or *request_id*.
- **Docs & signatures** (from §1.5)—hashes and acceptance timestamps.
- **Deliverables & approvals** (proofs/finals manifests).
- **Geo/time** events (check‑ins, scheduled time windows, IP/device changes).
- **Finance**: charge, refund, payout records (§1.9).
- **Comms**: notification delivery (for “no response” claims).
- **Risk**: user risk scores (§1.6.G).

Evidence appears in a **chronological timeline** within the case.
