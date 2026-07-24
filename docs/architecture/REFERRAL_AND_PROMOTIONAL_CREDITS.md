# Referral and Promotional Credit System

**Version:** v0.1.0

**Date:** 2026-07-24

**Status:** Proposed Architecture - Pending Owner, Privacy, Security, Finance,
and Compliance Approval

**Document Owner:** Growth and Product Architect / Privacy

**Purpose:** Define privacy-first referral and promotional credit system with
unique random opaque referral codes, abuse protection without invasive tracking,
credit buckets/lots future architecture, and legal and security requirements.

**Note:** Documentation only. No payment gateways, no real provider calls.

## Purpose

Establish a referral loop and promotional credit system that is abuse-protected,
fraud-resistant, privacy-first, and financially sustainable with clear
accounting separation between promotional and purchased credits.

## In Scope

- Unique random opaque referral code per eligible user
- New user and referrer promotional credits with privacy-preserving fraud controls
- Promotional credit accounting via Credit Buckets or Credit Lots future
  architecture
- Abuse protection without invasive tracking, fraud review, legal notes

## Out of Scope

- Final credit amounts and exact promotional campaign rules (future,
  CONFIGURED_LIMIT pending cost analysis)
- Real payment gateway integration (future)
- Production referral engine code and final fraud detection implementation
  (future PRs)

## Unique Referral Code per Eligible User

- Each eligible user gets a unique referral code that is fully random and opaque
- Code generation must be atomic and idempotent, unique index in database table
  `referral_codes` with fields: id, user_id (owner), code (unique random opaque),
  created_at, is_active, usage_count, max_usage (CONFIGURED_LIMIT),
  expires_at, revoked_at
- Eligibility: user must have completed onboarding, first chat, maybe purchased
  credits or completed activation, not banned, not flagged for abuse
- Code must be easy to share: link `https://platform.com/r/{code}` and code itself,
  QR code optional

## Referral Code Format

New required rules to fix contradiction where code was derived from user_id but
also must not reveal user_id:

- Referral codes must be fully random and opaque
- Referral codes must never contain, encode, or derive from user_id, email,
  phone number, name, or account creation timestamp
- No portion of code may be user_id substring, email prefix, phone suffix,
  or timestamp
- Code length and character set are CONFIGURED_LIMIT and must be chosen after
  abuse-rate and collision analysis (e.g., length CONFIGURED_LIMIT, charset
  alphanumeric without ambiguous characters, case-insensitive)
- Codes must be unique: unique index, collision check, retry on collision
- Codes must be revocable: is_active false, revoked_at timestamp, audit log
- Codes must be rotatable: user can request new code, old code revoked,
  new code generated random opaque, no link to old code
- Codes must not be guessable from other public account attributes: no
  sequential codes, no user_id + random suffix, no email prefix + random,
  must be cryptographically random, sufficient entropy

## New User Promotional Credit and Referrer Promotional Credit

- New user promotional credit: when new user signs up via referral link/code and
  completes activation (e.g., first chat, onboarding, verified basic
  authentication), both new user and referrer get promotional credits
- Referrer promotional credit: existing user who referred new user gets credit
  after new user activation, not just signup, to prevent farming
- Both credits are promotional, not cash and never withdrawable, may expire
- Separate accounting metadata for promotional vs purchased credits: source
  (referral, campaign, admin_grant), campaign_id, referral_code,
  referrer_user_id pseudonymous, expiry_date, is_expired, allowed_scope,
  non_cashable flag
- Example flow:

  1. User A gets referral code random opaque, e.g., `X7K9P2`, shares link
  2. User B clicks link, signs up, completes onboarding and first chat and
     verified basic authentication
  3. System checks abuse protection: no self-referral, velocity rate limits
     per account and per campaign, reward caps, manual review for anomalies
     above CONFIGURED_LIMIT
  4. If passes, create promotional credit lots:
     - New user B: promotional credit CONFIGURED_LIMIT, source referral,
       campaign_id, expiry CONFIGURED_LIMIT
     - Referrer A: promotional credit CONFIGURED_LIMIT, source referral,
       campaign_id, expiry CONFIGURED_LIMIT
  5. Increment referral_codes usage_count atomically
  6. Log audit metadata: referrer_user_id pseudonymous, new_user_id pseudonymous,
     referral_code, campaign_id, timestamps, not raw sensitive content, no
     invasive tracking identifiers

## Privacy-First Fraud Controls

The current Referral document previously used invasive fraud controls that
conflict with platform's privacy-first commitments. Remove or restrict the
following as default fraud signals:

- Device fingerprinting: must not be used by default, no collection of device
  attributes, canvas fingerprinting, or persistent device ids for referral
- Long-lived IP tracking: no permanent IP retention, no building IP history
  for user profiling
- Phone number linkage as an identity signal: phone numbers must not be used as
  Referral identity signal beyond normal account authentication (e.g., OTP for
  signup, but not for linking referrals)
- Email domain profiling as a fraud signal: email domain must not be used as
  fraud signal (e.g., disposable domain list is not a fraud signal by itself)
- Payment method fingerprinting: payment method details must not be used as
  Referral fraud signal (payment method may be used for payment fraud, not
  referral fraud)
- Treating VPN or proxy use as a fraud signal: VPN or proxy use alone must never
  be a fraud signal, ban reason, or automatic reward denial

Replace with a privacy-preserving default model:

- No device fingerprinting by default
- No permanent IP retention
- If IP is used for short-term abuse detection, it must be handled with keyed
  HMAC using a rotatable secret, retained for minimum necessary time (e.g.,
  CONFIGURED_LIMIT hours), and never used for user profiling
- VPN or proxy use alone must never be a fraud signal, ban reason, or automatic
  reward denial
- Phone numbers must not be used as a Referral identity signal beyond normal
  account authentication
- Payment method details must not be used as a Referral fraud signal
- Any expansion of fraud signals is an Open Decision and requires Privacy,
  Security, Legal, and Owner approval

Allowed baseline signals:

- Account age of the referred user: e.g., new account created within
  CONFIGURED_LIMIT hours may need additional verification, but not automatic denial
- Verified basic authentication requirements: e.g., email verified, basic
  onboarding completed, first chat completed
- Velocity rate limits per account and per campaign: max referrals per user per
  day/week CONFIGURED_LIMIT, max signups per campaign per hour CONFIGURED_LIMIT
- Reward caps per user and per campaign: max promotional credits per user per
  month CONFIGURED_LIMIT, max total campaign budget CONFIGURED_LIMIT
- Manual review for anomalies above CONFIGURED_LIMIT: unusual spike in referral
  code usage, multiple accounts created in short time from same campaign,
  etc.

Human oversight:

- Any automatic denial or reward reversal must be appealable (user can appeal,
  provide additional verification, human review)
- Fraud decisions above CONFIGURED_LIMIT require human review (e.g., banning
  referral code, revoking promotional credits, banning user accounts)
- Audit records for referral decisions must not contain raw sensitive content
  or invasive tracking identifiers (e.g., no raw IP, no device fingerprint, no
  phone number, no payment method details, only pseudonymous user ids, HMAC of
  IP if needed for short-term abuse detection, campaign_id, timestamps, result)

## Promotional Credit Accounting

The current Wallet stores a single balance and does not separate promotional and
purchased credits. Do not claim the existing wallet already tracks separate
credit types.

Document a future architecture using either Credit Buckets or Credit Lots:

- Each Lot has:
  - lot_id: unique identifier, UUID
  - source: purchase, promotional_campaign, refund, admin_grant
  - initial_amount: decimal, e.g., CONFIGURED_LIMIT credits
  - remaining_amount: decimal, e.g., CONFIGURED_LIMIT credits remaining
  - campaign_id (if applicable): e.g., referral campaign, onboarding campaign
  - allowed_scope: models, features, channels allowed, e.g., chat only, or all
  - issued_at: DateTime
  - expires_at: DateTime, e.g., CONFIGURED_LIMIT days after issued_at
  - non_cashable flag: true for promotional, true for purchased (non-withdrawable)
  - refundable flag: true for purchased, false for promotional
  - accounting_class: e.g., promotional, purchased, refund, admin_grant

- Consumption rules:
  - Ledger remains the single append-only source of truth (ledger_transactions
    append-only ledger with positive and negative amount entries, atomic
    credit/debit with SELECT FOR UPDATE, balance never negative)
  - Available balance = sum of remaining_amount across active lots (active means
    not expired, not fully consumed, is_active true)
  - Consumption order between promotional and purchased lots is an Open Decision
    requiring Finance and Owner approval (e.g., promotional first vs purchased
    first, or user choice, or campaign policy)
  - Expired lots are closed and are not treated as user income or refunds
    (expiry is not credit, not income, just closure of lot)
  - Purchased credits must not be described as cash equivalent (they are internal
    platform credits, non-transferable, non-withdrawable, governed by approved
    Refund Policy)
  - Promotional credits are never cash and never withdrawable (non_cashable true,
    non-withdrawable, may expire)

- Removal of unapproved numeric defaults:
  - Remove specific credit amounts, e.g., 100 credits for referral, 50 for new user
  - Remove expiration days, e.g., 30 days, 60 days, 90 days as approved values
  - Remove code lengths, e.g., 6-8 alphanumeric characters as approved
  - Remove reward tiers
  - Replace with CONFIGURED_LIMIT placeholders
  - Any mathematical example must be labeled NON_PRODUCTION_MATH_EXAMPLE

## Referral Security and Legal Notes

Add explicit requirements:

- Referral rewards must be granted through the same append-only ledger used for
  all credit operations (ledger_transactions, idempotency, atomic, balance never
  negative)
- Reward issuance must be idempotent (same referral event with same operation id
  returns same result, no duplicate lots, no double credit)
- Reward issuance must not bypass the wallet's atomic constraints (SELECT FOR
  UPDATE, available balance check, no negative balance)
- Reward issuance must not create negative balances or duplicate lots (check
  available balance, check lot existence by operation id)
- Any bulk issuance requires human approval and audit logging (e.g., campaign
  with 1000 users, admin grant, manual review, approval gate)
- Cross-tenant leakage of referral data is prohibited (user A must not see
  user B's referral code usage, referral codes are private to owner, audit logs
  pseudonymous)
- Public campaign copy must not misrepresent legal terms (e.g., must not say
  promotional credits are cash, must not say referral creates employment, must
  clearly state expiry and non-cashable)
- Referral does not create employment, agency, or investment relationship
- Compliance review is required for any monetary or cash-equivalent
  interpretation of promotional credits (e.g., if promotional credits could be
  considered cash equivalent in some jurisdiction, legal review required)

## Related Documents

- Security Index: [../security/README.md](../security/README.md)
- Multi-Provider Routing: [MULTI_PROVIDER_MODEL_ROUTING.md](MULTI_PROVIDER_MODEL_ROUTING.md)
- Pricing and Unit Economics: [PRICING_AND_UNIT_ECONOMICS.md](PRICING_AND_UNIT_ECONOMICS.md)
- Wallet and Payments: WALLET_AND_PAYMENTS.md (planned, future - not clickable yet)
- Agent Security Model: [../security/AGENT_SECURITY_MODEL.md](../security/AGENT_SECURITY_MODEL.md)
- Data Classification: [DATA_CLASSIFICATION_AND_RETENTION.md](DATA_CLASSIFICATION_AND_RETENTION.md)
- Channel Security: [../security/CHANNEL_SECURITY_TELEGRAM_WEB_MOBILE.md](../security/CHANNEL_SECURITY_TELEGRAM_WEB_MOBILE.md)

## Open Decisions

- Exact credit amounts for new user and referrer (CONFIGURED_LIMIT placeholders)
- Referral code format: length CONFIGURED_LIMIT, character set CONFIGURED_LIMIT,
  generation method cryptographically random, collision analysis
- Eligibility criteria for referral code and for receiving promotional credits
- Abuse protection thresholds (CONFIGURED_LIMIT) and fraud review triggers and
  privacy-preserving model details
- Promotional credit expiry period and usage order (first vs last) and allowed
  scope and accounting_class
- Credit Buckets vs Credit Lots architecture and Lot fields and consumption order
- Fraud signals expansion: any expansion requires Privacy, Security, Legal,
  Owner approval (Open Decision)
- Referral code randomness: fully random and opaque, never contains user_id, email,
  phone, name, timestamp, not guessable
- Owner, privacy, finance, growth, security, legal, compliance approval required
  for all decisions

## Planned Completion Stage

Phase 1 - Referral and Growth

## Status Note

Proposed Architecture - Pending Owner, Privacy, Security, Finance, and Compliance
Approval. Will be completed later with product, finance, growth, security, privacy,
legal, and owner review. No real payment gateways in this PR.
