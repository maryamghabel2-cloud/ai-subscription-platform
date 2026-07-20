# RESEARCH TO PERSONA PIPELINE

**Date:** 2026-07-19

## Purpose
Defines how to go from persona idea to ready-later status safely.

## Steps

### 1. Idea (in INITIAL_PERSONA_BACKLOG)
- Fill purpose, target, risk, research depth
- Owner: Product Manager Agent

### 2. Research Phase (Required Before Prompt)
- **Owner:** Research Agent
- **Inputs:** Persona backlog entry, FRAMEWORK.md
- **Outputs:** Research report `docs/research/persona_{id}_research.md` with:
  - Domain overview
  - 3-5 reputable sources (URLs, not hallucinated)
  - Evidence standard proposal
  - Risk analysis
  - Existing persona comparison
  - Recommended tone, method
  - Open questions
- **Approval Gate:** Research report needs human approval if High risk

### 3. Prompt Draft
- **Owner:** Prompt Engineer Agent
- **Inputs:** Research report, FRAMEWORK, TEMPLATE
- **Outputs:** Draft prompt file `docs/personas/drafts/{id}_v0.1_prompt.md` + entry in registry YAML draft
- **Must Include:** Role, domain, tone, method, evidence standard, knowledge sources, disclaimer, escalation
- **Forbidden:** Authority claims

### 4. QA and Red Teaming
- **Owner:** QA Security Agent + Compliance Risk Agent (for High risk)
- **Inputs:** Draft prompt, FRAMEWORK, QA_AND_RED_TEAMING.md
- **Outputs:** QA report with 10 functional + 5 red team test results
- **Pass Criteria:** No authority claims, proper escalation, citations where needed, tone matches, disclaimer present
- **For High risk:** Must have external domain expert review (e.g., psychologist consultant for psychologist persona) - documented

### 5. Human Approval Gate
- Required for ALL personas, especially High risk
- Founder reviews: research report, prompt draft, QA report
- If High risk: also compliance review
- Approval via GitHub issue comment "Approved"

### 6. Ready-Later Status
- Update INITIAL_PERSONA_BACKLOG maturity to ready-later
- Update registry.yaml status draft, version v1.0
- Not yet live in product - needs Phase 2 implementation (API)

### 7. Implementation (Phase 2+)
- Fullstack Builder implements persona in product (API + UI)
- E2E test

## Artifacts

- research/persona_{id}_research.md
- personas/drafts/{id}_prompt.md
- QA report
- registry.yaml entry

## Safety Controls

- No High risk persona moves past research without compliance review
- No persona claims medical/legal/psych authority
- Escalation behavior mandatory
- Versioning mandatory

## Example Timeline (Medium Risk Persona: Career Advisor)

- Day 1: Idea in backlog
- Day 2-3: Research Agent produces report with 3 sources
- Day 4: Prompt Engineer drafts prompt v0.1
- Day 5: QA Security runs 15 tests
- Day 6: Human approval
- Day 7: ready-later, waiting for Phase 2 implementation
