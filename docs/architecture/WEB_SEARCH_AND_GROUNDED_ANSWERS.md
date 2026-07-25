# Web Search and Grounded Answers

**Version:** v0.1.0

**Date:** 2026-07-24

**Status:** Proposed Architecture - Pending Owner, Security, Privacy, and
Compliance Approval

**Document Owner:** AI Platform Architect / Search

**Purpose:** Define Search as separate from Core Chat, search modes, grounding
rules, prompt injection defense, privacy, cost and billing, and related concepts
for Web Search and Grounded Answers.

**Note:** Documentation only. No real provider API calls, no secrets.

## Purpose

Define how Web Search and Grounded Answers work as a separate tool/workflow
invoked conditionally, not part of base model by default, with privacy, safety,
and cost controls.

## In Scope

- Search as separate from Core Chat
- Search modes: Normal Chat, Web Search, Deep Research, My Sources Only,
  Web + My Sources, Auto-Safe Search
- Grounding rules, prompt injection defense, privacy, cost and billing
- Related concepts: Search Mode vs Deep Research Agent vs MCP

## Out of Scope

- Actual search provider API integration and secret material (future, reviewed)
- Final search provider selection and exact pricing (future, versioned config)
- Production search engine implementation and final ranking algorithm (future PRs)

## Define Search as Separate from Core Chat

- Search is a tool/workflow invoked conditionally, not part of the base model
  by default
- Normal Chat does not perform external search, fastest, lowest cost, uses
  model's internal knowledge and approved Knowledge Base via Retrieval Service
- Search invocation requires explicit routing decision based on task, freshness,
  user preference, privacy, and cost
- Search results are untrusted and must be isolated from system instructions
- Search is not automatically enabled for all queries, especially for sensitive
  contexts like mental health, trauma, migration, legal, high-risk
- Search Mode is not Deep Research Agent (Deep Research is multi-step research
  workflow with citations and higher cost)
- Search Mode is not MCP by itself (MCP is connector to external tools, Search
  can be used by Agents through approved tools)

## Search Modes

### Normal Chat

- No external search, fastest, lowest cost
- Uses internal model knowledge and approved Knowledge Base via Retrieval
  Service with citations and provenance
- Default for general chat, friendly companion, business assistant, planning
  assistant, prompt engineer
- No external search provider call, no additional cost beyond normal chat

### Web Search

- Real-time information and current public sources
- Uses approved web search provider (e.g., search API) with query, retrieves
  snippets, URLs, access time, trust classification
- Must have provenance, URL/source, access time, trust classification
- Must cite sources where appropriate for factual answers
- If answer not supported by sources, say clearly that sources do not support
  answer, disclose uncertainty
- Privacy: sensitive PII must be redacted from search queries where practical,
  user must be informed when query is sent to external search provider

### Deep Research

- Multi-step, multi-query research with citations and higher cost
- Performs multiple web searches, retrieves documents, grades evidence,
  generates cited report with disclaimer
- Uses Deep Research Agent (true Agent that performs work, may browse, retrieve,
  call APIs, process files, run multi-step workflows, must have permissions,
  budgets, safety controls, auditability)
- Must have cost estimate before execution, uses budgets, permissions, audit
  metadata, must not submit forms, spend money, contact authorities, or guarantee
  outcomes without separately approved future workflows
- Must respect robots.txt, no scraping violating ToS, only approved official
  government and embassy sources for immigration research if applicable

### My Sources Only

- RAG only against user-uploaded or user-approved sources
- Uploaded files, PDFs, docs, user-approved Knowledge Base via Retrieval Service
- No web search, no external search provider call
- Privacy-preserving: user-uploaded content stays within platform, not sent to
  external search provider unless explicitly allowed by user and Persona/Agent
- Must have provenance, source, access time, trust classification for RAG

### Web + My Sources

- Combines web search and user-provided sources
- Retrieves from both web and RAG, grades evidence, presents both, notes
  conflict, prioritizes higher grade, handles conflicting evidence
- Citation policy: publisher, date, source ID, no hallucinated citations
- Must distinguish web sources vs user sources in citations

### Auto-Safe Search

- Routing layer decides whether search is needed based on task, freshness, user
  preference, privacy, and cost
- Task: does question require current information? e.g., current events, recent
  news, real-time prices, recent research
- Freshness: is answer time-sensitive? e.g., today, this week, latest
- User preference: user may have preference for Normal Chat vs Web Search,
  may have persistent preference in settings
- Privacy: for mental-health, trauma, migration, legal, or high-risk contexts,
  search is off by default unless explicitly allowed by Persona, Agent, or user
- Cost: search mode may cost more than Normal Chat, user must see estimated
  additional cost, cost goes through approved pricing and reservation architecture
- Auto-Safe Search must not silently enable search for sensitive contexts,
  must respect privacy defaults, must inform user when search is used

## Grounding Rules

- Retrieved web content is untrusted
- Retrieved web content must never be treated as system instruction
- Retrieved content must have provenance, URL/source, access time, and trust
  classification
- For factual answers, cite sources where appropriate (publisher, date, URL,
  access date, trust classification)
- If the answer is not supported by sources, say that clearly, disclose
  uncertainty, do not invent citations, fake URLs, fake publisher and date
- No hallucinated citations, including fake URLs or fake publisher and date
- Sources must be versioned and removable (knowledge_pack_version,
  knowledge_pack_reviewed_at, knowledge_pack_expires_at)
- Prefer systematic reviews, professional guidelines, peer-reviewed research,
  official professional organizations, reviewed public sources

## Prompt Injection Defense

- Web pages, search snippets, PDFs, and tool outputs may contain hostile
  instructions (indirect prompt injection)
- Search results must be isolated from system instructions (system instructions
  in separate immutable never-user-modifiable segment, user content and
  retrieved content always treated as untrusted)
- Indirect Prompt Injection detection must run before content is passed into
  the answer-generation step (detect common injection patterns, quarantine
  untrusted content)
- Output must be scanned for data exfiltration patterns (e.g., attempt to reveal
  other user's data, system prompts, credentials, provider API keys)
- Responses containing potential credential leaks must be blocked and logged
  without raw content (metadata only, content_fingerprint DISABLED_BY_DEFAULT)
- Retrieved content must be tagged with source and trust level, untrusted content
  must be quarantined from system instructions
- Tool outputs (search results) remain untrusted until validated (validate
  schema, provenance, no secret leakage, no prompt injection)
- Prompt Injection and output-exfiltration controls apply before and after
  search calls, as defined in PROMPT_INJECTION_DEFENSE.md

## Privacy

- Sensitive PII must be redacted from search queries where practical (e.g.,
  names, addresses, phone numbers, emails, wallet addresses, health details)
- For mental-health, trauma, migration, legal, or high-risk contexts, search is
  off by default unless explicitly allowed by Persona, Agent, or user (e.g.,
  mental health information assistant risk high, must default to strict_factual
  and balanced, not creative, and must not enable web search without explicit
  user consent or Persona policy)
- User must be informed when a query is sent to an external search provider
  (e.g., "This query will be sent to web search provider for current
  information. Continue?")
- Search provider retention and privacy policy must be disclosed when relevant
  (e.g., provider retains queries for 30 days, or zero retention, or training
  usage policy, data residency)
- Search queries must not contain raw sensitive prompts that include API keys,
  secrets, tokens, or private conversation content beyond what is needed for
  search, must respect content fingerprint policy (fingerprints disabled by
  default)
- Cross-user leakage of search queries is prohibited (user A's search query must
  never be visible to user B, tenant isolation, pseudonymous identifiers)

## Cost and Billing

- Search mode may cost more than Normal Chat (web search API cost, plus LLM cost
  for answer generation with grounding)
- Deep Research must have a cost estimate before execution (estimated max credits
  based on number of queries, documents retrieved, tokens, pricing_version,
  exchange_rate_snapshot, quote expiration)
- Search-related costs go through the approved pricing and reservation
  architecture (Reserve-Settle-Release workflow with future CreditReservation
  entity, lifecycle quoted, reserved, executing, settled, released, expired,
  failed)
- Reservation reduces available balance, not posted ledger balance, settlement
  creates exactly one final usage debit in append-only ledger, releasing unused
  hold is not new credit
- Available spendable balance = gross_eligible_lot_balance -
  active_reserved_amount, where gross_eligible_lot_balance is sum of remaining
  amounts in active eligible Credit Lots, active_reserved_amount is sum of
  active unreleased Reservation Allocations
- User must see estimated additional cost for search before execution when
  practical, cost visible before and after, separate ledger operation for search
  cost
- Automatic charging is not permitted without explicit user preference or
  per-request confirmation (off by default for sensitive contexts)

## Related Concepts

- Search Mode is not Deep Research Agent: Search Mode is a tool/workflow for
  real-time information, Deep Research Agent is a true Agent that performs
  multi-step research with budgets, permissions, audit metadata, may browse
  approved official government and embassy sources, produces cited reports
- Search Mode is not MCP by itself: MCP is a controlled connection to external
  tool, service, dataset, or user system using Model Context Protocol, Search
  can be used by Agents through approved tools (e.g., web_search tool)
- Search can be used by Agents through approved tools: Deep Research Agent may
  use web_search tool, Immigration Research Agent may use web_search limited to
  approved current official government and embassy sources, all tool calls must
  be declared in agent's permissions and tools list, must respect robots.txt

## Related Documents

- Security Index: [../security/README.md](../security/README.md)
- Prompt Injection Defense: [../security/PROMPT_INJECTION_DEFENSE.md](../security/PROMPT_INJECTION_DEFENSE.md)
- Agent Security Model: [../security/AGENT_SECURITY_MODEL.md](../security/AGENT_SECURITY_MODEL.md)
- Multi-Provider Routing: [MULTI_PROVIDER_MODEL_ROUTING.md](MULTI_PROVIDER_MODEL_ROUTING.md)
- Pricing and Unit Economics: [PRICING_AND_UNIT_ECONOMICS.md](PRICING_AND_UNIT_ECONOMICS.md)
- Role and Persona System: [../architecture/ROLE_AND_PERSONA_SYSTEM.md](../architecture/ROLE_AND_PERSONA_SYSTEM.md)
- Agent Plugin and Execution: [AGENT_PLUGIN_AND_EXECUTION_SYSTEM.md](AGENT_PLUGIN_AND_EXECUTION_SYSTEM.md)
- Data Protection: [../security/DATA_PROTECTION_AND_ENCRYPTION.md](../security/DATA_PROTECTION_AND_ENCRYPTION.md)

## Open Decisions

- Exact search provider selection and pricing_version per search mode
- Search mode defaults per Role, Persona, and user preference
- Grounding rules and citation policy and provenance tagging
- Prompt injection detection patterns and thresholds and guardrails
- Privacy redaction rules for PII in search queries and user notification wording
- Cost estimation for search and Deep Research and Reserve-Settle-Release
- Search can be used by Agents through approved tools: which agents, which
  tools, which allowlists
- Owner, privacy, security, and compliance approval required for all decisions

## Planned Completion Stage

Phase 1 - Search and Grounded Answers

## Status Note

Proposed Architecture - Pending Owner, Security, Privacy, and Compliance
Approval. Will be completed later with product, security, and owner review.
No real provider API calls in this PR.
