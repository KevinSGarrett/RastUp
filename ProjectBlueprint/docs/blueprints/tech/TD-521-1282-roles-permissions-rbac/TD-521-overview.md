---
id: TD-521
title: "**1.28.2 Roles & permissions (RBAC)**"
source_doc: "TechDevBlueprint.docx"
source_path: "docs\blueprints\tech\TD-521-1282-roles-permissions-rbac\TD-521-overview.md"
parent_id: 
anchor: "TD-521"
checksum: "sha256:be7427255e1f0d1847bb21d0751d3e05de958be893848dafc296ac18de2d98f9"
last_modified: "2025-11-06T20:40:46Z"
doc_kind: "TD"
h_level: 2
---
<a id="TD-521"></a>
## **1.28.2 Roles & permissions (RBAC)**

**Initial roles**

- *super_admin* (break‑glass, time‑boxed)
- *trust_safety* (reports, DMCA, disputes, suspensions)
- *finance_ops* (refunds, payout hold/release, reconciliation views)
- *support* (account lookup, resend emails, reset MFA, grant limited credits)
- *content_ops* (help/announcements/city SEO snippets)
- *search_curator* (pins, synonyms)
- *docs_admin* (template/versioning & envelope monitor)
- *engineering* (feature flags, config, observability read)

**Recommended path:** *admin/rbac/policy.json*

*{*  
*"trust_safety": \["case:\*","user:suspend","listing:unpublish","message:read_case_bound","audit:read"\],*  
*"finance_ops": \["payment:refund","payout:hold\|release","order:view","recon:view","audit:read"\],*  
*"support": \["user:view","user:resend_email","mfa:reset","credits:grant_limited","audit:read_own"\],*  
*"content_ops": \["cms:\*","announcement:\*","seo:snippet_edit"\],*  
*"search_curator": \["search:pin","search:synonym"\],*  
*"docs_admin": \["docs:template_crud","docs:envelope_view"\],*  
*"engineering": \["flag:\*","config:\*","observability:\*"\]*  
*}*  

**SSO & step‑up:** OIDC (Google/Okta) group→role mapping; **WebAuthn** step‑up for finance/disputes; short admin session TTL; re‑auth for destructive actions.
