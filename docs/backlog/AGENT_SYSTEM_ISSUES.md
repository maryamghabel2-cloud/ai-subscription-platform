# AGENT SYSTEM ISSUES

**Milestone:** Phase 0 Foundation

## ISSUE-AGENT-01: Define Agent OS Docs

- **Title:** Create 7 agent OS docs
- **Purpose:** Safe agent coordination
- **Owner:** Product Manager
- **Dependencies:** None
- **Acceptance:** 7 docs exist, explain 3 types, L0-L4, permission model, approval gates list 15 items, control tower concept
- **Priority:** P0
- **Phase:** phase-0
- **Risk:** Medium

## ISSUE-AGENT-02: Project-Building Agent Specs

- **Title:** 20 agent specs
- **Purpose:** How to use external agents now
- **Owner:** Orchestrator
- **Dependencies:** AGENT-01
- **Acceptance:** 20 files, each has purpose, when to use, phase, inputs, outputs, tools now/later, permissions, forbidden, approval-required, success metrics, example prompt, report format
- **Priority:** P0
- **Phase:** phase-0
- **Risk:** Low

## ISSUE-AGENT-03: Runtime Agent Architectures

- **Title:** 5 runtime architecture docs
- **Purpose:** Future product agents
- **Owner:** Product Manager
- **Dependencies:** AGENT-01
- **Acceptance:** 5 files, explain difference vs project-building, persona system, wallet, RAG, safety, versioning, Telegram, API
- **Priority:** P1
- **Phase:** phase-0
- **Risk:** Low

## ISSUE-AGENT-04: Agent Control Tower Spec

- **Title:** Control tower observability doc + runbook + reporting cadence
- **Purpose:** Monitor agents
- **Owner:** Orchestrator + DevOps
- **Dependencies:** AGENT-01
- **Acceptance:** Control tower doc explains registry, logs, monitoring, kill switch, reporting cadence weekly
- **Priority:** P1
- **Phase:** phase-0
- **Risk:** Low

## ISSUE-AGENT-05: Human Approval Gates Implementation Plan

- **Title:** Approval gates doc + GitHub label workflow
- **Purpose:** Prevent unsafe autonomy
- **Owner:** Compliance Risk
- **Dependencies:** AGENT-01
- **Acceptance:** HUMAN_APPROVAL_GATES lists 15 actions requiring approval, manual GitHub approval via comment, no auto-merge, future UI concept
- **Priority:** P0
- **Phase:** phase-0
- **Risk:** High
