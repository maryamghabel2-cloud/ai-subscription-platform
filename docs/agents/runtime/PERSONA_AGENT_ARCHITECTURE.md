# PERSONA AGENT ARCHITECTURE

**Date:** 2026-07-19  
**Phase:** 2

## Overview
Persona system allows user to chat with specialist evidence-based assistants.

## Architecture Components

- **Persona Registry Schema:** `docs/personas/PERSONA_REGISTRY_SCHEMA.md` - JSON schema for each persona
- **Framework:** `PERSONA_FRAMEWORK.md` - role, domain, tone, method, evidence standard, knowledge sources, prompt policy, escalation, risk, versioning, evaluation
- **Template:** `PERSONA_TEMPLATE.md`
- **Pipeline:** `RESEARCH_TO_PERSONA_PIPELINE.md` - research → draft → QA/red teaming → approval → versioned release
- **QA:** `PERSONA_QA_AND_RED_TEAMING.md`

## Persona Runtime Flow

1. User selects persona (e.g., Career Advisor, SEO Advisor)
2. Frontend sends persona_id + message to /personas/{id}/chat (future API)
3. Backend loads persona prompt template + knowledge sources (RAG if attached)
4. Prompt Enhancer enhances user message
5. LLM call with persona system prompt + enhanced user prompt + RAG context
6. Response includes disclaimer if risk medium/high (e.g., "This is information, not professional advice, consult ...")
7. Audit log: persona version, prompt version, model, tokens
8. Wallet deducts credits

## Prompt Policy

- No authoritative claims: "I am not a doctor/lawyer/psychologist, this is information only"
- Evidence standard: For each persona, define required knowledge sources (e.g., for Career Advisor: labor market data, resume best practices)
- Escalation: If user asks for diagnosis, legal verdict, therapy, persona must escalate: suggest professional consultation, provide general info only
- Tone: Defined per persona (e.g., structured, direct for Psychologist evidence-based, but not therapy)
- Method: How persona reasons (e.g., STAR for career)

## Memory

- Phase 1-2: Session memory only
- Future: Optional long-term memory with user consent, deletable

## Wallet/Credit

- Chat billed per token or per message (simple for Phase 2)
- Persona premium may cost more

## Versioning

- Persona version: v1.0.0, changelog in registry
- Prompt version tracked per response

## Safety

- Risk classification: Low (Prompt Engineer, SEO Advisor), Medium (Career, Sales), High (Physician, Legal, Psychologist, Vet) → High requires deep research, compliance review, red teaming before release
- See PERSONA_QA_AND_RED_TEAMING.md for evaluation tests
- Human approval required for any legal/medical/psych persona prompt changes

## Future RAG

- Phase 7: Persona can have attached knowledge base (e.g., SEO Advisor has SEO guide docs)
- Retrieval with citations
