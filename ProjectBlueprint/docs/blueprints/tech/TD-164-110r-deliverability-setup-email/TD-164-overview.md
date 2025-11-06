---
id: TD-164
title: "**1.10.R Deliverability setup (email)**"
source_doc: "TechDevBlueprint.docx"
source_path: "docs\blueprints\tech\TD-164-110r-deliverability-setup-email\TD-164-overview.md"
parent_id: 
anchor: "TD-164"
checksum: "sha256:00ff9312c8fd611be6a4b0c58da246de690d3cd75393ad8013d93e24569f6a39"
last_modified: "2025-11-06T20:40:46Z"
doc_kind: "TD"
h_level: 2
---
<a id="TD-164"></a>
## **1.10.R Deliverability setup (email)**

**R.1 Domain authentication (SES, production domain e.g.,** ***notify.rastup.com*****)**

- **SPF**: *v=spf1 include:amazonses.com -all*
- **DKIM**: enable **Easy DKIM** in SES; publish 3 CNAMEs; rotate annually (calendar reminder + auto‑rotate playbook).
- **DMARC**: start with *v=DMARC1; p=quarantine;* [*rua=mailto:dmarc@rastup.com*](mailto:rua=mailto:dmarc@rastup.com)*;* [*ruf=mailto:dmarc@rastup.com*](mailto:ruf=mailto:dmarc@rastup.com)*; fo=1; pct=50*, graduate to *p=reject* after warmup.
- **BIMI** (optional, post‑DMARC‑reject): publish SVG logo and VMC (later, cost‑gated flag).

**R.2 SES configuration**

- Verify domain + sender identities ([*no-reply@notify.rastup.com*](mailto:no-reply@notify.rastup.com) for system, *billing@notify…* for finance, *support@…* for support).
- **Event destinations** → SNS topics for *Delivery*, *Bounce*, *Complaint*, *Open* (optional), *Click* (optional).
- Shared IPs at MVP; consider **dedicated IPs** after steady volume (requires warmup).

**R.3 IP warmup (if dedicated IPs)**

- Ramp plan for first 2–4 weeks: daily volume ladder + mix of high‑engagement templates (booking receipts) to build reputation.
- Dashboards: deliverability by mailbox provider (Gmail, Outlook, Yahoo), bounce/complaint thresholds.

**R.4 From/Reply‑To policy**

- Transactional: *From: RastUp \<no-reply@notify…\>* with **Reply‑To support** when useful.
- Avoid sending marketing from transactional subdomain.
