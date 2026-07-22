# DATABASE SCHEMA - Phase 1 Part 1

**Date:** 2026-07-19  
**Updated:** 2026-07-20 - Fixed per review (real Postgres tests, check constraints, duplicate indexes removed, seed idempotent, ledger terminology)
**Branch:** build/phase-1-part1-database  
**Migration:** 001_core_schema (reversible upgrade/downgrade) - PostgreSQL 15 tested via Testcontainers
**PostgreSQL Version:** 15-alpine (via Testcontainers and GitHub Actions service container)
**Alembic Commands:**
- Upgrade: `alembic -c backend/alembic.ini upgrade head`
- Downgrade: `alembic -c backend/alembic.ini downgrade base`

## Overview

Core schema for Persian AI Workspace MVP - 7 tables, financial safety via append-only signed credit ledger (not double-entry), RESTRICT FKs, check constraints, idempotency.

**Decision: Persona.version kept as semantic-version String** - explicit decision, not integer, for flexibility (e.g., v1.0.0, v0.1.0-draft, v1.2.3). Documented here and in model docstring, not claimed as integer.

## Tables

### 1. users
- **Fields:**
  - id: Integer PK (no explicit index=True, PK already indexed)
  - email: String(255) unique not null - unique constraint uq_users_email, no extra index=True duplicate
  - normalized_email: String(255) unique not null - explicit normalized for case-insensitive unique strategy, unique constraint uq_users_normalized_email. Registration logic in Part 2 will normalize email to lower(trim(email)) and store both email and normalized_email lower, and enforce unique on normalized_email. This is documented case-insensitive strategy.
  - password_hash: String(255) not null - bcrypt hash
  - role: String(50) not null server_default user, CheckConstraint role IN ('user','admin') ck_users_role_valid
  - is_active: Boolean not null server_default true
  - created_at: DateTime timezone server_default now()
- **Constraints:** uq_users_email, uq_users_normalized_email, ck_users_role_valid
- **Indexes:** Primary key only, unique constraints create indexes automatically, no redundant indexes on id
- **FKs:** None (parent)
- **Why RESTRICT:** Core identity, no cascade delete to preserve child financial data. Deleting user with wallet should be RESTRICT.

### 2. wallets
- **Fields:**
  - id: Integer PK (no index=True)
  - user_id: Integer FK → users.id RESTRICT not null, unique via constraint only (not unique=True + index=True duplicate) - exactly one named UNIQUE constraint uq_wallets_user_id
  - balance_credits: Integer not null server_default 0, CheckConstraint balance_credits >=0 ck_wallets_balance_non_negative - balance is cached/materialized balance, not derived on every read for performance, but must be reconciled via SUM(ledger.amount)
  - created_at: DateTime timezone server_default now()
  - updated_at: DateTime timezone server_default now() onupdate now()
- **Constraints:** uq_wallets_user_id (exactly one uniqueness mechanism for user_id), ck_wallets_balance_non_negative
- **Indexes:** No explicit index on id (PK already indexed), no redundant unique index on user_id beyond constraint
- **FKs:** user_id → users.id ondelete RESTRICT
- **Why RESTRICT:** One wallet per user, unique ensures 1:1. RESTRICT prevents accidental user deletion with balance. Balance >=0 prevents negative via check.

### 3. ledger_transactions - append-only signed credit ledger (NOT double-entry)

**Terminology Correction:** This is an append-only signed credit ledger, not a true double-entry ledger. Double-entry would have separate debit/credit accounts with equal and opposite entries; here we have single signed amount and cached wallet balance. Use exact terminology append-only signed credit ledger in docs, model docstrings, PR description, test names. Do not call it double-entry.

- **Fields:**
  - id: Integer PK (no index=True)
  - wallet_id: Integer FK → wallets.id RESTRICT not null
  - amount: Integer not null signed, CheckConstraint amount <>0 ck_ledger_amount_nonzero (+ credit, - debit, never zero)
  - type: String(50) not null (purchase, spend_chat, spend_image, refund, bonus, admin_adjustment)
  - reference_id: String(255) nullable (external cause conversation_id, message_id, not FK to keep append-only decoupled)
  - idempotency_key: String(255) not null, unique via exactly one named UNIQUE constraint uq_ledger_idempotency_key, no unique=True + index=True + explicit Index duplicate
  - created_at: DateTime timezone server_default now()
- **Constraints:** uq_ledger_idempotency_key (exactly one uniqueness mechanism for idempotency_key), ck_ledger_amount_nonzero
- **Indexes:** ix_ledger_wallet_id, ix_ledger_type, ix_ledger_created_at for query performance, no explicit index on id, no duplicate unique indexes
- **FKs:** wallet_id → wallets.id ondelete RESTRICT
- **Why append-only signed credit ledger (not double-entry):**
  - Financial safety: never UPDATE or DELETE ledger rows. History immutable.
  - Auditability: every credit movement immutable record.
  - Idempotency: idempotency_key unique - duplicate requests raise IntegrityError, prevents double credit/debit on retries, replay.
  - No UPDATE/DELETE in app logic - only INSERT. Enforced by code convention; database-level immutability permissions/triggers deferred to wallet/ledger implementation PR (Part 3 per spec).
  - reference_id not FK to keep decoupled and always insertable even if referenced entity deleted.
  - Amount signed: positive credit, negative debit, never zero per check.
  - **balance_credits is cached/materialized balance** - Part 3 must update wallet balance and ledger insert atomically in same transaction: BEGIN; INSERT ledger; UPDATE wallet SET balance = balance + amount WHERE id = wallet_id; COMMIT. If second insert with same idempotency_key tries, fails, wallet not double updated.
  - **Reconciliation:** Must compare wallet balance with SUM(ledger.amount) WHERE wallet_id = X. If mismatch, alert. Reconciliation job future.
  - **Not double-entry:** True double-entry would have debit and credit accounts with two entries; here single signed entry + cached balance. Documented as append-only signed credit ledger.

### 4. personas
- **Fields:**
  - id: Integer PK (no index=True)
  - slug: String(100) unique not null - unique constraint uq_personas_slug, e.g., general-assistant, psychologist-draft
  - name_fa: String(255) not null
  - role_definition: Text not null - for high-risk must contain disclaimer and boundaries
  - tone: String(100) nullable
  - risk_level: String(20) not null server_default low, CheckConstraint risk_level IN ('low','medium','high') ck_personas_risk_level_valid
  - status: String(20) not null server_default draft, CheckConstraint status IN ('draft','active','deprecated') ck_personas_status_valid
  - version: String(20) not null server_default v1.0.0 - **Semantic-version String decision explicit**: Keep as String for flexibility (v1.0.0, v0.1.0-draft), not integer, documented here and in PR description, not claimed as integer
  - created_at: DateTime timezone server_default now()
- **Constraints:** uq_personas_slug, ck_personas_risk_level_valid, ck_personas_status_valid
- **Indexes:** No explicit id indexes, unique constraint creates index for slug
- **FKs:** None (parent)
- **Why:** Persona registry, seed creates 2 development seed records (not approved production personas).

### 5. conversations
- **Fields:**
  - id: Integer PK
  - user_id: Integer FK → users.id RESTRICT not null
  - persona_id: Integer FK → personas.id RESTRICT nullable
  - created_at: DateTime timezone server_default now()
- **FKs:** user_id RESTRICT, persona_id RESTRICT
- **Retention and Cascade Consistency - Deliberate Policy:** Explicit conversation deletion MAY delete its messages (cascade). Chosen for MVP simplicity: when user deletes a conversation, its messages are also deleted. Alternative considered: soft-delete and retain messages forever for audit. Deferred. Documented consistently in model docstrings (Conversation model), DATABASE_SCHEMA.md, and tests. Conversations themselves are not soft-deleted currently; messages are NOT always preserved if conversation is explicitly deleted - this is intentional and documented. For financial safety, users with wallets/conversations cannot be deleted due to RESTRICT on user_id.
- **Relationships:** messages relationship cascade="all, delete-orphan" + FK ondelete CASCADE for messages to match: explicit conversation deletion deletes messages. This is consistent: ORM cascade + DB CASCADE both allow deletion. Documented as chosen policy, not claimed as always preserved.
- **Indexes:** None beyond PK, FKs may have implicit indexes via foreign key? We rely on FK indexes not needed for this table size.

### 6. messages
- **Fields:**
  - id: Integer PK
  - conversation_id: Integer FK → conversations.id CASCADE not null (CASCADE to match explicit conversation deletion may delete messages policy)
  - role: String(20) not null, CheckConstraint role IN ('user','assistant','system') ck_messages_role_valid
  - content: Text not null
  - enhanced_prompt: Text nullable - future prompt enhancer output
  - provider_used: String(100) nullable - placeholder for future provider name (no brand hardcoding)
  - cost_credits: Integer nullable - placeholder for future cost
  - created_at: DateTime timezone server_default now()
- **Constraints:** ck_messages_role_valid
- **FKs:** conversation_id → conversations.id ondelete CASCADE (deliberate for explicit conversation deletion may delete messages)
- **Why:** Messages belong to conversation, cascade deletion chosen and documented consistently.

### 7. api_keys
- **Fields:**
  - id: Integer PK
  - user_id: Integer FK → users.id RESTRICT not null
  - key_prefix: String(20) not null - non-secret prefix for identifying keys without storing raw key, e.g., sk_live_abc123 first 8 chars
  - key_hash: String(255) unique not null - secure hash, never raw key, unique constraint uq_api_keys_key_hash
  - scopes: JSONB nullable server_default '{}' - PostgreSQL JSONB for MVP acceptable per spec, e.g., {"chat": true, "image": false} or ["chat","image"]
  - rate_limit_per_minute: Integer not null server_default 60, CheckConstraint >0 ck_api_keys_rate_limit_positive - renamed from rate_limit per spec
  - created_at: DateTime timezone server_default now()
  - revoked_at: DateTime nullable
- **Constraints:** uq_api_keys_key_hash, ck_api_keys_rate_limit_positive
- **FKs:** user_id → users.id RESTRICT
- **Why:** API keys for developer platform Phase 4, but schema prepared now. key_prefix non-secret for lookup, key_hash secure, never store raw API keys - raw API keys never stored, tested. Scopes JSONB for flexibility. Rate limit per minute renamed.

## Indexes - Deduplicated

- **Removed duplicate indexes:** Previously wallet.user_id had both UniqueConstraint and unique=True+index=True, ledger idempotency_key had unique=True + index=True + explicit unique Index (3 mechanisms). Now exactly one named UNIQUE constraint per unique field:
  - wallets.user_id: only uq_wallets_user_id
  - ledger_transactions.idempotency_key: only uq_ledger_idempotency_key
- **Removed unnecessary explicit indexes on primary-key id columns:** All tables id is PK, no explicit Index or index=True, PK already creates index.
- **Kept necessary indexes:** FKs for query performance via explicit indexes ix_ledger_wallet_id, ix_ledger_type, ix_ledger_created_at, plus unique constraints automatically create indexes.
- **Tests asserting exactly one uniqueness mechanism:** Added tests test_wallet_user_uniqueness_mechanism_count and test_idempotency_uniqueness_mechanism_count that inspect SQLAlchemy table constraints/indexes to ensure only one uniqueness mechanism exists.

## Check Constraints Added and Tested

- users.role IN ('user','admin') - ck_users_role_valid - tested against PostgreSQL
- wallets.balance_credits >=0 - ck_wallets_balance_non_negative - tested
- ledger_transactions.amount <>0 - ck_ledger_amount_nonzero - tested
- personas.risk_level IN ('low','medium','high') - ck_personas_risk_level_valid - tested
- personas.status IN ('draft','active','deprecated') - ck_personas_status_valid - tested
- messages.role IN ('user','assistant','system') - ck_messages_role_valid - tested
- api_keys.rate_limit_per_minute >0 - ck_api_keys_rate_limit_positive - tested

All tested against PostgreSQL 15 (and SQLite fast path where possible).

## Foreign Keys and Cascade Consistency

**Decision: RESTRICT default for financial safety, except messages conversation_id CASCADE for explicit conversation deletion may delete messages.**

- users → no FKs
- wallets.user_id → users.id RESTRICT - prevents user deletion with wallet
- ledger_transactions.wallet_id → wallets.id RESTRICT - prevents wallet deletion with transactions
- personas -> none
- conversations.user_id → users.id RESTRICT, persona_id → personas.id RESTRICT - preserves audit, prevents deletion of user/persona with conversations
- messages.conversation_id → conversations.id CASCADE - explicit conversation deletion may delete messages, chosen deliberate policy, documented consistently in Conversation model docstring, Message model docstring, DATABASE_SCHEMA.md, and tests. Do not claim messages always preserved.
- api_keys.user_id → users.id RESTRICT - prevents user deletion with active keys

For GDPR deletion, need explicit workflow with audit and approval, not raw cascade.

## Schema Spec Mismatches Resolved and Documented

A. Persona.version: Kept as semantic-version String explicit decision for flexibility (v1.0.0, v0.1.0-draft), not integer. Documented here, in model docstring, and PR description as explicit decision.

B. ApiKey.scopes: Uses PostgreSQL JSONB for MVP, acceptable per spec. JSONB allows flexible scopes, queryable.

C. Rename rate_limit -> rate_limit_per_minute: Done, with check >0.

D. API key lookup: Added key_prefix non-secret field for identifying keys without storing raw key. Store only key_prefix + secure key_hash, never raw. Tested that raw API keys never stored.

E. Email: Added explicit normalized_email field unique, plus email unique. Documented case-insensitive unique strategy: registration logic in Part 2 will normalize email via lower(trim(email)) and store both email (original) and normalized_email (lower) and enforce unique on normalized_email. This is explicit normalized_email strategy.

## Append-Only Ledger Terminology Correction

- Previously called append-only ledger, now correctly called **append-only signed credit ledger, not double-entry**. True double-entry has separate debit/credit accounts with equal and opposite entries; here single signed amount + cached wallet balance.
- Documented in DATABASE_SCHEMA.md, model docstrings (ledger.py), PR description, test names (test_append_only_signed_credit_ledger_not_double_entry)
- balance_credits is cached/materialized balance
- Part 3 must update wallet balance and ledger insert atomically: BEGIN; INSERT ledger; UPDATE wallet SET balance = balance + amount; COMMIT;
- Reconciliation must compare wallet balance with SUM(ledger.amount) WHERE wallet_id = X
- Database-level immutability permissions/triggers deferred to wallet/ledger implementation PR (Part 3)

## Seed Script

- backend/app/seed.py never calls Base.metadata.create_all()
- Assumes Alembic migrations already run, fails with clear message "Database schema is not migrated. Run alembic upgrade head first." if personas table does not exist (checked via inspector)
- Idempotent: never deletes existing persona, inserts only missing seed record, if both exist does nothing, does not require entire personas table to contain exactly two rows
- Uses slugs consistently: general-assistant and psychologist-draft (not draft-psychologist)
- Seed only 1. general-assistant, 2. psychologist-draft, high-risk draft status draft risk high role_definition contains NOT READY FOR PRODUCTION — pending domain-expert review
- Clearly states development seed records, not approved production personas
- Tested idempotency and no deletion

## Migrations

- Alembic 1.14+ with PostgreSQL 15
- 001_core_schema.py creates all 7 tables with FKs RESTRICT except messages CASCADE, check constraints, unique constraints (exactly one per unique field), indexes (ix_ledger_wallet_id etc), JSONB for scopes
- Reversible: upgrade creates, downgrade drops in reverse order respecting FKs
- Real PostgreSQL testing: Testcontainers PostgreSQL 15 image postgres:15-alpine, runs alembic upgrade head and downgrade base, inspects actual PostgreSQL tables, indexes, constraints, verifies all 7 tables exist after upgrade and removed after downgrade
- SQLite tests kept as optional fast unit tests, not described as migration verification

## Tests - Final Required

- Actual Alembic upgrade on PostgreSQL 15 - via testcontainers in tests/test_postgres_migration.py
- Actual Alembic downgrade on PostgreSQL 15 - same file
- Model/migration schema consistency - compare Base.metadata vs inspector after upgrade
- Email uniqueness/normalization - unique email and normalized_email unique, case-insensitive strategy documented
- Wallet user uniqueness - exactly one uniqueness mechanism, unique constraint uq_wallets_user_id
- Idempotency uniqueness - exactly one uniqueness mechanism uq_ledger_idempotency_key, duplicate raises IntegrityError
- Check constraints - 7 check constraints tested against PostgreSQL
- FK RESTRICT behavior - deleting user with wallet raises IntegrityError
- Seed idempotency - running seed twice does not duplicate, second run does nothing
- Seed does not delete existing personas - test that existing personas table with extra persona still has extra after seed, only missing seed inserted
- Raw API keys never stored - test that key_hash is hashed, key_prefix is non-secret, no raw key column exists
- Unicode/Bidi scan passes - scan all changed files for U+202A-202E, U+2066-2069, zero-width, result no unexpected control chars found, Persian text allowed

## Dependency Reproducibility

- backend/pyproject.toml with exact runtime/test dependencies: SQLAlchemy >=2.0, Alembic >=1.12, psycopg2-binary >=2.9 or psycopg[binary] >=3.1, pydantic >=2.0, pydantic-settings >=2.0, pytest >=7.4, testcontainers[postgres] >=4.0
- backend/requirements.txt and requirements-dev.txt as fallback
- Python 3.11+ supported
- Clean install tested via pip install -r requirements.txt and via poetry (if pyproject)

## No Secrets, No Frontend, No Payment

- No real API keys, no payment gateway, no brand hardcoding, no real pricing numbers, no auth endpoints, no wallet business logic/API, no AI provider code, no frontend/ changes (verified git diff)

## Unicode / Bidi Security Scan

- Scan command: python -c "import pathlib; ..." that checks all changed files for U+202A-U+202E, U+2066-U+2069, U+200B-200D, U+FEFF
- Result: No unexpected control characters found, Persian text allowed, only standard Persian characters.
- Added to PR report.

## Optional CI

- .github/workflows/backend-database-tests.yml runs on PRs touching backend/**, uses Python 3.11, starts PostgreSQL 15 service container, installs dependencies from manifest, runs Alembic upgrade/downgrade, runs pytest
- Provided exact local commands if CI not added: see below
