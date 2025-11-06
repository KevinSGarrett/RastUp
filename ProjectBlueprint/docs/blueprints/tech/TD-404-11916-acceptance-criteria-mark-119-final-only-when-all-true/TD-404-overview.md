---
id: TD-404
title: "**1.19.16 Acceptance criteria — mark §1.19 FINAL only when ALL true**"
source_doc: "TechDevBlueprint.docx"
source_path: "docs\blueprints\tech\TD-404-11916-acceptance-criteria-mark-119-final-only-when-all-true\TD-404-overview.md"
parent_id: 
anchor: "TD-404"
checksum: "sha256:16c6baf9ceb7bad2f47fc8483493f25852d03dd991873e5811c210d958912ac9"
last_modified: "2025-11-06T20:40:46Z"
doc_kind: "TD"
h_level: 2
---
<a id="TD-404"></a>
## **1.19.16 Acceptance criteria — mark §1.19 FINAL only when ALL true**

2036. Locale selection persists; server adds *lang* & *dir* correctly; **no auto‑redirect loops**; hreflang alternates present on SEO pages.
2037. ICU MessageFormat is used across web/app/emails; prices/dates/numbers localized; dual‑timezone display where relevant.
2038. RTL renders correctly: layout mirrored, icons swapped, reading order valid; no clipped/truncated text.
2039. A11y: WCAG 2.2 AA checks pass (axe/pa11y + manual SR runs); keyboard navigation works across all interactive components.
2040. Public pages (SEO) pre‑render localized titles/descriptions/JSON‑LD with **SFW images** only; Safe‑Mode rules respected.
2041. Catalogs load per‑locale (no shipping all); bundle budgets met; Node SSR has full‑icu.
2042. Translation workflow operational: extraction → PR review → pseudolocalized QA → deploy; glossary maintained.
2043. Emails localized, with quiet hours by timezone; no 18+ previews in emails.
2044. Costs controlled: catalogs on S3/CDN; no paid localization SaaS at launch.

# **§1.20 — Mobile (PWA + Optional Native Shells), Push, and Device Capabilities**

*(app architecture · PWA config & offline · optional RN/Expo shells · deep links & routing · auth/session on device · push notifications (APNs/FCM/Pinpoint) · file uploads from camera · Safe‑Mode & age‑gated UX · performance budgets · a11y on mobile · CI/CD & releases · telemetry · tests · cost posture)*

**Purpose.** Specify the complete mobile experience: a first‑class **Progressive Web App (PWA)** that covers the entire user journey (discovery → messages → booking → delivery), with an optional **React Native (Expo) shell** for app store presence when/if desired. This section defines how we implement offline, push, deep‑links, device uploads, Safe‑Mode gating, performance, a11y, telemetry, CI/CD, and costs. All artifacts are **inline text** for your Word doc with “Recommended filename/path” tags so your builders can later lift them into the repo.
