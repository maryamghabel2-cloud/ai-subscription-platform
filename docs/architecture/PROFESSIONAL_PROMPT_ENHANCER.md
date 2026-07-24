# Professional Prompt Enhancer

**Version:** v0.1.0

**Date:** 2026-07-24

**Status:** Draft - Structure Only

**Document Owner:** AI Platform Architect / Product

**Purpose:** Define optional professional prompt enhancer as cross-platform paid
feature with per-request and persistent preference, cost transparency, separate
ledger operation, and specialized profiles.

**Note:** Documentation only. No real provider API calls, no secrets.

## Purpose

Establish a prompt enhancer that helps users write better prompts for general
chat, strict factual research, image generation, video generation, and
advertising copy, with transparent cost and user control.

## In Scope

- Prompt enhancer as cross-platform paid feature, off by default, per-request
  or persistent preference, cost transparency, separate ledger operation,
  specialized profiles

## Out of Scope

- Final prompt enhancer implementation and exact prompt templates (future PRs)
- Final pricing for enhancer step (future, CONFIGURED_LIMIT)
- Production enhancer engine code (future PRs)

## Cross-Platform Paid Feature

- The Prompt Enhancer is a cross-platform paid feature, available on Website,
  Mobile application, Telegram, and Developer APIs
- It is a paid feature because it calls an additional LLM to enhance the user's
  original prompt, incurring provider cost (input/output tokens)
- It must be billed separately as a separate ledger operation for transparency
- It must not be silently enabled, must have user consent and cost transparency

## User Experience: Off by Default

- Off by default for all users, to avoid unexpected cost and to respect user
  autonomy
- User can enable per-request via toggle or button: "Enhance prompt" or
  Persian "بهبود پرامپت"
- User can enable as a persistent preference in settings: e.g., "Always enhance
  my prompts for image generation" or "Always enhance for research"
- First-use onboarding should explain what prompt enhancer does, its cost, and
  how to enable/disable
- User must be able to change preference later in settings page
- Normal Assistant is default mode, not enhanced, to avoid accidental cost

## Show Enhanced Prompt to User Before Execution When Appropriate

- When appropriate, show enhanced prompt to user before execution for
  transparency and editability
- Example: User writes "a cat", enhancer produces "a fluffy Persian cat sitting
  on a wooden table, soft natural lighting, high detail, 4k, professional photo"
- Show both original and enhanced prompt, allow user to edit enhanced prompt or
  revert to original
- For research and factual modes, show enhanced prompt with added context and
  citations structure, but must not invent citations, must not hallucinate
  sources
- For advertising copy, show enhanced prompt with marketing angles, but must
  not invent factual claims, prices, or medical/legal claims

## Clearly Show Additional Estimated Cost for the Enhancement Step

- Clearly show additional estimated cost for the enhancement step before user
  confirms
- Example: "Enhancement will cost approximately 2 credits (estimated). Original
  request will cost approximately 5 credits. Total approximately 7 credits."
- Use Model Catalog pricing: input/output token price, pricing_version
- Estimated cost must be based on max tokens for enhancer model, not actual yet,
  and must be updated after actual usage with Reserve-Settle-Refund workflow
- Cost must be displayed in Persian and English, with credit and Toman/USD
  equivalents if applicable, using static 190600 Toman per USD for MVP, later
  real-time rate

## Separate Ledger Operation for the Enhancer Cost

- Separate ledger operation for the enhancer cost for transparency and audit
- When user enables enhancer, two ledger operations occur:
  1. Reserve and settle for enhancer step: estimate enhancer cost, reserve
     credits atomically, execute enhancer LLM call, measure actual usage,
     settle, refund unused reservation
  2. Reserve and settle for main request: estimate main request cost based on
     enhanced prompt, reserve, execute main provider request, measure actual
     usage, settle, refund
- Each ledger entry must have metadata: is_enhancer boolean, enhancer_profile,
  original prompt hash replaced with content_fingerprint DISABLED_BY_DEFAULT per
  privacy hardening, enhanced prompt hash similarly disabled, provider_id,
  model_id, token counts, cost, timestamps, not raw sensitive content
- Raw prompts (original and enhanced) must remain outside technical logs, only
  in separate encrypted product-data store when required for user-facing feature
  per retention settings (conversation history), not in technical audit logs

## Specialized Profiles

- **General chat:** Enhances user prompt for general conversation, more helpful,
  more structured, more Persian-aware, more context
- **Strict factual research:** Enhances prompt for research, study workspace, RAG
  with sources, evidence grading, must not invent citations, must disclose
  uncertainty, must be citation-aware, must never invent fake URLs or publisher
  and date, default for high-risk personas strict_factual
- **Image generation:** Enhances prompt for Professional Image Studio, adds
  style, lighting, composition, aspect ratio, background, but must not invent
  factual citations, must not imitate copyrighted style without consent
- **Video generation:** Enhances prompt for Professional Video Studio, adds
  motion, camera movement, storyboard, character consistency, voice-over and
  subtitles considerations
- **Advertising copy:** Enhances prompt for advertising campaigns, ad creatives,
  variants, posters, banners, social media assets, website assets, must not
  invent factual claims, legal rules, medical claims, provider prices, current
  events, must be balanced

Each profile must have:

- id, display_name_fa, display_name_en, description, system_instructions,
  default_tone, allowed_tones, default_response_mode, allowed_response_modes,
  risk_level, disclaimer_policy, safety_profile, enabled
- Versioned registry similar to Role registry, adding new profile should not
  require changing core enhancer logic
- User customization: custom enhancer instructions, tone, formal/casual,
  concise/detailed, language, creativity mode

## Related Documents

- Security Index: [../security/README.md](../security/README.md)
- Multi-Provider Routing: [MULTI_PROVIDER_MODEL_ROUTING.md](MULTI_PROVIDER_MODEL_ROUTING.md)
- Pricing and Unit Economics: [PRICING_AND_UNIT_ECONOMICS.md](PRICING_AND_UNIT_ECONOMICS.md)
- Accuracy and Creativity: [ACCURACY_CREATIVITY_CONTROL.md](ACCURACY_CREATIVITY_CONTROL.md)
- Role and Persona System: [ROLE_AND_PERSONA_SYSTEM.md](ROLE_AND_PERSONA_SYSTEM.md)
- Agent Plugin and Execution: [AGENT_PLUGIN_AND_EXECUTION_SYSTEM.md](AGENT_PLUGIN_AND_EXECUTION_SYSTEM.md)

## Open Decisions

- Exact prompt enhancer system_instructions per profile and version
- Cost for enhancer step (CONFIGURED_LIMIT placeholder, requires provider cost
  analysis, finance and owner approval)
- Whether to show enhanced prompt before execution always or only when
  appropriate (e.g., always for image/video, optional for chat)
- Persistent preference storage: user_role_preferences table with
  prompt_enhancer_enabled boolean and enhancer_profile
- Owner, product, and finance approval required for all decisions

## Planned Completion Stage

Phase 1 - Prompt Enhancer

## Status Note

Draft - Structure Only. Will be completed later with product, AI, and owner
review. No real provider API calls in this PR.
