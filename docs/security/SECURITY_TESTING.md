# Security Testing

**Purpose:** Define security testing, scanning, and verification strategy.

**Status:** Draft - Structure Only

**Note:** This is a structure-only stub. Final security testing policy will be completed in later PRs.

## Scope

This document will cover:

- Types of testing: static analysis, dependency scanning, secret scanning, container scanning, dynamic scanning, penetration testing, red-teaming, prompt injection testing
- Persona QA and red-teaming: care_truthfulness_policy, belief_validation_policy, professional_handoff_policy, crisis_response_policy, prohibited_authority_claims
- Agent security testing: permission model, tool allowlisting, budget enforcement, approval gates
- Channel security testing: Telegram, Web, Mobile input validation, auth, rate limiting
- Wallet and payment security testing: atomic credit/debit, balance never negative, idempotency, sandbox vs real provider isolation
- Data protection testing: encryption, retention, deletion, anonymization
- Continuous scanning: CI secret scan, dependency updates, vulnerability management
- No production data in testing, no real secrets in tests

Final policy will require security, QA, and engineering review.

## Linkage

- Security Index: [README.md](README.md)
- Persona QA: [../personas/PERSONA_QA_AND_RED_TEAMING.md](../personas/PERSONA_QA_AND_RED_TEAMING.md)
- Agent Security Model: [AGENT_SECURITY_MODEL.md](AGENT_SECURITY_MODEL.md)

## Status

Draft - Structure Only. Will be completed later.
