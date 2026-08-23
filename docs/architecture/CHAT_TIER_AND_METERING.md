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

## Section 5: Tier Assignment Algorithm

Token Budget Manager assigns a user-facing tier before execution using deterministic
rules, not machine-learned pricing.

### 5.1 Estimate Score Inputs
- input_message_size_bucket: low / medium / high
- recent_context_bucket: low / medium / high
- summarized_context_bucket: none / small / large
- output_budget_bucket: low / medium / high
- model_cost_bucket: low / medium / high
- reasoning_cost_bucket: none / present
- safety_overhead_bucket: standard / elevated

### 5.2 Tier Decision Rules
Tier 1 requires low input, low/medium context, low output, low model cost, and no
reasoning. Tier 3 applies to high input/context/output/model cost, large summary
with medium/high output, or reasoning with medium/high context. Tier 2 is all
other requests. Numeric bucket boundaries are operational configuration, versioned
and auditable; assignment happens before reservation.

### 5.3 Configuration Surface
| Config Key | Purpose | Example Value Type |
|---|---|---|
| tier_input_low_max | Low input bucket | integer |
| tier_input_medium_max | Medium input bucket | integer |
| tier_context_low_max | Low context bucket | integer |
| tier_output_low_max | Low output bucket | integer |
| tier_model_cost_map | Model class mapping | JSON |
| tier_reasoning_enabled_classes | Reasoning classes | array |
| tier_safety_overhead_mode | Safety mode | enum |

Values are operationally configured, not hardcoded here.

## Section 6: Quote / Reserve / Settle / Release Rules

Quote: compute tier before provider execution; show/accept quote; quote is maximum
user charge. Reserve: after acceptance reserve quoted credits; failure stops
provider execution. Settle: on success settle `min(actual_mapped_credits,
quoted_credits)` and Phase 1 absorbs internal cost variance. Release: failure,
timeout, or cancellation releases full reservation; success releases unused
remainder.

Invariants: actual_credits never exceeds quoted_credits; reservation precedes
settlement; released reservations do not settle; settled reservations do not
release twice; each transition has immutable ledger entry.

## Section 7: Worked Examples

| Scenario | Estimated Tier | Quoted Credits | Final Outcome | User Charge |
|---|---|---|---|---|
| Short question, short context | Tier 1 | 1 | success | 1 |
| Moderate request/history | Tier 2 | 2 | success | 2 |
| Large request, long context | Tier 3 | 3 | timeout, release | 0 |
| Lower actual usage | Tier 3 | 3 | settle 2, release 1 | 2 |

Examples are illustrative; exact thresholds are configured outside this document.

## Document Status: Part 2 of 3 Complete

This document contains Document Control, Overview, Sections 1–7, tier assignment,
and quote/reserve/settle/release rules. Pending in Part 3: variance telemetry,
summarization trigger, retry/failure semantics, and implementation notes.
