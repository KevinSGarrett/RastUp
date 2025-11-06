---
id: TD-154
title: "**1.10.A Canon & invariants**"
source_doc: "TechDevBlueprint.docx"
source_path: "docs\blueprints\tech\TD-154-110a-canon-invariants\TD-154-overview.md"
parent_id: 
anchor: "TD-154"
checksum: "sha256:578345476cef9a9332f4f42d24ba5d1991776b6dc4c397b6a76ec1749e1b1da2"
last_modified: "2025-11-06T20:40:46Z"
doc_kind: "TD"
h_level: 2
---
<a id="TD-154"></a>
## **1.10.A Canon & invariants**

927. **User control first:** channel‑level **preferences** (opt‑in/out by category) and **quiet hours** are enforced server‑side for all non‑critical comms.
928. **Critical vs non‑critical:** payment receipts, security, and legal notices always send (with minimal content); marketing is opt‑in and rate‑limited.
929. **One source of truth:** every message is a **templated document** with **variables** and an **audit trail** (who/what/why/when).
930. **Dedupe & batching:** collapse bursts (e.g., 5 rapid messages → 1 digest) and never notify a user about their **own** action unless explicitly warranted.
931. **Deliverability & compliance:** authenticated domains (SPF/DKIM/DMARC), bounce/complaint suppression, List‑Unsubscribe, CAN‑SPAM/TCPA/GDPR hygiene.
932. **Cost aware:** SES for email (default); FCM/APNs for push; SNS/Twilio for SMS behind a cost gate; in‑app first where possible.
