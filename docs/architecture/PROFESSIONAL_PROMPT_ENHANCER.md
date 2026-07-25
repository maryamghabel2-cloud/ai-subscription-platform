# Professional Prompt Enhancer

**Version:** v0.1.0

**Date:** 2026-07-24

**Status:** Proposed Architecture - Pending Owner, Privacy, Security, Finance,
and Compliance Approval

**Document Owner:** AI Platform Architect / Product

**Purpose:** Define Professional Prompt Enhancer as Platform-owned Workflow /
Service (not Role, not Specialist Persona, not Agent) with classification,
dedicated profile schema, UX and billing, privacy and logging requirements.

**Note:** Documentation only. No real provider API calls, no secrets.

## Purpose

Establish a prompt enhancer that helps users write better prompts for general
chat, strict factual research, image generation, video generation, advertising
copy, and storytelling, with transparent cost and user control, while preserving
safety and preventing prompt injection bypass.

## In Scope

- Classification as Platform-owned Workflow / Service, not Role, not Persona,
  not Agent
- Dedicated Enhancer Profile schema (not reusing Role registry fields)
- UX and billing rules with Reserve-Settle-Release and cost transparency
- Privacy and logging rules with fingerprint policy and cross-user leakage
  prohibition

## Out of Scope

- Final prompt enhancer implementation and exact prompt templates (future PRs)
- Final pricing for enhancer step (future, CONFIGURED_LIMIT)
- Production enhancer engine code and provider wiring (future PRs)

## Classification

The Prompt Enhancer must be classified explicitly as:

- a Platform-owned Workflow / Service
- not a Role
- not a Specialist Persona
- not an Agent

Update the document to state:

- The Enhancer takes untrusted user content as input (user prompt is untrusted,
  must be treated as untrusted, must not be treated as system instruction)
- The Enhancer outputs a proposed enhanced prompt (enhanced prompt is still
  untrusted user content, not system instruction, not trusted)
- The proposed enhanced prompt is still untrusted user content (must be treated
  as untrusted, must go through Prompt Injection Guard before main provider)
- The Enhancer must not modify system instructions, Role instructions, Persona
  policies, safety policies, or knowledge-base retrieval rules (system
  instructions are in separate immutable never-user-modifiable segment)
- The Enhancer must not execute tools (no tool calls, no browsing, no API calls
  beyond enhancer LLM call, no file processing beyond approved knowledge base)
- The Enhancer must not access provider secrets (no provider API keys in prompts,
  no secrets in logs, no secret in client, secrets come only from approved
  secrets manager)
- The Enhancer must not perform autonomous browsing or retrieval (no web search,
  no file reader beyond approved, no RAG beyond approved, autonomous browsing
  belongs to Agent, not Enhancer)
- The Enhancer must run before the main provider call and must not bypass Prompt
  Injection defenses (must run prompt injection guard before enhancer and after
  enhancer, before main provider)
- The Enhancer output must be re-scanned by the Prompt Injection Guard before
  being sent to the main provider (guard scans for direct injection, indirect
  injection, jailbreak, tool abuse, data exfiltration, system prompt disclosure)

## Profile Structure

Do not reuse Role registry fields for Enhancer profiles.

Introduce a dedicated Enhancer Profile schema:

- **profile_id:** String, e.g., general_chat, strict_factual_research,
  image_generation, video_generation, advertising_copy, storytelling,
  CONFIGURED_VALUE
- **version:** String, semantic version, e.g., v1.0.0
- **display_name_fa:** String, Persian display name, e.g., چت عمومی
- **display_name_en:** String, English display name, e.g., General Chat
- **description:** Text, one sentence purpose, Persian first
- **category:** Enum, chat, research, image, video, advertising, storytelling
- **allowed_input_modalities:** List, e.g., ["text", "image", "file"] or
  ["text"] only, per profile
- **allowed_output_modalities:** List, e.g., ["text"] or ["text", "image_prompt"]
- **allowed_content_categories:** List, e.g., ["general", "advertising",
  "storytelling", "research"] per profile
- **prohibited_content_categories:** List, e.g., ["medical_advice",
  "legal_advice", "disallowed", "non_consensual"] per profile
- **risk_level:** String, low, medium, high, high-risk requires expert and
  Trust and Safety review
- **max_output_length_policy:** CONFIGURED_LIMIT, e.g., max output length for
  enhanced prompt, e.g., CONFIGURED_LIMIT tokens
- **provider_policy:** CONFIGURED_POLICY, e.g., which provider/model to use
  for enhancer, e.g., fast model for enhancer, balanced model
- **pricing_reference:** CONFIGURED_PRICING_POLICY, e.g., reference to Model
  Catalog pricing_version for enhancer cost estimation
- **safety_review_status:** Enum, pending, approved, rejected, with reviewer
  name, credentials, date, expiry
- **enabled:** Boolean, whether profile is enabled

Rules:

- Enhancer profiles must not claim professional authority (must not claim to be
  licensed psychologist, therapist, doctor, lawyer, etc.)
- High-risk profiles (for example medical, legal, mental-health related
  advertising) require expert and Trust and Safety review (expert reviewer
  name, credentials, date, expiry, benchmark)
- Enhancer must not silently rewrite user intent, invent facts, invent citations,
  or introduce claims the user did not make (e.g., must not invent fake URLs,
  fake publisher and date, fake medical claims, fake legal rules, fake prices)
- Enhancer must preserve the user's factual and safety-relevant intent (e.g., if
  user says "I need general information about coping with stress, not therapy",
  enhancer must preserve "general information, not therapy" and must not rewrite
  to "I need therapy")

## UX and Billing

### User Experience Rules

- Off by default for all users, to avoid unexpected cost and to respect user
  autonomy and privacy
- User may enable per-request via toggle or button: "Enhance prompt" or Persian
  "بهبود پرامپت"
- User may enable as a persistent preference in settings: e.g., "Always enhance
  my prompts for image generation" or "Always enhance for research"
- User must be able to preview the enhanced prompt before execution when
  practical (e.g., for image/video generation, show enhanced prompt in UI,
  allow edit)
- User must be able to edit or reject the enhanced prompt (e.g., edit enhanced
  prompt text area, revert to original, or reject and use original)
- User must see an estimated additional cost before enhancement is used (e.g.,
  "Enhancement will cost approximately CONFIGURED_LIMIT credits (estimated).
  Original request will cost approximately CONFIGURED_LIMIT credits. Total
  approximately CONFIGURED_LIMIT credits." – NON_PRODUCTION_MATH_EXAMPLE, actual
  amounts are CONFIGURED_LIMIT placeholders)
- First-use onboarding should explain what prompt enhancer does, its cost,
  how to enable/disable, and that enhanced prompt is still untrusted user content
- User must be able to change preference later in settings page
- Normal Assistant is default mode, not enhanced, to avoid accidental cost and
  accidental high-risk exposure

### Billing Rules

- Enhancer usage is a separate operation type in the ledger (e.g., operation_type
  = prompt_enhancement, is_enhancer = true, enhancer_profile = profile_id)
- Enhancer must go through the Reserve-Settle-Release workflow the same way as
  normal AI usage (future CreditReservation or UsageReservation entity with
  lifecycle quoted, reserved, executing, settled, released, expired, failed)
- Reservation reduces available balance, not posted ledger balance, settlement
  creates exactly one final usage debit in append-only ledger, releasing unused
  hold is not new credit, user must never be debited twice, idempotent
- Enhancer cost must be visible before and after execution (estimated cost
  before, actual cost after settlement, with pricing_version and
  exchange_rate_snapshot)
- Automatic charging is not permitted without an explicit user preference or
  per-request confirmation (off by default, requires per-request toggle or
  persistent preference with explicit consent)
- Enhancer cost estimates must use CONFIGURED_LIMIT placeholders in this
  document (e.g., enhancer cost = CONFIGURED_LIMIT credits, not 2 credits as
  production-approved)
- Any mathematical example must be labeled NON_PRODUCTION_MATH_EXAMPLE (e.g.,
  "Example: original cost CONFIGURED_VALUE credits, enhancer cost
  CONFIGURED_VALUE credits, total CONFIGURED_VALUE credits –
  NON_PRODUCTION_MATH_EXAMPLE, actual amounts are CONFIGURED_LIMIT placeholders")

## Privacy and Logging

- Raw user prompts must not be stored in technical logs (technical Agent audit
  logs must not store raw sensitive prompts, uploaded file contents,
  conversation text, or raw AI responses by default)
- Enhanced prompts must not be stored in technical logs (same rule, no raw
  enhanced prompt in technical logs)
- Enhancer must respect the user's memory settings (e.g., session_only,
  memory_policy per Role, user-controlled retention, non-retention by default
  for sensitive Telegram conversations unless user explicitly enables memory)
- Enhancer must not persist prompts across sessions unless the user has
  explicitly enabled long-term memory for that context (e.g., user preference
  prompt_enhancer_enabled and long-term memory enabled, with consent)
- Enhancer input and output are governed by the same content fingerprint policy
  defined in the Agent security architecture (fingerprints disabled by default,
  keyed HMAC only if separately approved: content_fingerprint
  DISABLED_BY_DEFAULT, fingerprint_method APPROVED_KEYED_HMAC_ONLY_IF_REQUIRED,
  HMAC-SHA-256 with protected, env-specific, versioned, rotatable secret, not
  for analytics/profiling/cross-user comparison)
- Cross-user leakage of prompts is prohibited (user A's original or enhanced
  prompt must never be visible to user B, no cross-user access, tenant isolation
  FK RESTRICT, pseudonymous identifiers in logs, no raw sensitive content)

## Cross-Document Consistency: Credit Lots vs Reservations

Clarification to reconcile with PRICING_AND_UNIT_ECONOMICS.md and
REFERRAL_AND_PROMOTIONAL_CREDITS.md:

- A Credit Lot is a balance-tracking construct: where credits come from and
  their rules, expiry, scope, source, initial_amount, remaining_amount,
  campaign_id, allowed_scope, issued_at, expires_at, non_cashable flag,
  refundable flag, accounting_class. Defined in REFERRAL_AND_PROMOTIONAL_CREDITS.md.

- A Reservation/Settlement is a transaction-tracking construct: how a specific
  operation holds and then consumes credits. Lifecycle quoted, reserved,
  executing, settled, released, expired, failed. Defined in
  PRICING_AND_UNIT_ECONOMICS.md.

- A single operation (including Prompt Enhancer cost) may draw from one or more
  active Credit Lots according to the (still Open Decision) consumption order
  policy, but must always go through the Reservation lifecycle for atomicity.
  Available balance = sum of remaining_amount across active lots.

- These are complementary layers, not competing systems: Credit Lots track
  balance origin and rules; Reservations track transaction holds and consumption.
  Ledger remains single append-only source of truth. Enhancer cost goes through
  same Reserve-Settle-Release workflow as normal AI usage.

- Enhancer billing: Enhancer usage is a separate operation type in the ledger
  (is_enhancer true, enhancer_profile), must go through Reserve-Settle-Release
  with idempotency, available balance check, no double debit, no negative balance.

## Related Documents

- Multi-Provider Routing: [MULTI_PROVIDER_MODEL_ROUTING.md](MULTI_PROVIDER_MODEL_ROUTING.md)
- Pricing and Unit Economics: [PRICING_AND_UNIT_ECONOMICS.md](PRICING_AND_UNIT_ECONOMICS.md)
- Referral and Promotional Credits: [REFERRAL_AND_PROMOTIONAL_CREDITS.md](REFERRAL_AND_PROMOTIONAL_CREDITS.md)
- Security Index: [../security/README.md](../security/README.md)
- Secrets and Key Management: [../security/SECRETS_AND_KEY_MANAGEMENT.md](../security/SECRETS_AND_KEY_MANAGEMENT.md)
- Prompt Injection Defense: [../security/PROMPT_INJECTION_DEFENSE.md](../security/PROMPT_INJECTION_DEFENSE.md)
- Agent Security Model: [../security/AGENT_SECURITY_MODEL.md](../security/AGENT_SECURITY_MODEL.md)
- Accuracy and Creativity: [ACCURACY_CREATIVITY_CONTROL.md](ACCURACY_CREATIVITY_CONTROL.md)
- Role and Persona System: [ROLE_AND_PERSONA_SYSTEM.md](ROLE_AND_PERSONA_SYSTEM.md)
- Agent Plugin and Execution: [AGENT_PLUGIN_AND_EXECUTION_SYSTEM.md](AGENT_PLUGIN_AND_EXECUTION_SYSTEM.md)
- Data Protection: [../security/DATA_PROTECTION_AND_ENCRYPTION.md](../security/DATA_PROTECTION_AND_ENCRYPTION.md)
- Logging and Monitoring: [../security/LOGGING_AND_MONITORING.md](../security/LOGGING_AND_MONITORING.md)

## Open Decisions

- Exact enhancer profile schema and field types and allowed modalities per profile
- System_instructions per profile and version and safety_review_status
- Cost for enhancer step (CONFIGURED_LIMIT placeholder, requires provider cost
  analysis, finance and owner approval)
- Whether to show enhanced prompt before execution always or only when practical
  (e.g., always for image/video, optional for chat)
- Persistent preference storage: user_role_preferences table with
  prompt_enhancer_enabled boolean and enhancer_profile and long-term memory
  consent
- Privacy and logging: content fingerprint policy, cross-user leakage
  prohibition, memory settings
- Owner, product, privacy, security, finance, and compliance approval required

## Planned Completion Stage

Phase 1 - Prompt Enhancer

## Status Note

Proposed Architecture - Pending Owner, Privacy, Security, Finance, and Compliance
Approval. Will be completed later with product, AI, privacy, security, and owner
review. No real provider API calls in this PR.
