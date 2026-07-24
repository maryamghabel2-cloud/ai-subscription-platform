# Secrets and Key Management

**Version:** v0.1.0

**Date:** 2026-07-24

**Status:** Draft - Structure Only

**Document Owner:** Security Architect / DevOps

**Purpose:** Define detailed secrets and key management policy for provider API
keys, payment credentials, Telegram bot tokens, encryption keys, secret storage,
rotation, leak detection, and third-party agent secrets.

**Note:** Structure-only. No real secrets. Final policy will be completed later.

## Purpose

Define how secrets are identified, stored, rotated, and revoked without leaking.

## In Scope

- What counts as a secret, storage rules, rotation, leak detection and response,
  third-party agent secrets

## Out of Scope

- Actual secret values and production key material (forbidden in docs PR)
- Final rotation schedule and tooling details (future PRs)
- Provider connection and real gateway activation (forbidden)

## What Counts as a Secret

- Provider API keys: LLM, image, video, audio, embedding, moderation via provider
  abstraction, cost tracking, no logging of raw keys
- Payment gateway credentials: ZarinPal API key/merchant ID future, crypto
  verification TRC20/TON future, sandbox mock provider exists for dev/test,
  real gateways not active
- Telegram bot tokens: ordinary users link account to platform's bot, do not
  provide token; business customers may connect own token via reviewed
  integration where token encrypted at rest
- Database connection strings: Postgres DATABASE_URL, no plaintext in code,
  no logging, encrypted at rest
- Encryption keys: HMAC fingerprint secret for
  APPROVED_KEYED_HMAC_ONLY_IF_REQUIRED, protected, env-specific, versioned,
  rotatable, content_fingerprint DISABLED_BY_DEFAULT
- Session signing secrets: SECRET_KEY, CSRF secret, session signing, JWT if used
- CSRF secrets: CSRF token generation and validation, non-HttpOnly cookie
- Webhook verification tokens: Telegram X-Telegram-Bot-Api-Secret-Token, payment
  callback secrets, external callback secrets
- Admin credentials: admin grant, service accounts, break-glass accounts
- CI/CD deployment tokens: GitHub Actions, Docker registry, deployment keys

## Secret Storage Rules

- No secret may be stored in source code, git history, or documentation
- No secret may appear in logs or HTTP responses or URLs or client-side code
- Secrets must be stored in a dedicated secrets manager or environment variables
- Each environment must have separate secrets (development, staging, production)
- Development secrets must never be used in production
- Secrets must be encrypted at rest, no plaintext sensitive data in client,
  no secrets in localStorage

## Key Rotation

- All secrets must be rotatable without requiring a code deployment
- Rotation must be tested before being required (runbook tested)
- Old secrets must remain valid for a CONFIGURED_LIMIT grace period during
  rotation to allow zero-downtime rotation
- Rotation events must be logged in the audit trail (metadata only, no raw
  secret, action type, timestamp, operator, outcome)

## Leak Detection and Response

- A secret-scanning step must run in CI on every push (e.g., gitleaks, GitHub
  secret scanning, custom patterns for sk-, ghp_, BEGIN PRIVATE KEY only as
  examples to detect, not real secrets)
- Detected exposed secrets must be revoked immediately
- If a secret is found in a commit, the commit must be considered compromised
  and the secret rotated before any further deployment
- An incident must be raised for any confirmed secret leak, with severity,
  containment, and post-incident review

## Third-Party Agent Secrets

- Agents must never receive full environment secrets
- Each approved agent receives only the specific, scoped credentials it needs
  (least privilege)
- Agent credentials must be separate from platform credentials (different
  namespace, different rotation)
- Agent credentials must be revocable independently without affecting platform
- Secret isolation: Telegram bot tokens encrypted at rest, provider keys via
  abstraction, no secret in logs, HMAC fingerprint secret protected,
  env-specific, versioned, rotatable

## Related Documents

- Security Index: [README.md](README.md)
- Data Protection: [DATA_PROTECTION_AND_ENCRYPTION.md](DATA_PROTECTION_AND_ENCRYPTION.md)
- Provider Abstraction: [../architecture/PROVIDER_ABSTRACTION_STRATEGY.md](../architecture/PROVIDER_ABSTRACTION_STRATEGY.md)
- Channel Security: [CHANNEL_SECURITY_TELEGRAM_WEB_MOBILE.md](CHANNEL_SECURITY_TELEGRAM_WEB_MOBILE.md)
- Logging and Monitoring: [LOGGING_AND_MONITORING.md](LOGGING_AND_MONITORING.md)

## Open Decisions

- Secret manager choice (env vs managed secret service like Vault, AWS Secrets)
- Rotation frequency and emergency procedure and grace period CONFIGURED_LIMIT
- Detection tooling and CI integration (gitleaks, GitHub Advanced Security)
- Owner approval required for all decisions

## Planned Completion Stage

Phase 1 - Secrets

## Status Note

Draft - Structure Only. Will be completed later.
