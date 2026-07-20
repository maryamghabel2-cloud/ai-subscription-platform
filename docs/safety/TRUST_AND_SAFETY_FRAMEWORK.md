# TRUST AND SAFETY FRAMEWORK

**Date:** 2026-07-20
**Status:** Planning doc only

## Purpose
Define trust and safety policies for Persian AI Platform - content, personas, image/video, Telegram, API.

## Principles

- Safety by design, not afterthought
- Evidence-based, not authoritative for high-risk domains
- Human approval gates for publishing, spending, contacting, pricing, config, merge, deploy, API keys, persona sensitive edits
- Absolutely forbidden actions have no approval path: ToS bypass, geographic/sanctions/KYC bypass, fake identities, hiding prohibited locations, sharing/reselling unauthorized credentials/raw supplier keys, CSAM, non-consensual intimate imagery, deepfake without consent, claiming professional authority

## Content Policies

### General AI Content
- No disallowed content: hate, harassment, self-harm encouragement (must provide crisis resources + escalation), non-violent wrongdoing facilitation, CSAM, non-consensual intimate imagery
- No medical diagnosis, no legal verdict, no psychological therapy session, no emergency replacement - provide general info only with disclaimer + escalation to professional
- No guarantee claims: no guarantee job, ranking, income
- No hallucinated citations: must cite real sources with publisher+date+source ID or say not in sources

### Persona-Specific

- **Risk Levels:** Low (Prompt Engineer, SEO Advisor, Instagram Strategist, Product Photography Advisor), Medium (Career Advisor, Sales, E-commerce, Business Automation), High (Psychologist evidence-based structured direct, Physician Assistant, Legal Assistant, Vet, Plant with pesticide)
- **High Risk Requirements:** Minimum 7 primary sources, domain-expert reviewer name/credentials/date, last knowledge review date, expiry schedule 1 month, benchmark 15 safety prompts, accuracy >=90%, hallucinated citations 0%, proper escalation 100%, disclaimer 100%
- **Psychologist:** Structured, direct, evidence-based mental-health information and guided-assessment assistant, NOT generic compassionate companion. Provides psychoeducation, general coping strategies based on reputable sources, guided self-reflection questions with disclaimer that formal assessment requires professional. Clear boundaries against false professional identity, unsupported diagnosis, unsafe treatment, emergency replacement. If crisis (self-harm): immediate crisis resources general, encourage professional help, no therapy session.
- **Physician/Legal:** General info only, disclaimer "Not medical/legal advice, consult qualified professional, if emergency call emergency services", no diagnosis, no verdict
- **All Personas:** Structured, direct where appropriate, domain-specific, evidence-based, citation-aware, non-generic

### Image Generation

- NSFW filter: block explicit nudity, sexual content involving minors (CSAM absolute forbidden)
- Copyrighted style: block style that imitates living artist without consent? Policy: allow style but not direct copy, need compliance review
- Product photography: no trademarked logo removal without permission? General guidance
- No disallowed content

### Video & Character

- Consent gate for character: cannot create deepfake of real person without explicit consent checkbox + human review flag
- No non-consensual intimate imagery
- No impersonation of real person for deception

### Telegram & Business Agents

- No spam: rate limit 30 msg/min per bot, no bulk broadcast without human approval
- Token encrypted at rest, never in logs, audit log access
- Support draft replies: draft → human review → send (not auto)
- No bulk messaging to customers without approval

### API Platform

- API key hashed, prefix shown once, scopes least privilege, rate limit 60/min, credit check, insufficient → 402
- Revoke API key requires human user action
- No auto key creation without user action

## Human Approval Gates (Recap)

- Publishing public content, spending money, contacting customers, bulk messages, changing prices/config, merging PRs, deploying prod, creating/deleting API keys, modifying legal/medical/psych personas, launching paid campaigns, issuing refunds/credits above threshold, creating new agent type, escalating maturity, deleting data, banning users
- Absolutely forbidden: ToS bypass, geographic/sanctions/KYC bypass, fake identities, hiding prohibited locations, credential sharing/reselling - no approval may authorize

## Enforcement

- QA Security Agent checks PRs for forbidden patterns
- Compliance/Risk Agent reviews High-risk persona changes
- Trust & Safety Agent (L1 report) defines policies and checklists
- If forbidden detected, PR closed without merge

## Audit Logs

- Who, what, when, result, rollback reference
- For persona responses: persona version, prompt version, knowledge-pack version, model, tokens, cost, disclaimer present, escalation triggered
- For safety blocks: blocked reason, input hash, timestamp

## Versioning & Review

- Safety framework version v1.0
- Review schedule: monthly for high-risk areas, plus when guideline updates

## Linkage
- Human Approval Gates: HUMAN_APPROVAL_GATES.md
- Persona Framework: PERSONA_FRAMEWORK.md
- Data Classification: DATA_CLASSIFICATION_AND_RETENTION.md
- Evaluation: MODEL_EVALUATION_STRATEGY.md
