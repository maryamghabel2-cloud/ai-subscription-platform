# Multi-Provider and Model Routing Architecture

**Version:** v0.1.0

**Date:** 2026-07-24

**Status:** Draft - Structure Only

**Document Owner:** AI Platform Architect

**Purpose:** Define multi-provider abstraction pattern, model catalog schema,
routing modes, fallback rules, and compliance constraints for Chat, Vision,
Embeddings, STT, TTS, Image and Video generation.

**Note:** Documentation only. No real provider API calls, no secrets.

## Purpose

Establish a provider-agnostic routing layer that supports multiple AI providers
and models with explicit privacy, cost, and quality controls.

## In Scope

- Multi-provider abstraction pattern (e.g., LiteLLM or similar interface)
- Support for Chat, Vision, Embeddings, STT, TTS, Image generation,
  Video generation
- Model Catalog schema and routing modes
- Fallback rules and compliance constraints

## Out of Scope

- Actual provider API integration and secret material (future, reviewed)
- Final model pricing and exact catalog entries (future, versioned config)
- Production enforcement code (future PRs)

## Multi-Provider Abstraction Pattern

- Provider abstraction interface similar to LiteLLM or similar interface
- Single normalized interface for Chat, Vision, Embeddings, STT, TTS, Image
  generation, Video generation
- Provider-specific adapters translate normalized request to provider-specific
  parameters (temperature, top_p, top_k mapped from Accuracy and Creativity modes
  via provider-neutral config layer)
- Core chat logic uses normalized modes (strict_factual, balanced, creative),
  not raw provider parameters
- Adding new provider does not require changing core chat logic, only mapping
  in config layer with evaluation and versioned tests
- Cost tracking per call for unit economics, token counts, latency, error,
  version logging
- Provider abstraction strategy: see PROVIDER_ABSTRACTION_STRATEGY.md

## Supported Modalities

- Chat: text chat, Persian-first, user-selectable models, automatic routing
- Vision: image understanding, file/image/PDF attachments, product photography
- Embeddings: vector store query for RAG, knowledge base retrieval with citations
- STT: speech-to-text for voice input, accessibility and mobile
- TTS: text-to-speech for voice output, accessibility
- Image generation: Professional Image Studio, product photography, advertising,
  posters, banners, artistic images, brand concepts
- Video generation: Professional Video Studio, text-to-video, image-to-video,
  product advertisements, brand videos, educational videos, storyboards,
  character workflows, voice-over and subtitles

## Model Catalog Schema

- **provider_id:** String, e.g., openai, anthropic, google, self_hosted
- **model_id:** String, e.g., gpt-4o, claude-3-5-sonnet, gemini-1-5-pro,
  self-hosted-llama
- **context_window:** Integer, e.g., CONFIGURED_LIMIT tokens
- **input/output token price:** Decimal, e.g., per 1K tokens, pricing_version
  tracked, e.g., v1, v2
- **pricing_version:** String, version of pricing, e.g., v1.0.0, for audit and
  rollback
- **privacy_classification:** Enum, e.g., privacy_preferred, standard, low_privacy,
  data_retention_possible, no_training_possible, zero_retention
- **supported_regions:** List, e.g., ["global", "EU", "US", "IR-allowed"],
  must respect sanctions and geographic restrictions, no bypass permitted
- **capabilities:** List, e.g., chat, vision, function_calling, image_generation,
  video_generation, embeddings, stt, tts
- **quality_score:** Decimal or enum, e.g., High/Medium/Low, from evaluation
- **cost_tier:** Enum, e.g., free, low, medium, high, from provider pricing
- **model_policy:** String, e.g., auto_routing, fast, balanced, strong

Exact schema fields are Open Decisions and require product, finance, and
security review.

## Routing Modes

- **manual_model_selection:**
  - User explicitly selects preferred model within allowed range
  - Backend validates requested model is in allowed_response_modes for Role
  - Example: Writer allows balanced, creative; user chooses creative

- **auto_best_quality:**
  - System routes to best quality model for task, regardless of cost, within
    privacy constraints
  - Example: research, study workspace, RAG with sources, high-risk personas
    strict_factual should use strongest model with citations

- **auto_lowest_cost:**
  - System routes to lowest cost model that meets quality threshold
  - Example: simple chat, friendly companion, general questions
  - Must respect privacy classification, no silent fallback to weaker privacy

- **auto_free:**
  - System routes to free tier models only, abuse-protected, rate limited
  - Example: free tier users, promotional credits, trial

- **auto_privacy_preferred:**
  - System routes to privacy-preferred models (zero retention, no training)
  - Example: mental health information assistant, sensitive personal content,
    trauma, migration, private files
  - Must never silently fall back to lower privacy provider

## Fallback Rules

- Never silently fall back to a more expensive model
- Never silently fall back to a weaker privacy provider
- If preferred model unavailable, return explicit error with alternatives,
  or ask user to choose, or route to same cost and same or stronger privacy
  tier with user notification
- Fallback must be logged as security event with metadata only, no raw
  sensitive content
- Fallback rules must be versioned and require owner approval

## Compliance Constraints

- Explicitly state: No sanctions, geographic, KYC, or Terms of Service bypass
  is permitted.
- Use legally compliant providers or self-hosted models.
- No bypassing provider ToS, no bypassing geographic restrictions, no bypassing
  sanctions, no bypassing KYC, no using fake identities, no hiding prohibited
  end-user locations.
- Absolutely forbidden NO-GO actions have no approval path, no human approval
  may authorize these.
- Provider and region allowlist must be reviewed and versioned, no silent
  addition of non-compliant providers.

## Cost and Privacy Considerations

- Cost tracking per call: input/output/cached/reasoning tokens, embeddings,
  STT/TTS seconds, image/video units, storage, retries, payment fees
- Privacy classification influences routing: privacy_preferred models for
  sensitive conversations, standard for general chat
- All-in variable cost includes provider cost plus overhead, used for pricing
  and unit economics (see PRICING_AND_UNIT_ECONOMICS.md)

## Related Documents

- Security Index: [../security/README.md](../security/README.md)
- Provider Abstraction: [PROVIDER_ABSTRACTION_STRATEGY.md](PROVIDER_ABSTRACTION_STRATEGY.md)
- Accuracy and Creativity: [ACCURACY_CREATIVITY_CONTROL.md](ACCURACY_CREATIVITY_CONTROL.md)
- Role and Persona System: [ROLE_AND_PERSONA_SYSTEM.md](ROLE_AND_PERSONA_SYSTEM.md)
- Pricing and Unit Economics: [PRICING_AND_UNIT_ECONOMICS.md](PRICING_AND_UNIT_ECONOMICS.md)
- Agent Security Model: [../security/AGENT_SECURITY_MODEL.md](../security/AGENT_SECURITY_MODEL.md)

## Open Decisions

- Exact Model Catalog schema and field types
- Supported modalities per provider and per model
- Routing mode defaults per Role and per user preference
- Fallback rules and user notification wording
- Provider and region allowlist and compliance review process
- Cost and privacy classification methodology
- Owner approval required for all decisions

## Planned Completion Stage

Phase 1 - Provider Abstraction and Routing

## Status Note

Draft - Structure Only. Will be completed later with product, finance, security,
and owner review. No real provider API calls in this PR.
