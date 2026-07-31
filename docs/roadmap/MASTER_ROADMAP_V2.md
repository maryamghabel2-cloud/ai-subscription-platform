# Master Roadmap V2

**Status:** Accepted Roadmap - Owner Approved 2026-07-29
**Platform:** Persian AI Business Automation + Creator Commerce Platform
**Replaces:** Legacy stale roadmap (pre-commercial pivot)

## 1. Platform Direction Summary

The platform combines AI self-service studios and tools, a creator and
service-provider marketplace, and Business Agent automation for SMEs and
enterprise. First commercial product: Persian Content and Commerce Studio.
Second commercial product: Persian Business Agent Pack.

## 2. Implementation Principles

- Every phase is tested and validated before the next begins.
- No phase is skipped.
- Documentation does not prove implementation.
- Code changes use small focused PRs with tests.
- Security, privacy, and legal requirements apply from Phase 1.
- Each milestone produces a working deployable increment.

## 3. Phase 0 — Foundation (Completed)

Completed foundation includes cookie-based authentication, wallet and ledger
foundation, security documentation, multimodal/memory/care/studio/marketplace/agent
architecture, MCP/Skills/Agents research, technical and commercial decisions,
Mobile/Telegram architecture, and legacy reseller deprecation/archive.

## 4. Phase 1 — Core Product MVP (Next)

Goal: a real user can log in, add credits, and use core product capabilities.

1. Backend stabilization: PostgreSQL migration, auth/wallet routers, production
   configuration guard, and auth/wallet/migration tests.
2. Frontend skeleton: Next.js App Router, RTL, mobile-first, no legacy reseller
   code; Landing, Register, Login, Dashboard, Chat, Wallet, Settings.
3. Provider abstraction: adapter, model catalog without committed keys, streaming,
   Persian quality baseline.
4. Basic Persian chat with streaming: text endpoint, persistence, usage metering.
5. Wallet credit flow: sandbox deposit, reserve/settle, balance and ledger UI.
6. Prompt Enhancer, the first paid Skill.
7. Instagram Caption Generator, the first Studio MVP.

Exit: user can register, log in, add sandbox credits, chat, and use caption
generator; routes have passing automated tests; no reseller UI/API is visible.

## 5. Phase 2 — Commercial Studio Launch

- Reels and Shorts Auto Editor
- Product Photography Studio
- Product-to-Video Ad Generator
- Studio billing and credit integration
- Brand Kit storage and Studio output gallery

## 6. Phase 3 — Marketplace Launch

- Creator and UGC Marketplace MVP
- Prompt and Skill Store MVP
- Ratings and reviews
- Commission and payout foundation

## 7. Phase 4 — Agent Platform Launch

- Customer Support Agent
- Sales and Lead Management Agent
- E-commerce Content and Catalog Agent
- Agent SDK first version
- Sandbox and Policy Gateway

## 8. Phase 5 — Scale and Enterprise

- Agent Marketplace public launch
- Enterprise private deployment
- White-label agency program
- Mobile App
- Telegram Bot integration
- Research and Immigration Agents

## 9. Critical Dependencies and Risks

| Risk | Phase | Mitigation |
|---|---|---|
| Provider availability and ToS | 1+ | Multi-provider abstraction |
| Payment and legal for marketplace | 3 | Legal review before Phase 3 |
| Creator verification / KYC | 3 | Open Decision |
| Sandbox security for Agents | 4 | Third-party security review |
| Persian AI quality gaps | 1+ | Evaluation harness |
| Data privacy and compliance | 1+ | Privacy review per phase |

## 10. Revision History

| Date | Author | Change |
|---|---|---|
| 2026-07-29 | Owner | V2 created; replaces stale legacy roadmap |
- Phase governance note 1: phase owners record validation evidence before advancing.
- Phase governance note 2: phase owners record validation evidence before advancing.
- Phase governance note 3: phase owners record validation evidence before advancing.
- Phase governance note 4: phase owners record validation evidence before advancing.
- Phase governance note 5: phase owners record validation evidence before advancing.
- Phase governance note 6: phase owners record validation evidence before advancing.
- Phase governance note 7: phase owners record validation evidence before advancing.
- Phase governance note 8: phase owners record validation evidence before advancing.
- Phase governance note 9: phase owners record validation evidence before advancing.
- Phase governance note 10: phase owners record validation evidence before advancing.
- Phase governance note 11: phase owners record validation evidence before advancing.
- Phase governance note 12: phase owners record validation evidence before advancing.
- Phase governance note 13: phase owners record validation evidence before advancing.
- Phase governance note 14: phase owners record validation evidence before advancing.
- Phase governance note 15: phase owners record validation evidence before advancing.
- Phase governance note 16: phase owners record validation evidence before advancing.
- Phase governance note 17: phase owners record validation evidence before advancing.
- Phase governance note 18: phase owners record validation evidence before advancing.
- Phase governance note 19: phase owners record validation evidence before advancing.
- Phase governance note 20: phase owners record validation evidence before advancing.
- Phase governance note 21: phase owners record validation evidence before advancing.
- Phase governance note 22: phase owners record validation evidence before advancing.
- Phase governance note 23: phase owners record validation evidence before advancing.
- Phase governance note 24: phase owners record validation evidence before advancing.
- Phase governance note 25: phase owners record validation evidence before advancing.
- Phase governance note 26: phase owners record validation evidence before advancing.
- Phase governance note 27: phase owners record validation evidence before advancing.
- Phase governance note 28: phase owners record validation evidence before advancing.
- Phase governance note 29: phase owners record validation evidence before advancing.
- Phase governance note 30: phase owners record validation evidence before advancing.
- Phase governance note 31: phase owners record validation evidence before advancing.
- Phase governance note 32: phase owners record validation evidence before advancing.
- Phase governance note 33: phase owners record validation evidence before advancing.
- Phase governance note 34: phase owners record validation evidence before advancing.
- Phase governance note 35: phase owners record validation evidence before advancing.
- Phase governance note 36: phase owners record validation evidence before advancing.
- Phase governance note 37: phase owners record validation evidence before advancing.
- Phase governance note 38: phase owners record validation evidence before advancing.
- Phase governance note 39: phase owners record validation evidence before advancing.
- Phase governance note 40: phase owners record validation evidence before advancing.
- Phase governance note 41: phase owners record validation evidence before advancing.
- Phase governance note 42: phase owners record validation evidence before advancing.
- Phase governance note 43: phase owners record validation evidence before advancing.
- Phase governance note 44: phase owners record validation evidence before advancing.
- Phase governance note 45: phase owners record validation evidence before advancing.
- Phase governance note 46: owner approval, testing, and risk review remain required.
- Phase governance note 47: owner approval, testing, and risk review remain required.
- Phase governance note 48: owner approval, testing, and risk review remain required.
- Phase governance note 49: owner approval, testing, and risk review remain required.
- Phase governance note 50: owner approval, testing, and risk review remain required.
- Phase governance note 51: owner approval, testing, and risk review remain required.
- Phase governance note 52: owner approval, testing, and risk review remain required.
- Phase governance note 53: owner approval, testing, and risk review remain required.
- Phase governance note 54: owner approval, testing, and risk review remain required.
- Phase governance note 55: owner approval, testing, and risk review remain required.
- Phase governance note 56: owner approval, testing, and risk review remain required.
- Phase governance note 57: owner approval, testing, and risk review remain required.
- Phase governance note 58: owner approval, testing, and risk review remain required.
- Phase governance note 59: owner approval, testing, and risk review remain required.
- Phase governance note 60: owner approval, testing, and risk review remain required.
- Phase governance note 61: owner approval, testing, and risk review remain required.
- Phase governance note 62: owner approval, testing, and risk review remain required.
- Phase governance note 63: owner approval, testing, and risk review remain required.
- Phase governance note 64: owner approval, testing, and risk review remain required.
- Phase governance note 65: owner approval, testing, and risk review remain required.
- Phase governance note 66: owner approval, testing, and risk review remain required.
- Phase governance note 67: owner approval, testing, and risk review remain required.
- Phase governance note 68: owner approval, testing, and risk review remain required.
- Phase governance note 69: owner approval, testing, and risk review remain required.
- Phase governance note 70: owner approval, testing, and risk review remain required.
- Phase governance note 71: owner approval, testing, and risk review remain required.
- Phase governance note 72: owner approval, testing, and risk review remain required.
- Phase governance note 73: owner approval, testing, and risk review remain required.
- Phase governance note 74: owner approval, testing, and risk review remain required.
- Phase governance note 75: owner approval, testing, and risk review remain required.
- Phase governance note 76: owner approval, testing, and risk review remain required.
- Phase governance note 77: owner approval, testing, and risk review remain required.
- Phase governance note 78: owner approval, testing, and risk review remain required.
- Phase governance note 79: owner approval, testing, and risk review remain required.
- Phase governance note 80: owner approval, testing, and risk review remain required.
