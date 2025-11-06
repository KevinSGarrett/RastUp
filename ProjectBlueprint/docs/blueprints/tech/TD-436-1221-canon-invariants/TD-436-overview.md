---
id: TD-436
title: "**1.22.1 Canon & invariants**"
source_doc: "TechDevBlueprint.docx"
source_path: "docs\blueprints\tech\TD-436-1221-canon-invariants\TD-436-overview.md"
parent_id: 
anchor: "TD-436"
checksum: "sha256:a91589f0ce8b6af9c26ac544ba659273d1e37b0804a9e8adb88024777254a9d9"
last_modified: "2025-11-06T20:40:46Z"
doc_kind: "TD"
h_level: 2
---
<a id="TD-436"></a>
## **1.22.1 Canon & invariants**

2139. **Processor:** **Stripe Connect (Express)** for providers/studios. Buyers pay through **PaymentIntents**; platform fees via application fee or separate charges+transfers.
2140. **Bank linking:** default to **Stripe Financial Connections** for ACH; consider **Plaid** only if we need features FinConn/Link don’t cover (e.g., specific institutions, account switch UX constraints).
2141. **Escrow posture:** no true escrow at launch. We either **capture immediately** and **transfer post‑completion** or **authorize then capture** for short holds.
2142. **Idempotency everywhere:** client and server actions that move money must be idempotent.
2143. **Compliance:** Stripe handles KYC for connected accounts and 1099‑K. We never store PAN; only tokens/ids.
2144. **Credits scope:** referral/promo credits reduce **platform fees only** unless a promo explicitly subsidizes subtotal.
2145. **Cost posture:** launch with **cards + Apple/Google Pay**; add ACH when volume justifies ops overhead and delayed funding.
