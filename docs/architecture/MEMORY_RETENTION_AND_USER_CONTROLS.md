# Memory, Retention, and User Controls

**Version:** v0.1.0

**Date:** 2026-07-29

**Status:** Proposed Architecture - Pending Owner Approval and Implementation

**Document Owner:** Architecture / Privacy / Security

## 1. Purpose and Status

- Proposed architecture only; it does not prove memory, retention jobs, or deletion pipelines are implemented.

- It serves individual privacy, business knowledge, creator delivery, and future agent context.

- Implementation needs separate code, tests, security, privacy, legal, and product review.


## 2. Memory Levels and Scopes

- L-M1: current message context; default on per request; conversation owner can delete.

- L-M2: conversation history; default on; conversation owner can delete.

- L-M3: cross-conversation user memory; strictly opt-in; user can forget or disable.

- L-M4: workspace/business knowledge; workspace scoped; workspace admin controls access.

- L-M5: agent operational context; default off unless approved; tenant owner controls it.


## 3. Canonical Domain Concepts

- Memory Item: stored contextual fact or reference.

- Memory Source: conversation, asset, document, or approved workspace record.

- Provenance: source, reason, extractor, and confirmation metadata.

- Retention Class: policy category rather than feature-specific duration.

- Forget Request: exclusion from future retrieval.

- Deletion Evidence: metadata proving lifecycle action without raw content.


## 4. Individual User Memory

- Conversation history is on by default.

- Cross-conversation memory is strictly opt-in.

- Sensitive-topic memory requires explicit confirmation.

- Users can view, edit, export, forget, and disable memory.

- No silent memory writes are allowed.

- Memory extraction must be reviewable.


## 5. Business and Workspace Memory

- Workspace-scoped knowledge bases may use business documents, FAQs, and catalogs.

- Role-based access applies within a workspace.

- Member removal removes access to workspace memory.

- Workspace deletion cascades to dependent knowledge references.

- Business memory is not personal memory.


## 6. Agent Context Memory

- Support and sales agents have bounded customer-context rules.

- Customer PII is minimized in agent memory.

- Per-customer forget requests are supported.

- Agent memory reads and writes are auditable.

- Agent memory never crosses tenants or customers.


## 7. Creator Marketplace Records

- Brief history and delivery package retention are distinct.

- Rights and consent records may require longer-lived retention classes.

- Dispute-window handling is an Open Decision.

- Creator portfolio references are separate from private chat memory.


## 8. Retention Policy Framework

- Use CONFIGURED_CONVERSATION_RETENTION.

- Use CONFIGURED_TRANSCRIPT_RETENTION.

- Use CONFIGURED_RAW_AUDIO_RETENTION.

- Use CONFIGURED_ASSET_SOURCE_RETENTION.

- Use CONFIGURED_ASSET_FINAL_RETENTION.

- Use CONFIGURED_MEMORY_ITEM_RETENTION.

- Use CONFIGURED_RIGHTS_RECORD_RETENTION.

- Use CONFIGURED_AUDIT_LOG_RETENTION.

- Use CONFIGURED_DELETED_GRACE_PERIOD.

- Backup expiry interacts with deletion; legal hold remains an Open Decision.


## 9. User Control Surface

- View my memory.

- Edit memory item.

- Forget specific item.

- Forget conversation.

- Export my data.

- Disable memory features.

- Workspace admin controls.

- Per-agent memory toggle.


## 10. Deletion and Forget Semantics

- Soft delete is recoverable within configured grace policy.

- Hard delete removes eligible stored content.

- Forget excludes memory without necessarily deleting source.

- Cascade deletion includes derived assets, embeddings, and indexes.

- Forget invalidates embedding and index retrieval.

- Provider deletion requests are used where supported.

- Deletion evidence is metadata.


## 11. Memory Provenance and Trust

- Every memory item records source and reason.

- Sensitive extracted memory remains untrusted until confirmed.

- A model must not claim to remember what is not stored.

- False-memory fabrication is prohibited.

- Provenance is visible to the user where appropriate.


## 12. Cross-Boundary Isolation Rules

- Cross-tenant memory access is forbidden.

- Cross-workspace leakage is forbidden.

- Personal memory must not leak into business context.

- Business memory must not leak into personal chats without membership.

- Agent memory must not cross customers.

- Creators cannot see brand-private memory beyond brief scope.


## 13. Provider and Model Interaction

- Memory injection into prompts is scoped and minimal.

- Provider retention and training policy require disclosure.

- No long-term memory storage at provider by default.

- Embedding storage location and deletion are tracked.

- Design remains provider-neutral.


## 14. Compliance and Legal Boundaries

- Support data-subject access, export, and delete requests.

- Iranian and international considerations remain Open Decisions.

- Children and minor data remain an Open Decision.

- Breach notification links to incident response.

- This document does not invent legal procedures.


## 15. Proposed Implementation PR Sequence

- 1. memory item and provenance metadata model

- 2. conversation retention flags

- 3. user memory control API

- 4. forget/exclusion mechanics

- 5. workspace knowledge base model

- 6. embedding lifecycle hooks

- 7. deletion cascade jobs

- 8. agent context boundaries

- 9. export pipeline

- 10. admin/workspace controls UI later

- Every PR requires tests and rollback planning.


## 16. Open Decisions

- default retention values per class

- memory extraction model policy

- embedding store choice

- export format

- legal hold

- minors policy

- provider deletion verification

- business-customer data-processing terms

### Related Documents

- [DATA_PROTECTION_AND_ENCRYPTION.md](../security/DATA_PROTECTION_AND_ENCRYPTION.md)
- [MULTIMODAL_MEDIA_ASSET_AND_JOB_FOUNDATION.md](MULTIMODAL_MEDIA_ASSET_AND_JOB_FOUNDATION.md)
