# Security Testing

**Version:** v0.1.0

**Date:** 2026-07-24

**Status:** Draft - Structure Only

**Document Owner:** Security Architect / QA

**Purpose:** Define secret scanning, dependency scanning, SAST, DAST, access-control tests, IDOR tests, prompt injection test suite, agent red teaming, file-upload security tests, and penetration testing.

**Note:** This is a structure-only stub. Final security testing policy will be completed later.

## In Scope

- Secret scanning: no `sk-` raw, no `ghp_` raw tokens, no `BEGIN PRIVATE KEY` raw in repo, CI scanning, pre-commit hooks, GitHub secret scanning, no secrets in docs, no tokens in remote URLs
- Dependency scanning: direct and transitive dependencies, known vulnerabilities, license compliance, supply-chain scanning for third-party agents
- SAST: static application security testing for backend (FastAPI, SQLAlchemy), frontend (Next.js), infra (Docker)
- DAST: dynamic scanning for Web, API, Mobile, Telegram webhook
- Access-control tests: authentication, authorization, least privilege, tenant isolation (user can only access own wallet, conversations, API keys), admin access, IDOR tests (insecure direct object reference), session security (HttpOnly cookies, CSRF)
- Prompt injection test suite: direct injection, indirect injection via RAG context and file uploads, jailbreak, tool abuse, RAG poisoning, data exfiltration, system-prompt disclosure, output guardrails, care_truthfulness_policy and belief_validation_policy
- Agent red teaming: agent permission boundaries, tool allowlists, budget enforcement, human approval gates, absolutely forbidden NO-GO actions, secret isolation, content_fingerprint DISABLED_BY_DEFAULT
- File-upload security tests: file type validation, size limits, malware scanning, no execution of uploaded content, privacy-preserving handling
- Penetration testing: periodic external and internal pen tests, scope, rules of engagement, remediation tracking

## Out of Scope

- Final test cases, exact tooling, implementation (future PRs)
- Production pen test results (future)

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

- Phase 1 - Testing

## Status

Draft - Structure Only. Will be completed later.
