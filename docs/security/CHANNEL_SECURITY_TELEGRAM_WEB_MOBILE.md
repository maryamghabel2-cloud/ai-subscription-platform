# Channel Security - Telegram, Web, Mobile

**Version:** v0.1.0

**Date:** 2026-07-24

**Status:** Proposed Architecture - Pending Owner Approval and Implementation

**Document Owner:** Security Architect

**Purpose:** Define detailed per-channel security policies for website, mobile
application, Telegram bot, and developer API, including honest limitations,
technical controls, privacy defaults, and API security.

**Note:** Implementation Evidence: This documentation PR does not prove that the described controls are implemented, tested, deployed, or production-ready. Code, automated tests, deployment evidence, and security verification remain the authoritative implementation evidence.

## Purpose

Define security controls for each channel that connects users to the platform.

## In Scope

- Web application security, mobile application security, Telegram channel
  security, developer API security, channel-specific privacy limitations

## Out of Scope

- Final CSP rules, exact rate limits, exact retention settings, implementation
  code (future PRs)

## Web Application Security

- HTTPS enforced everywhere, HSTS headers, TLS 1.2+
- Secure, HttpOnly, SameSite cookies (Secure, HttpOnly, SameSite=Lax or Strict)
- CSRF protection on all state-changing endpoints (CSRF token non-HttpOnly)
- Content Security Policy headers: default-src self, no inline scripts unless
  nonce, no secrets in client
- XSS prevention in all user-facing templates and APIs: input validation,
  output encoding
- Strict input validation and output encoding for all user inputs
- Rate limiting on all authentication and sensitive endpoints:
  register, login, password-reset, refresh, wallet, payment intent

## Mobile Application Security

- Secure local storage (no plaintext sensitive data): Keychain on iOS,
  Keystore on Android, no raw tokens in UserDefaults/SharedPreferences
- App lock with biometric option (Face ID, Touch ID, fingerprint)
- Certificate pinning for API connections to prevent MITM
- No sensitive content in push notification payloads (no conversation text,
  no wallet balance, no tokens)
- Screenshot privacy option where OS supports it (FLAG_SECURE)
- Local cache encryption for conversations, uploaded files, generated images
- User-controlled data deletion: user can delete conversation, image, uploaded
  doc, account, cache clear

## Telegram Channel Security

### Honest Limitations That Must Always Be Communicated to Users

- Telegram bot chats are not end-to-end encrypted.
- Telegram stores messages on its servers.
- Bots receive all messages sent to them in private chats.
- The platform must never claim that Telegram bot conversations are
  end-to-end encrypted.

### Technical Controls

- Webhook authenticity must be verified using the
  X-Telegram-Bot-Api-Secret-Token header on every incoming webhook.
- Telegram bot token must be stored encrypted at rest using a secrets manager.
- The bot token must never appear in logs, URLs, or responses.
- If the bot token is suspected compromised, it must be regenerated
  immediately via BotFather and old token revoked.
- Group access must be disabled unless a separately reviewed use case
  requires it.
- Group privacy mode must remain enabled (bot only receives messages that
  mention it or are direct commands, not all group messages).

### Privacy Defaults

- Sensitive Telegram conversations must use non-retention by default.
- Users must be offered a clear opt-in before any conversation content is
  stored in the platform's database.
- Telegram user identifiers must be stored using only the minimum necessary
  scope (Telegram user id, not phone number, not username unless needed).
- No Telegram phone numbers must be stored.
- The mobile application is the preferred and recommended channel for highly
  sensitive conversations.

- Ordinary end users link their account to platform's Telegram bot, do not
  provide bot token.
- Future business customers may connect own bot token via separate reviewed
  integration where token is encrypted at rest.
- Anti-spam: rate limit CONFIGURED_LIMIT, no bulk broadcast without approval,
  privacy-aware, no secret in logs.

## Developer API Security

- API keys must be short-lived or rotatable (CONFIGURED_LIMIT lifetime)
- API keys must be stored hashed, never in plaintext (key_hash, key_prefix)
- Each API key must have defined scopes and rate limits (CONFIGURED_LIMIT)
- API key usage must be logged for anomaly detection (metadata only, no raw key)
- API keys must be revocable without service disruption
- Tenant isolation: API key can only access own user's data, no cross-user
- X-API-Key auth, no API key in URL query string

## Related Documents

- Security Index: [README.md](README.md)
- Boundaries: [../architecture/ROLE_PERSONA_AGENT_BOUNDARIES.md](../architecture/ROLE_PERSONA_AGENT_BOUNDARIES.md)
- Agent Plugin and Execution: [../architecture/AGENT_PLUGIN_AND_EXECUTION_SYSTEM.md](../architecture/AGENT_PLUGIN_AND_EXECUTION_SYSTEM.md)
- Identity and Access: [IDENTITY_AND_ACCESS_CONTROL.md](IDENTITY_AND_ACCESS_CONTROL.md)
- Data Protection: [DATA_PROTECTION_AND_ENCRYPTION.md](DATA_PROTECTION_AND_ENCRYPTION.md)
- Secrets Management: [SECRETS_AND_KEY_MANAGEMENT.md](SECRETS_AND_KEY_MANAGEMENT.md)

## Open Decisions

- Exact rate limits, retention, and privacy notice wording per channel
- Webhook verification method and secret rotation (X-Telegram-Bot-Api-Secret-Token)
- CSP rules and HSTS max-age
- Certificate pinning implementation and backup pins
- Owner approval for channel security controls

## Planned Completion Stage

Phase 1 - Channel Security

## Status Note

Proposed Architecture - Pending Owner Approval and Implementation. Implementation and verification are separate future work. Open Decisions remain unresolved until explicitly approved.
