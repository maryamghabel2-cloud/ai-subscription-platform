# Produkt Vision - Persian AI Platform

**Version:** v2 - Product Identity Audit
**Date:** 2026-07-23
**Status:** Proposed Product Architecture — Pending Owner Approval
**Decision Owner:** Founder (pending Project Manager review)

## Vision Statement - Updated Identity

Build a Persian-first multimodal AI Workspace and
Professional Creative Studio.

It helps Iranian creators, businesses, developers, students,
and everyday users work smarter with AI - from general chat
and source-grounded study to professional image and video
production and business automation.

We are not a subscription reseller.

We are a product platform with our own user accounts,
wallet and credit billing, extensible Role and Persona system,
Studio workflows, Agent system, and growth loops.

## Product Identity

**Official Identity:**
Persian-first multimodal AI Workspace and
Professional Creative Studio

**What it means:**

- **Multimodal:** Text chat, voice input and output, file, image,
  and PDF attachments, image generation, video generation,
  study workspace with sources.

- **Persian-first:** RTL layout, Persian primary navigation,
  Persian forms and error messages, Persian-compatible typography,
  mobile-first, but global-quality AI models via provider abstraction.

- **Workspace:** Unified billing via wallet and credits,
  memory policy per Role, conversation history, file attachments,
  prompt enhancer, study workspace.

- **Professional Creative Studio:** Core revenue product,
  not minor side feature. Structured workflows for professional
  image and video creation.

## What the Platform Includes

- **General AI chat** - Persian-first, user-selectable models,
  automatic model routing.

- **User-selectable models** - User can choose preferred model
  within allowed range.

- **Automatic model routing** - System may route to best model
  for task (fast for simple chat, stronger for research).

- **Custom Roles and specialist Personas** - Extensible registry-based
  Role system. Adding new Role should not require changing core chat
  logic.

- **Voice input and output** - Speech-to-text and text-to-speech
  for accessibility and mobile.

- **File, image, and PDF attachments** - Upload for analysis,
  RAG, product photography.

- **Professional Prompt Enhancer** - Enhances user prompts.

- **Professional Image Studio** - Core revenue product.
  Structured workflow for professional image creation.

- **Professional Video Studio** - Core revenue product.
  Structured workflow for video creation.

- **Source-Grounded Study Workspace** - Upload PDFs and docs,
  ask questions with citations, RAG attachment.

- **Deep Research Agents** - Multi-step research workflows
  with sources and evidence grading.

- **Immigration Research Agent** - Future specialist persona
  for general immigration information (evidence-based,
  not legal advice).

- **Mobile application** - Native or PWA, Persian-first,
  voice, camera for product photography.

- **Privacy-aware Telegram integration** - User connects bot
  via encrypted token, bot runs business agents,
  privacy-aware: token encrypted at rest, no secret in logs,
  anti-spam, no bulk without approval.

- **Developer APIs** - Own APIs for chat, image, RAG,
  with API keys (hashed), scopes, rate limiting, usage logs.

- **Prompt Marketplace** - Future idea: user-created prompts,
  with review.

- **Agent Marketplace** - Future idea (Phase 8): user-created
  business agents, with review and rev-share.

## Professional Image and Video Studios - Core Revenue Products

**Studios are core revenue products, not minor side features.**

They are structured workflows, not simple Roles.

**Image Studio is not limited to Instagram or e-commerce product photos.**

Supported future use cases must include:

- Product photography - e-commerce, catalog
- Advertising campaigns - ad creatives, variants
- Posters, Banners - marketing materials
- Social media assets - Instagram, Telegram, etc.
- Website assets - hero images, backgrounds
- Artistic images - creative, conceptual
- Brand concepts - logo concepts, brand mood boards
- Background replacement - remove or replace background
- Image editing - crop, adjust, retouch
- Inpainting and outpainting - fill missing, extend image
- Upscaling - increase resolution
- Text-to-video - prompt to video
- Image-to-video - animate image
- Product advertisements - video ads from product photos
- Brand videos - brand story
- Educational videos - explainer, tutorial
- Storyboards - for video planning
- Character workflows - consistent character across images and videos
- Voice-over and subtitles - for video

**Studio Workflow Definition:**

Structured image and video generation workflow with steps:

- Upload or select
- Settings (model, style, aspect ratio, etc.)
- Prompt enhance
- Generate
- Review
- Edit with inpaint, outpaint, upscaling
- Select and download

Must not be incorrectly classified as a simple Role.

See `ROLE_PERSONA_AGENT_BOUNDARIES.md`.

## Problem Summary

- Persian users face language, payment, and access barriers
  to global AI tools.

- Existing tools are fragmented: chat here, image there,
  video elsewhere.

- No unified billing, no Role system tailored for Persian
  business context and personal preferences.

- No simple way for businesses to deploy Telegram agents
  or product studios.

- No professional studio workflows for creators - need guided,
  not just prompt box.

## Solution Principles (Updated)

1. **Persian-first multimodal UX** but global-quality AI
   via provider abstraction.

2. **Credit-based billing** via wallet - simple, transparent,
   no shared accounts, atomic and idempotent,
   balance never negative.

3. **Extensible Role and Persona system** - ordinary Roles
   (conversation-only) and specialist Personas (versioned,
   evidence-aware, domain-specific, still conversation-only,
   may use approved knowledge retrieval, no autonomous external actions).

4. **Professional Creative Studio as core revenue**
   - Not side feature.

5. **Accuracy and Creativity control** - User-friendly label
   "Accuracy and Creativity" Persian "دقت و خلاقیت" with modes
   strict_factual, balanced, creative - not "hallucination level".

6. **Telegram and Business Agents** - low-code agents that run
   in Telegram or business workflows, privacy-aware.

7. **Developer API Platform** - own APIs for chat, image, RAG
   with hashed keys, scopes, rate limiting.

8. **Agent Operating System** for building the product itself
   (external agents now L1 report/draft and L2 branch+PR,
   internal later L3/L4 with approval gates).

## What This Platform Is Not (De-scoped Legacies)

- Not a reseller of shared Netflix or GPT accounts
  - Deprecated model, archived to branch
    `archive/legacy-code-2026-07-19`.

- Not automated procurement from GGSel or FunPay
  - Deprecated, no scraping.

- Not crypto payment at Phase 0/1
  - Credit wallet planned.

- No bypassing provider ToS, KYC, geographic pricing tricks,
  sanctions - absolutely forbidden, no approval may authorize.

- No shared consumer accounts, no API-key resale violating ToS.

- Not a generic compassionate companion for mental health
  - Psychologist is future evidence-based structured direct
    assistant with clear boundaries, not therapist.

## Success Metrics (North Star)

- **Activation:** User signs up → completes onboarding asking
  preferred Role and communication style → completes first chat
  with Normal Assistant → buys credits → uses studio.

- **Retention:** Weekly active users who use 2+ tools
  (chat + studio, or chat + persona).

- **Business:** Credit purchase conversion, LTV, referral loop,
  studio usage as revenue engine.

## Non-Goals for Phase 0 / Audit Phase

- Building production AI models from scratch
  - Use provider abstraction.

- Medical, legal, or psychological diagnosis
  or authoritative advice
  - Only evidence-based information with disclaimer and escalation.

- Fully autonomous agents that spend money or publish
  without human approval
  - All spending and publishing requires approval.

- Real AI provider integration in this audit PR
  - Documentation only.

## Linkage

- Roadmap: `docs/roadmap/MASTER_ROADMAP.md`
- Agent OS: `docs/agents/AGENT_OPERATING_SYSTEM.md`
- Roles and Personas: `docs/architecture/ROLE_AND_PERSONA_SYSTEM.md`
  and `ROLE_PERSONA_AGENT_BOUNDARIES.md`
- Agent Execution: `docs/architecture/AGENT_PLUGIN_AND_EXECUTION_SYSTEM.md`
- Personas: `docs/personas/PERSONA_FRAMEWORK.md`
  (with mandatory evidence fields)
- Accuracy and Creativity:
  `docs/architecture/ACCURACY_CREATIVITY_CONTROL.md`
- Safety: `docs/safety/TRUST_AND_SAFETY_FRAMEWORK.md`
