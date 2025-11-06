---
id: TD-35
title: "**1.3.P Test plan (must‑pass, CI + sandbox)**"
source_doc: "TechDevBlueprint.docx"
source_path: "docs\blueprints\tech\TD-35-13p-test-plan-mustpass-ci-sandbox\TD-35-overview.md"
parent_id: 
anchor: "TD-35"
checksum: "sha256:5e282933ceddcdf3625a3fe30b01ee4b83b2acbf7175d3cd9a879768bf889963"
last_modified: "2025-11-06T20:40:46Z"
doc_kind: "TD"
h_level: 2
---
<a id="TD-35"></a>
## **1.3.P Test plan (must‑pass, CI + sandbox)**

**Happy paths**

227. **Single‑leg Talent booking** (card): docs → pay → confirm → complete → payout queued.
228. **LBG Talent + Studio** (card+deposit auth): attach studio → docs for both legs → confirm → complete → studio deposit voided automatically → payouts queued.

**Alternates**  
3) **ACH flow**: bank link → confirm → settlement window; payouts delayed.  
4) **3DS challenge**: requires_action → client completes → webhook resumes.

**Edge & failure**  
5) **Atomicity fail**: after docs, Talent ok but Studio deposit auth fails → no charge; both legs remain *awaiting_payment*.  
6) **Change order**: add overtime → new charge or incremental capture; receipts updated; taxes re‑quoted.  
7) **Cancellation banding**: test each policy window; verify computed refunds per leg and group summary.  
8) **Dispute**: receive dispute webhook → evidence pack built → outcome recorded; payout clawback applied if lost.  
9) **Reconciliation**: daily close matches sums; artificial mismatch triggers red alert and payout pause.  
10) **Idempotency**: duplicate webhook deliveries don’t double‑apply state; duplicate client calls return same objects.
