# AGENT RUNBOOK

**Date:** 2026-07-19

## Purpose
How to run, monitor, pause, disable agents (project-building L2 and future L3).

## Project-Building L2 External Agents (Current)

### How to Run

- Research Agent: Provide issue with research question, attach relevant docs, ask for report with sources
- Fullstack Builder: Provide issue with acceptance criteria + relevant phase doc, ask to create branch + PR draft

### How to Monitor

- GitHub: Check branches `feat/*`, PRs with label `agent-task`
- PR description must include tools used, cost, approval needed

### How to Pause/Disable

- Stop assigning issues to that agent type
- Remove label `agent-*`
- No API key to revoke (external tool is founder's account)

### Troubleshooting

- If agent produces broken code: Request fix in same PR, or close PR and create new issue
- If agent adds secret: Immediately rotate secret, remove commit via revert (not history rewrite), add to .gitignore, scan with gitleaks

## Future L3 Internal Agents (Not Built Now)

### Example: SEO Technical Agent (L3 draft-only)

- **Run:** Scheduled daily 2am via cron or Celery beat
- **Scope:** Read-only crawl site, produce report `reports/seo_2026-07-19.md` draft
- **Permissions:** Read site, write draft report to `reports/` folder in branch or draft CMS, not publish
- **Monitoring:** Check logs in `agent_audit_logs` table, check report created
- **Pause:** Disable Celery beat schedule or revoke API key with scope seo:read
- **Kill Switch:** Set env `ENABLE_SEO_AGENT=False` or revoke key
- **Rollback:** Delete draft report, revert branch if needed

### General L3 Runbook

- **Enable:** Set env flag true + create scoped API key + schedule
- **Disable:** Set flag false + revoke key
- **Logs:** Check audit logs table
- **Approval:** Any publish, spend, contact, pricing, config change must go via approval issue

## Safety

- All L3 agents start as read-only or draft-only
- No auto-publish, no auto-spend, no auto-contact
- Human approval required per HUMAN_APPROVAL_GATES
