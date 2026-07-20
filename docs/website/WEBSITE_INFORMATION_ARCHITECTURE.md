# WEBSITE INFORMATION ARCHITECTURE

**Date:** 2026-07-19

## Planned Pages (All Not Built Yet in Phase 0 - Requirements Only)

- **Home** `/` - Hero, tools overview, social proof future, CTA, FAQ
- **Chat** `/chat` - General Persian chat, prompt enhancer inline
- **Specialist Personas** `/personas` - List of personas with cards, risk, disclaimer
- **Persona Detail** `/personas/{id}` - Persona explanation, evaluation, CTA to try
- **Product Studio** `/product-studio` - Upload product, generate, gallery
- **Product Studio Category** `/product-studio/{category}` - Programmatic SEO
- **Image Generation** `/image` - Simple prompt→image (Phase 3)
- **Video Generation** `/video` - Future Phase 5
- **Character Studio** `/character` - Future Phase 5
- **API Platform** `/api` - Developer landing, pricing, docs link
- **Telegram Agents** `/telegram-agents` - Connect bot, FAQ
- **Business Agents** `/business-agents` - FAQ, lead qualifier, content drafter
- **Research/RAG** `/research` - Upload docs, ask (Phase 7)
- **Pricing** `/pricing` - Credit packs, FAQ, comparison
- **Blog** `/blog` - List, categories
- **Blog Post** `/blog/{slug}` - Article with schema, internal links
- **Docs** `/docs` - Help docs, how to use
- **Use-Cases** `/use-cases/{business}` - e.g., clothing store
- **Contact** `/contact` - Form, not auto-contact without approval to email send? Form submit requires human approval to reply? Actually contact form sends to founder email - needs approval gate for bulk? No, single contact is allowed but must not auto-bulk.
- **Terms** `/terms` - Terms of service
- **Privacy** `/privacy` - Privacy policy
- **Refund Policy** `/refund` - Refund policy
- **Safety Policy** `/safety` - Safety, disclaimers, persona risk, escalation

## Navigation

- Header: Home, Chat, Personas, Product Studio, API, Pricing, Blog, Docs
- Footer: Product (Chat, Personas, Studio, API, Telegram, Business), Company (About, Contact, Blog), Legal (Terms, Privacy, Refund, Safety), Social (Telegram, Instagram)

## Sitemap Concept

```
/           Home
/chat       General chat
/personas   Directory
/personas/{id} Detail
/product-studio
/product-studio/{category}
/api        API Platform
/telegram-agents
/business-agents
/pricing
/blog
/blog/{slug}
/docs
/use-cases/{business}
/contact
/terms
/privacy
/refund
/safety
```

## Technical

- Next.js 14 App Router
- Tailwind
- SEO: sitemap.xml dynamic, robots.txt, schema markup
- i18n: Persian first, English maybe later - Phase 1 simple mix, Phase 2 Persian UI (scope limit says no Persian full translation in Phase 1? Actually Phase 0 says no Persian UI translation Phase 2 - means keep simple for Phase 1)

## Safety

- Persona pages include risk level and disclaimer
- Safety page explains evidence-based assistants, not professional authority
- No medical/legal advice without disclaimer
