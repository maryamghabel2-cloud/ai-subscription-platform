# Third-Party Agent Review

**Version:** v0.1.0

**Date:** 2026-07-24

**Status:** Draft - Structure Only

**Document Owner:** Security Architect / Product

**Purpose:** Define security review of ready-made Agents, repository and source
verification, license review, dependency and supply-chain scanning, static and
dynamic analysis, prompt injection testing, remediation before approval, version
review and revocation.

**Note:** Structure-only stub. Final review policy will be completed later.

## Purpose

Define how third-party and marketplace agents are reviewed before approval.

## In Scope

- Why third-party agent review is mandatory:
  - Agents can execute tools, call APIs, read files, and affect user data
  - A malicious or vulnerable agent can exfiltrate data, abuse resources, or
    compromise other users
  - Supply-chain attacks via agent dependencies are a real threat

- Review checklist before any third-party agent is approved:

  - Source verification:
    - Agent source repository and author identity confirmed
    - License verified as compatible with commercial use
    - Commit history reviewed for suspicious changes
    - Cryptographic checksum or signed release verified

  - Dependency and supply-chain scan:
    - All dependencies audited for known vulnerabilities
    - SBOM generated
    - No transitive dependency with known critical CVE
    - License compatibility checked

  - Security analysis:
    - Static analysis for code quality and vulnerability patterns
    - Dynamic analysis in isolated sandbox environment
    - Prompt injection test: can the agent be hijacked via crafted input?
    - Tool abuse test: can the agent call unauthorized tools or exceed its
      budget via crafted input?
    - Data exfiltration test: can the agent leak user data to external endpoints?

  - Remediation requirement:
    - All critical and high-severity findings must be remediated before approval
    - Medium findings must be documented and have a mitigation plan
    - Low findings must be documented

- Approved agent manifest:
  - Agent must have an approved manifest including: id, name, version, author,
    source, license, checksum, runtime type, required tools, read permissions,
    write permissions, network allowlist, secret requirements, maximum cost,
    maximum execution time, maximum iterations, human approval gates, risk level,
    review status, rollback version

- Runtime isolation:
  - Approved agents run in a sandboxed environment
  - Agents never inherit the full application environment or secrets
  - Network calls are restricted to the approved allowlist
  - Tool calls are restricted to the approved allowlist
  - Secret isolation: separate scoped credentials

- Re-review requirement:
  - Any update to a third-party agent requires re-review
  - Agents must be reviewed again on a CONFIGURED_LIMIT cadence
  - Security advisories against agent dependencies trigger immediate re-review

## Out of Scope

- Final checklist and exact scanning tools (future PRs)
- Marketplace business logic and rev-share (future Phase 8)
- Implementation code

## Related Documents

- Security Index: [README.md](README.md)
- Agent Security Model: [AGENT_SECURITY_MODEL.md](AGENT_SECURITY_MODEL.md)
- Human Approval Gates: [../agents/HUMAN_APPROVAL_GATES.md](../agents/HUMAN_APPROVAL_GATES.md)
- Source Quality Policy: [../research/SOURCE_QUALITY_POLICY.md](../research/SOURCE_QUALITY_POLICY.md)
- Security Testing: [SECURITY_TESTING.md](SECURITY_TESTING.md)

## Open Decisions

- Scanning toolset and CI integration
- Review SLA and approver roles
- Revocation criteria and communication
- SBOM format and storage
- Owner approval required

## Planned Completion Stage

Phase 2 - Marketplace Prep

## Status Note

Draft - Structure Only. Will be completed later.
