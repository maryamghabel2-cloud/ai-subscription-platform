# AGENT SYSTEM ISSUES

**Milestone:** Phase 0 Foundation  
**Updated:** 2026-07-20 - Added 8 new agents, total 28

## ISSUE-AGENT-01: Define Agent OS Docs

- **Title:** Create 7 agent OS docs
- **Purpose:** Safe agent coordination with 3 types, L0-L4, absolutely forbidden NO-GO
- **Owner:** Product Manager
- **Dependencies:** None
- **Acceptance:** 7 docs exist, explain 3 types (project-building 28, runtime 11, internal 5), L0 Manual, L1 Report/Draft, L2 Branch+PR, L3 Internal API-connected, L4 Controlled automation, permission model with allow/forbid/approval + absolutely forbidden section (ToS bypass, geographic/sanctions/KYC bypass, fake identities, hiding locations, credential sharing - no approval may authorize), control tower concept with 44 total agents tracked
- **Priority:** P0
- **Phase:** phase-0
- **Risk:** Medium

## ISSUE-AGENT-02: Project-Building Agent Specs (Now 28)

- **Title:** Create 28 agent specs (was 20, added 8 per review)
- **Purpose:** How to use external agents now with L1/L2 mix, not all L2
- **Owner:** Orchestrator (docs/planning PRs only, not product code)
- **Dependencies:** AGENT-01
- **Acceptance:** 28 files in docs/agents/project/ exist, each has purpose, when to use, phase relevance, inputs, outputs, tools now/later, permissions, forbidden + absolutely forbidden (no approval may authorize ToS, geographic, sanctions, KYC, fake identities, hiding locations, credential sharing), approval-required, success metrics, example prompt, example report format. Counts: L1 report/draft and L2 branch+PR mix per registry, not all L2. New agents: UX Product Design (L2), Brand Visual Identity (L1), ML Inference Engineer (L2), Model Evaluation (L1), Trust & Safety (L1), Data Privacy Governance (L1), Localization & Accessibility (L2), SRE Incident Response (L1)
- **Priority:** P0
- **Phase:** phase-0
- **Risk:** Low

## ISSUE-AGENT-03: Runtime Agent Architectures

- **Title:** Create 5 runtime architecture docs
- **Purpose:** Future user-facing agents with wallet, RAG, safety
- **Owner:** Product Manager + Fullstack Builder
- **Dependencies:** AGENT-01
- **Acceptance:** 5 files exist, explain difference project vs runtime, persona system with mandatory evidence fields, prompt enhancer, memory, wallet, RAG with citations, safety, versioning, audit, Telegram (token encrypted), API (key hashed prefix), no absolute forbidden actions
- **Priority:** P1
- **Phase:** phase-0
- **Risk:** Low

## ISSUE-AGENT-04: Agent Control Tower Spec

- **Title:** Control tower observability doc + runbook + reporting cadence
- **Purpose:** Monitor 44 agents, logs, kill switch
- **Owner:** Orchestrator + DevOps + SRE Incident Response
- **Dependencies:** AGENT-01
- **Acceptance:** Control tower doc explains registry (28+11+5=44), logs (PR description + future agent_audit_logs), monitoring (branches docs/*, mvp/*, labels agent-task/needs-human-approval), kill switch (disable API key, pause schedule, revert), reporting cadence weekly, absolutely forbidden monitoring
- **Priority:** P1
- **Phase:** phase-0
- **Risk:** Low

## ISSUE-AGENT-05: Human Approval Gates Implementation Plan

- **Title:** Approval gates doc + GitHub label workflow + absolutely forbidden NO-GO section
- **Purpose:** Prevent unsafe autonomy, define NO-GO
- **Owner:** Compliance Risk + Trust & Safety
- **Dependencies:** AGENT-01
- **Acceptance:** HUMAN_APPROVAL_GATES has 14 approval-required actions (publishing, spending, contacting, bulk, pricing, config, merge, deploy, API keys, persona sensitive edits, campaigns, refunds above threshold, new agent/maturity escalation, deleting data) AND separate ABSOLUTELY FORBIDDEN / NO-GO section with 9 items (ToS bypass, geographic, sanctions, KYC, fake identities, hiding prohibited locations, credential sharing/reselling, CSAM/non-consensual/deepfake without consent, claiming professional authority) with statement "No human approval may authorize these actions". Manual GitHub approval via comment, no auto-merge, future UI concept, enforcement via QA Security and Compliance review, logging of blocked attempts
- **Priority:** P0
- **Phase:** phase-0
- **Risk:** High

## ISSUE-AGENT-06: New 8 Agents - Governance & Evaluation

- **Title:** Create 8 new agent specs per review: UX Product Design, Brand Visual Identity, ML Inference Engineer, Model Evaluation, Trust & Safety, Data Privacy Governance, Localization & Accessibility, SRE Incident Response
- **Purpose:** Cover missing disciplines for Persian-first, safe, evaluable platform
- **Owner:** Orchestrator + Product Manager
- **Dependencies:** AGENT-02
- **Acceptance:** 8 new files exist in docs/agents/project/ with same structure (purpose, when to use, phase relevance, inputs, outputs, tools now/later, permissions, forbidden + absolutely forbidden, approval-required, metrics, example prompt/report), added to AGENT_REGISTRY.md (now 28), AGENT_OPERATING_SYSTEM.md, AGENT_CONTROL_TOWER.md, relevant roadmap phases (Phase 0 Foundation includes UX, Brand, Trust Safety, Data Privacy, Model Eval, Localization; Phase 1 includes UX, Brand, Trust Safety, Data Privacy, Localization, SRE; etc.), backlog, README agent summary
- **Priority:** P0
- **Phase:** phase-0
- **Risk:** Medium

## ISSUE-AGENT-07: Governance Documents - Architecture, Evaluation, Safety, Research

- **Title:** Create 7 governance docs: SYSTEM_CONTEXT, PROVIDER_ABSTRACTION_STRATEGY, DATA_CLASSIFICATION_AND_RETENTION, MODEL_EVALUATION_STRATEGY, PERSONA_EVALUATION_STRATEGY, TRUST_AND_SAFETY_FRAMEWORK, SOURCE_QUALITY_POLICY
- **Purpose:** Phase 0 governance planning docs only, no code
- **Owner:** Research + Compliance Risk + Trust & Safety + Data Privacy Governance + ML Inference + Model Evaluation + Architect (Orchestrator)
- **Dependencies:** Product vision, Agent OS, Persona Framework
- **Acceptance:** 7 files exist in docs/architecture/, docs/evaluation/, docs/safety/, docs/research/ with planning content, no secrets, no production code, link to relevant docs, mention absolutely forbidden actions have no approval path
- **Priority:** P0
- **Phase:** phase-0
- **Risk:** Medium
