# Non-Functional Requirements

## Document Control
**Status:** Draft (Part 1A of 3 — Parts 1B and 2 pending)
**Phase:** Phase 1 — In Progress
**Last updated:** 2026-08-23
**Related:** [ADR-0002](../decisions/0002-phase-1-product-metering-and-infrastructure.md), [API](API_CONTRACT_V1.md), [Chat](API_CONTRACT_V1_CHAT.md), [Features](API_CONTRACT_V1_FEATURES.md), [Metering](CHAT_TIER_AND_METERING.md), [Resilience](TIMEOUT_AND_RESILIENCE.md)

## Overview
This document defines Phase 1 non-functional requirements. It covers performance,
usability, accessibility, reliability, observability, and security. Functional
correctness alone is insufficient for release readiness. Requirements guide QA and
production-readiness review.

## Section 1: Performance Requirements
| NFR ID | Requirement | Target | Applies To | Notes |
|---|---|---|---|---|
| NFR-PERF-001 | API reads respond | 500 ms p95 | auth/me, wallet, history, admin | Excludes provider generation |
| NFR-PERF-002 | Wallet reserve completes | 1 s p95 | Wallet reserve | Pre-provider |
| NFR-PERF-003 | Chat quote calculation | 1 s p95 | Token Budget Manager | Before reservation |
| NFR-PERF-004 | Chat first token | Lower target; 20 s budget | Chat streaming | Provider-dependent |
| NFR-PERF-005 | Feature first response | Lower target; 30 s budget | Enhancer, Caption | Provider-dependent |
| NFR-PERF-006 | Background jobs | No foreground impact | Cleanup, expiry | Batch only |

Targets are Phase 1 goals, measured after C0 baseline verification. Provider
latency is partly external; internal latency remains observable.

## Section 2: Capacity and Concurrency
| NFR ID | Requirement | Initial Target | Applies To | Notes |
|---|---|---|---|---|
| NFR-CAP-001 | Authenticated users | 100 concurrent users | Auth endpoints | Load baseline |
| NFR-CAP-002 | Billable operations | 5 concurrent | Reserve/provider | Rate aligned |
| NFR-CAP-003 | Chat messages | 20 messages/minute | Chat | Resilience aligned |
| NFR-CAP-004 | Billable requests | 30 requests/minute | Features | Resilience aligned |
| NFR-CAP-005 | Expiry sweeper | Batch-oriented | Background job | No full lock |
| NFR-CAP-006 | History pagination | Max 50 per page | Lists | No unbounded results |

Exact production-scale targets may change after usage telemetry.

## Document Status: Part 1A of 3 Complete

This document contains Document Control, Overview, Performance Requirements, and
Capacity and Concurrency.

Pending in Part 1B: UX/Responsiveness, Accessibility, RTL/Persian quality.
Pending in Part 2: Security/Privacy, Observability, Reliability, C0/C1 items,
and final status.
