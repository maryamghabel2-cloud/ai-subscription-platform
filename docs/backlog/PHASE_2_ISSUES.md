# PHASE 2 ISSUES - Personas

**Milestone:** Phase 2 Personas

## ISSUE-2-01: Persona Framework Implementation

- **Title:** Implement persona registry schema + framework code
- **Purpose:** Evidence-based persona system
- **Owner:** Prompt Engineer
- **Dependencies:** Phase 1, Phase 0 persona docs
- **Acceptance:** Persona schema JSON, registry.yaml with 5 initial low-risk personas, framework fields enforced, no medical/legal authority claims
- **Priority:** P0
- **Phase:** phase-2
- **Risk:** Medium

## ISSUE-2-02: Persona Chat API

- **Title:** API /personas/list and /personas/{id}/chat
- **Purpose:** Chat with persona
- **Owner:** Fullstack Builder
- **Dependencies:** 2-01
- **Acceptance:** List returns 5 personas, chat returns persona-styled response with disclaimer if needed, audit log, wallet deduct, version tracked
- **Priority:** P0
- **Phase:** phase-2
- **Risk:** Medium

## ISSUE-2-03: Persona Directory UI

- **Title:** /personas and /personas/{id} pages
- **Purpose:** Browse personas
- **Owner:** Website Builder
- **Dependencies:** 2-02
- **Acceptance:** Directory grid shows risk badge, maturity, purpose, disclaimer banner, detail page shows knowledge sources, escalation, disclaimer, CTA try
- **Priority:** P0
- **Phase:** phase-2
- **Risk:** Low

## ISSUE-2-04: Persona QA and Red Teaming Reports

- **Title:** QA 15 tests per persona + red team 5 tests
- **Purpose:** Safety
- **Owner:** QA Security + Compliance Risk
- **Dependencies:** 2-01
- **Acceptance:** QA reports in docs/personas/qa/ with pass/fail, no authority claims, proper escalation, compliance review for any Medium risk, human approval gate for prompt changes
- **Priority:** P0
- **Phase:** phase-2
- **Risk:** High
