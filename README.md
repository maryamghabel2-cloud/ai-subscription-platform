# Persian AI Workspace - Persian-first Multimodal AI Workspace (Phase 1 Continuation)

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

## Project Structure Now (Phase 1 - Auth and Wallet Foundations Implemented, Real Payment Providers Not Active)

This Pull Request changes documentation and GitHub planning files only. The inherited repository still contains legacy application code (backend/ and frontend/ placeholders from earlier phase). This PR does not modify production application code, does not add secrets, and does not deploy.

### Key Docs

- **Roadmap:** [`docs/roadmap/MASTER_ROADMAP.md`](docs/roadmap/MASTER_ROADMAP.md)
- **Agent Operating System:** [`docs/agents/AGENT_OPERATING_SYSTEM.md`](docs/agents/AGENT_OPERATING_SYSTEM.md)
- **Human Approval Gates:** [`docs/agents/HUMAN_APPROVAL_GATES.md`](docs/agents/HUMAN_APPROVAL_GATES.md)
- **Product Vision:** [`docs/vision/PRODUCT_VISION.md`](docs/vision/PRODUCT_VISION.md)
- **Persona Framework:** [`docs/personas/PERSONA_FRAMEWORK.md`](docs/personas/PERSONA_FRAMEWORK.md)

### Roadmap Phases

See `docs/roadmap/MASTER_ROADMAP.md`:

- Phase 0: Foundation (completed, merged e4ad2f1, no longer current) - docs, Agent OS, GitHub structure, safety gates
- Phase 1: Core MVP (current continuation) - Part 1 Database (users/wallets/ledger), Part 2 Auth (opaque session tokens HttpOnly), Part 3A Wallet foundations implemented (atomic credit/debit, ledger append-only, balance never negative), Real payment providers not active (sandbox mock only, ZarinPal Part 3B future)
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

**Three categories (Updated 2026-07-20 - 28 project-building agents, mix L1/L2):**

1. **Project-building agents** (28 total: 19 L1 report/draft + 9 L2 branch+PR): Orchestrator (L2 docs/planning PRs only, does NOT write product code), Product Manager (L1), Fullstack Builder (L2), Website Builder (L2), DevOps (L2), QA/Security (L2), Research (L1), Prompt Engineer (L2), RAG Knowledge (L1), SEO Content (L1 draft-only), Growth Marketing (L1), Social Media (L1), Analytics (L1), Customer Success (L1), Sales/Partnership (L1), Compliance/Risk (L1), Finance/Unit Economics (L1), Supplier Scout (L1), App Store/ASO (L1), Execution Coach (L1), plus new per review: UX/Product Design (L2), Brand Visual Identity (L1), ML Inference Engineer (L2), Model Evaluation (L1), Trust & Safety (L1), Data Privacy Governance (L1), Localization & Accessibility (L2), SRE/Incident Response (L1) - **Authoritative: Total 28 = 19 L1 + 9 L2** - L1 = prompt-driven that returns report/draft NO branch/PR, L2 = may create scoped branch + PR, Orchestrator = L2 but docs/planning PRs only. Human approval required for merge/publish/spending.


## Authoritative Count (Extracted From Files - 2026-07-20 Verification)

**Total project-building agents: 28**
- **L1: 19** - Prompt-driven external agent that returns a report or draft, NO branch/PR
- **L2: 9** - May create scoped branch + PR (Orchestrator = L2 but docs/planning PRs only)

**Breakdown:**
- L1 (19): ANALYTICS, APP_STORE_ASO, BRAND_VISUAL_IDENTITY, COMPLIANCE_RISK, CUSTOMER_SUCCESS, DATA_PRIVACY_GOVERNANCE, EXECUTION_COACH, FINANCE_UNIT_ECONOMICS, GROWTH_MARKETING, MODEL_EVALUATION, PRODUCT_MANAGER, RAG_KNOWLEDGE, RESEARCH, SALES_PARTNERSHIP, SEO_CONTENT, SOCIAL_MEDIA, SRE_INCIDENT_RESPONSE, SUPPLIER_SCOUT, TRUST_SAFETY
- L2 (9): DEVOPS, FULLSTACK_BUILDER, LOCALIZATION_ACCESSIBILITY, ML_INFERENCE_ENGINEER, ORCHESTRATOR (docs/planning only), PROMPT_ENGINEER, QA_SECURITY, UX_PRODUCT_DESIGN, WEBSITE_BUILDER

| Agent Name | File | Maturity |
|---|---|---|
| Analytics Agent | ANALYTICS_AGENT.md | L1 |
| App Store/ASO Agent | APP_STORE_ASO_AGENT.md | L1 |
| Brand Visual Identity Agent | BRAND_VISUAL_IDENTITY_AGENT.md | L1 |
| Compliance/Risk Agent | COMPLIANCE_RISK_AGENT.md | L1 |
| Customer Success Agent | CUSTOMER_SUCCESS_AGENT.md | L1 |
| Data Privacy Governance Agent | DATA_PRIVACY_GOVERNANCE_AGENT.md | L1 |
| DevOps Agent | DEVOPS_AGENT.md | L2 |
| Execution Coach Agent | EXECUTION_COACH_AGENT.md | L1 |
| Finance/Unit Economics Agent | FINANCE_UNIT_ECONOMICS_AGENT.md | L1 |
| Fullstack Builder Agent | FULLSTACK_BUILDER_AGENT.md | L2 |
| Growth Marketing Agent | GROWTH_MARKETING_AGENT.md | L1 |
| Localization & Accessibility Agent | LOCALIZATION_ACCESSIBILITY_AGENT.md | L2 |
| ML Inference Engineer Agent | ML_INFERENCE_ENGINEER_AGENT.md | L2 |
| Model Evaluation Agent | MODEL_EVALUATION_AGENT.md | L1 |
| Orchestrator Agent | ORCHESTRATOR_AGENT.md | L2 (docs/planning PRs only) |
| Product Manager Agent | PRODUCT_MANAGER_AGENT.md | L1 |
| Prompt Engineer Agent | PROMPT_ENGINEER_AGENT.md | L2 |
| QA/Security Agent | QA_SECURITY_AGENT.md | L2 |
| RAG Knowledge Agent | RAG_KNOWLEDGE_AGENT.md | L1 |
| Research Agent | RESEARCH_AGENT.md | L1 |
| Sales/Partnership Agent | SALES_PARTNERSHIP_AGENT.md | L1 |
| SEO Content Agent | SEO_CONTENT_AGENT.md | L1 |
| Social Media Agent | SOCIAL_MEDIA_AGENT.md | L1 |
| SRE/Incident Response Agent | SRE_INCIDENT_RESPONSE_AGENT.md | L1 |
| Supplier Scout Agent | SUPPLIER_SCOUT_AGENT.md | L1 |
| Trust & Safety Agent | TRUST_SAFETY_AGENT.md | L1 |
| UX/Product Design Agent | UX_PRODUCT_DESIGN_AGENT.md | L2 |
| Website Builder Agent | WEBSITE_BUILDER_AGENT.md | L2 |



2. **Runtime product agents** (for customers, 11): General Persian Chat, Prompt Enhancer, Specialist Personas (evidence-based, structured, direct where appropriate, citation-aware), Image Studio, Product Photography Studio, Video Gen, Character Tools (consent gate), Telegram Agent (encrypted token), Business Agents (FAQ/lead/content draft), Research/RAG (citations), Developer API (hashed keys).

3. **Internal operations agents** (future, 5): SEO tech crawler, content draft, growth reporter, support draft, research scout - all draft-only initially, publish requires approval, future L3.

**Maturity Levels (Corrected per review):**
- L0 Manual: Human does task, no agent.
- L1 Prompt-driven external agent that returns a report or draft (no branch/PR itself)
- L2 External agent that may create a scoped branch and Pull Request (docs or code per separation of duties)
- L3 Internal API-connected agent (future, scoped key, read + draft-create, not publish)
- L4 Controlled automation with mandatory human approval gates (future idea, never for absolutely forbidden actions)

**Approval Gates - Must Require Human Approval (14 actions):**
- publishing public content, spending money, contacting customers, bulk messages, changing prices, changing production config, merging PRs, deploying to production, creating/deleting API keys, modifying legal/medical/psychological personas, launching paid campaigns, issuing refunds/credits above threshold, creating new agent type or escalating maturity, deleting data/banning users.

**Absolutely Forbidden / NO-GO (No human approval may authorize):**
- bypassing provider Terms of Service, bypassing geographic restrictions, bypassing sanctions, bypassing KYC, using fake identities, hiding prohibited end-user locations, sharing/reselling unauthorized credentials or raw supplier keys, CSAM, non-consensual intimate imagery, deepfake without consent, claiming professional authority (medical/legal/psych diagnosis/verdict/therapy).

See `docs/agents/HUMAN_APPROVAL_GATES.md` and `docs/agents/AGENT_PERMISSION_MODEL.md`.

### Documentation Map (Updated Phase 0 - 90 files → now 105+ files)

- Vision: `docs/vision/` (3 files)
- Roadmap: `docs/roadmap/` (10 files: MASTER + 9 phases 0-8, each with objective, in/out scope, dependencies, deliverables, agents, tests, risk controls including absolutely forbidden, exit criteria)
- Agents: `docs/agents/` (7 OS docs + project/ 28 specs (was 20, added 8 new: UX/Product Design, Brand Visual Identity, ML Inference Engineer, Model Evaluation, Trust & Safety, Data Privacy Governance, Localization & Accessibility, SRE Incident Response) with L1/L2 mix per registry + runtime/ 5 architectures) + 7 new governance docs in architecture/evaluation/safety/research
- Architecture: `docs/architecture/` (SYSTEM_CONTEXT, PROVIDER_ABSTRACTION_STRATEGY, DATA_CLASSIFICATION_AND_RETENTION)
- Evaluation: `docs/evaluation/` (MODEL_EVALUATION_STRATEGY, PERSONA_EVALUATION_STRATEGY with mandatory evidence fields)
- Safety: `docs/safety/` (TRUST_AND_SAFETY_FRAMEWORK)
- Research: `docs/research/` (SOURCE_QUALITY_POLICY with source hierarchy, publisher, dates, evidence grade, geographic scope, etc.)
- Personas: `docs/personas/` (6 files: framework with mandatory fields source hierarchy, evidence grade, publisher, publication/update/access dates, geographic scope, last review, conflicting handling, min primary sources, expert reviewer, citation requirements, benchmark, accuracy/hallucination metrics, knowledge-pack version, expiry; template, registry schema, backlog 14 personas with mandatory fields, pipeline, QA/red teaming)
- Growth: `docs/growth/` (8 files growth system, SEO strategy, content engine, launch plan, experiment backlog, referral ideas, social, landing strategy - no auto-publish rule)
- Website: `docs/website/` (6 files IA 15 pages + landing, pricing, agent directory, blog, SEO technical)
- Ops: `docs/ops/` (8 files workflow, branching, labels, milestones, DoD with HttpOnly cookies Secure SameSite, release, runbook, reporting cadence)
- Backlog: `docs/backlog/` (8 files epics + PHASE_0_ISSUES now includes 13 issues including repository metadata update task, PHASE_1_ISSUES, PHASE_2_ISSUES, AGENT_SYSTEM_ISSUES now 7 issues for 28 agents + governance docs, GROWTH, WEBSITE, PERSONA - each with title/purpose/owner/dependencies/AC/priority/phase/risk)
- GitHub Templates: `.github/ISSUE_TEMPLATE/` (7 templates: feature, persona, research, agent_task, growth_experiment, seo_content, bug) + `pull_request_template.md` with checklist, approval gates, absolutely forbidden, rollback

### Legacy Deprecation Notice

- **Shared consumer accounts:** Deprecated, violates provider ToS, archived.
- **Automated procurement from GGSel/FunPay/Oyunfor/Kie.ai/ShareTool:** Deprecated, no scraping, no bypassing geographic/KYC restrictions.
- **API-key resale, supplier scraping, crypto payment for MVP:** Not in Phase 0/1. Credit-based wallet planned, no mock payment verification.
- Old code archived, not deleted: `archive/legacy_2026-07-19/` on branch `archive/legacy-code-2026-07-19`.

### Quick Start (Phase 0 Merged - Docs on Main)

```bash
git clone https://github.com/maryamghabel2-cloud/ai-subscription-platform.git
cd ai-subscription-platform

# Docs are now on main (Phase 0 merged on 2026-07-19)
cat docs/roadmap/MASTER_ROADMAP.md
cat docs/agents/AGENT_OPERATING_SYSTEM.md
cat docs/CHANGELOG.md

# Verify branch exists before checkout - old docs branch was merged and may be deleted
git ls-remote --heads origin
```

Documentation for Phase 0 is now on `main`. No production build yet for Phase 0. The previous branch `docs/phase-0-agent-operating-system` was merged in PR #2 (merge commit e4ad2f1) and is no longer the source of truth.

For future MVP skeleton (Phase 1), see `docs/roadmap/PHASE_1_CORE_MVP.md` and upcoming branches for Phase 1 Part 1 (Database Schema). Always verify current remote branches with `git ls-remote --heads origin` before referencing.

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

**Status:** Phase 0 completed (merged e4ad2f1 on 2026-07-19, no longer current). Phase 1 Part 1 Database, Part 2 Auth (opaque session tokens), Part 3A Wallet foundations implemented (wallet table balance>=0, ledger append-only signed, atomic SELECT FOR UPDATE, sandbox mock provider only). Real payment providers are not active (ZarinPal Part 3B, crypto Part 3C future). Product direction: Persian-first multimodal AI Workspace and Professional Creative Studio (see docs/vision/PRODUCT_VISION.md). Latest merges: 6c38d6a product architecture audit, 093af0cb12ff43cad4bbd5a42400c0351bbfc741 architecture finalization v0.1.4-docs-aligned.
