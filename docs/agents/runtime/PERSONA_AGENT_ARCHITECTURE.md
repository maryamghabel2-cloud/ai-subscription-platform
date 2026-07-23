# DEPRECATED - PERSONA AGENT ARCHITECTURE

**Date:** 2026-07-19

**Updated:** 2026-07-23 - DEPRECATED, see new docs

**Status:** DEPRECATED - Do not use this terminology, confusing mix of Persona and Agent

## Deprecation Notice

> **DEPRECATION NOTICE:** This file name `PERSONA_AGENT_ARCHITECTURE`
> is confusing because it mixes Persona (which is a versioned,
> evidence-aware, domain-specific Role, still conversation-only,
> may use approved knowledge retrieval, does not independently
> perform external actions) and Agent (which performs work,
> may use tools, browse, retrieve, call APIs, process files,
> run multi-step workflows).
>
> **Specialist Persona is a versioned Role, not an Agent.**
> See new clear separation:
>
> - **Boundaries:**
>   `docs/architecture/ROLE_PERSONA_AGENT_BOUNDARIES.md` - Defines strict
>   separation: Role (conversation-only, no tools), Specialist Persona
>   (versioned Role, still conversation-only, may use approved knowledge
>   retrieval, no autonomous external actions, high-risk requires expert
>   review), Agent (performs work, tools, permissions, budgets, safety,
>   audit), Channel Adapter (Website, mobile, Telegram, API),
>   Studio Workflow (structured image/video generation, core revenue)
>
> - **Role and Persona System:**
>   `docs/architecture/ROLE_AND_PERSONA_SYSTEM.md` - Extensible
>   registry-based Role system, adding new Role should not require
>   changing core chat logic, fields, initial ordinary Roles,
>   high-risk future specialist Personas
>
> - **Agent Plugin and Execution:**
>   `docs/architecture/AGENT_PLUGIN_AND_EXECUTION_SYSTEM.md` - True Agents
>   that perform work as plugins with permissions, budgets, safety, audit
>
> - **Accuracy and Creativity:**
>   `docs/architecture/ACCURACY_CREATIVITY_CONTROL.md` - User-friendly label
>   "Accuracy and Creativity" Persian "دقت و خلاقیت" with modes
>   strict_factual, balanced, creative, provider-neutral config layer
>
> - **Persona Framework:**
>   `docs/personas/PERSONA_FRAMEWORK.md` - Mandatory evidence fields,
>   safety framing
>
> **Replacement:** For Persona definition, use ROLE_AND_PERSONA_SYSTEM.md
> and PERSONA_FRAMEWORK.md. For Agents that perform work, use
> AGENT_PLUGIN_AND_EXECUTION_SYSTEM.md and runtime Business Agent,
> Telegram Agent, Research Agent architectures. For Image/Video Studios,
> use Studio Workflow definition, not simple Role.
>
> **Existing links:** This file is kept with deprecation note to avoid
> breaking existing links silently. Update references in other docs to
> point to new boundaries doc.

---

## Original Content (Deprecated but preserved for history)

**Date:** 2026-07-19

**Phase:** 2

## Overview (Old - Confusing Terminology)

Persona system allows user to chat with specialist evidence-based
assistants. This was previously called "Persona Agent" but should be
called "Specialist Persona (versioned Role)" per new boundaries.

## Architecture Components (Old)

- **Persona Registry Schema:**
  `docs/personas/PERSONA_REGISTRY_SCHEMA.md`

- **Framework:** `PERSONA_FRAMEWORK.md`

- **Template:** `PERSONA_TEMPLATE.md`

- **Pipeline:** `RESEARCH_TO_PERSONA_PIPELINE.md`

- **QA:** `PERSONA_QA_AND_RED_TEAMING.md`

## Persona Runtime Flow (Old - Should be Role Runtime Flow)

1. User selects persona (e.g., Career Advisor)

2. Frontend sends persona_id + message to /personas/{id}/chat (future API)

3. Backend loads persona prompt template + knowledge sources (RAG if attached)

4. Prompt Enhancer enhances user message

5. LLM call with persona system prompt + enhanced user prompt + RAG context

6. Response includes disclaimer if risk medium/high

7. Audit log: persona version, prompt version, model, tokens

8. Wallet deducts credits

## Prompt Policy (Old)

- No authoritative claims

- Evidence standard

- Escalation

- Tone

- Method

## Memory, Wallet/Credit, Versioning, Safety, Future RAG (Old)

See original sections - now replaced by ROLE_AND_PERSONA_SYSTEM.md
and new architecture docs.

## Migration Guide

- Rename "Persona Agent" → "Specialist Persona (versioned Role, conversation-only)"

- Rename "Image Agent" → "Image Studio Workflow"

- Rename "Product Photography Agent" → "Product Photography Studio Workflow"

- Keep "Business Agent", "Telegram Agent", "Research Agent" as true Agents that perform work

- Channel Adapters (Website, mobile, Telegram, API) must not be classified as
  Role or Agent merely because they connect users

## Linkage

- Boundaries:
  [ROLE_PERSONA_AGENT_BOUNDARIES](../../architecture/ROLE_PERSONA_AGENT_BOUNDARIES.md)

- Role and Persona System:
  [ROLE_AND_PERSONA_SYSTEM](../../architecture/ROLE_AND_PERSONA_SYSTEM.md)

- Agent Plugin and Execution:
  [AGENT_PLUGIN_AND_EXECUTION_SYSTEM](../../architecture/AGENT_PLUGIN_AND_EXECUTION_SYSTEM.md)

- Accuracy and Creativity:
  [ACCURACY_CREATIVITY_CONTROL](../../architecture/ACCURACY_CREATIVITY_CONTROL.md)

- Persona Framework:
  [PERSONA_FRAMEWORK](../../personas/PERSONA_FRAMEWORK.md)
