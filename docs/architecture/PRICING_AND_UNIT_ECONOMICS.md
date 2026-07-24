# Pricing, Profit, Wallet, and Unit Economics

**Version:** v0.1.0

**Date:** 2026-07-24

**Status:** Draft - Structure Only

**Document Owner:** Product Architect / Finance

**Purpose:** Define business decision for target contribution margin, mathematical
clarification of selling price, all-in variable cost components, hybrid
monetization, and billing workflow Reserve-Settle-Refund.

**Note:** Documentation only. No payment gateways, no real provider API calls,
no secrets.

## Purpose

Define how the Persian-first AI Workspace prices AI usage with sustainable
unit economics while keeping billing simple and transparent.

## In Scope

- Business decision for contribution margin, mathematical clarification,
  all-in variable cost components, hybrid monetization, billing workflow
- Wallet, ledger, payment intent foundations already implemented
- Credit-based billing, atomic and idempotent, balance never negative

## Out of Scope

- Final pricing numbers and exact credit packages (future, CONFIGURED_LIMIT)
- Real payment gateway integration (ZarinPal Part 3B, crypto Part 3C future)
- Production pricing engine code (future PRs)
- Final promotional credit amounts (CONFIGURED_LIMIT pending cost analysis)

## Business Decision: Contribution Margin

- **Target contribution margin is 70%.**
- **Minimum contribution margin is 50%.**
- Contribution margin is defined as (selling_price - all_in_variable_cost) /
  selling_price
- Business must maintain at least 50% margin on every billable AI operation
  to cover fixed costs, support, and profit
- Target of 70% allows buffer for retries, storage, payment fees, and
  promotional credits
- Margins below 50% require product-owner and finance approval and must not be
  silently allowed

## Mathematical Clarification

- **Formula:** selling_price = all_in_variable_cost / (1 - target_margin)
- Example: if all_in_variable_cost = $0.03 and target_margin = 0.70 (70%),
  then selling_price = 0.03 / (1 - 0.70) = 0.03 / 0.30 = $0.10
- If target_margin = 50% (minimum), selling_price = all_in_variable_cost /
  (1 - 0.50) = all_in_variable_cost / 0.50 = 2x cost
- All calculations must use decimal arithmetic, not floating point for money
  where possible, or store credits as integer smallest unit
- Pricing version must be tracked: pricing_version, e.g., v1.0.0, for audit
- Exchange rate for display: static 190600 Toman per USD for MVP, later
  real-time rate from Bonbast or Arzbin (future)

## All-In Variable Cost Components

- Input tokens: provider input token price per 1K tokens, per model,
  pricing_version tracked
- Output tokens: provider output token price per 1K tokens, includes reasoning
  tokens if applicable (e.g., chain-of-thought)
- Cached tokens: cached input at reduced price if provider supports
- Reasoning tokens: for models that bill separately for reasoning
- Embeddings: vector store query, embedding price per 1K tokens or per call
- STT seconds: speech-to-text seconds, provider STT price per second or minute
- TTS seconds: text-to-speech seconds, provider TTS price
- Image units: image generation per image, per resolution, per model
- Video units: video generation per second, per resolution, per model
- Storage: uploaded files, generated images/videos, conversation history,
  vector store, per GB per month
- Retries: provider retries due to transient failures, must be included in cost
- Payment fees: ZarinPal fee, crypto network fee, exchange rate spread, future

## Hybrid Monetization

- **Free tier (abuse-protected):**
  - Limited credits per day/week, rate limited, no bulk
  - Anti-abuse: device/account farming prevention, velocity rate limits,
    no self-referral, fraud review triggers
  - Purpose: activation, referral loop, product-led growth
  - Free tier models: auto_free routing mode, lowest cost models

- **Wallet/pay-as-you-go:**
  - User buys credit packages, wallet table with balance_credits check >=0,
    ledger_transactions append-only ledger with positive and negative amount
    entries, atomic credit/debit with SELECT FOR UPDATE, idempotency,
    balance never negative enforced at DB and code
  - Credit packages in config: CREDIT_PACKAGES list, exact amounts are
    CONFIGURED_LIMIT placeholders pending provider cost analysis
  - Packages are purchased via payment intents, sandbox mock provider only in
    Part 3A, real ZarinPal Part 3B and crypto Part 3C future

- **Subscription entitlements:**
  - Future: monthly subscription that grants entitlements (e.g., X credits per
    month, Y image generations, Z video seconds, access to certain personas)
  - Entitlements are separate from wallet, must not be double-billed
  - Subscription is not shared consumer accounts, no reselling, no ToS bypass

- **Promotional credits:**
  - New user promotional credit and referrer promotional credit via referral
    system (see REFERRAL_AND_PROMOTIONAL_CREDITS.md)
  - Promotional credits are not cash and may expire (expiry date, e.g., 30 days)
  - Separate accounting metadata for promotional vs purchased credits: source,
    expiry, campaign, referral code
  - Promotional credits used first or last? Open Decision, requires finance
    review, must be documented and versioned

## Billing Workflow (Reserve-Settle-Refund)

This workflow ensures atomic and idempotent billing, balance never negative,
and accurate settlement based on actual provider usage.

1. **Estimate max cost:**
   - Based on model, max tokens, image/video units, estimated STT/TTS, storage
   - Use Model Catalog: input/output token price, pricing_version

2. **Reserve credits atomically (using existing wallet features):**
   - SELECT FOR UPDATE wallet row, check balance >= estimated max cost
   - If insufficient, return error with required credits, do not execute provider
   - Create ledger entry with pending reservation, idempotency key

3. **Execute provider request:**
   - Call provider abstraction with provider-neutral config mapped from Accuracy
     and Creativity mode
   - Track actual usage: input/output tokens, cached tokens, reasoning tokens,
     embeddings, STT/TTS seconds, image/video units

4. **Measure actual usage:**
   - Provider returns usage: tokens, embeddings, seconds, units
   - Calculate all_in_variable_cost based on actual usage and Model Catalog
     pricing_version

5. **Settle credits:**
   - Calculate selling_price = all_in_variable_cost / (1 - target_margin)
   - Deduct actual selling_price from wallet atomically
   - Create ledger entry with settled cost, provider_id, model_id, prompt hash
     replaced with content_fingerprint DISABLED_BY_DEFAULT per privacy hardening
   - Update payment intent with actual cost if applicable

6. **Refund unused reservation:**
   - Refund = estimated max cost - actual selling_price
   - If refund > 0, credit wallet atomically
   - Create ledger entry for refund, idempotency
   - If actual cost > estimated max due to provider returning more tokens than
     estimated, handle as overage: either allow small overage within buffer or
     require re-reservation, must not make balance negative, requires product
     and finance review

- All steps must be atomic and idempotent, balance never negative, ledger
  append-only, audit metadata only by default (pseudonymous user id, agent id,
  provider id, model id, token counts, cost, timestamps, not raw sensitive
  content)

## Related Documents

- Security Index: [../security/README.md](../security/README.md)
- Multi-Provider Routing: [MULTI_PROVIDER_MODEL_ROUTING.md](MULTI_PROVIDER_MODEL_ROUTING.md)
- Wallet and Payments: WALLET_AND_PAYMENTS.md (planned, future - not clickable yet)
- Referral and Promotional Credits: [REFERRAL_AND_PROMOTIONAL_CREDITS.md](REFERRAL_AND_PROMOTIONAL_CREDITS.md)
- Provider Abstraction: [PROVIDER_ABSTRACTION_STRATEGY.md](PROVIDER_ABSTRACTION_STRATEGY.md)
- Agent Plugin and Execution: [AGENT_PLUGIN_AND_EXECUTION_SYSTEM.md](AGENT_PLUGIN_AND_EXECUTION_SYSTEM.md)
- Data Classification: [DATA_CLASSIFICATION_AND_RETENTION.md](DATA_CLASSIFICATION_AND_RETENTION.md)

## Open Decisions

- Exact target and minimum contribution margin numbers (currently 70% target,
  50% minimum, requires finance and owner approval)
- All-in variable cost components and pricing_version per model
- Credit package amounts and exchange rate real-time source (CONFIGURED_LIMIT)
- Free tier limits and abuse protection thresholds (CONFIGURED_LIMIT)
- Subscription entitlement amounts and pricing (future)
- Promotional credit expiry and usage order (first vs last)
- Reserve-Settle-Refund buffer for overage handling
- Owner and finance approval required for all decisions

## Planned Completion Stage

Phase 1 - Pricing and Unit Economics

## Status Note

Draft - Structure Only. Will be completed later with product, finance, security,
and owner review. No real payment gateways in this PR.
