# Phase 1 - Core MVP

**Phase:** PHASE_1_CORE_MVP  
**Date:** 2026-07-19  
**Status:** Planned (Phase 0 is current)

## Objective
Working deployable skeleton: Auth, wallet mock, general chat, prompt enhancer, landing page.

## In Scope
- FastAPI + Postgres: User, Wallet ledger (mock), auth (register/login/me)
- Next.js 14 landing, login, register, dashboard
- General Persian chat (wrapper, not training)
- Prompt enhancer tool
- Wallet credit display (no real payment yet)
- Header, ChatBox components

## Out of Scope
Payment integration, admin dashboard, personas, image studio, video, Telegram, API platform, RAG, Persian full UI, SEO agents

## Dependencies
Phase 0 docs

## Technical Deliverables
- backend: User model, JWT, /auth/*, /chat echo then real LLM
- frontend: pages, axios JWT interceptor, protected dashboard
- docker-compose: postgres, backend, frontend
- alembic migrations

## UX Deliverables
- Landing with value prop + CTA
- Login/register forms
- Dashboard chat
- Error handling Persian/English mix simple

## Business Deliverables
- Credit mock, no real purchase
- Activation metric tracked

## Required Agents
Fullstack Builder, Website Builder, DevOps, QA Security, Prompt Engineer

## Test Requirements
- Auth flow e2e
- Protected /chat requires JWT
- Wallet mock display
- Landing loads

## Risk Controls
- Payment confusion → clearly mark mock
- Token storage → use localStorage for MVP but document httpOnly future
- No rate limit → add basic
- All human approval gates from HUMAN_APPROVAL_GATES.md must apply: spending money, publishing, contacting customers, changing prices/config, merging, deploying, API keys, persona changes, paid campaigns, refunds/credits above threshold require human approval.
- Audit logs required for all state-changing actions.
- No medical/legal/psychological authoritative claims.

## Exit Criteria
User can register, login, chat general, see wallet mock, landing live locally via docker compose
