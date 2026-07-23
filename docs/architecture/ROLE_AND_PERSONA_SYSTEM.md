# Role and Persona System

**Date:** 2026-07-23

**Status:** Proposed Product Architecture — Pending Owner Approval

**Decision Owner:** Founder (pending Project Manager review)

**Purpose:** Document extensible registry-based Role system where
adding new Role does not require changing core chat logic.

## Core Principle

Adding a new Role should not require changing core chat logic.

Roles and Specialist Personas are data in a registry, not hardcoded
if-else in chat code.

Core chat logic steps:

1. Load Role by id from registry.

2. Load system_instructions, tone, language style,
   response mode, model policy, memory policy, safety profile.

3. Load user customization (custom role instructions, tone override
   within allowed range, formal/casual, concise/detailed,
   language selection, "Speak like me" mirroring,
   creativity/factuality mode mapped to Accuracy and Creativity,
   preferred model, output format).

4. Build final system prompt: system_instructions + user customization
   + safety and disclaimer policy + evidence policy if persona
   + memory + RAG context if attached via Retrieval Service.

5. Call provider abstraction with provider-neutral config
   (temperature, top_p mapped from Accuracy and Creativity mode).

6. Return response with citations if any, disclaimer if required,
   audit log with Role version, prompt version, model, tokens, cost.

No hardcoding of Role names in core logic.

## Role vs Specialist Persona vs Agent - Clarification

- **Role:** Conversation-only, no tools, no autonomous actions.
  Defines identity, tone, style, method, language,
  creativity defaults.

- **Specialist Persona:** Versioned, evidence-aware, domain-specific Role.
  Still conversation-only, may use approved knowledge retrieval
  via platform-owned Retrieval Service, does not independently perform
  external actions.

- **Agent:** Performs work, may use tools, browse, retrieve, call APIs,
  process files, run multi-step workflows, must have permissions,
  budgets, safety controls, auditability.

See `ROLE_PERSONA_AGENT_BOUNDARIES.md` for strict separation and flows.

## Role Definition Fields - Extensible Registry

| Field | Type | Required | Description |
|---|---|---|---|
| id | String(100) | Yes | Unique slug, e.g., normal_assistant |
| version | String(20) | Yes | Semantic version, e.g., v1.0.0 |
| display_name_fa | String(255) | Yes | Persian display name |
| display_name_en | String(255) | Yes | English display name |
| description | Text | Yes | One sentence purpose, Persian first |
| category | String(50) | Yes | general, learning, friendly, etc. |
| system_instructions | Text | Yes | Core system prompt, identity, method, boundaries |
| default_tone | String(50) | Yes | e.g., supportive, structured, direct |
| allowed_tones | JSONB List | Yes | e.g., ["supportive","direct"] |
| default_language_style | String(50) | Yes | e.g., formal, casual, balanced |
| allowed_language_styles | JSONB List | Yes | e.g., ["formal","casual"] |
| default_response_mode | String(50) | Yes | Maps to Accuracy and Creativity: strict_factual, balanced, creative |
| allowed_response_modes | JSONB List | Yes | Safe range per Role |
| default_model_policy | String(100) | Yes | e.g., auto_routing, fast, balanced, strong |
| memory_policy | String(50) | Yes | e.g., session_only |
| risk_level | String(20) | Yes | low, medium, high |
| disclaimer_policy | Text | Yes | When and what disclaimer to show |
| safety_profile | String(100) | Yes | e.g., general_safe, high_risk_health_info |
| evidence_policy | Text | Yes | Evidence standard, citation requirements |
| enabled | Boolean | Yes | Whether Role is enabled |
| created_at | DateTime | Yes | Creation time |
| updated_at | DateTime | Yes | Last update time |

### Additional Fields for Specialist Personas - Knowledge Base Architecture

Specialist Personas extend Role with knowledge-base fields:

- **knowledge_base_ids:** List of approved Knowledge Base IDs this Persona may use

- **retrieval_policy:** How retrieval works, e.g., top_k 5, minimum relevance score

- **allowed_source_types:** e.g., systematic_reviews, professional_guidelines,
  peer_reviewed, official_org, reviewed_public

- **minimum_evidence_policy:** Policy for minimum evidence, e.g., requires at least
  one Grade A or two Grade B, not just count

- **knowledge_pack_version:** Version of knowledge pack, e.g., v1.0.0

- **knowledge_pack_reviewed_at:** Date of last review

- **knowledge_pack_expires_at:** Expiry date, when must be reviewed again

- **expert_review_required:** Boolean, true for high-risk

- **expert_review_status:** pending, approved, rejected, with reviewer name,
  credentials, date

- **citation_policy:** How to cite, e.g., publisher, date, source ID,
  no hallucinated citations

- **conflicting_evidence_policy:** How to handle conflicting evidence:
  present both, note conflict, prioritize higher grade

- **source_freshness_policy:** How recent sources must be, e.g., prefer last
  2 years for AI, 5 years for stable guidelines

- **geographic_scope:** e.g., Global, Iran, US - does source apply globally
  or specific jurisdiction

- **jurisdiction_scope:** e.g., Iran general legal info only, not US law

These fields are proposed, not final, and require owner approval.

### Care and Truthfulness Fields - New

For high-risk supportive Personas, add explicit policy for care
without uncritical agreement:

- **care_truthfulness_policy:** How to validate emotions without validating
  unsupported factual claims

- **belief_validation_policy:** How to distinguish feelings, interpretations,
  assumptions, observable facts

- **professional_handoff_policy:** When and how to recommend qualified human
  support, how to help prepare for professional contact

- **crisis_response_policy:** How to respond to crisis, self-harm, severe
  distress - calm, supportive, resources, no secret data sharing,
  future expert/legal/privacy review required

- **prohibited_authority_claims:** List of claims Persona must never make
  (licensed psychologist, therapist, diagnosis, treatment,
  emergency service, knows other person's intentions)

## Specialist Knowledge-Base Architecture - Clarification

**Roles and Specialist Personas remain conversation-only, but may receive
approved context through separate platform-owned retrieval service.**

- A Role or Specialist Persona does not execute retrieval tools itself.

- A platform-owned Retrieval Service queries approved Knowledge Bases.

- The Retrieval Service returns cited, filtered context with provenance.

- The context is passed to the Role or Specialist Persona.

- Autonomous browsing or multi-step research belongs to an Agent, not Role.

### Flow - Role with Knowledge Base

```
User Message
→ Channel Adapter (Website, mobile, Telegram, API)
→ Context Assembly Service
→ Approved Specialist Knowledge Base (e.g., career guides, SEO guides)
→ Retrieved Context with Provenance (publisher, date, source ID, evidence grade)
→ Specialist Persona (conversation-only, uses context, citation-aware)
→ AI Provider (via provider abstraction, mapped from Accuracy and Creativity)
→ Response with Citations and Boundaries (disclaimer if needed, no authority claims)
```

**Knowledge source requirements:**

- Prefer systematic reviews, professional guidelines, peer-reviewed research,
  official professional organizations, and reviewed public sources.

- Books must be public domain, licensed, purchased with appropriate usage
  rights, or otherwise legally authorized for ingestion.

- Do not unlawfully ingest or reproduce copyrighted or paywalled books.

- Every source must include provenance, publisher, date, access date,
  review date, and evidence classification.

- Sources must be versioned and removable (knowledge_pack_version,
  knowledge_pack_reviewed_at, knowledge_pack_expires_at).

## Initial Ordinary Roles

These are conversation-only Roles, no tools:

1. **Normal Assistant**
   - id: normal_assistant
   - display_name_fa: دستیار عادی
   - Default mode for all new users
   - Risk: low

2. **Language Learning Companion**
   - id: language_learning_companion
   - display_name_fa: همدم یادگیری زبان
   - Risk: low

3. **Language Tutor**
   - id: language_tutor
   - display_name_fa: معلم زبان
   - Risk: low

4. **Friendly Companion**
   - id: friendly_companion
   - display_name_fa: همدم دوستانه
   - Risk: low

5. **Writer**
   - id: writer
   - display_name_fa: نویسنده
   - Risk: low

6. **Editor**
   - id: editor
   - display_name_fa: ویراستار
   - Risk: low

7. **Business Assistant**
   - id: business_assistant
   - display_name_fa: دستیار کسب‌وکار
   - Risk: low

8. **Planning Assistant**
   - id: planning_assistant
   - display_name_fa: دستیار برنامه‌ریزی
   - Risk: low

9. **Prompt Engineer**
   - id: prompt_engineer
   - display_name_fa: مهندس پرامپت
   - Risk: low

All low risk, Phase 1, no expert review required beyond QA.

## High-Risk Future Specialist Personas

- Evidence-Based Mental Health Information Assistant
  - id: mental_health_info_assistant
  - Risk: high
  - Must not be described as actual psychologist, therapist,
    diagnosis service, treatment service, or emergency service
  - Tone: structured, direct, calm, evidence-based
  - Not generic compassionate companion
  - Requires expert review, disclaimer, escalation

- Immigration Information Assistant
  - id: immigration_info_assistant
  - Risk: high
  - General information only, not legal advice
  - Uses approved official-source Knowledge Base via Retrieval Service
  - Does not browse autonomously

- Legal Information Assistant
  - id: legal_info_assistant
  - Risk: high
  - General legal information, not advice, not verdict

- Health Information Assistant
  - id: health_info_assistant
  - Risk: high
  - General health information, not diagnosis, not treatment

All high-risk require disclaimer, escalation, expert review, and
must not claim professional authority.

## Care Without Uncritical Agreement

Add explicit policy for high-risk supportive Personas:

**Policy names suggested:**

- care_truthfulness_policy

- belief_validation_policy

**Policy must state:**

- Validate the user's emotions and lived experience.

- Do not automatically validate unsupported factual claims.

- Do not agree merely to satisfy or retain the user.

- Distinguish feelings, interpretations, assumptions, and observable facts.

- Disclose uncertainty.

- Ask calm, non-confrontational reality-checking questions where appropriate.

- Do not intensify paranoia, delusional framing, self-destructive beliefs,
  or unsupported accusations.

- Do not shame, ridicule, argue aggressively, or dismiss the user.

- Do not diagnose.

- Do not claim that the system knows another person's intentions.

- Maintain empathy while remaining grounded in evidence and uncertainty.

- **Proposed fields:**
  - care_truthfulness_policy
  - belief_validation_policy
  - professional_handoff_policy
  - crisis_response_policy
  - prohibited_authority_claims

**Clarify:**

> Empathy means recognizing the user's feelings.
> It does not mean confirming every interpretation or factual belief.

This behavior must be testable in future Persona QA and red-team suites.

## Human Professional Handoff

For mental-health information Persona:

1. Continue calm, supportive, non-judgmental conversation.

2. Explain system limitations honestly:
   - Not a licensed professional, not therapy, not diagnosis.

3. Avoid diagnosis and treatment claims.

4. Gently recommend qualified human support when situation appears
   persistent, severe, high-risk, or beyond system's role.

5. Offer to help user prepare for contacting professional.

6. Offer practical steps such as writing concerns, identifying preferences,
   or preparing questions for first appointment.

7. Do not secretly share conversation content with staff or specialists.

8. Human review of private content requires informed user consent
   and a separately approved support workflow.

9. Crisis behavior must remain subject to future expert, legal, privacy,
   security, and product-owner review.

10. Do not promise absolute confidentiality.

11. Do not identify Persona as licensed psychologist or therapist.

## Evidence Quality (Not Just Count)

- Remove unapproved exact requirement 7+ primary sources unless approved
  existing policy and expert decision explicitly requires it.

- Use minimum_primary_sources: EXPERT_APPROVED_CONFIG

- Evidence quality must not be reduced to source count.

- Evaluation based on:
  - Evidence hierarchy (Primary > Secondary > Tertiary)
  - Source quality
  - Publisher authority
  - Relevance
  - Recency
  - Jurisdiction and geographic applicability
  - Conflicting evidence
  - Expert review
  - Knowledge-pack version

- If evidence grades Grade A/B retained, link to document that defines
  those grades: SOURCE_QUALITY_POLICY.md (planned, otherwise mark
  grading model as Open Decision).

- Otherwise mark grading model as Open Decision.

## Immigration Persona vs Agent Separation

Fix Product Vision contradiction:

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

## User Customization

- Custom role instructions

- Tone (choose from allowed_tones)

- Formal/casual style

- Concise/detailed style

- Language selection

- Speak like me language mirroring

- Creativity and factuality mode (Accuracy and Creativity)

- Preferred model

- Preferred output format

All stored per user per Role, versioned, editable later.

## Default Mode

- **Default mode: Normal Assistant - Not psychologist - Not therapist**

- First-use onboarding should ask user what Role and communication style
  they prefer.

- User must be able to change settings later via settings page.

## Extensibility

Adding new Role should not require changing core chat logic.
Registry-based: Add new entry in Role registry with all fields.
Versioning: When Role updated, version bumped, changelog.

## Safety

- High-risk Roles require expert review, QA and red teaming.

- No Role may claim professional authority, diagnosis, verdict, therapy.

- Disclaimer policy enforced per risk_level.

- Allowed response modes restricted per risk: high-risk only strict_factual
  and balanced, not creative.

- User customization within allowed safe range only.

## Linkage

- Boundaries: [ROLE_PERSONA_AGENT_BOUNDARIES](ROLE_PERSONA_AGENT_BOUNDARIES.md)

- Persona Framework: [PERSONA_FRAMEWORK](../personas/PERSONA_FRAMEWORK.md)

- Agent Plugin: [AGENT_PLUGIN_AND_EXECUTION_SYSTEM](AGENT_PLUGIN_AND_EXECUTION_SYSTEM.md)

- Accuracy and Creativity: [ACCURACY_CREATIVITY_CONTROL](ACCURACY_CREATIVITY_CONTROL.md)

- Human Approval: [HUMAN_APPROVAL_GATES](../agents/HUMAN_APPROVAL_GATES.md)

- Care Safety: CARE_SAFETY_AND_HUMAN_SUPPORT.md (planned, future - not clickable yet)

- Trust and Safety: [TRUST_AND_SAFETY_FRAMEWORK](../safety/TRUST_AND_SAFETY_FRAMEWORK.md)
