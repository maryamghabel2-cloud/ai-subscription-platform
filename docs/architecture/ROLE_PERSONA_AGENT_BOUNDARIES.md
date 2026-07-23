# ROLE / PERSONA / AGENT / CHANNEL / STUDIO BOUNDARIES

**Date:** 2026-07-23
**Status:** Architecture Definition - Documentation Only
**Purpose:** Clarify strict separation that was sometimes mixed in Phase 0 docs (e.g., PERSONA_AGENT_ARCHITECTURE confusing terminology)

## Definitions - Strict Separation

### Role
- **What it is:** Conversation-only behavior
- **Tools:** No tools - no browsing, no API calls, no file processing, no autonomous actions
- **Defines:** Identity, tone, style, method, language, creativity defaults, response mode, model policy, memory policy, risk level, disclaimer policy, safety profile, evidence policy
- **Example:** Normal Assistant, Language Tutor, Friendly Companion, Writer, Business Assistant, Prompt Engineer
- **Extensibility:** Adding new Role should not require changing core chat logic - registry-based
- **User customization:** Users can customize Role instructions, tone, formal/casual, concise/detailed, language, "Speak like me" mirroring, creativity/factuality mode, preferred model, output format
- **Default:** Normal Assistant - not psychologist, not therapist
- **Storage:** Versioned registry with fields per ROLE_AND_PERSONA_SYSTEM.md

### Specialist Persona
- **What it is:** A versioned, evidence-aware, domain-specific Role
- **Still conversation-only:** No tools that perform external actions independently, may use approved knowledge retrieval (RAG) with citations, does not browse internet, does not call external APIs autonomously, does not process files beyond approved knowledge base, does not run multi-step workflows that affect external world
- **Versioned:** Has version, knowledge-pack version, changelog, source hierarchy, evidence grade, publisher, dates, geographic scope, last review, expiry, benchmark, accuracy/hallucination metrics
- **Domain-specific:** Career, Sales, SEO, Product Photography Advisor, etc.
- **Evidence-aware:** Based on primary sources, citations required, no hallucinated citations, conflicting evidence handling
- **High-risk Personas require expert review:** Psychologist (evidence-based mental health information assistant, not actual psychologist), Immigration Information Assistant, Legal Information Assistant, Health Information Assistant - must not claim professional authority, must have disclaimers and escalation
- **Example:** Evidence-Based Mental Health Information Assistant (future, risk high, structured direct, not generic compassionate companion, not therapist/diagnosis/treatment/emergency service)
- **Registry:** Same registry as Roles but with additional evidence fields, risk classification, expert reviewer requirement

### Agent
- **What it is:** Performs work - may use tools, may browse, retrieve, call APIs, process files, run multi-step workflows
- **Must have:** Permissions, budgets, safety controls, auditability, approval gates
- **Examples:**
  - **Project-building Agents** (28): Orchestrator (L2 docs/planning only, does NOT write product code), Fullstack Builder (L2 branch+PR), DevOps, etc. - used by founder to build product
  - **Runtime Product Agents** (future, 11): These are actually better called Tools or Workflows? For clarity, runtime "agents" that perform work for customers should be called Tools, Studio Workflows, or Business Agents, not confused with conversation-only Roles/Personas. Examples needing rename: Image Generation Studio Workflow (not "Image Agent"), Product Photography Studio Workflow (not "Product Photography Agent"), Video Generation Studio Workflow, Telegram Business Agent (performs work via Telegram, uses tools, so true Agent), Research Agent (Deep Research Agent that browses and retrieves)
- **Permissions:** Allow/forbid/approval-required per AGENT_PERMISSION_MODEL.md, plus absolutely forbidden NO-GO (ToS bypass, geographic/sanctions/KYC bypass, fake identities, hiding locations, credential sharing)
- **Maturity:** L0 Manual, L1 report/draft NO branch/PR, L2 branch+PR, L3 internal API-connected, L4 controlled automation with mandatory gates

### Channel Adapter
- **What it is:** Website, mobile app, Telegram, or API interface that connects users to Roles/Personas/Agents/Studios
- **Must NOT be classified as a Role or Agent merely because it connects users**
- **Examples:**
  - Website Adapter: Next.js 14 App Router, Tailwind, RTL, Persian typography, Header, ChatBox
  - Mobile App Adapter: Native or PWA, voice input/output, camera for product photography, privacy-aware
  - Telegram Adapter: Telegram Bot API integration, encrypted token at rest, webhook, anti-spam, no bulk without approval
  - API Adapter: Developer APIs with hashed keys, scopes, rate limiting, usage logs
- **Responsibilities:** Auth (HttpOnly cookies), input handling (voice, file, image, PDF attachments), output rendering, billing check, audit logging, but not conversation logic itself
- **Not a Role:** Channel Adapter does not define identity/tone/method

### Studio Workflow
- **What it is:** Structured image/video generation workflow with steps: upload/select, settings (model, style, aspect ratio, etc.), prompt enhance, generate, review, edit (inpaint/outpaint/upscale), select, download
- **Must NOT be incorrectly classified as a simple Role**
- **Examples:**
  - Professional Image Studio: Core revenue product, not minor side feature, supports product photography, advertising campaigns, posters, banners, social media assets, website assets, artistic images, brand concepts, background replacement, image editing, inpainting/outpainting, upscaling
  - Professional Video Studio: Core revenue product, text-to-video, image-to-video, product advertisements, brand videos, educational videos, storyboards, character workflows, voice-over and subtitles
- **Components:** UI for upload, settings, gallery, prompt enhancer, model routing, cost calculation, credit deduction, storage (S3 compatible), audit logs
- **Difference from Role:** Role is conversation-only, Studio performs work (image/video generation) via tools/APIs, has cost, has workflow state machine
- **Revenue:** Core revenue products, not side features

## Deprecating Confusing Terminology

### PERSONA_AGENT_ARCHITECTURE.md
- **File:** `docs/agents/runtime/PERSONA_AGENT_ARCHITECTURE.md`
- **Problem:** Name combines Persona and Agent, implying Specialist Persona is an Agent that performs work, but Specialist Persona is defined as conversation-only versioned Role, not Agent that performs external actions. This mixes concepts.
- **Action:** Deprecate this file. Add deprecation note at top: "DEPRECATED - See docs/architecture/ROLE_PERSONA_AGENT_BOUNDARIES.md and ROLE_AND_PERSONA_SYSTEM.md and PERSONA_FRAMEWORK.md. Specialist Persona is a versioned Role, still conversation-only, may use approved knowledge retrieval, does not independently perform external actions. For Agents that perform work, see AGENT_PLUGIN_AND_EXECUTION_SYSTEM.md and runtime Business Agent, Telegram Agent, Research Agent architectures."
- **Replacement:** Use ROLE_AND_PERSONA_SYSTEM.md for Persona definition, and AGENT_PLUGIN_AND_EXECUTION_SYSTEM.md for true Agents, and STUDIO workflow docs for Image/Video Studios.
- **Link preservation:** Do not break existing links silently. Keep file with deprecation note and link to replacement docs, update references in other docs to point to new boundaries doc.

### Other Confusing Terms to Avoid
- "Image Agent" → Use "Image Studio Workflow" or "Image Generation Tool"
- "Product Photography Agent" → Use "Product Photography Studio Workflow"
- "Video Agent" → Use "Video Studio Workflow"
- "Persona Agent" → Use "Specialist Persona" (which is a Role, not Agent) or "Persona Runtime" if referring to runtime execution of Persona (still conversation-only)
- Keep "Business Agent" and "Telegram Agent" and "Research Agent" and "Developer API Agent" as true Agents that perform work (they use tools, browse, retrieve, call APIs, process files, run multi-step workflows)

## Mapping Old → New Terminology

| Old (Confusing) | New (Clear) | Type |
|---|---|---|
| Persona Agent | Specialist Persona (versioned Role) | Role |
| Image Agent | Image Studio Workflow | Studio Workflow |
| Product Photography Agent | Product Photography Studio Workflow | Studio Workflow |
| Video Agent | Video Studio Workflow | Studio Workflow |
| Character Agent | Character Workflow (part of Video Studio) | Studio Workflow |
| Telegram Agent (if only connects) | Telegram Channel Adapter + Telegram Business Agent (performs work) | Channel Adapter + Agent |
| Business Agent (FAQ, lead) | Business Agent (true Agent, performs work) | Agent |
| Research Agent (Deep Research) | Deep Research Agent (true Agent, browses, retrieves, evidence grading) | Agent |
| Developer API Agent | API Channel Adapter + Developer Tools | Channel Adapter |

## Enforcement

- All new docs must use clear separation: Role (conversation-only, no tools), Specialist Persona (versioned Role, still conversation-only, evidence-aware), Agent (performs work, tools, permissions, budgets, safety, audit), Channel Adapter (Website, mobile, Telegram, API), Studio Workflow (structured image/video generation, core revenue)
- No new file should be named PERSONA_AGENT_ARCHITECTURE
- Existing file PERSONA_AGENT_ARCHITECTURE.md should have deprecation note and link to this boundaries doc
- README, PRODUCT_VISION, ROADMAP, AGENT_REGISTRY, etc. should be updated to use new terminology where possible, but do not break existing links silently - add deprecation notes and update references gradually

## Linkage

- Role and Persona System: ROLE_AND_PERSONA_SYSTEM.md
- Agent Plugin and Execution: AGENT_PLUGIN_AND_EXECUTION_SYSTEM.md
- Persona Framework: ../personas/PERSONA_FRAMEWORK.md
- Agent Operating System: ../agents/AGENT_OPERATING_SYSTEM.md
- Human Approval Gates: ../agents/HUMAN_APPROVAL_GATES.md
