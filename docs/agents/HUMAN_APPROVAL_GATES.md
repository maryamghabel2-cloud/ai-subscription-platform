# HUMAN APPROVAL GATES

**Date:** 2026-07-19
**Status:** Mandatory for all agents L1-L4

## Rule
Any action that does any of the following **must** require explicit human approval (founder) before execution:

1. Publishing public content (blog post, social media post, landing page update, docs site update, public GitHub release notes that are marketing-facing)
2. Spending money (API costs beyond zero budget, ad spend, supplier purchase, hiring external agent that costs, credit issuance above threshold)
3. Contacting customers (email reply, Telegram DM, support ticket that sends external message, sales outreach)
4. Sending bulk messages (newsletter, Telegram broadcast, SMS)
5. Changing prices, credit costs, wallet logic, pricing page
6. Changing production configuration (env vars, feature flags, database schema in prod, infrastructure)
7. Merging PRs
8. Deploying to production (including staging that user can see)
9. Creating/deleting API keys (user-facing or internal)
10. Modifying legal/medical/psychological personas (prompts, knowledge sources, disclaimers, escalation behavior)
11. Launching paid campaigns (Google Ads, social ads)
12. Issuing refunds or credits above threshold (founder sets threshold, e.g., > $5 / 500k IRR)
13. Creating new agent type or escalating maturity L2→L3 or L3→L4
14. Deleting data, revoking access, banning users
15. Bypassing provider ToS, geographic, KYC checks

## How Approval Works (Phase 0 Manual)

- Agent creates GitHub issue with label `needs-human-approval` and template `agent_task.md`
- In PR description, section “Approval Required: …”
- Founder comments “Approved” or requests changes
- No auto-merge - founder merges manually after approval

## Future Approval UI (Not Built Now)

- Future Control Tower dashboard will have approval queue
- But Phase 0-2 is manual GitHub

## Evidence Required for Approval

- What changed, why, risk assessment, cost, rollback plan
- For persona changes: research sources, red team results, disclaimer
- For spending: amount, budget, ROI estimate
- For publishing: draft content, SEO checklist, brand voice check

## Audit
- All approvals logged: who approved, when, what

## Zero Exceptions
- No agent may self-approve
- No L4 autonomous agent may bypass even if marked L4 - gates still apply
