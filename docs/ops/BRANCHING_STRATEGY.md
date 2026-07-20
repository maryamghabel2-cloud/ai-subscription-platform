# BRANCHING STRATEGY

**Date:** 2026-07-19

## Main Branch

- `main` - protected, always deployable (future)
- No direct commits
- PRs only
- History never rewritten, no force-push

## Feature Branches

- Format: `type/short-description`
  - `feat/auth` - feature (example, not necessarily present)
  - `fix/login-bug` - fix (example)
  - `docs/phase-0-agent-operating-system` - docs (current, exists remotely)
  - `chore/archive-legacy` - chore (example)
  - `archive/legacy-code-2026-07-19` - archive (exists remotely, legacy code preservation)
  - For MVP, a future branch like `mvp/v1-core-foundation` could be created later - verify existence with `git ls-remote --heads origin` before claiming it exists
- From main, short-lived
- Delete after merge (optional)

## Release Branches (Future)

- Not needed Phase 0-1
- Future: `release/v1.0` if needed

## Hotfix (Future)

- `hotfix/critical-bug` from main

## Rules

- Never merge without human approval
- Never force-push
- Never delete history
- Only docs branches may be merged without code review? No, still need checklist
- Archive branches never merged to main (except docs archival already done via PR #1 which was docs only)

## Solo Founder Adjustment

- Founder is both author and reviewer, but must still follow checklist in PR template to avoid ADHD scope creep
- Use PR description as self-review
