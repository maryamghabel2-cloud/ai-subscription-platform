# Image and Video Studios

**Version:** v0.1.0

**Date:** 2026-07-29

**Status:** Proposed Architecture - Pending Owner Approval and Implementation

**Document Owner:** Architecture / Studio / Security

## 1. Purpose and Status

- Proposed architecture only; no rendering, queues, providers, billing, publishing, or frontend is implemented.

- Builds on media asset/job and multimodal chat architecture.


## 2. Studio Product Scope

- Covers self-service image/video studio workflows.

- Covers reviewable outputs, draft generation, export/download, and optional approved publishing.

- Does not define creator marketplace fulfillment, prompt marketplace monetization, agent marketplace runtime, payment, or escrow.

| Workflow | Input | Output | Primary buyer | First autonomy level |
|---|---|---|---|---|
| Reels and Shorts Auto Editor | raw video/audio | reviewable short-form variants | creators, shops | L2 draft |
| Product Photography Studio | product images | professional product-photo variants | e-commerce sellers | L2 draft |
| Product-to-Video Ad Generator | product images/URL/description | ad video drafts | shops, marketers | L2 draft |

Internal generation/editing is L1/L2. External publishing is L3 Approval Write.
Scheduled auto-publishing is not enabled in v1.


## 3. Shared Studio Workflow Model

- brief

- prompt enhancement

- asset selection

- job estimation

- credit reservation hook

- processing

- reviewable output set

- user approval

- export / publish / handoff

- Studio Project, Creative Brief, Variant Set, Render Job, Review Stage, Approval Action, and Delivery Package are shared concepts.


### Provider Abstraction Boundary

- Use provider-neutral media adapters.
- Declare capabilities per operation.
- Record privacy classification and training/retention policy.
- Do not silently fall back in a way that weakens privacy or raises cost.
- Do not select a provider in this document.

### Job Lifecycle Boundary

- Reuse media job foundation states.
- Support multi-step studio progress, cancellation, and partial outputs.
- Bound retries with CONFIGURED_STUDIO_JOB_TIMEOUT,
  CONFIGURED_STUDIO_MAX_VARIANTS, and CONFIGURED_STUDIO_MAX_DURATION.
- Do not use concrete numeric values.

## 4. Reels and Shorts Auto Editor

- raw clip ingestion

- silence/filler detection

- transcript generation

- Persian subtitle and caption overlay

- hook/title variants

- highlight extraction

- aspect-ratio conversion

- optional B-roll insertion

- CTA suggestions

- preview set for review

- No direct publishing without approval. Music choice remains Open Decision. Subtitle rendering must be Persian/RTL safe.


## 5. Product Photography Studio

- source image upload

- background removal

- scene prompt selection

- lighting/shadow harmonization

- e-commerce neutral shot

- lifestyle/ad shot

- platform-specific crops

- upscaling

- before/after review

- Source ownership or permission is required. Generated scenes must not misrepresent product characteristics.


## 6. Product-to-Video Ad Generator

- product URL, source images, or structured product input

- selling-point extraction

- script/hook generation

- scene ordering

- text overlay plan

- voiceover plan

- visual motion plan

- ad variant generation

- review before export or publishing

- Product and comparative claims require review. Generated ad drafts are not auto-published.


## 7. Brand Kit and Style Controls

- logo

- palette

- font policy

- tone-of-voice

- CTA style

- do/do-not constraints

- workspace-level brand presets

- Brand kit is workspace-scoped. Font security and licensing remain Open Decisions.


## 8. Prompt Enhancer and Creative Brief Flow

- A user brief may be vague.

- The system may generate a clearer prompt draft.

- Users may preview or edit enhanced prompts.

- Expensive render paths show estimate before execution.

- Prompt enhancement does not publish or spend without the defined flow.


## 9. Output Variants and Review Workflow

- variant grouping

- thumbnail/previews

- rating/selection

- reject/regenerate path

- version history

- variant comparison

- return to chat/workspace context

- delivery package for creator/brand review


## 10. Export and External Publishing Boundary

- Local export/download is allowed if output exists.

- External publishing is an L3 Approval Write action.

- Publish targets are future integrations only.

- Approval actor is recorded.

- No silent auto-posting.


## 11. Rights, Consent, and Likeness Controls

- creator consent tracking

- rights record for uploaded/generated assets

- no non-consensual likeness use

- no deceptive deepfake-like workflow

- brand usage restrictions

- UGC and human creator rights preserved for later marketplace use


## 12. Billing and Cost Estimation Hooks

- estimate before render

- reserve/settle/refund integration point

- separate image, video, audio, and transcript cost drivers

- variant count affects estimate

- No billing implementation in this PR.


## 13. Safety and Abuse Controls

- moderation boundary for generated media

- NSFW and exploitative content controls

- likeness misuse detection

- counterfeit or trademark misuse review

- prompt injection resistance for uploaded text/transcripts

- abuse metadata to Security Agent

- Trust & Safety review dependency; no legal-policy hardcoding.


## Persian-First and RTL Requirements

- Require Persian caption quality for Reels/Shorts.
- Use RTL-safe text layout in images and video overlays.
- Support Persian fonts for captions and ad copy.
- Handle mixed Persian/English text.
- Support Persian ad-copy tone variants such as formal and casual.
- Persian voiceover quality remains a provider Open Decision.
- Do not render reversed or broken Persian characters in media.
- Maintain an evaluation set for Persian caption and ad-copy quality.

## 14. Proposed Implementation PR Sequence

- 1. studio project metadata model

- 2. creative brief and variant-set model

- 3. product photography pipeline stub

- 4. reels pipeline stub

- 5. product-to-video pipeline stub

- 6. prompt enhancer integration

- 7. review and approval state model

- 8. export package and download API

- 9. publish integration later

- 10. brand kit storage later

- All PRs require tests and rollback plans.


## 15. Open Decisions

- render engine choice

- licensed music handling

- subtitle rendering engine

- ad-claim policy review

- creator-rights metadata model

- watermark policy

- export resolution policy

- image/video provider shortlist

- publish target priority

- brand-font upload policy

### Related Documents

- [MULTIMODAL_MEDIA_ASSET_AND_JOB_FOUNDATION.md](MULTIMODAL_MEDIA_ASSET_AND_JOB_FOUNDATION.md)
- [MULTIMODAL_CHAT_VOICE_AND_STREAMING.md](MULTIMODAL_CHAT_VOICE_AND_STREAMING.md)
