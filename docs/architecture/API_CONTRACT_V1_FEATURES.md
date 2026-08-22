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

## Document Status: Part 1 of 3 Complete

This document currently contains Document Control, Overview, Shared Feature
Principles, and Section 1 Prompt Enhancer API.

Pending in Part 2: Section 2 Caption Generator API.

Pending in Part 3: Admin Usage API, shared response shapes, provider-failure
propagation, and implementation status summary.

Do not treat this contract as complete or implementation-ready until Parts 2 and 3 are merged.
