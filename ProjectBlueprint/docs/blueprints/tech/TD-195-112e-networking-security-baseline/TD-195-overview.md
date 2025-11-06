---
id: TD-195
title: "**1.12.E Networking & security baseline**"
source_doc: "TechDevBlueprint.docx"
source_path: "docs\blueprints\tech\TD-195-112e-networking-security-baseline\TD-195-overview.md"
parent_id: 
anchor: "TD-195"
checksum: "sha256:3c2d92022c2e592c4088895f8457413df82352b059d0041a80b5a6af0fc7f4d5"
last_modified: "2025-11-06T20:40:46Z"
doc_kind: "TD"
h_level: 2
---
<a id="TD-195"></a>
## **1.12.E Networking & security baseline**

- **VPC** for Aurora + Typesense/OpenSearch; Lambdas in private subnets with NAT **only where needed** (watch NAT cost).
- **Security groups**: least privilege; no public RDS; AppSync → Lambda via VPC endpoints if required.
- **WAF** on CloudFront: bot rate limits, SQLi/XSS rules, country blocks (configurable).
- **TLS**: ACM certs for all domains; enforced HTTPS everywhere.
- **KMS**: CMKs for RDS, Dynamo, S3 buckets (customer-managed where necessary).
- **CORS & CSP**: locked to app domains + Stripe/e‑sign domains.
- **PII partitioning**: sensitive data in Aurora; no PII in search indexes or logs.
