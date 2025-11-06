---
id: TD-163
title: "**1.10.J Acceptance criteria (for Part 1) — we won’t move to Part 2 until all hold**"
source_doc: "TechDevBlueprint.docx"
source_path: "docs\blueprints\tech\TD-163-110j-acceptance-criteria-for-part-1-we-wont-move-to-part-2-until-all-hold\TD-163-overview.md"
parent_id: 
anchor: "TD-163"
checksum: "sha256:7fb64e21752924a357d07b3e2028452431499b94b177cca49bb5eb6d2dc2f0a9"
last_modified: "2025-11-06T20:40:46Z"
doc_kind: "TD"
h_level: 2
---
<a id="TD-163"></a>
## **1.10.J Acceptance criteria (for Part 1) — we won’t move to Part 2 until all hold**

986. Template catalog exists with MJML→HTML render and variable schemas; at least the MVP templates are authored (booking, docs, payments, messages, trust, promotions).
987. Providers wired (SES, APNs/FCM, SNS/Twilio behind flags); Comms Router applies preferences, quiet hours, dedupe, and batching.
988. Message audits stored with immutable link to rendered bodies (email) or payload snapshots (push/SMS/in‑app).
989. User Preference & Quiet Hours UI/APIs functional; List‑Unsubscribe endpoints live and audited.
990. Channel workers respect cost gates (e.g., SMS limited to critical flows where configured).
991. Idempotency & retries verified; dedupe prevents burst spam.

# **§1.10 — Notifications & Comms**

**Part 2/2: deliverability, suppression, in‑app center, experiments & localization, tracking & privacy, admin, telemetry/SLOs, full test matrix, acceptance**

This completes the communications layer begun in §1.10 (Part 1). We won’t move to the next major subsection until §1.10 passes the 99.9% bar.
