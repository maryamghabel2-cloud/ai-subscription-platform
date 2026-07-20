# PERSONA REGISTRY SCHEMA

**Date:** 2026-07-19  
**Updated:** 2026-07-20 - Added mandatory evidence fields per review

## Purpose
Single JSON/YAML file that lists all personas, their metadata, version, status, with strengthened evidence-based fields.

## Schema (YAML Example - Full Mandatory Fields)

```yaml
personas:
  - id: prompt_engineer
    name: Prompt Engineer
    version: v1.0.0
    knowledge_pack_version: v1.0.0
    maturity: ready-later # idea/planned/research-needed/ready-later
    status: active # draft/active/archived
    risk_level: Low # Low/Med/High
    domain: prompt engineering
    geographic_scope: Global
    target_users: developers, creators
    purpose: Helps craft better prompts via evidence-based methods
    tone: structured, direct, helpful # Must be specific, not generic
    method: "Explain prompt components, provide 3 variants with evidence"
    evidence_standard: "Prompt engineering guides from reputable sources, Grade A/B"
    source_hierarchy: "Primary > Secondary > Tertiary, Tertiary not acceptable alone"
    minimum_primary_sources: 3
    knowledge_sources_required: # Before ready, list needed
      - "OpenAI prompt guide"
      - "Anthropic prompt library"
    knowledge_sources_actual: # Actual with mandatory fields
      - source_id: SRC-001
        title: "Prompt Engineering Guide"
        publisher: "OpenAI"
        publication_date: "2024-02-10"
        update_date: "2024-05-01"
        access_date: "2026-07-19"
        primary_vs_secondary: "Primary"
        evidence_grade: "A"
        geographic_scope: "Global"
        url: "https://platform.openai.com/docs/guides/prompt-engineering"
        excerpt_use: "Used for prompt components"
      - source_id: SRC-002
        title: "Prompt Library"
        publisher: "Anthropic"
        publication_date: "2024-03-20"
        access_date: "2026-07-19"
        primary_vs_secondary: "Primary"
        evidence_grade: "A"
        geographic_scope: "Global"
        url: "https://docs.anthropic.com/claude/docs/prompt-library"
    conflicting_evidence_handling: "Present both views, note conflict, prioritize higher grade + newer, disclose uncertainty"
    domain_expert_reviewer_requirement:
      required: false # true for High risk
      reviewer_name: ""
      credentials: ""
      review_date: ""
      comments: ""
    last_knowledge_review_date: "2026-07-19"
    expiry_review_schedule: "6 months for Low"
    prompt_policy: "No authority claims, general info, disclaimer, escalation"
    escalation_behavior: "If legal/medical prompt requested, escalate to suggest professional"
    prompt_version: v1.0.0
    model: "gpt-4o-mini or equivalent"
    credit_cost: 1
    benchmark_dataset: "20 prompt engineering scenario prompts"
    accuracy_metrics:
      factual_accuracy: 95%
      hallucinated_citations: 0%
      proper_escalation: 100%
      disclaimer_present: 100%
    hallucination_metrics:
      fake_citation_rate: 0%
    citation_requirements: "Every non-common-knowledge claim must cite source ID + publisher + date, no hallucination"
    disclaimer: "Evidence-based assistant, not certified, info only, based on OpenAI and Anthropic guides"
    evaluation_tests_passed: true
    qa_date: "2026-07-19"
    red_team_date: "2026-07-19"
    changelog:
      - version: v0.1
        date: 2026-07-10
        changes: "Idea"
      - version: v1.0.0
        date: 2026-07-19
        changes: "Research done, prompt v1, QA passed"
```

## High-Risk Example Fields (Psychologist)

```yaml
  - id: psychologist_evidence_based
    name: "Psychologist - Evidence-Based Information & Guided Assessment Assistant"
    risk_level: High
    domain: mental health information, psychoeducation, coping strategies general info
    tone: structured, direct, calm, evidence-based # Not generic compassionate companion
    method: "Psychoeducation + evidence-based coping + guided self-reflection questions with disclaimer that formal assessment requires professional"
    evidence_standard: "APA general info, WHO mental health general info, peer-reviewed coping RCTs, Grade A/B only"
    minimum_primary_sources: 7
    knowledge_sources_actual:
      - source_id: SRC-001
        title: "Understanding Psychotherapy"
        publisher: "American Psychological Association"
        publication_date: "2023-11-01"
        access_date: "2026-07-19"
        primary_vs_secondary: "Primary"
        evidence_grade: "A"
        geographic_scope: "Global general info, not Iran jurisdiction specific"
        url: "https://www.apa.org/topics/psychotherapy"
    domain_expert_reviewer_requirement:
      required: true
      reviewer_name: "Dr. Example, Licensed Psychologist, PhD"
      credentials: "Licensed Psychologist, CA #12345"
      review_date: "2026-07-20"
      comments: "Approved with disclaimer and escalation"
    last_knowledge_review_date: "2026-07-20"
    expiry_review_schedule: "1 month or when APA guideline updates"
    disclaimer: "I am an evidence-based mental health information assistant, not a psychologist, not therapy, not diagnosis, not emergency service. Information only based on APA and WHO general info. For specific situation consult qualified mental health professional. If crisis contact local crisis line/emergency services."
    benchmark_dataset: "15 psychology safety eval prompts (crisis, diagnosis attempt, therapy request)"
    accuracy_metrics:
      proper_escalation_for_crisis: 100%
      no_diagnosis: 100%
      disclaimer_present: 100%
      hallucinated_citations: 0%
```

## Mandatory Fields List (Per Review)

- source hierarchy
- primary vs secondary source distinction
- evidence grade (A/B/C/D)
- source publisher
- publication/update date
- access date
- geographic/jurisdiction scope
- last knowledge review date
- conflicting-evidence handling policy
- minimum number of primary sources (Low 3+, Medium 5+, High 7+)
- domain-expert reviewer requirement (name, credentials, date for High)
- citation requirements (publisher+date+source ID, no hallucination)
- benchmark dataset
- accuracy and hallucination metrics (%)
- knowledge-pack version
- expiry/review schedule

## Storage

- Phase 0-2: docs/personas/registry.yaml (future file)
- Phase 3+: DB table personas + prompt versions + knowledge packs

## Validation

- Research agent must fill all mandatory fields before ready-later
- Compliance/Risk must review High risk, check source publisher, dates, primary count, expert reviewer
- No persona moves to ready-later without QA + red team + accuracy metrics
- Human approval required for High risk prompt changes
- No persona claims authority, must be structured, direct where appropriate, domain-specific, evidence-based, citation-aware, non-generic
