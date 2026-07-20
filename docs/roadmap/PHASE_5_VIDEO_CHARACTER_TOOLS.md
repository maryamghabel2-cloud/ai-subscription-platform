# Phase 5 - Video & Character Tools

**Phase:** PHASE_5_VIDEO_CHARACTER_TOOLS  
**Date:** 2026-07-19  
**Status:** Planned (Phase 0 is current)

## Objective
Video generation and AI character/influencer workflow (guided, not fully autonomous).

## In Scope
- Text/image→video short clips
- AI character creation: face, voice, script
- Character video workflow

## Out of Scope
Real-time deepfake of real persons without consent, Telegram automation without approval

## Dependencies
Phase 3 image studio pattern, wallet

## Technical Deliverables
- Video model API wrapper
- Async job queue (Celery/ARQ future) for long video renders
- Character asset storage

## UX Deliverables
- Video Studio + Character Studio separate pages
- Progress tracker for render

## Business Deliverables
- Higher credit cost for video

## Required Agents
UX Product Design, ML Inference Engineer, Model Evaluation, Trust & Safety (deepfake consent), Data Privacy Governance, SRE Incident Response + existing
Fullstack Builder, Research, Prompt Engineer, Compliance Risk (deepfake policy)


**Additional per review (new 8 agents):** UX Product Design, ML Inference Engineer, Model Evaluation, Trust & Safety (deepfake consent), Data Privacy Governance, SRE Incident Response

## Test Requirements
- Video job: submit → polling → result
- Character consent check: cannot clone real person without consent checkbox + human review flag

## Risk Controls
- Deepfake misuse → consent gate + human approval for character publish
- Costly video → pre-calc cost, confirm spend
- All human approval gates from HUMAN_APPROVAL_GATES.md must apply: spending money, publishing, contacting customers, changing prices/config, merging, deploying, API keys, persona changes, paid campaigns, refunds/credits above threshold require human approval.
- Audit logs required for all state-changing actions.
- No medical/legal/psychological authoritative claims.

## Exit Criteria
User can generate 5s video and character video, billed, with consent gate