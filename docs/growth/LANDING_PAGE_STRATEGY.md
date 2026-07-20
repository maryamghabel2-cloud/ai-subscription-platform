# LANDING PAGE STRATEGY

**Date:** 2026-07-19

## Types

- **Home:** General value prop, tools overview, CTA to register
- **Tool Landing:** /chat, /prompt-enhancer, /product-studio, /telegram-agents
- **Persona Landing:** /personas/{id} - explains persona, risk, disclaimer, CTA to try
- **Use-Case Landing:** /use-cases/{business} e.g., clothing store product photography
- **Comparison Landing (Future, Evidence-Based):** Persian AI vs global tools - must be evidence-based, no false claims
- **API Landing:** /api - developer focused, docs link, curl example

## Programmatic SEO Landing

- /product-studio/{category}: 50 categories, template + unique FAQ
- /personas/{id}: 14 personas eventual

## Structure (Each Landing)

- Hero: Headline Persian, sub-headline benefit, CTA
- Social proof (future): testimonials
- How it works: 3 steps
- Features: 3-6 bullets
- FAQ: Schema markup FAQPage
- Final CTA
- Footer: links, disclaimer if persona page

## SEO Requirements

- Meta title 50-60 chars Persian, includes primary keyword
- Meta description 150-160 chars
- H1 single, H2 sections
- Alt text for images
- Internal links to related landings
- Schema: Organization, Product, FAQPage, BreadcrumbList

## Approval Workflow

- Website Builder creates branch + landing file in `frontend/src/app/...` or markdown
- PR with SEO checklist: title, description, headings, alt, internal links, schema
- Growth Marketing + SEO Content review
- Human approval → merge → deploy

## Metrics

- Visit, bounce, time on page, CTA click, signup conversion per landing
- Rank for target keyword

## Safety

- No guarantee claims
- Persona landing includes disclaimer and risk level
- No medical/legal authority claims
