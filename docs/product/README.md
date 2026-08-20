# Phase 1 Product Requirements

## Purpose

This folder contains Phase 1 product requirement documents for the Persian-first
commercial MVP. They describe intended behavior and do not establish implementation
status.

## Important Status Notice

These PRDs are product specifications only. They do not authorize implementation
until reviewed and approved by the owner, and until the D2 Technical Contracts
milestone is completed.

## PRD Status

| PRD | Purpose | Status | Phase | Link |
|---|---|---|---|---|
| General Chat | Platform activation capability | Draft (pending owner review) | Phase 1 | [PRD](GENERAL_CHAT_PRD.md) |
| Prompt Enhancer | First paid Skill | Draft (pending owner review) | Phase 1 | [PRD](PROMPT_ENHANCER_PRD.md) |
| Instagram Caption Generator | First Studio tool MVP | Draft (pending owner review) | Phase 1 | [PRD](INSTAGRAM_CAPTION_GENERATOR_PRD.md) |
| Wallet & Credits | Billing and credit transparency layer | Draft (pending owner review) | Phase 1 | [PRD](WALLET_AND_CREDITS_PRD.md) |

## Recommended Reading Order

1. Wallet & Credits establishes billing foundation.
2. General Chat establishes activation.
3. Prompt Enhancer establishes the first paid Skill.
4. Instagram Caption Generator establishes the first Studio tool.

## Dependencies Between PRDs

All billable features depend on Wallet reserve/settle/release lifecycle. General
Chat is the activation surface. Prompt Enhancer can hand off to General Chat.
Caption Generator is the first monetizable Studio tool. All features share credit
billing and secure HttpOnly cookie authentication.

## Cross-Cutting Product Principles

- Persian-first and RTL.
- Credit transparency before billable actions.
- Reserve before provider call, settle on success, release on failure.
- Tenant isolation.
- Browser-accessible authentication token storage is forbidden.
- Provider-agnostic design.
- Sandbox/mock payment only in Phase 1.

## Aggregated Open Decisions

### General Chat
- Per-message credit price, provider/model, retention duration, timeout policy.

### Prompt Enhancer
- Enhancement price, favorite requirement, history retention, input length.

### Instagram Caption Generator
- Initial/regenerate price, hashtag defaults and bounds, history retention,
  description length, provider selection, prohibited-category ownership.

### Wallet & Credits
- Credit packages, pricing, low-balance threshold, reservation expiration, receipt
  retention, reserved-balance display, corrective-entry governance.

All listed items require owner decision before D2 Technical Contracts approval.

## Related Documents

- [Master Roadmap](../roadmap/MASTER_ROADMAP.md)
- [Phase 1 Core MVP](../roadmap/PHASE_1_CORE_MVP.md)
- [Current Implementation Status](../CURRENT_IMPLEMENTATION_STATUS.md)
- [Documentation Index](../README.md)
