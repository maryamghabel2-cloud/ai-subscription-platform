# Product Vision - Persian AI Platform

**Version:** v2 - Product Identity Audit

**Date:** 2026-07-23

**Status:** Proposed Product Architecture — Pending Owner Approval

**Decision Owner:** Founder (pending Project Manager review)

## Vision Statement

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

### Core Chat and Customization

- **General AI chat** - Persian-first, with user-selectable models,
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

### Professional Studios - Core Revenue Products

- **Professional Image Studio** - Core revenue product.
  Structured workflow for professional image creation.

- **Professional Video Studio** - Core revenue product.
  Structured workflow for video creation.

**Image Studio is not limited to Instagram or e-commerce product photos.**

Supported future use cases must include:

- Product photography - e-commerce, catalog
- Advertising campaigns - ad creatives, variants
- Posters
- Banners
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

### Study and Research

- **Source-Grounded Study Workspace** - Upload PDFs and docs,
  ask questions with citations, RAG attachment.

- **Deep Research Agents** - Multi-step research workflows
  with sources and evidence grading.

- **Immigration Research Agent** - Future separate capability
  (see Immigration Persona vs Agent separation below).

### Channels and Platform

- **Mobile application** - Native or PWA, Persian-first,
  voice, camera for product photography.

- **Privacy-aware Telegram integration**
  - Ordinary end users link their account to the platform's
    Telegram bot.
  - Ordinary users do not provide a bot token.
  - Future business customers may connect their own bot token
    through a separate reviewed integration where the token
    is encrypted at rest.
  - Privacy-aware: token encrypted, no secret in logs,
    anti-spam, no bulk without approval.

- **Developer APIs** - Own APIs for chat, image, RAG,
  with API keys (hashed), scopes, rate limiting, usage logs.

- **Prompt Marketplace** - Future idea: user-created prompts,
  with review.

- **Agent Marketplace** - Future idea (Phase 8): user-created
  business agents, with review and rev-share.

## Wallet and Ledger Status - Corrected

- **Wallet and Ledger foundations are implemented** in Phase 1 Part 3A
  (migration 003_payment_intents, wallet table with balance_credits
  check >=0, ledger_transactions append-only signed credit ledger
  with idempotency, atomic credit/debit with SELECT FOR UPDATE).

- **Real payment providers are not active.**
  - Only sandbox mock provider is active in Part 3A.
  - Real ZarinPal integration is Part 3B (future).
  - Real crypto verification (TRC20, TON) is Part 3C (future).
  - Exchange rate is static 190600 Toman per USD for MVP,
    later real-time rate from Bonbast or Arzbin.

- **Balance never negative** enforced at DB and code level.

## Problem Summary

- Persian users face language, payment, and access barriers
  to global AI tools.

- Existing tools are fragmented: chat here, image there,
  video elsewhere.

- No unified billing, no Role system tailored for Persian
  business context and personal preferences.

- No simple way for businesses to deploy Telegram agents
  or product studios.

- No professional studio workflows for creators.

## Solution Principles (Updated)

1. **Persian-first multimodal UX** but global-quality AI
   via provider abstraction.

2. **Credit-based billing** via wallet - simple, transparent,
   no shared accounts, atomic and idempotent,
   balance never negative.

3. **Extensible Role and Persona system** - ordinary Roles
   (conversation-only) and specialist Personas (versioned,
   evidence-aware, domain-specific, still conversation-only,
   may use approved knowledge retrieval).

4. **Professional Creative Studio as core revenue**
   - Not side feature.

5. **Accuracy and Creativity control** - User-friendly label
   "Accuracy and Creativity" Persian "دقت و خلاقیت" with modes
   strict_factual, balanced, creative.

6. **Telegram and Business Agents** - low-code agents that run
   in Telegram or business workflows, privacy-aware.

7. **Developer API Platform** - own APIs for chat, image, RAG
   with hashed keys, scopes, rate limiting.

8. **Agent Operating System** for building the product itself
   (external agents now L1 report/draft and L2 branch+PR,
   internal later L3/L4 with approval gates).

## What This Platform Is Not (De-scoped Legacies)

- Not a reseller of shared Netflix or GPT accounts
  - Deprecated model, archived.

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

## Default Mode

- **Default mode: Normal Assistant - Not psychologist - Not therapist**

- First-use onboarding should ask user what Role and communication
  style they prefer.

- User must be able to change these settings later.

Normal Assistant is default for all new users to avoid accidental
high-risk exposure.

## Immigration Persona vs Agent - Separation (Fixed Contradiction)

**Previously Product Vision listed Immigration Research Agent as
Specialist Persona, which mixes concepts.**

**Corrected:**

- **Immigration Information Persona:**
  - Conversation-only
  - Uses approved official-source Knowledge Base through Retrieval Service
  - Provides general information
  - Does not browse autonomously
  - Does not provide legal advice

- **Immigration Research Agent:**
  - Performs multi-step research
  - May browse approved current official government and embassy sources
  - Produces cited reports
  - Uses budgets, permissions, and audit metadata
  - Must not submit forms, spend money, contact authorities,
    or guarantee outcomes without separately approved future workflows

Do not describe an Immigration Research Agent as a Specialist Persona.

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

- Roadmap: [MASTER_ROADMAP](../roadmap/MASTER_ROADMAP.md)
- Agent OS: [AGENT_OPERATING_SYSTEM](../agents/AGENT_OPERATING_SYSTEM.md)
- Roles and Personas: [ROLE_AND_PERSONA_SYSTEM](../architecture/ROLE_AND_PERSONA_SYSTEM.md)
- Boundaries: [ROLE_PERSONA_AGENT_BOUNDARIES](../architecture/ROLE_PERSONA_AGENT_BOUNDARIES.md)
- Agent Execution: [AGENT_PLUGIN_AND_EXECUTION_SYSTEM](../architecture/AGENT_PLUGIN_AND_EXECUTION_SYSTEM.md)
- Accuracy and Creativity: [ACCURACY_CREATIVITY_CONTROL](../architecture/ACCURACY_CREATIVITY_CONTROL.md)
- Personas: [PERSONA_FRAMEWORK](../personas/PERSONA_FRAMEWORK.md)
- Safety: [TRUST_AND_SAFETY_FRAMEWORK](../safety/TRUST_AND_SAFETY_FRAMEWORK.md)
- Provider Abstraction: [PROVIDER_ABSTRACTION_STRATEGY](../architecture/PROVIDER_ABSTRACTION_STRATEGY.md)
- Human Approval Gates: [HUMAN_APPROVAL_GATES](../agents/HUMAN_APPROVAL_GATES.md)
