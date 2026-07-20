# MASTER ROADMAP - Persian AI Platform

**Version:** Phase 0 Planning  
**Date:** 2026-07-19  
**Branch:** docs/phase-0-agent-operating-system

## Overview

Platform evolves from documentation & foundation → core MVP → personas → image studio → API platform → video/character → Telegram/business agents → Research/RAG → Agent Marketplace.

Legacy reseller model is **deprecated**.

## Phases

| Phase | Name | Goal | Status |
|---|---|---|---|
| 0 | Foundation | Docs, Agent OS, GitHub structure, safety gates | **Current** |
| 1 | Core MVP | Auth, wallet mock, general chat, prompt enhancer, landing | Planned |
| 2 | Personas | Evidence-based specialist personas framework, initial 5 personas | Planned |
| 3 | Image Studio | Image generation + Product Photography Studio | Planned |
| 4 | API Platform | Developer APIs, API keys, usage logs | Planned |
| 5 | Video & Character Tools | Video gen, AI character/influencer workflow | Planned |
| 6 | Telegram & Business Agents | Telegram integration, business agents low-code | Planned |
| 7 | Research & RAG | Upload docs, RAG attachment, citations, research persona | Planned |
| 8 | Agent Marketplace | Future marketplace for user-created agents | Future Idea |

## Cross-Cutting Systems (Built Gradually)

- Agent Operating System (`docs/agents/AGENT_OPERATING_SYSTEM.md`)
- Growth System (`docs/growth/GROWTH_SYSTEM.md`)
- Website IA (`docs/website/WEBSITE_INFORMATION_ARCHITECTURE.md`)
- Ops: GitHub workflow, labels, milestones, DoD

## Dependencies Rule

Each phase doc must list: objective, in/out scope, dependencies, technical/UX/business deliverables, required agents, test requirements, risk controls, exit criteria.

## Phases Link

- Phase 0: `PHASE_0_FOUNDATION.md`
- Phase 1: `PHASE_1_CORE_MVP.md`
- Phase 2: `PHASE_2_PERSONAS.md`
- Phase 3: `PHASE_3_IMAGE_STUDIO.md`
- Phase 4: `PHASE_4_API_PLATFORM.md`
- Phase 5: `PHASE_5_VIDEO_CHARACTER_TOOLS.md`
- Phase 6: `PHASE_6_TELEGRAM_BUSINESS_AGENTS.md`
- Phase 7: `PHASE_7_RESEARCH_RAG.md`
- Phase 8: `PHASE_8_AGENT_MARKETPLACE.md`

## Solo Founder + External Agents Model

Phase 0-2: Founder + **project-building external agents** (full-stack builder, research, SEO, growth) that output PRs/reports. Human approval required for all publishing, spending, merging.

Phase 3+: Some agents may become **internal L3/L4** API-connected with strict approval gates. See `AGENT_MATURITY_MODEL.md`

## Safety

All monetary, publishing, customer-contact, pricing, production config actions require human approval. See `HUMAN_APPROVAL_GATES.md`
