# Prompt Injection Defense

**Version:** v0.1.0

**Date:** 2026-07-24

**Status:** Draft - Structure Only

**Document Owner:** Security Architect / AI Safety

**Purpose:** Define defenses against direct prompt injection, indirect prompt injection, jailbreak attempts, tool abuse, RAG poisoning, data exfiltration, system-prompt disclosure, and input/output guardrails.

**Note:** This is a structure-only stub. Final policy will be completed later.

## In Scope

- Direct Prompt Injection: user messages attempting to override system instructions, role impersonation, authority claims (e.g., claiming to be psychologist/therapist)
- Indirect Prompt Injection: injected instructions in uploaded files, PDFs, RAG context, tool outputs, web search results, Telegram messages
- Jailbreak attempts: attempts to bypass safety, trust and safety policy, care_truthfulness_policy, belief_validation_policy
- Tool abuse: causing Agent to perform forbidden actions via injected tool calls (spend money, publish, contact customers, delete data, bypass geographic/KYC/ToS)
- RAG poisoning: malicious documents in approved Knowledge Bases, provenance verification, publisher/date/review date/evidence classification required, versioned and removable sources
- Data exfiltration: attempts to extract other users' data, secrets, API keys, prompts via injection
- System-prompt disclosure: prevent extraction of system_instructions, knowledge_base_ids, retrieval_policy
- Input and output guardrails: input validation, output filtering, citation integrity (no hallucinated citations), disclaimer enforcement, escalation to professional
- Role/Persona/Agent separation: conversation-only Roles must not execute tools based on injected instructions, autonomous browsing belongs to Agent with permissions/budgets/audit

## Out of Scope

- Final guardrail implementation, exact filter lists, model-specific mappings (future PRs)
- Red-team test cases (future Security Testing doc)

## Related Documents

- Security Index: [README.md](README.md)
- Accuracy and Creativity: [../architecture/ACCURACY_CREATIVITY_CONTROL.md](../architecture/ACCURACY_CREATIVITY_CONTROL.md)
- Role/Persona/Agent Boundaries: [../architecture/ROLE_PERSONA_AGENT_BOUNDARIES.md](../architecture/ROLE_PERSONA_AGENT_BOUNDARIES.md)
- Persona QA: [../personas/PERSONA_QA_AND_RED_TEAMING.md](../personas/PERSONA_QA_AND_RED_TEAMING.md)
- Agent Security Model: [AGENT_SECURITY_MODEL.md](AGENT_SECURITY_MODEL.md)

## Open Decisions

- Guardrail implementation per channel and per model
- Testing methodology for prompt injection suite
- Owner approval for thresholds

## Planned Completion Stage

- Phase 1 - AI Safety

## Status

Draft - Structure Only. Will be completed later.
