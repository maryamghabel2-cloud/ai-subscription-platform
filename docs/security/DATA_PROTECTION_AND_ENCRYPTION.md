# Data Protection and Encryption

**Version:** v0.1.0

**Date:** 2026-07-24

**Status:** Proposed Architecture - Pending Owner Approval and Implementation

**Document Owner:** Security Architect / Privacy

**Purpose:** Define encryption in transit, encryption at rest, field-level
encryption, data minimization, retention, deletion, backup security, and
user-controlled privacy, with clear distinction between hashing,
storage-level encryption, application/field-level encryption, and reversible
encryption.

**Note:** Implementation Evidence: This documentation PR does not prove that the
described controls are implemented, tested, deployed, or production-ready. Code,
automated tests, deployment evidence, and security verification remain the
authoritative implementation evidence.

## Purpose

Define how data is protected, minimized, retained, and deleted, and how
field-level protection is proposed for sensitive content.

## In Scope

- Encryption in transit, encryption at rest, field-level encryption,
  hashing vs encryption distinction, data minimization, retention, deletion,
  backup security, user-controlled privacy

## Out of Scope

- Exact encryption algorithms, key lengths, rotation schedule (future PRs)
- Implementation code and concrete backup tooling (future)

## Encryption in Transit

- TLS 1.2+, HSTS, certificate validation, no downgrade, no plaintext sensitive
  data in transit
- API and Web and Mobile and Telegram webhook must use TLS
- Certificate pinning for Mobile API connections where appropriate
- No sensitive content in push notification payloads

## Encryption at Rest

- Database: users, wallets, ledgers, conversations, messages, api_keys table,
  file storage: uploaded files, generated images/videos, product photos
- File storage: uploaded files, generated images/videos, product photos
- Secrets: provider keys, Telegram bot tokens encrypted at rest via secrets
  manager, HMAC fingerprint secret protected, env-specific, versioned, rotatable
- Backups: encrypted backups, retention, restoration testing, access control,
  no secrets in backups in plaintext

## Field-Level Data Protection

Distinguish:

- **Hashing:** One-way, irreversible, e.g., API key hash (key_hash), password
  hashing bcrypt with pre-hash, no raw API key stored, key_prefix for lookup
  only, not reversible, not encryption

- **Storage-level encryption:** Transparent database encryption, disk encryption,
  volume encryption, protects data at rest at storage layer, but data is
  plaintext to database process, does not protect against application-level
  access or compromised database credentials

- **Application/field-level encryption:** Application encrypts specific fields
  before storage, with explicit key management, envelope encryption, key IDs
  and versions, associated-data binding, audited access, separate from storage
  encryption, protects against compromised database or backup access

- **Reversible encryption:** Symmetric encryption that can be decrypted with key,
  e.g., AES-GCM, used for field-level encryption where application needs to
  read plaintext, must have key management, rotation, re-encryption

Do not classify wallet constraints or API-key hashing as field-level encryption:

- Wallet balance check `balance_credits >=0` enforced at DB and code is a
  constraint, not field-level encryption
- API-key hashing (key_hash) is hashing, one-way, not reversible, not
  field-level encryption

Propose field/application-level protection for:

- Conversation content: long-term conversations may contain sensitive personal
  content, mental health, trauma, migration, private files, should be considered
  for application-level encryption with envelope encryption, key IDs and
  versions, associated-data binding (e.g., user_id, conversation_id)
- Message content: messages within conversations, same protection as conversation
  content, field-level encryption with envelope encryption
- Long-term memory: memory policy per Role, session_only vs long-term memory,
  long-term memory may contain sensitive personal content, should be considered
  for field-level encryption
- Sensitive support cases: support cases that contain trauma, abuse, grief, loss,
  mental health, should be field-level encrypted, access audited, retention
  limited, non-retention by default unless user explicitly enables memory
- Sensitive attachment metadata: attachment filenames, descriptions, metadata
  that may contain PII, should be considered for field-level encryption or
  redaction, no raw sensitive content in logs
- Provider credentials and integration tokens: provider API keys, Telegram bot
  tokens, payment gateway credentials, HMAC fingerprint secret, must be encrypted
  at rest via secrets manager, not in code, git history, documentation, logs,
  URLs, or client-side code, provider-neutral envelope encryption not needed but
  secrets manager with KEK/DEK
- Highly sensitive retained Agent/Persona state: agent execution state that may
  contain sensitive personal content, persona memory, should be considered for
  field-level encryption, access audited, retention limited

Require provider-neutral envelope encryption, key IDs and versions, separate
KEK/DEK management, rotation/re-encryption, associated-data binding, audited
access, and deletion/backup handling:

- Provider-neutral envelope encryption: application generates DEK (data encryption
  key) per field or per record, encrypts field with DEK using AES-GCM, encrypts
  DEK with KEK (key encryption key) from KMS/secrets manager, stores encrypted
  DEK alongside ciphertext, with key ID and version
- Key IDs and versions: each encrypted field stores key_id and key_version and
  DEK version, for rotation and audit, e.g., key_id: CONFIGURED_KEY_ID,
  key_version: v1, dek_version: v1
- Separate KEK/DEK management: KEK managed by KMS/secrets manager, never leaves
  KMS, DEK generated per field or per record, encrypted with KEK, KEK rotation
  re-encrypts DEKs, DEK rotation re-encrypts fields
- Rotation/re-encryption: KEK rotation must re-encrypt DEKs, DEK rotation must
  re-encrypt fields, rotation events logged with metadata only, no raw keys,
  old keys remain valid for CONFIGURED_SECRET_ROTATION_GRACE_PERIOD during
  planned rotation, compromised credentials receive no grace period
- Associated-data binding: use AES-GCM associated data (AAD) binding to
  user_id, conversation_id, or other context to prevent ciphertext swapping across
  tenants or objects
- Audited access: every field-level decryption access must be logged with
  metadata only (pseudonymous user id, object type, object id hash, key_id,
  timestamp, result, no raw sensitive content)
- Deletion/backup handling: deletion must delete ciphertext and DEK, or make DEK
  unrecoverable (crypto-shredding), backups must be encrypted, retention,
  restoration testing, access control, no secrets in backups in plaintext

Do not claim these controls are implemented. They are proposed future
architecture, not implemented in current database schema. Future migrations,
atomic PostgreSQL tests, concurrency tests, and rollback tests are required
before activation. Existing Wallet and Ledger behavior must not be described as
already supporting these features.

## Data Minimization

- Collect only needed data, pseudonymous identifiers in logs
- No raw sensitive content by default, content_fingerprint DISABLED_BY_DEFAULT,
  fingerprint_method APPROVED_KEYED_HMAC_ONLY_IF_REQUIRED
- No permanent IP tracking, no device fingerprinting by default, privacy-
  preserving abuse controls

## Retention and Deletion

- Per data type: users, wallets, ledger_transactions append-only ledger with
  positive and negative amount entries, payment_intents, personas,
  conversations, messages, api_keys
- User-controlled deletion, legal holds if required, versioned config
- Deletion: user can delete conversation, image, uploaded doc, account deletion
  workflow, hard delete vs soft delete, audit trail of deletion, no recovery
  after hard delete unless backup, crypto-shredding for field-level encrypted
  fields

## Backup Security

- Encrypted backups, retention, restoration testing, access control
- No secrets in backups in plaintext, KEK/DEK separation, rotation

## User-Controlled Privacy

- Retention settings, memory policy per Role, session_only options
- Consent for human review of private content requires informed user consent
  and separately approved support workflow, no secret sharing
- Non-retention by default for sensitive Telegram conversations unless user
  explicitly enables memory

## Related Documents

- Security Index: [README.md](README.md)
- Data Classification: [../architecture/DATA_CLASSIFICATION_AND_RETENTION.md](../architecture/DATA_CLASSIFICATION_AND_RETENTION.md)
- Secrets Management: [SECRETS_AND_KEY_MANAGEMENT.md](SECRETS_AND_KEY_MANAGEMENT.md)
- Logging and Monitoring: [LOGGING_AND_MONITORING.md](LOGGING_AND_MONITORING.md)
- Agent Security Model: [AGENT_SECURITY_MODEL.md](AGENT_SECURITY_MODEL.md)

## Open Decisions

- Encryption algorithm choices (AES-GCM, ChaCha20-Poly1305) and key management
  service (KMS, Vault, AWS KMS)
- Field-level encryption scope: which fields require application-level encryption
  vs storage-level encryption vs hashing
- Key IDs and versions strategy and rotation/re-encryption workflow
- Associated-data binding design (user_id, conversation_id, tenant_id)
- Retention periods per data type and legal requirements and deletion workflow
- Owner, security, privacy, legal, compliance approval required

## Planned Completion Stage

Phase 1 - Data Protection

## Status Note

Proposed Architecture - Pending Owner Approval and Implementation. Implementation
and verification are separate future work. Open Decisions remain unresolved
until explicitly approved.
