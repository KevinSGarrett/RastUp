---
id: TD-282
title: "**1.15.K Chargebacks & representment**"
source_doc: "TechDevBlueprint.docx"
source_path: "docs\blueprints\tech\TD-282-115k-chargebacks-representment\TD-282-overview.md"
parent_id: 
anchor: "TD-282"
checksum: "sha256:38144b2504156a56bbd9b674de69acf6065393e6ffcbb8e3009eb17db8982680"
last_modified: "2025-11-06T20:40:46Z"
doc_kind: "TD"
h_level: 2
---
<a id="TD-282"></a>
## **1.15.K Chargebacks & representment**

- **Notifications**: case created of type *chargeback* with card‑network reason code and due date.

- **Evidence pack** includes:

  - Signed docs, delivery approvals, message history, IP/device matches, geotime, studio check‑in, manifest checksums, comms delivery.

- **Submission**: representment summary + attachments; track provider ref & due date.

- **Outcomes**:

  - **Won** → release holds; reverse expense.
  - **Lost** → GL *Expense:Chargebacks*, optional risk downgrade (§1.6), optional review of promotions eligibility (§1.7).
