# Referral and Promotional Credit System

**Version:** v0.1.0

**Date:** 2026-07-24

**Status:** Draft - Structure Only

**Document Owner:** Growth and Product Architect

**Purpose:** Define unique referral code per eligible user, new user and referrer
promotional credits, abuse protection, fraud review triggers, promotional credit
accounting, and CONFIGURED_LIMIT placeholders for credit amounts.

**Note:** Documentation only. No payment gateways, no real provider calls.

## Purpose

Establish a referral loop and promotional credit system that is abuse-protected,
fraud-resistant, and financially sustainable with clear accounting separation
between promotional and purchased credits.

## In Scope

- Unique referral code per eligible user
- New user promotional credit and referrer promotional credit
- Abuse protection, fraud review triggers, promotional credits not cash and may
  expire, separate accounting metadata, CONFIGURED_LIMIT placeholders

## Out of Scope

- Final credit amounts and exact promotional campaign rules (future,
  CONFIGURED_LIMIT pending cost analysis)
- Real payment gateway integration (future)
- Production referral engine code (future PRs)

## Unique Referral Code per Eligible User

- Each eligible user gets a unique referral code, e.g., `user_id` + random suffix,
  or short code like 6-8 alphanumeric characters, collision-free, case-insensitive
- Code generation must be atomic and idempotent, unique index in database table
  `referral_codes` with fields: id, user_id (owner), code (unique), created_at,
  is_active, usage_count, max_usage (CONFIGURED_LIMIT)
- Eligibility: user must have completed onboarding, first chat, maybe purchased
  credits or completed activation, not banned, not flagged for abuse
- Code must be easy to share: link `https://platform.com/r/{code}` and code itself
- Referral code must not expose raw user id, email, or phone number, use hashed
  or random code

## New User Promotional Credit and Referrer Promotional Credit

- New user promotional credit: when new user signs up via referral link/code and
  completes activation (e.g., first chat, onboarding), both new user and referrer
  get promotional credits
- Referrer promotional credit: existing user who referred new user gets credit
  after new user activation, not just signup, to prevent farming
- Both credits are promotional, not cash, may expire (e.g., 30 days, 60 days)
- Separate accounting metadata for promotional vs purchased credits: source
  (referral, campaign, admin grant), campaign_id, referral_code, referrer_user_id,
  expiry_date, is_expired, used_first_or_last policy
- Example flow:

  1. User A gets referral code `ABC123`, shares link
  2. User B clicks link, signs up, completes onboarding and first chat
  3. System checks abuse protection: no self-referral, no device farming,
     velocity rate limits, fraud review triggers
  4. If passes, create promotional credit ledger entries:
     - New user B: promotional credit CONFIGURED_LIMIT, source referral,
       expiry 30 days
     - Referrer A: promotional credit CONFIGURED_LIMIT, source referral,
       expiry 30 days
  5. Increment referral_codes usage_count atomically
  6. Log audit metadata: referrer_user_id pseudonymous, new_user_id pseudonymous,
     referral_code, campaign, timestamps, not raw sensitive content

## Abuse Protection

- No self-referral: user cannot refer themselves, cannot use own code, check
  user_id != referrer_user_id, check device fingerprint, IP, email domain
- Device/account farming prevention: device fingerprinting, IP velocity checks,
  email domain rate limits, phone number verification if used, CAPTCHA if needed,
  no bulk creation of accounts from same device/IP within CONFIGURED_LIMIT window
- Velocity rate limits: max referrals per user per day/week CONFIGURED_LIMIT,
  max signups per IP per hour CONFIGURED_LIMIT, max promotional credits per
  device per month CONFIGURED_LIMIT
- Fraud review triggers:
  - Unusual spike in referral code usage above CONFIGURED_LIMIT
  - Multiple accounts from same device/IP/email domain
  - Disposable email domains
  - VPN/proxy usage for farming
  - Referral code used by user who shares same payment method
  - New user activation without real usage (e.g., no chat, no wallet activity)
- Promotional credits are not cash and may expire: expiry date, e.g., 30 days,
  60 days, 90 days, after expiry balance not usable, ledger entry for expiry
- Separate accounting metadata for promotional vs purchased credits: source,
  expiry, campaign, referral_code, is_promotional boolean, used tracking

## Fraud Review Triggers and Handling

- Automatic flag: if referral code usage exceeds CONFIGURED_LIMIT per day, or
  if same device/IP creates more than CONFIGURED_LIMIT accounts per day, flag
  for review
- Manual review: growth and security team reviews flagged referrals, checks
  device fingerprint, IP, email, payment method, usage patterns
- Actions on fraud confirmed:
  - Revoke promotional credits (ledger entry with negative promotional credit,
    not affecting purchased credits)
  - Ban referral code (is_active false)
  - Ban user accounts if severe, with audit trail, human approval required
  - No auto-banning without human approval for high-impact actions
- Audit logging: fraud review actions logged with metadata only, no raw
  sensitive content, tamper-resistant

## Promotional vs Purchased Credits Accounting

- Promotional credits:
  - Source: referral, campaign, admin grant, onboarding bonus
  - Not cash, may expire, not withdrawable, not transferable
  - May have restrictions: e.g., cannot be used for certain high-cost models,
    or can only be used for chat, not studio, or vice versa – Open Decision
  - Expiry: 30 days default, configurable per campaign, CONFIGURED_LIMIT placeholder
- Purchased credits:
  - Source: payment intent completed via sandbox mock provider (current) or real
    ZarinPal/crypto future
  - Not expiring (or long expiry), cash-equivalent for billing, but still credits
    not cash, balance never negative
  - No expiry unless explicitly stated, audit trail

- Separate accounting metadata:
  - ledger_transactions table with fields: id, user_id, amount (positive for credit,
    negative for debit), type (purchase, promotional, referral, refund, expiry),
    source, campaign_id, referral_code, expiry_date, is_promotional boolean,
    created_at, idempotency_key
  - Wallet table with balance_credits check >=0, but promotional and purchased
    credits may be tracked separately via ledger, not just balance
  - Exact accounting for promotional vs purchased credits usage order: e.g.,
    promotional credits used first or last? Open Decision, requires finance and
    product-owner review, must be documented and versioned

## Exact Credit Amounts as CONFIGURED_LIMIT Placeholders

- Exact credit amounts are CONFIGURED_LIMIT placeholders pending provider cost
  analysis
- Example: new user promotional credit = CONFIGURED_LIMIT credits, referrer
  promotional credit = CONFIGURED_LIMIT credits
- Must not hardcode values like 100 credits for referral, 50 credits for new user
  as production-approved without finance and owner approval
- Use placeholders and state clearly: Exact credit amounts are Open Decisions
  and must not be treated as production-approved values, require provider cost
  analysis, finance and owner approval, versioned config

## Related Documents

- Security Index: [../security/README.md](../security/README.md)
- Multi-Provider Routing: [MULTI_PROVIDER_MODEL_ROUTING.md](MULTI_PROVIDER_MODEL_ROUTING.md)
- Pricing and Unit Economics: [PRICING_AND_UNIT_ECONOMICS.md](PRICING_AND_UNIT_ECONOMICS.md)
- Wallet and Payments: WALLET_AND_PAYMENTS.md (planned, future - not clickable yet)
- Agent Security Model: [../security/AGENT_SECURITY_MODEL.md](../security/AGENT_SECURITY_MODEL.md)
- Data Classification: [DATA_CLASSIFICATION_AND_RETENTION.md](DATA_CLASSIFICATION_AND_RETENTION.md)

## Open Decisions

- Exact credit amounts for new user and referrer (CONFIGURED_LIMIT placeholders)
- Referral code format and length and generation method
- Eligibility criteria for referral code and for receiving promotional credits
- Abuse protection thresholds (CONFIGURED_LIMIT) and fraud review triggers
- Promotional credit expiry period and usage order (first vs last)
- Whether promotional credits can be used for all models or restricted
- Owner, finance, growth, and security approval required for all decisions

## Planned Completion Stage

Phase 1 - Referral and Growth

## Status Note

Draft - Structure Only. Will be completed later with product, finance, growth,
security, and owner review. No real payment gateways in this PR.
