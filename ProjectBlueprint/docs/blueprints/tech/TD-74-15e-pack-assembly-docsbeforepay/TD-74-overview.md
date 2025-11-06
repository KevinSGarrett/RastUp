---
id: TD-74
title: "**1.5.E Pack assembly (Docs‑Before‑Pay)**"
source_doc: "TechDevBlueprint.docx"
source_path: "docs\blueprints\tech\TD-74-15e-pack-assembly-docsbeforepay\TD-74-overview.md"
parent_id: 
anchor: "TD-74"
checksum: "sha256:286d5259a4d36506bc5d9e43a133d8510c9c39d116ef1cd1bd64b5ce487f30dc"
last_modified: "2025-11-06T20:40:46Z"
doc_kind: "TD"
h_level: 2
---
<a id="TD-74"></a>
## **1.5.E Pack assembly (Docs‑Before‑Pay)**

**When generated:**

- During checkout after *startCheckout*, **before** payment.
- For each **leg**, resolve which **template(s)** apply via city/role gates and pack them.

**Resolver inputs:**

- Leg times, location, price lines, tax quote, deposit policy (for studios), buyer/seller identities, role fields, SOW deliverables (from Brief/Shot list summary if present).

**Algorithm (high‑level):**

490. Determine applicable templates (by *leg.type*, city, role).
491. Validate all required variables can be bound; if not, return *DOC_VARS_MISSING* with a list.
492. Fill variables (see mapping in §1.5.F).
493. Render Markdown → PDF (headless Chromium or a template renderer).
494. Create envelopes with the e‑sign provider; map **signer roles → emails**; send.
495. Update *doc_pack* → *issued* and *doc_instance.envelope_status='sent'*.
496. Block payment step until **every envelope** in both relevant packs is *completed*.

**Re‑issue rules:**

- If *start_at/end_at*, *location*, *deliverables*, *deposit_policy*, or **counterparty** changes → invalidate pack (*superseded*) and re‑generate (fresh template version selection).
- All **previous** PDFs remain immutable evidence; receipts reference the **active** pack.
