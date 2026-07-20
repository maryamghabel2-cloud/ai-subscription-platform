# RELEASE STRATEGY

**Date:** 2026-07-19

## For Phase 0

- No release, docs only, PR not merged until founder review

## For Phase 1 Core MVP (Future)

- **Local:** docker compose up --build
- **Staging (Future):** Not in Phase 0, but plan: staging env with same compose, env from secure vault (not repo)
- **Production (Future):** Not now, no deploy in Phase 0 docs branch

## Release Types

- **Patch:** Bug fix, no feature
- **Minor:** New feature (e.g., new persona, new tool)
- **Major:** Phase launch (e.g., Phase 1 MVP, Phase 2 Personas)

## Steps for Future Release (Not Now)

1. All issues in milestone closed and meet DoD
2. QA Security report pass
3. HUMAN_APPROVAL_GATES checked (spending, publishing, pricing, config, persona)
4. Founder approves release via issue comment
5. Tag release `v1.0.0` from main
6. Deploy manually (no auto-deploy in Phase 0-2)
7. Post-release: monitor, experiment backlog, reporting cadence

## Rollback

- For code: git revert tag or revert PR
- For content: unpublish or revert landing file
- For pricing/wallet: revert config + ledger correction with approval

## No Auto-Deploy in Phase 0-2

- Human must deploy manually after approval
