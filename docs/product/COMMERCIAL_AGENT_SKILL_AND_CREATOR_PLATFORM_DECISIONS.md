# Commercial Agent, Skill, and Creator Platform Decisions

**Version:** v0.1.0

**Date:** 2026-07-28

**Status:** Proposed Commercial Decision Record - Pending Owner Approval

**Document Owner:** Product / Commercial / Security

## 1. Purpose and Status

This record turns market and platform research into commercial planning choices.
It does not approve implementation, provider activation, customer outreach, or
external automation. Owner approval is required before any decision becomes
Accepted, and implementation PRs still require security and product review.

## 2. Revised Product Positioning

The platform is not only an AI workspace. It is proposed as a **Persian AI Business Automation + Creator Commerce Platform**: a workspace where individuals,
creators, service providers, and businesses can use bounded AI tools, buy or sell
approved services, and later automate approved workflows.

The positioning favors useful Persian-language work over generic chat: content,
commerce, operations, documents, customer support, and developer productivity.

## 3. Commercial Thesis

Persian-speaking businesses and creators need practical output, not abstract AI
access. The commercial thesis is to combine draft-first tools, localized workflows,
creator services, and carefully bounded automation. Revenue should come from clear
value units: credits, subscriptions, assisted services, and marketplace outcomes.

Trust is a product feature. A capability that is commercially attractive but cannot
meet consent, privacy, security, or approval requirements remains deferred.

## 4. Priority Markets

Priority market evaluation includes:

- short-form video / reels editing;
- Instagram and Telegram content;
- UGC and creator campaigns;
- product photo and product-to-video;
- e-commerce catalog automation;
- website / landing page / SEO automation;
- support and sales automation;
- document / office automation;
- browser / no-API Iranian workflow automation;
- coding and DevOps;
- education/course creators;
- real estate;
- clinic/salon admin.

These are market hypotheses. Local legal, platform-policy, privacy, and service
availability constraints must be reviewed before activation.

## 5. Three-Layer Platform Model

The proposed model has three layers:

1. **AI self-service tools:** bounded Product Skills that produce drafts,
   transformations, research, and workflow assistance.
2. **Creator marketplace:** a curated Creator marketplace where approved people
   can offer services, templates, and assisted outcomes.
3. **Business agent automation:** permissioned Agent workflows for repetitive,
   auditable business operations after stronger controls are available.

Each layer has distinct risk, pricing, approval, and support responsibilities.
Marketplace discovery is not runtime approval, and an Agent does not inherit a
creator's authority.

## 6. Content and Creator Commerce Decisions

Content commerce should start with draft creation, review, and handoff rather than
automatic public publishing. Creator-facing offerings may include prompt packs,
content briefs, product visual direction, caption drafts, and campaign planning.

**Social posting is allowed as draft-first and approval-gated.** A human owner
reviews destination, copy, media, audience, and timing before any external action.
Bulk messaging, impersonation, and unreviewed automated outreach remain deferred.

## 7. E-commerce, Website, and SEO Decisions

Commerce tools should help normalize catalogs, draft listing text, generate image
briefs, propose landing-page structures, and create SEO content briefs. They must
not claim ranking outcomes or change a live storefront without explicit approval.

Website and SEO work should be reversible where possible: draft files, previews,
and review queues before publication. Catalog and customer data remain tenant
scoped. Price, inventory, payment, and fulfillment actions require separate
business rules and approvals.

## 8. Automation Philosophy and Autonomy Levels

Autonomy is a policy ladder, not a marketing feature:

- **L1:** assistive generation; produces a draft with no external side effect.
- **L2:** structured recommendation; prepares a proposed action for review.
- **L3:** bounded execution; performs an approved reversible action in a narrow
  scope with audit metadata.
- **L4:** approval-gated automation; may act only after explicit human approval
  for each consequential action or approved batch.
- **L5:** autonomous operation; not available in v1 and requires future owner,
  security, legal, and product decisions.

L1 and L2 are the commercial starting point. L3 needs robust authorization,
rollback, audit, and cancellation controls. L4 is limited to documented workflows.
L5 is not a current product commitment.

## 9. Ready-Made Agent Adoption Policy

Curated ready-made Agent adoption may occur only after certification, localization,
source verification, license review, sandbox testing, and ongoing re-review.

**No unreviewed ready-made Agent may execute directly in the core application
runtime.** Candidate packages run only in approved isolated environments using
synthetic data until evidence supports a separate decision.

Certification includes immutable version/checksum, dependency review, network
allowlist, secret isolation, output policy, Persian evaluation, cancellation, and
human-review requirements.

## 10. Commercial Agent Suites

Commercial suites are product bundles, not unrestricted agents:

- Content suite: research, scripts, captions, visual briefs, and review queues.
- Commerce suite: product data normalization, listing drafts, image briefs, and
  customer-support draft responses.
- Office suite: document extraction, summaries, templates, and approval routing.
- Developer suite: read-only code context, review drafts, and bounded DevOps
  recommendations.

Every suite must expose the relevant autonomy level and side-effect boundary.

## 11. Skill Packs for Revenue

Skill packs package coherent, bounded outcomes:

- Persian SEO brief pack;
- product photography and listing pack;
- creator campaign planning pack;
- document and office productivity pack;
- support-response draft pack;
- education/course-content pack.

A pack may include templates, Product Skills, guidance, and creator assistance.
It must not hide external data sharing, automation, or recurring charges.

## 12. Creator Marketplace Decisions

The Creator marketplace is a curated service layer, not an unmoderated code or
Agent marketplace. Creator profiles, listings, portfolios, pricing, and delivery
rules require a separate trust-and-safety design.

Creator-delivered work can include human services, approved templates, and
reviewable deliverables. It cannot automatically obtain tenant secrets, payment
control, raw private conversations, or broad publishing authority.

## 13. Revenue Model

The proposed revenue model combines:

- freemium access for limited drafts and exploration;
- credits for metered generation or media work;
- SME SaaS subscriptions for business workflows;
- enterprise setup/retainer for configuration and support;
- marketplace commission on eligible creator transactions;
- premium creator listing where policy permits;
- AI enhancement fee for bounded assisted workflows;
- white-label / agency offerings after tenancy and support requirements are met.

Pricing must be transparent, show credit impact before a billable operation, and
avoid implying that a model outcome is guaranteed.

## 14. Persian Localization Requirements

Localization is more than translation. Product acceptance requires right-to-left
layout, mixed Persian/English text handling, Persian terminology, culturally
appropriate content controls, localized business flows, and understandable consent
language.

Where relevant, evaluate Jalali calendar needs, local document conventions, local
business vocabulary, and legal or platform constraints. Persian quality and RTL
behavior are release criteria for any commercial pack marketed as Persian-first.

## 15. What Is Deferred Versus Forbidden

Deferred pending stronger evidence and approvals:

- social auto-publishing;
- payment write actions;
- arbitrary browser control;
- arbitrary script execution;
- autonomous customer contact;
- autonomous deployment;
- third-party Agent Marketplace.

Forbidden in v1:

- cross-tenant data search;
- unrestricted shell;
- secret inheritance;
- automatic spending;
- autonomous PR merge;
- raw private conversation access by default.

**Browser automation is allowed only for allowlisted domains** and only under a
separately approved, bounded workflow with appropriate user approval.

## 16. Recommended First Commercial Product

The first commercial product is **Persian Content and Commerce Studio**. It bundles
L1 and L2 content creation, product visual briefs, listing drafts, Persian SEO
briefs, document assistance, and creator handoff. It prioritizes visible value and
reviewable outputs over autonomous external action.

Initial success measures should be owner-approved engagement, conversion, repeat
use, delivery quality, and support burden indicators, without inventing targets in
this record.

## 17. Recommended Second Commercial Product

The second commercial product is **Persian Business Agent Pack**. It follows only
after the first product validates permissions, audit, credits, and review flows.
It begins with L2 and selected L3 workflow assistance for support, catalog, office,
and business operations, not autonomous customer contact or payment actions.

## 18. Implementation Sequencing

1. Define Product Skill registry and versioned manifests.
2. Deliver Content and Commerce Studio draft-first Skills.
3. Add credits, audit metadata, and creator handoff workflow.
4. Establish creator verification and marketplace delivery policy.
5. Evaluate bounded business workflows using synthetic data.
6. Add approval-gated L3 automation only where reversible and auditable.
7. Evaluate Persian Business Agent Pack after owner and security decisions.

Core MVP work can proceed before higher-autonomy automation. Each phase requires
separate acceptance, privacy, security, and product approval.

## 19. Owner Approval Checklist

- [ ] Revised product positioning accepted.
- [ ] Priority market order accepted.
- [ ] Three-layer platform model accepted.
- [ ] L1–L5 autonomy model accepted.
- [ ] Ready-made Agent certification policy accepted.
- [ ] Persian Content and Commerce Studio accepted as first product.
- [ ] Persian Business Agent Pack accepted as second product.
- [ ] Revenue model direction accepted.
- [ ] Deferred and forbidden capability boundaries accepted.
- [ ] Implementation sequencing accepted.

## 20. Open Decisions

- First creator categories and verification requirements.
- Marketplace commission and premium-listing policy.
- Credit pricing and AI enhancement fee policy.
- Enterprise setup/retainer service boundaries.
- White-label / agency eligibility and tenant model.
- First L3 workflow eligible for approval-gated automation.
- Browser allowlist ownership and review cadence.
- Localized payment, tax, and legal requirements.
- Creator dispute, refund, and content moderation policy.

### Related Documents

- Technical v1 decisions: [MCP_SKILLS_AGENTS_V1_DECISIONS.md](MCP_SKILLS_AGENTS_V1_DECISIONS.md)
- Skills research: [SKILLS_LANDSCAPE_RESEARCH.md](../research/SKILLS_LANDSCAPE_RESEARCH.md)
- Agents research: [AGENTS_LANDSCAPE_RESEARCH.md](../research/AGENTS_LANDSCAPE_RESEARCH.md)
- Agent security: [AGENT_SECURITY_MODEL.md](../security/AGENT_SECURITY_MODEL.md)
