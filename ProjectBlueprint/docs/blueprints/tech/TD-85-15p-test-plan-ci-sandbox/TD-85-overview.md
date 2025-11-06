---
id: TD-85
title: "**1.5.P Test plan (CI + sandbox)**"
source_doc: "TechDevBlueprint.docx"
source_path: "docs\blueprints\tech\TD-85-15p-test-plan-ci-sandbox\TD-85-overview.md"
parent_id: 
anchor: "TD-85"
checksum: "sha256:ee0d184bed1155cec6260adf62b72a7112e281402b0b63ebf8a304ddef650984"
last_modified: "2025-11-06T20:40:46Z"
doc_kind: "TD"
h_level: 2
---
<a id="TD-85"></a>
## **1.5.P Test plan (CI + sandbox)**

**Library & templates**

543. Create/publish clause v2; ensure v1 remains immutable; template references correct clause versions.
544. City/role gates: Houston‑only template isn’t applied in non‑gated city.
545. Variables: missing var → *DOC_VARS_MISSING* with exact field list.

**Pack assembly & signing**  
4) Generate packs for LBG (Talent + Studio); envelopes created; Doc‑Before‑Pay enforced.  
5) Signer email bounce → re‑send after email change.  
6) Envelope expired → re‑issue pack; prior PDFs retained as superseded.

**Hashing & evidence**  
7) Render & store PDF; verify pre‑sign vs post‑sign hash strategy; receipts reference post‑sign hash.  
8) Evidence export contains PDFs, metadata, and sign events.

**Re‑issue triggers**  
9) Reschedule booking time → pack invalidated; re‑generated; prior pack voided.  
10) Change deposit or deliverables → pack invalidated; new pack required.

**Admin**  
11) Clause edit requires dual approval; diff viewer shows exact changes; publish logs audit.  
12) Void envelope audit trail present; legal hold blocks changes.

**Integration**  
13) Messaging panel shows live doc status; action cards prompt signing; completion system message posted.  
14) Checkout blocks payment until all envelopes completed; then proceeds to payment intent confirm.
