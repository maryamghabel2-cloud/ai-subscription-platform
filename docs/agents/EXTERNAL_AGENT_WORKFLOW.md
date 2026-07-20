# EXTERNAL AGENT WORKFLOW

**Date:** 2026-07-19
**Purpose:** How founder uses external agents (coding, research, etc.) today safely.

## Workflow (L2 - Current)

1. **Define Task**
   - Founder creates GitHub issue using one of templates: feature_request, persona_design, research_task, agent_task, growth_experiment, seo_content_task, bug_report
   - Add labels: `phase-0`, `agent-task`, relevant agent label e.g., `agent-fullstack`
   - Fill: purpose, owner agent type, inputs, outputs expected, acceptance criteria, risk level

2. **Assign External Agent**
   - Example: For code task, use Fullstack Builder external agent (e.g., Cursor, Claude Code)
   - Provide prompt from agent spec file in `docs/agents/project/*.md` → “Example prompt for external use”
   - Attach relevant docs: PRODUCT_VISION, relevant phase doc, permission model

3. **Agent Produces Output**
   - Expected: Branch with changes (e.g., `feat/auth`) OR markdown report in `docs/` or `research/` folder
   - Must include: what was done, tools used, cost, approval needed, risks, rollback notes
   - Must NOT: commit to main, spend money without approval, publish content, contact customers, add secrets

4. **Human Review**
   - Founder reviews PR diff, report, checks against Acceptance Criteria
   - Uses HUMAN_APPROVAL_GATES.md checklist
   - If approval-required actions present, create approval issue

5. **Approval Gate**
   - For publishing, spending, contacting, pricing, config, merge, deploy, API keys, persona sensitive edits: require explicit human approval (comment “Approved”)
   - No auto-merge

6. **Merge / Publish**
   - Founder merges PR after approval
   - If content publishing (blog, social draft), founder publishes manually

7. **Log**
   - Add entry to reporting cadence doc or weekly report

## Tools External Agents May Use Now
- GitHub (read, write branch, open PR draft)
- Local file system (branch)
- Web search (research agents)
- LLM APIs with pre-approved budget cap (founder sets)

## Tools They May Use Later (L3)
- Internal API with scoped key (read, draft-create)
- Draft CMS (not publish)
- Read-only analytics

## Forbidden Now
- Direct main commit, force-push, deleting history
- Spending money beyond $0 without approval (all spending needs approval in Phase 0)
- Publishing, bulk messaging, contacting customers

## Example Final Report Format (Must be in Agent PR/Report)

```
## Agent: Fullstack Builder
## Task: Build auth endpoints
## Inputs: docs/roadmap/PHASE_1_CORE_MVP.md, PRODUCT_VISION
## Outputs: backend/app/api/auth.py, tests, PR #x
## Tools Used: GitHub branch, Python, FastAPI
## Cost: 150k tokens (~$0.30)
## Approval Needed: Merge PR
## Risks: None
## Rollback: git revert <sha>
## Tests: pytest passed
## Next: QA/Security agent review
```

See each `docs/agents/project/*.md` for example prompt.
