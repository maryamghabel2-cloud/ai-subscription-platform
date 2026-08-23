# Phase 1 Data Model

## Document Control
**Title:** Phase 1 Data Model
**Status:** Draft (Part 1 of 4 — Parts 2, 3, 4 pending)
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

## Document Status: Part 2 of 4 Complete

This document contains Document Control, Overview, Principles, Section 1 Core
Tables, and Section 2 Wallet/Ledger Tables.

Pending in Part 3: Feature Tables. Pending in Part 4: Indexes, retention,
migrations, and C0/C1 items.
