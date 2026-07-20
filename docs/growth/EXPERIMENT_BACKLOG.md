# EXPERIMENT BACKLOG

**Date:** 2026-07-19

## Template

```
Title: [Experiment - e.g., Product Studio CTA Copy Test]
Hypothesis: If we change CTA from "شروع کنید" to "عکس محصول بسازید رایگان", then signup conversion from product-studio landing will increase 20%
Owner Agent: Growth Marketing
Phase: Phase 3
Metric: Landing → signup conversion
Duration: 7 days
Traffic: 500 visits
Approval Required: Human approval to change landing copy + to launch experiment
Rollback: Revert landing file via git revert
Result: (to be filled)
Next: ...
```

## Backlog Ideas (Draft)

### EXP-001: Landing Hero Copy Test
- Hypothesis: Benefit-focused hero increases signup vs feature-focused
- Owner: Growth Marketing
- Phase: 1
- Metric: Visit → signup
- Priority: High

### EXP-002: Product Studio Before/After Slider
- Hypothesis: Showing before/after increases activation
- Owner: Website Builder + Growth
- Phase: 3
- Metric: Activation (upload → generate)
- Priority: High

### EXP-003: Persona Card Disclaimer Position
- Hypothesis: Disclaimer in card top vs bottom affects trust and activation
- Owner: Product Manager + Compliance
- Phase: 2
- Metric: Persona chat activation
- Priority: Medium

### EXP-004: Credit Pack Pricing Anchoring
- Hypothesis: Showing 3 packs with middle highlighted increases purchase
- Owner: Finance + Growth
- Phase: 1 (mock)
- Metric: Mock purchase click
- Priority: Medium

### EXP-005: Telegram Bot CTA
- Hypothesis: Adding Telegram bot demo video increases Telegram agent interest signup
- Owner: Growth Marketing
- Phase: 6
- Metric: Telegram page → waitlist
- Priority: Low (future)

## Rules
- No experiment that changes prices, config, production without approval
- No experiment that contacts customers without approval
- Each experiment needs approval issue

## Storage
- Future: `experiments/` folder or Growth tool
- Now: This doc + GitHub issues with label `growth-experiment`
