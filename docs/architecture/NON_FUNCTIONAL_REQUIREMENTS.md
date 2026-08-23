# Non-Functional Requirements

## Document Control
**Status:** Draft — Complete Non-Functional Requirements
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

## Section 3: UX and Responsiveness Requirements
| NFR ID | Requirement | Target / Rule | Applies To | Notes |
|---|---|---|---|---|
| NFR-UX-001 | Credit estimate visible | Mandatory | Billable features | Trust |
| NFR-UX-002 | Available credits visible | Mandatory | Header/wallet | Awareness |
| NFR-UX-003 | Loading feedback | <= 300 ms | Interactive UI | Responsiveness |
| NFR-UX-004 | Readable billable error | Mandatory | Features | No silent failure |
| NFR-UX-005 | Insufficient link | Mandatory | Billable features | Wallet recovery |
| NFR-UX-006 | Copy feedback | <= 300 ms | Copy actions | Toast/inline |
| NFR-UX-007 | Chat state distinct | Mandatory | Chat | Generating/done/failed |
| NFR-UX-008 | Regenerate billed | Mandatory | Caption | Spend clarity |

Billing visibility and failure states are release readiness requirements.

## Section 4: Accessibility Requirements
| NFR ID | Requirement | Target / Rule | Applies To | Notes |
|---|---|---|---|---|
| NFR-A11Y-001 | Keyboard navigation | Mandatory | UI | No mouse-only action |
| NFR-A11Y-002 | Focus states | Mandatory | UI | Visible focus |
| NFR-A11Y-003 | Form labels | Mandatory | Forms | Screen readers |
| NFR-A11Y-004 | Heading hierarchy | Mandatory | Tools | Semantic order |
| NFR-A11Y-005 | Accessible errors | Mandatory | Async flows | Live status |
| NFR-A11Y-006 | Accessible names | Mandatory | Copy/wallet | Clear control |
| NFR-A11Y-007 | Non-color status | Mandatory | Status UI | Icon/text |

Phase 1 targets pragmatic WCAG AA alignment where feasible.

## Section 5: RTL and Persian Language Quality
| NFR ID | Requirement | Target / Rule | Applies To | Notes |
|---|---|---|---|---|
| NFR-RTL-001 | RTL layout | Mandatory | Global UI | No broken alignment |
| NFR-RTL-002 | Mixed scripts | Mandatory | Core features | Bilingual |
| NFR-RTL-003 | Readable numerals/punctuation | Mandatory | Text screens | No mirroring |
| NFR-RTL-004 | Persian output readability | Mandatory | Generated output | QA |
| NFR-RTL-005 | Copyable hashtags | Mandatory | Caption | No corruption |
| NFR-RTL-006 | No LTR assumptions | Mandatory | Core surfaces | Buttons/tables |

Material Persian readability defects are release blockers.

## Section 6: Security and Privacy Requirements
| NFR ID | Requirement | Target / Rule | Applies To | Notes |
|---|---|---|---|---|
| NFR-SEC-001 | HttpOnly Secure cookies | Mandatory | Auth | No browser token storage |
| NFR-SEC-002 | Password hashes | Mandatory | Users | bcrypt/argon2 |
| NFR-SEC-003 | HTTPS | Mandatory | APIs | No production HTTP |
| NFR-SEC-004 | CSRF defense | Mandatory | Mutations | SameSite/token |
| NFR-SEC-005 | Tenant isolation | Mandatory | Data | No cross tenant |
| NFR-SEC-006 | Admin metadata only | Mandatory | Admin | No content |
| NFR-SEC-007 | Secrets protected | Mandatory | Runtime | No repo/logs |
| NFR-SEC-008 | Rate limits | Mandatory | Sensitive APIs | Resilience |
| NFR-SEC-009 | Input validation | Mandatory | Features | Type/length |
| NFR-SEC-010 | Injection defense | Mandatory | Features | Policy |
| NFR-SEC-011 | Immutable ledger | Mandatory | Wallet | Compensate only |
| NFR-SEC-012 | PII minimization | Mandatory | Telemetry | No full content |

## Section 7: Observability and Monitoring Requirements
| NFR ID | Requirement | Target / Rule | Applies To | Notes |
|---|---|---|---|---|
| NFR-OBS-001 | request_id | Mandatory | APIs | Error shape |
| NFR-OBS-002 | Structured logs | Mandatory | Backend | JSON preferred |
| NFR-OBS-003 | Billing metrics | Mandatory | Wallet | Lifecycle |
| NFR-OBS-004 | Provider metrics | Mandatory | Gateway | Route latency |
| NFR-OBS-005 | Circuit metrics | Mandatory | Resilience | State changes |
| NFR-OBS-006 | Variance events | Mandatory | Metering | Cost review |
| NFR-OBS-007 | Job metrics | Mandatory | Jobs | Counts/errors |
| NFR-OBS-008 | Settle alerts | Mandatory | Wallet | Money risk |
| NFR-OBS-009 | Expiry alerts | Mandatory | Sweeper | Stuck paths |
| NFR-OBS-010 | No content logs | Mandatory | Logs | Privacy |

## Section 8: Reliability and Operational Readiness
| NFR ID | Requirement | Target / Rule | Applies To | Notes |
|---|---|---|---|---|
| NFR-REL-001 | Liveness/readiness separate | Mandatory | Deploy | Health |
| NFR-REL-002 | DB readiness | Mandatory | Deploy | Fail closed |
| NFR-REL-003 | Failure release | Mandatory | Features | No stranded credits |
| NFR-REL-004 | Expiry sweeper | Every minute | Jobs | 10-minute safety |
| NFR-REL-005 | Retention job | Daily | Jobs | 90-day policy |
| NFR-REL-006 | Alembic reviewed | Mandatory | Schema | Versioned |
| NFR-REL-007 | External config | Mandatory | Runtime | No hardcoded values |
| NFR-REL-008 | Clear degraded errors | Mandatory | APIs | Fail fast |
| NFR-REL-009 | Backup/restore | Mandatory | Ops | Test once |
| NFR-REL-010 | Iran access test | Mandatory | Production | No VPN target |

## Section 9: Open Items for C0/C1
C0 proves latency, pre-reservation limits/circuit behavior, no failure charge,
idempotency, tenant isolation, no browser tokens, RTL, admin metadata, expiry.
C1 delivers configuration, logs/metrics, background jobs, probes, accessibility,
backup runbook, and Iran-access evidence. Beyond MVP: certification, active-active,
APM selection, real-payment NFRs.

## Final Status
This is a complete draft of Phase 1 NFRs for C0/C1.
