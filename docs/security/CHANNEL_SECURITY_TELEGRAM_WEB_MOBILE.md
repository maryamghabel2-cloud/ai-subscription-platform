# Channel Security - Telegram, Web, Mobile

**Version:** v0.1.0

**Date:** 2026-07-24

**Status:** Draft - Structure Only

**Document Owner:** Security Architect

**Purpose:** Define website security, mobile application security, Telegram bot
security, API security, and channel-specific privacy limitations.

**Note:** This is a structure-only stub. Final channel security policy will be
completed later.

## Purpose

Define security controls for each channel that connects users.

## In Scope

- Website security:
  - Next.js 14 App Router, Tailwind, RTL, Persian typography
  - CSP, HSTS, input validation, output encoding
  - HttpOnly cookies Secure SameSite, CSRF, rate limiting, anti-spam
  - No secrets in client, privacy-preserving logs

- Mobile application security:
  - Native or PWA, voice input/output, camera for product photography
  - Secure storage (Keychain/Keystore), biometric considerations
  - Privacy-aware, preferred future channel for highly sensitive conversations
  - Non-retention by default unless user enables memory

- Telegram bot security:
  - Telegram bot chats must not be described as end-to-end encrypted.
  - Telegram is a convenience channel, not the preferred channel for highly
    sensitive conversations.
  - The future mobile app is the preferred channel for highly sensitive
    conversations.
  - Telegram identifiers must be minimized (no excessive collection,
    pseudonymous if possible).
  - Telegram bot tokens must be encrypted at rest.
  - Webhook authenticity must be verified (Telegram webhook secret, IP
    allowlist if applicable).
  - Sensitive Telegram conversations should use non-retention by default
    unless the user explicitly enables memory.
  - Ordinary end users link their account to platform's Telegram bot, do
    not provide bot token.
  - Future business customers may connect own bot token via separate reviewed
    integration where token is encrypted at rest.
  - Anti-spam: rate limit CONFIGURED_LIMIT, no bulk broadcast without approval,
    privacy-aware, no secret in logs.

- API security:
  - Hashed API keys (key_hash, key_prefix unique), scopes, rate limiting,
    usage logs, X-API-Key auth, tenant isolation, no raw keys in logs

- Channel-specific privacy limitations:
  - Telegram not end-to-end encrypted, Web and Mobile may have different
    retention, user must be informed, consent for human review requires
    informed user consent and separately approved workflow, no secret sharing
  - Channel adapter must not be classified as Role or Agent merely because it
    connects users
  - Audit logging for channel access, no raw sensitive content by default,
    content_fingerprint DISABLED_BY_DEFAULT

## Out of Scope

- Final CSP rules and exact rate limits
- Exact retention settings and privacy notice wording
- Webhook verification method and secret rotation details
- Implementation code (future PRs)

## Related Documents

- Security Index: [README.md](README.md)
- Role/Persona/Agent Boundaries: [../architecture/ROLE_PERSONA_AGENT_BOUNDARIES.md](../architecture/ROLE_PERSONA_AGENT_BOUNDARIES.md)
- Agent Plugin and Execution: [../architecture/AGENT_PLUGIN_AND_EXECUTION_SYSTEM.md](../architecture/AGENT_PLUGIN_AND_EXECUTION_SYSTEM.md)
- Identity and Access Control: [IDENTITY_AND_ACCESS_CONTROL.md](IDENTITY_AND_ACCESS_CONTROL.md)
- Data Protection: [DATA_PROTECTION_AND_ENCRYPTION.md](DATA_PROTECTION_AND_ENCRYPTION.md)

## Open Decisions

- Exact rate limits, retention, and privacy notice wording per channel
- Webhook verification method and secret rotation
- Owner approval for channel security controls

## Planned Completion Stage

Phase 1 - Channel Security

## Status Note

Draft - Structure Only. Will be completed later.
