# PRICING PAGE REQUIREMENTS

**Date:** 2026-07-19

## Structure

- Hero: "قیمت ساده، شفاف، بر اساس اعتبار" (example)
- Credit Packs: 3 packs (Small 100 credits, Medium 500 + 10% bonus, Large 1000 + 20% bonus) - example numbers, not final
- Cost per Tool Table: Chat per 1k tokens, Image per generation, Product Photo per 5 images, Video per second future, Telegram per execution, API per 1k tokens
- FAQ: How credits work, expiration?, refund?, what if insufficient?
- Comparison: Us vs fragmented tools (evidence-based, no false claims)
- Final CTA: Buy credits (mock in Phase 1)

## Wallet Logic (Future, Not Built Now)

- Credit purchase → ledger entry → balance update atomic
- Spend: check balance → deduct with request ID idempotent → ledger → audit log
- Insufficient → 402 with message
- No auto price changes without approval (see HUMAN_APPROVAL_GATES)

## Approval Gates

- Changing prices, credit costs, wallet logic requires human approval
- Pricing page content change requires approval

## Safety

- No hidden fees, clear expiration policy
- Refund policy link
- No auto issuing credits above threshold without approval

## Metrics

- Pricing page → purchase intent click, FAQ expand
