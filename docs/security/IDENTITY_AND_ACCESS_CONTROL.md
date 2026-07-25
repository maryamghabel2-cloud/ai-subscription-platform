# Identity and Access Control

**Version:** v0.1.0

**Date:** 2026-07-24

**Status:** Proposed Architecture - Pending Owner Approval and Implementation

**Document Owner:** Security Architect

**Purpose:** Define authentication, authorization, least privilege, session
security, tenant isolation, admin access, and service and Agent identities.

**Note:** Implementation Evidence: This documentation PR does not prove that the described controls are implemented, tested, deployed, or production-ready. Code, automated tests, deployment evidence, and security verification remain the authoritative implementation evidence.

## Purpose

Define how identities are established, authenticated, and authorized, and how
access is controlled across Web, Mobile, Telegram, and API.

## In Scope

- Authentication:
  - Registration, login, password hashing (bcrypt with pre-hash for 72 bytes)
  - Opaque session tokens HttpOnly, Secure, SameSite, CSRF non-HttpOnly
  - Refresh token rotation, CONFIGURED_SESSION_LIFETIME session, CONFIGURED_REFRESH_LIFETIME refresh, revoke on logout
- Authorization:
  - RBAC/ABAC for users, roles, personas, agents, studios
  - Wallet: user can only access own wallet, balance never negative at DB and code
- Least privilege:
  - Users, agents, services get minimal permissions, no sharing, no cross-user
- Session security:
  - get_client_ip only trusts X-Forwarded-For if in TRUSTED_PROXIES
  - Rate limiting: register CONFIGURED_RATE_LIMIT, login CONFIGURED_RATE_LIMIT with CONFIGURED_LOCKOUT_THRESHOLD, password-reset, refresh
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

## Object-Level Authorization and IDOR/BOLA Defense

It must require:

- Authorization on every object-level read and write
- User and tenant identity derived from the trusted authenticated context
- Never trusting user_id, owner_id, tenant_id, wallet_id, conversation_id,
  file_id, payment_id, API key ID, or Agent execution ID supplied by the
  client as proof of ownership
- Service-layer ownership and tenant checks (e.g., check wallet.user_id ==
  authenticated user_id, conversation.user_id == authenticated user_id)
- Repository/query-layer tenant scoping (e.g., SELECT ... WHERE user_id = :auth_user_id,
  FK RESTRICT, unique constraints)
- Defense-in-depth database isolation (e.g., RLS where appropriate, row-level
  security, foreign keys, unique constraints, ownership constraints)
- Database row-level security where appropriate (e.g., Postgres RLS policies)
- Foreign keys, unique constraints, and ownership constraints (e.g.,
  uq_wallets_user_id, uq_ledger_idempotency_key, conversations user_id FK)
- Protection against horizontal and vertical privilege escalation (e.g., user
  cannot access other user's wallet, cannot escalate to admin)
- Uniform non-enumerating unauthorized responses (e.g., return 404 or 403
  without revealing existence, same response for not found and unauthorized)
- No assumption that UUIDs or unguessable IDs provide authorization (UUID is not
  proof of ownership, must still check ownership)
- Negative tests for cross-user and cross-tenant access (e.g., test that user A
  cannot read user B's wallet, conversation, file, payment intent)
- Audit events for repeated unauthorized object access attempts (e.g., log
  pseudonymous user id, object type, object id hash, timestamp, result, no raw
  sensitive content)

Explicitly connect this section to:

- Wallets: wallet.user_id must equal authenticated user_id, check before read/write
- Ledger entries: ledger.user_id or wallet_id must equal authenticated, no cross-user
- Payment intents: payment_intent.user_id must equal authenticated, no cross-user
- Conversations: conversation.user_id must equal authenticated
- Messages: message.conversation_id must belong to user's conversation
- Files: file.user_id or conversation_id must belong to user, no cross-user
- Memories: memory.user_id must equal authenticated, memory policy per Role
- API keys: api_key.user_id must equal authenticated, key_prefix and key_hash unique
- Agent executions: agent_execution.user_id must equal authenticated, no cross-user
- Studio jobs: studio_job.user_id must equal authenticated, no cross-user

Keep implementation details provider-neutral (e.g., Postgres RLS, SELECT FOR UPDATE,
FK RESTRICT, unique indexes, pseudonymous identifiers).

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

Proposed Architecture - Pending Owner Approval and Implementation. Implementation and verification are separate future work. Open Decisions remain unresolved until explicitly approved.
