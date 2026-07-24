# Agent Security Model

**Version:** v0.1.0

**Date:** 2026-07-24

**Status:** Draft - Structure Only

**Document Owner:** Security Architect

**Purpose:** Define agent sandboxing, tool allowlists, permission boundaries, network allowlists, budgets, human approval gates, agent isolation, and secret isolation.

**Note:** This is a structure-only stub. Final agent security model will be completed later.

## In Scope

- Agent sandboxing: Agents that perform work must run with least privilege, isolated from other users' data, no direct commit to main, no force-push, no history deletion
- Tool allowlists: web_search (approved official sources for immigration), file_reader, image_generation_api, telegram_send, knowledge_retrieval, embedding, LLM – must be declared per agent in permissions and tools list
- Permission boundaries: allow, forbid, approval-required per AGENT_PERMISSION_MODEL, plus absolutely forbidden NO-GO (ToS bypass, geographic/sanctions/KYC bypass, fake identities, sharing unauthorized credentials, CSAM, non-consensual imagery, deepfake without consent, claiming professional authority)
- Network allowlists: for Deep Research Agent and Immigration Research Agent, may browse approved current official government and embassy sources, respect robots.txt, no scraping violating ToS
- Budgets: per execution max credits CONFIGURED_LIMIT, per day max cost CONFIGURED_LIMIT, per user spend limit CONFIGURED_LIMIT, rate limit CONFIGURED_LIMIT – exact values are Open Decisions requiring product/finance/trust and safety review
- Human approval gates: publishing public content, spending money, contacting customers, bulk Telegram broadcast, pricing/config changes, merge/deploy, API keys, persona sensitive edits, campaigns, refunds above threshold require human approval
- Agent isolation: user data isolation (own data only), no cross-user access, pseudonymous identifiers in audit logs, no raw sensitive prompts in technical logs
- Secret isolation: Telegram bot tokens encrypted at rest, provider keys via abstraction, no secret in logs, HMAC fingerprint secret protected, env-specific, versioned, rotatable, content_fingerprint DISABLED_BY_DEFAULT

## Out of Scope

- Final budget numbers, exact permission matrix, implementation code (future PRs)

## Related Documents

- Security Index: [README.md](README.md)
- Agent Plugin and Execution: [../architecture/AGENT_PLUGIN_AND_EXECUTION_SYSTEM.md](../architecture/AGENT_PLUGIN_AND_EXECUTION_SYSTEM.md)
- Agent Permission Model: [../agents/AGENT_PERMISSION_MODEL.md](../agents/AGENT_PERMISSION_MODEL.md)
- Human Approval Gates: [../agents/HUMAN_APPROVAL_GATES.md](../agents/HUMAN_APPROVAL_GATES.md)
- Logging and Monitoring: [LOGGING_AND_MONITORING.md](LOGGING_AND_MONITORING.md)

## Open Decisions

- Exact tool allowlist per agent type (business, research, Telegram, studio)
- Budget and rate limit numbers
- Approval gate thresholds

## Planned Completion Stage

- Phase 1 - Agent Security

## Status

Draft - Structure Only. Will be completed later.
