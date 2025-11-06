---
id: TD-446
title: "**1.22.11 Fraud controls & risk flags (tied to §1.18 / §1.15)**"
source_doc: "TechDevBlueprint.docx"
source_path: "docs\blueprints\tech\TD-446-12211-fraud-controls-risk-flags-tied-to-118-115\TD-446-overview.md"
parent_id: 
anchor: "TD-446"
checksum: "sha256:f54585921c955e172a313b8bafba6692ccbd5ac97e2297fe8f561c5ced2f7ec9"
last_modified: "2025-11-06T20:40:46Z"
doc_kind: "TD"
h_level: 2
---
<a id="TD-446"></a>
## **1.22.11 Fraud controls & risk flags (tied to §1.18 / §1.15)**

- Signals: rapid multi‑card attempts, device fingerprint mismatch, same IP across multiple buyers, new provider with unusually high prices, excessive outbound messages/spam.
- Actions: enforce **3DS** on high‑risk cards, **manual review** holds, increase **reserve**, delay transfer until IDV passes.
- Every decision is written to the **immutable audit** trail (see §1.18.H).
