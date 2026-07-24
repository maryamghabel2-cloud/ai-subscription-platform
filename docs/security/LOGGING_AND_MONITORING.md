# Logging and Monitoring

**Purpose:** Define security logging, monitoring, alerting, and audit principles.

**Status:** Draft - Structure Only

**Note:** This is a structure-only stub. Final logging and monitoring policy will be completed in later PRs.

## Scope

This document will cover:

- What to log: security events, authentication attempts, authorization failures, agent executions, approval records, rate limit hits, payment intent state changes
- What NOT to log by default: raw sensitive prompts, uploaded file contents, conversation text, raw AI responses, deterministic unkeyed hashes of user messages
- Audit metadata allowed: pseudonymous user id, agent id/version/execution id, tool names, provider/model ids, content_fingerprint DISABLED_BY_DEFAULT, fingerprint_method APPROVED_KEYED_HMAC_ONLY_IF_REQUIRED, token counts, cost, timestamps, approval records, result status, error category without sensitive content, rollback reference
- Log protection: append-only, tamper-evident, retention, access control
- Monitoring and alerting: anomaly detection, brute force, abuse, payment fraud, prompt injection attempts
- Separation: technical logs vs product-data store for user-facing features
- Compliance: no localStorage for sensitive data in backend, no secrets in logs

Final policy will require security, SRE, and privacy review.

## Linkage

- Security Index: [README.md](README.md)
- Agent Plugin and Execution: [../architecture/AGENT_PLUGIN_AND_EXECUTION_SYSTEM.md](../architecture/AGENT_PLUGIN_AND_EXECUTION_SYSTEM.md)
- Data Protection: [DATA_PROTECTION_AND_ENCRYPTION.md](DATA_PROTECTION_AND_ENCRYPTION.md)

## Status

Draft - Structure Only. Will be completed later.
