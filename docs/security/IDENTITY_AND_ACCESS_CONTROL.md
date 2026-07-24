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
access is controlled.

## In Scope

- Authentication:
  - Registration, login, password hashing (bcrypt with pre-hash)
  - Opaque session tokens HttpOnly, Secure, SameSite
  - CSRF non-HttpOnly, refresh token rotation, 30min session / 30 days refresh
- Authorization:
  - RBAC/ABAC for users, roles, personas, agents, studios
  - Wallet: user can only access own wallet, balance never negative
- Least privilege:
  - Users, agents, services get minimal permissions, no sharing
- Session security:
  - get_client_ip only trusts X-Forwarded-For if in TRUSTED_PROXIES
  - Rate limiting (register, login, password-reset, refresh)
- Tenant isolation:
  - User data, conversations, messages, wallets, API keys isolated per user
  - FK RESTRICT, no cross-user access
- Admin access:
  - Admin grant requires approval, audit logging, no secret sharing
- Service and Agent identities:
  - agent_plugins registry, permissions allow/forbid/approval-required
  - Absolutely forbidden NO-GO, service API keys hashed
- Channel adapter auth:
  - Web HttpOnly cookies, Mobile secure storage, Telegram webhook, API X-API-Key

## Out of Scope

- Final password policy numbers and exact rate limits (CONFIGURED_LIMIT)
- Final session lifetimes and MFA rollout (future PRs)
- Implementation code (future)

## Related Documents

- Security Index: [README.md](README.md)
- Agent Permission Model: [../agents/AGENT_PERMISSION_MODEL.md](../agents/AGENT_PERMISSION_MODEL.md)
- Human Approval Gates: [../agents/HUMAN_APPROVAL_GATES.md](../agents/HUMAN_APPROVAL_GATES.md)
- Agent Security Model: [AGENT_SECURITY_MODEL.md](AGENT_SECURITY_MODEL.md)

## Open Decisions

- Exact session lifetimes, rate limit numbers, lockout policy
- MFA requirements and rollout stage
- Admin role definition and approval workflow
- Owner approval required

## Planned Completion Stage

Phase 1 - Auth Hardening

## Status Note

Draft - Structure Only. Will be completed later.
