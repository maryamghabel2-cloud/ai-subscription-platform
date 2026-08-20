# Instagram Caption Generator PRD

## 1. Document Control

**Status:** Draft (Part 1 of 2)
**Phase:** Phase 1 — In Progress
**Owner:** Product
**Last updated:** 2026-08-20
**Related:** [Chat](GENERAL_CHAT_PRD.md), [Wallet](WALLET_AND_CREDITS_PRD.md), [Prompt Enhancer](PROMPT_ENHANCER_PRD.md), [Phase 1](../roadmap/PHASE_1_CORE_MVP.md)
**Implementation state:** Pending implementation.

## 2. Product Overview and Business Goal

Instagram Caption Generator is the first Studio tool in Persian Content and
Commerce Studio. It creates reviewable captions and hashtags for Persian creators
and shops, using credits per generation. It provides a monetizable bridge from
chat/Prompt Enhancer into commercial Studio workflows.

## 3. Target Users

- Instagram shop owner: needs fast product copy for frequent listings.
- Content creator: needs tone-consistent captions for audience engagement.
- Social media manager: needs variants for distinct client brands.
- Local small-business owner: needs Persian marketing copy without specialist skill.

## 4. User Problems and Jobs to Be Done

- Turn a rough product description into publishable Persian social copy.
- Match a caption to a brand tone without rewriting it manually.
- Create mixed Persian/English hashtags suitable for selected channels.
- Compare multiple options before choosing a caption.
- Know credit impact before generating paid content.

## 5. User Stories

- As a shop owner, I want to describe a product so that I can generate relevant copy.
- As a creator, I want to select tone so that captions match my public voice.
- As a manager, I want length selection so that copy fits campaign format.
- As a marketer, I want platform selection so that wording fits the destination.
- As a bilingual user, I want language mode so that copy matches my audience.
- As a user, I want hashtag count selection so that I control tag density.
- As a user, I want three variations so that I can compare creative approaches.
- As a user, I want copy buttons so that I can reuse caption and tags separately.
- As a returning user, I want history so that I can revisit prior work.
- As a credit-conscious user, I want an estimate so that I can decide to generate.
- As a user with low credits, I want a clear block so that I can open the wallet.
- As a user, I want unsafe description handling so that disallowed content is not generated.

## 6. Phase 1 Scope

- Text product/topic description and optional text audience description.
- Optional text-only image context; image upload and vision analysis are out of scope.
- Tones: professional, casual, funny, promotional, luxury, educational.
- Lengths: short, medium, long.
- Targets: Instagram, Telegram, LinkedIn, Twitter/X.
- Language modes: Persian, English, mixed.
- Hashtag count selection, three variations by default, up to five by user choice.
- Separate caption/hashtag output, character count, platform-fit warning, copy,
  regenerate, history, credit estimate/reserve/settle/release, RTL/error states.

## 7. Out of Scope

Image upload, vision analysis, automatic posting, scheduling, multi-account
management, published-post analytics, competitor analysis, real payment activation,
and bulk CSV import.

## 8. Functional Requirements

1. ICG-FR-001: Authenticated submit accepts description and rejects empty, too-short, or policy-invalid text.
2. ICG-FR-002: Tone selection persists in generation request and returned metadata.
3. ICG-FR-003: Length selection constrains requested caption intent.
4. ICG-FR-004: Platform selection applies destination-specific output constraints.
5. ICG-FR-005: Language mode is sent with the request and displayed with results.
6. ICG-FR-006: Hashtag count selection controls requested hashtag output.
7. ICG-FR-007: API returns credit estimate before provider execution.
8. ICG-FR-008: Insufficient credits block provider execution before generation.
9. ICG-FR-009: Valid generation reserves credits before provider dispatch.
10. ICG-FR-010: Default generation returns three distinct variations; user may request up to five.
11. ICG-FR-011: Each result separates caption text, hashtags, and character count.
12. ICG-FR-012: Copy caption or hashtags performs no credit charge.
13. ICG-FR-013: Regeneration creates a new billable request with visible estimate.
14. ICG-FR-014: Successful outputs persist tenant-scoped history for reopen.
15. ICG-FR-015: Unsafe content produces an actionable policy state and releases any hold.
16. ICG-FR-016: All history and requests enforce tenant isolation.

## Document Status: Part 1 of 2 Complete
Sections 1-8 are written. Sections 9 (UI States) through 17 (Open Decisions) will be completed in Part 2. This document is not yet complete or ready for implementation review.
