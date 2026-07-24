# Secrets and Key Management

**Version:** v0.1.0

**Date:** 2026-07-24

**Status:** Draft - Structure Only

**Document Owner:** Security Architect / DevOps

**Purpose:** Define provider API keys, payment credentials, Telegram bot tokens, encryption keys, secret storage, rotation, revocation, and leak detection.

**Note:** This is a structure-only stub. No real secrets are contained. Final policy will be completed later.

## In Scope

- Provider API keys: AI provider keys (OpenAI, Anthropic, etc.) via provider abstraction, stored in environment variables, encrypted at rest, no hardcoding, no logging
- Payment credentials: ZarinPal (future), crypto verification (TRC20, TON future), sandbox mock provider exists for development and testing, real gateways not active, sandbox completion must never be enabled in production
- Telegram bot tokens: ordinary end users link account to platform's Telegram bot, do not provide token; future business customers may connect own bot token via separate reviewed integration where token is encrypted at rest, webhook authenticity verified, no secret in logs
- Encryption keys: HMAC fingerprint secret for APPROVED_KEYED_HMAC_ONLY_IF_REQUIRED use case, protected, environment-specific, versioned, rotatable
- Secret storage: environment variables, secret manager, encrypted at rest, no secrets in code, git history, logs, or client
- Rotation: regular rotation schedule, emergency rotation on compromise, versioned secrets
- Revocation: immediate revocation, audit trail, user notification if needed
- Leak detection: CI secret scanning (no `sk-` raw, no `ghp_` raw tokens, no `BEGIN PRIVATE KEY` raw in repo), pre-commit hooks, GitHub secret scanning, no secrets in docs

## Out of Scope

- Actual secret values, production key material, provider connection (forbidden in docs PR)
- Final rotation schedule and tooling (future PRs)

## Related Documents

- Security Index: [README.md](README.md)
- Data Protection and Encryption: [DATA_PROTECTION_AND_ENCRYPTION.md](DATA_PROTECTION_AND_ENCRYPTION.md)
- Provider Abstraction: [../architecture/PROVIDER_ABSTRACTION_STRATEGY.md](../architecture/PROVIDER_ABSTRACTION_STRATEGY.md)
- Channel Security: [CHANNEL_SECURITY_TELEGRAM_WEB_MOBILE.md](CHANNEL_SECURITY_TELEGRAM_WEB_MOBILE.md)

## Open Decisions

- Secret manager choice (env vs managed secret service)
- Rotation frequency and emergency procedure
- Detection tooling and CI integration

## Planned Completion Stage

- Phase 1 - Secrets

## Status

Draft - Structure Only. Will be completed later.
