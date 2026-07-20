---
name: Agent Task
about: Task for project-building external agent (coding, research, SEO, etc.)
title: "[Agent Task] "
labels: ["agent-task", "needs-human-approval"]
assignees: []
---

## Agent ID
e.g., fullstack_builder, seo_content, research, etc.

## Purpose
What should agent do?

## Task Description
Detailed description from backlog.

## Inputs
- docs/vision/PRODUCT_VISION.md
- docs/roadmap/...
- docs/agents/...
- Existing code (read-only)

## Outputs Expected
- Branch name: `type/short-description`
- PR with description format from EXTERNAL_AGENT_WORKFLOW.md
- Or markdown report

## Acceptance Criteria
- [ ] Criteria from backlog
- [ ] No secrets
- [ ] No direct main commit, no force-push
- [ ] Tests pass if code
- [ ] Report includes: what, tools, cost, approval needed, risks, rollback

## Phase Label
phase-0, phase-1, etc.

## Risk Level
Low/Medium/High

## Approval Required
- [ ] Publishing public content
- [ ] Spending money (all spending in Phase 0 needs approval)
- [ ] Contacting customers
- [ ] Changing prices/config
- [ ] Merging/Deploying
- [ ] API keys
- [ ] Persona sensitive edits

## Rollback Plan
How to rollback.

## Notes
