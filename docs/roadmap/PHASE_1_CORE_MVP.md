# Phase 1 - Core MVP

**Phase:** PHASE_1_CORE_MVP  
**Date:** 2026-07-19  
**Updated:** 2026-07-20 - Fixed auth to HttpOnly cookies, added Persian-first baseline
**Status:** Planned (Phase 0 is current)

## Objective
Working deployable skeleton: Auth (secure), wallet mock, general Persian chat, prompt enhancer, Persian-first landing page.

## In Scope
- FastAPI + Postgres: User, Wallet ledger (mock), auth (register/login/me) with secure HttpOnly cookies
- Next.js 14 landing (Persian-first baseline), login, register, dashboard
- General Persian chat (wrapper, not training)
- Prompt enhancer tool (Persian-aware)
- Wallet credit display (no real payment yet)
- Header, ChatBox components with RTL, Persian typography, mobile-first

## Out of Scope
Payment integration (real), admin dashboard, personas, image studio, video, Telegram, API platform, RAG, full localization polish (Phase 2), SEO agents

## Dependencies
Phase 0 docs, especially AGENT_OPERATING_SYSTEM, HUMAN_APPROVAL_GATES, PERSONA_FRAMEWORK for safety

## Technical Deliverables
- backend: User model, JWT via HttpOnly cookies (Secure flag in production, SameSite=Lax/Strict, short-lived access sessions ~30min, refresh rotation future), /auth/* with CSRF protection where applicable, /chat echo then real LLM, no localStorage for tokens
- frontend: pages with axios withCredentials true, protected dashboard checks /auth/me via cookie, no token in localStorage, no auth token in JS accessible storage
- docker-compose: postgres:15-alpine, backend uvicorn reload, frontend npm dev, ports 5432:5432, 8000:8000, 3000:3000, env file from .env.example, alembic migrations
- Cookie settings: HttpOnly, Secure in prod, SameSite=Lax, Path=/, Max-Age short-lived, CSRF token double-submit or SameSite protection

## UX Deliverables
- **Persian-First Baseline (Must in Phase 1):** RTL layout dir=rtl, Persian primary navigation (خانه، چت، پرسوناها، استودیو محصول، قیمت‌گذاری - or at least Persian labels for core nav), Persian forms and user-facing error messages (e.g., ایمیل قبلا ثبت شده, رمز عبور اشتباه), Persian-compatible typography (Vazirmatn or similar), mobile-first responsive layout (tested 360px, 768px, 1024px)
- Landing with value prop Persian (or bilingual) + CTA
- Login/register forms Persian labels, Persian error messages
- Dashboard chat with RTL, Persian placeholder
- Error handling Persian primary, English fallback
- Full localization polish deferred to Phase 2, but baseline Persian UX not out of scope

## Business Deliverables
- Credit mock, no real purchase, clearly marked as mock
- Activation metric tracked (signup → first chat)
- Pricing page shows credit packs mock

## Required Agents
Already updated - UX Product Design, Brand Visual Identity, Trust Safety, Data Privacy, Localization, SRE + existing
Fullstack Builder (L2), Website Builder (L2), DevOps (L2), QA Security (L2), Prompt Engineer (L2), plus new: UX/Product Design (L2), Localization & Accessibility (L2), Trust & Safety (L1), Data Privacy Governance (L1)


**Additional per review (new 8 agents):** Already updated - UX Product Design, Brand Visual Identity, Trust Safety, Data Privacy, Localization, SRE

## Test Requirements
- Auth flow e2e: register → login sets HttpOnly cookie → /auth/me returns user → logout clears cookie → protected /chat 401 without cookie
- No token in localStorage, no token in JS, Secure flag in prod, SameSite=Lax/Strict
- CSRF protection where applicable (e.g., double submit or SameSite)
- Protected /chat requires cookie auth
- Wallet mock display
- Landing loads with RTL, Persian nav, Persian form labels, mobile-first
- Persian typography loads
- Accessibility: labels for forms

## Risk Controls
- **Auth Security:** Do NOT use localStorage for JWT. Use HttpOnly cookies with Secure flag in production, SameSite=Lax or Strict, short-lived access sessions (e.g., 30min), CSRF protection via SameSite + CSRF token if needed. No token in localStorage, no token in URL. Passwords bcrypt, email validation, rate limit login (5/min).
- **Payment confusion:** Clearly mark wallet mock as mock, no real purchase
- **Rate limit:** Add basic rate limiting for auth (login 5/min per IP) and chat (30/min)
- **Persian UX:** RTL tested, Persian error messages, not English-only
- All human approval gates from HUMAN_APPROVAL_GATES.md must apply: spending money, publishing, contacting customers, changing prices/config, merging, deploying, API keys, persona changes, paid campaigns, refunds/credits above threshold require human approval.
- Absolutely forbidden actions have no approval path: ToS bypass, geographic/sanctions/KYC bypass, fake identities, hiding prohibited locations, credential sharing
- Audit logs required for all state-changing actions
- No medical/legal/psychological authoritative claims

## Exit Criteria
- User can register with Persian form, see Persian error messages if duplicate email
- Login sets HttpOnly Secure SameSite cookie, not localStorage
- /auth/me returns user via cookie auth
- User can chat general Persian (RTL UI) and see wallet mock
- Landing live locally via docker compose with RTL, Persian nav, mobile-first, Persian typography
- No localStorage JWT, no insecure auth design
- Docs updated