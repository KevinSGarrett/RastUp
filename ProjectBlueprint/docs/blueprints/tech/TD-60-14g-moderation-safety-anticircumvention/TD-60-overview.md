---
id: TD-60
title: "**1.4.G Moderation, safety, anticircumvention**"
source_doc: "TechDevBlueprint.docx"
source_path: "docs\blueprints\tech\TD-60-14g-moderation-safety-anticircumvention\TD-60-overview.md"
parent_id: 
anchor: "TD-60"
checksum: "sha256:c804cdeed65859d3282e14b750c472db89e8e6fcda4cfe4669b4c20c3241c289"
last_modified: "2025-11-06T20:40:46Z"
doc_kind: "TD"
h_level: 2
---
<a id="TD-60"></a>
## **1.4.G Moderation, safety, anticircumvention**

- **Text filters**: regex + ML models for PII/banlist (emails, phone, Venmo/CashApp handles).

  - First hit → **nudge** (educational banner).
  - Repeat → **soft block** sending with “Use on‑platform checkout.”
  - Abuse → escalation to T&S; rate‑limits or temp mutes per thread.

- **NSFW**: all previews scanned; respect Safe‑Mode (blur/blocked).

- **Report/Block**: per thread; blocks hide typing & DMs, and notify Support.

- **Audit**: every moderation action writes immutable admin audit with reason.
