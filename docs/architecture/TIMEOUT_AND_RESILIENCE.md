# Timeout and Resilience

## Document Control
**Status:** Draft — Complete Timeout and Resilience
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

## Section 3: Circuit Breaker Policy

Circuit breaker protects provider routes from cascading failures. It applies per
provider route/model class. Closed permits calls; Open rejects before reservation;
Half-Open allows probes. Initial configurable trip targets: 50% errors across 20
requests in 2 minutes, or 5 consecutive timeouts/connection failures. Open waits
60 seconds; three probes with two successes closes. Circuit-open rejection creates
no reservation or charge.

## Section 4: Rate Limiting

| Dimension | Initial Target | On Exceed |
|---|---|---|
| Per-user billable requests | 30 / minute | 429 rate_limited |
| Per-user chat messages | 20 / minute | 429 rate_limited |
| Per-user login attempts | 10 / 15 minutes | 429 rate_limited |
| Per-IP login attempts | 30 / 15 minutes | 429 rate_limited |
| Tenant concurrent billable ops | 5 | 429 rate_limited |

Values are configuration targets. Reject before reservation; if rejection occurs
after hold, release immediately.

## Section 5: Background Jobs

Reservation expiry sweeper runs every minute, releases reserved entries expired
beyond 10 minutes, appends one release ledger entry, and never double-releases.
Feature retention cleanup runs daily: soft-delete 90-day histories, optionally
hard-delete after 30-day grace, never delete ledger/receipts. Session cleanup runs
daily for expired/revoked sessions. Settle/release retry uses bounded backoff and
alerts on exhausted settle retries. Jobs are tenant-safe and log counts/errors.

## Section 6: Degraded Mode and Health Checks

Liveness is process up; readiness includes database and critical configuration.
DB or wallet outage returns service error and creates no new reservation. Open
provider circuit returns provider_unavailable without reservation. High load returns
rate_limited before reservation. Never leave a billable request unresolved.

## Section 7: Open Items for D2.6 / C0 / C1

D2.6 refines limits, SLOs, alert thresholds, dashboards. C0 proves expiry release,
no charge on failure, idempotent settle/release, circuit pre-reservation rejection,
and staged timeouts. C1 delivers configurable timeout, breaker store, rate limiter,
background jobs, metrics, and structured failure logs.

## Final Status
This is a complete draft of Phase 1 Timeout and Resilience for C0/C1.
