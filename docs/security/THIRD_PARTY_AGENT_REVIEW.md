# Third-Party Agent Review

**Version:** v0.1.0

**Date:** 2026-07-24

**Status:** Proposed Architecture - Pending Owner Approval and Implementation

**Document Owner:** Security Architect / Product

**Purpose:** Define detailed Third-Party Agent Security Review policy covering
why review is mandatory, review checklist, approved manifest, runtime isolation,
and re-review requirements.

**Note:** Implementation Evidence: This documentation PR does not prove that the described controls are implemented, tested, deployed, or
production-ready. Code, automated tests, deployment evidence, and security verification remain the authoritative implementation evidence.

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

## Intake and Initial Triage Workflow

Define lifecycle states:

- **Submitted:** Agent submitted via Skill Builder or external import, private
  draft, no public visibility, versioned

- **Intake Validation:** Validate intake package completeness, required fields,
  no secrets in package, no hardcoding of Role names, no claiming professional
  authority

- **Quarantined:** Candidate is quarantined until approved, no access to real
  user data, no access to production credentials, isolated sandbox only

- **License and Provenance Review:** License verified as compatible with
  commercial use, author/publisher identity confirmed, provenance verified

- **Security Review:** Dependency and supply-chain scan, static and dynamic
  analysis, prompt injection test, tool abuse test, data exfiltration test

- **Remediation Required:** Critical and high-severity findings must be
  remediated before approval, medium findings must have mitigation plan

- **Sandbox Evaluation:** Dynamic analysis in isolated sandbox environment, no
  network by default, then allowlisted network, no access to real user data

- **Human Approval:** Human approval gates for publishing, spending, contacting
  customers, pricing, config, merge, deploy, API keys, persona sensitive edits,
  high-risk requires expert review

- **Approved:** Published only after approval, versioned, with review status,
  rollback version, audit trail

- **Suspended / Revoked / Rejected:** Approval may be revoked immediately if
  compromise detected, new CVE in dependencies, malicious behavior, or policy
  violation

The intake package must include:

- Repository or official source (e.g., GitHub URL, official partner source)
- Immutable commit or release identifier (e.g., commit SHA, tag, release version)
- Author/publisher identity (e.g., GitHub profile, PGP signature, publisher
  authority, geographic/jurisdiction)
- License (e.g., MIT, Apache, proprietary, public domain, licensed, purchased
  with appropriate usage rights, legally authorized)
- Commercial-use compatibility (e.g., compatible with commercial use)
- Checksums/signatures when available (e.g., SHA256, Sigstore, Cosign)
- Runtime and language (e.g., Python, Node, Docker, WASM)
- Dependency lockfiles (e.g., package-lock.json, poetry.lock, yarn.lock)
- SBOM when available (SPDX or CycloneDX)
- Required tools (e.g., web_search, file_reader, image_generation_api)
- Read/write permissions (e.g., own data only, no cross-user, draft-only)
- Network destinations (e.g., approved official government and embassy sources,
  no arbitrary internet)
- Secret requirements (e.g., none or specific scoped credentials, separate from
  platform, revocable independently)
- Data classifications accessed (e.g., public, internal, confidential, no
  sensitive personal data)
- Cost/time/iteration requirements (e.g., max cost CONFIGURED_LIMIT, max
  execution time CONFIGURED_AGENT_MAX_DURATION, max iterations
  CONFIGURED_AGENT_MAX_ITERATIONS)
- Known limitations (e.g., no vision support, no file support, no tool support)
- Security contact (e.g., security@example.com)
- Update and disclosure policy (e.g., how updates are disclosed, security
  advisory process)

Intake rules:

- No code execution during initial intake (static analysis only, no dynamic
  execution until quarantined sandbox)
- No access to real user data (test with synthetic data, canary tokens, no real
  user data)
- No access to production credentials (no provider API keys, no Telegram bot
  tokens, no HMAC secrets, no DATABASE_URL)
- Unknown license means HOLD or REJECT (cannot approve with unknown license)
- Unverifiable publisher/provenance means HOLD or REJECT (cannot approve if
  author identity or provenance cannot be verified)
- Repository popularity or star count is not security evidence (stars, forks,
  downloads are not security evidence)
- A README claim is not security evidence (README saying secure is not evidence)
- Every candidate starts untrusted (default-deny, must pass all checks)
- Every candidate is quarantined until approved (no public visibility, no
  production access until approved)
- Approval applies only to a specific reviewed version/checksum (e.g., commit
  SHA, tag, checksum, not to future versions)
- New versions require re-review (any update requires re-review, even minor)
- Approval may be revoked immediately (if compromise, new CVE, malicious behavior)

This workflow must later be reusable by the Skills/Agents/MCP
landscape-research process: the intake package and lifecycle states are designed
to be reused by internal Skills, Verified External Skills, and User-Provided
Skills and MCP Connectors, with same quarantine and review process.

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
- Agents must be reviewed again on a CONFIGURED_LIMIT cadence (e.g., CONFIGURED_REVIEW_CADENCE,
  CONFIGURED_REVIEW_CADENCE) even if no changes, to check for new CVEs and advisories
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

Proposed Architecture - Pending Owner Approval and Implementation. Implementation and verification are separate future work. Open Decisions remain
unresolved until explicitly approved.
