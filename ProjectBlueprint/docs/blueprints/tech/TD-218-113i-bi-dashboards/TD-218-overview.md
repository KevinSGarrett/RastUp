---
id: TD-218
title: "**1.13.I BI & dashboards**"
source_doc: "TechDevBlueprint.docx"
source_path: "docs\blueprints\tech\TD-218-113i-bi-dashboards\TD-218-overview.md"
parent_id: 
anchor: "TD-218"
checksum: "sha256:8c71c1cee6b16be602ef1f43cacffcbdb6e1255a9d42f3638145c4ea2bb3186b"
last_modified: "2025-11-06T20:40:46Z"
doc_kind: "TD"
h_level: 2
---
<a id="TD-218"></a>
## **1.13.I BI & dashboards**

- **QuickSight** workspaces per function: **Executive**, **City Ops**, **Trust**, **Finance**, **Support**, **Growth**.
- Use **SPICE** extracts for fast loads; refresh cadences (NRT where appropriate, otherwise daily).
- **Metabase** (optional) for self‑serve exploration; connects to Athena; row‑level guards via Lake Formation.

**Core dashboards** (initial)

- **Executive**: GMV, take rate, bookings, CAC/LTV (when available), city trends, SLO tiles.
- **Operations**: payout backlog, recon variance, cancellation/refund bands, dispute queue.
- **Trust**: IDV/BG funnels, risk bucket movement, dispute outcomes.
- **Growth/Promotions**: impressions/clicks/invalid rate, CPA proxy, campaign pacing.
- **Comms**: delivery vs bounce/complaints, digest suppression, opt‑out flow.
- **Studios**: verification rate, amenity usage, quote success %.
