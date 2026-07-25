# Security Testing

**Version:** v0.1.0

**Date:** 2026-07-24

**Status:** Proposed Architecture - Pending Owner Approval and Implementation

**Document Owner:** Security Architect / QA

**Purpose:** Define secret scanning, dependency scanning, SAST, DAST,
access-control tests, IDOR tests, prompt injection test suite, agent red
teaming, file-upload security tests, and penetration testing.

**Note:** Implementation Evidence: This documentation PR does not prove that the described controls are implemented, tested, deployed, or production-ready. Code, automated tests, deployment evidence, and security verification remain the authoritative implementation evidence. Final security testing policy will be completed later, but this PR contains substantive policy, not just a stub.
completed later.

## Purpose

Define how we test security continuously.

## In Scope

- Secret scanning:
  - No raw `sk-` , no raw `ghp_` tokens, no `BEGIN PRIVATE KEY` raw in repo
  - CI scanning, pre-commit hooks, GitHub secret scanning, no secrets in docs,
    no tokens in remote URLs
- Dependency scanning:
  - Direct and transitive dependencies, known vulnerabilities, license
    compliance, supply-chain scanning for third-party agents
- SAST:
  - Static application security testing for backend (FastAPI, SQLAlchemy),
    frontend (Next.js), infra (Docker)
- DAST:
  - Dynamic scanning for Web, API, Mobile, Telegram webhook
- Access-control tests:
  - Authentication, authorization, least privilege, tenant isolation
  - User can only access own wallet, conversations, API keys
  - Admin access, IDOR tests (insecure direct object reference)
  - Session security (HttpOnly cookies, CSRF)
- Prompt injection test suite:
  - Direct injection, indirect injection via RAG context and file uploads
  - Jailbreak, tool abuse, RAG poisoning, data exfiltration,
    system-prompt disclosure, output guardrails
  - care_truthfulness_policy and belief_validation_policy
- Agent red teaming:
  - Agent permission boundaries, tool allowlists, budget enforcement
  - Human approval gates, absolutely forbidden NO-GO actions
  - Secret isolation, content_fingerprint DISABLED_BY_DEFAULT
- File-upload security tests:
  - File type validation, size limits, malware scanning, no execution of
    uploaded content, privacy-preserving handling
- Penetration testing:
  - Periodic external and internal pen tests, scope, rules of engagement,
    remediation tracking

## Out of Scope

- Final test cases and exact tooling (future PRs)
- Production pen test results (future)
- Implementation code

## Security Testing Cadence and Event Triggers

Require:

- Secret scanning on every PR (e.g., gitleaks, GitHub secret scanning, custom
  patterns for sk-, ghp_, BEGIN PRIVATE KEY only as examples to detect, not
  real secrets, no tokens in remote URLs)
- Dependency and supply-chain scanning on every PR (e.g., npm audit, pip audit,
  Snyk, Dependabot, SBOM generation)
- SAST on every relevant PR (e.g., CodeQL, Semgrep for backend FastAPI,
  frontend Next.js, infra Docker)
- Access-control and IDOR negative tests on every relevant backend PR (e.g.,
  test that user A cannot read user B's wallet, conversation, file, payment
  intent, API key, agent execution, studio job)
- Prompt-injection regression tests on every relevant AI/Agent PR (e.g., direct,
  indirect, jailbreak, tool abuse, RAG poisoning, data exfiltration,
  system-prompt disclosure, output guardrails)
- DAST in a controlled staging environment before applicable releases (e.g.,
  OWASP ZAP, Burp Suite, dynamic scanning for Web, API, Mobile, Telegram webhook)
- Internal security review using CONFIGURED_INTERNAL_TEST_CADENCE (e.g., weekly,
  bi-weekly, no invented monthly/quarterly without approval, use placeholder)
- External penetration testing using CONFIGURED_EXTERNAL_PENTEST_CADENCE (e.g.,
  quarterly, bi-annually, no invented monthly/quarterly without approval, use
  placeholder)
- Re-testing after critical security fixes (e.g., fix for auth bypass, wallet
  tampering, prompt injection, IDOR, secret leak)
- Re-testing after authentication, authorization, wallet, payment, upload, Agent,
  MCP, or provider-boundary changes (any change to auth, wallet, ledger, payment
  intents, file upload, agent tool calls, MCP connectors, provider abstraction)
- Event-triggered testing after material incidents (e.g., incident severity
  medium/high/critical triggers re-testing of related components)
- Remediation tracking with CONFIGURED_REMEDIATION_SLA (e.g., critical
  vulnerability fixed within CONFIGURED_REMEDIATION_SLA, high within
  CONFIGURED_REMEDIATION_SLA, medium/low documented with mitigation plan)

Do not invent monthly, quarterly, 90-day, or other numeric cadence. Use
CONFIGURED_INTERNAL_TEST_CADENCE, CONFIGURED_EXTERNAL_PENTEST_CADENCE,
CONFIGURED_REMEDIATION_SLA placeholders.

## Security Merge Gates

A relevant PR must not merge when:

- Secret scanning fails (e.g., detected exposed secret, raw sk-, ghp_ token,
  BEGIN PRIVATE KEY in commit, token in remote URL)
- A new critical or high-severity vulnerability is unresolved (e.g., dependency
  with critical CVE, SAST high-severity finding, no mitigation)
- Access-control or tenant-isolation tests fail (e.g., IDOR test fails, user A
  can read user B's wallet)
- IDOR/BOLA negative tests fail (e.g., cross-user or cross-tenant access not
  blocked, ownership checks missing)
- Required migration or rollback safety is missing (e.g., no migration for new
  table, no rollback plan for security-sensitive change)
- Prompt-injection/tool-abuse tests fail for Agent or AI changes (e.g., direct
  injection bypass, tool abuse, data exfiltration, system-prompt disclosure)
- Security-sensitive changes lack a threat assessment (e.g., no threat model
  update for new attack surface, no security review)
- A new dependency or external Agent has not passed required review (e.g.,
  source verification, license review, dependency scan, SBOM, static/dynamic
  analysis, prompt injection test, approval record missing)
- Required owner or security approval is missing (e.g., human approval gates
  for publishing, spending, contacting customers, pricing, config, merge, deploy,
  API keys, persona sensitive edits)

Document exception handling:

- Exceptions require named owner approval (e.g., product owner, security
  architect, founder)
- Business justification (e.g., why exception needed, risk acceptance)
- Compensating controls (e.g., additional monitoring, rate limiting, human
  approval, temporary mitigation)
- Expiry date using CONFIGURED_EXCEPTION_EXPIRY (e.g., exception expires after
  CONFIGURED_EXCEPTION_EXPIRY, requires re-review)
- Tracking issue (e.g., GitHub issue number, Jira ticket, with owner and
  timeline)
- Re-review (e.g., exception must be re-reviewed on expiry or on
  CONFIGURED_REVIEW_CADENCE)
- No exceptions for committed secrets or deliberate cross-tenant access (e.g.,
  no exception for secret in git history, no exception for IDOR bypass)

## Related Documents

- Security Index: [README.md](README.md)
- Persona QA: [../personas/PERSONA_QA_AND_RED_TEAMING.md](../personas/PERSONA_QA_AND_RED_TEAMING.md)
- Agent Security Model: [AGENT_SECURITY_MODEL.md](AGENT_SECURITY_MODEL.md)
- Prompt Injection Defense: [PROMPT_INJECTION_DEFENSE.md](PROMPT_INJECTION_DEFENSE.md)

## Open Decisions

- Testing toolset and CI integration
- Test coverage and frequency
- Owner approval for pen test scope

## Planned Completion Stage

Phase 1 - Testing

## Status Note

Proposed Architecture - Pending Owner Approval and Implementation. Implementation and verification are separate future work. Open Decisions remain unresolved until explicitly approved.
