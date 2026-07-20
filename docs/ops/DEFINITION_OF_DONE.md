# DEFINITION OF DONE

**Date:** 2026-07-19

## For Docs (Phase 0)

- Markdown file exists in correct path
- Has required sections from deliverables spec
- No secrets, no medical/legal authority claims, no unsafe autonomy recommendation
- Human approval gates mentioned where relevant
- Links to related docs are valid (no 404 within docs/)
- Spell-checked, coherent, Persian summary where required? Not required for Phase 0 docs but README has Persian summary

## For Code (Phase 1+ Future, Not Now)

- Feature branch from main
- Code in `backend/` or `frontend/` with tests
- Tests pass locally (pytest, npm build)
- No secrets, no P0 vulnerabilities
- PR template checklist filled
- PR description includes: what, why, tools, approval needed, risks, rollback
- If persona: QA and red teaming report attached
- If publishing/spending/pricing/config/API keys/persona high-risk: label `needs-human-approval` and founder comment Approved
- No direct main commit, no force-push
- Docker compose up works if relevant
- Docs updated if needed (README, relevant docs/roadmap phase doc exit criteria)

## For Issues

- Template used
- Title, purpose, owner agent type, dependencies, acceptance criteria, priority, phase label, risk level filled

## For Launch (See LAUNCH_PLAN)

- QA Security tests pass
- Persona QA/red team passed if personas
- Human approval gates checked
- Pricing correct, wallet tested
- Landing/blog approved and manually published
- Analytics events firing
- Rollback plan documented
- Founder approved
