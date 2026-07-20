# PROVIDER ABSTRACTION STRATEGY - Phase 0 Governance

**Date:** 2026-07-20
**Status:** Planning doc only

## Purpose
Avoid lock-in to single AI provider, enable swapping image/video/embedding providers, track cost per action, maintain compliance (no ToS bypass).

## Why Abstraction

- Chat: OpenAI-compatible API (e.g., OpenAI, Anthropic, local compatible) - approach: wrapper interface with model name, tokens, cost
- Image: Stability, DALL·E, Flux, etc. - wrapper with prompt, negative prompt, style, cost per image
- Video: Runway, Pika, etc. - wrapper async job queue
- Embedding: OpenAI embeddings or local compatible - wrapper
- All wrappers must log model version, tokens/cost, latency, error

## Design Principles

- Interface: e.g., `ChatProvider.generate(prompt, system_prompt, persona_id, ...)` returns response + tokens + cost + model version
- Provider config in env, not hardcoded, no secrets in repo, via .env.example placeholders
- Cost tracking per call for unit economics (Finance agent)
- No scraping or bypassing provider ToS - only official APIs
- No sharing/reselling unauthorized credentials - each provider API key is founder's key with limited scope, stored in vault future, not repo
- Provider failure handling: retry with exponential backoff, circuit breaker, fallback to secondary provider if configured, but no auto spend beyond budget without approval
- Versioning: Provider version logged in audit log for persona responses

## Absolutely Forbidden

- Bypassing provider ToS, geographic restrictions, sanctions, KYC, using fake identities, hiding prohibited locations
- Sharing/reselling unauthorized credentials or raw supplier keys - no approval may authorize
- Scraping GGSel/FunPay/Oyunfor/Kie.ai/ShareTool marketplaces - deprecated model

## Future (Not Built Now)

- Phase 3: Image provider abstraction interface
- Phase 5: Video provider async
- Phase 7: Embedding provider

## Linkage
- System Context: SYSTEM_CONTEXT.md
- Model Evaluation: MODEL_EVALUATION_STRATEGY.md
- Trust & Safety: TRUST_AND_SAFETY_FRAMEWORK.md
