# SOURCE QUALITY POLICY

**Date:** 2026-07-20
**Status:** Planning doc only

## Purpose
Define how to evaluate source quality for persona knowledge, research reports, growth content, RAG.

## Mandatory Fields Per Source (Per Persona Framework Review)

- **Source ID:** e.g., SRC-001
- **Title**
- **Publisher:** e.g., American Psychological Association, WHO, Harvard Business Review, Google
- **Publication/Update Date:** e.g., 2024-03-15
- **Access Date:** e.g., 2026-07-20
- **Primary vs Secondary:** Primary (original research, official guideline, direct data) vs Secondary (summary of primary, textbook, reputable secondary)
- **Evidence Grade:** Grade A (high-quality RCT/meta/official guideline), Grade B (cohort, reputable org), Grade C (expert consensus, case series), Grade D (anecdotal, not acceptable alone for high-risk)
- **Geographic/Jurisdiction Scope:** Global, Iran, US, EU, etc. Must consider if source applies to Persian user context
- **URL:** Real URL, not hallucinated, accessible
- **Excerpt/Use:** How used in persona or report
- **Last Knowledge Review Date:** When source was last reviewed for currency
- **Conflicting Evidence Handling:** Policy for this source if conflicts with others

## Source Hierarchy

- **Primary:** Peer-reviewed research, official guidelines (APA, WHO, Google SEO Starter), direct data from reputable org, original research paper
- **Secondary:** Reputable secondary summary that cites primary (e.g., NIMH summary of RCT, Moz summary of Google guideline, HBR article summarizing research)
- **Tertiary:** General guides, blog posts that summarize secondary - not acceptable alone for High-risk personas, okay as supplementary for Low risk if primary present

## Evidence Grade

- **Grade A:** High-quality RCT, meta-analysis, systematic review, official guideline from major reputable org (APA, WHO, Google SEO Starter Guide)
- **Grade B:** Cohort study, case-control, reputable org report (e.g., labor market report from reputable source)
- **Grade C:** Expert consensus, case series, reputable textbook
- **Grade D:** Anecdotal, personal blog, forum post - not acceptable alone, only as supplementary with disclaimer

## Minimum Primary Sources

- Low risk personas: 3+ primary sources
- Medium risk personas: 5+ primary sources
- High risk personas (psychologist, physician, legal, vet): 7+ primary sources, Grade A/B only, domain-expert reviewer required

## Publisher Reputation

- Acceptable: Major reputable orgs (APA, WHO, NIMH, Harvard, Stanford, Google, Moz, Search Engine Journal with caution, official government sites)
- Not acceptable: Personal blog without credentials, forum post, AI-generated content without sources, content farm

## Publication/Update Date & Access Date

- Must be recent enough: For rapidly evolving fields (AI, SEO), prefer last 2 years. For stable guidelines (CBT coping), up to 5 years maybe acceptable but note update date
- Access date shows when we retrieved - important for web content that may change

## Geographic/Jurisdiction Scope

- Example: US labor law does not apply to Iran - must note scope, say "This is US general info, for Iran consult local expert"
- For legal assistant: Must specify Iran jurisdiction general info only, not US law for Iran user without disclaimer
- For career: Iran labor market data vs global best practices - note both

## Last Knowledge Review Date & Expiry/Review Schedule

- Low risk: Review every 6 months
- Medium risk: 3 months
- High risk: 1 month or when guideline updates (e.g., APA updates)
- Must be tracked in registry: last_knowledge_review_date, expiry_review_schedule

## Conflicting Evidence Handling

- Policy: Present both views, note conflict, prioritize higher evidence grade + newer + more reputable publisher, disclose uncertainty, avoid cherry-picking, cite both sources
- Example: Two sources conflict on resume length - present both: "Source A (HBR, 2023, Grade B) says 1 page, Source B (reputable HR guide, 2024, Grade B) says 2 pages acceptable for experience - conflict noted, choose based on..."

## Citation Requirements

- Every non-common-knowledge factual claim must have citation: [Source ID, Publisher, Publication Date, Primary/Secondary, Evidence Grade]
- Example: "STAR method improves interview performance [SRC-001, Harvard Business Review, 2023-05-10, Secondary, Grade B]"
- No hallucinated citations - URL must be real and accessible, publisher real, date real
- If RAG attached: include doc ID + chunk ID + publisher + date

## Domain-Expert Reviewer Requirement

- High risk: Licensed/domain expert reviewer required with name, credentials, license #, review date, comments, approval
- Medium risk: Recommended, but at least Compliance/Risk + QA Security review
- Low risk: QA Security + Compliance review, expert optional

## Benchmark Dataset

- For each persona, define benchmark dataset of prompts: functional + red team, with gold standard answers expert reviewed
- Track accuracy %, hallucination %, escalation %, disclaimer %

## Accuracy & Hallucination Metrics

- Factual Accuracy % vs gold standard
- Hallucinated Citations % (must 0%)
- Proper Escalation % (must 100% for crisis/diagnosis/verdict/therapy attempts)
- Citation Correctness % (publisher+date+ID real and correct)

## Knowledge-Pack Version

- Version for each persona's knowledge pack, changelog, e.g., career_knowledge_pack v1.2.0

## Access & Storage

- Research reports stored in docs/research/ or research/
- Sources listed with full mandatory fields
- No secrets, no fake URLs

## Quality Policy Enforcement

- Research Agent must fill all mandatory fields
- Prompt Engineer must check source hierarchy and evidence grade
- QA Security must check no hallucinated citations, publisher/date present, primary count met
- Compliance/Risk must review High risk source quality
- Human approval gate requires source quality checklist

## Absolutely Forbidden

- Using fake identities, hiding prohibited locations, sharing/reselling unauthorized credentials - no approval may authorize
- Hallucinating sources (fake publisher, fake URL, fake date)
- Claiming authority based on low-quality sources

## Linkage
- Persona Framework: PERSONA_FRAMEWORK.md
- Research to Persona Pipeline: RESEARCH_TO_PERSONA_PIPELINE.md
- Trust & Safety: TRUST_AND_SAFETY_FRAMEWORK.md
