# Timeout and Resilience

## Document Control
**Status:** Draft (Part 1 of 2 — Part 2 pending)
**Phase:** Phase 1 — In Progress
**Last updated:** 2026-08-23
**Related:** [ADR-0002](../decisions/0002-phase-1-product-metering-and-infrastructure.md), [Chat API](API_CONTRACT_V1_CHAT.md), [Features API](API_CONTRACT_V1_FEATURES.md), [Metering](CHAT_TIER_AND_METERING.md)

## Overview
This document defines Phase 1 timeout budgets, failure handling, and resilience.
Users must never lose credits due to provider or system failure. All failure paths
release reservations. Values are configuration targets, not final hardcoded policy.

## Section 1: Timeout Budget Model

### 1.1 The 60-Second Total Budget
| Stage | Budget | Applies To | On Timeout |
|---|---|---|---|
| Connection establishment | 5s | Provider calls | Release; provider_unavailable |
| First token / byte | 20s | Streaming Chat | Release; provider_timeout |
| First response | 30s | Enhancer/Caption | Release; provider_timeout |
| Stream idle gap | 15s | Streaming Chat | Release; failed message |
| Total request duration | 60s | Provider calls | Release; provider_timeout |

Values are initial targets, calibrated in C0, externalized, and nested in total.

### 1.2 Internal Timeouts
| Operation | Budget | On Timeout |
|---|---|---|
| Database query | 5s | internal_error; no pre-reservation charge |
| Wallet reserve | 5s | fail before provider; no charge |
| Wallet settle | 10s | idempotent retry and alert |
| Wallet release | 10s | idempotent retry and expiry safety net |

### 1.3 Critical Settle/Release Rules
Provider success with failed settle retries idempotently; value was delivered and
settlement must complete. Provider failure with failed release retries; the
10-minute expiry job releases remaining hold. Settle failure cannot double charge;
release failure cannot lock credits beyond expiry.

## Section 2: Provider Failure Handling

| Failure Type | Detection | Response | Billing Effect |
|---|---|---|---|
| Connection/DNS | Immediate | provider_unavailable | Release |
| Provider 5xx | Status | provider_unavailable | Release |
| Provider 429 | Status | rate_limited | Release |
| Timeout | Budget exceeded | provider_timeout | Release |
| Malformed response | Validation | provider_unavailable | Release |
| Mid-stream disconnect | Stream interruption | error event | Release |
| Content policy rejection | Provider code | unsafe_content | Release |

Every failure releases reservation, logs request/route/stage/elapsed metadata, and
returns actionable machine-readable error. Partial streaming output may be marked
failed but is free. Phase 1 does not silently retry, mid-request failover, or queue
failed work.

## Document Status: Part 1 of 2 Complete
This document contains Document Control, Overview, Timeout Budget Model, and
Provider Failure Handling. Pending: Circuit Breaker, Rate Limiting, Background
Jobs, Degraded Mode/Health, and D2.6/C0 items.
