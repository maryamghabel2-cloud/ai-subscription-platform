# BUSINESS AGENT ARCHITECTURE

**Date:** 2026-07-19  
**Phase:** 6

## Purpose
Business agents help shop owners automate FAQ, lead qualification, content drafting.

## Types

- FAQ Agent: Answers common questions from knowledge base (products, shipping)
- Lead Qualifier: Asks 3-4 questions, scores lead
- Instagram Content Drafter: Drafts captions/hashtags (draft-only, human publishes)

## Architecture

- **Config:** Business agent config = {persona_id, knowledge_sources (FAQ docs), tools (none in Phase 6 MVP), approval gates}
- **Execution:** Triggered via Telegram or web widget (future), logs execution
- **Permissions:** Draft content, not publish without approval; no bulk messaging without approval; no spending
- **Wallet:** Execution billed per run

## Safety

- No autonomous customer contact without approval for bulk
- Support draft replies: draft → human review → send (future L3)
- Audit logs: who triggered, input, output, time

## Telegram Integration Concept
- Business agent can be attached to Telegram bot (see TELEGRAM_AGENT_ARCHITECTURE)
- Token encrypted, webhook `POST /telegram/webhook/{agent_id}`

## Difference from Project-Building Business Agents
- Project-building Customer Success Agent drafts support replies for founder's business (internal)
- Runtime Business Agent is product feature for end-users' businesses
