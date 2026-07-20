# DEVELOPER API AGENT ARCHITECTURE

**Date:** 2026-07-19  
**Phase:** 4

## Purpose
Developer API Platform lets developers use chat, image, embeddings via API key.

## Components

- **API Key Model:** id, user_id, name, prefix (e.g., sk_live_abc123...), hashed_key (bcrypt), scopes (chat:image:read), last_used_at, created_at, is_active
- **Key Creation:** POST /api-keys → returns full key once, stores hash, shows prefix. Human approval? No, but rate limit key creation (5/hour). Approval required for increasing rate limit scope.
- **Auth Middleware:** Check X-API-Key header, lookup hash, check is_active, check scopes, rate limit (Redis future), credit check
- **Usage Logging:** Table api_usage_logs: key_id, endpoint, tokens, cost, timestamp, request_id
- **Wallet:** Check balance before call, deduct credits atomically, idempotent via request_id header
- **Docs:** /docs/api with curl examples

## Endpoints Concept (Future)

- POST /v1/chat
- POST /v1/image/generate
- POST /v1/embeddings
- GET /v1/usage

## Safety

- Key shown only once, prefix logged
- Scopes: least privilege
- Rate limit 60/min per key (MVP)
- No auto key creation without user action
- Revoke API key requires human user action (not agent autonomous)
- Audit logs for key create/delete/list

## Difference from Project-Building Agents
- Project-building Fullstack Builder uses GitHub API with founder's token to create PRs (external agent)
- Runtime Developer API Agent is product feature: end-user developers get API keys to call platform's own AI APIs

## Not Built Now
- Only spec, no code in Phase 0
