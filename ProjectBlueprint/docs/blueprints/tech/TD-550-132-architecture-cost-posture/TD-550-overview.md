---
id: TD-550
title: "**1.3.2 Architecture & cost posture**"
source_doc: "TechDevBlueprint.docx"
source_path: "docs\blueprints\tech\TD-550-132-architecture-cost-posture\TD-550-overview.md"
parent_id: 
anchor: "TD-550"
checksum: "sha256:dfc5ca18d39d2e789cd643b9c06a0a8b706221eb41b48156b2d362e7d6884308"
last_modified: "2025-11-06T20:40:46Z"
doc_kind: "TD"
h_level: 2
---
<a id="TD-550"></a>
## **1.3.2 Architecture & cost posture**

- **Frontend**: Next.js web (SSR for booking; ISR for directory), React Native apps.
- **API**: AppSync GraphQL → Lambda resolvers → Aurora Postgres (core booking) + DynamoDB (idempotent event log) + S3 (contracts/attachments).
- **Payments**: **Stripe Connect** (Standard/Express) + **PaymentIntents** for cards and **Financial Connections** (ACH). Funds are captured immediately to platform balance and **transferred** to providers on completion (acts as “escrow” without relying on card auth holds that expire). *No extra PSP at launch to control cost and complexity.*
- **Compliance**: Stripe KYC/KYB for providers, 3DS when required, PCI burden offloaded to Stripe.
- **Cost**: Pure serverless, small Aurora Serverless v2 floor, aggressive CloudFront caching, no paid DAM or workflow SaaS.
