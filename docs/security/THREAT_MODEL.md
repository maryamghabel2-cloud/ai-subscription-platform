# Threat Model

**Version:** v0.1.0

**Date:** 2026-07-24

**Status:** Draft - Structure Only

**Document Owner:** Security Architect

**Purpose:** Define protected assets, threat actors, attack surfaces, trust
boundaries, threat categorization, and risk prioritization.

**Note:** This is a structure-only stub. Final threat model will be completed
later.

## Purpose

Define what we protect, who might attack, how they might attack, and how we
prioritize risks.

## In Scope

- Protected assets:
  - User accounts, wallets, ledgers (append-only ledger with positive and
    negative amount entries)
  - Payment intents, sandbox mock provider
  - Conversations, messages, uploaded files
  - API keys, prompts, generated images/videos
  - Telegram identifiers, session tokens, HMAC secrets
- Threat actors:
  - External attackers, malicious users, compromised agents
  - Supply-chain attackers, insider threats
- Attack surfaces:
  - Authentication, session management, wallet/ledger
  - Payment-intent, file upload, RAG context
  - Prompt injection, tool abuse, channel spoofing, API abuse, secret leakage
- Trust boundaries:
  - User ↔ channel adapter ↔ context assembly ↔ retrieval ↔ persona/agent
  - Wallet/ledger atomic operations
  - Payment sandbox isolation
- Threat categorization: STRIDE or similar
- Risk prioritization: likelihood, impact, mitigations, residual risk

## Out of Scope

- Final risk ratings and mitigation implementation (future PRs)
- Penetration test results (future)

## Related Documents

- Security Index: [README.md](README.md)
- Security Architecture: [SECURITY_ARCHITECTURE.md](SECURITY_ARCHITECTURE.md)
- Data Protection: [DATA_PROTECTION_AND_ENCRYPTION.md](DATA_PROTECTION_AND_ENCRYPTION.md)
- Agent Security Model: [AGENT_SECURITY_MODEL.md](AGENT_SECURITY_MODEL.md)

## Open Decisions

- Threat modeling methodology (STRIDE vs other)
- Exact asset inventory and data classification mapping
- Risk acceptance criteria
- Owner approval required

## Planned Completion Stage

Phase 1 - Threat Modeling

## Status Note

Draft - Structure Only. Will be completed later.
