# AGENT CONTROL TOWER

**Date:** 2026-07-19
**Purpose:** Observability for all agent activity - project-building and future runtime/internal.

## What Control Tower Does (Phase 0 Doc, Future Build)

Phase 0: Manual checklist + GitHub labels + docs.
Future: Dashboard.

### Registry
- Single source: AGENT_REGISTRY.md
- Each agent has ID, status, maturity (L1 report/draft vs L2 branch+PR mix, not all L2), owner, permissions
- Count updated: 28 project-building agents (was 20) + 11 runtime + 5 internal = 44 total agents tracked - Authoritative: Total 28 project-building = 19 L1 + 9 L2 per file extraction 2026-07-20 verification


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


- New agents: UX/Product Design (L2), Brand Visual Identity (L1), ML Inference Engineer (L2), Model Evaluation (L1), Trust & Safety (L1), Data Privacy Governance (L1), Localization & Accessibility (L2), SRE/Incident Response (L1)

### Logs
- Project-building external agents: Log via PR description + report footer: agent ID, tools used, inputs, outputs, tokens/cost, approval needed, risk flags
- Future internal L3: Store in DB `agent_audit_logs`: agent_id, action, target, payload hash, approver, timestamp, result, rollback id

### Monitoring
- GitHub: Track branch `docs/phase-0-*`, `mvp/*`, label `agent-task`, `needs-human-approval`
- Future: Metrics - agent runs, approval wait time, rejection rate, cost

### Kill Switch
- For L3/L4 future: Ability to disable agent API key, pause schedule, revert last change
- Documented in AGENT_RUNBOOK.md

### Reporting Cadence
- Weekly: Execution Coach + Orchestrator report: what agents did, what's pending approval, blockers
- See REPORTING_CADENCE.md

## Phase 0 Implementation (Now)
- Manual: founder reviews PRs with label `agent-task`
- Use HUMAN_APPROVAL_GATES.md checklist before merge/deploy/publish

## Future Implementation (Not Now)
- Not building control tower UI in Phase 0
- Placeholder for Phase 4+ platform's admin view (no admin dashboard in Phase 1 per scope limits)

## Safety Integration
- All approval-required actions must create GitHub issue with template `agent_task.md` and label `needs-human-approval`
- No auto-merge, no auto-deploy
