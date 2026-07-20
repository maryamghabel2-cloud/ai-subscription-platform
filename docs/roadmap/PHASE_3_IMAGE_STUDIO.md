# Phase 3 - Image Studio & Product Photography

**Phase:** PHASE_3_IMAGE_STUDIO  
**Date:** 2026-07-19  
**Status:** Planned (Phase 0 is current)

## Objective
Image generation + guided product photography studio for creators.

## In Scope
- Image generation (prompt→image)
- Product Photography Studio: upload product, choose background, lighting, get 5 variants
- Credit cost per image

## Out of Scope
Video, character tools, Telegram agents

## Dependencies
Phase 1 wallet, Phase 2 persona pattern reusable for Product Photography Advisor

## Technical Deliverables
- Image model API wrapper (external provider for MVP, not training)
- Studio workflow state machine: upload → prompt enhance → generate → select
- Storage: S3 compatible (for MVP local volume)
- Background removal optional

## UX Deliverables
- Studio UI: upload, settings, gallery, download
- Before/after slider
- Product Photography Advisor persona embedded

## Business Deliverables
- Studio pack credit pricing
- Referral: share result

## Required Agents
UX Product Design, Brand Visual Identity, ML Inference Engineer, Model Evaluation, Trust & Safety, Data Privacy Governance, Localization & Accessibility, SRE Incident Response + existing
Fullstack Builder, Prompt Engineer, Research (product photo best practices), Growth Marketing (SEO for studio)


**Additional per review (new 8 agents):** UX Product Design, Brand Visual Identity, ML Inference Engineer, Model Evaluation, Trust & Safety, Data Privacy Governance, Localization & Accessibility, SRE Incident Response

## Test Requirements
- Upload 2MB image, generate, download
- NSFW filter test
- Credit deduction idempotent

## Risk Controls
- Copyrighted style prompts → block
- NSFW → filter
- Cost overrun → per-image cost cap
- All human approval gates from HUMAN_APPROVAL_GATES.md must apply: spending money, publishing, contacting customers, changing prices/config, merging, deploying, API keys, persona changes, paid campaigns, refunds/credits above threshold require human approval.
- Audit logs required for all state-changing actions.
- No medical/legal/psychological authoritative claims.

## Exit Criteria
Creator can upload product photo and get 5 studio results, billed, downloadable