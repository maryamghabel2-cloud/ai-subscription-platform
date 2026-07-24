# Threat Model

**Version:** v0.1.0

**Date:** 2026-07-24

**Status:** Draft - Structure Only

**Document Owner:** Security Architect

**Purpose:** Define protected assets, threat actors, attack surfaces, trust boundaries, threat categorization, and risk prioritization.

**Note:** This is a structure-only stub. Final threat model will be completed in later PRs.

## In Scope

- Protected assets: user accounts, wallets, ledgers (append-only ledger with positive and negative amount entries), payment intents, sandbox mock provider, conversations, messages, uploaded files, API keys, prompts, generated images/videos, Telegram identifiers, session tokens, HMAC fingerprint secrets
- Threat actors: external attackers, malicious users, compromised agents, supply-chain attackers, insider threats
- Attack surfaces: authentication, session management, wallet/ledger, payment-intent, file upload, RAG context, prompt injection, tool abuse, channel spoofing (Telegram webhook), API abuse, secret leakage
- Trust boundaries: user ↔ channel adapter ↔ context assembly ↔ retrieval service ↔ persona/agent ↔ provider; wallet/ledger atomic operations; payment sandbox isolation
- Threat categorization: STRIDE or similar, with examples per category
- Risk prioritization: likelihood, impact, existing mitigations, residual risk

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

## Planned Completion Stage

- Phase 1 - Threat Modeling

## Status

Draft - Structure Only. Will be completed later.
