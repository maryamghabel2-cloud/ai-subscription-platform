# Phase 6 - Telegram & Business Agents

**Phase:** PHASE_6_TELEGRAM_BUSINESS_AGENTS  
**Date:** 2026-07-19  
**Status:** Planned (Phase 0 is current)

## Objective
Telegram integration and low-code business agents for sales/support/content.

## In Scope
- Telegram bot connect: user creates bot, provides token (stored encrypted), webhook set
- Business Agents: FAQ bot, lead qualifier, content drafter
- Agent execution logs

## Out of Scope
Bulk messaging without approval, spam, auto-contacting customers without gate

## Dependencies
Phase 2 personas pattern, Phase 4 API key system for business agent auth

## Technical Deliverables
- Telegram webhook endpoint: /telegram/webhook/{agent_id}
- Bot token encrypted at rest
- Business agent config: persona + tools + approval gates
- Message queue

## UX Deliverables
- Telegram Agents page: create, connect, test chat
- Business Agents directory

## Business Deliverables
- Business agent subscription future

## Required Agents
Fullstack Builder, DevOps, Customer Success, Compliance Risk, Growth Marketing

## Test Requirements
- Connect test bot, send /start → echo
- Token encrypted not in logs
- No bulk send without approval

## Risk Controls
- Spam → rate limit + human approval for broadcast
- Token leak → encrypted, audit log access
- All human approval gates from HUMAN_APPROVAL_GATES.md must apply: spending money, publishing, contacting customers, changing prices/config, merging, deploying, API keys, persona changes, paid campaigns, refunds/credits above threshold require human approval.
- Audit logs required for all state-changing actions.
- No medical/legal/psychological authoritative claims.

## Exit Criteria
Owner can connect Telegram bot and get FAQ answers via platform agent
