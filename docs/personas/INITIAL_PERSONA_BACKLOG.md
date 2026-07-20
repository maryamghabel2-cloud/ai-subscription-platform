# INITIAL PERSONA BACKLOG

**Date:** 2026-07-19  
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

### 10. Psychologist - Evidence-based, Structured, Direct Tone
- **Purpose:** Provide evidence-based mental health information, coping strategies general info, NOT therapy
- **Target:** Users seeking general wellness info
- **Maturity:** idea
- **Risk:** High
- **Research depth:** Very High - needs psychologist consultant, DSM-5 general info only, no diagnosis
- **Knowledge sources:** Need licensed psychologist to review, reputable mental health orgs (APA general info), coping strategies evidence-based
- **Notes:** MUST include: "I am not a psychologist, not therapy, information only, if crisis contact professional/crisis line, escalation to human professional" - must have red teaming, compliance review, human approval gate for any prompt change. Not in Phase 2, future after research pipeline.

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
