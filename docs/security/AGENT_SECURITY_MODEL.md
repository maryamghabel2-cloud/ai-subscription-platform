# Agent Security Model

**Version:** v0.1.0

**Date:** 2026-07-24

**Status:** Draft - Structure Only

**Document Owner:** Security Architect

**Purpose:** Define agent sandboxing, tool allowlists, permission boundaries,
network allowlists, budgets, human approval gates, agent isolation, and secret
isolation.

**Note:** This is a structure-only stub. Final model will be completed later.

## Purpose

Define how Agents that perform work are secured.

## In Scope

- Agent sandboxing:
  - Agents run with least privilege, isolated from other users' data
  - No direct commit to main, no force-push, no history deletion
- Tool allowlists:
  - web_search (approved official sources for immigration)
  - file_reader, image_generation_api, telegram_send
  - knowledge_retrieval, embedding, LLM
  - Must be declared per agent in permissions and tools list
- Permission boundaries:
  - Allow, forbid, approval-required per AGENT_PERMISSION_MODEL
  - Absolutely forbidden NO-GO (ToS bypass, geographic/sanctions/KYC bypass,
    fake identities, sharing unauthorized credentials, CSAM, non-consensual
    imagery, deepfake without consent, claiming professional authority)
- Network allowlists:
  - For Deep Research and Immigration Research Agents, may browse approved
    current official government and embassy sources
  - Respect robots.txt, no scraping violating ToS
- Budgets:
  - Per execution max credits CONFIGURED_LIMIT
  - Per day max cost CONFIGURED_LIMIT
  - Per user spend limit CONFIGURED_LIMIT
  - Rate limit CONFIGURED_LIMIT
  - Exact values are Open Decisions requiring product/finance/trust review
- Human approval gates:
  - Publishing public content, spending money, contacting customers
  - Bulk Telegram broadcast, pricing/config changes, merge/deploy, API keys,
    persona sensitive edits, campaigns, refunds above threshold
- Agent isolation:
  - User data isolation (own data only), no cross-user access
  - Pseudonymous identifiers in audit logs, no raw sensitive prompts
- Secret isolation:
  - Telegram bot tokens encrypted at rest, provider keys via abstraction
  - No secret in logs, HMAC fingerprint secret protected, env-specific,
    versioned, rotatable, content_fingerprint DISABLED_BY_DEFAULT

## Out of Scope

- Final budget numbers and exact permission matrix
- Implementation code (future PRs)

## Related Documents

- Security Index: [README.md](README.md)
- Agent Plugin and Execution: [../architecture/AGENT_PLUGIN_AND_EXECUTION_SYSTEM.md](../architecture/AGENT_PLUGIN_AND_EXECUTION_SYSTEM.md)
- Permission Model: [../agents/AGENT_PERMISSION_MODEL.md](../agents/AGENT_PERMISSION_MODEL.md)
- Human Approval Gates: [../agents/HUMAN_APPROVAL_GATES.md](../agents/HUMAN_APPROVAL_GATES.md)
- Logging and Monitoring: [LOGGING_AND_MONITORING.md](LOGGING_AND_MONITORING.md)

## Open Decisions

- Exact tool allowlist per agent type (business, research, Telegram, studio)
- Budget and rate limit numbers
- Approval gate thresholds
- Owner approval required

## Planned Completion Stage

Phase 1 - Agent Security

## Status Note

Draft - Structure Only. Will be completed later.
