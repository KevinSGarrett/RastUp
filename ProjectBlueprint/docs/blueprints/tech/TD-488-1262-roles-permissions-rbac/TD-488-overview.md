---
id: TD-488
title: "**1.26.2 Roles & permissions (RBAC)**"
source_doc: "TechDevBlueprint.docx"
source_path: "docs\blueprints\tech\TD-488-1262-roles-permissions-rbac\TD-488-overview.md"
parent_id: 
anchor: "TD-488"
checksum: "sha256:343fec7ea61e6931e91f8042b01cd5d724d497aca6bda2220cda2e20b4217284"
last_modified: "2025-11-06T20:40:46Z"
doc_kind: "TD"
h_level: 2
---
<a id="TD-488"></a>
## **1.26.2 Roles & permissions (RBAC)**

**Roles (initial set)**

- *super_admin* (break‑glass; very limited holders)
- *trust_safety* (reports, DMCA, disputes, suspensions)
- *finance_ops* (refunds, holds, releases, reconciliation views)
- *support* (account lookups, resend emails, reset MFA, limited credits)
- *content_ops* (help/announcements/city content; SEO snippets)
- *search_curator* (pins, synonyms; §1.21)
- *docs_admin* (templates/versioning; §1.25)
- *engineering* (feature flags, config, read‑only observability)

**Recommended path:** *admin/rbac/policy.json*

*{*  
*"trust_safety": \["case:\*", "user:suspend", "listing:unpublish", "message:read_case_bound", "audit:read"\],*  
*"finance_ops": \["payment:refund", "payout:hold\|release", "order:view", "recon:view", "audit:read"\],*  
*"support": \["user:view", "user:resend_email", "mfa:reset", "credits:grant_limited", "audit:read_own"\],*  
*"content_ops": \["cms:\*", "announcement:\*", "seo:snippet_edit"\],*  
*"search_curator": \["search:pin", "search:synonym"\],*  
*"docs_admin": \["docs:template_crud", "docs:envelope_view"\],*  
*"engineering": \["flag:\*", "config:\*", "observability:\*"\]*  
*}*  

**SSO.** OIDC (Google Workspace / Okta) with group→role mapping. Session lifetime short; re‑auth for destructive actions.
