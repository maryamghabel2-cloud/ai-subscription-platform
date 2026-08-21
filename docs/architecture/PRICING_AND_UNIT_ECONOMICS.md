# Pricing, Profit, Wallet, and Unit Economics

**Version:** v0.1.0

**Date:** 2026-07-24

**Status:** Proposed Architecture - Pending Owner, Finance, Security, and
Compliance Approval

**Document Owner:** Product Architect / Finance

**Purpose:** Define business decision for target contribution margin,
mathematical clarification of selling price, expanded all-in variable cost
components, hybrid monetization, billing workflow Reserve-Settle-Release with
future CreditReservation entity, pricing quote and settlement, and margin policy.

**Note:** Documentation only. No payment gateways, no real provider API calls,
no secrets.

## Purpose

Define how the Persian-first AI Workspace prices AI usage with sustainable unit
economics while keeping billing simple, transparent, and privacy-preserving.

## In Scope

- Business decision for contribution margin and mathematical clarification
- Expanded all-in variable cost components
- Hybrid monetization (Free tier, Wallet/pay-as-you-go, Subscription, Promotional)
- Billing workflow Reserve-Settle-Release with future CreditReservation entity
- Pricing quote and settlement and margin policy clarification

## Out of Scope

- Final pricing numbers and exact credit packages (future, CONFIGURED_LIMIT)
- Real payment gateway integration (ZarinPal Part 3B, crypto Part 3C future)
- Production pricing engine code and final exchange-rate supplier (future)
- Final promotional credit amounts (CONFIGURED_LIMIT pending cost analysis)

## Business Decision: Contribution Margin

- **Target contribution margin is 70%.**
- **Minimum contribution margin for ordinary paid metered operations is 50%.**
- Contribution margin is defined as (selling_price - all_in_variable_cost) /
  selling_price
- Business must maintain at least 50% margin on every ordinary paid metered
  operation to cover fixed costs, support, and profit
- Target of 70% allows buffer for retries, storage, payment fees, and
  promotional credits
- Margins below 50% for ordinary paid operations require product-owner and
  finance approval and must not be silently allowed
- Free-tier, promotional, and subscription operations may have different
  campaign/cohort economics under an explicitly approved budget (separate
  from ordinary paid metered operations)

## Mathematical Clarification

- **Formula:** selling_price = all_in_variable_cost / (1 - target_margin)
- **NON_PRODUCTION_MATH_EXAMPLE:** If all_in_variable_cost = CONFIGURED_VALUE
  and target_margin = 0.70 (70%), then selling_price = CONFIGURED_VALUE /
  (1 - 0.70) = CONFIGURED_VALUE / 0.30. This is a non-production math example
  for illustration only, not a production price.

- All calculations must use decimal arithmetic, not floating point for money
  where possible, or store credits as integer smallest unit
- Use CONFIGURED_ROUNDING_POLICY and CONFIGURED_MINIMUM_BILLABLE_UNIT for
  rounding and minimum billable unit, both are Open Decisions requiring finance
  and owner approval
- Pricing version must be tracked: pricing_version, e.g., v1.0.0, for audit and
  rollback, settlement must use pricing version accepted at reservation time
- Exchange rate handling:
  - Use EXCHANGE_RATE_SNAPSHOT for each quote/reservation, versioned and
    timestamped, stored as snapshot for audit
  - EXCHANGE_RATE_SNAPSHOT source is CONFIGURED_CURRENCY_SOURCE, not a named
    commercial supplier without approval
  - No static production-looking rate such as 190600 Toman per USD as approved
    value; if used in example, label as NON_PRODUCTION_MATH_EXAMPLE
  - Exchange rates must be versioned, timestamped, stored as snapshot for each
    quote/reservation, subject to finance and owner approval

## All-In Variable Cost Components

Expanded list:

- Input tokens: provider input token price per 1K tokens, per model, pricing_version
- Output tokens: provider output token price per 1K tokens
- Cached tokens: cached input at reduced price if provider supports
- Provider-reported reasoning usage: provider-reported reasoning tokens if
  applicable, not internal chain-of-thought
- Embeddings: vector store query, embedding price per 1K tokens or per call
- Reranking: reranking service price per call or per document if used
- Web search: web search API price per search if used for Deep Research
- STT: speech-to-text seconds, provider STT price per second or minute,
  CONFIGURED_LIMIT placeholder
- TTS: text-to-speech seconds, provider TTS price per second
- Image generation/editing: image generation per image, per resolution, editing
  per operation, upscaling, inpainting/outpainting
- Video generation: video generation per second, per resolution, per model
- Storage: uploaded files, generated images/videos, conversation history,
  vector store, per GB per month
- Bandwidth and egress: data transfer out, CDN egress, per GB
- Safety/moderation calls: moderation API price per call if used
- Failed but provider-billed requests: provider may bill even if output not
  usable, must be included in cost accounting
- Expected retries: provider retries due to transient failures, must be included
- Payment fees: payment gateway fee, crypto network fee, exchange rate spread
- Currency-conversion buffer: buffer for exchange rate fluctuation, per
  CONFIGURED_ROUNDING_POLICY
- Provider taxes or fees where applicable: VAT, sales tax, provider service fees
- Other metered variable infrastructure: vector DB query, search, cache, etc.

Do not state or imply that internal chain-of-thought should be requested,
stored, logged, or exposed. Only provider-reported reasoning usage if provider
bills separately for reasoning may be included, not internal model thinking.

## Hybrid Monetization

- **Free tier (abuse-protected):**
  - Limited credits per day/week, rate limited, no bulk, no self-referral
  - Anti-abuse: privacy-preserving account and campaign abuse controls,
    velocity rate limits, fraud review triggers
  - Device fingerprinting is disabled by default
  - VPN or proxy use alone is not a fraud signal
  - No permanent IP tracking
  - Referral and promotional abuse controls must follow
    REFERRAL_AND_PROMOTIONAL_CREDITS.md
  - Additional tracking signals require Privacy, Security, Legal, and Owner
    approval
  - Purpose: activation, referral loop, product-led growth
  - Free tier models: auto_free routing mode, lowest cost models, provider-free
    model status versioned and may expire

- **Wallet/pay-as-you-go:**
  - User buys credit packages, wallet table with balance_credits check >=0,
    ledger_transactions append-only ledger with positive and negative amount
    entries, atomic credit/debit with SELECT FOR UPDATE, idempotency, balance
    never negative enforced at DB and code
  - Credit packages in config: CREDIT_PACKAGES list, exact amounts are
    CONFIGURED_LIMIT placeholders pending provider cost analysis
  - Packages are purchased via payment intents, sandbox-only mock provider
    exists for development and testing, real payment gateways not active,
    sandbox completion must never be enabled in production

- **Subscription entitlements:**
  - Future: monthly subscription that grants entitlements (e.g., CONFIGURED_LIMIT
    credits per month, image generations, video seconds)
  - Entitlements separate from wallet, must not be double-billed
  - No shared consumer accounts, no ToS bypass

- **Promotional credits:**
  - New user promotional and referrer promotional via referral system
  - Not cash and may expire (expiry date CONFIGURED_LIMIT)
  - Separate accounting metadata for promotional vs purchased credits: source,
    expiry, campaign, referral code, is_promotional
  - Usage order: promotional vs purchased vs subscription is Open Decision,
    requires finance review, versioned config

## Billing Workflow: Reserve-Settle-Release (Future Architecture)

The current Wallet and Ledger support posted credit/debit operations. They do
not currently implement pending credit reservations. Do not claim the existing
Wallet already supports pending reservations.

Document a future separate entity: CreditReservation or UsageReservation.

### Proposed Lifecycle

- **quoted:** Quote created with estimated max credits, pricing_version,
  exchange_rate_snapshot, expiration, privacy classification, balance source

- **reserved:** Reservation reduces available balance, not posted ledger balance.
  Available balance = posted balance - sum(reserved not yet settled). Reservation
  created atomically, idempotent, with operation id.

- **executing:** Provider request is executing, actual usage not yet known.

- **settled:** Settlement creates exactly one final usage debit in the
  append-only ledger. Uses pricing version accepted at reservation time. Do not
  retroactively charge different price because Provider Catalog changed while
  request was running.

- **released:** Releasing an unused hold is not a new credit or user income.
  Unused reservation amount is released back to available balance, no new ledger
  credit, only reservation state change to released.

- **expired:** Reservation expired before execution or settlement, e.g., quote
  expiration or scheduled orphan cleanup. Full reservation released.

- **failed:** Provider rejected, timeout, failure, or user cancellation before
  settlement. Reservation released or partially settled per refund policy.

### Required Principles

- Reservation reduces available balance, not the posted ledger balance.
- Settlement creates exactly one final usage debit in the append-only ledger.
- Releasing an unused hold is not a new credit or user income, only release.
- The user must never be debited twice (idempotency, operation id).
- PaymentIntent is for purchasing credits and must not be updated for normal
  AI usage settlement.
- Usage reservation and PaymentIntent are separate domains.
- Reservation, settlement, release, expiry, and failure are idempotent (same
  operation id returns same result).
- Concurrent operations must not make available balance or posted balance
  negative (SELECT FOR UPDATE, atomic checks).
- Reservation expiry and orphan cleanup require a future scheduled process
  (e.g., cron job that releases expired reservations).
- A future database migration is required before this workflow is implemented
  (new table credit_reservations or usage_reservations).

### Failure Behavior

- Provider rejected before execution: release full reservation, state failed,
  no debit, idempotent.
- Timeout with unknown provider result: reconcile before charging again, do not
  double-charge, state remains executing until reconciliation, then settled or
  released per provider actual usage if known.
- Provider failure with no usable output: apply the approved refund policy,
  e.g., release reservation or charge minimal cost for failed but provider-billed
  requests if provider billed, per finance and owner approved policy.
- User cancellation before provider execution: release reservation, state
  released, no debit.
- Retry must reuse the same operation id or create an explicitly linked retry
  (retry_of_operation_id) to avoid double-charging, idempotent.
- Never charge beyond the user-approved maximum without new consent (approved
  estimate or reservation max).

## Credit Lots vs Reservations - Complementary Layers

Required clarification to reconcile Reservation lifecycle with Credit Lot model
from REFERRAL_AND_PROMOTIONAL_CREDITS.md and Reserve-Settle-Release statement in
PROFESSIONAL_PROMPT_ENHANCER.md:

- **A Credit Lot is a balance-tracking construct:** Where credits come from and
  their rules, expiry, scope, source (purchase, promotional_campaign, refund,
  admin_grant), initial_amount, remaining_amount, campaign_id, allowed_scope,
  issued_at, expires_at, non_cashable flag, refundable flag, accounting_class.
  Lots track where credits come from and their rules.

- **A Reservation/Settlement is a transaction-tracking construct:** How a specific
  operation holds and then consumes credits. Lifecycle quoted, reserved,
  executing, settled, released, expired, failed. Reservation reduces available
  balance, not posted ledger balance. Settlement creates exactly one final usage
  debit in append-only ledger.

- **A single operation may draw from one or more active Credit Lots:** According
  to the (still Open Decision) consumption order policy (e.g., promotional first
  vs purchased first), but must always go through the Reservation lifecycle for
  atomicity. Available balance = sum of remaining_amount across active lots.
  Expired lots are closed and not treated as user income or refunds.

- **These are complementary layers, not competing systems:** Credit Lots track
  balance origin and rules; Reservations track transaction holds and consumption.
  Ledger remains single append-only source of truth. PaymentIntent is for
  purchasing credits and must not be updated for normal AI usage settlement.
  Usage reservation and PaymentIntent are separate domains.

Cross-linked from:
- REFERRAL_AND_PROMOTIONAL_CREDITS.md defines Credit Lots
- PROFESSIONAL_PROMPT_ENHANCER.md uses Reserve-Settle-Release for enhancer cost

## Define One Consistent Balance Model

Replace ambiguous or conflicting available-balance formulas with:

- **gross_eligible_lot_balance =** sum of remaining amounts in active, eligible
  Credit Lots

- **active_reserved_amount =** sum of active, unreleased Reservation Allocations

- **available_spendable_balance =** gross_eligible_lot_balance -
  active_reserved_amount

Clarify:

- A Reservation may allocate its hold across one or more Credit Lots
- A future ReservationAllocation entity records:
  - reservation_id
  - credit_lot_id
  - reserved_amount
  - settled_amount
  - released_amount
  - status
- Reservation does not create a posted Ledger debit
- Settlement creates exactly one final usage debit
- Settlement consumes the allocated Credit Lots atomically
- Release removes the hold without creating a Ledger credit
- Available balance must never become negative

## Define The Financial Source of Truth

State clearly:

- The append-only Ledger is the authoritative source of posted financial
  transactions
- Credit Lots are the authoritative allocation layer for source, expiry,
  allowed scope, non-cashable status, and consumption eligibility
- Credit Lot remaining amounts must not become an unrelated second balance
- Ledger posting, Credit Lot consumption, and Reservation settlement must occur
  atomically in one database transaction
- Credit Lot remaining amounts must be derivable or reconcilable from issuance
  and consumption records
- A future reconciliation process must compare:
  - posted wallet balance
  - Ledger totals
  - Credit Lot totals
  - active Reservation Allocations
- Any mismatch must create a financial security alert
- The required database entities and reconciliation process are not implemented
  yet and require future migrations and tests

## Pricing Quote and Settlement

### User Quote Must Include

- Operation type: e.g., chat, image generation, video generation, STT, TTS,
  embeddings, web search, reranking
- Provider/model or routing policy: e.g., provider_a/model_a or
  auto_balanced, manual_model_selection
- Estimated maximum credits: based on max tokens, image/video units, etc.
- Pricing_version: version of Model Catalog pricing used for quote
- Exchange_rate_snapshot: EXCHANGE_RATE_SNAPSHOT, versioned, timestamped,
  stored as snapshot for audit, source CONFIGURED_CURRENCY_SOURCE
- Quote expiration: quote_expiration: CONFIGURED_QUOTE_EXPIRATION, after expiry
  quote invalid
  - Example: CONFIGURED_QUOTE_EXPIRATION with CONFIGURED_LIMIT placeholder
- Privacy classification: e.g., privacy_preferred, standard, requires policy
  evidence
- Whether promotional, subscription, or purchased balance will be used: source
  of balance, promotional expiry, subscription entitlements

### Settlement Must Use Pricing Version Accepted at Reservation Time

- Settlement must use the pricing version accepted at reservation time
  (pricing_version from quote/reservation).
- Do not retroactively charge a different price because the Provider Catalog
  changed while the request was running (e.g., provider price increase during
  execution).
- Exchange rate snapshot from quote must be used for settlement, not current
  rate, unless explicitly approved and disclosed.

### Margin Policy Clarification

Owner-approved provisional business target:

- Target contribution margin: 70%
- Minimum contribution margin for ordinary paid metered operations: 50%

Pending validation:

- actual provider costs
- all-in variable cost measurement
- finance review
- cohort economics
- periodic owner review

Free-tier, promotional, and subscription operations may have different
campaign/cohort economics under an explicitly approved budget (e.g., free tier
platform-subsidized budget, promotional campaign budget, subscription
entitlement budget).

No unapproved negative-margin route may be activated silently. All negative
margin or below-minimum-margin routes require product-owner, finance, and
owner approval and must be explicitly documented as campaign/cohort economics,
not ordinary paid metered operations.

Do not list the existence of the 70%/50% target itself as an unresolved
Open Decision. The target is Owner-approved provisional, pending validation
above.

## Related Documents

- Multi-Provider Routing: [MULTI_PROVIDER_MODEL_ROUTING.md](MULTI_PROVIDER_MODEL_ROUTING.md)
- Referral and Promotional Credits: [REFERRAL_AND_PROMOTIONAL_CREDITS.md](REFERRAL_AND_PROMOTIONAL_CREDITS.md)
- Professional Prompt Enhancer: [PROFESSIONAL_PROMPT_ENHANCER.md](PROFESSIONAL_PROMPT_ENHANCER.md)
- Security Index: [../security/README.md](../security/README.md)
- Secrets and Key Management: [../security/SECRETS_AND_KEY_MANAGEMENT.md](../security/SECRETS_AND_KEY_MANAGEMENT.md)
- Prompt Injection Defense: [../security/PROMPT_INJECTION_DEFENSE.md](../security/PROMPT_INJECTION_DEFENSE.md)
- Agent Security Model: [../security/AGENT_SECURITY_MODEL.md](../security/AGENT_SECURITY_MODEL.md)
- Provider Abstraction: [PROVIDER_ABSTRACTION_STRATEGY.md](PROVIDER_ABSTRACTION_STRATEGY.md)
- Agent Plugin and Execution: [AGENT_PLUGIN_AND_EXECUTION_SYSTEM.md](AGENT_PLUGIN_AND_EXECUTION_SYSTEM.md)
- Data Classification: [DATA_CLASSIFICATION_AND_RETENTION.md](DATA_CLASSIFICATION_AND_RETENTION.md)
- Wallet and Payments: WALLET_AND_PAYMENTS.md (planned, future - not clickable yet)

## Open Decisions

- Exact target and minimum contribution margin numbers (70% target, 50% minimum
  for ordinary paid, requires finance and owner approval)
- All-in variable cost components and pricing_version per model
- Credit package amounts and EXCHANGE_RATE_SNAPSHOT source
  (CONFIGURED_CURRENCY_SOURCE) and CONFIGURED_ROUNDING_POLICY and
  CONFIGURED_MINIMUM_BILLABLE_UNIT
- Free tier limits and abuse protection thresholds (CONFIGURED_LIMIT)
- Subscription entitlement amounts and pricing (future)
- Promotional credit expiry and usage order (first vs last) and allowed model
  scope (Open Decision)
- Reserve-Settle-Release: CreditReservation table schema, scheduled orphan cleanup,
  future migration, idempotency, failure handling, refund policy
- Quote fields and expiration and settlement using accepted pricing version
- Owner, finance, security, privacy, legal approval required for all decisions

## Planned Completion Stage

Phase 1 - Pricing and Unit Economics

## Status Note

Proposed Architecture - Pending Owner, Finance, Security, and Compliance Approval.
Will be completed later with product, finance, security, and owner review.
No real payment gateways in this PR.

## ADR-0002 Phase 1 Credit Pricing

User-facing billing unit is credits. Credits are the only Phase 1 billing unit;
real fiat pricing is deferred. See [ADR-0002](../decisions/0002-phase-1-product-metering-and-infrastructure.md).

| Feature | Credit Cost | Billing Model |
|---|---|---|
| General Chat | 1, 2, or 3 credits | Tiered by Token Budget Manager |
| Prompt Enhancer | 2 credits | Fixed per enhancement |
| Caption Generator (initial) | 5 credits | Fixed per generation (3 variations) |
| Caption Generator (regenerate) | 5 credits | New billable request |
| Copy / Read History | 0 credits | Free |

## Quote-Before-Execution Policy
The estimate is shown before execution and accepted quote is maximum charge. The
platform never settles above quote. Phase 1 absorbs unexpected provider variance
and records pricing-variance metadata.

## Internal Cost Metering
Internal tracking uses provider-reported prompt, completion, reasoning, cached
tokens and cost. OpenRouter usage data is separate from user credits and informs
future fiat pricing.

## Sandbox Credit Packages
100 credits, 500 credits, and 2,000 credits are sandbox packages. No fiat price is
approved in Phase 1.

## Deferred
Chat tier boundaries, estimation, and cost multipliers are D2. Real currency pricing
is deferred beyond D2.
