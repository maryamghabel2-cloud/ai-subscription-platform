# Logging and Monitoring

**Version:** v0.1.0

**Date:** 2026-07-24

**Status:** Proposed Architecture - Pending Owner Approval and Implementation

**Document Owner:** Security Architect / SRE

**Purpose:** Define privacy-preserving technical logs, security events, anomaly
detection, alerting, log integrity, and no raw sensitive conversation content.

**Note:** Implementation Evidence: This documentation PR does not prove that the described controls are implemented, tested, deployed, or
production-ready. Code, automated tests, deployment evidence, and security verification remain the authoritative implementation evidence.

## Purpose

Define what we log, how we monitor, and how we alert without exposing raw
sensitive content.

## In Scope

- Privacy-preserving technical logs:
  - Must NOT store raw sensitive prompts, uploaded file contents, conversation
    text, raw AI responses by default
  - Must NOT store deterministic unkeyed hashes of user messages or AI responses
    (unkeyed SHA-256 disallowed)
  - content_fingerprint DISABLED_BY_DEFAULT
  - fingerprint_method APPROVED_KEYED_HMAC_ONLY_IF_REQUIRED (HMAC-SHA-256 with
    protected, env-specific, versioned, rotatable secret if ever required for
    separately approved security use case, not for analytics/profiling/cross-user)
- Default audit metadata allowed:
  - User pseudonymous identifier (hashed or internal id, not raw email)
  - Agent id, agent version, execution id
  - Tool names
  - Provider id, model id
  - Token and usage counts
  - Estimated and settled cost
  - Timestamps (created_at, last_used_at)
  - Approval records (who approved, when)
  - Result status (success/failure)
  - Error category without sensitive content (timeout, rate_limit, not raw stack
    trace with prompt)
  - Rollback reference
- Security events:
  - Authentication success/failure, authorization failures
  - Session creation/revocation, agent permission denials
  - Approval requests, rate limit hits, payment intent state changes
  - Wallet credit/debit atomic with SELECT FOR UPDATE, balance never negative
- Anomaly detection:
  - Brute force, credential stuffing, abuse, prompt injection attempts
  - Tool abuse, data exfiltration signals, payment fraud, channel spoofing
- Alerting:
  - Thresholds, routing, on-call, human approval for high-impact actions
  - Reversible protective actions
- Log integrity:
  - Append-only, tamper-evident, retention, access control
  - No raw sensitive content, encrypted product-data store only when required
    for user-facing feature per retention settings (conversations, images,
    uploaded files)
- No raw sensitive conversation content:
  - Raw content remains outside technical logs, only in separate encrypted
    product-data store when required

## Out of Scope

- Final log schema, exact retention periods, alerting tooling (future PRs)
- Implementation code (future)

## Related Documents

- Security Index: [README.md](README.md)
- Agent Plugin and Execution: [../architecture/AGENT_PLUGIN_AND_EXECUTION_SYSTEM.md](../architecture/AGENT_PLUGIN_AND_EXECUTION_SYSTEM.md)
- Data Protection: [DATA_PROTECTION_AND_ENCRYPTION.md](DATA_PROTECTION_AND_ENCRYPTION.md)
- Security Agent Runtime: [SECURITY_AGENT_RUNTIME.md](SECURITY_AGENT_RUNTIME.md)

## Open Decisions

- Log schema and storage (append-only audit log table)
- Retention periods and access control
- Alert thresholds and routing
- Owner approval required

## Planned Completion Stage

Phase 1 - Logging

## Status Note

Proposed Architecture - Pending Owner Approval and Implementation. Implementation and verification are separate future work. Open Decisions remain
unresolved until explicitly approved.
