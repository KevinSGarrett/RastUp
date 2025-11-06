---
id: TD-555
title: "**1.3.7 Money movement (“escrow”), release & payouts**"
source_doc: "TechDevBlueprint.docx"
source_path: "docs\blueprints\tech\TD-555-137-money-movement-escrow-release-payouts\TD-555-overview.md"
parent_id: 
anchor: "TD-555"
checksum: "sha256:74465a6d33bb80e5abcfa93d5ff591fe537c9fc237b6ff64707022dd38322fa2"
last_modified: "2025-11-06T20:40:46Z"
doc_kind: "TD"
h_level: 2
---
<a id="TD-555"></a>
## **1.3.7 Money movement (“escrow”), release & payouts**

- **Charge & hold semantics**: capture funds to platform balance at confirm (IB) or on provider accept (RTB). This behaves as “escrow” without relying on card authorizations that time‑out.

NonTechBlueprint

- **Completion signals**:

  - **Time‑based jobs** (e.g., model for 3 hours): provider taps **Completed** after session → buyer has **24–48h** to confirm or dispute.
  - **Deliverable‑based jobs** (e.g., photo/video/creator posts): provider marks **Delivered** per milestone; buyer review window per milestone. **Auto‑release** after window if no dispute.

NonTechBlueprint

- **Payout timing**: standard release **~48h** after completion/expiry; **new‑provider risk policy**: first **X** payouts delayed up to **7 days** to reduce chargeback/fraud risk (configurable; relax with reputation). **ACH** primary; PayPal etc. optional later. Tips after completion.

NonTechBlueprint
