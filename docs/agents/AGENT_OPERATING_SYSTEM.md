# AGENT OPERATING SYSTEM

**Version:** Phase 0  
**Date:** 2026-07-19

## Purpose
Define how founder uses agents to build and run a Persian AI platform safely, with clear separation between project-building agents (now) and runtime product agents (for customers) and future internal ops agents.

## Three Types of Agents

### 1. Project-Building Agents (Used by Founder to Build Product) - PRIMARY for Phase 0
- **Who they serve:** Founder
- **Examples:** Orchestrator, Product Manager, Fullstack Builder, Website Builder, DevOps, QA/Security, Research, Prompt Engineer, RAG Knowledge, SEO/Content, Growth Marketing, Social Media, Analytics, Customer Success, Sales/Partnership, Compliance/Risk, Finance/Unit Economics, Supplier Scout, App Store/ASO, Execution Coach
- **Current form:** L1/L2 external agents (ChatGPT, Claude, coding agents, research agents) that produce PRs, reports, research docs
- **Future form:** L2→L3 API-connected with approval gates
- **Billing:** Founder pays external tool directly, not via platform wallet
- **Safety:** All publishing, spending, merging, deploying, pricing changes require human approval

### 2. Runtime Product Agents (Used by Customers Inside Platform)
- **Who they serve:** End-users of platform
- **Examples:** General Persian Chat, Prompt Enhancer, Specialist Personas (Career Advisor, SEO Advisor, etc.), Product Photography Studio agent, Video gen agent, Telegram business agent, Developer API agent
- **Current form:** Not built yet, defined in `docs/agents/runtime/`
- **Future form:** L3/L4 internal, API-connected, credit-billed, with guardrails
- **Safety:** Evidence-based framing, risk classification, escalation to human professional, audit logs, wallet credit checks

### 3. Internal Operations Agents (Future, Inside Company/Product)
- **Who they serve:** Internal growth, support, research, SEO, marketing
- **Examples:** SEO technical crawler, content writer (draft only), growth experiment reporter, customer support draft responder, research scouter
- **Current form:** Project-building external agents with human review (L1/L2)
- **Future form:** L3/L4 internal, read-only or draft-only initially, publish requires approval
- **Safety:** Draft → human review → publish. No autonomous bulk messaging or spending.

## Lifecycle
Project-building (Phase 0-2) → Some become Internal Ops L2/L3 (Phase 3-5) → Runtime product agents become L3 with gates → Marketplace (Phase 8) idea with strict review.

## Documentation Map
- Operating System: this file
- Registry: AGENT_REGISTRY.md (all agents list)
- Maturity: AGENT_MATURITY_MODEL.md (L0-L4)
- Permissions: AGENT_PERMISSION_MODEL.md
- Control Tower: AGENT_CONTROL_TOWER.md (observability)
- External Workflow: EXTERNAL_AGENT_WORKFLOW.md
- Approval Gates: HUMAN_APPROVAL_GATES.md

## Key Rules
- No agent can spend money, publish content, contact customers, change pricing/config, merge PRs, deploy prod, create/delete API keys, modify legal/medical/psych personas, launch campaigns, issue refunds above threshold without human approval.
- All actions logged.
- Rollback plan required for state-changing actions.
