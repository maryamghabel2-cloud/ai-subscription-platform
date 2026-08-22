# Phase 1 Feature API Contract — Enhancer, Caption, and Admin

## Document Control
**Status:** Draft (Part 1 of 3 — Parts 2 and 3 pending)
**Phase:** Phase 1 — In Progress
**Last updated:** 2026-08-21
**Scope:** Prompt Enhancer, Caption Generator, Admin Usage.
**Related:** [ADR-0002](../decisions/0002-phase-1-product-metering-and-infrastructure.md), [Auth/Wallet](API_CONTRACT_V1.md), [Chat](API_CONTRACT_V1_CHAT.md), [Enhancer PRD](../product/PROMPT_ENHANCER_PRD.md), [Caption PRD](../product/INSTAGRAM_CAPTION_GENERATOR_PRD.md)

## Overview
This contract defines non-chat Phase 1 features. Prompt Enhancer is the first paid
Skill and Caption Generator is the first Studio tool. Both use wallet
reserve/settle/release from API_CONTRACT_V1.md.

## Shared Feature Principles
- Feature execution is billable; read/copy/history is free unless stated otherwise.
- Estimate is visible before execution.
- Reservation precedes provider execution.
- Actual credits never exceed quote.
- Failure or timeout releases reservation.
- Billable endpoints require idempotency.
- History is tenant scoped.
- Provider/model identifiers remain configuration.

## Section 1: Prompt Enhancer API

### POST /api/v1/enhancer/enhance
Request: `{"raw_prompt":"string","style":"creative|professional|technical|marketing|concise","idempotency_key":"uuid","send_to_chat":false}`. Validate session, non-empty prompt within 2,000 characters, and style; quote/reserve 2 credits; execute; persist raw/enhanced prompt and style; settle on success or release on failure. `send_to_chat` returns handoff metadata only. Success `200`: `{"id":"uuid","raw_prompt":"string","enhanced_prompt":"string","style":"creative","quoted_credits":2,"actual_credits":2,"created_at":"iso8601","send_to_chat_available":true}`. Errors: `not_authenticated`, `validation_error`, `insufficient_credits`, `invalid_style`, `rate_limited`, `provider_unavailable`, `internal_error`. Same key/payload has no duplicate result. Implementation: Pending implementation.

### GET /api/v1/enhancer/history
Query: page default 1, page_size default 20 maximum 50. Success `200` paginated items include id, style, raw_prompt_preview, created_at, quoted_credits, actual_credits. Error: `not_authenticated`. Billing: free. Implementation: Pending implementation.

### GET /api/v1/enhancer/history/{id}
Success `200` returns id, raw_prompt, enhanced_prompt, style, created_at, quoted_credits, actual_credits. Errors: `not_authenticated`, `not_found`. Billing: free. Implementation: Pending implementation.

### POST /api/v1/enhancer/history/{id}/handoff-to-chat
Request: `{"target_conversation_id":"uuid|null"}`. Returns existing enhancement handoff payload without Chat execution or Enhancer charge. A later Chat run is independently billed. Success `200`: `{"enhancement_id":"uuid","target_conversation_id":"uuid|null","handoff_payload":{"content":"enhanced prompt text"}}`. Errors: `not_authenticated`, `not_found`, `conversation_not_found`. Implementation: Pending implementation.

## Section 2: Instagram Caption Generator API

### POST /api/v1/caption/generate
Request includes description (required, maximum 1,000 characters), tone
professional/casual/funny/promotional/luxury/educational, length short/medium/long,
platform instagram/telegram/linkedin/twitter, language_mode persian/english/mixed,
hashtag_count default 10 within 3–30, variation_count default 3 within 1–5,
optional text-only image_context, and required idempotency_key. Image upload and
vision analysis are out of Phase 1 scope.

Validate ownership and inputs; quote/reserve 5 credits; generate; persist request
and results; settle on success or release on failure/timeout. Success `200` returns
id, variations containing separate caption/hashtags/character_count/platform_fit,
request settings, quoted_credits 5, actual_credits 5, created_at. platform_fit is
based on Instagram 2,200 characters; other thresholds are D2. Errors include
not_authenticated, validation_error, insufficient_credits, invalid_tone,
invalid_platform, invalid_length, invalid_language_mode, hashtag_count_out_of_range,
variation_count_out_of_range, description_too_long, unsafe_content, rate_limited,
provider_unavailable, internal_error. Same key/payload returns cached result.
Implementation: Pending implementation.

### POST /api/v1/caption/regenerate
Request: original_generation_id and required idempotency_key. It loads original
parameters, shows a new 5-credit quote, reserves, generates, persists linked result,
and settles or releases. It is a new billable request. Errors include original_not_found
plus generation errors. Implementation: Pending implementation.

### GET /api/v1/caption/history
Query page default 1, page_size default 20 maximum 50. Returns paginated tenant
history: id, description_preview, tone, platform, variation_count, created_at,
quoted_credits, actual_credits. Billing: free. Implementation: Pending implementation.

### GET /api/v1/caption/history/{id}
Returns tenant-scoped full generation result, variations, hashtags, character counts,
platform fit, and original settings. Errors: not_authenticated, not_found. Billing:
free. Implementation: Pending implementation.

## Document Status: Part 2 of 3 Complete

This document currently contains Document Control, Overview, Shared Feature
Principles, Section 1 Prompt Enhancer API (4 endpoints), and Section 2 Instagram
Caption Generator API (4 endpoints).

Pending in Part 3: Admin Usage API, shared provider-failure propagation rules,
implementation status summary, and open items for D2.3+.
