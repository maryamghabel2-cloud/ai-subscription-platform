# Phase 1 API Contract V1

## Document Control

**Title:** Phase 1 API Contract V1
**Status:** Draft (Part A of 3 — Parts B and C pending)
**Phase:** Phase 1 — In Progress
**Last updated:** 2026-08-21
**Scope when complete:** Auth + Wallet/Credits
**Related:** [ADR-0002](../decisions/0002-phase-1-product-metering-and-infrastructure.md), [Pricing](PRICING_AND_UNIT_ECONOMICS.md), [Chat](../product/GENERAL_CHAT_PRD.md), [Wallet](../product/WALLET_AND_CREDITS_PRD.md)

## API Design Principles

- JSON request and response bodies.
- HTTPS only in deployed environments.
- Version paths begin `/api/v1/`.
- Secure HttpOnly cookie session authentication only.
- State-changing requests use CSRF token validation or SameSite protection.
- Mutation idempotency uses `Idempotency-Key`; Part C defines details.
- Error responses use the standard shape below.
- List responses use pagination shape below.
- Every request is scoped to authenticated tenant/user.
- Sensitive endpoints are rate-limited; limits are deferred to D2.5/NFR.

## Standard Shapes

### Error Response
```json
{"error":{"code":"machine_readable_snake_case","message":"human-readable message","request_id":"uuid"}}
```

### Paginated List Response
```json
{"items":[],"total":0,"page":1,"page_size":20,"has_next":false}
```

### Credit Balance
```json
{"available_credits":0,"reserved_credits":0,"total_credits":0}
```

## Section 1: Authentication API

### POST /api/v1/auth/register
Description: Create a user and establish secure session. Request:
```json
{"email":"user@example.invalid","password":"string","display_name":"optional"}
```
Success: `201` with `{"id":"uuid","email":"string","display_name":"string|null","created_at":"timestamp"}` and session cookie. Errors: `email_already_registered`, `invalid_email`, `weak_password`, `validation_error`. Security: raw token never appears in body. Implementation status: Backend foundation exists — validation required (`backend/app/api/auth.py`).

### POST /api/v1/auth/login
Description: Authenticate user and set session cookie. Request:
```json
{"email":"user@example.invalid","password":"string"}
```
Success: `200` user object and session cookie. Errors: `invalid_credentials`, `account_locked`, `validation_error`, `rate_limited`. Security: generic credential failure prevents enumeration; attempts are rate-limited. Implementation status: Backend foundation exists — validation required.

### POST /api/v1/auth/logout
Description: End current session. Request: none; session cookie used. Success: `200` with `{"message":"logged_out"}` and cookie cleared. Errors: `not_authenticated`. Security: invalidate server-side session. Implementation status: Backend foundation exists — validation required.

### POST /api/v1/auth/refresh
Description: Rotate valid session/refresh cookie. Request: none. Success: `200` with `{"message":"session_refreshed"}` and new cookie; prior session invalidated. Errors: `session_expired`, `invalid_session`. Security: rotation prevents continued use of prior session. Implementation status: Pending implementation validation.

### GET /api/v1/auth/me
Description: Return current authenticated user. Request: none. Success: `200` user object. Errors: `not_authenticated`. Security: cookie session only. Implementation status: Backend foundation exists — validation required.

## Section 2: Wallet and Credits API

These endpoints implement ADR-0002 quote/reserve/settle/release policy. Phase 1
uses sandbox/mock top-up only.

### GET /api/v1/wallet/balance
Returns `{"available_credits":95,"reserved_credits":5,"total_credits":100,"low_balance":false}` with `200`. Errors: `not_authenticated`. No billing event; balances remain separate. Implementation: Backend foundation exists — validation required.

### GET /api/v1/wallet/transactions
Query: `page`, `page_size`, `date_from`, `date_to`, `feature`, `direction`, `status`. Returns paginated immutable transactions with id, type, amount_credits, direction, feature, status, created_at, settled_at, description, reference_id. Errors: `not_authenticated`, `invalid_filter`. No billing event.

### GET /api/v1/wallet/transactions/{id}
Returns one tenant-scoped transaction and nullable receipt_url with `200`. Errors: `not_authenticated`, `not_found`. Reading never changes balance.

### POST /api/v1/wallet/topup/intent
Request `{"package_size":100}`; allowed packages 100, 500, 2000. Returns `201` pending intent with mock_confirmation_token. Errors: `not_authenticated`, `invalid_package`, `validation_error`. Sandbox/mock only, no fiat price or real provider. `Idempotency-Key` required.

### POST /api/v1/wallet/topup/confirm
Request `{"intent_id":"uuid","mock_confirmation_token":"string"}`. Valid token credits once and returns succeeded transaction/balance; invalid token records failed with no credit; replay returns final state. Errors: `not_authenticated`, `intent_not_found`, `invalid_token`, `already_processed`. `Idempotency-Key` required.

### POST /api/v1/wallet/reserve
Request `{"feature":"chat","quoted_credits":2,"idempotency_key":"uuid"}`. Returns `201` reservation, status reserved, expiry now plus 10 minutes, and balance. Checks spendable credits, moves available to reserved, and blocks provider call on `insufficient_credits`. Errors: `not_authenticated`, `insufficient_credits`, `validation_error`, `idempotent_replay`.

### POST /api/v1/wallet/settle
Request `{"reservation_id":"uuid","actual_credits":1}`. Returns settled reservation, released unused credits, and balance. Actual credits cannot exceed quote; settlement creates immutable ledger entry. Errors: `not_authenticated`, `reservation_not_found`, `already_settled`, `exceeds_quote`, `validation_error`, `settlement_conflict`.

### POST /api/v1/wallet/release
Request `{"reservation_id":"uuid","reason":"provider_timeout"}`; allowed reasons include provider_timeout, provider_failure, user_canceled, validation_failure, expired, internal_error. Returns released balance and immutable release entry. Errors: `not_authenticated`, `reservation_not_found`, `already_finalized`, `validation_error`. Replay is idempotent.

## Document Status: Part B of 3 Complete

This document currently contains Document Control, API Design Principles, Standard
Shapes, Section 1 Authentication API, and Section 2 Wallet and Credits API.

Pending in Part C:
- Section 3: Common Error Codes Reference
- Section 4: Idempotency Rules
- Section 5: Session and Cookie Contract
- Section 6: Implementation Status Summary
- Section 7: Open Contracts for D2.2

Do not treat this contract as complete or implementation-ready until Part C is
merged into this file.
