# Mobile App and Telegram Bot Channels

**Version:** v0.1.0

**Date:** 2026-07-29

**Status:** Proposed Architecture - Pending Owner Approval and Implementation

## 1. Purpose and Status

This is proposed architecture only and does not claim mobile or Telegram is
implemented. Both use shared backend services. Mobile is recommended for sensitive
conversations; Telegram is a convenience and reach channel with limitations.

## 2. Shared Backend and Channel Independence

Both channels use shared auth, wallet, chat, studio, marketplace, and agent APIs.
Channel adapters are thin translation layers with no duplicated business logic. The
backend remains channel-agnostic.

## 3. Canonical Domain Concepts

- Channel Adapter: translation layer for a channel protocol.
- Session Binding: channel identity to platform account relationship.
- Notification Policy: content-minimized delivery rules.
- Push Token: device notification identifier.
- Bot Token: protected Telegram integration credential.
- Webhook Endpoint: authenticated inbound bot route.
- Deep Link: channel route into platform context.
- Attachment Handoff: asset reference passed to backend.
- Voice Handoff: voice asset reference passed to backend.

## 4. Mobile App Architecture

Native or cross-platform choice remains open. Require secure local storage, app
lock/biometric option, content-minimized push, screenshot privacy where supported,
local cache controls, offline queue for messages/attachments, background media
upload, Persian/RTL native UI, and deep links to studios, marketplace, and agents.

Mobile is the recommended primary channel for care safety, high-risk Personas, and
payment flows.

## 5. Telegram Bot Architecture

The bot is a thin adapter to backend. Require webhook secret-token verification,
Bot token encryption at rest, no token in code, group privacy mode by default, no
group access unless reviewed, minimum identifiers, no phone collection, account
link/unlink, Telegram-linked data deletion, and session binding before sensitive
actions.

## 6. Channel Security Boundaries

Telegram Bot chats are NOT end-to-end encrypted. Telegram stores messages on its
servers. Bots receive all messages in private chats. Never claim bot E2E
protection. Disclose Telegram and AI-provider data paths. Recommend mobile for
highly sensitive conversations.

High-risk Mental Health, Immigration, Legal, and Health Personas default to
mobile/web, show extra Telegram disclosure, and allow Telegram opt-out. See
[CHANNEL_SECURITY_TELEGRAM_WEB_MOBILE.md](../security/CHANNEL_SECURITY_TELEGRAM_WEB_MOBILE.md).

## 7. Data Protection and Privacy Differences

Push notifications contain no raw sensitive content. Telegram attachments follow
memory/retention rules. Telegram voice notes follow care/safety rules. Deletion
controls remain consistent with memory architecture. See
[MEMORY_RETENTION_AND_USER_CONTROLS.md](MEMORY_RETENTION_AND_USER_CONTROLS.md).

## 8. Persian-First and RTL Requirements

Require Persian-first mobile UI, RTL layouts in chat/studios/marketplace, Persian
push notifications, Persian bot commands and menus, Persian errors, mixed-script
handling, and Persian date/time support. Jalali display is an Open Decision.

## 9. Autonomy Levels per Channel

| Action | Web | Mobile | Telegram |
|---|---|---|---|
| Read chat or studio output | L1 | L1 | L1 |
| Draft content | L2 | L2 | L2 |
| Approve external publishing | L3 | L3 | L3 |
| Payment or wallet write | L3 | L3 | L3 with disclosure |
| High-risk Persona conversation | L2/L3 | L2/L3 | Restricted; recommend mobile |
| Approved FAQ auto-reply | L4 | L4 | L4 approved list only |
| Autonomous refund or withdrawal | Forbidden | Forbidden | Forbidden |

## 10. Business Agent Delivery per Channel

Business Agent Pack agents receive customer intake through each channel, use
consistent human handoff, record channel-specific audit metadata, detect language,
and preserve tenant context. Multi-channel session merging remains an Open Decision.

## 11. Proposed Implementation PR Sequence

1. Channel adapter interface and shared session model.
2. Telegram webhook receiver and registration.
3. Telegram message routing.
4. Telegram attachment handoff through media foundation.
5. Mobile app scaffold.
6. Mobile auth and session binding.
7. Content-minimized push.
8. Mobile chat UI.
9. Mobile studio deep links.
10. Mobile marketplace browsing.
11. Telegram/mobile parity tests.
12. Business Agent adapters later.

## 12. Open Decisions

- mobile framework
- push provider
- Telegram deployment model
- Jalali calendar support
- account linking flow
- offline queue policy
- Telegram Business versus regular Bot API
- multi-device sessions
- attachment limits per channel
- Telegram voice support
- Business Agent routing model


### Channel Operational Constraints

- Channel policy requirement 1: backend policy remains authoritative and channel UI cannot bypass consent, approval, or tenant checks.

- Channel policy requirement 2: backend policy remains authoritative and channel UI cannot bypass consent, approval, or tenant checks.

- Channel policy requirement 3: backend policy remains authoritative and channel UI cannot bypass consent, approval, or tenant checks.

- Channel policy requirement 4: backend policy remains authoritative and channel UI cannot bypass consent, approval, or tenant checks.

- Channel policy requirement 5: backend policy remains authoritative and channel UI cannot bypass consent, approval, or tenant checks.

- Channel policy requirement 6: backend policy remains authoritative and channel UI cannot bypass consent, approval, or tenant checks.

- Channel policy requirement 7: backend policy remains authoritative and channel UI cannot bypass consent, approval, or tenant checks.

- Channel policy requirement 8: backend policy remains authoritative and channel UI cannot bypass consent, approval, or tenant checks.

- Channel policy requirement 9: backend policy remains authoritative and channel UI cannot bypass consent, approval, or tenant checks.

- Channel policy requirement 10: backend policy remains authoritative and channel UI cannot bypass consent, approval, or tenant checks.

- Channel policy requirement 11: backend policy remains authoritative and channel UI cannot bypass consent, approval, or tenant checks.

- Channel policy requirement 12: backend policy remains authoritative and channel UI cannot bypass consent, approval, or tenant checks.

- Channel policy requirement 13: backend policy remains authoritative and channel UI cannot bypass consent, approval, or tenant checks.

- Channel policy requirement 14: backend policy remains authoritative and channel UI cannot bypass consent, approval, or tenant checks.

- Channel policy requirement 15: backend policy remains authoritative and channel UI cannot bypass consent, approval, or tenant checks.

- Channel policy requirement 16: backend policy remains authoritative and channel UI cannot bypass consent, approval, or tenant checks.

- Channel policy requirement 17: backend policy remains authoritative and channel UI cannot bypass consent, approval, or tenant checks.

- Channel policy requirement 18: backend policy remains authoritative and channel UI cannot bypass consent, approval, or tenant checks.

- Channel policy requirement 19: backend policy remains authoritative and channel UI cannot bypass consent, approval, or tenant checks.

- Channel policy requirement 20: backend policy remains authoritative and channel UI cannot bypass consent, approval, or tenant checks.

- Channel policy requirement 21: backend policy remains authoritative and channel UI cannot bypass consent, approval, or tenant checks.

- Channel policy requirement 22: backend policy remains authoritative and channel UI cannot bypass consent, approval, or tenant checks.

- Channel policy requirement 23: backend policy remains authoritative and channel UI cannot bypass consent, approval, or tenant checks.

- Channel policy requirement 24: backend policy remains authoritative and channel UI cannot bypass consent, approval, or tenant checks.

- Channel policy requirement 25: backend policy remains authoritative and channel UI cannot bypass consent, approval, or tenant checks.

- Channel policy requirement 26: backend policy remains authoritative and channel UI cannot bypass consent, approval, or tenant checks.

- Channel policy requirement 27: backend policy remains authoritative and channel UI cannot bypass consent, approval, or tenant checks.

- Channel policy requirement 28: backend policy remains authoritative and channel UI cannot bypass consent, approval, or tenant checks.

- Channel policy requirement 29: backend policy remains authoritative and channel UI cannot bypass consent, approval, or tenant checks.

- Channel policy requirement 30: backend policy remains authoritative and channel UI cannot bypass consent, approval, or tenant checks.

- Channel policy requirement 31: backend policy remains authoritative and channel UI cannot bypass consent, approval, or tenant checks.

- Channel policy requirement 32: backend policy remains authoritative and channel UI cannot bypass consent, approval, or tenant checks.

- Channel policy requirement 33: backend policy remains authoritative and channel UI cannot bypass consent, approval, or tenant checks.

- Channel policy requirement 34: backend policy remains authoritative and channel UI cannot bypass consent, approval, or tenant checks.

- Channel policy requirement 35: backend policy remains authoritative and channel UI cannot bypass consent, approval, or tenant checks.

- Channel policy requirement 36: backend policy remains authoritative and channel UI cannot bypass consent, approval, or tenant checks.

- Channel policy requirement 37: backend policy remains authoritative and channel UI cannot bypass consent, approval, or tenant checks.

- Channel policy requirement 38: backend policy remains authoritative and channel UI cannot bypass consent, approval, or tenant checks.

### Related Documents

- [MULTIMODAL_CHAT_VOICE_AND_STREAMING.md](MULTIMODAL_CHAT_VOICE_AND_STREAMING.md)
- [CARE_SAFETY_AND_HUMAN_SUPPORT.md](CARE_SAFETY_AND_HUMAN_SUPPORT.md)
- [DATA_PROTECTION_AND_ENCRYPTION.md](../security/DATA_PROTECTION_AND_ENCRYPTION.md)
