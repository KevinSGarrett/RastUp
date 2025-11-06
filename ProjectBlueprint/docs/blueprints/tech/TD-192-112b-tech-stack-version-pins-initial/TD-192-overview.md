---
id: TD-192
title: "**1.12.B Tech stack & version pins (initial)**"
source_doc: "TechDevBlueprint.docx"
source_path: "docs\blueprints\tech\TD-192-112b-tech-stack-version-pins-initial\TD-192-overview.md"
parent_id: 
anchor: "TD-192"
checksum: "sha256:f10b1ec605cd95ac9d687d19143d6c51315bea3abe676c0565ae56b0b8d547a4"
last_modified: "2025-11-06T20:40:46Z"
doc_kind: "TD"
h_level: 2
---
<a id="TD-192"></a>
## **1.12.B Tech stack & version pins (initial)**

- **Frontend:** Next.js (App Router), React 18, TypeScript 5, Node LTS.
- **Hosting & Edge:** Amplify Hosting + CloudFront; ISR/SSR enabled where needed.
- **BFF/API:** AWS AppSync (GraphQL) + Lambda resolvers (Node 20), with pipeline resolvers for auth, validation, and rate‑limits.
- **Auth:** Amazon Cognito (User Pool + Identity Pool).
- **Relational:** Amazon Aurora PostgreSQL **Serverless v2** (multi‑AZ, autoscaling).
- **NoSQL/Hot path:** DynamoDB (messaging, presence, comms dedupe, ads caches, trust cache).
- **Search:** **Typesense** (MVP) with optional adapter to **OpenSearch Serverless** (feature‑flag).
- **Queues/Orchestration:** SQS + SNS + EventBridge; AWS Step Functions for §1.3 saga.
- **Object storage & CDN:** S3 (private + public buckets) + CloudFront; Lambda@Edge for image transforms; optional MediaConvert (flag).
- **Moderation:** Rekognition/Vision model (NSFW banding); ClamAV Lambda for basic AV.
- **E‑sign:** Dropbox Sign or DocuSign via adapter (flag).
- **Payments/Tax:** Stripe (+ Financial Connections for ACH) and TaxJar/Avalara/Stripe Tax via adapter.

**Suggested modules:** we adopt cost‑efficient open‑source options where safe (e.g., Typesense, MJML for email, image proxy), and keep vendor count minimal (Stripe handles cards + ACH).
