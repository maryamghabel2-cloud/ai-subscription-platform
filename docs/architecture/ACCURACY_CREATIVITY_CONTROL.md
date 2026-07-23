# Accuracy and Creativity Control

**Date:** 2026-07-23

**Status:** Proposed Product Architecture — Pending Owner Approval

**Purpose:** Define user-friendly label for accuracy and creativity modes,
avoid "hallucination level" wording, define normalized modes,
and describe provider-neutral configuration.

## User-Facing Label

- **Do NOT expose a user setting called "hallucination level."**
  - This is technical jargon, negative framing, and confusing for users.

- **Use user-friendly label:** `Accuracy and Creativity`

- **Persian UX concept:** `دقت و خلاقیت`
  - User-friendly, positive framing, understandable.

## Normalized Modes

Define three normalized modes that are provider-neutral and user-friendly.

### 1. strict_factual

- **Persian label:** دقیق و مستند

- **Description:** Low creativity, high accuracy, factual, citation-aware.

- **Behavior:**
  - No unsupported factual claims.
  - Citation-aware: must cite sources when making factual claims.
  - Must disclose uncertainty if sources conflict or not found.
  - Must never invent citations, including fake URLs or fake publisher
    and date.

- **Use cases:**
  - Research, study workspace, RAG with sources, fact-checking.
  - When user asks for evidence-based information.
  - High-risk personas such as health information, legal information,
    and immigration information should default to `strict_factual`
    or `balanced`, not `creative`.

- **Provider mapping:**
  - Provider-validated deterministic configuration.
  - Lower creativity, more deterministic.

### 2. balanced

- **Persian label:** متعادل

- **Description:** General-purpose conversation with moderate creativity.

- **Behavior:**
  - Helpful, balanced accuracy and creativity.
  - Suitable for most chats.

- **Use cases:**
  - General chat, business assistant, planning assistant,
    prompt engineer, everyday questions.

- **Provider mapping:**
  - Provider-validated general-purpose configuration.

### 3. creative

- **Persian label:** خلاق

- **Description:** Storytelling, advertising, brainstorming, role-play,
  and creative writing.

- **Behavior:**
  - May invent fictional elements only when the task is clearly creative,
    such as story, ad copy, brainstorming ideas, role-play,
    artistic images, or brand concepts.
  - Must never invent factual citations, legal rules, medical claims,
    provider prices, or current events.
  - Even in creative mode, factual domains remain restricted.

- **Use cases:**
  - Writer, editor, advertising campaign, poster, banner,
    social media assets, artistic images, brand concepts,
    storytelling, storyboard, character workflows.

- **Provider mapping:**
  - Provider-validated creative configuration.

## Symbolic Guidance (Not Production Defaults)

Exact temperature, top_p, and top_k values are **Open Decisions**
and must not be treated as production-approved values.

- **strict_factual:**
  - Lower creativity.
  - Provider-validated deterministic configuration.
  - Must be selected per model, not merely per provider.

- **balanced:**
  - Provider-validated general-purpose configuration.
  - Must be selected per model.

- **creative:**
  - Provider-validated creative configuration.
  - Must be selected per model.

State clearly:

- Exact mappings must be selected per model, not merely per provider.

- Exact values require model evaluation and versioned tests.

- Do not assume all models from one provider support the same parameters.

- Values must be documented in versioned evaluation reports, not hardcoded
  as unvalidated defaults in architecture docs.

No exact numeric defaults are provided here.

## Role and Persona Default Modes

Each Role may recommend a default response mode:

- **Normal Assistant:** `balanced`

- **Language Learning Companion:** `balanced`

- **Writer:** `creative` (but must not invent factual citations)

- **Editor:** `balanced`

- **Business Assistant:** `balanced`

- **Planning Assistant:** `balanced`

- **Prompt Engineer:** `balanced`

- **Career Advisor (medium risk):** `balanced`, may allow `strict_factual`,
  not `creative`

- **Sales Advisor:** `balanced`

- **SEO Advisor:** `balanced`

- **Evidence-Based Mental Health Information Assistant (high risk):**
  `strict_factual` only

- **Immigration Information Assistant (high risk):** `strict_factual` only

- **Legal Information Assistant (high risk):** `strict_factual` only

- **Health Information Assistant (high risk):** `strict_factual` only

**Rule:** High-risk specialist personas must NOT default to `creative`.
Allowed safe range should be restricted to `strict_factual` and `balanced`.

## User Override Within Safe Range

Users may override default response mode only within the Role's allowed
safe range.

- Example: Normal Assistant allows `strict_factual`, `balanced`, `creative`
  → user may choose any of the three.

- Example: Career Advisor allows `strict_factual`, `balanced`
  → user may choose those, but NOT `creative`.

- Example: Mental Health Information Assistant allows `strict_factual` only
  → user cannot override to `creative`.

- Example: Writer allows `balanced`, `creative`
  → may allow creative as default, but also balanced for factual writing.

**Enforcement:**

- UI Role selector shows allowed modes per Role.

- Backend validates requested mode is in `allowed_response_modes`.

- Rejects with 400 if not allowed.

## Separation of Factuality and Empathy

This is critical and was previously ambiguous.

- **Accuracy and Creativity controls factual behavior and creative freedom.**

- **It does NOT control kindness, warmth, empathy, respect, or Care Principle.**

- `strict_factual` must NOT mean cold, robotic, abrupt, or dismissive.

- A mental-health information Persona may remain `strict_factual` while still
  responding calmly, warmly, compassionately, and without judgment.

- **Empathy and respect are independent of factuality mode.**
  - A response can be both factually strict and emotionally supportive.
  - Example: Providing evidence-based coping information in a calm,
    warm, non-judgmental tone.

- **Legitimate emotional conversations must not be abruptly terminated.**
  - If user discusses trauma, grief, loss, seeking support, do not end
    conversation abruptly.
  - Provide supportive, non-judgmental response within safe boundaries,
    encourage professional support if needed, offer general coping
    information.

- **Detailed Care and human-support workflows will be defined in the
  future `CARE_SAFETY_AND_HUMAN_SUPPORT` architecture document.**
  - This document is not implemented in this PR.
  - It will define how to respond to users in distress, crisis resources,
    escalation, and human-support handoff.

- **No Persona may claim to be a licensed psychologist or therapist.**
  - Must not claim professional license, diagnosis, therapy, treatment,
    or emergency service.
  - Must include disclaimer and escalation to professional.

## Care Without Uncritical Agreement

For high-risk supportive Personas, add explicit policy:

**Policy names:**

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

**Clarify:**

> Empathy means recognizing the user's feelings.
> It does not mean confirming every interpretation or factual belief.

**Proposed fields for registry (if retained):**

- care_truthfulness_policy

- belief_validation_policy

- professional_handoff_policy

- crisis_response_policy

- prohibited_authority_claims

This behavior must be testable in future Persona QA and red-team suites.

See `ROLE_AND_PERSONA_SYSTEM.md` for full human professional handoff
behavior (9 required steps plus additional safety notes).

## Violence and Sensitive-Content Wording (Refined)

Previously overly broad wording forbade all "violent content" and could
be interpreted as prohibiting legitimate discussion of trauma or history.

Clearly distinguish:

**Allowed examples (must not be prohibited):**

- Discussing trauma, war, abuse, grief, and loss

- Seeking emotional support related to those experiences

- Historical, journalistic, educational, or fictional discussion

- Safety-oriented analysis of violence

- Non-graphic contextual discussion of difficult topics

- Personal narratives about overcoming adversity

**Restricted or prohibited examples (per Trust and Safety policy):**

- Operational instructions intended to facilitate real-world harm

- Instructions that enable illegal harmful activity

- Non-consensual sexual imagery

- Sexual exploitation

- CSAM (Child Sexual Abuse Material)

- Targeted abuse or harassment toward protected characteristics

- Other content prohibited by the approved Trust and Safety policy

**Principles:**

- Do not make sensitive discussion itself prohibited.

- Do not weaken protections against illegal or exploitative content.

- Allow supportive, educational, journalistic, and fictional contexts.

- Restrict instructions that facilitate harm, not discussion of harm.

## Provider-Neutral Configuration Layer

**Problem:** Different providers use different sampling parameters.

- OpenAI: temperature, top_p, presence_penalty, frequency_penalty, etc.

- Anthropic: temperature, top_p, top_k, etc.

- Google: temperature, top_p, top_k, etc.

- Local models: various parameters

**Solution:**

- Provider-neutral config layer maps normalized modes
  (`strict_factual`, `balanced`, `creative`) to provider-specific
  parameters.

- Core chat logic uses normalized modes, not raw provider parameters.
  - Adding new provider does not require changing core logic.
  - Only mapping in config layer needs update, with evaluation.

- Exact mappings must be selected per model, not merely per provider.
  - Example: GPT-4o vs GPT-4o-mini may need different values even though
    both from OpenAI.
  - Values require model evaluation and versioned tests.
  - Do not assume all models from one provider support same parameters.

- Config layer is versioned and documented in evaluation reports.

**Storage:**

- User preference: `user_role_preferences` table with `response_mode`

- Role registry: `default_response_mode` and `allowed_response_modes`

- Audit log: logs which mode was used per response (prompt hash,
  not raw content, per privacy logging correction)

## Safety

- **Never invent citations:** Even in creative mode, must never invent
  factual citations, fake URLs, fake publisher or date.

- **Never invent legal rules, medical claims, provider prices,
  current events:** Even in creative mode, these remain disallowed.

- **High-risk personas restricted to strict_factual and balanced:**
  To avoid unsafe creative invention for health, legal, immigration.

- **Must disclose uncertainty:** In strict_factual, if sources conflict
  or not found, disclose uncertainty.

- **Human approval for persona prompt changes, especially high-risk:**
  Per `HUMAN_APPROVAL_GATES.md`.

## Persian UX

- **Label:** `دقت و خلاقیت`
  - User-friendly, positive, understandable.
  - Not technical jargon `سطح توهم`.

- **Modes Persian:**
  - `strict_factual`: `دقیق و مستند`
    - کمترین خلاقیت، بیشترین دقت، بدون ادعای بدون پشتوانه، با ذکر منبع

  - `balanced`: `متعادل`
    - مناسب برای گفتگوی روزمره، تعادل دقت و خلاقیت

  - `creative`: `خلاق`
    - داستان‌نویسی، تبلیغات، طوفان فکری، نقش‌آفرینی
    - فقط زمانی که وظیفه واضحاً خلاقانه است می‌تواند عناصر داستانی اختراع کند
    - هرگز نباید استناد واقعی، قوانین حقوقی، ادعاهای پزشکی،
      قیمت ارائه‌دهندگان، یا رویدادهای جاری را اختراع کند

- **UI:** Slider or 3 buttons with Persian labels and descriptions.

- **First-use onboarding:** Ask user preferred Accuracy and Creativity mode.

## Linkage

- Role and Persona System:
  [ROLE_AND_PERSONA_SYSTEM](ROLE_AND_PERSONA_SYSTEM.md)

- Persona Framework:
  [PERSONA_FRAMEWORK](../personas/PERSONA_FRAMEWORK.md)

- Agent Plugin and Execution:
  [AGENT_PLUGIN_AND_EXECUTION_SYSTEM](AGENT_PLUGIN_AND_EXECUTION_SYSTEM.md)

- Provider Abstraction:
  [PROVIDER_ABSTRACTION_STRATEGY](PROVIDER_ABSTRACTION_STRATEGY.md)

- Evaluation: [PERSONA_EVALUATION_STRATEGY](../personas/PERSONA_QA_AND_RED_TEAMING.md)

- Trust and Safety:
  [TRUST_AND_SAFETY_FRAMEWORK](../safety/TRUST_AND_SAFETY_FRAMEWORK.md)

- Future Care: CARE_SAFETY_AND_HUMAN_SUPPORT.md (planned, future - not clickable yet)
