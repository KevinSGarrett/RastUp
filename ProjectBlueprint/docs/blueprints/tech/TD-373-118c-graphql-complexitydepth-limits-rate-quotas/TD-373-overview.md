---
id: TD-373
title: "**1.18.C GraphQL Complexity/Depth Limits + Rate Quotas**"
source_doc: "TechDevBlueprint.docx"
source_path: "docs\blueprints\tech\TD-373-118c-graphql-complexitydepth-limits-rate-quotas\TD-373-overview.md"
parent_id: 
anchor: "TD-373"
checksum: "sha256:74ae3eb97ae6cffe4fa8aea1085410f59c4a386c16697ea6674f59753cf4785e"
last_modified: "2025-11-06T20:40:46Z"
doc_kind: "TD"
h_level: 2
---
<a id="TD-373"></a>
## **1.18.C GraphQL Complexity/Depth Limits + Rate Quotas**

**Recommended path:** *security/graphql/limits.md*

*GraphQL Limits*  
*- Max depth: 8*  
*- Max cost: 2,000 per query (field weights; nested lists penalized)*  
*- Max input payload: 256 KB*  
*- Introspection: enabled in dev/stage; disabled in prod except for whitelisted admin IPs*  
  
*Rate Quotas (per 5 minutes)*  
*- Anonymous: 120 requests*  
*- Authenticated user: 900 requests*  
*- Admin OIDC: 1,200 requests*  
*- Burst: 20 requests/second/user*  
*Enforced by WAF + AppSync throttling + identity-aware API Gateway usage plans (if used).*  

**Resolver guard (pseudocode)**  
**Path:** *security/graphql/cost-limiter.ts*

*export function enforceLimits(ctx) {*  
*if (ctx.depth \> 8 \|\| ctx.cost \> 2000) throw new Error("QUERY_LIMIT_EXCEEDED");*  
*if (ctx.inputSize \> 256\*1024) throw new Error("INPUT_TOO_LARGE");*  
*}*
