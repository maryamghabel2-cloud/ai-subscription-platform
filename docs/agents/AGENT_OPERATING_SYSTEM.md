# AGENT OPERATING SYSTEM

**Version:** Phase 0  
**Date:** 2026-07-19  
**Updated:** 2026-07-20 - Added 8 new agents, fixed L1/L2 consistency, added absolutely forbidden

## Purpose
Define how founder uses agents to build and run a Persian AI platform safely, with clear separation between project-building agents (now) and runtime product agents (for customers) and future internal ops agents.

## Three Types of Agents

### 1. Project-Building Agents (Used by Founder to Build Product) - PRIMARY for Phase 0
- **Count:** 28 agents (was 20, added 8 new per review) - Authoritative: Total 28 = 19 L1 + 9 L2 per file extraction 2026-07-20 verification


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


- **Who they serve:** Founder
- **Examples:** Orchestrator (L2 docs/planning PRs only), Product Manager (L1 report), Fullstack Builder (L2 code PRs), Website Builder (L2), DevOps (L2), QA/Security (L2), Research (L1 report), Prompt Engineer (L2), RAG Knowledge (L1), SEO/Content (L1 draft), Growth Marketing (L1 report), Social Media (L1 draft), Analytics (L1), Customer Success (L1 draft), Sales/Partnership (L1), Compliance/Risk (L1 report), Finance/Unit Economics (L1), Supplier Scout (L1 report, does NOT automate purchasing), App Store/ASO (L1), Execution Coach (L1), plus new: UX/Product Design (L2), Brand Visual Identity (L1), ML Inference Engineer (L2), Model Evaluation (L1), Trust & Safety (L1), Data Privacy Governance (L1), Localization & Accessibility (L2), SRE/Incident Response (L1)
- **Current form:** Mix L1 (prompt-driven that returns report/draft) and L2 (external that may create scoped branch and PR). Not all are L2 - see registry for exact mapping. Orchestrator is L2 but only documentation/planning PRs, not application-code PRs.
- **Future form:** Some L1/L2 → L3 internal API-connected draft-only with approval gates
- **Billing:** Founder pays external tool directly, not via platform wallet
- **Safety:** All publishing, spending, merging, deploying, pricing changes require human approval. Absolutely forbidden actions (ToS bypass, geographic/sanctions/KYC bypass, fake identities, hiding prohibited locations, credential sharing) have no approval path - NO-GO.

### 2. Runtime Product Agents (Used by Customers Inside Platform)
- **Who they serve:** End-users of platform
- **Examples:** General Persian Chat, Prompt Enhancer, Specialist Personas (Career Advisor, SEO Advisor, etc.), Product Photography Studio agent, Video gen agent, Telegram business agent, Developer API agent
- **Current form:** Not built yet, defined in `docs/agents/runtime/`
- **Future form:** L3/L4 internal, API-connected, credit-billed, with guardrails
- **Safety:** Evidence-based framing, risk classification, escalation to human professional, audit logs, wallet credit checks, no absolute forbidden actions

### 3. Internal Operations Agents (Future, Inside Company/Product)
- **Who they serve:** Internal growth, support, research, SEO, marketing
- **Examples:** SEO technical crawler, content writer (draft only), growth experiment reporter, customer support draft responder, research scouter
- **Current form:** Project-building external agents with human review (L1/L2 mix)
- **Future form:** L3/L4 internal, read-only or draft-only initially, publish requires approval
- **Safety:** Draft → human review → publish. No autonomous bulk messaging or spending. No absolute forbidden.

## Lifecycle
Project-building (Phase 0-2) L1/L2 mix → Some become Internal Ops L3 draft-only (Phase 3-5) → Runtime product agents become L3 with gates → Marketplace (Phase 8) idea with strict review.

## Documentation Map
- Operating System: this file
- Registry: AGENT_REGISTRY.md (28 project-building + 11 runtime + 5 internal)
- Maturity: AGENT_MATURITY_MODEL.md (L0 Manual, L1 Report/Draft, L2 Branch+PR, L3 Internal API-connected, L4 Controlled automation)
- Permissions: AGENT_PERMISSION_MODEL.md (allow/forbid/approval + absolutely forbidden NO-GO)
- Control Tower: AGENT_CONTROL_TOWER.md (observability)
- External Workflow: EXTERNAL_AGENT_WORKFLOW.md
- Approval Gates: HUMAN_APPROVAL_GATES.md (15 approval-required + 9 absolutely forbidden)

## Key Rules
- No agent can spend money, publish content, contact customers, change pricing/config, merge PRs, deploy prod, create/delete API keys, modify legal/medical/psych personas, launch campaigns, issue refunds above threshold without human approval.
- **Absolutely forbidden - No human approval may authorize:** bypassing provider Terms of Service, bypassing geographic restrictions, bypassing sanctions, bypassing KYC, using fake identities, hiding prohibited end-user locations, sharing/reselling unauthorized credentials/raw supplier keys, CSAM, non-consensual intimate imagery, deepfake without consent, claiming professional authority.
- All actions logged, including blocked forbidden attempts.
- Rollback plan required for state-changing actions.
- Orchestrator does NOT write product code - only docs/planning PRs, issue breakdowns, task briefs, agent assignments, dependency maps, weekly reports, blocker reports, PR review summaries. Code implementation by specialist agents (Fullstack, Website, DevOps, etc.).
