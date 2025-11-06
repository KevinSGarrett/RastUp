---
id: TD-360
title: "**1.18.F Network & edge protections**"
source_doc: "TechDevBlueprint.docx"
source_path: "docs\blueprints\tech\TD-360-118f-network-edge-protections\TD-360-overview.md"
parent_id: 
anchor: "TD-360"
checksum: "sha256:743ffead1a8cf52a9dc35871a5f435a66eaf85a91cd003135f089b49ab21d759"
last_modified: "2025-11-06T20:40:46Z"
doc_kind: "TD"
h_level: 2
---
<a id="TD-360"></a>
## **1.18.F Network & edge protections**

- **CloudFront + WAF**:

  - Managed rule sets (AWS Core, Bot Control), plus custom: block obvious scanners, rate‑limit */graphql* and POSTs.
  - Allowlist Stripe & provider IPs for webhook ingress (alternate: use API Gateway with a shared secret HMAC).

- **AWS Shield Standard** (at least) enabled on CF/ALB.

- **Lambdas**: in VPC only if they need RDS; otherwise public (reduces cold‑start & cost). Use **VPC endpoints** for S3/Secrets if inside VPC.

**Inline artifact — WAF rate rule example**  
**Path:** *security/waf/rate-limit-graphql.json*

*{ "Name":"GraphQLRateLimit","RateLimit":2000,"ScopeDownStatement":*  
*{"ByteMatchStatement":{"SearchString":"/graphql","FieldToMatch":{"UriPath":{}},"TextTransformations":\[{"Priority":0,"Type":"NONE"}\],"PositionalConstraint":"CONTAINS"}}*  
*}*
