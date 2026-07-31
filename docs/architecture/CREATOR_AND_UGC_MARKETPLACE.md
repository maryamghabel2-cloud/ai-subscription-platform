# Creator and UGC Marketplace

**Version:** v0.1.0

**Date:** 2026-07-29

**Status:** Proposed Architecture - Pending Owner Approval and Implementation

**Document Owner:** Marketplace / Product / Security

## 1. Purpose and Status

- Proposed architecture only; no marketplace, payment, escrow, matching, or frontend is implemented.

- It connects brands with creators and service providers using AI assistance and commission boundaries.


## 2. Marketplace Participants and Roles

- Buyer: business or brand.

- Creator: UGC creator, editor, photographer, copywriter, SEO specialist, social manager, website builder, or automation specialist.

- Platform: matching, QA, escrow boundary, and commission record.

- | Category | Example service | First phase |

- |---|---|---|

- | UGC creator | Short-form delivery | later |

- | Editor | Reels editing | later |

- | Photographer | Product variants | later |

- | Copywriter | Persian campaigns | later |

- | SEO specialist | Content brief | later |


## 3. Canonical Domain Concepts

- Brief

- Enhanced Brief

- Creator Profile

- Portfolio Item

- Match Proposal

- Order

- Milestone

- Deliverable

- Revision Request

- Delivery Package

- Usage License Record

- Consent Record

- Commission Record

- Dispute Case


## 4. Brief Creation and AI Brief Enhancer

- Buyer describes need in plain Persian.

- AI Brief Enhancer creates scope, deliverables, targets, tone, brand kit, budget range, deadline, and usage-rights draft.

- Buyer reviews and approves enhanced brief from L2 draft to approval.

- Briefs are versioned.


## 5. Creator Profiles and Verification

- Profiles include skills, categories, portfolio, and languages.

- Tiers: unverified, identity-verified, platform-certified.

- Verification method remains Open Decision.

- Portfolio references delivered work with permission.

- Ratings and completion metrics require anti-fraud controls.

- Creators are independent, not platform employees.


## 6. Matching and Discovery

- AI-assisted matching considers category, style, budget, and availability.

- Manual browse and invite are supported.

- No auto-assignment without both-side acceptance.

- Fairness and anti-bias are Open Decisions.


## 7. Order Lifecycle

- States: draft, brief_approved, proposed, accepted, in_progress, delivered, revision_requested, approved, completed, cancelled, disputed.

- State transitions are metadata audit logged.

- Deadline and milestone tracking are required.

- Cancellation policy details remain Open Decision.


## 8. Delivery, Revision, and AI-Assisted QA

- Creator uploads through media foundation.

- AI QA gives brief-compliance hints, technical checks, and caption/RTL sanity.

- AI QA is advisory (L2), never auto-rejects human work.

- Buyer review and revision requests are supported.

- CONFIGURED_REVISION_ROUNDS bounds revision policy.

- Version history is preserved.


## 9. Rights, Consent, and Usage License Model

- Every delivery requires a Usage License Record.

- Record scope, platforms, duration, exclusivity, and territory.

- Creator consent covers likeness where applicable.

- Brands cannot use content beyond licensed scope.

- Platform training or marketing use requires explicit consent.

- License transfer occurs on completion, not before settlement.


## 10. Payment, Escrow, and Commission Boundary

- BOUNDARY ONLY: buyer funding may use an escrow-like hold; mechanism is Open Decision.

- Funds release on approval.

- Platform commission uses CONFIGURED_MARKETPLACE_COMMISSION_RATE.

- Payout methods are Open Decisions.

- Refund handling follows cancellation/dispute policy.

- No payment implementation exists in this document.


## 11. Dispute and Resolution Framework

- Dispute window follows approved policy.

- Evidence includes brief version, deliverables, revision history, and message metadata.

- Resolution ladder: AI-assisted summary, platform mediator, final decision.

- Outcomes: release, partial release, refund, rework.

- CONFIGURED_DISPUTE_RESOLUTION_SLA represents policy timing.


## 12. Trust, Safety, and Anti-Fraud

- Fake portfolio signals

- off-platform payment circumvention metadata signals

- review authenticity controls

- prohibited content enforcement

- creator impersonation prevention

- buyer abuse and scope-creep signals

- Security Agent anomaly metadata integration


## 13. AI-Human Collaboration Model

- AI drafts; human perfects.

- Human work may be AI-enhanced only with creator and buyer consent.

- Label AI-assisted versus human-original deliverables.

- Creator studio credit policy remains Open Decision.


## 14. Autonomy Levels and Human Approval

| Action | Level | Notes |
|---|---|---|
| Browse creator profiles and portfolios | L1 | Read-only |
| Read published briefs | L1 | Read-only |
| AI brief enhancement suggestion | L2 | Draft, buyer must accept |
| AI match/creator recommendation | L2 | Draft, buyer must select |
| AI QA notes on delivery | L2 | Advisory, human decides |
| Publish a brief | L3 | Explicit buyer approval |
| Accept an order (as creator) | L3 | Explicit creator approval |
| Submit delivery | L3 | Explicit creator action |
| Approve delivery / request revision | L3 | Explicit buyer approval |
| Release funds (future) | L3 | Requires payment/legal approval |
| Auto-hiring without buyer/creator consent | Forbidden in v1 | — |
| Auto-payout without approval | Forbidden in v1 | — |
| Cross-brand content reuse without rights | Forbidden | — |

L4 (Bounded Autonomy) may later apply to narrow, low-risk actions such as automatic
FAQ replies inside creator support workflows, only after separate approval. L5
(High Autonomy) is not permitted for money movement, hiring, publishing, or rights
decisions in v1. Every L3+ action is recorded in the audit trail as metadata only,
without raw private message content.

## 15. Persian-First Marketplace Requirements

- Persian industry brief templates

- RTL profile and portfolio rendering

- plain-language Persian license summaries

- Jalali alongside Gregorian display

- Iranian business workflow fit and Instagram-first targets


## 16. Proposed Implementation PR Sequence

- 1. creator profile and category models

- 2. brief and enhanced-brief models

- 3. order lifecycle state machine

- 4. deliverable and license models

- 5. matching v1 manual browse/invite

- 6. AI brief enhancer

- 7. AI QA advisory checks

- 8. dispute case model

- 9. commission recording without payment

- 10. payment/escrow later after legal review

- 11. frontend marketplace UI later


## 17. Open Decisions

- commission rate

- escrow/payment legal structure

- creator verification method

- payout methods

- revision rounds default

- dispute SLA

- exclusivity pricing

- creator studio credit policy

- matching fairness policy

- cross-border creators policy

