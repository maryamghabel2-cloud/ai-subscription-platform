# Phase 0 - Foundation

**Phase:** PHASE_0_FOUNDATION  
**Date:** 2026-07-19  
**Status:** Planned (Phase 0 is current)

## Objective
Create complete planning structure so solo founder can coordinate external agents safely.

## In Scope
- Product vision, business model, user personas
- Master roadmap + 9 phase docs (this set)
- Agent Operating System, Registry, Maturity, Permissions, Control Tower
- Project-building agent specs (20 agents)
- Runtime agent overview + architectures (5)
- Persona framework, template, registry schema, backlog, pipeline, QA/red teaming
- Growth, SEO, content engine, launch, experiment backlog, referral, social, landing
- Website IA + 6 page requirement docs
- Ops: GitHub workflow, branching, labels, milestones, DoD, release, runbook, reporting
- Backlog: Epics + 7 phase/area issue files
- GitHub templates: 7 issue templates + PR template
- README update to reflect new platform
- No production code, no secrets, no deploy

## Out of Scope
- Real payment, real AI inference, production build, shared-account resale, crypto, procurement agents, Persian UI full translation

## Dependencies
None - this is first

## Technical Deliverables
- docs/ folder structure
- .github/ISSUE_TEMPLATE + pull_request_template
- All docs linked, no secrets

## UX Deliverables
- README explains roadmap
- Website IA defined (not built)

## Business Deliverables
- Business model draft
- Growth system draft
- Unit economics tracking plan

## Required Agents
Orchestrator, Product Manager, Research, Compliance/Risk, Growth Marketing, SEO Content

## Test Requirements
- Documentation coherence check
- No secrets scan (gitleaks manual)
- All phase docs have required sections

## Risk Controls
- Scope creep → enforce HARD RULES
- Claiming authority for medical/legal → use evidence-based framing
- Unsafe autonomy → require HUMAN_APPROVAL_GATES
- All human approval gates from HUMAN_APPROVAL_GATES.md must apply: spending money, publishing, contacting customers, changing prices/config, merging, deploying, API keys, persona changes, paid campaigns, refunds/credits above threshold require human approval.
- Audit logs required for all state-changing actions.
- No medical/legal/psychological authoritative claims.

## Exit Criteria
- Branch docs/phase-0-agent-operating-system pushed
- PR titled 'docs: define phase 0 roadmap and agent operating system' opened, not merged
- All files listed in deliverables exist
