# ADR-0002 — Phase 1 Product, Metering, and Infrastructure Decisions

## 1. Title
ADR-0002 — Phase 1 Product, Metering, and Infrastructure Decisions

## 2. Status
Owner Approved

## 3. Date
2026-08-20

## 4. Decision Owners
Product Owner and Technical Program Management

## 5. Scope
Phase 1. Implementation status: Decision approved; implementation pending.

## 6. Context
Phase 1 requires user-facing credit rules, provider routing, infrastructure
constraints, and privacy boundaries before D2 Technical Contracts.

## 7. Owner-Approved Decisions
General Chat tiers are 1, 2, and 3 credits. Prompt enhancement is 2 credits.
Caption generation and regeneration are 5 credits. Sandbox credit packages are
100, 500, and 2,000 credits. These are user-facing credits, not fiat prices.

## 8. AI Usage Metering Policy
Chat estimate considers input, retained/summarized context, output budget, model
multiplier, cached tokens, and reasoning tokens. Tier thresholds are deferred to
D2. Estimate is shown before execution and is the maximum user charge.

### Prompt Enhancer Policy

- Price per enhancement: 2 credits.
- Maximum raw prompt length: 2,000 characters.
- History retention: 90 days.
- Favorites are deferred from required Phase 1 MVP scope and may be added only
  by separate approval as a low-risk optional item.

### Caption Generator Policy

- Initial generation: 5 credits; regeneration: 5 credits as a new billable request.
- Default hashtag count: 10; minimum: 3; maximum: 30.
- Maximum description length: 1,000 characters.
- History retention: 90 days.
- Instagram platform-fit reference threshold: 2,200 characters.
- Other platform-fit thresholds are deferred to D2.

## 9. Credit Reservation and Settlement Policy
Reserve quote before provider call; settle actual successful charge; release unused
reservation; never settle above approved quote. Phase 1 absorbs unexpected cost
variance and records metadata. Failure, timeout, and cancellation release the full
reservation; canceled output may remain labeled canceled. Copy/history are free.

- Initial request timeout target: 60 seconds. D2 defines connection,
  first-token, idle-stream, and total timeout budgets.

## 10. Token Optimization Policy
Use deterministic Token Budget Manager, not an autonomous optimizer. It estimates,
routes approved lower/stronger models, budgets input/output, trims context,
summarizes older history only after D2 trigger, uses available caching, records
estimated/actual costs, and blocks insufficient quoted credits. It cannot change
pricing or silently remove safety-relevant context.

## 11. Provider Gateway Policy
OpenRouter is primary MVP gateway; expected funding is USDC-compatible but no
account/funding activation occurs here. Record prompt, completion, reasoning,
cached tokens, provider cost, and route metadata when available. MixRoute is
disabled-by-default fallback candidate pending compatibility, privacy, security,
regional, accounting, timeout, billing, and reliability due diligence. Model IDs
remain configuration, not business logic.

## 12. Infrastructure and Iran Accessibility Policy
Backend runs outside Iran; Germany or another suitable European region is preferred.
Iran accessibility without end-user VPN is a production acceptance requirement and
must be tested on Iranian mobile/fixed networks. Owner can pay crypto and lacks an
international card. Final vendor is deferred; a Hetzner-class VPS through reputable
crypto-capable reseller is an option, not vendor commitment. Initial target: 2 vCPU,
4 GB RAM, at least 40 GB SSD, supported Ubuntu LTS. Brand/domain are deferred.

## 13. Data Retention and Privacy Policy
Chat and enhancement history retention is 90 days; caption history is 90 days.
Admins receive metadata-only usage, not content. Provider retention disclosure and
deleted-data handling remain D2/D3 contract work.

## 14. Wallet and Ledger Policy
Low balance is below 20 available credits. Reservation expiration is 10 minutes;
receipt retention is 12 months. UI shows available and reserved balance. Ledger is
append-only; corrections use new compensating entries. Real gateways, cards,
recurring billing, tax invoices, bank integrations are out of Phase 1.

### Additional Owner-Approved Product Decisions

- Caption Generator returns 3 variations by default and allows a maximum of 5.
- Product Owner owns prohibited-category policy approval; detailed policy is deferred to D3.
- Copying captions and hashtags is free.
- Copying existing enhancements, reopening enhancement history, and sending an
  existing enhanced prompt to Chat are free; a new Chat run remains independently billable.

## 15. Deferred to D2 Technical Contracts
D2: tier boundaries, estimation, multipliers, model IDs, routing/fallback, timeout
budgets, summarization, quote validity, variance telemetry, non-Instagram norms,
usage normalization, Iran testing, vendor criteria. Beyond D2: brand/domain, real
payment/fiat pricing, subscriptions, production funding.

## 16. Consequences
PRDs and D2 contracts must honor quote caps, release behavior, configurable models,
and credit-only Phase 1 billing.

## 17. Risks and Mitigations
Provider cost variance is absorbed in Phase 1 and logged. Iran reachability needs
multi-network testing. Sandbox payment and no real gateway reduce financial risk.

## 18. Validation Required Before Production
Validate provider accounting, routing, timeouts, quote/idempotency, Iran access,
privacy, payment/legal approach, and end-to-end reserve/settle/release tests.

## 19. Related Documents
- [ADR-0001](0001-canonical-commercial-roadmap.md)
- [Product PRDs](../product/README.md)
- [Pricing and Unit Economics](../architecture/PRICING_AND_UNIT_ECONOMICS.md)
- [Provider Routing](../architecture/MULTI_PROVIDER_MODEL_ROUTING.md)
