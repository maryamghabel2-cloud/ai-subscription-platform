# SYSTEM CONTEXT - Phase 0 Governance

**Date:** 2026-07-20
**Status:** Planning doc only, no code

## Purpose
Define system boundaries, actors, external dependencies, data flows at high level.

## Context Diagram (C4 Level 1)

**Actors:**
- End User (Creator, Business Owner, Developer, Researcher) - Persian, via web (Phase 1) or Telegram (Phase 6 future)
- Founder (solo founder + external project-building agents)
- External AI Providers (OpenAI-compatible API for chat, image model API, video model API, embedding model) - wrapper, not training from scratch

**System:** Persian AI Workspace Platform
- Frontend: Next.js 14 App Router, Tailwind, RTL, Persian typography, mobile-first
- Backend: FastAPI, Postgres, Alembic, JWT HttpOnly cookies, wallet ledger mock Phase 1
- Storage: Postgres for user/wallet/ledger, future S3-compatible for images/videos, future pgvector for RAG

**External Systems:**
- Email (future for verification, not Phase 0)
- Telegram Bot API (Phase 6)
- S3-compatible storage (Phase 3)
- Analytics (PostHog future)

## Boundaries

- Platform does NOT include training LLMs from scratch in Phase 0-1
- No direct access to supplier marketplaces GGSel/FunPay etc - deprecated
- No shared consumer accounts, no credential reselling - absolutely forbidden
- No bypassing ToS, geographic, sanctions, KYC, fake identities, hiding locations - absolutely forbidden

## Data Flows (High Level)

- User register/login → backend auth → HttpOnly cookie set → protected routes check cookie → wallet check → LLM API call → audit log → response
- Image studio: upload → prompt enhance → image model API → storage → gallery
- Persona chat: select persona → load persona prompt + knowledge pack version + RAG (future) → LLM → disclaimer + citations → audit
- Telegram: user Telegram message → Telegram webhook → business agent logic → reply via Telegram API

## Non-Functional

- Security: HttpOnly cookies, Secure flag prod, SameSite Lax/Strict, CSRF, bcrypt, rate limiting, no secrets in repo
- Privacy: Data classification, retention (see DATA_CLASSIFICATION_AND_RETENTION)
- Safety: Human approval gates for publishing/spending/contact/pricing/config/merge/deploy/API keys/persona edits

## Deployment Context (Future, Not Now)

- Phase 1 local: docker compose postgres + backend + frontend
- Future staging/prod: Not in Phase 0 - will need SRE Incident Response runbook

## Linkage
- Provider Abstraction: PROVIDER_ABSTRACTION_STRATEGY.md
- Data: DATA_CLASSIFICATION_AND_RETENTION.md
- Trust & Safety: TRUST_AND_SAFETY_FRAMEWORK.md
