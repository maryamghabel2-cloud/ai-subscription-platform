# Data Protection and Encryption

**Version:** v0.1.0

**Date:** 2026-07-24

**Status:** Draft - Structure Only

**Document Owner:** Security Architect / Privacy

**Purpose:** Define encryption in transit, encryption at rest, field-level encryption, data minimization, retention, deletion, backup security, and user-controlled privacy.

**Note:** This is a structure-only stub. Final policy will be completed later.

## In Scope

- Encryption in transit: TLS 1.2+, HSTS, certificate validation, no downgrade, API and Web and Mobile and Telegram webhook must use TLS
- Encryption at rest: database (users, wallets, ledgers, conversations, messages, api_keys), file storage (uploaded files, generated images/videos), secrets (provider keys, Telegram bot tokens encrypted at rest, HMAC fingerprint secret protected)
- Field-level encryption: sensitive fields (e.g., API key hash not raw, token encrypted), no raw sensitive prompts in technical logs
- Data minimization: collect only needed data, pseudonymous identifiers in logs, no raw sensitive content by default, content_fingerprint DISABLED_BY_DEFAULT, fingerprint_method APPROVED_KEYED_HMAC_ONLY_IF_REQUIRED
- Retention: per data type (users, wallets, ledger_transactions append-only ledger with positive and negative amount entries, payment_intents, personas, conversations, messages, api_keys), user-controlled deletion, legal holds if required
- Deletion: user can delete conversation, image, uploaded doc, account deletion workflow, hard delete vs soft delete, audit trail of deletion
- Backup security: encrypted backups, retention, restoration testing, access control
- User-controlled privacy: retention settings, memory policy per Role, session_only options, consent for human review of private content requires informed user consent and separately approved support workflow, no secret sharing

## Out of Scope

- Exact encryption algorithms, key lengths, rotation schedule (future PRs)
- Implementation code (future)

## Related Documents

- Security Index: [README.md](README.md)
- Data Classification and Retention: [../architecture/DATA_CLASSIFICATION_AND_RETENTION.md](../architecture/DATA_CLASSIFICATION_AND_RETENTION.md)
- Secrets and Key Management: [SECRETS_AND_KEY_MANAGEMENT.md](SECRETS_AND_KEY_MANAGEMENT.md)
- Logging and Monitoring: [LOGGING_AND_MONITORING.md](LOGGING_AND_MONITORING.md)

## Open Decisions

- Encryption algorithm choices and key management service
- Retention periods per data type
- Deletion workflow and verification

## Planned Completion Stage

- Phase 1 - Data Protection

## Status

Draft - Structure Only. Will be completed later.
