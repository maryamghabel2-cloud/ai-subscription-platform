# Multimodal Chat, Voice, and Streaming

**Version:** v0.1.0

**Date:** 2026-07-29

**Status:** Proposed Architecture - Pending Owner Approval and Implementation

**Document Owner:** Architecture / Product / Security

## 1. Purpose and Status

This is proposed architecture only. It does not prove chat, voice, streaming,
uploads, providers, queues, or frontend components are implemented. This layer
depends on the secure media asset/job foundation and serves workspace UX and
commercial studio workflows.

## 2. Supported User Journeys

Future journeys include text-only Persian chat, chat with image or PDF/document
attachment, voice note to text interaction, optional text-to-speech playback,
chat handoff to Reels/Product/UGC workflows, studio outputs returned into a
conversation, and future agent-assisted workflow initiation.

External publishing is not included in these journeys.

## 3. Canonical Domain Concepts

- **Conversation:** tenant-owned ordered interaction container.
- **Message:** structured user, assistant, system, tool, or event record.
- **Message Role:** authorization-aware origin category for a message.
- **Message Part:** typed text, citation, attachment, event, or tool payload.
- **Attachment Reference:** permissioned message pointer to a media asset version.
- **Voice Note:** user-provided audio asset intended for transcription.
- **Transcript:** derived text associated with a voice/audio asset.
- **Streaming Session:** bounded delivery channel for partial response events.
- **Tool/Event Message:** visible, structured status rather than hidden side work.
- **Studio Handoff Intent:** structured draft to start a commercial studio flow.
- **Reviewable Output:** user-visible draft or asset requiring review as applicable.
- **Delivery Message:** message containing approved output references.

## 4. Conversation and Message Model

A message model supports text parts, image/video/audio/PDF/document references,
system/assistant/user/tool/event roles, message status, revision/regeneration
relationships, citation metadata, and handoff metadata.

Raw files are assets, not message bodies. Message references point to assets, and
cross-tenant reuse is forbidden. Every reference requires tenant and ownership
checks at read time.

## 5. Attachment and Asset References

Require message-to-asset linking, attachment ownership, reviewable previews,
transcript/caption association, asset-version references, and signed-access
boundaries. Deleted assets in old conversations show a safe unavailable state.
Raw signed URLs must not appear in logs.

Attachment ingestion follows
[MULTIMODAL_MEDIA_ASSET_AND_JOB_FOUNDATION.md](MULTIMODAL_MEDIA_ASSET_AND_JOB_FOUNDATION.md),
not a separate ad hoc upload path.

## 6. Voice Note Input Boundary

Future support includes user-recorded Persian voice notes, speech-to-text,
transcript review where appropriate, noisy-audio handling, unsupported-language
detection, and consent/retention boundaries.

Raw audio is not retained forever by assumption. Transcript retention depends on a
later retention policy. Provider choice remains open. Voice-note upload uses the
media foundation.

## 7. Speech Output Boundary

Optional Persian text-to-speech playback may generate a per-message playback
artifact. It does not assume autoplay. Playback is a generated asset with
accessibility value, cost awareness, and provider neutrality.

## 8. Streaming Response Model

Streaming supports token/text events, structured events, partial assistant output,
interruption, cancellation, regeneration, handoff updates, and completion states.

Streaming does not imply persistence until completion policy decides. User-visible
partial output may differ from final stored message. Streaming cannot hide
background write actions.

## 9. Chat-to-Studio and Studio-to-Chat Handoff

A user expresses intent in chat; the system generates a structured handoff draft;
the user reviews/approves where needed; a studio job ID returns to the conversation;
progress appears as event messages; and final outputs return as reviewable asset
references.

Examples include "turn this raw clip into 3 Reels", "make product photos for this
item", and "turn these product assets into an ad video". Studio initiation is L2
draft or L3 Approval Write depending on the action.

## 10. Multimodal Safety and Trust Boundaries

Transcripts, OCR text, file metadata, captions, and subtitles are untrusted input.
They must not become trusted instructions. Apply moderation boundaries for text,
image, audio, and video; impersonation, likeness, and consent checks; and the rule
that model output alone cannot authorize sensitive action.

See [PROMPT_INJECTION_DEFENSE.md](../security/PROMPT_INJECTION_DEFENSE.md).

## 11. Privacy, Logging, and Retention Boundaries

Use metadata-only logs by default. Do not log raw audio, full transcript, or raw
prompts in technical logs. Conversation retention is separate from asset retention,
and transcript retention is separate from raw audio retention.

Workspace/project deletion must account for both messages and referenced assets.
Future memory policy is separate. Do not hardcode retention periods.

## 12. Billing and Usage Hooks

Future hooks cover text usage, speech-to-text, text-to-speech, attachment-related
processing, studio handoff estimates, and reserve/settle references. This document
does not implement billing.

### Usage Attribution Rules

Usage records must attribute text, speech, attachment, and studio handoff activity
to the tenant, conversation, message, and applicable job without recording raw
content. Estimates are reviewable before a billable studio workflow where required.
A failed or cancelled operation must preserve enough metadata for fair settlement
review without exposing provider credentials or internal traces.

### Notification Boundary

Chat event messages may notify a user about progress while the conversation is
open. Future push, email, Telegram, or other external notification delivery is a
separate product decision and must not be inferred from chat streaming support.

## 13. Accessibility and Persian-First UX

Require RTL-safe chat rendering, mixed Persian/English handling, readable code/log
blocks, Persian punctuation/numeral considerations, transcript and subtitle
readability, screen-reader support, and no autoplay assumption.

## 14. Error Handling and Fallback Behavior

Handle missing upload references, failed transcripts, unsupported media, streaming
interruption, unavailable providers, rejected handoffs, deleted assets, and user
cancellation. User messages must be fair and actionable without leaking provider
or scanner internals.

### Interaction Event Rules

Streaming events must have a conversation ID, message ID, session ID, event type,
sequence reference where applicable, and tenant boundary. Clients may reconnect,
but reconnection does not grant access to another tenant's session.

Event types may include started, text_delta, citation_available, tool_status,
handoff_draft, job_progress, partial_output, completed, cancelled, and failed.
An event is not a durable authorization grant.

### Review and Regeneration Rules

Regeneration creates a related message revision rather than overwriting audit
history. A user can discard a draft, request another draft, or approve a handoff.
Approval must identify the reviewed scope; approving a caption draft does not
authorize external publishing or a different studio job.

### Agent Interaction Boundary

Future business Agents can initiate a structured handoff intent, but must not
silently send messages, publish content, spend credits, or start high-impact studio
jobs. Agent-initiated actions follow the same tenant, approval, audit, cancellation,
and output-policy boundaries as user-initiated actions.

### Citation and Provenance Boundary

Citations, transcript confidence, OCR source references, and studio result
provenance are message metadata. They should allow users to understand source and
transformation context without exposing private provider prompts, credentials, or
other tenants' data.

### Security Test Expectations

Future tests include cross-tenant attachment rejection, expired signed reference
rejection, transcript prompt-injection tests, cancellation races, reconnect safety,
partial-output handling, and event ordering. Tests must cover Persian and mixed
RTL/LTR rendering where relevant.

## 15. Proposed Implementation PR Sequence

1. Conversation/message metadata model.
2. Attachment reference model.
3. Text streaming transport.
4. Voice-note upload and transcript stub.
5. TTS playback artifact stub.
6. Event-message and progress model.
7. Chat-to-studio handoff draft model.
8. Frontend chat attachment rendering.
9. Voice UX later.
10. Commercial studio integration later.

Each future PR requires tests, security review, and rollback planning.

## 16. Open Decisions

- conversation persistence model
- transcript review UX
- voice autoplay
- STT/TTS provider shortlist
- transcript retention
- event-stream transport choice
- partial message persistence policy
- chat attachment preview policy
- subtitle delivery format
- multilingual switching behavior

### Related Documents

- [COMMERCIAL_AGENT_SKILL_AND_CREATOR_PLATFORM_DECISIONS.md](../product/COMMERCIAL_AGENT_SKILL_AND_CREATOR_PLATFORM_DECISIONS.md)
- [DATA_PROTECTION_AND_ENCRYPTION.md](../security/DATA_PROTECTION_AND_ENCRYPTION.md)
- [LOGGING_AND_MONITORING.md](../security/LOGGING_AND_MONITORING.md)
- [IDENTITY_AND_ACCESS_CONTROL.md](../security/IDENTITY_AND_ACCESS_CONTROL.md)
