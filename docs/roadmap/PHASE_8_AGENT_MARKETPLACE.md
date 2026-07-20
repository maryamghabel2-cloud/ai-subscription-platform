# Phase 8 - Agent Marketplace (Future Idea)

**Phase:** PHASE_8_AGENT_MARKETPLACE  
**Date:** 2026-07-19  
**Status:** Planned (Phase 0 is current)

## Objective
Future marketplace where users can publish/share business agents (with review).

## In Scope
Idea only - not built now. Doc defines concept, revenue share idea, review process idea.

## Out of Scope
Everything - this is future concept, not implemented in Phase 0-7

## Dependencies
All previous phases + strong moderation + compliance

## Technical Deliverables
- Concept: agent card, version, permissions manifest, approval flow
- No code in Phase 0

## UX Deliverables
- Concept page: directory idea

## Business Deliverables
- Idea: rev-share 70/30, review + human approval for marketplace listing

## Required Agents
Product Manager, Compliance Risk, Finance Unit Economics, Orchestrator

## Test Requirements
No tests - concept only

## Risk Controls
- Unsafe agents → must have approval gates + audit + rollback
- IP/legal → compliance review before any marketplace
- All human approval gates from HUMAN_APPROVAL_GATES.md must apply: spending money, publishing, contacting customers, changing prices/config, merging, deploying, API keys, persona changes, paid campaigns, refunds/credits above threshold require human approval.
- Audit logs required for all state-changing actions.
- No medical/legal/psychological authoritative claims.

## Exit Criteria
Concept doc exists, no code, clearly marked Future Idea
