# Persian AI Workspace - Platform Roadmap (Phase 0)

> **New Direction:** This repository is no longer an AI subscription account reseller. The legacy shared-account model is **deprecated** and archived.

> **Legacy Code:** Original backend/frontend incomplete code has been archived to branch `archive/legacy-code-2026-07-19` at `archive/legacy_2026-07-19/` for reference without deletion of history.

We are now building a **phased Persian-first AI platform** for creators, businesses, developers, and everyday users.

## What the Platform Will Include (Phased)

**User-facing:**
- General Persian chat
- Prompt enhancement
- Specialist personas (evidence-based, not authoritative)
- Image generation
- Product Photography Studio
- Video generation
- AI character/influencer tools
- Telegram integration
- Wallet and credit billing
- Developer APIs
- Business agents
- Research and RAG
- Future Agent Marketplace (idea)

**How it will be built:**
- Solo founder + **external project-building agents** (coding agents, research agents, design agents, marketing agents, SEO agents) now
- Some of these may become **internal automated agents** later, connected to APIs with strict approval gates

## Project Structure Now (Phase 0)

This branch `docs/phase-0-agent-operating-system` contains **documentation + GitHub planning only** - no production code, no secrets, no deploy.

### Key Docs

- **Roadmap:** [`docs/roadmap/MASTER_ROADMAP.md`](docs/roadmap/MASTER_ROADMAP.md)
- **Agent Operating System:** [`docs/agents/AGENT_OPERATING_SYSTEM.md`](docs/agents/AGENT_OPERATING_SYSTEM.md)
- **Human Approval Gates:** [`docs/agents/HUMAN_APPROVAL_GATES.md`](docs/agents/HUMAN_APPROVAL_GATES.md)
- **Product Vision:** [`docs/vision/PRODUCT_VISION.md`](docs/vision/PRODUCT_VISION.md)
- **Persona Framework:** [`docs/personas/PERSONA_FRAMEWORK.md`](docs/personas/PERSONA_FRAMEWORK.md)

### Roadmap Phases

See `docs/roadmap/MASTER_ROADMAP.md`:

- Phase 0: Foundation (current) - docs, Agent OS, GitHub structure, safety gates
- Phase 1: Core MVP - auth, wallet mock, general chat, prompt enhancer, landing
- Phase 2: Specialist Personas - evidence-based assistants
- Phase 3: Image Studio & Product Photography
- Phase 4: API Platform - API keys, usage logs
- Phase 5: Video & Character Tools
- Phase 6: Telegram & Business Agents
- Phase 7: Research & RAG with citations
- Phase 8: Agent Marketplace (future idea)

Each phase doc includes: objective, in/out scope, dependencies, technical/UX/business deliverables, required agents, test requirements, risk controls, exit criteria.

### Agent System Summary

**Three categories:**

1. **Project-building agents** (20): Orchestrator, Product Manager, Fullstack Builder, Website Builder, DevOps, QA/Security, Research, Prompt Engineer, RAG Knowledge, SEO Content, Growth Marketing, Social Media, Analytics, Customer Success, Sales/Partnership, Compliance/Risk, Finance/Unit Economics, Supplier Scout, App Store/ASO, Execution Coach - all L2 external now, PR/report output, human approval required.

2. **Runtime product agents** (for customers): General Persian Chat, Prompt Enhancer, Specialist Personas, Image Studio, Product Photography Studio, Video Gen, Character Tools, Telegram Agent, Business Agents, Research/RAG, Developer API.

3. **Internal operations agents** (future): SEO tech crawler, content draft, growth reporter, support draft, research scout - all draft-only initially, publish requires approval.

**Maturity Levels:**
- L0 Manual
- L1 Prompt-driven external agent
- L2 Semi-automated external agent with PR/report output (current primary)
- L3 Internal API-connected agent (future, draft-only + approval)
- L4 Autonomous with strict human approval gates (future idea, never for money/publishing/customer contact/pricing/config/merge/deploy/API keys/persona sensitive changes)

**Approval Gates - Must Require Human Approval:**
- publishing public content, spending money, contacting customers, bulk messages, changing prices, changing production config, merging PRs, deploying to production, creating/deleting API keys, modifying legal/medical/psychological personas, launching paid campaigns, issuing refunds/credits above threshold.

See `docs/agents/HUMAN_APPROVAL_GATES.md`.

### Documentation Map

- Vision: `docs/vision/`
- Roadmap: `docs/roadmap/` (9 phases)
- Agents: `docs/agents/` (OS, registry, maturity, permission, control tower, workflow, approval gates, project/ 20 specs, runtime/ 5 architectures)
- Personas: `docs/personas/` (framework, template, registry schema, backlog of 14 personas, pipeline, QA/red teaming)
- Growth: `docs/growth/` (growth system, SEO strategy, content engine, launch plan, experiment backlog, referral ideas, social media, landing strategy)
- Website: `docs/website/` (IA + 5 page requirements + SEO technical)
- Ops: `docs/ops/` (GitHub workflow, branching, labels, milestones, DoD, release, runbook, reporting cadence)
- Backlog: `docs/backlog/` (epics + 7 issue lists)
- GitHub Templates: `.github/ISSUE_TEMPLATE/` (7 templates) + `pull_request_template.md`

### Legacy Deprecation Notice

- **Shared consumer accounts:** Deprecated, violates provider ToS, archived.
- **Automated procurement from GGSel/FunPay/Oyunfor/Kie.ai/ShareTool:** Deprecated, no scraping, no bypassing geographic/KYC restrictions.
- **API-key resale, supplier scraping, crypto payment for MVP:** Not in Phase 0/1. Credit-based wallet planned, no mock payment verification.
- Old code archived, not deleted: `archive/legacy_2026-07-19/` on branch `archive/legacy-code-2026-07-19`.

### Quick Start (Phase 0 Docs Only)

```bash
git clone https://github.com/maryamghabel2-cloud/ai-subscription-platform.git
cd ai-subscription-platform
git checkout docs/phase-0-agent-operating-system

# Read roadmap
cat docs/roadmap/MASTER_ROADMAP.md
cat docs/agents/AGENT_OPERATING_SYSTEM.md

# No production build yet - docs only branch
```

For future MVP skeleton (Phase 1), see branch `mvp/v1-core-foundation` (separate docs/code) which will have docker compose.

### Growth & Safety

- No auto-publishing without review
- Growth loops: SEO → landing → signup → activation → referral
- Metrics: visits, signup conversion, activation, credit purchase, retention, CAC, LTV
- Persona safety: Evidence-based assistants, not certified professionals. For high-risk domains (psychologist, physician, legal, vet, plant with chemicals), require deep research, compliance review, disclaimer, escalation to professional, red teaming.
- No medical, legal, psychological authority claims.

### Contributing

This is documentation + planning phase. Use issue templates:

- Feature Request
- Persona Design
- Research Task
- Agent Task
- Growth Experiment
- SEO Content Task
- Bug Report

PRs require checklist from `pull_request_template.md`, no direct main commit, no secrets, human approval required for all publishing/spending/pricing/config/merge/deploy/API keys/persona changes.

### Links

- Master Roadmap: [docs/roadmap/MASTER_ROADMAP.md](docs/roadmap/MASTER_ROADMAP.md)
- Agent OS: [docs/agents/AGENT_OPERATING_SYSTEM.md](docs/agents/AGENT_OPERATING_SYSTEM.md)
- Approval Gates: [docs/agents/HUMAN_APPROVAL_GATES.md](docs/agents/HUMAN_APPROVAL_GATES.md)
- Product Vision: [docs/vision/PRODUCT_VISION.md](docs/vision/PRODUCT_VISION.md)
- Persona Framework: [docs/personas/PERSONA_FRAMEWORK.md](docs/personas/PERSONA_FRAMEWORK.md)
- Growth System: [docs/growth/GROWTH_SYSTEM.md](docs/growth/GROWTH_SYSTEM.md)

### License

MIT - See LICENSE file. This is planning documentation, not production code.

---

**Status:** Phase 0 - Foundation docs in PR, not merged to main yet. See PR: `docs: define phase 0 roadmap and agent operating system`
