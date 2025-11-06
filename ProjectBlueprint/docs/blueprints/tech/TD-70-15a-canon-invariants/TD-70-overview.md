---
id: TD-70
title: "**1.5.A Canon & invariants**"
source_doc: "TechDevBlueprint.docx"
source_path: "docs\blueprints\tech\TD-70-15a-canon-invariants\TD-70-overview.md"
parent_id: 
anchor: "TD-70"
checksum: "sha256:9bd9031eeafd8ecabaaf47d1ddc15770dc326cd5282536e6d77876e6b463cf0a"
last_modified: "2025-11-06T20:40:46Z"
doc_kind: "TD"
h_level: 2
---
<a id="TD-70"></a>
## **1.5.A Canon & invariants**

464. **Docs‑Before‑Pay:** Checkout cannot capture funds unless **every required doc** for each leg has been generated and fully signed (all signers complete).
465. **Per‑leg packs:** LBG has **one Doc Pack per leg** (Talent leg pack; Studio leg pack). Packs can contain multiple documents.
466. **Immutable evidence:** Rendered PDFs are hashed (SHA‑256) and written to S3 with WORM‑like retention; every receipt references doc hashes.
467. **Versioned clauses:** All doc content is composed from a **clause library** with semantic versioning and city gates.
468. **Re‑issue on change:** Any scope/time/location change that affects the contract content **invalidates** prior signatures and requires re‑issue (with clear UX).
469. **Privacy & redaction:** PII and signatures are stored securely; evidence exports support **minimal disclosure** redactions for disputes.
470. **Seven‑year retention** (configurable) for all signed docs and envelope metadata.
