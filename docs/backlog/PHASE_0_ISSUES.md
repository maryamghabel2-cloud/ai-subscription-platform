# PHASE 0 ISSUES

**Date:** 2026-07-19  
**Milestone:** Phase 0 Foundation

## Issue Template for Each

- Title, Purpose, Owner Agent Type, Dependencies, Acceptance Criteria, Priority, Phase Label, Risk Level

---

### ISSUE-0-01: Create Product Vision Docs

- **Title:** Create PRODUCT_VISION, BUSINESS_MODEL, USER_PERSONAS
- **Purpose:** Define new platform vision, not reseller
- **Owner Agent Type:** Product Manager
- **Dependencies:** None
- **Acceptance Criteria:** Files exist in docs/vision/, coherent, link to roadmap, no hype, no reseller claims
- **Priority:** P0
- **Phase Label:** phase-0
- **Risk Level:** Low

### ISSUE-0-02: Create Master Roadmap + 9 Phase Docs

- **Title:** Create MASTER_ROADMAP and PHASE_0 to PHASE_8 docs with required sections
- **Purpose:** Phased plan for solo founder + external agents
- **Owner:** Product Manager + Orchestrator
- **Dependencies:** 0-01
- **Acceptance:** All 10 roadmap files exist, each has objective, in/out scope, dependencies, technical/UX/business deliverables, required agents, test requirements, risk controls, exit criteria
- **Priority:** P0
- **Phase:** phase-0
- **Risk:** Low

### ISSUE-0-03: Agent Operating System Docs

- **Title:** Create AGENT_OPERATING_SYSTEM, REGISTRY, MATURITY, PERMISSION, CONTROL_TOWER, EXTERNAL_WORKFLOW, HUMAN_APPROVAL_GATES
- **Purpose:** Define 3 agent types, L0-L4, permissions, approval gates
- **Owner:** Product Manager + Compliance Risk
- **Dependencies:** 0-01
- **Acceptance:** 7 files exist, explain three types, maturity, permission model, approval gates list (publishing, spending, contacting, bulk, pricing, config, merge, deploy, API keys, persona edits, campaigns, refunds)
- **Priority:** P0
- **Phase:** phase-0
- **Risk:** Medium (safety critical)

### ISSUE-0-04: Project-Building Agent Specs (20 agents)

- **Title:** Create 20 agent specs in docs/agents/project/
- **Purpose:** Define how to use external agents to build product
- **Owner:** Orchestrator
- **Dependencies:** 0-03
- **Acceptance:** 20 files exist, each has purpose, when to use, phase relevance, inputs, outputs, tools now/later, permissions, forbidden, approval-required, success metrics, example prompt, example report
- **Priority:** P0
- **Phase:** phase-0
- **Risk:** Low

### ISSUE-0-05: Runtime Agent Architectures

- **Title:** Create runtime overview + 4 architecture docs
- **Purpose:** Define future user-facing agents
- **Owner:** Product Manager + Fullstack Builder
- **Dependencies:** 0-03
- **Acceptance:** 5 files exist, explain difference project vs runtime, persona system, prompt enhancer, memory, wallet, RAG, safety, versioning, audit, Telegram, API
- **Priority:** P1
- **Phase:** phase-0
- **Risk:** Low

### ISSUE-0-06: Persona System Docs

- **Title:** Create persona framework, template, registry schema, backlog, pipeline, QA/red teaming
- **Purpose:** Safe evidence-based personas
- **Owner:** Prompt Engineer + Compliance Risk
- **Dependencies:** 0-01
- **Acceptance:** 6 files exist, framework defines role, domain, tone, method, evidence standard, knowledge source requirements, prompt policy, escalation, risk classification, versioning, evaluation, future RAG. Backlog includes 14 personas with maturity, risk, research depth.
- **Priority:** P0
- **Phase:** phase-0
- **Risk:** High (medical/legal/psych framing)

### ISSUE-0-07: Growth & Marketing Docs

- **Title:** Create growth system, SEO strategy, content engine, launch plan, experiment backlog, referral, social, landing strategy
- **Purpose:** Growth loops without auto-publishing
- **Owner:** Growth Marketing + SEO Content
- **Dependencies:** 0-01
- **Acceptance:** 8 files exist, include growth loops, SEO clusters, landing types, programmatic SEO ideas, content approval workflow, experiment template, metrics (visits, signup conversion, activation, credit purchase, retention, CAC, LTV), no auto-publish rule
- **Priority:** P1
- **Phase:** phase-0
- **Risk:** Medium

### ISSUE-0-08: Website & Launch Docs

- **Title:** Create website IA + 5 page requirement docs + SEO technical
- **Purpose:** Plan website
- **Owner:** Website Builder + SEO Content
- **Dependencies:** 0-01
- **Acceptance:** 6 files exist, list planned pages: Home, Chat, Personas, Product Studio, API, Telegram, Business, Pricing, Blog, Docs, Contact, Terms, Privacy, Refund, Safety
- **Priority:** P1
- **Phase:** phase-0
- **Risk:** Low

### ISSUE-0-09: Ops Docs

- **Title:** Create GitHub workflow, branching, labels, milestone, DoD, release, runbook, reporting cadence
- **Purpose:** Solo founder GitHub ops
- **Owner:** Orchestrator + DevOps
- **Dependencies:** None
- **Acceptance:** 8 files exist, define workflow, labels list, milestones per phase, DoD, release strategy, agent runbook, reporting cadence weekly
- **Priority:** P0
- **Phase:** phase-0
- **Risk:** Low

### ISSUE-0-10: Backlog Docs

- **Title:** Create epics + 7 backlog issue files
- **Purpose:** Planned issues for Phase 0-2, agent system, growth, website, persona
- **Owner:** Product Manager
- **Dependencies:** 0-02
- **Acceptance:** 8 backlog files exist, each issue has title, purpose, owner agent type, dependencies, acceptance criteria, priority, phase label, risk level
- **Priority:** P0
- **Phase:** phase-0
- **Risk:** Low

### ISSUE-0-11: GitHub Templates

- **Title:** Create 7 issue templates + PR template
- **Purpose:** Standardize external agent tasks
- **Owner:** Orchestrator
- **Dependencies:** 0-09
- **Acceptance:** .github/ISSUE_TEMPLATE/ 7 files + pull_request_template.md exist, include approval gates, risk, checklists
- **Priority:** P0
- **Phase:** phase-0
- **Risk:** Low

### ISSUE-0-12: README Update

- **Title:** Update README to reflect Persian AI platform roadmap, deprecate reseller, link to MASTER_ROADMAP and AGENT_OPERATING_SYSTEM
- **Purpose:** Public-facing clarity
- **Owner:** Product Manager
- **Dependencies:** 0-02, 0-03
- **Acceptance:** README updated, mentions platform not reseller, phases, agent operating system, links, no hype, no secrets, wording "This Pull Request changes documentation and GitHub planning files only" not "This branch contains documentation only", and does not claim any branch exists unless verified via `git ls-remote --heads origin` (e.g., no reference to branches that are not present remotely)
- **Priority:** P0
- **Phase:** phase-0
- **Risk:** Low

### ISSUE-0-13: GitHub Repository Metadata Update (Owner Task)

- **Title:** Update GitHub repository About/Description and topics after brand selection
- **Purpose:** Remove legacy subscription-reseller wording from GitHub About, update description to Persian AI Workspace, update topics
- **Owner Agent Type:** Product Manager + Orchestrator (L1 report, owner executes manually)
- **Dependencies:** Brand selection (UX/Product Design + Brand Visual Identity agents reports)
- **Acceptance Criteria:**
  - [ ] Owner manually updates GitHub repo About/Description: remove "Comprehensive Iranian website for selling foreign subscriptions and AI APIs at discounted prices with AI automation" legacy wording, replace with new platform description: "Persian AI Workspace - phased platform for chat, personas, image studio, video, Telegram business agents, API platform, RAG - built with agent operating system"
  - [ ] Remove legacy topics if any related to reseller, add new topics: persian-ai, ai-workspace, nextjs, fastapi, product-photography, telegram-bot, rag, ai-personas, etc. after brand selection
  - [ ] Do NOT change repository metadata automatically via API without owner approval - this is manual owner task
  - [ ] Document new description and topics in docs/ops/RELEASE_STRATEGY.md or separate docs/website/BRAND_SELECTION.md future
  - [ ] PR that updates README About reference only, not auto metadata change
- **Priority:** P2 (after brand selection)
- **Phase Label:** phase-0
- **Risk Level:** Low (but requires owner approval, no auto without approval)
- **Approval Required:** Yes - owner must approve new description and topics via issue comment before any manual update
- **RollBack:** Revert description to previous via GitHub UI edit
- **Notes:** Do not change repository metadata automatically without owner approval. This is documented owner task, not automated by any agent.
