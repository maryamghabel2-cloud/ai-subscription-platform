# SEO TECHNICAL REQUIREMENTS

**Date:** 2026-07-19

## Sitemap

- /sitemap.xml dynamic: includes all public pages: home, tool landings, persona directory + detail, product-studio categories (if programmatic), blog posts, docs, use-cases, pricing
- Update on publish, submit to Google Search Console future

## Robots.txt

- /robots.txt: allow all public, disallow /dashboard, /api, /dashboard/*
- Sitemap reference

## Schema Markup

- Organization schema on home
- Product schema on tool landings if applicable
- FAQPage schema on pages with FAQ (home, pricing, tool landings, blog with FAQ)
- BreadcrumbList on hierarchical pages
- HowTo schema for studio how-to
- BlogPosting for blog

## Meta

- Title 50-60 chars Persian, primary keyword near start
- Description 150-160 chars Persian with CTA
- Open Graph, Twitter Card

## Performance

- Core Web Vitals: LCP <2.5s, CLS <0.1, INP <200ms
- Image optimization: next/image, WebP
- Lazy loading for below fold

## Security Headers (Future)

- CSP, X-Frame-Options, etc. (not Phase 0)

## Internal Linking

- Silos: Chat cluster links within, Product Studio cluster, etc.
- Breadcrumb navigation

## Tools

- Now: Manual checklist
- Future L3: SEO technical agent that crawls and reports draft issues, not auto-fix without approval
