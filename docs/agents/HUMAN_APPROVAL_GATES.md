# HUMAN APPROVAL GATES

**Date:** 2026-07-19  
**Updated:** 2026-07-20 - Added ABSOLUTELY FORBIDDEN section  
**Status:** Mandatory for all agents L1-L4

## Rule - Approval Required
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

## ABSOLUTELY FORBIDDEN / NO-GO ACTIONS

The following actions are **never allowed** and **no human approval may authorize these actions**. They must never be performed by any agent at any maturity level (L1-L4), even if a human explicitly requests them. If encountered in an issue or prompt, agent must refuse and report via compliance channel.

1. **Bypassing provider Terms of Service** - Scraping, circumventing rate limits, using unofficial APIs that violate ToS, reselling services in violation of provider ToS
2. **Bypassing geographic restrictions** - Using VPNs, proxies, fake locations, or regional pricing tricks to evade provider geo-blocks
3. **Bypassing sanctions** - Facilitating access for sanctioned regions, evading export controls, or obscuring end-user jurisdiction to violate sanctions
4. **Bypassing KYC** - Creating fake accounts, bypassing identity verification, using synthetic identities to circumvent KYC/AML
5. **Using fake identities** - Synthetic personas, stolen identities, fake documents, impersonation of real persons without consent
6. **Hiding prohibited end-user locations** - Obscuring IP, location, jurisdiction to hide that user is in prohibited region
7. **Sharing or reselling unauthorized credentials or raw supplier keys** - Sharing raw supplier API keys, reselling credentials that are not authorized for resale, distributing supplier secrets, shared consumer accounts (Netflix, ChatGPT shared), API-key resale violating provider ToS
8. **Generating or facilitating CSAM, non-consensual intimate imagery, or deepfake of real persons without explicit consent**
9. **Claiming medical, legal, or psychological professional authority, diagnosis, verdict, or therapy**

**Statement:** No human approval may authorize these actions. If task requires any of these, agent must stop, document why it is forbidden, and escalate to Compliance/Risk agent and founder for alternative compliant approach.

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
- All forbidden action attempts logged as blocked + reported

## Zero Exceptions for Approval Gates

- No agent may self-approve
- No L4 autonomous agent may bypass approval gates even if marked L4
- Forbidden actions have no approval path - they are NO-GO

## Enforcement

- QA Security Agent must check PRs for forbidden patterns
- Compliance/Risk Agent must review High-risk persona changes and any task mentioning ToS, geographic, sanctions, KYC, identities, credentials
- If forbidden action detected, PR must be closed without merge
