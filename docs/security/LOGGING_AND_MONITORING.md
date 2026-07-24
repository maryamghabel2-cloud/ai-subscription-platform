# Logging and Monitoring

**Version:** v0.1.0

**Date:** 2026-07-24

**Status:** Draft - Structure Only

**Document Owner:** Security Architect / SRE

**Purpose:** Define privacy-preserving technical logs, security events, anomaly detection, alerting, log integrity, and no raw sensitive conversation content.

**Note:** This is a structure-only stub. Final policy will be completed later.

## In Scope

- Privacy-preserving technical logs: must NOT store raw sensitive prompts, uploaded file contents, conversation text, raw AI responses by default, must NOT store deterministic unkeyed hashes of user messages or AI responses (unkeyed SHA-256 disallowed), content_fingerprint DISABLED_BY_DEFAULT, fingerprint_method APPROVED_KEYED_HMAC_ONLY_IF_REQUIRED (HMAC-SHA-256 with protected, env-specific, versioned, rotatable secret if ever required for separately approved security use case, not for analytics/profiling/cross-user comparison)
- Default audit metadata allowed: user pseudonymous identifier (hashed or internal id, not raw email if possible), agent_id, agent_version, execution_id, tool names, provider_id, model_id, token and usage counts, estimated and settled cost, timestamps (created_at, last_used_at), approval records (who approved, when), result status (success/failure), error category without sensitive content (timeout, rate_limit, not raw stack trace with prompt), rollback reference
- Security events: authentication success/failure, authorization failures, session creation/revocation, agent permission denials, approval requests, rate limit hits, payment intent create/complete/fail/expire, wallet credit/debit atomic with SELECT FOR UPDATE, balance never negative
- Anomaly detection: brute force, credential stuffing, abuse, prompt injection attempts, tool abuse, data exfiltration signals, payment fraud, channel spoofing
- Alerting: thresholds, routing, on-call, human approval for high-impact actions, reversible protective actions
- Log integrity: append-only, tamper-evident, retention, access control, no raw sensitive content, encrypted product-data store only when required for user-facing feature per retention settings (conversations, generated images/videos, uploaded files)
- No raw sensitive conversation content: raw content remains outside technical logs, only in separate encrypted product-data store when required

## Out of Scope

- Final log schema, exact retention periods, alerting tooling (future PRs)
- Implementation code (future)

## Related Documents

- Security Index: [README.md](README.md)
- Agent Plugin and Execution: [../architecture/AGENT_PLUGIN_AND_EXECUTION_SYSTEM.md](../architecture/AGENT_PLUGIN_AND_EXECUTION_SYSTEM.md)
- Data Protection and Encryption: [DATA_PROTECTION_AND_ENCRYPTION.md](DATA_PROTECTION_AND_ENCRYPTION.md)
- Security Agent Runtime: [SECURITY_AGENT_RUNTIME.md](SECURITY_AGENT_RUNTIME.md)

## Open Decisions

- Log schema and storage (append-only audit log table)
- Retention periods and access control
- Alert thresholds and routing

## Planned Completion Stage

- Phase 1 - Logging

## Status

Draft - Structure Only. Will be completed later.
