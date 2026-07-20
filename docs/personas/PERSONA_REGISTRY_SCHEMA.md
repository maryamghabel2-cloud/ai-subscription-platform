# PERSONA REGISTRY SCHEMA

**Date:** 2026-07-19

## Purpose
Single JSON/YAML file that lists all personas, their metadata, version, status.

## Schema (YAML Example)

```yaml
personas:
  - id: prompt_engineer
    name: Prompt Engineer
    version: v1.0
    maturity: ready-later
    status: active / draft / archived
    risk_level: Low
    domain: prompt engineering
    target_users: developers, creators
    purpose: Helps craft better prompts via evidence-based methods
    tone: structured, direct, helpful
    method: "Explain prompt components, provide 3 variants"
    evidence_standard: "Prompt engineering guides from reputable sources"
    knowledge_sources_required:
      - "OpenAI prompt guide"
      - "Anthropic prompt library"
    knowledge_sources_actual:
      - "https://platform.openai.com/docs/guides/prompt-engineering"
    prompt_policy: "No authority claims, general info"
    escalation_behavior: "If legal/medical prompt requested, escalate"
    prompt_version: v1.0.0
    model: "gpt-4o-mini or equivalent"
    credit_cost: 1
    disclaimer: "Evidence-based assistant, not certified, info only"
    evaluation_tests_passed: true
    qa_date: 2026-07-19
    red_team_date: 2026-07-19
    changelog:
      - v0.1: Idea
      - v1.0: Research done, prompt v1, QA passed
```

## Fields Required

- id (snake_case unique)
- name
- version (semver)
- maturity (idea/planned/research-needed/ready-later)
- status (draft/active/archived)
- risk_level (Low/Med/High)
- domain
- target_users
- purpose
- tone, method
- evidence_standard
- knowledge_sources_required (list)
- knowledge_sources_actual (list with URLs, must be real)
- prompt_policy
- escalation_behavior
- prompt_version
- model (future)
- credit_cost
- disclaimer
- evaluation_tests_passed (bool)
- qa_date, red_team_date
- changelog

## Storage

- Phase 0-2: `docs/personas/registry.yaml` (future file)
- Phase 3+: DB table personas + prompt versions table

## Validation

- Research agent must fill knowledge_sources_required
- Compliance/Risk agent must review High risk
- No persona moves to ready-later without QA and red teaming
- Human approval required for High risk persona prompt changes
