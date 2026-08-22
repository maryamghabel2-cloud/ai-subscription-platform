# Phase 1 Feature API Contract — General Chat

## Document Control

**Title:** Phase 1 Feature API Contract — General Chat
**Status:** Draft (Part 1 of 3 — Parts 2 and 3 pending)
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

## Document Status: Part 2 of 3 Complete

This document currently contains:
- Document Control
- Overview
- Core Principles
- Section 1: Conversation Management Endpoints (3 endpoints)
- Section 2: Message Endpoints (send, cancel, delete)

Pending in Part 3:
- Streaming Response Contract (SSE event types)
- Billing Lifecycle Summary table
- Implementation Status table
- Open items for D2.2b (Enhancer, Caption, Admin)

Do not treat this contract as complete or implementation-ready until Part 3 is merged into this file.
