# Secrets and Key Management

**Purpose:** Define principles for secrets, API keys, tokens, and cryptographic key management.

**Status:** Draft - Structure Only

**Note:** This is a structure-only stub. Final secrets management policy will be completed in later PRs. No real secrets are contained in this stub.

## Scope

This document will cover:

- Types of secrets: provider API keys, Telegram bot tokens, payment provider keys, session secrets, HMAC fingerprint secrets
- Storage: environment variables, encrypted at rest, no secrets in code, logs, or git history
- Generation: random, sufficient entropy, versioned, rotatable
- Distribution: least privilege, need-to-know, no sharing in plain text
- Rotation and revocation: regular rotation, emergency revocation, audit
- Detection: secret scanning in CI, no `sk-`, `ghp_`, `BEGIN PRIVATE KEY` in docs
- Separation of secrets per environment: development, staging, production

Final policy will require security and DevOps review. No production secrets will be added in documentation PRs.

## Linkage

- Security Index: [README.md](README.md)
- Data Protection: [DATA_PROTECTION_AND_ENCRYPTION.md](DATA_PROTECTION_AND_ENCRYPTION.md)
- Provider Abstraction: [../architecture/PROVIDER_ABSTRACTION_STRATEGY.md](../architecture/PROVIDER_ABSTRACTION_STRATEGY.md)

## Status

Draft - Structure Only. Will be completed later.
