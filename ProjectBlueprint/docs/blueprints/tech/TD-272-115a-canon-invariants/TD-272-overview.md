---
id: TD-272
title: "**1.15.A Canon & invariants**"
source_doc: "TechDevBlueprint.docx"
source_path: "docs\blueprints\tech\TD-272-115a-canon-invariants\TD-272-overview.md"
parent_id: 
anchor: "TD-272"
checksum: "sha256:bd4d7fe6844235f809b4070a92671513ffd5ca935efb325d6b5f2f46b8565400"
last_modified: "2025-11-06T20:40:46Z"
doc_kind: "TD"
h_level: 2
---
<a id="TD-272"></a>
## **1.15.A Canon & invariants**

1603. **Single front door** for all issues (“Support Center”), but **typed cases** with tailored flows.
1604. **Evidence first**: timelines aggregate **messages, deliverables, docs, approvals, geotime metadata**, and **payment records**—no decisions without evidence.
1605. **Refund math is deterministic** (driven by cancellation bands, completion status, and doc acceptance); manual overrides require **reasons + dual approval**.
1606. **Chargebacks ≠ refunds**: separate workflows; chargebacks follow card‑network timelines with **representment** packages.
1607. **Payout safety**: severe open cases place **holds** on affected payouts until resolved.
1608. **DMCA & policy**: legal requirements honored; immutable audits; content can be hidden rapidly but restored with counter‑notice if eligible.
1609. **Cost‑conscious**: in‑house ticketing with SES email bridge; optional external helpdesk later via adapter; storage in S3 with lifecycle policies.
1610. **Privacy**: no raw PII in case summaries beyond what’s necessary; redaction tools for doxxing.
1611. **SLAs by severity**: response and resolution targets with SLO monitoring; breached cases auto‑escalate.
