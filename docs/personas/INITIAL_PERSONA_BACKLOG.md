# INITIAL PERSONA BACKLOG

**Date:** 2026-07-19
**Updated:** 2026-07-20 - Added mandatory evidence fields per review

**Mandatory Fields for Each Persona (Per PERSONA_FRAMEWORK):**
- source hierarchy (Primary > Secondary > Tertiary)
- primary vs secondary distinction
- evidence grade (A/B/C/D)
- source publisher, publication/update date, access date
- geographic/jurisdiction scope
- last knowledge review date
- conflicting-evidence handling policy
- minimum number of primary sources (Low 3+, Medium 5+, High 7+)
- domain-expert reviewer requirement (name, credentials, date for High)
- citation requirements (publisher+date+source ID, no hallucination)
- benchmark dataset (scenario prompts)
- accuracy and hallucination metrics (factual accuracy %, hallucinated citations 0%, proper escalation 100%)
- knowledge-pack version
- expiry/review schedule (Low 6 months, Medium 3 months, High 1 month)

Specialist personas must be structured, direct where appropriate, domain-specific, evidence-based, citation-aware, non-generic.
  
**Total:** 14 initial ideas - all start as idea/planned/research-needed, not ready yet.

## Low Risk - Can Be First (Phase 2)

### 1. Prompt Engineer
- **Purpose:** Help craft better prompts for chat/image/video
- **Target:** Creators, developers, all users
- **Maturity:** planned
- **Risk:** Low
- **Research depth:** Medium - need prompt guides from OpenAI, Anthropic
- **Knowledge sources:** OpenAI prompt guide, Anthropic library, LangChain prompts
- **Notes:** Good first persona, reusable across platform

### 2. Researcher
- **Purpose:** Evidence-based research assistant, summary with citations
- **Target:** Students, researchers
- **Maturity:** planned
- **Risk:** Medium (hallucination risk) → require citations
- **Research depth:** High - need RAG evaluation
- **Knowledge sources:** Need to define citation standard
- **Notes:** Will need RAG in Phase 7, but Phase 2 can be general research with disclaimer

### 3. SEO Advisor
- **Purpose:** Evidence-based SEO guidance, not guarantee rankings
- **Target:** Creators, business owners
- **Maturity:** planned
- **Risk:** Low
- **Research depth:** Medium - SEO guides
- **Knowledge sources:** Google SEO starter guide, Moz, Search Engine Journal
- **Notes:** No guarantee #1 ranking, must include that

### 4. Instagram Content Strategist
- **Purpose:** Draft content calendar, captions, hashtags - draft only, human publishes
- **Target:** Creators, small shops
- **Maturity:** idea
- **Risk:** Low
- **Research depth:** Medium
- **Knowledge sources:** Instagram best practices, Persian content trends
- **Notes:** Must say draft, human approval to publish

### 5. Product Photography Advisor
- **Purpose:** Guide product studio settings, lighting, background advice
- **Target:** Creators
- **Maturity:** planned
- **Risk:** Low
- **Research depth:** Medium
- **Knowledge sources:** Product photography guides
- **Notes:** Links to Phase 3 Image Studio

## Medium Risk - Phase 2 Later After Low Risk

### 6. Career Advisor
- **Purpose:** Resume, interview, job search general info
- **Target:** Job seekers 22-35
- **Maturity:** research-needed
- **Risk:** Medium (affects employment)
- **Research depth:** High - labor market, resume best practices
- **Knowledge sources:** HBR resume guide, Persian job market data
- **Notes:** No guarantee job, no personalized career verdict without human professional

### 7. Sales Advisor
- **Purpose:** Sales script, objection handling general info
- **Target:** Business owners
- **Maturity:** research-needed
- **Risk:** Medium
- **Research depth:** High
- **Knowledge sources:** Sales methodologies (SPIN, Challenger)
- **Notes:** General info, not specific business legal advice

### 8. E-commerce Advisor
- **Purpose:** Shop setup, pricing, shipping general info
- **Target:** Business owners
- **Maturity:** idea
- **Risk:** Medium
- **Research depth:** Medium
- **Notes:** No financial guarantee

### 9. Business Automation Advisor
- **Purpose:** Workflow automation ideas (Telegram, no code)
- **Target:** Business owners
- **Maturity:** idea
- **Risk:** Medium
- **Research depth:** Medium
- **Notes:** No code execution without approval

## High Risk - Requires Deep Research, Compliance Review, Not Phase 2

### 10. Psychologist - Evidence-based, Structured, Direct Mental-Health Information and Guided-Assessment Assistant (Future)
- **Purpose:** Provide evidence-based mental health information, psychoeducation, general coping strategies (e.g., grounding, behavioral activation general info) based on reputable sources, and guided self-reflection questions with clear disclaimer that formal assessment requires professional. NOT therapy, NOT diagnosis, NOT treatment plan, NOT emergency replacement. Must be structured, direct, evidence-based, NOT merely generic compassionate companion.
- **Target:** Users seeking general mental wellness information, psychoeducation - not crisis, not seeking diagnosis
- **Maturity:** idea
- **Risk:** High
- **Research depth:** Very High - needs licensed psychologist consultant, DSM-5-TR general info only (not diagnostic criteria applied to user), APA general info, WHO mental health general info, peer-reviewed coping RCTs
- **Knowledge sources (Mandatory fields):**
  - Source 1: Title, Publisher APA, Publication Date 2023-11, Access Date 2026-07-20, Primary, Evidence Grade A, Geographic Scope Global general info, URL real
  - Plus 6+ more primary sources (minimum 7 for High risk)
- **Source Hierarchy:** Primary (peer-reviewed RCTs, official APA/WHO general info) > Secondary (reputable summaries) > Tertiary not acceptable alone
- **Evidence Grade:** Grade A/B only
- **Geographic Scope:** Global general info, note Iran local resources for crisis need local validation
- **Last Knowledge Review Date:** To be set when research done
- **Conflicting-Evidence Handling:** Present both views, note conflict, prioritize higher grade + newer, disclose uncertainty
- **Minimum Primary Sources:** 7+
- **Domain-Expert Reviewer Requirement:** Licensed psychologist name, credentials (e.g., PhD, license #), review date required, comments
- **Citation Requirements:** Every coping strategy claim must cite publisher + date + source ID, no hallucination
- **Benchmark Dataset:** 15 psychology safety eval prompts (crisis, diagnosis attempt, therapy request, guarantee, disallowed content)
- **Accuracy Metrics:** Proper escalation for crisis/diagnosis 100%, no diagnosis 100%, disclaimer present 100%, hallucinated citations 0%
- **Knowledge-Pack Version:** v0.1 idea
- **Expiry/Review Schedule:** 1 month or when APA guideline updates
- **Notes:** MUST include disclaimer: "I am an evidence-based mental health information assistant, not a psychologist, not therapy, not diagnosis, not emergency service. Information only based on [Publisher, Date], for general info only, consult qualified mental health professional for your situation. If you are in crisis or thinking about self-harm, contact local crisis line or emergency services immediately and reach out to trusted person." Must have structured direct tone, not generic companion. Must have guided self-reflection questions with disclaimer that formal assessment requires professional. Must have red teaming, compliance review, Trust & Safety review, human approval gate for any prompt change. Not in Phase 2, future after research pipeline. Absolutely forbidden to claim authority, give diagnosis, create treatment plan, replace emergency.


### 11. Physician Assistant
- **Purpose:** General health information, not diagnosis, not treatment
- **Target:** Users seeking general health info
- **Maturity:** idea
- **Risk:** High
- **Research depth:** Very High - needs medical reviewer, reputable sources like WHO general info
- **Knowledge sources:** WHO, Mayo Clinic general info, but no specific diagnosis
- **Notes:** Must say: "Information only, not medical advice, consult qualified physician, if emergency call emergency services" - High risk, not Phase 2

### 12. Legal Assistant
- **Purpose:** General legal information, not legal advice, not verdict
- **Target:** Users seeking general legal info
- **Maturity:** idea
- **Risk:** High
- **Research depth:** Very High - needs legal reviewer
- **Knowledge sources:** General legal info sources, but no specific case advice
- **Notes:** Disclaimer: "Not legal advice, consult qualified lawyer" - not Phase 2

### 13. Veterinarian Assistant
- **Purpose:** General pet care info, not diagnosis
- **Target:** Pet owners
- **Maturity:** idea
- **Risk:** High (animal health)
- **Research depth:** High
- **Knowledge sources:** Vet general info
- **Notes:** Disclaimer, encourage vet consultation

### 14. Plant Advisor
- **Purpose:** General plant care info (watering, light)
- **Target:** Plant owners
- **Maturity:** idea
- **Risk:** Medium/High if pesticide advice (toxicity) → must avoid pesticide dosage, say consult expert
- **Research depth:** Medium
- **Knowledge sources:** Horticulture guides
- **Notes:** Avoid chemical dosage, general care only

## Maturity Definitions
- idea: Just idea in backlog
- planned: In backlog with purpose/target defined
- research-needed: Need research report before prompt draft
- ready-later: Research done, prompt draft, needs QA/red teaming + human approval

## Next
- Use RESEARCH_TO_PERSONA_PIPELINE.md to move from idea → research → draft → QA → ready-later
- High-risk personas require compliance review and are NOT in Phase 2
