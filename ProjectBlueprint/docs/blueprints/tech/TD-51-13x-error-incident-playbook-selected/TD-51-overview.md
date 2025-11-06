---
id: TD-51
title: "**1.3.X Error & Incident Playbook (selected)**"
source_doc: "TechDevBlueprint.docx"
source_path: "docs\blueprints\tech\TD-51-13x-error-incident-playbook-selected\TD-51-overview.md"
parent_id: 
anchor: "TD-51"
checksum: "sha256:a36012492ebaca1bf443711c12f9ebd30467404e8cc4c1d4532390de00c3fea8"
last_modified: "2025-11-06T20:40:46Z"
doc_kind: "TD"
h_level: 2
---
<a id="TD-51"></a>
## **1.3.X Error & Incident Playbook (selected)**

- **PI fail after docs** → user sees *CHK_ATOMIC_FAIL*; LBG remains awaiting payment; guide to retry or change method.
- **ACH return** → auto-notify; re-attempt as allowed; payouts halted until resolution.
- **Payout failed** → retry; if repeated, set *paused* and notify Finance; show Seller banner.
- **Recon gate** → payouts paused; visible banner in Admin; action required to unpause.
- **Deposit claim abuse** → T&S review; throttle studio claims; require additional evidence.
