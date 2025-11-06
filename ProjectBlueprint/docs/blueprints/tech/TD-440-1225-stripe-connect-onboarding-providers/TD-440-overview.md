---
id: TD-440
title: "**1.22.5 Stripe Connect onboarding (providers)**"
source_doc: "TechDevBlueprint.docx"
source_path: "docs\blueprints\tech\TD-440-1225-stripe-connect-onboarding-providers\TD-440-overview.md"
parent_id: 
anchor: "TD-440"
checksum: "sha256:2a4c4b14894012e564915dcfe9fe529c53206af4323cf21e5f2b292a5cc5b7b1"
last_modified: "2025-11-06T20:40:46Z"
doc_kind: "TD"
h_level: 2
---
<a id="TD-440"></a>
## **1.22.5 Stripe Connect onboarding (providers)**

- **Type:** **Express** accounts; Stripe‑hosted onboarding/updates.
- Enable capabilities for payments/transfers; Stripe handles KYC; we reflect verification status in UI (*account.updated* webhooks).
- **Payout schedule:** weekly by default; consider T+1/T+7 policy gates (see §1.22.11).

**Artifact — onboarding link resolver**  
**Recommended path:** *api/resolvers/payments/onboarding.ts*

*export async function createOnboardingLink(userId: string) {*  
*const acct = await lookupOrCreateStripeAccount(userId); // acct\_...*  
*const link = await stripe.accountLinks.create({*  
*account: acct,*  
*refresh_url: \`\${HOST}/onboarding/refresh\`,*  
*return_url: \`\${HOST}/onboarding/return\`,*  
*type: 'account_onboarding'*  
*});*  
*return link.url;*  
*}*
