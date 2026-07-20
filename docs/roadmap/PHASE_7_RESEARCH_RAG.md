# Phase 7 - Research & RAG

**Phase:** PHASE_7_RESEARCH_RAG  
**Date:** 2026-07-19  
**Status:** Planned (Phase 0 is current)

## Objective
Upload docs, RAG attachment, citations, research workflow.

## In Scope
- Upload PDF/docs
- RAG: embeddings, vector store (pgvector for MVP)
- Research persona with citations
- RAG attachment to chat

## Out of Scope
Training custom LLM, claiming authoritative research without sources

## Dependencies
Phase 2 persona framework, Phase 4 API embeddings

## Technical Deliverables
- Document model, chunk model, embedding model wrapper
- pgvector extension
- RAG retrieval: top-k with scores, citation IDs
- API: /research/upload, /research/query

## UX Deliverables
- Research Studio: upload, ask with sources
- Citation display

## Business Deliverables
- RAG as premium credit cost

## Required Agents
ML Inference Engineer, Model Evaluation, Trust & Safety, Data Privacy Governance, Localization & Accessibility + existing
RAG Knowledge, Research, Prompt Engineer, Fullstack Builder


**Additional per review (new 8 agents):** ML Inference Engineer, Model Evaluation, Trust & Safety, Data Privacy Governance, Localization & Accessibility

## Test Requirements
- Upload PDF, query → returns cited chunks
- No hallucinated citations → test with known doc
- Data deletion deletes vectors

## Risk Controls
- Privacy → doc private to user, no cross-tenant leakage test
- Hallucination → require citations
- All human approval gates from HUMAN_APPROVAL_GATES.md must apply: spending money, publishing, contacting customers, changing prices/config, merging, deploying, API keys, persona changes, paid campaigns, refunds/credits above threshold require human approval.
- Audit logs required for all state-changing actions.
- No medical/legal/psychological authoritative claims.

## Exit Criteria
User can upload doc and ask questions getting cited answers