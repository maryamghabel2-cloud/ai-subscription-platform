# AGENT CONTROL TOWER

**Date:** 2026-07-19
**Purpose:** Observability for all agent activity - project-building and future runtime/internal.

## What Control Tower Does (Phase 0 Doc, Future Build)

Phase 0: Manual checklist + GitHub labels + docs.
Future: Dashboard.

### Registry
- Single source: AGENT_REGISTRY.md
- Each agent has ID, status, maturity, owner, permissions

### Logs
- Project-building external agents: Log via PR description + report footer: agent ID, tools used, inputs, outputs, tokens/cost, approval needed, risk flags
- Future internal L3: Store in DB `agent_audit_logs`: agent_id, action, target, payload hash, approver, timestamp, result, rollback id

### Monitoring
- GitHub: Track branch `docs/phase-0-*`, `mvp/*`, label `agent-task`, `needs-human-approval`
- Future: Metrics - agent runs, approval wait time, rejection rate, cost

### Kill Switch
- For L3/L4 future: Ability to disable agent API key, pause schedule, revert last change
- Documented in AGENT_RUNBOOK.md

### Reporting Cadence
- Weekly: Execution Coach + Orchestrator report: what agents did, what's pending approval, blockers
- See REPORTING_CADENCE.md

## Phase 0 Implementation (Now)
- Manual: founder reviews PRs with label `agent-task`
- Use HUMAN_APPROVAL_GATES.md checklist before merge/deploy/publish

## Future Implementation (Not Now)
- Not building control tower UI in Phase 0
- Placeholder for Phase 4+ platform's admin view (no admin dashboard in Phase 1 per scope limits)

## Safety Integration
- All approval-required actions must create GitHub issue with template `agent_task.md` and label `needs-human-approval`
- No auto-merge, no auto-deploy
