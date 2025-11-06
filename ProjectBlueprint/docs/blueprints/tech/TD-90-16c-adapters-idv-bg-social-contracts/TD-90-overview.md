---
id: TD-90
title: "**1.6.C Adapters (IDV, BG, Social) — contracts**"
source_doc: "TechDevBlueprint.docx"
source_path: "docs\blueprints\tech\TD-90-16c-adapters-idv-bg-social-contracts\TD-90-overview.md"
parent_id: 
anchor: "TD-90"
checksum: "sha256:1e039a51d2e86dea037d91affc76dc5c9f6e412fb91a4643fd947715609f3083"
last_modified: "2025-11-06T20:40:46Z"
doc_kind: "TD"
h_level: 2
---
<a id="TD-90"></a>
## **1.6.C Adapters (IDV, BG, Social) — contracts**

**Common adapter shape (idempotent):**

- *start(user_id, params)* → *{ provider_ref, redirect_url/embedded_session }*
- *status(provider_ref)* → status enum + minimal signals (no raw PII)
- *webhook(event)* → HMAC verified; dedupe by provider_event_id
- Emits normalized events: *idv.started\|passed\|failed\|expired*, *bg.invited\|clear\|consider\|disputed\|expired*, *social.verified\|revoked*, all correlated by *user_id*.

**IDV provider options** (choose one; both fit the contract):

- **Persona** or **Stripe Identity**. We default to **Persona** for breadth; Stripe Identity is acceptable if cost/licensing or Stripe consolidation is preferred.

**BG provider**:

- **Checkr** with FCRA flow; alternative vendors possible with same contract.

**Social**:

- **Instagram Graph / TikTok / YouTube / X** OAuth; nightly snapshot; **verified** when OAuth proof valid and platform marks the account verified (or our threshold met).
