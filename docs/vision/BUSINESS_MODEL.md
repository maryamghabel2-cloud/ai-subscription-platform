# BUSINESS MODEL - Persian AI Platform

**Phase:** 0  
**Date:** 2026-07-19

## Model Overview

Credit-based SaaS with wallet. User buys credits (IRR), spends per action (chat token, image generation, video seconds, API call, Telegram agent execution).

## Why Credits, Not Subscriptions Only (Phase 1-2)

- Simpler than shared-account model (deprecated)
- Transparent cost per tool
- Enables API and business-agent usage
- Future subscription can be “monthly credit pack” - not blocking Phase 0

## Revenue Streams (Phased)

**Phase 1 Core:**
- Credit packs (small/medium/large) - manual purchase flow (no real payment in Phase 0/1 skeleton)
- Future: Zarinpal, direct bank, later crypto optional

**Phase 2-3:**
- Studio packs (product photography 50 images)
- Persona premium packs

**Phase 4+:**
- Developer API usage
- Telegram Business Agents subscription
- Team/business seats
- Agent Marketplace rev-share (Phase 8)

## Cost Structure

- AI inference costs (OpenAI compatible APIs, image/video models)
- Hosting (FastAPI, Next.js, Postgres, Redis - later)
- External agent costs (coding agents, research agents - controlled via approval gates)

## Unit Economics Targets (Draft)

- Must track per-action gross margin: cost to serve vs credit price
- CAC via content/SEO, not paid until LTV known
- LTV = credit purchases over 90 days
- Goal for Phase 1: Gross margin positive per chat/image, even if small

## What Is Out of Scope for Phase 0 Business

- Real payment activation
- Automated refunds > threshold without human approval
- Crypto billing
- Shared consumer accounts (never again)
- Claiming guaranteed provider discounts that violate ToS

## Wallet & Billing Design Principles (Future, Not Built Now)

- Wallet ledger must be auditable
- Credit purchase → ledger entry → balance update atomic
- Spend actions must be idempotent with request ID
- Daily spend limits
- Human approval required for refunds/credits above threshold (see HUMAN_APPROVAL_GATES)

## Growth Linkage

See `docs/growth/GROWTH_SYSTEM.md` for loops: SEO → landing → signup → activation → referral.

## Risk Controls

- No auto price changes without approval
- No auto issuing credits without approval
- Finance agent produces report, founder approves
