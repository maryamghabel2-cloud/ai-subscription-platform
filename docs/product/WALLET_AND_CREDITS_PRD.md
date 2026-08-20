# Wallet & Credits PRD

## 1. Document Control

| Field | Value |
|---|---|
| Status | Draft |
| Phase | Phase 1 In Progress |
| Last updated | 2026-08-20 |
| Related | [Status](../CURRENT_IMPLEMENTATION_STATUS.md), [Phase 1](../roadmap/PHASE_1_CORE_MVP.md), [Chat](GENERAL_CHAT_PRD.md) |

## 2. Product Overview and Business Goal

Wallet is the commercial trust and billing-transparency layer. Credits are the
only billing unit. Phase 1 uses sandbox/mock payment only; no real provider is
activated. Clear balances, holds, and ledger records build early-adopter trust.

## 3. Target Users

- Individual user: needs current spendable credits before using a feature.
- Business user: needs feature-level usage visibility for operating costs.
- Power user: needs searchable history and receipts for reconciliation.
- Workspace admin: needs metadata-only workspace usage oversight.

## 4. User Problems and Jobs to Be Done

- I ran out of credits mid-task and want an immediate sandbox top-up path.
- I want to know which feature consumed credits before I repeat a request.
- Payment failed and I need clarity without double-charging.
- I need to distinguish reserved credits from settled usage.
- I need a durable history without being able to accidentally alter it.

## 5. User Stories

- As an individual user, I want header balance so I can decide whether to start work.
- As a business user, I want a wallet dashboard so I can review credit activity.
- As a power user, I want transaction history so I can reconcile prior usage.
- As a user, I want date filtering so I can inspect a billing period.
- As a user, I want feature filtering so I can identify Chat, Enhancer, or Caption usage.
- As a user, I want credit/debit filtering so I can separate top-ups from charges.
- As a user, I want status filtering so I can find failed or pending top-ups.
- As a user, I want sandbox top-up creation so I can test credit purchase flow.
- As a user, I want mock confirmation success so I can see credits available once.
- As a user, I want failure feedback so I know no credits were added.
- As a low-balance user, I want warning before a billable action blocks me.
- As an insufficient-balance user, I want a wallet redirect so I can recover.
- As a user, I want usage breakdown so I can understand feature consumption.
- As a user, I want a receipt view so I can reference a successful top-up.
- As a workspace admin, I want metadata-only usage so I can monitor without private content.

## 6. Phase 1 Scope

Available balance; navigation balance; dashboard; append-only history; pagination;
date, feature, direction, and status filters; usage breakdown; sandbox intent;
mock confirmation; pending/succeeded/failed/canceled states; receipt display;
low-balance warning; insufficient-balance recovery; reserve/settle/release
visibility; idempotent duplicate handling.

## 7. Out of Scope

Real gateways, stored cards, bank integrations, external-method refunds, tax
invoices, currency conversion, subscriptions, promotional credits, and manual
ledger editing.

## 8. Functional Requirements

1. WALLET-FR-001: On authenticated wallet request, read the authoritative backend balance and return available/reserved state; failure returns no fabricated balance.
2. WALLET-FR-002: After login, navigation requests current balance and renders a loading state until response or error.
3. WALLET-FR-003: Wallet dashboard opens only for the authenticated tenant and returns an unauthorized state otherwise.
4. WALLET-FR-004: History returns immutable entries most-recent-first with page metadata.
5. WALLET-FR-005: Date input narrows history to matching timestamps or shows no-results.
6. WALLET-FR-006: Feature filter narrows entries by Chat, Prompt Enhancer, or Caption Generator.
7. WALLET-FR-007: Direction filter separates credits from debits without changing balance.
8. WALLET-FR-008: Status filter separates pending, succeeded, failed, and canceled records.
9. WALLET-FR-009: Sandbox top-up request creates a uniquely identified mock payment intent.
10. WALLET-FR-010: Intent creation exposes pending state and does not credit balance.
11. WALLET-FR-011: Successful mock confirmation creates one sandbox credit ledger entry and refreshes balance.
12. WALLET-FR-012: Failed mock confirmation records failure and never credits balance.
13. WALLET-FR-013: Duplicate confirmation returns original outcome and never double-credits.
14. WALLET-FR-014: History is read-only; users cannot edit or delete ledger entries.
15. WALLET-FR-015: Usage breakdown aggregates visible feature entries without exposing other tenants.
16. WALLET-FR-016: Low balance displays a warning before an eligible billable action.
17. WALLET-FR-017: Insufficient balance links to wallet recovery before provider execution.
18. WALLET-FR-018: Succeeded sandbox top-ups expose receipt data or an MVP-optional receipt state.
19. WALLET-FR-019: Every balance, intent, and history query enforces tenant isolation.

## 9. Transaction State Model

| State | Allowed transitions | Balance impact | User-visible status | Retry behavior |
|---|---|---|---|---|
| pending | succeeded, failed, canceled | none | Awaiting confirmation | same idempotency key |
| succeeded | none | one credit entry | Credits added | replay returns success |
| failed | none | none | Payment failed | new intent required |
| canceled | none | none | Canceled | new intent required |
| idempotent replay | original state | no new entry | Original result | no duplicate action |

## 10. Ledger Entry Types

- Sandbox top-up credit: credits from successful mock confirmation.
- Usage reservation: temporary hold before billable execution.
- Usage settlement: debit recording completed usage.
- Usage release: new reversal-of-hold entry after failure or cancellation.

Ledger history is append-only; historical entries are never mutated or deleted.
Corrective entries are an Open Decision: Owner decision required before D2.

--- Sections 11-19 will be added in D1.1b-Part2 ---
