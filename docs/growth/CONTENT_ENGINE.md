# CONTENT ENGINE

**Date:** 2026-07-19

## Purpose
System to produce SEO and educational content consistently, with human approval.

## Stages

1. **Topic Ideation:** Growth Marketing + SEO Content agents propose topics from SEO topic clusters, user questions, experiment backlog
2. **Brief:** Keyword, search intent, outline, internal links, CTA to product (landing, studio)
3. **Draft:** SEO Content Agent drafts blog post (L2 external, draft-only)
4. **Review:** Prompt Engineer checks prompt accuracy, Research checks sources, Compliance checks risky claims, QA checks grammar
5. **SEO Technical Check:** Meta title (50-60 chars Persian), meta description (150-160), headings, alt text, internal links, schema markup (FAQ, HowTo)
6. **Human Approval:** Founder approves via GitHub issue comment
7. **Publish:** Human publishes manually (no auto-publish)

## Content Types

- Blog: How-to, guide, listicle, case study (future)
- Landing copy: Use-case pages
- Persona docs: Persona explanation pages
- Help docs: How to use studio, API

## Tools Now (L1/L2)
- External LLM for draft
- Google Docs / markdown in repo `content/` (future)

## Tools Later (L3)
- Draft CMS that creates draft post in draft state, not live
- Human publishes via CMS UI

## Approval Required
- Publishing any blog, landing, docs public page → human approval

## Metrics
- Content → visit, visit → signup, activation

## Templates
- Content brief template in growth docs
- Blog post template with disclaimer section for persona pages

## Safety
- No medical/legal/psych advice without disclaimer and compliance review
- No guarantee claims (e.g., #1 ranking, guaranteed job)
- All drafts have footer: "Draft by SEO Content Agent, needs human approval"
