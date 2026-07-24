# Secrets and Key Management

**Version:** v0.1.0

**Date:** 2026-07-24

**Status:** Draft - Structure Only

**Document Owner:** Security Architect / DevOps

**Purpose:** Define provider API keys, payment credentials, Telegram bot tokens,
encryption keys, secret storage, rotation, revocation, and leak detection.

**Note:** This is a structure-only stub. No real secrets are contained. Final
policy will be completed later.

## Purpose

Define how secrets are stored, generated, distributed, rotated, and revoked
without leaking.

## In Scope

- Provider API keys:
  - AI provider keys via provider abstraction, env vars, encrypted at rest
  - No hardcoding, no logging, no client exposure
- Payment credentials:
  - ZarinPal future, crypto verification TRC20/TON future
  - Sandbox mock provider exists for development and testing
  - Real gateways not active, sandbox completion must never be enabled in prod
- Telegram bot tokens:
  - Ordinary users link account to platform's bot, do not provide token
  - Business customers may connect own token via reviewed integration where
    token is encrypted at rest
  - Webhook authenticity verified, no secret in logs
- Encryption keys:
  - HMAC fingerprint secret for APPROVED_KEYED_HMAC_ONLY_IF_REQUIRED
  - Protected, environment-specific, versioned, rotatable
- Secret storage:
  - Environment variables, secret manager, encrypted at rest
  - No secrets in code, git history, logs, or client
- Rotation:
  - Regular schedule, emergency rotation on compromise, versioned secrets
- Revocation:
  - Immediate revocation, audit trail, user notification if needed
- Leak detection:
  - CI secret scanning, pre-commit hooks, GitHub scanning
  - No raw `sk-` , raw `ghp_` tokens, no `BEGIN PRIVATE KEY` raw in repo

## Out of Scope

- Actual secret values and production key material (forbidden in docs PR)
- Final rotation schedule and tooling (future PRs)
- Provider connection (forbidden)

## Related Documents

- Security Index: [README.md](README.md)
- Data Protection: [DATA_PROTECTION_AND_ENCRYPTION.md](DATA_PROTECTION_AND_ENCRYPTION.md)
- Provider Abstraction: [../architecture/PROVIDER_ABSTRACTION_STRATEGY.md](../architecture/PROVIDER_ABSTRACTION_STRATEGY.md)
- Channel Security: [CHANNEL_SECURITY_TELEGRAM_WEB_MOBILE.md](CHANNEL_SECURITY_TELEGRAM_WEB_MOBILE.md)

## Open Decisions

- Secret manager choice (env vs managed service)
- Rotation frequency and emergency procedure
- Detection tooling and CI integration
- Owner approval required

## Planned Completion Stage

Phase 1 - Secrets

## Status Note

Draft - Structure Only. Will be completed later.
