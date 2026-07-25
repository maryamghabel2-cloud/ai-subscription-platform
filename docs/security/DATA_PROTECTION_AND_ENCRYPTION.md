# Data Protection and Encryption

**Version:** v0.1.0

**Date:** 2026-07-24

**Status:** Proposed Architecture - Pending Owner Approval and Implementation

**Document Owner:** Security Architect / Privacy

**Purpose:** Define encryption in transit, encryption at rest, field-level
encryption, data minimization, retention, deletion, backup security, and
user-controlled privacy.

**Note:** Implementation Evidence: This documentation PR does not prove that the described controls are implemented, tested, deployed, or production-ready. Code, automated tests, deployment evidence, and security verification remain the authoritative implementation evidence.

## Purpose

Define how data is protected, minimized, retained, and deleted.

## In Scope

- Encryption in transit:
  - TLS 1.2+, HSTS, certificate validation, no downgrade
  - API and Web and Mobile and Telegram webhook must use TLS
  - No plaintext sensitive data in transit
- Encryption at rest:
  - Database: users, wallets, ledgers, conversations, messages, api_keys
  - File storage: uploaded files, generated images/videos, product photos
  - Secrets: provider keys, Telegram bot tokens encrypted at rest, HMAC
    fingerprint secret protected, env-specific, versioned, rotatable
- Field-level encryption:
  - Sensitive fields: API key hash not raw, token encrypted, no raw sensitive
    prompts in technical logs
  - Wallet balance check >=0 enforced at DB and code
- Data minimization:
  - Collect only needed data, pseudonymous identifiers in logs
  - No raw sensitive content by default, content_fingerprint DISABLED_BY_DEFAULT,
    fingerprint_method APPROVED_KEYED_HMAC_ONLY_IF_REQUIRED
- Retention:
  - Per data type: users, wallets, ledger_transactions append-only ledger with
    positive and negative amount entries, payment_intents, personas,
    conversations, messages, api_keys
  - User-controlled deletion, legal holds if required, versioned config
- Deletion:
  - User can delete conversation, image, uploaded doc, account deletion workflow
  - Hard delete vs soft delete, audit trail of deletion, no recovery after
    hard delete unless backup
- Backup security:
  - Encrypted backups, retention, restoration testing, access control
  - No secrets in backups in plaintext
- User-controlled privacy:
  - Retention settings, memory policy per Role, session_only options
  - Consent for human review of private content requires informed user consent
    and separately approved support workflow, no secret sharing
  - Non-retention by default for sensitive Telegram conversations unless user
    explicitly enables memory

## Out of Scope

- Exact encryption algorithms, key lengths, rotation schedule (future PRs)
- Implementation code and concrete backup tooling (future)

## Related Documents

- Security Index: [README.md](README.md)
- Data Classification: [../architecture/DATA_CLASSIFICATION_AND_RETENTION.md](../architecture/DATA_CLASSIFICATION_AND_RETENTION.md)
- Secrets Management: [SECRETS_AND_KEY_MANAGEMENT.md](SECRETS_AND_KEY_MANAGEMENT.md)
- Logging and Monitoring: [LOGGING_AND_MONITORING.md](LOGGING_AND_MONITORING.md)

## Open Decisions

- Encryption algorithm choices and key management service
- Retention periods per data type and legal requirements
- Deletion workflow and verification and backup restoration testing
- Owner approval required for all decisions

## Planned Completion Stage

Phase 1 - Data Protection

## Status Note

Proposed Architecture - Pending Owner Approval and Implementation. Implementation and verification are separate future work. Open Decisions remain unresolved until explicitly approved.
