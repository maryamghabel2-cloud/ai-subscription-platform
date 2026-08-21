# Phase 1 Product Requirements

## Purpose

This folder contains Phase 1 Product Requirements Documents. PRDs describe
intended product behavior and do not prove implementation status.

## Authorization Notice

These PRDs do not independently authorize implementation. Owner approval, D2
Technical Contracts completion, prioritized engineering work, and human approval
before merge are required.

## PRD Status
| PRD | Purpose | Status | Phase | Link |
|---|---|---|---|---|
| General Chat | Activation | Draft (pending owner review) | Phase 1 | [PRD](GENERAL_CHAT_PRD.md) |
| Prompt Enhancer | First paid Skill | Draft (pending owner review) | Phase 1 | [PRD](PROMPT_ENHANCER_PRD.md) |
| Caption Generator | First Studio MVP | Draft (pending owner review) | Phase 1 | [PRD](INSTAGRAM_CAPTION_GENERATOR_PRD.md) |
| Wallet & Credits | Billing layer | Draft (pending owner review) | Phase 1 | [PRD](WALLET_AND_CREDITS_PRD.md) |

## Recommended Reading Order

1. Wallet & Credits
2. General Chat
3. Prompt Enhancer
4. Instagram Caption Generator

## Dependencies Between PRDs

All billable features depend on Wallet reserve/settle/release. General Chat is the
activation surface. Prompt Enhancer can hand off to General Chat. Caption Generator
is the first Studio tool. All four features use credits and secure HttpOnly-cookie
authentication.

## Cross-Cutting Product Principles

- Persian-first and RTL.
- Credit transparency before billable actions.
- Reserve before provider call, settle on success, release on failure.
- Tenant isolation.
- Browser-accessible authentication token storage is forbidden.
- Provider-agnostic design.
- Sandbox/mock payment only in Phase 1.

## Related Documents
- [ADR-0002](../decisions/0002-phase-1-product-metering-and-infrastructure.md)
- [Documentation Index](../README.md)
- [Master Roadmap](../roadmap/MASTER_ROADMAP.md)
- [Phase 1 Core MVP](../roadmap/PHASE_1_CORE_MVP.md)
- [Current Implementation Status](../CURRENT_IMPLEMENTATION_STATUS.md)

## Decision Status
| Decision | Resolution | Source |
|---|---|---|
| Chat tiers, quote cap, reserve/settle/release, failure/cancel release, free copy/history, retention, timeout, admin metadata | Owner Approved (ADR-0002, 2026-08-20) | [ADR-0002](../decisions/0002-phase-1-product-metering-and-infrastructure.md) |
| Prompt Enhancer price, length, history, Favorites deferral | Owner Approved (ADR-0002, 2026-08-20) | [ADR-0002](../decisions/0002-phase-1-product-metering-and-infrastructure.md) |
| Caption price, variations, hashtags, length, history, category ownership, Instagram threshold | Owner Approved (ADR-0002, 2026-08-20) | [ADR-0002](../decisions/0002-phase-1-product-metering-and-infrastructure.md) |
| Wallet packages, warning, reservation, receipts, balances, immutable ledger, metadata visibility | Owner Approved (ADR-0002, 2026-08-20) | [ADR-0002](../decisions/0002-phase-1-product-metering-and-infrastructure.md) |
| Infrastructure, Iran accessibility, OpenRouter primary, MixRoute disabled candidate, sandbox payment | Owner Approved (ADR-0002, 2026-08-20) | [ADR-0002](../decisions/0002-phase-1-product-metering-and-infrastructure.md) |

## Deferred to D2
Tier boundaries, estimation, model multipliers and IDs, routing/fallback, timeout
budgets, summarization, quote validity, variance telemetry, non-Instagram norms,
usage normalization, Iran testing method, and hosting-vendor criteria. Deferred to
D2 Technical Contracts.

## Deferred beyond D2
Brand/domain, real payment gateway, real fiat pricing, subscriptions, and production
provider funding are deferred beyond D2.
