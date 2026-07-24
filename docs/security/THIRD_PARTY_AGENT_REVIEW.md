# Third-Party Agent Review

**Version:** v0.1.0

**Date:** 2026-07-24

**Status:** Draft - Structure Only

**Document Owner:** Security Architect / Product

**Purpose:** Define detailed Third-Party Agent Security Review policy covering
why review is mandatory, review checklist, approved manifest, runtime isolation,
and re-review requirements.

**Note:** Structure-only. Final policy will be completed later.

## Purpose

Define how third-party and marketplace agents are reviewed before approval to
prevent data exfiltration, abuse, and supply-chain compromise.

## In Scope

- Why review is mandatory, review checklist, approved manifest, runtime
  isolation, re-review requirement

## Out of Scope

- Final checklist and exact scanning tools (future PRs)
- Marketplace business logic and rev-share (future Phase 8)
- Implementation code

## Why Third-Party Agent Review Is Mandatory

- Agents can execute tools, call APIs, read files, and affect user data
- Agents have permissions, budgets, and may have access to scoped credentials
- A malicious or vulnerable agent can exfiltrate data, abuse resources, or
  compromise other users via cross-tenant access attempts
- Supply-chain attacks via agent dependencies are a real threat: dependency
  confusion, typosquatting, malicious packages with known CVEs, prompt injection
  in dependencies

## Review Checklist Before Any Third-Party Agent Is Approved

### Source Verification

- Agent source repository and author identity confirmed (GitHub profile, PGP
  signature if available, publisher authority)
- License verified as compatible with commercial use (MIT, Apache, proprietary
  check, public domain, licensed, purchased with appropriate usage rights)
- Commit history reviewed for suspicious changes (large binary additions,
  obfuscated code, recent force-push)
- Cryptographic checksum or signed release verified (SHA256, Sigstore, Cosign)

### Dependency and Supply-Chain Scan

- All dependencies audited for known vulnerabilities (npm audit, pip audit,
  Snyk, GitHub Dependabot)
- SBOM generated (SPDX or CycloneDX) and stored with agent version
- No transitive dependency with known critical CVE at time of review
- License compatibility for all transitive dependencies checked

### Security Analysis

- Static analysis for code quality and vulnerability patterns (SAST, CodeQL,
  Semgrep)
- Dynamic analysis in isolated sandbox environment (no network by default,
  then allowlisted network, no access to real user data)
- Prompt injection test: can the agent be hijacked via crafted input? Test
  direct and indirect injection, jailbreak, tool abuse, RAG poisoning
- Tool abuse test: can the agent call unauthorized tools or exceed its budget
  via crafted input? Test budget enforcement CONFIGURED_LIMIT
- Data exfiltration test: can the agent leak user data to external endpoints?
  Test with canary tokens, no real user data

### Remediation Requirement

- All critical and high-severity findings must be remediated before approval
- Medium findings must be documented and have a mitigation plan with owner and
  timeline
- Low findings must be documented and tracked
- Re-scan after remediation, expert review, owner approval before publishing

## Approved Agent Manifest

- Agent must have an approved manifest including:
  - id, name, version, author, source, license, checksum, runtime type
  - Required tools: web_search, file_reader, image_generation_api, etc.
  - Read permissions: own data only, no cross-user, no raw secrets
  - Write permissions: draft-only or specific scopes, no direct main commit
  - Network allowlist: approved official government and embassy sources for
    immigration, no arbitrary internet unless approved
  - Secret requirements: none or specific scoped credentials, separate from
    platform, revocable independently
  - Maximum cost, maximum execution time, maximum iterations (CONFIGURED_LIMIT)
  - Human approval gates: publishing, spending, contacting customers, bulk
    messages, pricing, config, merge, deploy, API keys, persona sensitive edits
  - Risk level: low, medium, high, high-risk requires expert review
  - Review status: pending, approved, rejected, with reviewer name, credentials,
    date, expiry
  - Rollback version: previous known good version

## Runtime Isolation

- Approved agents run in a sandboxed environment (container, gVisor, Firecracker,
  or similar isolation, no privileged mode)
- Agents never inherit the full application environment or secrets (only scoped
  credentials they need)
- Network calls are restricted to the approved allowlist (egress filtering,
  no arbitrary internet unless approved official sources)
- Tool calls are restricted to the approved allowlist (tool allowlist, permission
  boundaries, budget enforcement)
- Secret isolation: separate scoped credentials, no sharing of full env,
  encrypted at rest, no secret in logs

## Re-Review Requirement

- Any update to a third-party agent requires re-review (new version, new
  dependencies, new permissions, new tools, new network allowlist)
- Agents must be reviewed again on a CONFIGURED_LIMIT cadence (e.g., 90 days,
  180 days) even if no changes, to check for new CVEs and advisories
- Security advisories against agent dependencies trigger an immediate re-review
  (critical CVE in dependency, malicious package report)

## Related Documents

- Security Index: [README.md](README.md)
- Agent Security Model: [AGENT_SECURITY_MODEL.md](AGENT_SECURITY_MODEL.md)
- Human Approval Gates: [../agents/HUMAN_APPROVAL_GATES.md](../agents/HUMAN_APPROVAL_GATES.md)
- Source Quality Policy: [../research/SOURCE_QUALITY_POLICY.md](../research/SOURCE_QUALITY_POLICY.md)
- Security Testing: [SECURITY_TESTING.md](SECURITY_TESTING.md)
- Agent Permission Model: [../agents/AGENT_PERMISSION_MODEL.md](../agents/AGENT_PERMISSION_MODEL.md)

## Open Decisions

- Scanning toolset and CI integration (CodeQL, Semgrep, Snyk, Dependabot)
- Review SLA and approver roles and required credentials
- Revocation criteria and communication and user notification
- SBOM format and storage location and retention
- Owner approval required for all decisions

## Planned Completion Stage

Phase 2 - Marketplace Prep

## Status Note

Draft - Structure Only. Will be completed later.
