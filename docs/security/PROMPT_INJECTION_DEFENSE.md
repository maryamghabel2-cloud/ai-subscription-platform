# Prompt Injection Defense

**Version:** v0.1.0

**Date:** 2026-07-24

**Status:** Draft - Structure Only

**Document Owner:** Security Architect / AI Safety

**Purpose:** Define defenses against direct prompt injection, indirect prompt
injection, jailbreak attempts, tool abuse, RAG poisoning, data exfiltration,
system-prompt disclosure, and input/output guardrails.

**Note:** This is a structure-only stub. Final policy will be completed later.

## Purpose

Define how we prevent and detect prompt injection and AI misuse.

## In Scope

- Direct Prompt Injection:
  - User messages attempting to override system instructions
  - Role impersonation, authority claims (e.g., claiming to be psychologist)
- Indirect Prompt Injection:
  - Injected instructions in uploaded files, PDFs, RAG context, tool outputs,
    web search results, Telegram messages
- Jailbreak attempts:
  - Attempts to bypass safety, trust and safety policy, care_truthfulness_policy,
    belief_validation_policy
- Tool abuse:
  - Causing Agent to perform forbidden actions via injected tool calls
  - Spend money, publish, contact customers, delete data, bypass geographic/KYC/ToS
- RAG poisoning:
  - Malicious documents in approved Knowledge Bases
  - Provenance verification, publisher/date/review date required, versioned
- Data exfiltration:
  - Attempts to extract other users' data, secrets, API keys, prompts
- System-prompt disclosure:
  - Prevent extraction of system_instructions, knowledge_base_ids
- Input and output guardrails:
  - Input validation, output filtering, citation integrity
  - Disclaimer enforcement, escalation to professional
- Role/Persona/Agent separation:
  - Conversation-only Roles must not execute tools based on injected instructions
  - Autonomous browsing belongs to Agent with permissions/budgets/audit

## Out of Scope

- Final guardrail implementation and exact filter lists
- Model-specific mappings and test cases (future Security Testing doc)

## Related Documents

- Security Index: [README.md](README.md)
- Accuracy and Creativity: [../architecture/ACCURACY_CREATIVITY_CONTROL.md](../architecture/ACCURACY_CREATIVITY_CONTROL.md)
- Boundaries: [../architecture/ROLE_PERSONA_AGENT_BOUNDARIES.md](../architecture/ROLE_PERSONA_AGENT_BOUNDARIES.md)
- Persona QA: [../personas/PERSONA_QA_AND_RED_TEAMING.md](../personas/PERSONA_QA_AND_RED_TEAMING.md)
- Agent Security Model: [AGENT_SECURITY_MODEL.md](AGENT_SECURITY_MODEL.md)

## Open Decisions

- Guardrail implementation per channel and per model
- Testing methodology for prompt injection suite
- Owner approval for thresholds

## Planned Completion Stage

Phase 1 - AI Safety

## Status Note

Draft - Structure Only. Will be completed later.
