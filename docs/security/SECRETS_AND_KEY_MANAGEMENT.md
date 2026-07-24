# Secrets and Key Management

**Version:** v0.1.0

**Date:** 2026-07-24

**Status:** Draft - Structure Only

**Document Owner:** Security Architect / DevOps

**Purpose:** Define provider API keys, payment credentials, Telegram bot tokens,
encryption keys, secret storage, rotation, revocation, and leak detection.

**Note:** Structure-only stub. No real secrets are contained. Final policy will
be completed later.

## Purpose

Define how secrets are stored, generated, distributed, rotated, and revoked
without leaking.

## In Scope

### What Counts as a Secret

- Provider API keys: LLM, image, video, audio, embedding, moderation via
  provider abstraction, cost tracking
- Payment gateway credentials: ZarinPal future, crypto TRC20/TON future,
  sandbox mock provider exists for dev/test, real gateways not active
- Telegram bot tokens: ordinary users link account to platform's bot, do not
  provide token; business customers may connect own token via reviewed
  integration where token encrypted at rest
- Database connection strings: Postgres DATABASE_URL, no plaintext in code
- Encryption keys: HMAC fingerprint secret for
  APPROVED_KEYED_HMAC_ONLY_IF_REQUIRED, protected, env-specific, versioned,
  rotatable, content_fingerprint DISABLED_BY_DEFAULT
- Session signing secrets: SECRET_KEY, CSRF secret, JWT if used
- Webhook verification tokens: Telegram X-Telegram-Bot-Api-Secret-Token,
  payment callback secrets
- Admin credentials: admin grant, service accounts, CI/CD deployment tokens

### Secret Storage Rules

- No secret may be stored in source code, git history, or documentation
- No secret may appear in logs or HTTP responses or URLs
- Secrets must be stored in dedicated secrets manager or env vars
- Each environment must have separate secrets (dev, staging, prod)
- Development secrets must never be used in production
- Secrets must be encrypted at rest, no plaintext sensitive data in client

### Key Rotation

- All secrets must be rotatable without requiring a code deployment
- Rotation must be tested before being required
- Old secrets must remain valid for a CONFIGURED_LIMIT grace period during
  rotation
- Rotation events must be logged in audit trail (metadata only, no raw secret)
- Emergency rotation on compromise, immediate revocation

### Leak Detection and Response

- A secret-scanning step must run in CI on every push
- Detected exposed secrets must be revoked immediately
- If a secret is found in a commit, commit must be considered compromised and
  secret rotated before any further deployment
- An incident must be raised for any confirmed secret leak
- No raw `sk-` , raw `ghp_` tokens, no `BEGIN PRIVATE KEY` raw in repo (these
  patterns mentioned only as examples to detect, not actual secrets)

### Third-Party Agent Secrets

- Agents must never receive full environment secrets
- Each approved agent receives only specific, scoped credentials it needs
- Agent credentials must be separate from platform credentials
- Agent credentials must be revocable independently
- Secret isolation: Telegram bot tokens encrypted at rest, provider keys via
  abstraction, no secret in logs, HMAC fingerprint secret protected

## Out of Scope

- Actual secret values and production key material (forbidden in docs PR)
- Final rotation schedule and tooling details (future PRs)
- Provider connection and real gateway activation (forbidden)

## Related Documents

- Security Index: [README.md](README.md)
- Data Protection: [DATA_PROTECTION_AND_ENCRYPTION.md](DATA_PROTECTION_AND_ENCRYPTION.md)
- Provider Abstraction: [../architecture/PROVIDER_ABSTRACTION_STRATEGY.md](../architecture/PROVIDER_ABSTRACTION_STRATEGY.md)
- Channel Security: [CHANNEL_SECURITY_TELEGRAM_WEB_MOBILE.md](CHANNEL_SECURITY_TELEGRAM_WEB_MOBILE.md)
- Secrets and Key Management: [SECRETS_AND_KEY_MANAGEMENT.md](SECRETS_AND_KEY_MANAGEMENT.md)

## Open Decisions

- Secret manager choice (env vs managed secret service)
- Rotation frequency and emergency procedure
- Grace period CONFIGURED_LIMIT value and testing
- Detection tooling and CI integration
- Owner approval required for all decisions

## Planned Completion Stage

Phase 1 - Secrets

## Status Note

Draft - Structure Only. Will be completed later.
