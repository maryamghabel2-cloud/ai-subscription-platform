# Phase 4 - API Platform

**Phase:** PHASE_4_API_PLATFORM  
**Date:** 2026-07-19  
**Status:** Planned (Phase 0 is current)

## Objective
Developer platform: API keys, usage logs, own chat/image/RAG APIs.

## In Scope
- API key create/delete/list
- Developer dashboard: usage, logs, credit
- Endpoints: /v1/chat, /v1/image, /v1/embeddings (proxy)
- Docs page

## Out of Scope
Video API, Telegram API, marketplace

## Dependencies
Phase 1 auth, wallet, Phase 3 image infra

## Technical Deliverables
- API key model: hashed key, prefix, last used, scopes
- Middleware: check X-API-Key, rate limit, credit check, ledger
- Versioned APIs, audit logs

## UX Deliverables
- API Platform landing
- Docs with curl examples
- Key management UI

## Business Deliverables
- API credit pricing, team seats future

## Required Agents
Fullstack Builder, DevOps, QA Security, Compliance Risk, Growth Marketing (dev marketing)

## Test Requirements
- Key create → use → revoke → 401
- Rate limit 60/min
- Credit insufficient → 402
- Audit log written

## Risk Controls
- Key leakage → show only once, prefix, allow rotation
- Abuse → rate limit + spend cap requiring approval
- All human approval gates from HUMAN_APPROVAL_GATES.md must apply: spending money, publishing, contacting customers, changing prices/config, merging, deploying, API keys, persona changes, paid campaigns, refunds/credits above threshold require human approval.
- Audit logs required for all state-changing actions.
- No medical/legal/psychological authoritative claims.

## Exit Criteria
Developer can create key, call chat/image API via curl, see usage
