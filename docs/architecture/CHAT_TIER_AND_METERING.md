# Chat Tier and Token Metering

## Document Control
**Title:** Chat Tier and Token Metering
**Status:** Draft (Part 1 of 3 — Parts 2 and 3 pending)
**Phase:** Phase 1 — In Progress
**Last updated:** 2026-08-23
**Related:** [ADR-0002](../decisions/0002-phase-1-product-metering-and-infrastructure.md), [API](API_CONTRACT_V1.md), [Chat API](API_CONTRACT_V1_CHAT.md), [Pricing](PRICING_AND_UNIT_ECONOMICS.md), [Chat PRD](../product/GENERAL_CHAT_PRD.md)

## Overview
Chat billing is user-facing credits, not provider tokens. Phase 1 has 1, 2, and
3 credit tiers. Token Budget Manager estimates before execution and assigns tier.
Displayed quote is maximum charge; internal provider cost is tracked separately.

## Section 1: Metering Principles
1. User pricing is predictable.
2. Raw tokens are internal inputs.
3. Quote-before-execution is mandatory.
4. User charge never exceeds accepted quote.
5. Prompt and expected completion affect estimate.
6. Conversation context affects estimate.
7. Summarized context affects estimate when used.
8. Cached discounts may reduce internal cost.
9. Reasoning tokens count when reported.
10. Provider/model identifiers are configuration.
11. Metering is auditable after execution.
12. Pricing is owner-controlled.

## Section 2: Inputs to the Chat Estimate
| Input | Description | Used in Estimate | User-visible? | Source |
|---|---|---|---|---|
| current_user_message_tokens | Current input | Yes | No | Token Budget Manager |
| recent_conversation_context_tokens | Recent history | Yes | No | Conversation state |
| summarized_context_tokens | Prior summary | Yes | No | Conversation state |
| configured_max_output_tokens | Output budget | Yes | No | Provider config |
| provider_model_cost_multiplier | Route cost factor | Yes | No | Provider config |
| reasoning_token_estimate | Reasoning usage | Yes | No | Provider config |
| cached_token_discount_estimate | Cache reduction | Yes | No | Provider data |
| safety_overhead_tokens | Safety instructions | Yes | No | System prompt |
| system_prompt_tokens | System context | Yes | No | System prompt |
| routing_overhead_tokens | Gateway overhead | Yes | No | Gateway |

## Section 3: User-Facing Tier Model
| Tier | User Charge | Meaning | Notes |
|---|---|---|---|
| Tier 1 | 1 credit | Low estimated cost | Short/simple |
| Tier 2 | 2 credits | Medium estimated cost | Moderate context/output |
| Tier 3 | 3 credits | High estimated cost | Long context/higher output |

Tiers are user-facing, not provider model classes. A Tier 1 request may route to
stronger provider when policy requires. Exact boundaries are deferred to Part 2.

## Section 4: Internal Cost vs User Charge
Internal cost uses provider token accounting; user charge uses credits. They may
differ. Phase 1 absorbs cost above quote and records variance for later review.

## Document Status: Part 1 of 3 Complete
This document contains Document Control, Overview, Metering Principles, Estimate
Inputs, Tier Model, and Internal Cost vs User Charge.

Pending in Part 2: assignment algorithm, quote/reserve/settle/release, idempotency,
and settlement examples.

Pending in Part 3: variance, summarization trigger, retry/failure semantics, and
implementation notes.
