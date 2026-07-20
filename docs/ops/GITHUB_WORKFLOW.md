# GITHUB WORKFLOW

**Date:** 2026-07-19

## Branching

- See BRANCHING_STRATEGY.md
- main protected, no direct commits, PRs require review (founder review in solo case = checklist)
- Feature branches: feat/..., fix/..., docs/..., chore/...

## PR Process

1. Create issue from template (feature_request, persona_design, etc.)
2. Add labels: phase-0, agent-*, needs-human-approval if needed
3. Create branch from main: `feat/auth` or `docs/phase-0-...`
4. External agent (L2) writes code in branch, opens PR draft with description format from EXTERNAL_AGENT_WORKFLOW.md
5. Checklist in PR template must be filled
6. Human approval gates checked (see HUMAN_APPROVAL_GATES.md)
7. QA Security agent review (if applicable)
8. Founder approves via comment, merges manually
9. No auto-merge, no auto-deploy

## Labels

See GITHUB_LABELS.md

## Milestones

See MILESTONE_PLAN.md - Phase 0, Phase 1, etc.

## Issues

- Use templates in .github/ISSUE_TEMPLATE
- Each issue must have: title, purpose, owner agent type, dependencies, acceptance criteria, priority, phase label, risk level

## Secrets

- No secrets in repo
- Use .env.example with placeholders
- gitleaks pre-commit hook recommended (future)

## CI (Future, Not Built Now)

- For Phase 1: GitHub Actions with pytest, npm build, gitleaks
- Not in Phase 0

## Control Tower

- PRs with label `agent-task` tracked
- PRs with label `needs-human-approval` need founder review before merge
