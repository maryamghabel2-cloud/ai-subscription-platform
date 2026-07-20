# AGENT MATURITY MODEL

**Date:** 2026-07-19  
**Updated:** 2026-07-20 - Aligned definitions per review

## Levels - Official Definitions (Use These Everywhere)

### L0 Manual
- Human does task, no agent.
- Use when: discovery, judgment, compliance decision, founder vision.
- Example: Founder writes PRODUCT_VISION.md manually.

### L1 Prompt-Driven External Agent That Returns a Report or Draft
- Founder uses external chat agent (ChatGPT, Claude) with prompt, gets advice/text/markdown report or draft file content, manually copies or pastes into branch.
- **Does NOT create branch or PR itself.** Returns report/draft for human to place.
- No tool access to GitHub write, no autonomous file write.
- Use: Research question, prompt draft, idea, analytics report draft, compliance checklist draft, finance model draft, supplier scout list draft.
- Approval: Human reviews output before using.
- Example: Research Agent returns `docs/research/video_models_2026.md` content as markdown in chat, founder creates file and PR.
- Count: Many project-building agents are L1 (see registry).

### L2 External Agent That May Create a Scoped Branch and Pull Request
- External coding or content agent (e.g., Cursor, Claude Code, coding model) that has ability to create a scoped feature branch (`feat/`, `docs/`, `fix/`) and open a Pull Request draft with files changed.
- Tools: GitHub read + write branch + open PR draft, local file system in branch, research browsing, but **not** connected to production, not spending money, not publishing to live site.
- Also may return report if simpler.
- Human approval: Required for merge, deploy, publish, spend, pricing/config changes, etc. (see HUMAN_APPROVAL_GATES).
- Example: Fullstack Builder Agent creates branch `feat/auth`, adds `backend/app/api/auth.py`, opens PR #x with description including tools used, cost, approval needed, risks, rollback.
- Count: Some project-building agents are L2 (fullstack, website, devops, QA/Security, prompt engineer, etc.) - not all 20.
- **Important:** Orchestrator is L2 but **only for documentation/planning PRs**, not application-code PRs (see ORCHESTRATOR_AGENT.md).

### L3 Internal API-Connected Agent
- Future (Phase 3+).
- Agent has API key with limited scope (read-only or draft-create) to internal system (e.g., SEO crawler that reads site, creates draft blog post in draft state in CMS or branch).
- Permissions: Allowed read, allowed draft-create, forbidden publish/delete/spend/contact.
- Human approval: Required to publish draft, to escalate permissions, to increase scope.
- Audit logs + rollback required + kill switch.
- Example: SEO Content Agent L3 draft-only: runs nightly, reads new persona pages, creates draft blog post in `content/drafts/`, not live, founder approves to publish.

### L4 Controlled Automation With Mandatory Human Approval Gates
- Future idea, not in Phase 0.
- Agent runs on schedule (e.g., daily growth report), has narrow scope, e.g., generate experiment report and post to Slack draft channel.
- **Never** autonomous for absolute forbidden actions (ToS bypass, geographic/sanctions/KYC bypass, fake identities, hiding locations, credential sharing) and never autonomous for approval-required actions (spending, publishing public content, contacting customers, bulk messages, changing prices/config, merging PRs, deploying to production, creating/deleting API keys, modifying legal/medical/psych personas, launching paid campaigns, issuing refunds/credits above threshold, creating new agent type or escalating maturity).
- Requires: approval gate UI, audit log, kill switch, rollback plan, rate limits, compliance review.

## Registry Consistency Rule

- Not all 20 (now 28) project-building agents are L2. Some are L1 (report/draft only), some are L2 (branch+PR).
- See AGENT_REGISTRY.md for current maturity per agent.
- All agent spec files must list **Maturity Now** matching registry.
- README summary must not claim all project-building agents are L2 - must say mix L1/L2.

## Maturity Progression

- Phase 0: Project-building agents start L1/L2.
- Phase 1-2: Some L1 may stay L1 (e.g., analytics report), some L2 may stay L2. Some may become L3 draft-only later (e.g., SEO Content → draft blog, Analytics → read-only dashboard).
- Runtime product agents: Start as L2/L3 when built, but with human approval for persona modifications and all approval gates.
- Internal ops agents: Start as L1/L2 external draft-only, future L3.

## Checklist to Move L1→L2 or L2→L3

- Permissions defined in AGENT_PERMISSION_MODEL.md
- Approval gates implemented per HUMAN_APPROVAL_GATES.md
- Absolutely forbidden actions checked - no approval may authorize them
- Audit logging implemented
- Rollback documented
- Human approval UI exists for L3+
- Risk review by Compliance/Risk agent + founder
- Tests for forbidden actions blocking (QA Security)
- For persona-related: QA and red teaming passed

## How to Count

- Project-building: Now 28 after adding 8 new - Authoritative: Total 28 = 19 L1 (report/draft) + 9 L2 (branch+PR) - Total 28 = 19 L1 + 9 L2 per file extraction 8 new (UX Product Design, Brand Visual Identity, ML Inference Engineer, Model Evaluation, Trust Safety, Data Privacy Governance, Localization Accessibility, SRE Incident Response)
- L1 vs L2 breakdown must be explicit in registry.

## Documentation Links Must Use This Rule

- README.md, AGENT_REGISTRY.md, AGENT_MATURITY_MODEL.md, and all agent specs in docs/agents/project/ must be consistent with above L1-L4 definitions.



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


