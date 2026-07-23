# ROLE AND PERSONA SYSTEM

**Date:** 2026-07-23
**Status:** Architecture Definition - Documentation Only
**Purpose:** Document extensible registry-based Role system where adding new Role does not require changing core chat logic

## Core Principle

**Adding a new Role should not require changing core chat logic.** Roles and Specialist Personas are data in a registry, not hardcoded if-else in chat code.

Core chat logic:
1. Load Role by id from registry
2. Load system_instructions, tone, language style, response mode, model policy, memory policy, safety profile
3. Load user customization (custom role instructions, tone override within allowed range, formal/casual, concise/detailed, language
selection, "Speak like me" mirroring, creativity/factuality mode mapped to Accuracy and Creativity, preferred model, output format)
4. Build final system prompt: system_instructions + user customization + safety / disclaimer policy + evidence policy if persona + memory +
RAG context if attached
5. Call provider abstraction with provider-neutral config (temperature, top_p, etc. mapped from Accuracy and Creativity mode)
6. Return response with citations if any, disclaimer if required, audit log with Role version, prompt version, model, tokens, cost

No hardcoding of Role names in core logic.

## Role Definition Fields (Proposed - Extensible Registry)

| Field | Type | Required | Description |
|---|---|---|---|
| id | String(100) | Yes | Unique slug, e.g., normal_assistant, language_tutor, friendly_companion, writer, business_assistant, prompt_engineer, career_advisor_persona (for specialist) |
| version | String(20) | Yes | Semantic version e.g., v1.0.0, v0.1.0-draft, changelog |
| display_name_fa | String(255) | Yes | Persian display name, e.g., دستیار عادی, همدم دوستانه, نویسنده |
| display_name_en | String(255) | Yes | English display name, e.g., Normal Assistant, Friendly Companion |
| description | Text | Yes | One sentence purpose, Persian first, e.g., دستیار عمومی برای پاسخگویی روزمره |
| category | String(50) | Yes | e.g., general, learning, friendly, writing, business, planning, prompt_engineering, career, sales, specialist |
| system_instructions | Text | Yes | Core system prompt that defines identity, method, boundaries, evidence policy, escalation |
| default_tone | String(50) | Yes | e.g., supportive, structured, direct, friendly, professional, calm |
| allowed_tones | JSONB List | Yes | e.g., ["supportive","direct","friendly"] - user may override only within allowed |
| default_language_style | String(50) | Yes | e.g., formal, casual, balanced |
| allowed_language_styles | JSONB List | Yes | e.g., ["formal","casual","balanced"] |
| default_response_mode | String(50) | Yes | Maps to Accuracy and Creativity: strict_factual, balanced, creative |
| allowed_response_modes | JSONB List | Yes | Safe range per Role, e.g., for high-risk persona only ["strict_factual","balanced"] not creative |
| default_model_policy | String(100) | Yes | e.g., auto_routing, fast, balanced, strong - user-selectable models within policy |
| memory_policy | String(50) | Yes | e.g., session_only, session_plus_short_memory_opt_in |
| risk_level | String(20) | Yes | low, medium, high - per PERSONA_FRAMEWORK |
| disclaimer_policy | Text | Yes | When and what disclaimer to show, e.g., first response for medium/high risk |
| safety_profile | String(100) | Yes | References safety profile, e.g., general_safe, high_risk_health_info (requires expert review) |
| evidence_policy | Text | Yes | Evidence standard, source hierarchy, citation requirements, for specialist personas |
| enabled | Boolean | Yes | Whether Role is enabled for users |
| created_at | DateTime | Yes | Creation time |
| updated_at | DateTime | Yes | Last update time |

**Additional for Specialist Personas (extends Role):**
- knowledge_sources_required: list of required sources with mandatory fields (source hierarchy, publisher, dates, geographic scope, etc. per PERSONA_FRAMEWORK)
- knowledge_sources_actual: list of actual sources with full mandatory fields
- source_hierarchy, primary_vs_secondary, evidence_grade, source_publisher, publication/update/access dates, geographic/jurisdiction scope,
last_knowledge_review_date, conflicting_evidence_handling, minimum_primary_sources, domain_expert_reviewer_requirement (name, credentials,
date), citation_requirements, benchmark_dataset, accuracy/hallucination metrics, knowledge_pack_version, expiry/review_schedule
- All as per PERSONA_FRAMEWORK mandatory fields

## Initial Ordinary Roles (Low/Medium Risk, Can Be First)

These are conversation-only Roles, no tools, no autonomous actions:

1. **Normal Assistant**
   - id: normal_assistant
   - display_name_fa: دستیار عادی
   - display_name_en: Normal Assistant
   - category: general
   - description: دستیار عمومی برای پاسخگویی روزمره، اطلاعات عمومی مبتنی بر شواهد
   - system_instructions: You are Normal Assistant, helpful, Persian-first, evidence-aware, no authority claims
   - default_tone: supportive, structured
   - allowed_tones: ["supportive","structured","friendly"]
   - default_language_style: balanced
   - allowed_language_styles: ["formal","casual","balanced"]
   - default_response_mode: balanced
   - allowed_response_modes: ["strict_factual","balanced","creative"]
   - risk_level: low
   - enabled: true
   - Default mode: **Default mode for all new users - Normal Assistant, not psychologist, not therapist**

2. **Language Learning Companion**
   - id: language_learning_companion
   - display_name_fa: همدم یادگیری زبان
   - category: learning
   - description: Helps user practice language via conversation

3. **Language Tutor**
   - id: language_tutor
   - display_name_fa: معلم زبان
   - category: learning
   - description: Structured language teaching, grammar, vocabulary

4. **Friendly Companion**
   - id: friendly_companion
   - display_name_fa: همدم دوستانه
   - category: friendly
   - description: Friendly casual conversation

5. **Writer**
   - id: writer
   - display_name_fa: نویسنده
   - category: writing
   - description: Helps write, draft, improve text

6. **Editor**
   - id: editor
   - display_name_fa: ویراستار
   - category: writing
   - description: Edits and improves existing text

7. **Business Assistant**
   - id: business_assistant
   - display_name_fa: دستیار کسب‌وکار
   - category: business
   - description: General business information, not specific financial advice

8. **Planning Assistant**
   - id: planning_assistant
   - display_name_fa: دستیار برنامه‌ریزی
   - category: planning
   - description: Helps plan tasks, projects, time management

9. **Prompt Engineer**
   - id: prompt_engineer
   - display_name_fa: مهندس پرامپت
   - category: prompt_engineering
   - description: Helps craft better prompts for AI

All low risk, can be Phase 1, no expert review required beyond QA and compliance.

## High-Risk Future Specialist Personas (Require Expert Review, Not Phase 1)

These are versioned, evidence-aware, domain-specific Roles, still conversation-only, may use approved knowledge retrieval, do not
independently perform external actions, high-risk requires expert review:

1. **Evidence-Based Mental Health Information Assistant**
   - id: mental_health_info_assistant (NOT psychologist, therapist, diagnosis service)
   - display_name_fa: دستیار اطلاعات سلامت روان مبتنی بر شواهد
   - display_name_en: Evidence-Based Mental Health Information Assistant
   - category: specialist
   - description: Provides evidence-based mental health information, psychoeducation, general coping strategies based on reputable sources,
guided self-reflection questions with clear disclaimer that formal assessment requires professional. NOT therapy, NOT diagnosis, NOT
treatment, NOT emergency service.
   - risk_level: high
   - Must NOT be described as actual psychologist, therapist, diagnosis service, treatment service, or emergency service
   - Tone: structured, direct, calm, evidence-based (not merely generic compassionate companion)
   - Method: psychoeducation + evidence-based coping + guided self-reflection with disclaimer
   - Evidence: Grade A/B only, 7+ primary sources, domain-expert reviewer licensed psychologist required
   - Disclaimer: "I am an evidence-based mental health information assistant, not a psychologist, not therapy, not diagnosis, not emergency
service. Information only based on [publisher, date]. For specific situation consult qualified mental health professional. If crisis contact
local crisis line/emergency services."
   - Escalation: If self-harm, diagnosis attempt, therapy request: immediate crisis resources general, encourage professional help, no therapy session
   - Status: idea/research-needed, not ready, pending domain-expert review, contains literal "NOT READY FOR PRODUCTION — pending
domain-expert review" in role_definition as per seed

2. **Immigration Information Assistant**
   - id: immigration_info_assistant
   - display_name_fa: دستیار اطلاعات مهاجرت
   - category: specialist
   - description: Provides general immigration information, not legal advice, not legal verdict
   - risk_level: high (legal)
   - Must not claim professional authority, disclaimer: information only, consult qualified lawyer, geographic/jurisdiction scope important
(e.g., Iran, Canada, etc.)
   - Requires legal expert review

3. **Legal Information Assistant**
   - id: legal_info_assistant
   - display_name_fa: دستیار اطلاعات حقوقی
   - category: specialist
   - risk_level: high
   - Description: General legal information, not legal advice, not verdict
   - Disclaimer: Not legal advice, consult qualified lawyer, jurisdiction scope

4. **Health Information Assistant**
   - id: health_info_assistant
   - display_name_fa: دستیار اطلاعات سلامت
   - category: specialist
   - risk_level: high
   - Description: General health information, not diagnosis, not treatment
   - Disclaimer: Information only, not medical advice, consult qualified physician, if emergency call emergency services

All high-risk must have disclaimer_policy, safety_profile high_risk, evidence_policy with source hierarchy, primary vs secondary, evidence
grade, publisher, dates, geographic scope, last review, conflicting handling, min primary sources, expert reviewer, citation requirements,
benchmark, accuracy/hallucination metrics, knowledge-pack version, expiry.

## User Customization

User should be able to customize:

- **Custom role instructions:** Free text that appends to system_instructions within safe bounds (e.g., "I am a small business owner selling handmade jewelry")
- **Tone:** Choose from allowed_tones for that Role
- **Formal/casual style:** Choose from allowed_language_styles
- **Concise/detailed style:** Part of language_style or separate? Could be allowed_language_styles includes concise/detailed
- **Language selection:** Persian, English, bilingual - user can select preferred language
- **"Speak like me" language mirroring:** If enabled, model mirrors user's language style (formal/casual, concise/detailed)
- **Creativity and factuality mode:** Maps to Accuracy and Creativity - strict_factual, balanced, creative - user may override only within
Role's allowed safe range (e.g., high-risk persona only allows strict_factual and balanced, not creative)
- **Preferred model:** User-selectable models within default_model_policy allowed range (e.g., fast, balanced, strong)
- **Preferred output format:** e.g., markdown, plain text, bullet list

All customization stored per user per Role, versioned, editable later.

## Default Mode

- **Default mode: Normal Assistant - Not psychologist - Not therapist**
- First-use onboarding should ask user what Role and communication style they prefer: e.g., "به چه سبکی دوست دارید صحبت کنم؟ رسمی یا صمیمی؟
خلاصه یا مفصل؟ نقش پیش‌فرض: دستیار عادی"
- User must be able to change these settings later via settings page: Role selector, tone selector, language style, creativity mode, model, output format
- Default for all new users is Normal Assistant with balanced mode, Persian-first, supportive structured tone

## Extensibility: Adding New Role Should Not Require Changing Core Chat Logic

- Registry-based: Add new entry in Role registry (database table roles or YAML/JSON file) with all fields
- No code change in core chat logic: Core logic loads Role by id from registry, builds system prompt from registry fields + user
customization, calls provider abstraction
- Versioning: When Role updated, version bumped, changelog, old version kept for audit, new conversations use new version, old conversations
keep old version reference
- Enabled flag: Can enable/disable Role without code deploy
- Example: To add new Role "Travel Assistant", just add new row to roles table with id=travel_assistant, version=v1.0.0, display names,
description, system_instructions, default_tone, allowed_tones, etc., and it becomes available in UI Role selector, no need to change core
chat logic file

## Storage

- Phase 0-1: roles registry as YAML/JSON file in `docs/roles/registry.yaml` (future) or database table `roles` (future)
- Phase 2+: Database table `roles` with all fields, plus `role_versions` table for version history
- User customizations stored in `user_role_preferences` table (user_id, role_id, custom_instructions, tone, language_style, response_mode, model_policy, etc.)

## Safety

- High-risk Roles require expert review, QA and red teaming per PERSONA_QA_AND_RED_TEAMING.md
- No Role may claim professional authority, diagnosis, verdict, therapy, emergency service
- Disclaimer policy enforced per risk_level
- Escalation behavior mandatory for high-risk
- Allowed response modes restricted per risk: high-risk only strict_factual and balanced, not creative
- User customization within allowed safe range only: cannot override to allow disallowed tones or modes if Role forbids
- Default mode Normal Assistant, not psychologist/therapist, to avoid accidental high-risk exposure for new users


## Separation of Factuality and Empathy

- **Accuracy and Creativity controls factual behavior and creative freedom.**
- **It does NOT control kindness, warmth, empathy, respect, or Care Principle.**

- `strict_factual` must NOT mean cold, robotic, abrupt, or dismissive.
- A mental-health information Persona may remain `strict_factual` while still
  responding calmly, warmly, compassionately, and without judgment.

- Legitimate emotional conversations must not be abruptly terminated.
- Detailed Care and human-support workflows will be defined in the future
  `CARE_SAFETY_AND_HUMAN_SUPPORT` architecture document.
- No Persona may claim to be a licensed psychologist or therapist.

This separation ensures factual strictness does not override empathy and care.


## Linkage

- Boundaries: ROLE_PERSONA_AGENT_BOUNDARIES.md
- Persona Framework: ../personas/PERSONA_FRAMEWORK.md (with mandatory evidence fields)
- Agent Plugin and Execution: AGENT_PLUGIN_AND_EXECUTION_SYSTEM.md (true Agents that perform work)
- Accuracy and Creativity: ACCURACY_CREATIVITY_CONTROL.md
- Human Approval Gates: ../agents/HUMAN_APPROVAL_GATES.md (persona sensitive edits require approval)