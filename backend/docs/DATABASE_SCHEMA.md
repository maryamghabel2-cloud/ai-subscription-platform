# DATABASE SCHEMA - Phase 1 Part 1

**Date:** 2026-07-19  
**Branch:** build/phase-1-part1-database  
**Migration:** 001_core_schema (reversible upgrade/downgrade)

## Overview

Core schema for Persian AI Workspace MVP - 7 tables, financial safety via append-only ledger and RESTRICT FKs.

## Tables

### 1. users
- **Fields:**
  - id: Integer PK, indexed
  - email: String(255) unique, not null, indexed - unique constraint ensures no duplicate accounts
  - password_hash: String(255) not null - bcrypt hash
  - role: String(50) not null default 'user' - e.g., user, admin
  - is_active: Boolean not null default True
  - created_at: DateTime timezone-aware server_default now()
- **Indexes:** ix_users_id, ix_users_email unique
- **FKs:** None (parent)
- **Why:** Core identity, no cascade delete to preserve child financial data

### 2. wallets
- **Fields:**
  - id: Integer PK
  - user_id: Integer FK → users.id, unique, not null, indexed - one wallet per user
  - balance_credits: Integer not null default 0
  - created_at: DateTime timezone
  - updated_at: DateTime timezone server_default now() onupdate now()
- **Indexes:** ix_wallets_id, ix_wallets_user_id unique, constraint uq_wallets_user_id
- **FKs:** user_id → users.id ondelete RESTRICT
- **Why:** Wallet per user, unique ensures 1:1. RESTRICT prevents accidental user deletion with balance.

### 3. ledger_transactions (append-only)
- **Fields:**
  - id: Integer PK
  - wallet_id: Integer FK → wallets.id not null indexed
  - amount: Integer not null signed - positive credit (purchase, refund, bonus), negative debit (spend_chat, etc.)
  - type: String(50) not null indexed - purchase, spend_chat, spend_image, refund, bonus, admin_adjustment
  - reference_id: String(255) nullable indexed - external cause (conversation_id, message_id) but NOT FK to keep append-only decoupled
  - idempotency_key: String(255) not null unique indexed - **critical for financial safety**
  - created_at: DateTime timezone indexed server_default now()
- **Indexes:** ix_ledger_transactions_id, ix_ledger_transactions_wallet_id, ix_ledger_transactions_type, ix_ledger_transactions_reference_id, ix_ledger_transactions_idempotency_key unique, ix_ledger_transactions_created_at, plus explicit ix_ledger_idempotency_key_unique unique
- **FKs:** wallet_id → wallets.id ondelete RESTRICT
- **Why append-only:**
  - Financial safety: never UPDATE or DELETE ledger rows. History must be immutable for auditability.
  - Balance derived from sum or maintained via atomic INSERT + wallet update in same transaction, but history never mutated.
  - No UPDATE/DELETE in application logic - only INSERT. Enforced by code convention; future DB permissions could enforce read-only for app user on updates/deletes.
  - reference_id is not FK to keep ledger decoupled and always insertable even if referenced entity deleted (soft).
  - idempotency_key unique indexed prevents double processing on retries, network issues, replay. Duplicate insert raises IntegrityError. This is tested.
  - Type field allows filtering and reporting.
  - RESTRICT on wallet_id prevents wallet deletion with transactions - ledger must not disappear.

### 4. personas
- **Fields:**
  - id: Integer PK
  - slug: String(100) unique not null indexed - e.g., general-assistant, draft-psychologist
  - name_fa: String(255) not null - Persian name
  - role_definition: Text not null - system prompt, for high-risk must contain disclaimer and boundaries
  - tone: String(100) nullable
  - risk_level: String(20) not null default low indexed - low, medium, high
  - status: String(20) not null default draft indexed - draft, active, deprecated
  - version: String(20) not null default v1.0.0
  - created_at: DateTime timezone server_default now()
- **Indexes:** ix_personas_id, ix_personas_slug unique, ix_personas_risk_level, ix_personas_status
- **FKs:** None (parent)
- **Why:** Persona registry, seed creates 2 placeholder personas.

### 5. conversations
- **Fields:**
  - id: Integer PK
  - user_id: Integer FK → users.id not null indexed
  - persona_id: Integer FK → personas.id nullable indexed
  - created_at: DateTime timezone server_default now()
- **Indexes:** ix_conversations_id, ix_conversations_user_id, ix_conversations_persona_id
- **FKs:** user_id → users.id ondelete RESTRICT, persona_id → personas.id ondelete RESTRICT
- **Why:** Conversation belongs to user, optionally with persona. RESTRICT prevents deleting user or persona while conversations exist, preserving audit trail.

### 6. messages
- **Fields:**
  - id: Integer PK
  - conversation_id: Integer FK → conversations.id not null indexed
  - role: String(20) not null indexed - user, assistant, system
  - content: Text not null
  - enhanced_prompt: Text nullable - future prompt enhancer output
  - provider_used: String(100) nullable - placeholder for future provider name (no brand hardcoding, just placeholder)
  - cost_credits: Integer nullable - placeholder for future cost
  - created_at: DateTime timezone server_default now()
- **Indexes:** ix_messages_id, ix_messages_conversation_id, ix_messages_role
- **FKs:** conversation_id → conversations.id ondelete RESTRICT (relationship has cascade delete-orphan for app-level deletion if conversation explicitly deleted, but DB FK is RESTRICT to force app logic to decide)
- **Why:** Messages belong to conversation. RESTRICT at DB level for safety, but ORM relationship cascade allows explicit conversation deletion to clean messages if needed. Cost and provider placeholders for future.

### 7. api_keys
- **Fields:**
  - id: Integer PK
  - user_id: Integer FK → users.id not null indexed
  - key_hash: String(255) unique not null indexed - hashed key, never raw
  - scopes: String(255) nullable default chat
  - rate_limit: Integer not null default 60
  - created_at: DateTime timezone server_default now()
  - revoked_at: DateTime timezone nullable
- **Indexes:** ix_api_keys_id, ix_api_keys_user_id, ix_api_keys_key_hash unique
- **FKs:** user_id → users.id ondelete RESTRICT
- **Why:** API keys for developer platform Phase 4, but schema prepared now. key_hash unique prevents duplicate hashes. RESTRICT prevents user deletion with active keys.

## Indexes Summary

- Unique: users.email, personas.slug, wallets.user_id, ledger_transactions.idempotency_key (two indexes: ix_... and ix_ledger_idempotency_key_unique), api_keys.key_hash
- Regular: FKs, type, risk_level, status, created_at, role, reference_id for query performance

## Foreign Keys and Cascade Decision

**Decision: Default RESTRICT for financial safety (documented here and in code).**

- **Why RESTRICT not CASCADE:**
  - Financial data (wallets, ledger_transactions) must never disappear accidentally via user deletion.
  - Audit trail (conversations, messages) must be preserved for compliance.
  - Personas referenced by conversations must not be deletable while in use.
  - Wallets with transactions must not be deletable.
  - Users with wallets, conversations, api_keys must not be deletable without explicit cleanup workflow that is audited and requires human approval for financial data.

- **Implementation:**
  - All FKs have ondelete='RESTRICT' in SQLAlchemy.
  - In SQLite tests, PRAGMA foreign_keys=ON enforced to test RESTRICT.
  - Application logic must explicitly handle deletion: e.g., to delete user, first ensure wallet balance 0, archive ledger, delete conversations via app logic with audit, then delete user. This prevents accidental cascade.
  - Relationship cascade="all, delete-orphan" only for Conversation->Messages to allow conversation deletion to clean messages when explicitly requested, but DB FK still RESTRICT to force app to load conversation first, not raw SQL delete.

- **Future:** For production Postgres, could add DEFERRABLE or additional checks, but RESTRICT remains default. For GDPR deletion, need explicit workflow with audit and approval.

## Append-Only Ledger Design - Deep Dive

- **What append-only means:** Only INSERT, never UPDATE/DELETE in app code. Ledger is immutable log.
- **Why:**
  - Auditability: Every credit movement has immutable record.
  - Idempotency: idempotency_key unique prevents double spend on retry. Duplicate key raises IntegrityError - tested.
  - Correctness: Wallet balance should be updated in same transaction as ledger insert: BEGIN; INSERT ledger; UPDATE wallet SET balance = balance + amount; COMMIT; If second insert with same idempotency_key tries, fails, wallet not double updated.
  - No UPDATE means no history rewriting, no lost audit.
  - reference_id not FK to keep decoupled: even if conversation deleted, ledger entry remains for financial audit.
- **How enforced:**
  - Code convention: No update/delete queries for ledger_transactions in codebase.
  - Tests: No update/delete in tests.
  - Future DB role: App DB user could have GRANT INSERT, SELECT on ledger_transactions but not UPDATE/DELETE.
  - Documentation here.
- **Idempotency key generation:** Should be client-generated UUID or server-generated deterministic from request context (e.g., hash of user_id + action + request_id). Must be unique per logical operation. Stored unique indexed.

## Seed Script

- backend/app/seed.py creates exactly 2 personas:
  - slug general-assistant, name_fa دستیار عمومی, risk_level low, status active, role_definition general Persian assistant info
  - slug draft-psychologist, name_fa پیش‌نویس روان‌شناس, risk_level high, status draft, role_definition contains literal "NOT READY FOR PRODUCTION — pending domain-expert review" to mark not ready and require expert review.
- Tested to create exactly 2.

## Migrations

- Alembic init: backend/alembic.ini, backend/alembic/env.py, backend/alembic/script.py.mako, backend/alembic/versions/001_core_schema.py
- 001_core_schema.py creates all 7 tables with FKs and indexes, especially unique index on idempotency_key (ix_ledger_transactions_idempotency_key and ix_ledger_idempotency_key_unique)
- Reversible: upgrade creates tables, downgrade drops tables in reverse order (api_keys, messages, ledger_transactions, conversations, wallets, personas, users) to respect FK dependencies. Tested up/down.

## Tests

- tests/test_migration.py: checks alembic files exist, checks Base.metadata.create_all creates 7 tables, checks idempotency unique index exists, checks drop_all removes tables (simulates down)
- tests/test_constraints.py: unique email raises IntegrityError, idempotency_key duplicate raises IntegrityError, FK RESTRICT prevents user deletion with wallet, wallet unique user_id
- tests/test_seed.py: seed creates exactly 2 personas with correct fields per spec, including high-risk draft persona containing NOT READY string

## What Is NOT Built (Per Scope Limits)

- No auth endpoints, no wallet business logic/API, no AI provider code, no frontend code, no real pricing numbers, no payment gateway, no brand name hardcoding, no real API keys (key_hash is placeholder hashed, no raw keys in seed).

## Future Phases

- Phase 1 Part 2: Auth endpoints will use users table
- Phase 1 Part 3: Wallet API will use wallets + ledger_transactions with idempotency
- Phase 2: Personas table will be used for specialist personas, status draft/active
- Phase 4: ApiKeys table for developer platform

## No Secrets

- No real API keys, no payment gateway credentials, no brand name hardcoding, no production DATABASE_URL with real password in repo (uses placeholder aiuser:aipass localhost). .env.example contains placeholder CHANGE_ME.
