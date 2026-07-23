# Role, Persona, Agent, Channel, Studio Boundaries

**Date:** 2026-07-23

**Status:** Proposed Product Architecture — Pending Owner Approval

**Purpose:** Clarify strict separation that was sometimes mixed in Phase 0 docs.

Previously, file `PERSONA_AGENT_ARCHITECTURE.md` mixed Persona and Agent concepts.
This document defines clear boundaries.

## Definitions - Strict Separation

### Role

- **What it is:** Conversation-only behavior.

- **Tools:** No tools - no browsing, no API calls, no file processing,
  no autonomous actions.

- **Defines:** Identity, tone, style, method, language,
  creativity defaults, response mode, model policy,
  memory policy, risk level, disclaimer policy,
  safety profile, evidence policy.

- **Example:** Normal Assistant, Language Tutor, Friendly Companion,
  Writer, Business Assistant, Prompt Engineer.

- **Extensibility:** Adding new Role should not require changing
  core chat logic - registry-based.

- **User customization:** Users can customize Role instructions, tone,
  formal or casual, concise or detailed, language,
  "Speak like me" mirroring, creativity and factuality mode,
  preferred model, output format.

- **Default:** Normal Assistant - not psychologist, not therapist.

- **Storage:** Versioned registry with fields per
  `ROLE_AND_PERSONA_SYSTEM.md`.

### Specialist Persona

- **What it is:** A versioned, evidence-aware, domain-specific Role.

- **Still conversation-only:** No tools that perform external actions
  independently.
  - May use approved knowledge retrieval (RAG) with citations.
  - Does not browse internet.
  - Does not call external APIs autonomously.
  - Does not process files beyond approved knowledge base.
  - Does not run multi-step workflows that affect external world.

- **Knowledge-base architecture:** Roles and Specialist Personas remain
  conversation-only but may receive approved context through separate
  platform-owned retrieval service. Role does not execute retrieval tools
  itself. Platform-owned Retrieval Service queries approved Knowledge Bases,
  returns cited filtered context, context passed to Role. Autonomous browsing
  and multi-step research belongs to Agent.

- **Versioned:** Has version, knowledge-pack version, changelog,
  source hierarchy, evidence grade, publisher, dates,
  geographic scope, last review, expiry, benchmark,
  accuracy and hallucination metrics.

- **Domain-specific:** Career, Sales, SEO, Product Photography Advisor.

- **Evidence-aware:** Based on primary sources, citations required,
  no hallucinated citations, conflicting evidence handling.

- **High-risk Personas require expert review:**
  - Psychologist (evidence-based mental health information assistant,
    not actual psychologist)
  - Immigration Information Assistant
  - Legal Information Assistant
  - Health Information Assistant
  - Must not claim professional authority, must have disclaimers
    and escalation.

- **Example:** Evidence-Based Mental Health Information Assistant
  (future, risk high, structured direct, not generic compassionate
  companion, not therapist, diagnosis, treatment, or emergency service).

- **Registry:** Same registry as Roles but with additional evidence fields,
  risk classification, expert reviewer requirement. Proposed fields include
  knowledge_base_ids, retrieval_policy, allowed_source_types,
  minimum_evidence_policy, knowledge_pack_version, knowledge_pack_reviewed_at,
  knowledge_pack_expires_at, expert_review_required, expert_review_status,
  citation_policy, conflicting_evidence_policy, source_freshness_policy,
  geographic_scope, jurisdiction_scope, care_truthfulness_policy,
  belief_validation_policy, professional_handoff_policy, crisis_response_policy,
  prohibited_authority_claims.

### Agent

- **What it is:** Performs work.

- **May use tools:** May browse, retrieve, call APIs, process files,
  run multi-step workflows.

- **Must have:** Permissions, budgets, safety controls, auditability.

- **Examples:**
  - **Project-building Agents (28):** Orchestrator (L2 docs and planning only,
    does NOT write product code), Fullstack Builder (L2 branch and PR),
    DevOps, etc. - used by founder to build product.
  - **Runtime Agents (future):** Telegram Business Agent, Deep Research Agent,
    Product Photography Studio Workflow (actually Studio Workflow, not simple
    Agent, but similar plugin), Immigration Research Agent.

- **Permissions:** Allow, forbid, approval-required per
  `AGENT_PERMISSION_MODEL.md`, plus absolutely forbidden NO-GO.

- **Maturity:** L0 Manual, L1 report and draft NO branch or PR,
  L2 branch and PR, L3 internal API-connected,
  L4 controlled automation with mandatory gates.

### Channel Adapter

- **What it is:** Website, mobile app, Telegram, or API interface
  that connects users to Roles, Personas, Agents, Studios.

- **Must NOT be classified as a Role or Agent merely because
  it connects users.**

- **Examples:**
  - Website Adapter: Next.js 14 App Router, Tailwind, RTL,
    Persian typography, Header, ChatBox.
  - Mobile App Adapter: Native or PWA, voice input and output,
    camera for product photography, privacy-aware.
  - Telegram Adapter: Telegram Bot API integration,
    encrypted token at rest, webhook, anti-spam.
  - API Adapter: Developer APIs with hashed keys, scopes,
    rate limiting, usage logs.

- **Responsibilities:** Auth (HttpOnly cookies), input handling
  (voice, file, image, PDF attachments), output rendering,
  billing check, audit logging.

- **Not a Role:** Channel Adapter does not define identity, tone,
  method.

### Studio Workflow

- **What it is:** Structured image and video generation workflow.

- **Must NOT be incorrectly classified as a simple Role.**

- **Examples:**
  - Professional Image Studio: Core revenue product.
  - Professional Video Studio: Core revenue product.

- **Workflow steps:**
  - Upload or select
  - Settings (model, style, aspect ratio, etc.)
  - Prompt enhance
  - Generate
  - Review
  - Edit with inpaint, outpaint, upscaling
  - Select and download

- **Tools:** image_generation_api, background removal, upscaling,
  video_generation_api.

- **Cost:** Calculated by pricing engine, not hardcoded.
  Exact limits and prices are Open Decisions and must not be treated
  as production-approved values.

- **Not a Role:** Not conversation-only, performs work via tools,
  has cost, has workflow state machine, core revenue product.

## Deprecating Confusing Terminology

### PERSONA_AGENT_ARCHITECTURE.md

- **File:** `docs/agents/runtime/PERSONA_AGENT_ARCHITECTURE.md`

- **Problem:** Name combines Persona and Agent, implying Specialist Persona
  is an Agent that performs work. But Specialist Persona is defined as
  versioned Role, still conversation-only.

- **Action:** Deprecate this file.
  - Add deprecation note at top with replacement docs.
  - Keep file with deprecation note to avoid breaking existing links silently.
  - Update references in other docs to point to new boundaries doc.

- **Replacement docs:**
  - `ROLE_PERSONA_AGENT_BOUNDARIES.md` (this file)
  - `ROLE_AND_PERSONA_SYSTEM.md`
  - `AGENT_PLUGIN_AND_EXECUTION_SYSTEM.md`
  - `ACCURACY_CREATIVITY_CONTROL.md`
  - `PERSONA_FRAMEWORK.md`

### Other Confusing Terms to Avoid

- **Image Agent** → Use `Image Studio Workflow` or `Image Generation Tool`

- **Product Photography Agent** → Use `Product Photography Studio Workflow`

- **Video Agent** → Use `Video Studio Workflow`

- **Character Agent** → Use `Character Workflow` (part of Video Studio)

- **Persona Agent** → Use `Specialist Persona` (versioned Role) or
  `Persona Runtime` if referring to runtime execution of Persona
  (still conversation-only)

- **Keep as true Agents:**
  - Business Agent (FAQ, lead)
  - Telegram Agent (performs work via Telegram)
  - Research Agent (Deep Research, browses, retrieves)
  - Developer API Agent (X-API-Key auth)
  - Immigration Research Agent (performs multi-step research, not a Persona)

## Mapping Old to New Terminology

| Old (Confusing) | New (Clear) | Type |
|---|---|---|
| Persona Agent | Specialist Persona (versioned Role) | Role |
| Image Agent | Image Studio Workflow | Studio Workflow |
| Product Photography Agent | Product Photography Studio Workflow | Studio Workflow |
| Video Agent | Video Studio Workflow | Studio Workflow |
| Character Agent | Character Workflow | Studio Workflow |
| Telegram Agent (if only connects) | Telegram Channel Adapter + Telegram Business Agent | Channel Adapter + Agent |
| Business Agent (FAQ, lead) | Business Agent (true Agent, performs work) | Agent |
| Research Agent (Deep Research) | Deep Research Agent | Agent |
| Immigration Agent mislabeled as Persona | Immigration Research Agent (Agent) vs Immigration Information Persona (Role) | Agent vs Role |

## Platform-Owned Context Assembly vs Role

Clarify this boundary:

- **Role is conversation-only and does not execute tools.**

- **Specialist Persona is still a Role.**

- **Platform-owned context assembly or retrieval service may retrieve
  approved knowledge.**

- **Retrieved context may then be supplied to the Role.**

- **Role itself does not browse, call APIs, modify data,
  or autonomously execute multi-step workflow.**

- **If autonomous retrieval or multi-step tool use occurs,
  that component is an Agent or platform service,
  not part of the Role definition.**

### Simple Flow - Role with Knowledge Base

```
User Message
→ Channel Adapter (Website, mobile, Telegram, API)
→ Context Assembly Service
→ Approved Specialist Knowledge Base
→ Retrieved Context with Provenance (publisher, date, source ID, evidence grade)
→ Specialist Persona (conversation-only, uses context, citation-aware)
→ AI Provider (via provider abstraction, mapped from Accuracy and Creativity)
→ Response with Citations and Boundaries
```

### Simple Flow - True Agent

```
User Request
→ Channel Adapter
→ Agent Execution Engine (checks permissions, budget, safety, approval)
→ Approved Tools (web_search, file_reader, image_generation_api, etc.)
→ Provider (via provider abstraction)
→ Result with audit metadata (not raw sensitive content by default)
```

## Immigration Persona vs Agent - Separation

- **Immigration Information Persona:**
  - Conversation-only
  - Uses approved official-source Knowledge Base through Retrieval Service
  - Provides general information
  - Does not browse autonomously
  - Does not provide legal advice

- **Immigration Research Agent:**
  - Performs multi-step research
  - May browse approved current official government and embassy sources
  - Produces cited reports
  - Uses budgets, permissions, and audit metadata
  - Must not submit forms, spend money, contact authorities, or guarantee
    outcomes without separately approved future workflows

Do not describe Immigration Research Agent as Specialist Persona.

## Care Without Uncritical Agreement - Reference

For high-risk supportive Personas, care_truthfulness_policy and
belief_validation_policy require:

- Validate user's emotions and lived experience
- Do not automatically validate unsupported factual claims
- Do not agree merely to satisfy or retain user
- Distinguish feelings, interpretations, assumptions, observable facts
- Disclose uncertainty
- Ask calm, non-confrontational reality-checking questions where appropriate
- Do not intensify paranoia, delusional framing, self-destructive beliefs,
  or unsupported accusations
- Do not shame, ridicule, argue aggressively, or dismiss user
- Do not diagnose
- Do not claim system knows another person's intentions
- Maintain empathy while remaining grounded in evidence and uncertainty

Clarify: "Empathy means recognizing the user's feelings. It does not mean
confirming every interpretation or factual belief."

See `ROLE_AND_PERSONA_SYSTEM.md` for full policy and handoff behavior.

## Enforcement

- All new docs must use clear separation.

- No new file should be named `PERSONA_AGENT_ARCHITECTURE`.

- Existing file `PERSONA_AGENT_ARCHITECTURE.md` should have deprecation note
  and link to this boundaries doc.

- README, PRODUCT_VISION, ROADMAP, AGENT_REGISTRY, etc. should be updated
  to use new terminology where possible, but do not break existing links
  silently - add deprecation notes and update references gradually.

## Linkage

- Role and Persona System: [ROLE_AND_PERSONA_SYSTEM](ROLE_AND_PERSONA_SYSTEM.md)

- Agent Plugin and Execution:
  [AGENT_PLUGIN_AND_EXECUTION_SYSTEM](AGENT_PLUGIN_AND_EXECUTION_SYSTEM.md)

- Persona Framework: [PERSONA_FRAMEWORK](../personas/PERSONA_FRAMEWORK.md)

- Agent Operating System:
  [AGENT_OPERATING_SYSTEM](../agents/AGENT_OPERATING_SYSTEM.md)

- Human Approval Gates:
  [HUMAN_APPROVAL_GATES](../agents/HUMAN_APPROVAL_GATES.md)

- Accuracy and Creativity:
  [ACCURACY_CREATIVITY_CONTROL](ACCURACY_CREATIVITY_CONTROL.md)

- Trust and Safety:
  [TRUST_AND_SAFETY_FRAMEWORK](../safety/TRUST_AND_SAFETY_FRAMEWORK.md)

- Future Care: CARE_SAFETY_AND_HUMAN_SUPPORT.md (planned, future - not clickable yet)
