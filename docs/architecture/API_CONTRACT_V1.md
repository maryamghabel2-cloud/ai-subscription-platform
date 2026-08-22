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

## Document Status: Part A of 3 Complete

This document currently contains: Document Control, API Design Principles,
Standard Shapes, and Section 1 (Authentication API).

Pending in Part B:
- Section 2: Wallet and Credits API (8 endpoints)

Pending in Part C:
- Section 3: Common Error Codes Reference
- Section 4: Idempotency Rules
- Section 5: Session and Cookie Contract
- Section 6: Implementation Status Summary
- Section 7: Open Contracts for D2.2

Do not treat this contract as complete or implementation-ready until Parts B
and C are merged into this file.
