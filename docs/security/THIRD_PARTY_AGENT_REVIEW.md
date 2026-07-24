# Third-Party Agent Review

**Purpose:** Define review process for third-party agents, marketplace agents, and external integrations.

**Status:** Draft - Structure Only

**Note:** This is a structure-only stub. Final third-party agent review policy will be completed in later PRs.

## Scope

This document will cover:

- Definitions: third-party agents, marketplace agents, business agents, Telegram agents, research agents
- Submission requirements: id, version, display names, description, category, permissions, tools, budget policy, safety profile, audit_required, rollback_plan
- Security review checklist: permissions, forbidden actions, data access, external API calls, prompt injection resistance, secret handling, compliance with ToS
- Privacy review: data classification, retention, no secret sharing
- Business review: pricing, rev-share, support, documentation
- Approval gates: human approval required for publishing, spending, contacting customers
- Monitoring: post-publication monitoring, auto-pause on abuse, revocation
- Absolutely forbidden: ToS bypass, geographic/KYC bypass, sharing unauthorized credentials, CSAM, non-consensual imagery

Final policy will require security, product-owner, and legal review.

## Linkage

- Security Index: [README.md](README.md)
- Agent Security Model: [AGENT_SECURITY_MODEL.md](AGENT_SECURITY_MODEL.md)
- Human Approval Gates: [../agents/HUMAN_APPROVAL_GATES.md](../agents/HUMAN_APPROVAL_GATES.md)

## Status

Draft - Structure Only. Will be completed later.
