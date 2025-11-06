---
id: TD-155
title: "**1.10.B Providers & architecture**"
source_doc: "TechDevBlueprint.docx"
source_path: "docs\blueprints\tech\TD-155-110b-providers-architecture\TD-155-overview.md"
parent_id: 
anchor: "TD-155"
checksum: "sha256:e86ecfd9fae36f44e7ec9c5b16d949c55fb3e41565d271ce157de90fbd0131c3"
last_modified: "2025-11-06T20:40:46Z"
doc_kind: "TD"
h_level: 2
---
<a id="TD-155"></a>
## **1.10.B Providers & architecture**

- **Email**: Amazon **SES** (default). Optional SendGrid adapter (feature‑flag).
- **Push**: Web push via Firebase **FCM**; mobile push via **APNs** (iOS) and **FCM** (Android).
- **SMS**: AWS **SNS SMS** (default) or **Twilio** via adapter (feature‑flag & per‑country pricing).
- **In‑app**: Real‑time via AppSync subscriptions; persisted in Aurora for unread counters.

**Pipeline (event‑driven):**  
Domain event → **Comms Router** (rules engine) → **Renderer** (select template, fill variables, localize) → **Channel workers** (email/push/SMS/in‑app) → Provider → **Webhook ingesters** (deliveries, opens, bounces, complaints) → **Suppression & analytics**.

**Backpressure & retries:** SQS queues per channel with DLQ; exponential backoff with idempotency keys.
