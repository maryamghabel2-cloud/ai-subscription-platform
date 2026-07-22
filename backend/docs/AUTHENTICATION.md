# AUTHENTICATION - Phase 1 Part 2

**Date:** 2026-07-20
**Branch:** build/phase-1-part2-auth
**Status:** Secure cookie-based authentication, no AI providers yet

## Auth Architecture

Use **opaque session-token authentication, NOT browser-accessible JWT**.

- Short-lived session token stored in HttpOnly cookie `nv_session` (30 minutes)
- Long-lived refresh token stored in HttpOnly cookie `nv_refresh` (30 days)
- CSRF token stored in non-HttpOnly cookie `nv_csrf` and required in X-CSRF-Token header for state-changing authenticated requests
- Store only token hashes in database (SHA256), never raw tokens
- Rotate refresh token on every refresh (old refresh invalidated)
- Revoke session on logout
- Password hashing via bcrypt, never log passwords or raw tokens

**Why opaque session tokens, not JWT in localStorage:**
- JWT in localStorage is vulnerable to XSS - any JS can steal token and exfiltrate
- HttpOnly cookies are not accessible to JS, mitigating XSS theft
- Opaque tokens allow server-side revocation (logout, password reset revokes all sessions, refresh rotation invalidates old)
- JWT browser-accessible is banned per hard rule: Do not store JWT or session tokens in localStorage
- Short-lived session + long-lived refresh with rotation balances security and UX

## Cookie Names and Requirements

**Session cookie:**
- name: nv_session
- HttpOnly: true
- Secure: true in production (False in local http for dev)
- SameSite: Lax
- Max-Age: 30 minutes (1800 seconds)
- Path: /

**Refresh cookie:**
- name: nv_refresh
- HttpOnly: true
- Secure: true in production
- SameSite: Lax
- Max-Age: 30 days (30*24*3600 seconds)
- Path: /

**CSRF cookie:**
- name: nv_csrf
- HttpOnly: false (must be readable by JS to send in header)
- Secure: true in production
- SameSite: Lax
- Max-Age: same as session (30 minutes)
- Path: /

All cookies set via `Response.set_cookie` with samesite="lax", httponly True/False per above, secure flag documented as True in prod.

## Session Lifetime

- Session: 30 minutes, sliding? Currently fixed 30 min from creation, last_used_at updated on each authenticated request for audit, but expires_at fixed. Future could extend on use.
- Refresh: 30 days, rotates on every refresh, old refresh invalidated (revoked_at set), new session+refresh+csrf set.

## Refresh Lifetime

- 30 days, rotation on every refresh: old session revoked, new session created, old refresh token cannot be reused (tested), new refresh token works.

## CSRF Mechanism

- Double submit cookie pattern: CSRF token stored in non-HttpOnly cookie nv_csrf and its hash stored in auth_sessions.csrf_token_hash
- For state-changing authenticated requests (logout, refresh, password-reset confirm via session, etc.), client must send X-CSRF-Token header with raw CSRF token value that matches cookie value and whose hash matches stored hash
- Validation in `core/csrf.py`: get cookie nv_csrf, get header X-CSRF-Token, compare equality, hash cookie token and compare with stored csrf_token_hash, raise 403 if missing/mismatch/invalid
- Required for: POST /auth/logout, POST /auth/refresh, POST /auth/password-reset/request? No, request is not authenticated but still rate limited, but per spec refresh and logout require CSRF, and other state-changing authenticated endpoints.

## Rate Limits (In-Memory MVP)

Simple in-memory rate limiting for MVP, documented that Redis-backed distributed rate limiting will be added later for multi-instance.

- register: 5 requests / hour / IP
- login: 10 requests / 15 minutes / IP
- password-reset request: 5 requests / hour / IP
- refresh: 30 requests / hour / session/user (keyed by IP + refresh token prefix for MVP)

Implementation in `core/rate_limit.py`: dict of deque timestamps, sliding window, returns True if rate limited (429). Storage in-memory, not distributed, acceptable for MVP single instance. Future: Redis with sliding window.

## Password Rules

- minimum 10 characters
- must include at least one letter
- must include at least one number
- reject common weak passwords: password, 123456, 123456789, qwerty, admin123, test123456 (exact match case-insensitive)
- Implemented in `core/security.py` validate_password_strength returns (is_valid, error_message)
- Tested: weak password rejected, strong passes

## Token Hashing

- Raw tokens never stored, only hashes stored via SHA256 hash_token(raw_token) = sha256(raw_token)
- For session: session_token_hash unique indexed, refresh_token_hash unique indexed, csrf_token_hash (not necessarily unique but stored hashed), password reset token_hash unique indexed
- Raw tokens returned only once in Set-Cookie headers (session, refresh, csrf) or via service layer for password reset token in tests (not public API - public API returns generic message)
- Hashing functions: hash_token (SHA256), hash_ip, hash_user_agent (SHA256 truncated 64 chars) for privacy, not storing raw IP/UA
- Never log passwords or raw tokens - code avoids logging raw values

## Why localStorage is Banned

- localStorage is accessible to JavaScript, vulnerable to XSS: attacker injected script can read localStorage and exfiltrate JWT/session tokens, leading to account takeover
- HttpOnly cookies not accessible to JS, mitigates XSS theft
- Additionally, HttpOnly + Secure + SameSite Lax protects against CSRF when combined with CSRF token double submit
- Hard rule: Do not store JWT or session tokens in localStorage - enforced via grep/assert no localStorage usage in backend (test_security_scans)

## Password Reset Skeleton

- **Request:** POST /auth/password-reset/request body email, always returns generic message "If an account with that email exists, a password reset link has been created." Rate limited 5/hour/IP, if user exists create password_reset_token (hashed only stored, raw token not stored, not exposed in production). For tests, expose token only through service layer, not public API (service returns raw token for test verification).
- **Confirm:** POST /auth/password-reset/confirm body token, new_password, validates token hash exists, not used, not expired (1 hour expiry), validates password strength, updates password_hash, marks token used_at, revokes all existing sessions for that user (all auth_sessions revoked_at set). Used token cannot be reused, expired token fails.
- **No email sending yet:** Do not send email yet per scope, for tests token exposed via service layer only, not public API. Future: email provider will send link with token.
- **Security:** Token stored hashed only, raw never stored, token single use, expires 1 hour, all sessions revoked after reset.

## Security Limitations Deferred to Later

- **Redis rate limiting:** Current in-memory, not distributed, acceptable for MVP single instance. Future: Redis-backed sliding window for multi-instance.
- **Email/SMS provider:** No real email sending for password reset yet, skeleton only. Future: email provider integration.
- **Device management UI:** No session list UI yet (list active sessions, revoke specific device). Future.
- **Session list UI:** Future: GET /auth/sessions list active sessions.
- **2FA:** Not in this PR, future.
- **Audit log:** No dedicated audit log table yet for auth events (login, logout, refresh, password reset). Future: audit log table.

## API Endpoints

- POST /auth/register: email, password, normalize email via lower(trim), reject duplicate normalized_email, create user, create wallet automatically if not exists, create auth session, set cookies nv_session, nv_refresh, nv_csrf, return sanitized user object (id, email, role, is_active, created_at, no password_hash)
- POST /auth/login: email, password, normalize email, generic error 401 Invalid email or password for invalid credentials, inactive user cannot login, create auth session, set cookies, return sanitized user
- POST /auth/logout: requires valid session (get_current_user), requires CSRF header X-CSRF-Token matching cookie and stored hash, revokes current session (revoked_at), clears cookies (delete_cookie)
- POST /auth/refresh: requires refresh cookie nv_refresh and CSRF header, verifies refresh token hash exists, not revoked, not expired, rotates session and refresh tokens (old refresh invalidated, new session created), sets new cookies
- GET /auth/me: requires valid session via nv_session cookie, returns sanitized current user, fails without cookie 401, fails with revoked session 401, fails with expired session 401
- POST /auth/password-reset/request: email, always generic response, if user exists create password_reset_token hashed only, do not send email yet, do not expose token in production response, for tests expose via service layer
- POST /auth/password-reset/confirm: token, new_password, validate token hash exists not used not expired, validate password strength, update password_hash, mark token used_at, revoke all existing sessions for that user

## Authorization Helpers

- get_db(): yields SessionLocal
- get_current_user(request, db): reads nv_session cookie, hashes, looks up auth_sessions by session_token_hash, checks revoked_at None, expires_at > now (timezone aware), updates last_used_at, gets user by user_id, checks is_active, attaches session to request.state, returns user, raises 401 if any fails
- require_admin(current_user): checks role == "admin", raises 403 if not admin, do not create broad admin business endpoints in this PR

## Tests

See backend/tests/ - 23+ tests covering registration, login, me, logout, refresh, CSRF, password reset, rate limiting, security scans, migration, etc. All must pass. PostgreSQL tests via Testcontainers for real migration verification.

## No Secrets

- No real API keys, payment keys, email credentials, SMS keys, production secrets in repo
- .env.example contains placeholder CHANGE_ME_RANDOM_SECRET
- No raw tokens or passwords logged
- No localStorage usage in backend (grep/assert)
- No AI provider logic, no wallet debit/credit business logic, no payment gateway
