# DATA CLASSIFICATION AND RETENTION - Phase 0 Governance

**Date:** 2026-07-20
**Status:** Planning doc only

## Purpose
Define what data is collected, classification, retention, deletion, privacy.

## Data Types

- **User Account:** email, hashed_password, is_active, created_at - Classification: Personal Data (PII low), Retention: while account active + 30 days after deletion request, Deletion: hard delete or anonymize after retention
- **Wallet Ledger:** user_id, credit balance, ledger entries (purchase, spend, refund) - Classification: Financial, Retention: 7 years for accounting (adjust per jurisdiction), Deletion: anonymize after retention, not immediate delete
- **Chat Conversations:** user_id, persona_id, messages, model, tokens, cost, timestamps - Classification: User Content + Personal Data, Retention: while account active or until user deletes conversation, user can delete per conversation, Deletion: hard delete messages + associated audit logs? Audit logs retained longer but anonymized? Need Data Privacy Governance agent recommendation
- **Images/Videos Generated:** user_id, prompt, negative prompt, model, storage path, credit cost - Classification: User Content, Retention: while account active or until user deletes, Deletion: delete from storage + DB
- **API Keys:** user_id, prefix, hashed_key, scopes, last_used - Classification: Secret (hashed), Retention: while active, Deletion: hard delete on revoke
- **Telegram Bot Tokens:** user_id, encrypted token, bot_id - Classification: Secret (encrypted), Retention: while bot connected, Deletion: decrypt? Actually hard delete encrypted token on disconnect, audit log that token deleted (not token itself)
- **Audit Logs:** agent_id, action, target, approver, timestamp, result, rollback id - Classification: Operational, Retention: 1 year minimum for security, maybe 7 years for financial actions, Deletion: not user-deletable, anonymize after retention
- **Research Docs Uploaded (Phase 7):** user_id, doc content, embeddings, chunks - Classification: User Content, Retention: while account active or until user deletes, Deletion: hard delete doc + chunks + embeddings
- **Agent Audit Logs (Project-Building):** PRs, reports - Classification: Internal, Retention: Git history forever (not deleted)

## Classification Levels

- **Public:** Blog posts, landing pages, docs - no PII
- **Internal:** Growth reports, experiment backlog (no PII)
- **Confidential:** User content, wallet, API keys hashed, tokens encrypted - need access control
- **Secret:** Raw secrets, API keys, tokens - encrypted at rest, never in logs, never in repo, never in PR

## Retention Schedule (Draft, Needs Data Privacy Governance Agent Review)

- User account: active +30 days after deletion request
- Wallet ledger: 7 years
- Chat: active until user deletes, else active +1 year after account deletion? To be decided with privacy agent
- Images/videos: active until user deletes
- API keys: active until revoked
- Telegram tokens: active until disconnect
- Audit logs: 1 year operational, 7 years financial/security
- Research docs: active until user deletes

## Principles

- Least privilege: only owner user can access own data, admin only with approval and audit?
- No cross-tenant leakage: user A cannot see user B's chats, images, docs - test via IDOR tests
- User can request deletion: need deletion workflow, human approval? For Phase 1 simple delete own conversation, delete account request needs approval?
- No secrets in repo, no secrets in logs, no secrets in PRs
- Encryption at rest for secrets (Fernet future, Vault future)
- Audit logging for data access (future)
- Absolutely forbidden: sharing/reselling unauthorized credentials, hiding prohibited locations, fake identities

## Future Implementation

- Phase 1: User table, no RLS yet, but IDOR tests
- Phase 3: S3 storage with private bucket, signed URLs
- Phase 7: pgvector with user_id filter for RAG, no cross-tenant leakage

## Linkage
- Trust & Safety: TRUST_AND_SAFETY_FRAMEWORK.md
- Provider Abstraction: PROVIDER_ABSTRACTION_STRATEGY.md
- Data Privacy Governance Agent spec
