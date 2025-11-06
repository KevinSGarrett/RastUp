---
id: TD-371
title: "**1.18.A Threat Model (assets, trust boundaries, controls)**"
source_doc: "TechDevBlueprint.docx"
source_path: "docs\blueprints\tech\TD-371-118a-threat-model-assets-trust-boundaries-controls\TD-371-overview.md"
parent_id: 
anchor: "TD-371"
checksum: "sha256:5128325fd79358f545b8c22a4c001c4db38a15d96591c891367d769847b02dfa"
last_modified: "2025-11-06T20:40:46Z"
doc_kind: "TD"
h_level: 2
---
<a id="TD-371"></a>
## **1.18.A Threat Model (assets, trust boundaries, controls)**

**Recommended path:** *security/threat-model/overview.md*

*Assets*  
*- A1: Money flows (Stripe Connect, payouts, refunds)*  
*- A2: PII (names, emails, phones), IDV artifacts (age/18+ evidence), studio contracts*  
*- A3: Content previews (SFW only), deliverable manifests (hashes + URLs)*  
*- A4: Auth & session tokens (Cognito JWTs, admin OIDC)*  
*- A5: Audit trails & evidence vault (DMCA, chargebacks)*  
*- A6: Secrets & keys (Stripe, KMS, Secrets Manager)*  
  
*Trust Boundaries*  
*- Edge (CloudFront/WAF) → App (Next.js/AppSync/Lambdas)*  
*- App → Data (Aurora/Dynamo/S3/Glue/Athena)*  
*- Providers (Stripe/IDV/e‑sign/SES) via webhooks*  
*- Admin/OIDC → AppSync Admin mode*  
  
*Primary Risks & Controls*  
*- Injection/XXE/SSRF → parameterized queries, SSRF‑blocked by VPC egress policy, S3 Access Points*  
*- AuthZ bypass → AppSync @auth rules + resolver checks + test matrix*  
*- Webhook replay → idempotency store + HMAC verification*  
*- PII leakage/logging → structured logs with redaction + log scans*  
*- DoS/Bot → WAF rate rules + GraphQL complexity limits + per‑actor quotas*  
*- Content abuse → NSFW scanning + Safe‑Mode + DMCA pipeline*
