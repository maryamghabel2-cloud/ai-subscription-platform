# Phase 1 Data Model

## Document Control
**Title:** Phase 1 Data Model
**Status:** Draft — Complete Phase 1 Data Model
**Phase:** Phase 1 — In Progress
**Last updated:** 2026-08-22
**Related:** [ADR-0002](../decisions/0002-phase-1-product-metering-and-infrastructure.md), [API Contract](API_CONTRACT_V1.md), [Chat Contract](API_CONTRACT_V1_CHAT.md), [Features Contract](API_CONTRACT_V1_FEATURES.md)

## Overview
Phase 1 uses PostgreSQL. The model supports authentication, wallet/credits, and
feature histories. Primary keys are UUID v4; ledger is append-only; feature
histories retain 90 days.

## Data Modeling Principles
- UUID v4 primary keys.
- TIMESTAMPTZ timestamps.
- Tenant isolation through user/tenant foreign keys.
- Ledger is INSERT-only.
- Soft deletion uses nullable deleted_at.
- Password hashes use bcrypt or argon2.
- Session tokens are stored only as hashes.
- No PII in telemetry.
- Foreign keys and query indexes are enforced.
- Retention uses background jobs.
- Alembic migrations are reversible where possible.

## Section 1: Core Tables

### Table 1: users
Stores account and tenant-base identity. Columns: id UUID PK; email VARCHAR(255)
NOT NULL UNIQUE; password_hash VARCHAR(255) NOT NULL; display_name VARCHAR(200)
NULL; status VARCHAR(20) default active; created_at/updated_at TIMESTAMPTZ;
deleted_at TIMESTAMPTZ NULL; failed_login_count INTEGER default 0; last_login_at
TIMESTAMPTZ NULL. Email uniqueness is case-insensitive. Hashes never contain
plaintext passwords. Implementation: Backend foundation exists — validation
required (`backend/app/models/user.py`).

### Table 2: auth_sessions
Stores active sessions with id UUID PK, user_id UUID FK users ON DELETE CASCADE,
token_hash VARCHAR(255) UNIQUE, refresh_token_hash nullable UNIQUE, created_at,
last_used_at, expires_at TIMESTAMPTZ, revoked_at nullable, ip_address INET nullable,
and user_agent TEXT nullable. Raw tokens exist only in HttpOnly cookies. Refresh
rotation invalidates prior session. Implementation: Backend foundation exists —
validation required (`backend/app/models/auth_session.py`).

### Table 3: tenants
Future workspace/organization scope: id UUID PK; name VARCHAR(200); owner_user_id
UUID FK users; created_at/updated_at TIMESTAMPTZ; status VARCHAR(20) default
active. Phase 1 creates one tenant per user; multi-user workspaces are deferred.
Implementation: Pending implementation.

### Table 4: user_tenant_memberships
Association: id UUID PK; user_id UUID FK users ON DELETE CASCADE; tenant_id UUID
FK tenants ON DELETE CASCADE; role VARCHAR(20) default owner; created_at
TIMESTAMPTZ; UNIQUE(user_id, tenant_id). Phase 1 has one owner membership per user.
Implementation: Pending implementation.

## Section 2: Wallet and Ledger Tables

### Table 1: wallets
One wallet per tenant, authoritative balances. Columns: id UUID PK; tenant_id UUID
NOT NULL UNIQUE FK tenants; available_credits INTEGER nonnegative; reserved_credits
INTEGER nonnegative; total_credits generated as available plus reserved; created_at,
updated_at TIMESTAMPTZ; version INTEGER for optimistic locking. Balance is
authoritative; ledger is audit trail. Implementation: Backend foundation exists —
validation required.

### Table 2: ledger_entries
Immutable append-only credit movements. Columns: id UUID PK; tenant_id UUID FK;
wallet_id UUID FK; entry_type top_up/reservation/settlement/release/correction;
direction credit/debit; amount INTEGER positive; feature nullable; reservation_id
nullable FK; top_up_intent_id nullable FK; status; description; created_at; created_by_request_id.
NO UPDATE or DELETE operations are permitted. Corrections use compensating entries.
Implementation: Backend foundation exists — validation required.

### Table 3: reservations
Tracks holds. Columns: id UUID PK; tenant_id/wallet_id UUID FKs; feature;
quoted_credits positive; actual_credits nullable and <= quoted_credits; status
reserved/settled/released/canceled/expired; expires_at TIMESTAMPTZ; timestamps;
idempotency_key UUID; request_metadata JSONB. Unique tenant/idempotency_key.
Expiration is 10 minutes. Implementation: Backend foundation exists — validation required.

### Table 4: top_up_intents
Sandbox top-up lifecycle. Columns: id UUID PK; tenant_id/wallet_id FKs;
package_size 100/500/2000; amount_credits; status pending/succeeded/failed/canceled;
mock_confirmation_token_hash; idempotency_key; created_at; confirmed_at; failed_reason.
Unique tenant/idempotency_key. Raw confirmation token is never stored. No real
payment gateway table exists in Phase 1. Implementation: Backend foundation exists — validation required.

### Table 5: receipt_snapshots
MVP-optional immutable receipt: id UUID PK; tenant_id FK; top_up_intent_id UNIQUE
FK; amount_credits; package_size; created_at; receipt_data JSONB. Retention: 12
months. Implementation: Pending implementation.

## Section 3: Feature Tables

### Table 10: conversations
Tenant chat container: id UUID PK; tenant_id UUID FK tenants; user_id UUID FK
users; title; status active/archived/deleted; created_at/updated_at/last_message_at
TIMESTAMPTZ; message_count; deleted_at. Soft delete applies; ledger entries remain.
Implementation: Pending implementation.

### Table 11: chat_messages
Message records: id UUID PK; conversation_id UUID FK conversations; tenant_id UUID
FK tenants; role; content nullable; status; reservation_id UUID FK reservations;
quoted_credits; actual_credits; tier; idempotency_key; timestamps; provider_metadata
JSONB. Unique tenant/idempotency_key when present. Content can be null for failed
or canceled output. Retention is 90 days. Implementation: Pending implementation.

### Table 12: enhancer_history
Enhancement records: id UUID PK; tenant_id/user_id UUID FKs; raw_prompt;
enhanced_prompt nullable; style; status; reservation_id UUID FK reservations;
quoted_credits default 2; actual_credits; idempotency_key; timestamps;
provider_metadata JSONB. Unique tenant/idempotency_key. Retention 90 days.
Implementation: Pending implementation.

### Table 13: caption_generation_history
Caption records: id UUID PK; tenant_id/user_id UUID FKs; original_generation_id
self FK; regeneration_number; description; tone; length; platform; language_mode;
hashtag_count CHECK 3–30; variation_count CHECK 1–5; text-only image_context;
variations JSONB; status; reservation_id UUID FK reservations; quoted_credits
default 5; actual_credits; idempotency_key; timestamps; provider_metadata JSONB.
Unique tenant/idempotency_key. Regeneration links original generation and is new
billable request. Image upload/vision is out of scope. Retention 90 days.
Implementation: Pending implementation.

### Feature Table Invariants

- Every feature table has tenant_id for row-level tenant isolation.
- reservation_id links usage to immutable ledger.
- Feature deletion never removes ledger entries.
- Retention is 90 days from feature activity.
- provider_metadata is observability only; ledger is billing source of truth.

## Section 4: Indexes and Query Patterns

Core indexes: users(email); auth_sessions(token_hash), auth_sessions(user_id,
expires_at); wallets(tenant_id); ledger_entries(tenant_id, created_at DESC),
ledger_entries(wallet_id, created_at); reservations(tenant_id, idempotency_key),
reservations(expires_at); conversations(tenant_id, updated_at DESC),
conversations(user_id); chat_messages(conversation_id, created_at),
chat_messages(tenant_id); enhancer_history(tenant_id, created_at DESC),
enhancer_history(idempotency_key); caption_generation_history(tenant_id,
created_at DESC), caption_generation_history(idempotency_key).

PostgreSQL partial index supports pending ledger entries; BRIN supports time
archiving. Tenant-scoped composite indexes and JSONB GIN indexes are used where
query evidence supports them. Migration files define final index names/order.

## Section 5: Retention Policy Implementation

Feature histories soft-delete after 90 days and hard-delete after an additional
30-day grace period. Ledger entries and receipts retain at least 12 months and
remain immutable. Expired/revoked sessions older than 30 days are cleaned.

A database function `cleanup_expired_data()` runs daily via approved scheduler.
Retention uses retention_expires_at trigger/computed policy, summary-only audit
records, and application queries respecting deletion state.

## Section 6: Migration Strategy

Alembic manages schema changes. Migrations are forward-only in production,
idempotent where possible, and manually reviewed. Initial order: core tables,
wallet/ledger, feature tables, indexes/retention triggers, cleanup scheduling.
Tables have timestamps where appropriate; autogenerate is scaffolding only.

## Section 7: Open Items for C0 / C1

C0 validates foreign keys, immutable ledger, tenant isolation, retention cleanup,
nonnegative balances, and idempotency. C1 implements cleanup, message_count trigger,
JSONB validation, partial indexes, and billing admin audit. Future phases add
multi-user roles, Enhancer favorites, real payment, and advanced RAG/agent models.

## Final Status
This document is a complete draft of the Phase 1 Data Model and authoritative
source for Alembic migrations in C0/C1 implementation.
