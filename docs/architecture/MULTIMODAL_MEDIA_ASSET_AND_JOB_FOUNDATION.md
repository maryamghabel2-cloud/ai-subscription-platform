# Multimodal Media Asset and Job Foundation

**Version:** v0.1.0

**Date:** 2026-07-29

**Status:** Proposed Architecture - Pending Owner Approval and Implementation

**Document Owner:** Architecture / Security / Product

## 1. Purpose and Status

This is proposed architecture. It does not prove uploads, media processing,
storage, queues, or providers are implemented. It supports AI self-service and
creator-assisted delivery. Implementation requires separate code, tests, security
review, privacy review, legal review, and provider selection.

## 2. Supported Product Outcomes

Future outcomes include raw video to reviewable Reels/Shorts output, product image
to professional product-photo variants, product assets to product-ad video drafts,
UGC creator upload/review/revision/delivery, and chat image, audio, video, PDF,
and general-file attachments. External publishing is not part of this foundation.

## 3. Canonical Domain Concepts

- **Media Asset:** tenant-owned source or generated binary/content object.
- **Upload Session:** authenticated, short-lived permission to submit one asset.
- **Asset Version:** immutable revision of an asset.
- **Asset Variant:** derived rendition, such as preview, thumbnail, or caption.
- **Processing Job:** asynchronous stateful request to transform or analyze input.
- **Job Input/Output:** versioned asset references consumed or produced by a job.
- **Provider Execution Record:** metadata about a provider operation and result.
- **Consent Record:** evidence of applicable user, creator, or likeness consent.
- **Rights and License Record:** evidence of permitted asset use and delivery.
- **Delivery Package:** approved set of final assets and related rights metadata.

Every asset, version, job, and delivery package is bound to a tenant and owner.
No asset reference authorizes cross-tenant access.

## 4. Asset Types

Supported types may include image, video, audio, PDF, text document, general
attachment, generated asset, edited asset, creator-delivered asset, thumbnail,
preview, caption, transcript, and subtitle file.

## 5. Asset Lifecycle

Lifecycle states are initiated, uploading, uploaded, quarantined, scanning,
accepted, rejected, processing, available, archived, deletion_pending, and
deleted. Deletion of a source asset must account for derived variants, backups,
provider copies, and delivery packages.

## 6. Secure Upload Pipeline

Require authenticated upload sessions; tenant/user ownership binding; short-lived
signed upload URLs; byte-size enforcement; MIME sniffing; extension/MIME
consistency checks; checksums; malware scanning; decompression-bomb protection;
media-parser hardening; quarantine before processing; metadata and EXIF handling;
and rejection reasons that do not leak scanner details.

No public bucket access is allowed. Raw asset content must not appear in technical
logs.

## 7. Semantic File and Duration Limits

Use only these undecided semantic limits:

- CONFIGURED_CHAT_IMAGE_MAX_BYTES
- CONFIGURED_CHAT_FILE_MAX_BYTES
- CONFIGURED_STUDIO_IMAGE_MAX_BYTES
- CONFIGURED_STUDIO_VIDEO_MAX_BYTES
- CONFIGURED_AUDIO_MAX_BYTES
- CONFIGURED_VIDEO_MAX_DURATION
- CONFIGURED_AUDIO_MAX_DURATION
- CONFIGURED_PDF_MAX_BYTES
- CONFIGURED_UPLOAD_SESSION_LIFETIME

Chat limits and Studio limits are separate policies.

## 8. Media Job Lifecycle

Job states are draft, estimating, awaiting_credit_reservation, queued, processing,
awaiting_user_review, succeeded, partially_succeeded, failed,
cancellation_requested, cancelled, and quarantined.

Jobs require idempotency, progress reporting, cancellation, timeout, retry policy,
safe partial results, failure-reason classification, and no unlimited retries.

## 9. Reels and Shorts Processing Boundary

A future reviewable pipeline may include ingestion, scene/silence analysis,
transcript, Persian captions, RTL caption layout, hook/highlight/cut/B-roll
suggestions, aspect-ratio transformation, brand-kit application, CTA draft, and
output variants. Music licensing remains an Open Decision; copyrighted music must
not be assumed available.

Internal media transformation may be automatic. External publishing is a separate
L3 Approval Write action requiring approval.

## 10. Product Photography and Product-to-Video Boundary

Future support may include background removal/replacement, professional product
photo variants, marketplace/social aspect ratios, enhancement, product-to-video
drafts, advertising concepts, product-focused B-roll, and brand-safe variants.

Require source-image ownership or permission, no misleading product claims, no
unapproved person likeness, version history, and user review before commercial
publication.

## 11. UGC and Creator Delivery Boundary

The delivery flow includes business brief, creator match reference, creator upload,
AI-assisted QA, revision request, approved delivery package, usage-rights metadata,
and consent/license evidence.

Marketplace payment and escrow are not implemented here. Creator content must not
be used outside agreed rights. AI enhancement must preserve creator and brand
consent records.

## 12. Storage and Encryption

Require private object storage, encryption at rest, TLS in transit, tenant-scoped
object keys, short-lived signed access, provider-neutral envelope encryption for
approved highly sensitive assets, key-version metadata, and backup/restore
considerations. These controls are not claimed as already implemented.

See [DATA_PROTECTION_AND_ENCRYPTION.md](../security/DATA_PROTECTION_AND_ENCRYPTION.md).

## 13. Privacy, Retention, and Deletion

Use separate retention policies for source, intermediate, final, preview,
transcript, caption, and creator-delivered assets. Require user and workspace
deletion controls, provider-retention disclosure, derivative-asset deletion graph,
backup-expiry handling, and legal hold as an Open Decision. Do not hardcode
retention values.

## 14. Provider Boundary

Require a provider-neutral media adapter with declared modality/operation
capability, privacy classification, retention/training policy, regional
availability, cost estimation, retry/cancellation capability, and versioned
configuration. Do not select or activate a provider. No silent fallback may weaken
privacy or increase cost.

## 15. Billing and Credit Hooks

Future reserve-settle-refund integration is: estimate maximum operation cost,
reserve credits, run processing, measure provider usage, settle actual usage,
refund unused reservation, and handle cancellation/failure fairly. This does not
implement billing.

## 16. Observability and Audit

Use metadata-only logs: job ID, asset ID, tenant ID, operation, lifecycle
transition, provider identifier, pricing version, result status, error class,
cancellation actor, and approval actor. Do not log raw media, full transcripts,
prompt secrets, credentials, or signed URLs.

## 17. Security and Abuse Controls

Require tenant-isolation, file-type bypass, malware/decompression, signed-URL
expiry, cross-user access, cancellation, and output-policy tests. Include
non-consensual intimate imagery controls, CSAM reporting/handling requirements,
impersonation/likeness-consent controls, and prompt-injection handling for
transcripts and metadata.

Jurisdiction-specific handling is an Open Decision requiring legal and Trust &
Safety review; this document does not invent legal procedures.

## 18. Proposed Implementation PR Sequence

1. Asset metadata models and migration.
2. Upload-session API with local test storage.
3. Quarantine and scan-state workflow.
4. Private object-storage adapter.
5. Media-job models and state machine.
6. Queue abstraction and synthetic worker.
7. Progress and cancellation API.
8. Cost estimate and credit reservation hook.
9. Image processing adapter.
10. Video processing adapter.
11. Persian transcript and caption adapter.
12. Secure download and delivery package.
13. Frontend uploader and job-progress UI.
14. Reels Studio workflow later.
15. Product Photography workflow later.

Each future PR requires tests and rollback plans.

## 19. Open Decisions

- storage provider
- queue technology
- malware scanner
- media processing runtime
- image provider shortlist
- video provider shortlist
- speech-to-text provider shortlist
- maximum file sizes
- maximum duration
- retention by asset class
- music licensing
- UGC usage-rights model
- creator delivery format
- export resolution
- watermark policy
- geographic processing constraints
- creator revision and dispute evidence
- transcript language-detection policy
- asset classification escalation workflow

## Related Documents

- [DATA_CLASSIFICATION_AND_RETENTION.md](DATA_CLASSIFICATION_AND_RETENTION.md)
- [PROVIDER_ABSTRACTION_STRATEGY.md](PROVIDER_ABSTRACTION_STRATEGY.md)
- [PRICING_AND_UNIT_ECONOMICS.md](PRICING_AND_UNIT_ECONOMICS.md)
- [PROMPT_INJECTION_DEFENSE.md](../security/PROMPT_INJECTION_DEFENSE.md)
- [LOGGING_AND_MONITORING.md](../security/LOGGING_AND_MONITORING.md)
- [SECURITY_TESTING.md](../security/SECURITY_TESTING.md)
