---
id: TD-77
title: "**1.5.H Hashing & immutability**"
source_doc: "TechDevBlueprint.docx"
source_path: "docs\blueprints\tech\TD-77-15h-hashing-immutability\TD-77-overview.md"
parent_id: 
anchor: "TD-77"
checksum: "sha256:03272601961e756fa8a122111c5cd0f3055037493b7200a2adb27423fae3b5a4"
last_modified: "2025-11-06T20:40:46Z"
doc_kind: "TD"
h_level: 2
---
<a id="TD-77"></a>
## **1.5.H Hashing & immutability**

- After rendering, compute **SHA‑256** of PDF bytes; store in *doc_instance.render_pdf_sha256*.
- Include the hash (shortened) in the PDF footer.
- All envelopes completed → verify provider’s returned PDF by recomputing a **post‑sign hash**; store both **pre‑sign** and **post‑sign** hashes with a small allowed delta (some providers stamp signatures).
- **Receipts** reference *doc_id* and *post_sign_hash*.
- **Evidence export** pulls PDFs and a CSV/JSON of envelope metadata + sign events.
