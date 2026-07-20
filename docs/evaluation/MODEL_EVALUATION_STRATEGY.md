# MODEL EVALUATION STRATEGY - Phase 0 Governance

**Date:** 2026-07-20
**Status:** Planning doc only

## Purpose
How to evaluate AI models (chat, image, video, embeddings) for quality, cost, latency, safety.

## Evaluation Dimensions

- **Quality:** Factual accuracy, coherence, Persian fluency, prompt adherence
- **Safety:** No disallowed content, no authority claims, proper escalation, no hallucinated citations (for persona), NSFW filter for image
- **Cost:** Tokens per response, cost per image second, cost per embedding
- **Latency:** P50, P95 response time
- **Persian:** RTL handling, Persian typography, Persian error messages quality (for Phase 1 baseline)
- **Citation:** For RAG personas, citation correctness, hallucinated citation rate 0%

## Benchmark Datasets (To Be Created)

- **General Chat:** 20 Persian general queries (e.g., "سلام، یک ایده برای کسب‌وکار کوچک")
- **Prompt Enhancer:** 20 prompts before/after, human rated improvement 1-5
- **Persona:** Per persona 20 scenarios + 15 safety red team prompts (from PERSONA_QA_AND_RED_TEAMING)
- **Image:** 20 product photo prompts, human rated adherence, quality, before/after
- **Video:** Future 10 text-to-video prompts
- **RAG:** 20 doc Q&A with known answers, citation correctness

## Metrics

- **Accuracy:** % correct vs gold standard (expert reviewed)
- **Hallucination:** % responses with hallucinated citations or unsupported claims (must 0% for persona factual)
- **Escalation:** % proper escalation for crisis/diagnosis/verdict/therapy (must 100%)
- **Disclaimer Present:** % Medium/High risk first response has disclaimer (must 100%)
- **Persian Fluency:** Human rated 1-5
- **Latency:** P50, P95
- **Cost:** Avg cost per request
- **NSFW:** % disallowed content blocked

## Process

1. Model Evaluation Agent (L1 report) defines benchmark and metrics per phase
2. Research Agent collects benchmark prompts
3. Fullstack Builder runs eval script (future: evals/ folder)
4. QA Security reviews
5. Report in docs/evaluation/reports/ with accuracy, hallucination, cost, latency, recommendation
6. Human approval required to change provider/model (approval gate: changing production config)

## Provider Abstraction Link

- Provider wrapper logs model version, tokens, cost per call
- Evaluation uses same wrapper

## Safety

- No evaluation that bypasses ToS, no scraping
- No sharing raw supplier keys
- Evaluation data no PII, no secrets

## Storage

- Future: `evals/` folder with datasets, `docs/evaluation/reports/` with reports
- Phase 0: Only strategy doc, no code

## Linkage
- Persona Evaluation: PERSONA_EVALUATION_STRATEGY.md (specific for personas)
- Provider Abstraction: PROVIDER_ABSTRACTION_STRATEGY.md
- Trust & Safety: TRUST_AND_SAFETY_FRAMEWORK.md
