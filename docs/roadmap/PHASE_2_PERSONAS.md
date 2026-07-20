# Phase 2 - Specialist Personas

**Phase:** PHASE_2_PERSONAS  
**Date:** 2026-07-19  
**Status:** Planned (Phase 0 is current)

## Objective
Evidence-based specialist assistants with research, validation, safety controls.

## In Scope
- Persona Framework, Template, Registry
- Initial 5 personas: Prompt Engineer, Researcher, Career Advisor, Sales Advisor, SEO Advisor (low-risk first)
- Persona directory UI
- Prompt versioning + audit logs

## Out of Scope
High-risk personas (Physician, Legal, Psychologist) → need deep research, not in Phase 2. Image/video generation.

## Dependencies
Phase 1 chat infrastructure

## Technical Deliverables
- Persona schema: role, domain, tone, method, evidence standard, knowledge sources, prompt policy, escalation, risk classification, versioning
- Persona registry JSON/YAML
- API: /personas/list, /personas/{id}/chat
- Prompt enhancer integrated

## UX Deliverables
- Specialist Personas page
- Persona cards with purpose, risk, knowledge sources
- Chat with persona selector

## Business Deliverables
- Persona usage as credit spend
- Content to explain each persona is assistant, not authority

## Required Agents
Prompt Engineer, RAG Knowledge, Research, Compliance Risk, QA Security

## Test Requirements
- Persona QA and red teaming per PERSONA_QA_AND_RED_TEAMING.md
- No medical/legal authoritative claims
- Escalation test: persona says consult professional

## Risk Controls
- Hallucinated expertise → require evidence standard + source requirements
- Over-confidence → tone direct but humble, include disclaimer
- All human approval gates from HUMAN_APPROVAL_GATES.md must apply: spending money, publishing, contacting customers, changing prices/config, merging, deploying, API keys, persona changes, paid campaigns, refunds/credits above threshold require human approval.
- Audit logs required for all state-changing actions.
- No medical/legal/psychological authoritative claims.

## Exit Criteria
5 personas live, evaluable, documented, with disclaimers and audit logs
