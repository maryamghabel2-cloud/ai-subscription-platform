# AGENT PLUGIN AND EXECUTION SYSTEM

**Date:** 2026-07-23
**Status:** Architecture Definition - Documentation Only
**Purpose:** Define how true Agents (that perform work) are built as plugins with permissions, budgets, safety controls, auditability, not confused with Roles/Personas which are conversation-only

## Definition - Agent vs Role/Persona

- **Role:** Conversation-only behavior, no tools, no autonomous actions, defines identity, tone, style, method, language, creativity defaults
- **Specialist Persona:** Versioned, evidence-aware, domain-specific Role, still conversation-only, may use approved knowledge retrieval with citations, does not independently perform external actions
- **Agent:** Performs work, may use tools, may browse, retrieve, call APIs, process files, run multi-step workflows, must have permissions, budgets, safety controls, auditability
- **Channel Adapter:** Website, mobile, Telegram, API interface, must not be classified as Role or Agent merely because it connects users
- **Studio Workflow:** Structured image/video generation workflow, must not be incorrectly classified as simple Role, core revenue product

## Agent Plugin System - Extensibility

**Goal:** Adding new Agent (that performs work) should be via plugin registration, not changing core execution engine.

**Plugin Definition Fields:**

- id: String unique, e.g., telegram_business_agent, deep_research_agent, product_photography_studio_workflow (though studio is workflow, not agent, but similar plugin)
- version: String semantic version
- display_name_fa, display_name_en
- description
- category: business, research, image, video, telegram, etc.
- type: agent vs studio_workflow vs channel_adapter (to avoid confusion)
- permissions: list of allowed actions (e.g., read_user_data, write_draft_content, call_external_api, process_files)
- forbidden_actions: list (e.g., spend_money, publish_public_content, contact_customers without approval - per permission model)
- approval_required_actions: list (publishing, spending, contacting, pricing, config, etc. per HUMAN_APPROVAL_GATES)
- tools: list of tools agent may use (e.g., web_search, file_reader, image_generation_api, video_generation_api, telegram_send, email_draft)
- budget_policy: e.g., max credits per execution, max cost per day, rate limit
- safety_profile: e.g., low, medium, high, with specific checks (NSFW filter for image, consent gate for character, anti-spam for Telegram)
- risk_level: low, medium, high
- enabled: boolean
- created_at, updated_at
- audit_required: boolean (all agents should have audit)
- rollback_plan: text describing how to rollback

**Registry:** Database table `agent_plugins` or YAML file, similar to Role registry, but for Agents that perform work.

**Core Execution Engine:**

- Loads Agent plugin by id from registry
- Checks permissions: is action allowed? Is it forbidden? Does it require approval? If approval required, creates approval issue and waits for human approval, does not execute autonomously.
- Checks budget: does user have enough credits? Does agent have budget remaining?
- Checks safety: runs safety checks per safety_profile (e.g., NSFW filter for image prompt, consent checkbox for character)
- Executes workflow: may be multi-step, e.g., Research Agent: 1. receive user query, 2. browse/search, 3. retrieve docs, 4. grade evidence, 5. generate answer with citations, 6. log audit, 7. deduct credits, 8. return response
- Logs audit: who triggered, what agent, what tools used, inputs, outputs, tokens, cost, timestamp, result, rollback reference
- Handles errors and rollback

No hardcoding of agent names in core execution logic.

## Tools That Agents May Use

- **Approved Knowledge Retrieval:** RAG attachment, vector store query with citations (for specialist personas and research agents)
- **Web Search/Browse:** For Deep Research Agent (future), must respect robots.txt, no scraping violating ToS
- **File Processing:** Read uploaded files, images, PDFs (for product photography studio, study workspace)
- **API Calls:** Call external AI provider APIs via provider abstraction (chat, image, video, embedding), with cost tracking
- **Telegram Send:** For Telegram Business Agent, send message via Telegram Bot API, but only after human approval for bulk, anti-spam, encrypted token
- **Draft Content Creation:** Create draft blog post, social post, support reply in draft state, not publish without approval
- **Image/Video Generation:** Call image/video model APIs via provider abstraction

All tools must be declared in agent's permissions and tools list.

## Permissions, Budgets, Safety Controls, Auditability

**Permissions per AGENT_PERMISSION_MODEL.md and AGENT_OPERATING_SYSTEM.md:**

- **Allowed:** Read docs, read user data (own data only), generate draft report, propose prompt improvements, analyze data, research browsing, run tests
- **Forbidden general:** Direct commit to main, force-push, delete history, spend money beyond budget, publish public content without review, contact customers without approval, delete production data, create/delete API keys without approval, bypass geographic/KYC/ToS, claim medical/legal/psych authority, generate NSFW/violent/illegal content
- **Absolutely Forbidden NO-GO:** ToS bypass, geographic/sanctions/KYC bypass, fake identities, hiding prohibited locations, sharing/reselling unauthorized credentials/raw supplier keys, CSAM, non-consensual imagery, deepfake without consent, claiming professional authority - no human approval may authorize

**Budgets:**
- Per execution max credits, per day max cost, per user max spend
- Checked before execution

**Safety Controls:**
- NSFW filter for image generation
- Consent gate for character workflows (real person deepfake requires explicit consent checkbox + human review flag)
- Anti-spam for Telegram (rate limit 30 msg/min, no bulk broadcast without approval)
- Disclaimer for high-risk personas
- Escalation to professional for crisis/diagnosis/verdict/therapy

**Auditability:**
- Who triggered (user_id, agent_id), what action, what tools used, inputs (prompt hash), outputs (response hash), tokens, cost, timestamp, result (success/failure), rollback reference
- Stored in append-only audit log table (future) `agent_audit_logs`

## Examples

### Telegram Business Agent (True Agent that performs work)

- **id:** telegram_business_agent
- **type:** agent
- **Permissions:** read_user_data (own), write_draft_content, call_external_api (Telegram Bot API), process_files (none)
- **Tools:** telegram_send (draft? Actually send is action, but for FAQ bot, send is allowed after check), knowledge_retrieval (FAQ docs)
- **Budget:** max 100 credits per day per user
- **Safety:** Anti-spam rate limit 30/min, no bulk broadcast without approval (requires human approval gate), token encrypted at rest, audit log access, spam detection auto-pause
- **Workflow:** User sends message to Telegram bot → webhook POST to /telegram/webhook/{agent_id} → check wallet balance → run FAQ logic (retrieve from knowledge base) → generate answer → send reply via Telegram API → log execution → deduct credits

### Deep Research Agent (True Agent)

- **id:** deep_research_agent
- **type:** agent
- **Permissions:** web_search (approved), knowledge_retrieval, call_external_api (embedding, LLM), process_files (upload docs)
- **Tools:** web_search, file_reader, embedding, LLM
- **Budget:** max 500 credits per research task
- **Safety:** Cite sources, evidence grading, no hallucinated citations, no disallowed content
- **Workflow:** Receive user query → search/browse → retrieve docs → grade evidence → generate answer with citations → log audit → deduct credits

### Product Photography Studio Workflow (Studio Workflow, not simple Role)

- **id:** product_photography_studio
- **type:** studio_workflow (not agent, not role)
- **Workflow:** Upload product photo → choose background, lighting, style → prompt enhance → generate 5 variants → review → edit (inpaint/outpaint/upscale) → select → download
- **Tools:** image_generation_api, background removal, upscaling
- **Cost:** Credit cost per image (e.g., 10 credits per 5 images)
- **Safety:** NSFW filter, trademarked logo handling, no copyrighted style imitation without consent
- **Not a Role:** Not conversation-only, performs work via tools, has cost, has workflow state machine, core revenue product

## Channel Adapter vs Agent

- **Channel Adapter** (Website, mobile, Telegram, API) connects users to Roles/Personas/Agents/Studios, handles auth (HttpOnly cookies), input (voice, file, image, PDF), output rendering, billing check, audit logging, but does NOT define conversation identity/tone/method itself.
- **Must not be classified as Role or Agent merely because it connects users.** Example: Telegram Channel Adapter that receives Telegram updates and forwards to Business Agent is adapter, while Telegram Business Agent that answers FAQs is true Agent.

## Execution System - Provider-Neutral

- Provider abstraction for chat, image, video, embedding: interface with model name, tokens, cost, latency, error, version logging
- Sampling parameters (temperature, top_p, etc.) mapped from Accuracy and Creativity modes via provider-neutral config layer (see ACCURACY_CREATIVITY_CONTROL.md)
- Different providers use different parameter names (e.g., OpenAI temperature, Anthropic top_p, etc.), so config layer translates normalized modes to provider-specific parameters
- Cost tracking per call for unit economics

## Safety and Approval Gates

- All Agents that perform work must respect HUMAN_APPROVAL_GATES.md: publishing, spending, contacting customers, bulk messages, pricing, config, merge, deploy, API keys, persona sensitive edits, campaigns, refunds above threshold require human approval
- Absolutely forbidden actions have no approval path
- Audit logs required
- Rollback plan required

## Linkage

- Boundaries: ROLE_PERSONA_AGENT_BOUNDARIES.md
- Role and Persona System: ROLE_AND_PERSONA_SYSTEM.md
- Agent Operating System: ../agents/AGENT_OPERATING_SYSTEM.md (28 project-building agents)
- Permission Model: ../agents/AGENT_PERMISSION_MODEL.md
- Human Approval Gates: ../agents/HUMAN_APPROVAL_GATES.md
- Persona Framework: ../personas/PERSONA_FRAMEWORK.md
- Accuracy and Creativity: ACCURACY_CREATIVITY_CONTROL.md
