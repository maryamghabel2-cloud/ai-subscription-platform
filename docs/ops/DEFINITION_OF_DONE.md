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

- Feature branch from main, no direct main commit, no force-push, no history rewrite
- Code in `backend/` or `frontend/` with tests
- Tests pass locally (pytest, npm build)
- No secrets, no P0 vulnerabilities, gitleaks check pass
- **Auth security:** No JWT in localStorage. Must use HttpOnly cookies with Secure flag in production, SameSite=Lax or Strict, short-lived access sessions (e.g., 30min), CSRF protection via SameSite + CSRF token where applicable. No token in URL, no token in JS. Passwords bcrypt, rate limiting login.
- **Persian-first MVP baseline:** RTL layout dir=rtl, Persian primary navigation, Persian forms and user-facing error messages, Persian-compatible typography, mobile-first layout tested 360/768/1024. Full polish may be deferred but baseline not out of scope.
- PR template checklist filled, PR description includes tools used, cost, approval needed, risks, rollback, tests
- If persona: QA and red teaming report attached with 10 functional +5 red team tests, evaluation metrics, evidence standard, source hierarchy, no authority claims, disclaimer, escalation behavior, human approval for high-risk prompt changes
- If publishing/spending/pricing/config/API keys/persona high-risk: label `needs-human-approval` and founder comment Approved
- Docker compose up works if relevant
- Docs updated if needed (README, relevant docs/roadmap phase doc exit criteria, no broken relative links)
- Absolutely forbidden actions never allowed: ToS bypass, geographic/sanctions/KYC bypass, fake identities, hiding prohibited locations, credential sharing/reselling unauthorized - no approval may authorize

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
