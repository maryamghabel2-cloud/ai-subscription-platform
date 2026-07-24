# Identity and Access Control

**Version:** v0.1.0

**Date:** 2026-07-24

**Status:** Draft - Structure Only

**Document Owner:** Security Architect

**Purpose:** Define authentication, authorization, least privilege, session security, tenant isolation, admin access, and service/agent identities.

**Note:** This is a structure-only stub. Final policy will be completed later.

## In Scope

- Authentication: registration, login, password hashing (bcrypt with pre-hash), opaque session tokens HttpOnly, Secure, SameSite, CSRF non-HttpOnly, refresh token rotation, 30min session / 30 days refresh
- Authorization: RBAC/ABAC for users, roles, personas, agents, studios, wallet (user can only access own wallet, balance never negative enforced at DB and code)
- Least privilege: users, agents, services get minimal permissions, no sharing
- Session security: get_client_ip only trusts X-Forwarded-For if in TRUSTED_PROXIES, rate limiting (register 5/hour, login 10/15min, password-reset, refresh)
- Tenant isolation: user data, conversations, messages, wallets, API keys isolated per user id, FK RESTRICT, no cross-user access
- Admin access: admin grant requires approval, audit logging, no secret sharing
- Service and Agent identities: agent_plugins registry, permissions (allow/forbid/approval-required), absolutely forbidden NO-GO, service API keys hashed
- Channel adapter auth: Web HttpOnly cookies, Mobile secure storage, Telegram webhook authenticity, API X-API-Key with hashed storage and scopes

## Out of Scope

- Final password policy numbers, exact rate limits (CONFIGURED_LIMIT placeholders), final session lifetimes (future PRs)
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

## Planned Completion Stage

- Phase 1 - Auth Hardening

## Status

Draft - Structure Only. Will be completed later.
