---
id: TD-534
title: "**1.28.15 Acceptance criteria — mark §1.28 FINAL only when ALL true**"
source_doc: "TechDevBlueprint.docx"
source_path: "docs\blueprints\tech\TD-534-12815-acceptance-criteria-mark-128-final-only-when-all-true\TD-534-overview.md"
parent_id: 
anchor: "TD-534"
checksum: "sha256:cf29a234909291393a5c90754ab2a462aeceb8652f07ac9902ea7746e379fbc4"
last_modified: "2025-11-06T20:40:46Z"
doc_kind: "TD"
h_level: 2
---
<a id="TD-534"></a>
## **1.28.15 Acceptance criteria — mark §1.28 FINAL only when ALL true**

2571. RBAC & SSO enforced; destructive/financial actions require step‑up; least‑privilege verified.
2572. Casework (reports/DMCA/disputes/fraud) runs end‑to‑end with SLA timers, evidence capture, and outcomes recorded.
2573. Finance console performs refunds, payout holds/releases; reconciliation viewers operate; all actions audited.
2574. Listing & user moderation tools function with privacy safeguards; message/media access is case‑bound and time‑boxed.
2575. Search curation and Smart Docs admin are operational; CMS publishes localized help/announcements/city snippets.
2576. Feature flags & risk knobs adjustable with 4‑eyes approval; complete audit trail.
2577. Observability dashboards live; SLO alerts wired; audit stream is immutable (S3 Object Lock).
2578. Costs/security match launch posture (serverless, CloudFront+WAF, IP allowlist).

# **§1.29 — Case Studies, Portfolios & Boards — Full Technical Spec**

**Purpose.** Showcase real work (case studies, portfolio sets) on role profiles to increase buyer trust and conversion; allow collaborators to be tagged and approve credits; let buyers and producers collect favorites on **Boards** and launch “**Request a similar shoot**” flows. All public surfaces must remain **SFW** with Safe‑Mode gating, collaborator approvals, and DMCA/abuse handling. This section implements the non‑technical acceptance: portfolio tab on profiles; tagging & approvals; collaborator links to profiles; “Add to Board”; Safe‑Mode/SFW only; and editor tools in the owner dashboard.

NonTechBlueprint
