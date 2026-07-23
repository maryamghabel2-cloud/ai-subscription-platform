# Agent Plugin and Execution System

**Date:** 2026-07-23

**Status:** Proposed Product Architecture — Pending Owner Approval

**Purpose:** Define how true Agents that perform work are built as plugins
with permissions, budgets, safety controls, and auditability.
Not to be confused with Roles or Specialist Personas which are
conversation-only.

## Definition - Agent vs Role and Persona

- **Role:** Conversation-only behavior, no tools, no autonomous actions.
  Defines identity, tone, style, method, language, and creativity defaults.

- **Specialist Persona:** Versioned, evidence-aware, domain-specific Role.
  Still conversation-only, may use approved knowledge retrieval with citations
  via platform-owned Retrieval Service.
  Does not independently perform external actions.

- **Agent:** Performs work, may use tools, browse, retrieve, call APIs,
  process files, or run multi-step workflows.
  Must have permissions, budgets, safety controls, and auditability.

- **Channel Adapter:** Website, mobile app, Telegram, or API interface.
  Must not be classified as a Role or Agent merely because it connects users.

- **Studio Workflow:** Structured image and video generation workflow.
  Must not be incorrectly classified as a simple Role.
  Core revenue product.

## Agent Plugin System - Extensibility

**Goal:** Adding new Agent should be via plugin registration,
not changing core execution engine.

### Plugin Definition Fields

- `id`: String unique, for example `telegram_business_agent`

- `version`: String semantic version

- `display_name_fa`, `display_name_en`

- `description`

- `category`: business, research, image, video, telegram, etc.

- `type`: `agent` vs `studio_workflow` vs `channel_adapter`

- `permissions`: list of allowed actions

- `forbidden_actions`: list per permission model

- `approval_required_actions`: list per human approval gates

- `tools`: list of tools agent may use

- `budget_policy`: e.g., max credits per execution, max cost per day,
  rate limit
  - Use configurable placeholders, not hardcoded production-approved values
  - See symbolic guidance below

- `safety_profile`: low, medium, high with specific checks

- `risk_level`: low, medium, high

- `enabled`: boolean

- `created_at`, `updated_at`

- `audit_required`: boolean

- `rollback_plan`: text describing how to rollback

**Registry:** Database table `agent_plugins` or YAML file,
similar to Role registry, but for Agents that perform work.

**Core Execution Engine:**

- Loads Agent plugin by id from registry.

- Checks permissions: is action allowed? Is it forbidden?
  Does it require approval? If approval required, creates approval issue
  and waits for human approval, does not execute autonomously.

- Checks budget: does user have enough credits?
  Does agent have budget remaining?

- Checks safety: runs safety checks per safety_profile.

- Executes workflow: may be multi-step.

- Logs audit metadata (not raw sensitive content by default, see privacy
  logging correction below).

- Handles errors and rollback.

- No hardcoding of agent names in core execution logic.

### Configurable Placeholders (Not Production-Approved)

Exact limits and prices are **Open Decisions** and must not be treated as
production-approved values.

- `max_credits_per_execution: CONFIGURED_LIMIT`

- `max_cost_per_day: CONFIGURED_LIMIT`

- `per_user_rate_limit: CONFIGURED_LIMIT`

- `studio_price: CALCULATED_BY_PRICING_ENGINE`

- `rate_limit_messages: CONFIGURED_LIMIT`

State clearly:

> Exact limits and prices are Open Decisions and must not be treated
> as production-approved values.
> They require product, finance, and trust and safety review,
> plus versioned tests.

Do not use hardcoded values such as:

- 100 credits per day per user (unapproved)

- 500 credits per Deep Research execution (unapproved)

- 10 credits per 5 images (unapproved)

- 30 messages per minute (unapproved)

All such numbers must be replaced with `CONFIGURED_LIMIT` or
`CALCULATED_BY_PRICING_ENGINE` and documented as open decisions.

## Tools That Agents May Use

- **Approved Knowledge Retrieval:** RAG attachment, vector store query
  with citations.

- **Web Search and Browse:** For Deep Research Agent and Immigration
  Research Agent (future), must respect robots.txt, no scraping
  violating ToS, only approved official government and embassy sources
  for immigration.

- **File Processing:** Read uploaded files, images, PDFs.

- **API Calls:** Call external AI provider APIs via provider abstraction,
  with cost tracking.

- **Telegram Send:** For Telegram Business Agent, send message via
  Telegram Bot API, but only after human approval for bulk,
  anti-spam, encrypted token.

- **Draft Content Creation:** Create draft blog post, social post,
  support reply in draft state, not publish without approval.

- **Image and Video Generation:** Call image and video model APIs
  via provider abstraction.

All tools must be declared in agent's permissions and tools list.

## Permissions, Budgets, Safety Controls, Auditability

### Permissions per AGENT_PERMISSION_MODEL.md

- **Allowed:** Read docs, read user data (own data only),
  generate draft report, propose prompt improvements,
  analyze data, research browsing, run tests.

- **Forbidden general:** Direct commit to main, force-push,
  delete history, spend money beyond budget,
  publish public content without review,
  contact customers without approval,
  delete production data, create or delete API keys without approval,
  bypass geographic, KYC, or ToS,
  claim medical, legal, or psych authority,
  generate illegal content.

- **Absolutely Forbidden NO-GO:** ToS bypass, geographic, sanctions,
  KYC bypass, fake identities, hiding prohibited locations,
  sharing or reselling unauthorized credentials or raw supplier keys,
  CSAM, non-consensual imagery, deepfake without consent,
  claiming professional authority.
  No human approval may authorize these.

### Budgets - Symbolic Guidance

- Per execution max credits: `max_credits_per_execution: CONFIGURED_LIMIT`

- Per day max cost: `max_cost_per_day: CONFIGURED_LIMIT`

- Per user max spend: `per_user_spend_limit: CONFIGURED_LIMIT`

- Rate limits: `per_user_rate_limit: CONFIGURED_LIMIT`

Checked before execution. Exact values are open decisions, not
production-approved.

### Safety Controls

- NSFW filter for image generation.

- Consent gate for character workflows.
  Real person deepfake requires explicit consent checkbox
  plus human review flag.

- Anti-spam for Telegram:
  - Rate limit: `per_user_rate_limit: CONFIGURED_LIMIT`
  - No bulk broadcast without approval (requires human approval gate).

- Disclaimer for high-risk personas.

- Escalation to professional for crisis, diagnosis, verdict, therapy.

### Audit Logging - Privacy Corrected

**Previous contradiction:** One section said "log inputs and outputs"
and another said "log hashes."

**Corrected policy:**

Technical Agent audit logs must **not** store raw sensitive prompts,
uploaded-file contents, conversation text, or raw AI responses by default.

**Default audit metadata may include:**

- User pseudonymous identifier (not raw email if possible, use hashed
  or internal id)

- Agent id, agent version, execution id

- Tool names used

- Provider id, model id

- Prompt hash (SHA256), response hash (SHA256)

- Token and usage counts

- Estimated and settled cost

- Timestamps (created_at, last_used_at)

- Approval records (who approved, when)

- Result status (success, failure)

- Error category without sensitive content (e.g., "timeout", "rate_limit",
  not raw stack trace with prompt)

- Rollback reference

**Raw content may only be retained in a separate encrypted product-data
store when required for the user-facing feature and according to the
user's retention settings.**

Examples where raw retention may be needed:

- User's conversation history for chat feature (stored in conversations
  and messages tables, not in technical audit logs)

- Generated images/videos for gallery feature

- Uploaded files for study workspace

Even then:

- Store in product-data store, not technical audit logs.

- Encrypt at rest if sensitive.

- Respect user's retention settings (user can delete conversation,
  image, uploaded doc).

- Do not put raw sensitive content in technical logs.

**No raw sensitive content in technical logs by default.**

This resolves previous contradiction.

Stored in append-only audit log table (future) `agent_audit_logs` with
only metadata above, not raw prompts.

## Examples

### Telegram Business Agent (True Agent)

- **id:** `telegram_business_agent`

- **type:** `agent`

- **Permissions:** `read_user_data` (own), `write_draft_content`,
  `call_external_api` (Telegram Bot API), `process_files` (none)

- **Tools:** `telegram_send`, `knowledge_retrieval` (FAQ docs)

- **Budget:** `max_cost_per_day: CONFIGURED_LIMIT`,
  `per_user_rate_limit: CONFIGURED_LIMIT`

- **Safety:** Anti-spam rate limit, no bulk broadcast without approval,
  token encrypted at rest, audit log access, spam detection auto-pause

- **Workflow:** User sends message to Telegram bot → webhook POST
  to `/telegram/webhook/{agent_id}` → check wallet balance →
  run FAQ logic → generate answer → send reply via Telegram API →
  log execution metadata → deduct credits

### Deep Research Agent (True Agent)

- **id:** `deep_research_agent`

- **type:** `agent`

- **Permissions:** `web_search` (approved), `knowledge_retrieval`,
  `call_external_api` (embedding, LLM), `process_files` (upload docs)

- **Tools:** `web_search`, `file_reader`, `embedding`, `LLM`

- **Budget:** `max_credits_per_execution: CONFIGURED_LIMIT`

- **Safety:** Cite sources, evidence grading, no hallucinated citations,
  no disallowed content

- **Workflow:** Receive user query → search and browse →
  retrieve docs → grade evidence → generate answer with citations →
  log audit metadata → deduct credits

### Immigration Research Agent (True Agent - Not Persona)

- **id:** `immigration_research_agent`

- **type:** `agent`

- **Permissions:** `web_search` limited to approved current official
  government and embassy sources, `knowledge_retrieval`,
  `call_external_api`

- **Tools:** `web_search` (official gov/embassy only), `file_reader`,
  `embedding`, `LLM`

- **Budget:** `max_credits_per_execution: CONFIGURED_LIMIT`

- **Safety:** Cite official sources, no hallucinated citations,
  no legal advice, general information only, must not submit forms,
  spend money, contact authorities, or guarantee outcomes without
  separately approved future workflows

- **Workflow:** Receive user query about general immigration info →
  search approved official government and embassy sources →
  retrieve docs → grade evidence → generate cited report with disclaimer
  (not legal advice) → log audit metadata → deduct credits

- **Must NOT be described as Specialist Persona.**
  Persona (conversation-only, uses Knowledge Base via Retrieval Service)
  vs Agent (multi-step research, may browse approved current official sources)

### Product Photography Studio Workflow (Studio Workflow, Not Role)

- **id:** `product_photography_studio`

- **type:** `studio_workflow` (not agent, not role)

- **Workflow:**
  - Upload product photo
  - Choose background, lighting, style
  - Prompt enhance
  - Generate variants
  - Review
  - Edit with inpaint, outpaint, upscaling
  - Select and download

- **Tools:** `image_generation_api`, background removal, upscaling

- **Cost:** `studio_price: CALCULATED_BY_PRICING_ENGINE`

- **Safety:** NSFW filter, trademarked logo handling,
  no copyrighted style imitation without consent

- **Not a Role:** Not conversation-only, performs work via tools,
  has cost, has workflow state machine, core revenue product

## Channel Adapter vs Agent

- **Channel Adapter:** Website, mobile app, Telegram, API.
  - Connects users to Roles, Personas, Agents, Studios.
  - Handles auth (HttpOnly cookies), input (voice, file, image, PDF),
    output rendering, billing check, audit logging.
  - Does NOT define conversation identity, tone, or method itself.

- **Must not be classified as Role or Agent merely because it
  connects users.**
  - Example: Telegram Channel Adapter that receives Telegram updates
    and forwards to Business Agent is adapter,
    while Telegram Business Agent that answers FAQs is true Agent.

## Execution System - Provider-Neutral

- Provider abstraction for chat, image, video, embedding:
  Interface with model name, tokens, cost, latency, error,
  version logging.

- Sampling parameters (temperature, top_p, etc.) mapped from
  Accuracy and Creativity modes via provider-neutral config layer.
  See `ACCURACY_CREATIVITY_CONTROL.md`.

- Different providers use different parameter names.
  Config layer translates normalized modes to provider-specific
  parameters. Exact mappings must be selected per model,
  not merely per provider, and require model evaluation
  and versioned tests.

- Cost tracking per call for unit economics.

## Safety and Approval Gates

- All Agents that perform work must respect `HUMAN_APPROVAL_GATES.md`:
  publishing, spending, contacting customers, bulk messages,
  pricing, config, merge, deploy, API keys, persona sensitive edits,
  campaigns, refunds above threshold require human approval.

- Absolutely forbidden actions have no approval path.

- Audit logs required (metadata only by default, per privacy correction).

- Rollback plan required.

## Linkage

- Boundaries: [ROLE_PERSONA_AGENT_BOUNDARIES](ROLE_PERSONA_AGENT_BOUNDARIES.md)

- Role and Persona System:
  [ROLE_AND_PERSONA_SYSTEM](ROLE_AND_PERSONA_SYSTEM.md)

- Agent Operating System:
  [AGENT_OPERATING_SYSTEM](../agents/AGENT_OPERATING_SYSTEM.md)

- Permission Model:
  [AGENT_PERMISSION_MODEL](../agents/AGENT_PERMISSION_MODEL.md)

- Human Approval Gates:
  [HUMAN_APPROVAL_GATES](../agents/HUMAN_APPROVAL_GATES.md)

- Persona Framework:
  [PERSONA_FRAMEWORK](../personas/PERSONA_FRAMEWORK.md)

- Accuracy and Creativity:
  [ACCURACY_CREATIVITY_CONTROL](ACCURACY_CREATIVITY_CONTROL.md)

- Trust and Safety: [TRUST_AND_SAFETY_FRAMEWORK](../safety/TRUST_AND_SAFETY_FRAMEWORK.md)

- Future Care: CARE_SAFETY_AND_HUMAN_SUPPORT.md (planned, future - not clickable yet)
