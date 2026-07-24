# Third-Party Agent Review

**Version:** v0.1.0

**Date:** 2026-07-24

**Status:** Draft - Structure Only

**Document Owner:** Security Architect / Product

**Purpose:** Define security review of ready-made Agents, repository and source
verification, license review, dependency and supply-chain scanning, static and
dynamic analysis, prompt injection testing, remediation before approval, version
review and revocation.

**Note:** This is a structure-only stub. Final review policy will be completed
later.

## Purpose

Define how third-party and marketplace agents are reviewed before approval.

## In Scope

- Security review of ready-made Agents:
  - Business agents, Telegram agents, research agents, studio workflows,
    future marketplace agents
- Repository and source verification:
  - Source code provenance, commit history, publisher authority
  - Geographic/jurisdiction applicability
- License review:
  - MIT, Apache, proprietary, compatibility, public domain, licensed, purchased
    with appropriate usage rights, legally authorized
- Dependency and supply-chain scanning:
  - Direct and transitive dependencies, known vulnerabilities, typosquatting,
    malicious packages
- Static and dynamic analysis:
  - Code quality, secret scanning, injection flaws, permission overreach,
    data exfiltration
- Prompt injection testing:
  - Direct/indirect injection, jailbreak, tool abuse, RAG poisoning,
    system-prompt disclosure, citation integrity
- Remediation before approval:
  - Issues must be fixed, re-scanned, expert review, owner approval before
    publishing
- Version review and revocation:
  - knowledge_pack_version, knowledge_pack_reviewed_at,
    knowledge_pack_expires_at, expert_review_required, expert_review_status,
    versioned and removable sources, revocation on compromise

## Out of Scope

- Final checklist and exact scanning tools (future PRs)
- Marketplace business logic (future Phase 8)
- Implementation code

## Related Documents

- Security Index: [README.md](README.md)
- Agent Security Model: [AGENT_SECURITY_MODEL.md](AGENT_SECURITY_MODEL.md)
- Human Approval Gates: [../agents/HUMAN_APPROVAL_GATES.md](../agents/HUMAN_APPROVAL_GATES.md)
- Source Quality Policy: [../research/SOURCE_QUALITY_POLICY.md](../research/SOURCE_QUALITY_POLICY.md)

## Open Decisions

- Scanning toolset and CI integration
- Review SLA and approver roles
- Revocation criteria and communication
- Owner approval required

## Planned Completion Stage

Phase 2 - Marketplace Prep

## Status Note

Draft - Structure Only. Will be completed later.
