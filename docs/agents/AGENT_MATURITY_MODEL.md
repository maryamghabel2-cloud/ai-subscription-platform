# AGENT MATURITY MODEL

**Date:** 2026-07-19

## Levels

### L0 Manual
- Human does task, no agent.
- Use when: discovery, judgment, compliance decision.
- Example: Founder writes vision.

### L1 Prompt-Driven External Agent
- Founder uses external chat agent (ChatGPT, Claude) with prompt, gets advice/text, manually copies.
- No tool access.
- Use: Research question, prompt draft, idea.
- Approval: Human reviews output before using.

### L2 Semi-Automated External Agent With PR/Report Output
- Current primary for Phase 0-2.
- External coding agent (e.g., Cursor, Copilot, coding model) produces file change or report, opens PR or provides markdown report.
- Tools: GitHub, file write in branch, research browsing, but **not** connected to production, not spending money, not publishing.
- Human approval: Required for merge, deploy, publish, spend.
- Example: Fullstack Builder Agent outputs backend auth files in branch `mvp/v1-core-foundation`, opens PR, founder reviews.

### L3 Internal API-Connected Agent
- Future (Phase 3+).
- Agent has API key with limited scope (read-only or draft-create) to internal system (e.g., SEO crawler that reads site, creates draft blog post in draft state).
- Permissions: Allowed read, allowed draft-create, forbidden publish/delete/spend.
- Human approval: Required to publish draft, to escalate permissions.
- Audit logs + rollback required.

### L4 Autonomous Agent With Strict Human Approval Gates
- Future idea, not in Phase 0.
- Agent runs on schedule (e.g., daily growth report), has narrow scope, e.g., generate experiment report and post to Slack draft channel.
- **Never** autonomous for: spending, publishing public content, contacting customers, changing prices/config, merging, deploying, API keys, persona legal/medical changes, campaigns, refunds above threshold.
- Requires: approval gate UI, audit log, kill switch, rollback plan, rate limits.

## Maturity Progression

Project-building agents start L1/L2 now. Some may become L3 draft-only later (e.g., SEO content → draft blog). Runtime product agents start L2/L3 but with human approval for persona modifications.

## Checklist to Move L2→L3
- Permissions defined in AGENT_PERMISSION_MODEL
- Approval gates implemented
- Audit logging implemented
- Rollback documented
- Human approval UI exists
- Risk review by Compliance/Risk agent + founder
- Tests for forbidden actions blocking
