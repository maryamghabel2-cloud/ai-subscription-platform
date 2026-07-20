# GROWTH SYSTEM

**Date:** 2026-07-19

## Growth Loops (Phase 0 Planning)

### Loop 1: SEO → Landing → Signup → Activation → Referral
- **Trigger:** Programmatic SEO pages (see SEO_STRATEGY) rank for Persian AI queries
- **Landing:** Specific landing per use case (product photography, Telegram bot)
- **Signup:** Credit pack teaser, low friction
- **Activation:** First chat, first image, first persona chat
- **Referral:** After activation, prompt to share result (image) with watermark + referral link

### Loop 2: Content → SEO → Activation
- Blog content answers Persian AI questions, links to studio
- Content engine produces drafts, human approves, publishes

### Loop 3: Product-Led (Future)
- User shares generated image/video with branding → new user visits

## Metrics

- **Visits:** Unique visitors, source (organic, direct, referral)
- **Signup Conversion:** Visit → signup %
- **Activation:** Signup → first chat/image/persona within 24h %
- **Credit Purchase:** Activation → credit purchase %
- **Retention:** Weekly active, using 2+ tools
- **CAC:** Cost per acquired customer (content cost + ads future)
- **LTV:** Credit purchases over 90 days

## Rules Preventing Auto-Publishing Without Review

- All blog posts: draft → SEO Content Agent creates draft → Growth Marketing + founder review → human publishes
- All social posts: draft → Social Media Agent draft → founder approves → manual publish
- All landing page changes: Website Builder creates branch + PR → human approval → merge → deploy
- No bulk email/Telegram without approval (see HUMAN_APPROVAL_GATES)

## Experiment Framework

- See EXPERIMENT_BACKLOG.md
- Each experiment has hypothesis, metric, owner agent, approval needed, duration, rollback

## Wallet & Growth Link
- Credit purchase is activation milestone
- Referral gives credits (future idea, needs approval for credit issuance above threshold)

## Phase 0 Implementation
- Docs only, no code
- Future: Analytics events spec
