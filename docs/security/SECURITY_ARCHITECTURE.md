# Security Architecture

**Version:** v0.1.0

**Date:** 2026-07-24

**Status:** Proposed Architecture - Pending Owner Approval and Implementation

**Document Owner:** Security Architect (Founder)

**Purpose:** Define detailed, implementation-ready Zero Trust and Defense in Depth
policy. Explain trust boundaries, assume-breach model, and security applied from
Phase 1 for Web, Mobile, Telegram, API, AI, Agent, Studio, and data.

**Note:** Implementation Evidence: This documentation PR does not prove that the described controls are implemented, tested, deployed, or
production-ready. Code, automated tests, deployment evidence, and security verification remain the authoritative implementation evidence. No
production code in this PR.

## Purpose

Define Zero Trust and Defense in Depth architecture for the Persian-first
multimodal AI Workspace.

## In Scope

- Zero Trust principles, Defense in Depth layers, trust boundaries,
  assume-breach model
- Mapping of Defense in Depth layers to merged foundations and planned product
  features (Auth, Wallet, Chat, etc.)

Make clear that merged foundations do not prove every documented security control is implemented or verified. Auth and Wallet may only be called
MERGED FOUNDATIONS, not implemented controls.
- Web, Mobile, Telegram, API, AI provider, payment provider, internal
  services, third-party agents, admin access

## Out of Scope

- Final implementation details and exact enforcement code (future PRs)
- Production network diagrams and concrete tooling choices

## Zero Trust Principles

### Never Trust, Always Verify

- Every request must be authenticated and authorized, regardless of source
- No implicit trust between internal services or components
- Verify authenticity of Telegram webhooks using
  X-Telegram-Bot-Api-Secret-Token header on every incoming webhook
- Verify authenticity of payment callbacks and external callbacks

### Assume Breach

- Assume attacker may already be inside one layer, design to limit blast radius
- No single layer is sufficient, multiple layers must fail for breach to succeed
- Agent tool outputs and RAG retrieved content are treated as untrusted and
  must be validated before use

### Least Privilege for Every Identity

- Users: can only access own wallet, conversations, API keys, uploaded files
- Agents: receive only specific scoped credentials they need, separate from
  platform credentials, revocable independently
- Services: minimal permissions, no sharing of full environment secrets
- Admins: admin grant requires approval, audit logging, no secret sharing

### Micro-Segmentation

- Separate trust zones: public Web/Mobile/Telegram/API, application, data,
  provider integrations, third-party agents
- Wallet and ledger atomic operations with SELECT FOR UPDATE, balance never
  negative enforced at DB and code, append-only ledger with positive and
  negative amount entries (not cryptographic signatures)
- Payment sandbox isolation: sandbox-only mock provider exists for development
  and testing, real gateways and blockchain verification not active, sandbox
  completion must never be enabled in production

### Continuous Validation

- Session validation on every request, HttpOnly Secure SameSite cookies, CSRF
- Rate limiting on all authentication and sensitive endpoints
- Continuous monitoring for anomaly detection and alerting
- Immutable audit trail, tamper-resistant logs, no raw sensitive content

## Defense in Depth Layers

### Network Perimeter

- TLS everywhere, HSTS, no plaintext sensitive data
- Firewall and network segmentation for internal services

### Transport Security (TLS Everywhere)

- TLS 1.2+ for Web, Mobile, Telegram webhook, API, AI provider, payment provider
- Certificate validation, no downgrade, HSTS headers

### Application Authentication and Authorization

- Opaque session tokens HttpOnly, refresh token rotation
- RBAC/ABAC for users, roles, personas, agents, studios
- API keys hashed, scopes, rate limits, revocable
- Tenant isolation: FK RESTRICT, no cross-user data access

### Input Validation and Output Guardrails

- Strict input validation for all user-facing templates and APIs
- Output encoding to prevent XSS
- Prompt injection defense: system instructions in separate immutable segment,
  user content and retrieved content always treated as untrusted
- Output guardrails: AI output must never contain raw API keys, secrets, tokens,
  scanned for data-exfiltration patterns before delivery

### Data Encryption at Rest and in Transit

- Encryption at rest: database, file storage, secrets, backups
- Encryption in transit: TLS for all channels
- Field-level encryption for sensitive fields
- Key management: environment-specific, versioned, rotatable secrets

### Secrets and Key Management

- No secrets in source code, git history, documentation, logs, or HTTP responses
- Managed secret storage is the production/staging source of truth (e.g., Vault,
  AWS Secrets Manager, dedicated secrets manager)
- Environment variables are only controlled runtime injection (e.g., secrets
  manager injects env var at runtime, env var is not source of truth)
- Secrets in dedicated secrets manager, each environment separate secrets
- Development secrets never used in production
- Rotation without code deployment, planned rotation may use bounded overlap:
  CONFIGURED_SECRET_ROTATION_GRACE_PERIOD (old secret remains valid for
  CONFIGURED_SECRET_ROTATION_GRACE_PERIOD during planned rotation)
- Suspected or confirmed compromised credentials must be revoked or disabled
  immediately (no waiting, immediate revocation, no grace period for compromised)
- A compromised credential receives no grace period (compromised credentials
  are revoked immediately, no overlap)
- Replacement credentials must be issued and dependent services recovered
  (issue new secret, update secrets manager, restart dependent services,
  verify recovery, audit log)
- Grace period CONFIGURED_SECRET_ROTATION_GRACE_PERIOD, audit trail

### Agent Sandboxing

- Approved agents run in sandboxed environment, no inheritance of full env
- Tool allowlists, permission boundaries, network allowlists, budgets
  CONFIGURED_AGENT_MAX_COST_CREDITS, human approval gates
- Agent isolation, secret isolation, no cross-user access

### Logging and Anomaly Detection

- Privacy-preserving technical logs, no raw sensitive prompts
- content_fingerprint DISABLED_BY_DEFAULT, fingerprint_method
  APPROVED_KEYED_HMAC_ONLY_IF_REQUIRED
- Security events, anomaly detection, alerting, log integrity

### Incident Response

- Severity definitions, containment, credential compromise, data exposure,
  agent compromise, recovery, post-incident review
- Human approval required for high-impact actions, reversible protective actions

## Trust Boundaries

### User to Web/Mobile/Telegram/API

- Web: CSP, HSTS, HttpOnly Secure SameSite cookies, CSRF, rate limiting
- Mobile: secure local storage, app lock with biometric, certificate pinning,
  no sensitive content in push payloads, screenshot privacy, local cache
  encryption, user-controlled deletion
- Telegram: honest limitations – not end-to-end encrypted, stores messages on
  servers, bots receive all private messages, must never claim end-to-end
  encrypted, convenience channel, minimize identifiers, tokens encrypted at rest,
  webhook authenticity verified, non-retention by default unless user enables
- API: short-lived or rotatable keys, hashed, scopes, rate limits, logged,
  revocable without disruption

### Application to AI Providers

- Provider abstraction, API keys stored in secrets manager, no logging of raw
  keys, cost tracking, model output validation, no raw sensitive content in logs

### Application to Payment Providers

- Sandbox-only mock provider exists for development and testing
- Real gateways and blockchain verification not active
- Payment callback from unexpected source is detection signal
- Wallet credit/debit atomic, ledger append-only, balance never negative

### Internal Services to Each Other

- No implicit trust, authenticated and authorized, least privilege
- Audit trail for service-to-service calls

### Third-Party Agents to the Platform

- Security review mandatory before approval: source verification, license,
  dependency and supply-chain scan, static/dynamic analysis, prompt injection
  test, tool abuse test, data exfiltration test
- Approved manifest required: id, name, version, author, source, license,
  checksum, runtime type, required tools, permissions, network allowlist,
  secret requirements, max cost, max execution time, max iterations, human
  approval gates, risk level, review status, rollback version
- Runtime isolation: sandboxed, no full env, network and tool allowlists
- Re-review on update and on CONFIGURED_THRESHOLD cadence

### Admins to the System

- Admin access requires approval, audit logging, no secret sharing
- Admin actions outside business hours are detection signal
- Multiple failed authorization attempts are detection signal

## Security Applied from Phase 1

### Mapping Defense in Depth Layers to Product Features

- Network perimeter + TLS: Web, Mobile, Telegram webhook, API, AI provider,
  payment provider integrations – planned from Phase 1
- Application Auth/AuthZ: Phase 1 Database (users), Authentication (opaque
  session tokens), Wallet (own wallet only) – MERGED FOUNDATIONS, Auth and Wallet
  foundations implemented, real payment providers not active
- Input validation/output guardrails: Prompt Enhancer, file upload scanning,
  RAG provenance – Phase 1 and Phase 2
- Data encryption: Phase 1 Database and Wallet, field-level encryption for
  API keys hashed – planned
- Secrets and key management: Phase 1 – env vars, encrypted at rest
  tested, no secrets in docs – planned
- Agent sandboxing: Phase 1 Agent Security Model, tool allowlists, budgets
  CONFIGURED_AGENT_MAX_COST_CREDITS, human approval gates – planned
- Logging and anomaly detection: Phase 1 Logging, privacy-preserving logs,
  anomaly detection, alerting – planned
- Incident response: Phase 1 IR – severity, containment, recovery – planned

### Auth, Wallet, and Chat Security Requirements

- Auth: password hashing bcrypt with pre-hash, opaque session tokens HttpOnly,
  Secure, SameSite, CSRF, refresh rotation, rate limiting CONFIGURED_RATE_LIMIT,
  get_client_ip only trusts X-Forwarded-For if in TRUSTED_PROXIES, no
  localStorage for sensitive data
- Wallet: user can only access own wallet, atomic credit/debit with SELECT FOR
  UPDATE, balance never negative at DB and code, ledger append-only ledger
  with positive and negative amount entries (not cryptographic signatures),
  idempotency, payment intent sandbox foundation implemented, sandbox-only mock
  provider, real gateways not active, sandbox completion must never be enabled
  in production
- Chat: conversation-only Roles do not execute tools, Specialist Personas may
  use approved Knowledge Base via Retrieval Service with citations, no
  autonomous browsing, no legal/medical/psych authority claims, care_truthfulness
  and belief_validation policies, professional handoff, crisis response

## Related Documents

- Security Index: [README.md](README.md)
- System Context: [../architecture/SYSTEM_CONTEXT.md](../architecture/SYSTEM_CONTEXT.md)
- Boundaries: [../architecture/ROLE_PERSONA_AGENT_BOUNDARIES.md](../architecture/ROLE_PERSONA_AGENT_BOUNDARIES.md)
- Data Protection: [DATA_PROTECTION_AND_ENCRYPTION.md](DATA_PROTECTION_AND_ENCRYPTION.md)
- Identity and Access: [IDENTITY_AND_ACCESS_CONTROL.md](IDENTITY_AND_ACCESS_CONTROL.md)
- Channel Security: [CHANNEL_SECURITY_TELEGRAM_WEB_MOBILE.md](CHANNEL_SECURITY_TELEGRAM_WEB_MOBILE.md)
- Agent Security Model: [AGENT_SECURITY_MODEL.md](AGENT_SECURITY_MODEL.md)

## Open Decisions

- Exact trust boundary diagrams and data flow diagrams
- Zero Trust control matrix per component and per channel
- Defense in Depth mapping to specific product features and stages
- Owner approval required for all decisions
- Tooling choices for enforcement and monitoring

## Planned Completion Stage

Phase 1 - Security Foundations

## Status Note

Proposed Architecture - Pending Owner Approval and Implementation. Implementation and verification are separate future work. Open Decisions remain
unresolved until explicitly approved.
