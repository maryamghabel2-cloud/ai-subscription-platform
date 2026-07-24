# Multi-Provider and Model Routing Architecture

**Version:** v0.1.0

**Date:** 2026-07-24

**Status:** Proposed Architecture - Pending Owner, Finance, Security, and
Compliance Approval

**Document Owner:** AI Platform Architect

**Purpose:** Define multi-provider abstraction pattern, Provider Catalog and
Model Catalog concepts, routing modes including auto_balanced, fallback rules,
free/promotional/paid routing separation, provider security and data controls,
and compliance constraints for Chat, Vision, Embeddings, STT, TTS, Image and
Video generation.

**Note:** Documentation only. No real provider API calls, no secrets.

## Purpose

Establish a provider-agnostic routing layer that supports multiple AI
providers and models with explicit privacy, cost, quality, and compliance
controls.

## In Scope

- Multi-provider abstraction pattern (e.g., LiteLLM or similar interface)
- Provider Catalog and Model Catalog concepts with detailed schema fields
- Support for Chat, Vision, Embeddings, STT, TTS, Image generation, Video
- Routing modes: manual_model_selection, auto_best_quality, auto_lowest_cost,
  auto_free, auto_privacy_preferred, auto_balanced
- Fallback rules, free/promotional/paid routing separation, compliance
- Provider security and data controls aligned with docs/security

## Out of Scope

- Actual provider API integration and secret material (future, reviewed)
- Final model pricing and exact catalog entries (future, versioned config)
- Production enforcement code and concrete provider wiring (future PRs)

## Multi-Provider Abstraction Pattern

- Provider abstraction interface similar to LiteLLM or similar interface
- Single normalized interface for Chat, Vision, Embeddings, STT, TTS, Image
  generation, Video generation
- Provider-specific adapters translate normalized request to provider-specific
  parameters via provider-neutral config layer
- Core chat logic uses normalized modes (strict_factual, balanced, creative),
  not raw provider parameters
- Adding new provider does not require changing core chat logic, only mapping
  in config layer with evaluation and versioned tests
- Cost tracking per call for unit economics, token counts, latency, error,
  version logging
- Provider abstraction strategy: see PROVIDER_ABSTRACTION_STRATEGY.md

## Provider Catalog

Provider Catalog must support:

- **provider_id:** String, e.g., provider_a, CONFIGURED_VALUE
- **display_name:** String, e.g., Provider A Display Name
- **adapter_type:** String, e.g., litellm, openai_compatible, self_hosted
- **supported_regions:** List, e.g., ["global", "EU", "US"], must respect
  sanctions and geographic restrictions, no bypass permitted
- **terms_version:** String, e.g., v1.0.0
- **terms_reviewed_at:** DateTime, e.g., 2026-07-24
- **privacy_policy_version:** String, e.g., v1.0.0
- **privacy_policy_reviewed_at:** DateTime
- **retention_policy:** Text, e.g., zero retention, no training, 30 days
- **training_usage_policy:** Text, e.g., no training on user data
- **data_residency:** String, e.g., EU, US, CONFIGURED_VALUE
- **legal_review_status:** Enum, e.g., pending, approved, rejected
- **security_review_status:** Enum, e.g., pending, approved, rejected
- **enabled:** Boolean
- **health_status:** Enum, e.g., healthy, degraded, unhealthy, unknown

Privacy labels such as zero-retention or no-training must never be accepted
without official policy or contract evidence, access/review date, policy version,
and legal/privacy review.

## Model Catalog

Model Catalog must support:

- **provider_id:** String, e.g., provider_a
- **model_id:** String, e.g., model_a, CONFIGURED_VALUE
- **display_name:** String, e.g., Model A Display Name
- **modality_capabilities:** List, e.g., ["chat", "vision", "tool_calling"]
- **streaming_support:** Boolean
- **tool_support:** Boolean
- **vision_support:** Boolean
- **file_support:** Boolean
- **context_window:** Integer, e.g., CONFIGURED_VALUE tokens
- **input_price:** Decimal, per 1K tokens, pricing_version tracked
- **output_price:** Decimal, per 1K tokens
- **cached_input_price:** Decimal, per 1K cached tokens if supported
- **reasoning_price:** Decimal, provider-reported reasoning usage if applicable
- **audio_input_price:** Decimal, STT price per second
- **audio_output_price:** Decimal, TTS price per second
- **image_price_units:** Decimal, per image, per resolution
- **video_price_units:** Decimal, per second, per resolution
- **currency:** String, e.g., USD, CONFIGURED_CURRENCY_SOURCE
- **pricing_version:** String, e.g., v1.0.0, for audit and rollback
- **effective_at:** DateTime, when pricing becomes effective
- **privacy_classification:** Enum, e.g., privacy_preferred, standard,
  low_privacy, requires policy evidence, access/review date, policy version
- **free_tier_eligible:** Boolean, whether provider reports zero usage price,
  versioned and may expire
- **subscription_requirements:** Text, e.g., requires subscription plan X or
  no subscription, entitlements
- **enabled:** Boolean, whether model is enabled
- **health_status:** Enum, e.g., healthy, degraded, unhealthy
- **evaluation_version:** String, e.g., v1.0.0, quality evaluation version

Do not use current commercial model names as permanent schema examples. Use
neutral examples such as provider_a, model_a, CONFIGURED_VALUE. Remove ambiguous
examples such as IR-allowed, gpt-4o, claude-3-5-sonnet, gemini-1-5-pro.

## Routing Modes

### manual_model_selection

- User explicitly selects preferred model within allowed range
- Backend validates requested model against:
  - enabled Model Catalog entry
  - required modality/capability (e.g., vision, tool_support, file_support)
  - user plan and entitlement (free, subscription, wallet)
  - wallet budget (available balance, not posted ledger balance)
  - Role or Persona model policy (default_model_policy, allowed_response_modes
    maps to capability, not direct model id check)
  - privacy and risk requirements (privacy_classification, high-risk personas
    limited to strict_factual and balanced)
  - region and provider compliance (supported_regions, terms_version,
    privacy_policy_version, legal_review_status, security_review_status)
  - current provider health (health_status healthy)

### auto_best_quality

- The best evaluated model that satisfies the user-approved budget, required
  capability, plan entitlement, privacy requirements, and provider compliance.
- Must not operate regardless of cost.
- No automatic route may exceed the approved estimate or reservation.
- If no model satisfies budget and capability, return explicit error with
  alternatives or ask user to increase budget, do not silently upgrade cost.

### auto_lowest_cost

- System routes to lowest cost model that meets quality threshold and satisfies
  budget, capability, privacy, and compliance.

### auto_free

- System routes to free tier models only, abuse-protected, rate limited.
- Free status is versioned and may expire, must not assume permanent free.

### auto_privacy_preferred

- System routes to privacy-preferred models (zero retention, no training) that
  satisfy budget and capability.
- Must never silently fall back to lower privacy provider.

### auto_balanced

- New routing mode that balances:
  - task capability (required modality, tool_support, vision_support)
  - Persian evaluation quality (Persian-first, RTL, typography, balanced vs
    creative)
  - expected cost (input/output token price, pricing_version)
  - user budget (available balance, wallet, promotional vs purchased)
  - privacy (privacy_classification, requires policy evidence)
  - latency (provider latency, streaming_support)
  - reliability (provider health_status, evaluation_version)
  - provider availability (supported_regions, enabled, health_status)

## Fallback Rules

- Never silently fall back to a more expensive model
- Never silently fall back to a weaker privacy provider
- If preferred model unavailable (health_status degraded/unhealthy), return
  explicit error with alternatives, or ask user to choose, or route to same cost
  and same or stronger privacy tier with user notification
- Fallback must be logged as security event with metadata only, no raw sensitive
  content
- Fallback rules must be versioned and require owner approval
- No automatic route may exceed the approved estimate or reservation without new
  user consent

## Free, Promotional, and Paid Routing

### Provider-Free Model

- Provider currently reports zero usage price (free_tier_eligible true)
- May still create infrastructure, storage, bandwidth, safety, or support cost
  for platform (all-in variable cost includes those)
- Free status is versioned and may expire (effective_at, pricing_version)
- Must not assume provider free tier is permanent, must track expiry

### User Free Tier

- May be platform-subsidized, uses a configured platform budget (separate from
  provider free tier)
- Must not assume a provider free tier is permanent
- Uses auto_free routing mode, abuse-protected, rate limited
- Never silently move a free user to paid usage without user confirmation or
  approved persistent preference

### Promotional Credits

- Are wallet credits governed by a campaign policy (source, campaign_id,
  expiry_date, is_promotional)
- Are not the same as a free provider model (promotional credits are platform
  credits, provider-free is provider pricing zero)
- Their allowed model scope is a separate Open Decision (e.g., can promotional
  credits be used for all models or only chat, not studio)
- Are not cash and may expire
- Never silently consume purchased credits after promotional credits run out
- Require user confirmation or an approved persistent preference before changing
  the payment source (promotional vs purchased vs subscription)

### Rules

- Never silently move a free user to paid usage
- Never silently consume purchased credits after promotional credits run out
- Require user confirmation or an approved persistent preference before changing
  the payment source (free vs promotional vs purchased vs subscription)

## Provider Security and Data Controls

Aligned with docs/security:

- Provider credentials come only from the approved secrets manager (not from
  code, git history, documentation, logs, URLs, client)
- Adapters receive only the specific scoped credential they need (least privilege,
  separate from platform credentials, revocable independently, secret isolation)
- No provider secret may enter prompts, logs, model output, or client code
- Raw content is minimized before provider transmission where practical (e.g.,
  truncate, redact, or summarize uploaded files if not needed for task, per
  privacy policy)
- Provider retention/training policy is disclosed before sensitive use (e.g.,
  mental health, trauma, migration, private files) – user must be informed of
  privacy_classification and retention_policy
- Provider responses and tool outputs remain untrusted until validated (validate
  schema, provenance, no secret leakage, no prompt injection)
- Prompt Injection and output-exfiltration controls apply before and after
  provider calls (input validation, output guardrails, jailbreak detection,
  content provenance tagging, quarantine untrusted content)
- Provider addition requires security, privacy, legal, finance, and owner review
  (terms_version, privacy_policy_version, legal_review_status,
  security_review_status, retention_policy, training_usage_policy, data_residency)

## Compliance Constraints

- No sanctions, geographic, KYC, or Terms of Service bypass is permitted
- Use legally compliant providers or self-hosted models
- No bypassing provider ToS, geographic restrictions, sanctions, KYC, fake
  identities, hiding prohibited end-user locations
- Absolutely forbidden NO-GO actions have no approval path
- Provider and region allowlist must be reviewed and versioned, no silent
  addition of non-compliant providers
- Privacy labels such as zero-retention or no-training must never be accepted
  without official policy or contract evidence, access/review date, policy
  version, legal/privacy review

## Cost and Privacy Considerations

- Cost tracking per call: input/output/cached/reasoning tokens, embeddings,
  reranking, web search, STT/TTS seconds, image/video units, storage,
  bandwidth and egress, safety/moderation calls, failed but provider-billed
  requests, expected retries, payment fees, currency-conversion buffer
- Privacy classification influences routing: privacy_preferred for sensitive
  conversations, standard for general chat
- All-in variable cost includes provider cost plus overhead, used for pricing
  and unit economics (see PRICING_AND_UNIT_ECONOMICS.md)
- All numeric limits and thresholds must use CONFIGURED_LIMIT placeholders

## Related Documents

- Security Index: [../security/README.md](../security/README.md)
- Provider Abstraction: [PROVIDER_ABSTRACTION_STRATEGY.md](PROVIDER_ABSTRACTION_STRATEGY.md)
- Accuracy and Creativity: [ACCURACY_CREATIVITY_CONTROL.md](ACCURACY_CREATIVITY_CONTROL.md)
- Role and Persona System: [ROLE_AND_PERSONA_SYSTEM.md](ROLE_AND_PERSONA_SYSTEM.md)
- Pricing and Unit Economics: [PRICING_AND_UNIT_ECONOMICS.md](PRICING_AND_UNIT_ECONOMICS.md)
- Agent Security Model: [../security/AGENT_SECURITY_MODEL.md](../security/AGENT_SECURITY_MODEL.md)
- Referral and Promotional Credits: [REFERRAL_AND_PROMOTIONAL_CREDITS.md](REFERRAL_AND_PROMOTIONAL_CREDITS.md)

## Open Decisions

- Exact Provider Catalog and Model Catalog schema and field types
- Supported modalities per provider and per model and evaluation_version
- Routing mode defaults per Role and per user preference and auto_balanced weights
- Fallback rules and user notification wording and logging
- Free, promotional, and paid routing exact rules and persistent preference
- Provider and region allowlist and compliance review process and legal review
- Cost and privacy classification methodology and evaluation
- Owner, finance, security, privacy, legal, and compliance approval required

## Planned Completion Stage

Phase 1 - Provider Abstraction and Routing

## Status Note

Proposed Architecture - Pending Owner, Finance, Security, and Compliance Approval.
Will be completed later with product, finance, security, and owner review. No real
provider API calls in this PR.
