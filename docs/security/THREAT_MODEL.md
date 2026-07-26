# Threat Model

**Version:** v0.1.0

**Date:** 2026-07-24

**Status:** Proposed Architecture - Pending Owner Approval and Implementation

**Document Owner:** Security Architect

**Purpose:** Define structured threat model with protected assets, threat actors,
attack surfaces, trust boundaries, threat categorization, and priority risk table.

**Note:** Implementation Evidence: This documentation PR does not prove that the described controls are implemented, tested, deployed, or
production-ready. Code, automated tests, deployment evidence, and security verification remain the authoritative implementation evidence.

## Purpose

Define what we protect, who might attack, how they might attack, and how we
prioritize risks.

## In Scope

- Protected assets, threat actors, attack surfaces, trust boundaries
- Threat categorization using STRIDE-inspired approach
- Priority risk table with Likelihood, Impact, Priority, Mitigation

## Out of Scope

- Final risk ratings and detailed mitigation implementation (future PRs)
- Penetration test results and exact exploit details (future)

## Protected Assets

### User Conversations and Memory

- Conversations, messages, memory policy per Role, session_only options
- Mental health and sensitive personal content: trauma, migration, private files
- Must not be in technical logs by default, only encrypted product-data store

### Mental Health and Sensitive Personal Content

- Evidence-based mental health info assistant, not psychologist
- Requires care_truthfulness_policy, belief_validation_policy, handoff, crisis
- No diagnosis, no uncritical agreement, no intensifying paranoia

### Uploaded Files and Images

- File, image, PDF attachments for analysis, RAG, product photography
- Must be scanned before extraction, quarantined if suspicious

### Wallet and Credit Balances

- Wallets table balance_credits check >=0, ledger_transactions append-only
  ledger with positive and negative amount entries
- Atomic credit/debit with SELECT FOR UPDATE, idempotency, balance never negative

### Provider API Keys and Payment Credentials

- AI provider keys via abstraction, secrets manager, encrypted at rest
- Payment gateway credentials: ZarinPal future, crypto TRC20/TON future,
  sandbox mock provider exists for dev/test, real gateways not active

### Telegram Bot Tokens

- Ordinary users link account to platform's bot, do not provide token
- Business customers may connect own token via reviewed integration where
  token encrypted at rest, webhook authenticity verified, no secret in logs

### Admin and Service Credentials

- Admin grant requires approval, audit logging
- Service credentials: agent_plugins, API keys hashed, scopes, rate limiting

### Encryption Keys

- HMAC fingerprint secret for APPROVED_KEYED_HMAC_ONLY_IF_REQUIRED
- Protected, env-specific, versioned, rotatable
- content_fingerprint DISABLED_BY_DEFAULT

### Session Tokens

- Opaque session tokens HttpOnly, Secure, SameSite, CSRF non-HttpOnly
- Refresh rotation, CONFIGURED_SESSION_LIFETIME session, CONFIGURED_REFRESH_LIFETIME refresh
- get_client_ip only trusts X-Forwarded-For if in TRUSTED_PROXIES

## Threat Actors

- External attackers: opportunistic, targeted, bots and scrapers
- Malicious users: abuse, fraud, prompt injection, exfiltration attempts
- Compromised agents: business, research, Telegram agents
- Malicious third-party agents: marketplace, supply-chain compromise
- Supply-chain attackers: dependency confusion, typosquatting, malicious pkgs
- Hostile AI: model extraction, prompt injection, jailbreak, tool abuse
- Insiders: employees, contractors, accidental or malicious
- Automated bots and scrapers: rate limit bypass, bulk, scraping
- Nation-state actors: APT, targeted surveillance

## Attack Surfaces

- Web application: Next.js App Router, auth, chat, file upload, wallet, API keys
- Mobile application: native or PWA, voice, camera, secure storage, push
  notifications, local cache encryption, user-controlled deletion
- Telegram bot webhook: X-Telegram-Bot-Api-Secret-Token header verification,
  group access disabled unless reviewed, group privacy enabled
- Developer API: keys short-lived or rotatable, hashed, scopes, rate limits,
  logged, revocable without disruption
- AI provider integration: provider abstraction, cost tracking, output validation,
  no raw sensitive content in logs
- Payment provider integration: sandbox mock, real gateways not active, payment
  callback from unexpected source is detection signal
- Agent tool calls: tool allowlists, permission boundaries, network allowlists,
  budgets CONFIGURED_LIMIT, human approval gates, secret isolation
- RAG and file upload inputs: file type validation, size limits, malware scan,
  provenance tagging, untrusted content quarantine
- Admin panel: admin access requires approval, audit logging, no secret sharing
- CI/CD pipeline: secret scanning, dependency scanning, SAST/DAST, no secrets
  in git history, no tokens in remote URLs

## Threat Categories (STRIDE-Inspired)

- Spoofing identity: session hijacking, Telegram webhook spoofing without secret,
  payment callback spoofing
- Tampering with data: wallet balance, ledger entries, payment intent state,
  RAG content, file upload, agent tool output
- Repudiation: user denies action, agent denies tool call, mitigation via
  immutable audit trail, append-only ledger, approval records, timestamps
- Information disclosure: conversations, files, wallet, API keys, provider keys,
  Telegram tokens, session tokens, encryption keys via logs or AI outputs
- Denial of service: rate limit bypass, bulk messages, expensive image gen,
  tool abuse, payment intent flooding
- Elevation of privilege: IDOR accessing other user's wallet, agent granting
  itself new permissions, disabling own audit logging
- Prompt injection and jailbreaking: direct, indirect, jailbreak, mitigation via
  separation of concerns, untrusted content handling, structured tool calls,
  output guardrails, jailbreak detection, provenance tagging
- Data exfiltration via AI outputs: tricking model into revealing user data,
  system prompts, credentials, mitigation via output guardrails, no raw secrets
- Agent tool abuse: using injection to trigger unauthorized tool calls: spend
  money, publish, contact customers, delete data, bypass geographic/KYC/ToS
- Supply-chain compromise: malicious dependency, third-party agent, compromised
  CI/CD token, secret leak, mitigation via dependency scanning, SBOM, source
  verification, re-review on CONFIGURED_LIMIT cadence

## Priority Risk Table

| Threat | Attack Surface | Likelihood | Impact | Priority | Mitigation |
|---|---|---|---|---|---|
| Spoofing session cookie | Web | Medium | High | High | HttpOnly Secure SameSite, rotation |
| Wallet tampering | Wallet ledger | Low | High | High | Atomic SELECT FOR UPDATE, never negative |
| Prompt injection override | Web Mobile Telegram API | High | High | High | Immutable system segment, untrusted handling |
| Exfiltration via AI output | AI integration | Medium | High | High | Guardrails, no raw secrets, block and log |
| Agent tool abuse spending | Agent tools | Medium | High | High | Allowlists, budgets, approval gates, NO-GO |
| IDOR wallet access | Web API Mobile | Medium | High | High | Tenant isolation, RBAC, least privilege |
| Payment callback spoof | Payment integration | Low | High | Medium | Webhook authenticity, sandbox isolation |
| Secret leak via logs | Logging | Medium | High | High | No raw prompts, DISABLED_BY_DEFAULT fingerprint |
| Telegram webhook spoof | Telegram webhook | Medium | Medium | Medium | Secret-Token header verification |
| Supply-chain third-party | Third-party agents CI/CD | Low | High | Medium | Source verify, SBOM, re-review cadence |
| RAG poisoning | RAG file upload | Medium | Medium | Medium | Provenance tagging, versioned removable |
| File upload malware | File upload | Medium | Medium | Medium | Type validation, size limits, quarantine |

## Related Documents

- Security Index: [README.md](README.md)
- Security Architecture: [SECURITY_ARCHITECTURE.md](SECURITY_ARCHITECTURE.md)
- Prompt Injection Defense: [PROMPT_INJECTION_DEFENSE.md](PROMPT_INJECTION_DEFENSE.md)
- Agent Security Model: [AGENT_SECURITY_MODEL.md](AGENT_SECURITY_MODEL.md)
- Data Protection: [DATA_PROTECTION_AND_ENCRYPTION.md](DATA_PROTECTION_AND_ENCRYPTION.md)

## Open Decisions

- Exact likelihood/impact/priority methodology and risk acceptance criteria
- Final priority risk table entries and mitigation details
- Tooling for threat modeling and tracking
- Owner approval required

## Planned Completion Stage

Phase 1 - Threat Modeling

## Status Note

Proposed Architecture - Pending Owner Approval and Implementation. Implementation and verification are separate future work. Open Decisions remain
unresolved until explicitly approved.
