# AGENT PERMISSION MODEL

**Date:** 2026-07-19  
**Updated:** 2026-07-20 - Added ABSOLUTELY FORBIDDEN section per review

## Principles
- Least privilege
- Draft-first, not publish-first
- Human approval for any money, publishing, customer contact, pricing/config, merge/deploy, API keys, persona sensitive edits, campaigns, refunds > threshold
- **No approval can authorize forbidden actions**

## Permission Categories

### Allowed Actions (No approval needed, but logged)
- Read docs, read code in branch, read GitHub issues (read-only)
- Generate markdown report, generate code diff in **feature branch only** (not main)
- Propose prompt improvements in draft file
- Analyze data locally, produce charts in report
- Research browsing (no auto-purchase)
- Run tests locally

### Forbidden Actions - General (Never allowed without approval path, but not in absolute NO-GO)
- Direct commit to main
- Force-push, history rewrite, delete files without archive
- Spend money (API costs beyond pre-approved budget, ad spend, supplier purchase)
- Publish public content (blog, social, docs site live, landing page live) without review
- Contact customers (email, Telegram bulk)
- Delete production data
- Create/delete API keys in production without approval
- Claim medical/legal/psychological authority
- Generate NSFW/violent/illegal content

### ABSOLUTELY FORBIDDEN / NO-GO ACTIONS (No Human Approval May Authorize)

The following are **absolutely forbidden** at any maturity level L1-L4. No human approval may authorize these actions. Agent must refuse and report.

1. **Bypassing provider Terms of Service** - Scraping that violates ToS, using unofficial APIs, circumventing rate limits or access controls, reselling in violation of ToS
2. **Bypassing geographic restrictions** - Using VPN/proxy/fake location to evade geo-blocks, regional pricing tricks
3. **Bypassing sanctions** - Facilitating access for sanctioned regions, obscuring jurisdiction to evade export controls or sanctions
4. **Bypassing KYC** - Fake accounts, synthetic identities, bypassing identity verification to evade KYC/AML
5. **Using fake identities** - Synthetic personas, stolen identities, fake documents, impersonation of real persons without explicit consent
6. **Hiding prohibited end-user locations** - Obscuring IP, location, jurisdiction to hide prohibited user location
7. **Sharing or reselling unauthorized credentials or raw supplier keys** - Sharing raw supplier API keys, reselling credentials not authorized for resale, distributing supplier secrets, shared consumer accounts (e.g., Netflix, ChatGPT shared), API-key resale violating provider ToS
8. **Generating CSAM, non-consensual intimate imagery, or deepfake of real person without explicit consent**
9. **Claiming professional authority, diagnosis, legal verdict, psychological therapy**

**Statement:** No human approval may authorize these actions. If task requires any, agent must stop, document refusal reason, and escalate to Compliance/Risk agent and founder.

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
- Modifying legal/medical/psychological personas (prompts, knowledge sources) - note: modifying to claim authority is forbidden, this is for legitimate evidence-based updates with approval
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
- Log blocked forbidden attempts as well

## Rollback Requirements
- For any state-changing action in draft→pending approval, must include rollback steps in PR/report:
  - How to revert file change (git revert)
  - How to revert price change
  - How to revoke API key
  - How to unpublish content
- Forbidden actions have no rollback path - they must never be executed

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
- Any attempt to make persona claim authority or bypass escalation is absolutely forbidden

## Enforcement
- QA Security Agent checks PRs for forbidden patterns (ToS bypass, geo bypass, sanctions, KYC, fake identity, credential sharing)
- Compliance/Risk reviews High-risk tasks
- If forbidden detected, PR closed without merge, reported
