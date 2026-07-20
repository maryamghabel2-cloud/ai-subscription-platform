# AGENT PERMISSION MODEL

**Date:** 2026-07-19

## Principles
- Least privilege
- Draft-first, not publish-first
- Human approval for any money, publishing, customer contact, pricing/config, merge/deploy, API keys, persona sensitive edits, campaigns, refunds > threshold

## Permission Categories

### Allowed Actions (No approval needed, but logged)
- Read docs, read code in branch, read GitHub issues (read-only)
- Generate markdown report, generate code diff in **feature branch only** (not main)
- Propose prompt improvements in draft file
- Analyze data locally, produce charts in report
- Research browsing (no auto-purchase)
- Run tests locally

### Forbidden Actions (Never allowed, even with approval via autonomous)
- Direct commit to main
- Force-push, history rewrite, delete files without archive
- Spend money (API costs beyond pre-approved budget, ad spend, supplier purchase)
- Publish public content (blog, social, docs site live, landing page live) without review
- Contact customers (email, Telegram bulk)
- Delete production data
- Create/delete API keys in production without approval
- Bypass geographic, KYC, or provider ToS restrictions
- Claim medical/legal/psychological authority
- Generate NSFW/violent/illegal content

### Approval-Required Actions (Require Human Approval Gate)
- Publishing public content (blog, social, landing, docs)
- Spending money (any amount - even small requires approval in Phase 0)
- Contacting customers (support reply, sales outreach, bulk messages)
- Sending bulk messages (email, Telegram)
- Changing prices, credit costs, wallet logic
- Changing production configuration (env, feature flags)
- Merging PRs
- Deploying to production (or staging that affects users)
- Creating/deleting API keys
- Modifying legal/medical/psychological personas (prompts, knowledge sources)
- Launching paid campaigns (ads)
- Issuing refunds or credits above threshold (e.g., > $5 or > 500k IRR - founder sets)
- Creating new agent or escalating maturity L2→L3 or L3→L4

## Audit Logging Requirements
- Who (agent ID + human approver)
- What (action, payload, target)
- When (timestamp)
- Result (success/failure)
- Rollback reference
- Store in append-only log (future: DB table agent_audit_logs)

## Rollback Requirements
- For any state-changing action in draft→pending approval, must include rollback steps in PR/report:
  - How to revert file change (git revert)
  - How to revert price change
  - How to revoke API key
  - How to unpublish content

## Tool-Specific Permissions

| Tool | Allowed Now (L1/L2) | Allowed Later (L3) | Notes |
|---|---|---|---|
| GitHub read | Yes | Yes | Read issues/PRs |
| GitHub write branch | Yes (feature branch) | Yes (feature) | Never main directly |
| GitHub merge | No | No | Human only |
| File write | Branch only | Branch + draft content folder | Never prod config without approval |
| Web search | Yes | Yes | Research agents |
| External API (OpenAI etc) | Yes with budget cap | Yes with scoped key, read/draft | No spend without approval |
| Deploy | No | No | Human only |
| Email/Telegram send | No | No (draft only) | Human sends |
| Payment/billing | No | No (read-only report) | Human approves |
| Publishing CMS | No | Draft only | Human publishes |

## Persona-Specific Additional
- Medical/Legal/Psych personas: All prompt changes require Compliance/Risk review + founder approval + QA red teaming (see PERSONA_QA_AND_RED_TEAMING.md)
