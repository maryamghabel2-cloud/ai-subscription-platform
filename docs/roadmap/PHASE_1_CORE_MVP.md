# Phase 1 — Core Product MVP

**Date:** 2026-08-11  
**Status:** In Progress  
**Canonical Roadmap:** [MASTER_ROADMAP.md](MASTER_ROADMAP.md)

## Purpose

Phase 1 turns validated platform foundations into a usable Persian-first product.
It separates existing code foundations from pending commercial MVP capabilities.
Documentation does not itself verify runtime behavior.

## Platform Foundation

The following foundations have source-code evidence and remain validation-required:

- Database and migrations: `backend/app/database.py`, `backend/alembic/`.
- Authentication/session: `backend/app/api/auth.py`, `backend/app/models/auth_session.py`.
- Wallet and ledger: `backend/app/api/wallet.py`, `backend/app/services/wallet_service.py`, `backend/app/models/ledger.py`.
- Sandbox payment intents: `backend/app/api/payments.py`, `backend/app/providers/payment/mock.py`.

Canonical authentication uses HttpOnly secure cookies and session rotation. Browser-
accessible authentication tokens, including localStorage storage, are forbidden.

## Commercial MVP Pending Scope

1. Replace the current legacy/incomplete frontend with a clean RTL frontend.
2. Add a provider/model abstraction without committing production credentials.
3. Add General Persian Chat with streaming and conversation persistence.
4. Add wallet reserve/settle usage flow for AI requests.
5. Add Prompt Enhancer as the first paid Skill.
6. Add Instagram Caption Generator as the first Studio MVP.

## Ordered Work and Acceptance Criteria

- Stabilize backend configuration and PostgreSQL migration path; acceptance: test
  suite and migration smoke validation are executed in a future implementation PR.
- Build clean frontend skeleton; acceptance: legacy reseller UI is absent from the
  new product surface and RTL pages render.
- Build provider abstraction and chat; acceptance: authenticated user receives
  streamed Persian text through approved provider configuration.
- Integrate wallet usage; acceptance: reserve/settle entries are auditable.
- Deliver Prompt Enhancer and Caption Generator; acceptance: user-controlled
  execution, credit estimate/settlement policy, and tests are present.

## Out of Scope

Real payment provider activation, creator marketplace fulfillment, media rendering,
Agent runtime, public MCP server, and high-risk autonomous actions are not Phase 1
implementation scope.

## Security Requirements

All state-changing work follows approval gates, tenant isolation, audit logging,
and secure-cookie auth. Authentication tokens must never be stored in localStorage,
URLs, or browser-accessible JavaScript storage.
