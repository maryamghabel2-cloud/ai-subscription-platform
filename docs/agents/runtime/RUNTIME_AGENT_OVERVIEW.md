# RUNTIME AGENT OVERVIEW - User-Facing Product Agents

**Date:** 2026-07-19

## Difference: Project-Building vs Runtime Product Agents

| Aspect | Project-Building | Runtime Product |
|---|---|---|
| Serves | Founder building product | End-users inside platform |
| Example | Fullstack Builder, SEO Content | General Chat, Persona, Image Studio, Telegram Agent |
| Billing | Founder pays external tool | User pays credits via wallet |
| Maturity Now | L1/L2 external | Not built yet, doc only |
| Safety | Approval gates for merge/publish/spend | Evidence-based, risk classification, escalation, wallet checks |
| Output | PRs, reports | Chat messages, images, video renders, agent execution logs |

## Runtime Agent System (Future)

- **General Persian Chat:** Wrapper over LLM, Persian-first, memory per conversation
- **Prompt Enhancer:** Takes user prompt → enhanced prompt (separate tool)
- **Specialist Personas:** Evidence-based assistants (see PERSONA_FRAMEWORK) - career, sales, SEO, etc. Not authoritative for high-risk domains
- **Image Studio:** Prompt → image, Product Photography Studio workflow
- **Video & Character Tools:** Async jobs, consent gates for character
- **Telegram Agent:** Webhook, encrypted token, business logic
- **Business Agents:** FAQ, lead qualifier, content drafter for shops
- **Research/RAG:** Upload docs, ask with citations
- **Developer API Agent:** X-API-Key auth, rate limit, usage logs

## Common Components for All Runtime Agents

- **Persona System:** role, domain, tone, method, evidence standard, knowledge sources, prompt policy, escalation, risk, versioning
- **Prompt Enhancer:** Enhance user prompt before sending to model
- **Memory:** Conversation memory (short-term per session, future long-term optional with consent)
- **Wallet/Credit Billing:** Check balance, deduct credits idempotently (request ID), ledger entry, insufficient → error
- **RAG Attachment:** Optional doc context for research persona, citation required
- **Safety/Risk Controls:** No medical/legal/psych diagnosis, escalation to professional, NSFW filter for image, consent gate for character, spam filter for Telegram
- **Versioning:** Prompt version, model version logged per response
- **Audit Logs:** user_id, agent_id, persona_id, prompt hash, response hash, model, tokens, cost, timestamp
- **Telegram Channel Integration:** Concept - user creates Telegram bot, provides token encrypted, sets webhook to platform
- **API Access Concept:** Developer creates API key (hashed, prefix shown once), uses X-API-Key header, rate limit, credit check, logs

## Wallet Integration Concept (Not Built Now)

```
User → Chat request → Check wallet balance → Deduct credits (atomic, idempotent) → Call LLM → Log tokens/cost → Return response → Audit log
If insufficient → 402 Payment Required with message to buy credits
```

## Safety First

- All high-risk persona changes require HUMAN_APPROVAL_GATES
- No persona claims medical/legal/psych authority
- Image NSFW blocked
- Character deepfake of real person requires consent checkbox + human review flag

See sub-docs for each runtime architecture.
