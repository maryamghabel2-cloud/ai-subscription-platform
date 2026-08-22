# Phase 1 Feature API Contract — General Chat

## Document Control

**Title:** Phase 1 Feature API Contract — General Chat
**Status:** Draft — Complete Chat Feature API Contract
**Phase:** Phase 1 — In Progress
**Last updated:** 2026-08-21
**Related:** [ADR-0002](../decisions/0002-phase-1-product-metering-and-infrastructure.md), [API Contract](API_CONTRACT_V1.md), [Chat PRD](../product/GENERAL_CHAT_PRD.md)

## Overview

General Chat is the platform activation capability. It uses tiered billing of 1,
2, or 3 credits determined by Token Budget Manager. Each message estimates,
reserves, executes, then settles or releases. Streaming is the default response
mode and is specified in a later part.

## Core Principles

- Conversation is a first-class resource.
- Message sending is billable with reserve/settle/release.
- Streaming is default; non-streaming is not supported.
- Copy and history reads are free.
- Cancellation releases full reservation and partial output is free.
- Provider failure releases reservation without charge.
- Actual settlement never exceeds quoted credits.
- Endpoints inherit secure HttpOnly cookie auth from API_CONTRACT_V1.md.

## Section 1: Conversation Management Endpoints

### POST /api/v1/chat/conversations
Creates an authenticated user's conversation. Request: `{"title":"string optional, max 200 chars"}`. Success `201`: `{"id":"uuid","title":"string","created_at":"iso8601","last_message_at":null,"message_count":0}`. Errors: `not_authenticated`, `validation_error`. Billing: free. Implementation status: Pending implementation.

### GET /api/v1/chat/conversations
Lists authenticated user's newest conversations. Query: page default 1; page_size default 20, maximum 50. Success `200` uses API_CONTRACT_V1 paginated shape; each item has id, title, created_at, last_message_at, message_count. Errors: `not_authenticated`. Billing: free. Implementation status: Pending implementation.

### GET /api/v1/chat/conversations/{id}
Gets one tenant-scoped conversation. Query: messages_page default 1; messages_page_size default 20. Success `200` includes id, title, timestamps, message_count, messages (id, role, content, status, created_at, credits_charged), messages_total, messages_has_next. Errors: `not_authenticated`, `not_found`. Billing: free. Implementation status: Pending implementation.

## Section 2: Message Endpoints

### POST /api/v1/chat/conversations/{id}/messages
Send a tenant-owned user message and stream assistant output. Request:
`{"content":"required non-empty string","idempotency_key":"uuid"}`. Steps:
1. validate ownership and content; 2. Token Budget Manager estimates tier 1/2/3;
3. reserve quoted credits; 4. reject insufficient credits before provider call;
5. execute provider streaming; 6. settle actual credits not exceeding quote on
success; 7. release on failure/timeout; 8. persist user and assistant messages.
Response is `text/event-stream`; Part 3 defines events. Final success carries
actual_credits and assistant message_id. Errors: not_authenticated,
conversation_not_found, validation_error, insufficient_credits, rate_limited,
provider_unavailable, internal_error. Same idempotency key, conversation, and
content cannot create duplicate reservation/message. Provider cost variance is
absorbed and logged. Implementation: Pending implementation.

### POST /api/v1/chat/conversations/{id}/messages/{message_id}/cancel
Validate ownership; stop active stream; release full reservation; mark canceled;
optionally store partial output as canceled. Returns `200` with message_id, status,
and released_credits. Errors: not_authenticated, not_found, already_finalized.
Repeated cancel returns current state without side effect. No Phase 1 partial-output charge.

### DELETE /api/v1/chat/conversations/{id}
MVP optional; deletion strategy is deferred to D2.3. If implemented, it is
tenant-scoped and returns `{"id":"uuid","status":"deleted"}`. Errors:
not_authenticated, not_found. It is free and never deletes immutable ledger entries.

## Section 3: Streaming Response Contract

Chat uses SSE `text/event-stream`; each event has `event` and JSON `data`.

| Event | When emitted | Payload fields | Billing effect |
|---|---|---|---|
| estimate | Before reserve | estimated_credits, tier, quote_id | None |
| reserved | Hold created | reservation_id, quoted_credits, expires_at | available -> reserved |
| token | Partial output | content | None |
| done | Settlement complete | message_id, actual_credits, quoted_credits, released_credits | settle/release |
| error | Failure | code, message, released_credits | Release |
| canceled | User cancellation | message_id, released_credits | Full release |

Estimate precedes reserved; tokens follow reservation; done follows settlement.
Error does not charge unless already settled. Canceled partial output is free.
Clients finalize only on done, error, or canceled.

## Section 4: Billing Lifecycle Summary

| Step | Action | Credit Effect | API/Service Contract |
|---|---|---|---|
| Estimate | Calculate tier | None | Internal metering |
| Reserve | Quote held | available -> reserved | Wallet reserve |
| Provider stream | Stream output | None | Provider gateway |
| Success | Final usage | settle actual <= quote; release excess | Wallet settle |
| Failure/Timeout | Provider fails | release full reservation | Wallet release |
| User Cancel | Active stream canceled | release; no partial charge | Wallet release |
| Retry | Idempotent retry | no duplicate charge | Idempotency contract |

Provider cost above quote is absorbed in Phase 1 and creates pricing-variance metadata.

## Section 5: Implementation Status

| Endpoint / Contract | Implementation Status | Notes |
|---|---|---|
| Conversation create/list/get | Pending implementation | No verified Chat endpoint in baseline |
| Send message stream | Pending implementation | Provider integration pending |
| Cancel message | Pending implementation | Cancel lifecycle pending |
| Delete conversation | MVP optional / pending D2.3 | Delete strategy deferred |
| SSE event format | Pending implementation | Defined here |
| Wallet integration | Backend foundation exists — validation required | API_CONTRACT_V1 reference |
| Token Budget Manager | Pending implementation | D2.4 tier boundaries |

Tests were not executed in this documentation task.

## Section 6: Open Items for D2.2b

1. Prompt Enhancer API contract
2. Prompt Enhancer history endpoint
3. Caption Generator API contract
4. Caption Generator history endpoint
5. Admin metadata-only usage endpoint
6. Shared feature-history response shape
7. Shared provider-failure error propagation rules

## Document Status: Complete Draft Chat Feature API Contract
