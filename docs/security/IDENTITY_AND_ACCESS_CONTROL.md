# Identity and Access Control

**Version:** v0.1.0

**Date:** 2026-07-24

**Status:** Draft - Structure Only

**Document Owner:** Security Architect

**Purpose:** Define authentication, authorization, least privilege, session
security, tenant isolation, admin access, and service and Agent identities.

**Note:** This is a structure-only stub. Final policy will be completed later.

## Purpose

Define how identities are established, authenticated, and authorized, and how
access is controlled across Web, Mobile, Telegram, and API.

## In Scope

- Authentication:
  - Registration, login, password hashing (bcrypt with pre-hash for 72 bytes)
  - Opaque session tokens HttpOnly, Secure, SameSite, CSRF non-HttpOnly
  - Refresh token rotation, 30min session, 30 days refresh, revoke on logout
- Authorization:
  - RBAC/ABAC for users, roles, personas, agents, studios
  - Wallet: user can only access own wallet, balance never negative at DB and code
- Least privilege:
  - Users, agents, services get minimal permissions, no sharing, no cross-user
- Session security:
  - get_client_ip only trusts X-Forwarded-For if in TRUSTED_PROXIES
  - Rate limiting: register 5/hour, login 10/15min, password-reset, refresh
  - Secure get_client_ip, no X-Forwarded-For trust unless trusted proxy
- Tenant isolation:
  - User data, conversations, messages, wallets, API keys isolated per user id
  - FK RESTRICT, unique indexes, no cross-user access, pseudonymous identifiers
    in logs
- Admin access:
  - Admin grant requires approval, audit logging, no secret sharing
  - Admin actions outside business hours are detection signal
  - Multiple failed authorization attempts are detection signal
- Service and Agent identities:
  - agent_plugins registry, permissions allow/forbid/approval-required
  - Absolutely forbidden NO-GO: ToS bypass, geographic/sanctions/KYC bypass,
    fake identities, sharing unauthorized credentials, CSAM, non-consensual imagery
  - Service API keys hashed, scopes, rate limiting, revocable
- Channel adapter auth:
  - Web HttpOnly cookies, Mobile secure storage, Telegram webhook authenticity
    verified via X-Telegram-Bot-Api-Secret-Token, API X-API-Key hashed

## Out of Scope

- Final password policy numbers and exact rate limits (CONFIGURED_LIMIT)
- Final session lifetimes and MFA rollout stage (future PRs)
- Implementation code and exact lockout policy (future)

## Related Documents

- Security Index: [README.md](README.md)
- Agent Permission Model: [../agents/AGENT_PERMISSION_MODEL.md](../agents/AGENT_PERMISSION_MODEL.md)
- Human Approval Gates: [../agents/HUMAN_APPROVAL_GATES.md](../agents/HUMAN_APPROVAL_GATES.md)
- Agent Security Model: [AGENT_SECURITY_MODEL.md](AGENT_SECURITY_MODEL.md)
- Channel Security: [CHANNEL_SECURITY_TELEGRAM_WEB_MOBILE.md](CHANNEL_SECURITY_TELEGRAM_WEB_MOBILE.md)

## Open Decisions

- Exact session lifetimes, rate limit numbers, lockout policy
- MFA requirements and rollout stage
- Admin role definition and approval workflow
- Owner approval required for all decisions

## Planned Completion Stage

Phase 1 - Auth Hardening

## Status Note

Draft - Structure Only. Will be completed later.
