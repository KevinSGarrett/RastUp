---
id: TD-584
title: "**1.4.D Email + Push templates (transactional & digest)**"
source_doc: "TechDevBlueprint.docx"
source_path: "docs\blueprints\tech\TD-584-14d-email-push-templates-transactional-digest\TD-584-overview.md"
parent_id: 
anchor: "TD-584"
checksum: "sha256:a9588e7fe02f9da9e28b19cb01e9669bf23ad1d6e6adab5abce91770b1d357e4"
last_modified: "2025-11-06T20:40:46Z"
doc_kind: "TD"
h_level: 2
---
<a id="TD-584"></a>
## **1.4.D Email + Push templates (transactional & digest)**

**Providers:** SES (email), Pinpoint/APNs/FCM (push).  
**Transactional events:** Message Request, Request Accepted/Declined, New Message, Card Proposals (reschedule/extras/approvals), Booking Confirmed/Rescheduled, Milestone Delivered, Dispute Opened.

**Email template structure** (HTML + text):

- **Subject patterns**:

  - \[RastUp\] {Name} sent a message
  - \[Action Required\] {Name} proposed {cardType}
  - \[Confirm\] Your booking with {Provider} is {status}

- **Header**: brand bar + thread subject + role chip

- **Body**: last message snippet or card summary + CTA buttons (**Open Thread**, **Approve**, **Decline**)

- **Footer**: notification preferences + legal

- **ICS attachment**: on **confirmed** bookings or **rescheduled** timeslots.

NonTechBlueprint

**Push payloads** mirror subjects with compact actions.
