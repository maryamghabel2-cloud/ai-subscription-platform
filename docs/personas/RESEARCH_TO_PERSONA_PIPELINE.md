# RESEARCH TO PERSONA PIPELINE

**Date:** 2026-07-19  
**Updated:** 2026-07-20 - Added mandatory evidence fields

## Purpose
Safe pipeline from idea to ready-later, with strengthened evidence standard.

## Steps

### 1. Idea (in INITIAL_PERSONA_BACKLOG)
- Fill purpose, target, risk, research depth, geographic scope
- Owner: Product Manager Agent (L1 report)

### 2. Research Phase (Required Before Prompt) - Strengthened

- **Owner:** Research Agent (L1 report)
- **Inputs:** Persona backlog entry, PERSONA_FRAMEWORK.md with mandatory fields
- **Outputs:** Research report `docs/research/persona_{id}_research.md` with:
  - Domain overview
  - **Source Hierarchy:** Primary > Secondary > Tertiary definition for this persona
  - **Minimum 3/5/7 primary sources collected** (Low 3+, Medium 5+, High 7+) each with:
    - Source ID, Title, Publisher, Publication/Update Date, Access Date, Primary vs Secondary, Evidence Grade A/B/C, Geographic/Jurisdiction Scope, URL (real, not hallucinated), Excerpt/Use
  - Evidence standard proposal (which grades acceptable)
  - Conflicting-evidence handling policy proposal
  - Geographic/jurisdiction scope analysis (e.g., Iran legal vs global general info)
  - Domain-expert reviewer requirement analysis (who needed for High risk)
  - Benchmark dataset proposal (which prompts/scenarios)
  - Risk analysis: what if persona gives wrong info
  - Existing persona comparison
  - Recommended tone (structured, direct where appropriate), method
  - Knowledge-pack version v0.1 idea
  - Open questions
  - Last knowledge review date = report date, Expiry schedule proposal
- **Approval Gate:** Research report needs human approval if High risk, plus compliance review

### 3. Prompt Draft - Strengthened

- **Owner:** Prompt Engineer Agent (L2 branch+PR)
- **Inputs:** Research report with full mandatory fields, FRAMEWORK, TEMPLATE
- **Outputs:**
  - Draft prompt file `docs/personas/drafts/{id}_v0.1_prompt.md` with:
    - Role, domain, tone (structured direct where appropriate), method, evidence standard, source hierarchy, knowledge sources with publisher+dates+primary distinction+grade+scope, conflicting evidence handling, citation requirements, disclaimer, escalation behavior, versioning
  - Entry in registry.yaml draft with all mandatory fields: source publisher, publication/update date, access date, geographic scope, last knowledge review date, conflicting-evidence handling, min primary sources count, domain-expert reviewer requirement, citation requirements, benchmark dataset, accuracy/hallucination metrics, knowledge-pack version, expiry/review schedule
  - Must be structured, domain-specific, evidence-based, citation-aware, non-generic
  - For Psychologist: structured, direct, evidence-based mental-health information and guided-assessment assistant, not generic compassionate companion
- **Forbidden:** Authority claims, hallucinated sources, missing mandatory fields

### 4. QA and Red Teaming - Strengthened

- **Owner:** QA Security Agent (L2) + Compliance/Risk (L1) + Domain Expert for High risk + new Trust & Safety, Model Evaluation agents
- **Inputs:** Draft prompt, FRAMEWORK, QA_AND_RED_TEAMING.md with benchmark dataset
- **Outputs:** QA report `docs/personas/qa/{id}_qa_report.md` with:
  - 10 functional tests
  - 5 red team tests
  - Benchmark dataset evaluation: accuracy %, hallucination % (must 0% fake citations), proper escalation %, disclaimer present %
  - Checks: source hierarchy respected? Primary count met? Publisher/date/access date present? Geographic scope considered? Conflicting evidence handling per policy? Domain-expert reviewer assigned for High? Citation requirements met? Structured direct domain-specific? For Psychologist: not generic companion, structured direct evidence-based?
  - Accuracy and hallucination metrics
- **Pass Criteria:** No authority claims, proper escalation, citations correct with publisher+date+source ID, disclaimer present, evidence grade respected, conflicting evidence handled, no hallucinated citations, benchmark accuracy >= threshold (e.g., 90%), hallucination 0%, domain-expert review for High

### 5. Human Approval Gate

- Required for ALL personas, especially High risk
- Founder reviews: research report with full mandatory fields, prompt draft, QA report with metrics
- If High risk: also compliance + domain expert review (name, credentials, date)
- Approval via GitHub issue comment "Approved" + label needs-human-approval removal

### 6. Ready-Later Status

- Update INITIAL_PERSONA_BACKLOG maturity to ready-later
- Update registry.yaml status draft, version v1.0.0, knowledge-pack version, last knowledge review date, expiry schedule, all mandatory fields filled
- Not yet live in product - needs Phase 2 implementation

### 7. Implementation (Phase 2+)

- Fullstack Builder (L2) implements persona in product (API + UI)
- E2E test: 15 tests + benchmark dataset
- Audit log: persona version, prompt version, knowledge-pack version, model

## Artifacts - Updated

- research/persona_{id}_research.md with full mandatory fields
- personas/drafts/{id}_prompt.md with structured direct evidence-based citation-aware
- personas/qa/{id}_qa_report.md with accuracy/hallucination metrics, benchmark
- registry.yaml entry with publisher, dates, geographic scope, last review, conflicting handling, min primary, expert reviewer, citation req, benchmark, metrics, knowledge-pack version, expiry

## Safety Controls

- No High risk persona moves past research without compliance + domain expert review
- No persona claims authority
- Escalation mandatory
- Versioning mandatory: persona version, prompt version, knowledge-pack version
- Expiry/review schedule mandatory
- No persona with geographic/jurisdiction scope mismatch (e.g., US law for Iran user without disclaimer)
