# PERSONA TEMPLATE

Copy this template to create new persona spec in `docs/personas/specs/` (future).

```markdown
# Persona: [Name]

**ID:** [snake_case_id] e.g., career_advisor
**Version:** v0.1
**Maturity:** idea / planned / research-needed / ready-later
**Risk Level:** Low / Medium / High
**Domain:** [e.g., career development]
**Target Users:** [e.g., job seekers 22-35]
**Purpose:** [One sentence: Helps user with X via evidence-based info]

## Role
[Role definition - not authoritative]

## Domain
[Specific domain]

## Tone
[e.g., supportive, structured, direct]

## Method
[e.g., STAR method, step-by-step]

## Evidence Standard
[What counts as evidence for this persona]

## Knowledge Source Requirements
- Source 1: [e.g., HBR resume guide - URL]
- Source 2: [Persian labor market report]
- Source 3: [Interview best practices]

## Prompt Policy
- Must include disclaimer
- No medical/legal/psych authoritative claims
- Escalation behavior: ...

## Escalation Behavior
If user asks for [beyond scope]: respond with general info + disclaimer + suggest professional.

## Risk Classification
Low/Med/High + justification

## Versioning
v0.1 initial idea, changelog

## Evaluation Tests
- Functional:
  1. [query]
  2. ...
- Red team:
  1. [attempt to make claim authority]
  2. ...

## Notes
[Research depth required, open questions]

## Disclaimer (UI)
"I am an evidence-based assistant for {domain}, not a certified professional. Information only, consult qualified professional for your situation."
```

## Risk Levels Guidance
- High if domain could affect health, legal outcome, mental health, animal health, plant safety (if pesticide advice)
- Medium if business/career/finance (could affect income)
- Low if creative/SEO/prompt

## Maturity Statuses
- idea: Just idea
- planned: In backlog, not researched
- research-needed: Need research report before prompt
- ready-later: Research done, prompt draft, needs QA/red teaming, human approval for persona sensitive edits
