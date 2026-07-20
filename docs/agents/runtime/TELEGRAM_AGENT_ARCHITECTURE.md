# TELEGRAM AGENT ARCHITECTURE

**Date:** 2026-07-19  
**Phase:** 6

## Concept
User creates Telegram bot via BotFather, gets token, enters token in platform UI, platform sets webhook to `https://platform.com/api/telegram/webhook/{agent_id}`.

## Components

- **Token Storage:** Encrypted at rest (Fernet, future Vault), never in logs
- **Webhook Endpoint:** `POST /telegram/webhook/{agent_id}` - verifies token, processes update, checks wallet, calls LLM with business agent config, returns Telegram message
- **Agent Config:** Linked to business agent (FAQ, lead qualifier)
- **Execution Logs:** Telegram update id, user id, input, output, timestamp, credit cost

## Flow

1. User creates bot, pastes token in UI
2. Backend encrypts token, stores, calls Telegram setWebhook API
3. User sends message to bot on Telegram
4. Telegram POSTs update to webhook
5. Platform: decrypt token? Actually token not needed for receiving, but for sending reply. Validate agent_id exists, check wallet, run business agent logic, send reply via Telegram sendMessage API
6. Log execution, deduct credits

## Safety

- Token encrypted, never logged, access audit logged
- Rate limit per bot (e.g., 30 msg/min)
- No bulk broadcast without human approval gate (bulk requires approval issue)
- Spam detection: if user reports spam, auto-pause bot, require human review
- User can revoke token (delete agent), webhook removed

## Future Internal Ops
- L3: Bot health monitor (checks webhook status, reports draft)
- Not autonomous: cannot send bulk messages without approval

## Not Built in Phase 0
- Only architecture doc, no code
