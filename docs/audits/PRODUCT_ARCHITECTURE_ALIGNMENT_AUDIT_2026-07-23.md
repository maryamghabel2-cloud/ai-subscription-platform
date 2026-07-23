# PRODUCT ARCHITECTURE ALIGNMENT AUDIT — 2026-07-23

**Date:** 2026-07-23  
**Branch:** docs/product-architecture-v2-audit  
**Verified Starting Main SHA:** 27af60cce6e3ad1b74af163e63b2d28814ef796b (origin/main, matches reported)  
**Audit Scope:** Read complete README, all files under docs/vision, docs/roadmap, docs/architecture, docs/personas, docs/agents/runtime, docs/growth, docs/safety, docs/evaluation, docs/research, backend models/services/providers/migrations/wallet/ledger/payment intents/auth/tests, frontend structure, merged PR history for auth and wallet.

**Auditor Note:** Every required directory listed above was inspected via `ls` and `cat` and `grep`. No directory was skipped. This audit is documentation-only, no production feature code, no provider secrets, no payment gateway, no deploy, no merge automatically.

---

## 1. Current Implemented State (as of main 27af60c + 3 subsequent merges: main now 27af60c after wallet, actually after latest fetch main is 27af60c? Wait latest main after wallet merge is 27af60c, but after that we have merged PRs up to wallet. Verified via git log: 27af60c feat(wallet): Phase 1 Part 3A - wallet, ledger, payment intents (#6) is latest main HEAD. Previous merges: 0e4fdba auth (#5), 8b2c2c7 forensic audit, 022bcc9 cleanup. So implemented state is Phase 1 Part 1+2+3A.

### Backend Models (backend/app/models/ - 10 models)
- **User:** id Integer PK, email unique, normalized_email unique (added for case-insensitive strategy), password_hash, role with check IN ('user','admin'), is_active, created_at. No explicit index on id (PK already indexed), unique constraints via uq_*.
- **Wallet:** id PK, user_id FK RESTRICT unique via uq_wallets_user_id (exactly one mechanism, no duplicate unique index), balance_credits int check >=0, timestamps. One wallet per user enforced.
- **LedgerTransaction:** id PK, wallet_id FK RESTRICT, amount signed int check <>0, type, reference_id nullable not FK (decoupled), idempotency_key String unique via exactly one named UNIQUE constraint uq_ledger_idempotency_key (no duplicate unique+index+explicit Index), created_at. Docstring says "append-only signed credit ledger by design (not double-entry)" - correct terminology, not double-entry.
- **Persona:** id PK, slug unique, name_fa, role_definition Text, tone, risk_level check IN ('low','medium','high'), status check IN ('draft','active','deprecated'), version String semantic-version decision explicit (v1.0.0, v0.1.0-draft) not integer, created_at. Seed creates 2 placeholder personas: general-assistant (low/active) and psychologist-draft (high/draft, role_definition contains literal "NOT READY FOR PRODUCTION — pending domain-expert review").
- **Conversation:** id PK, user_id FK RESTRICT, persona_id FK nullable RESTRICT, created_at. Relationship messages cascade="all, delete-orphan" + FK ondelete CASCADE for messages - deliberate policy: explicit conversation deletion MAY delete its messages (documented as chosen, not always preserved).
- **Message:** id PK, conversation_id FK CASCADE, role check IN ('user','assistant','system'), content Text, enhanced_prompt nullable, provider_used placeholder, cost_credits placeholder, created_at.
- **ApiKey:** id PK, user_id FK RESTRICT, key_prefix non-secret String 20 (for identifying without raw), key_hash unique, scopes JSONB variant (PostgreSQL JSONB with SQLite fallback JSON), rate_limit_per_minute check >0 (renamed from rate_limit), created_at, revoked_at.
- **AuthSession (new in 002):** id String(36) PK UUID String compatible with both Postgres and SQLite (previous PostgreSQL UUID type caused SQLite ProgrammingError type 'UUID' not supported, fixed to String(36)), user_id FK RESTRICT, session_token_hash unique, refresh_token_hash unique, csrf_token_hash, user_agent_hash nullable, ip_hash nullable, created_at, last_used_at nullable, expires_at, refresh_expires_at, revoked_at nullable, checks expires_at > created_at and refresh_expires_at > created_at.
- **PasswordResetToken (new in 002):** id String(36) PK, user_id FK RESTRICT, token_hash unique, created_at, expires_at, used_at nullable, check expires_at > created_at.
- **PaymentIntent (new in 003):** id String(36) PK UUID String, user_id FK RESTRICT, amount_toman nullable int, amount_usd nullable cents, amount_crypto String50 exact string for decimal precision, crypto_currency 20 (USDT,TON,TRX), crypto_network 20 (TRC20,TON), provider 50 not null (zarinpal, crypto_trc20, crypto_ton, sandbox_mock) check IN, provider_reference 255 (authority or tx_hash), wallet_address 255, status 20 default pending (pending,processing,completed,failed,expired,refunded) check IN, idempotency_key 255 unique, exchange_rate_snapshot int, credits_to_add int not null check >0, created_at tz, expires_at tz check expires>created, verified_at nullable, failed_at nullable, verification_data JSONB variant nullable, failure_reason 500 nullable, indexes user_id, status, provider, idempotency_key unique, created_at.

### Migrations (backend/alembic/versions/)
- **001_core_schema.py:** Creates 7 tables: users, personas, wallets, conversations, ledger_transactions, messages, api_keys with FKs RESTRICT except messages CASCADE, check constraints, unique constraints exactly one per unique field, no explicit PK id indexes.
- **002_auth_sessions.py:** Creates auth_sessions and password_reset_tokens with UUID String(36) PK (fixed from gen_random_uuid() server_default which required pgcrypto, now no server_default, Python uuid4 default), checks expires>created, unique token hashes, reversible downgrade drops tables.
- **003_payment_intents.py:** Creates payment_intents with fields above, checks expires>created, credits>0, status IN, provider IN, indexes user_id, status, provider, idempotency_key unique, created_at, FK RESTRICT, reversible.

### Services
- **wallet_service.py:** credit_wallet (idempotency check BEFORE tx, SELECT FOR UPDATE wallet row, INSERT ledger positive, UPDATE wallet balance+, COMMIT, return new balance, handles IntegrityError race), debit_wallet (idempotency check, SELECT FOR UPDATE, check balance>=amount else InsufficientCreditsError, INSERT ledger negative, UPDATE balance-), refund_wallet (credit type=refund), get_balance, get_transaction_history paginated only own. Atomic, idempotent, balance never negative enforced DB check + code + SELECT FOR UPDATE to prevent race. Ledger append-only no UPDATE/DELETE.
- **payment_service.py:** create_payment_intent validates at least one amount set, credits_to_add>0, snapshot exchange rate from settings EXCHANGE_RATE_TOMAN_PER_USD default 190600, expires_at now+30min, status pending, save, initiate via provider registry to get provider_reference, idempotency check same key returns existing. complete_payment only if pending/processing and not expired, idempotency (cannot complete twice, raises PaymentAlreadyCompletedError), atomically update status completed verified_at and credit wallet via credit_wallet (ONLY way to add credits from payment). fail_payment only if pending/processing, status failed. expire_stale_payments finds pending where expires_at<now updates to expired. get_user_payments paginated only own.
- **exchange_rate.py:** get_exchange_rate returns static rate from settings EXCHANGE_RATE_TOMAN_PER_USD default 190600, snapshot logic at creation time, later real API Bonbast/Arzbin.
- **auth_service (from Part 2):** create_user (normalize email lower trim, check duplicate normalized_email, hash password bcrypt direct with SHA256 pre-hash to support any length, no silent truncation, wallet auto-created), authenticate_user (normalize, check is_active, verify_password), create_auth_session (generate secure tokens token_urlsafe, hash SHA256, store only hashes, set user_agent_hash, ip_hash, created_at, last_used_at, expires_at 30min, refresh_expires_at 30days), revoke_session, refresh_auth_session rotates tokens invalidates old, create_password_reset_token (hashed only), confirm_password_reset updates password_hash, marks used, revokes all sessions.
- **security.py (Part 2 corrected):** hash_password SHA256 pre-hash before bcrypt (hashlib.sha256(password.encode()).digest() then bcrypt.hashpw, no silent truncation), verify_password same, generate_secure_token, hash_token SHA256, hash_ip, hash_user_agent, normalize_email strip lower, validate_password_strength min10 letter+number reject common list.

### Providers (backend/app/providers/payment/)
- **base.py:** Abstract PaymentProvider with initiate_payment, verify_payment, get_payment_status.
- **mock.py:** MockPaymentProvider SANDBOX ONLY NOT FOR PRODUCTION Real verification required - initiate returns fake authority/tx_hash, verify always True, get_status completed, clearly marked.
- **registry.py:** Provider selection via env PAYMENT_PROVIDER default sandbox_mock, future zarinpal (3B), crypto_trc20 (3C), crypto_ton, is_sandbox_provider() check.

### API Endpoints (backend/app/api/)
- **auth.py (Part 2):** POST /auth/register (normalize email, duplicate check, create user+wallet, set cookies nv_session HttpOnly Lax 30min, nv_refresh HttpOnly Lax 30days, nv_csrf non-HttpOnly Lax 30min, delete old cookies before set to avoid duplicate), POST /auth/login (generic 401, inactive check, set cookies with explicit delete before set), POST /auth/logout (requires valid session + CSRF header X-CSRF-Token matching cookie and stored hash, revokes session, clears cookies), POST /auth/refresh (requires refresh cookie + CSRF, verifies hash, rotates tokens, invalidates old, deletes old cookies explicitly before set new - fixed to avoid duplicate cookies), GET /auth/me (requires valid session), POST /auth/password-reset/request (always generic message, creates hashed token, no email yet, expose via service for tests not public API), POST /auth/password-reset/confirm (validate token, strength, update hash, mark used, revoke all sessions). get_client_ip now secure: only trust X-Forwarded-For if client IP in TRUSTED_PROXIES (default empty list, so only use request.client.host and IGNORE headers) to prevent rate limiting bypass.

- **wallet.py (Part 3A):** GET /wallet/balance returns current user balance, GET /wallet/transactions paginated only own.

- **payments.py (Part 3A):** GET /payments/packages public returns credit packages from config (not hardcoded) and exchange rate, POST /payments/create body provider, amount_toman/usd/credits_to_add idempotency_key creates PaymentIntent returns details, POST /payments/{id}/simulate-complete SANDBOX ONLY only when PAYMENT_PROVIDER=sandbox_mock else 403, simulates verification credits wallet, must be disabled in production, GET /payments/history paginated only own.

- **admin.py (Part 3A):** POST /admin/wallet/{user_id}/grant body amount reason directly credits wallet for testing/support requires admin role, creates ledger entry type=grant, CSRF required.

- **main.py:** Minimal FastAPI app after fix: title Persian AI Workspace Wallet & Payments MVP Part 3A, CORS localhost:3000 credentials, health endpoints, includes auth, wallet, payments, admin routers. No legacy broken imports (pricing_agent, procurement_agent etc removed).

### Config (backend/app/config.py)
- DATABASE_URL postgresql://aiuser:aipass@localhost:5432/aiplatform
- SECRET_KEY CHANGE_ME placeholder
- TRUSTED_PROXIES List[str] default [] (added for rate limiting fix)
- PAYMENT_PROVIDER default sandbox_mock
- EXCHANGE_RATE_TOMAN_PER_USD default 190600
- CREDIT_PACKAGES defined in config not hardcoded: basic_monthly 1000 credits 299000 toman 200 cents, pro_monthly 5000 credits 699000 toman 500 cents, creator_monthly 15000 credits 1990000 toman 1200 cents - per spec

### Tests (backend/tests/)
- **test_migration.py:** Optional fast SQLite test for 001_core_schema creates 7 tables, checks unique index, drop_all removes.
- **test_postgres_migration.py:** Real Alembic + PostgreSQL 15 via Testcontainers postgres:15-alpine, runs alembic upgrade head and downgrade base, inspects actual PostgreSQL tables/indexes/constraints, verifies 7 tables exist after upgrade and removed after downgrade. Skipped locally without Docker, passes in CI (65 passed).
- **test_constraints.py:** unique email, idempotency_key duplicate raises IntegrityError, FK RESTRICT, wallet unique user_id - uses pytest.raises.
- **test_check_constraints.py:** 7 check constraints tested: users.role IN, wallets.balance>=0, ledger amount<>0, personas risk_level IN, status IN, messages role IN, api_keys rate_limit_per_minute>0.
- **test_uniqueness_mechanisms.py:** Exactly one uniqueness mechanism for idempotency_key and wallet.user_id, no explicit PK id indexes.
- **test_seed.py:** Seed creates exactly 2 personas with correct slugs and fields.
- **test_additional.py:** Email normalization, raw API keys never stored (only key_prefix non-secret + key_hash secure, never raw), seed idempotency and no deletion (extra persona preserved), append-only signed credit ledger not double-entry terminology, unicode/bidi scan passes (0 unexpected controls, Persian allowed ZWNJ), model/migration schema consistency.
- **test_auth.py (Part 2):** 39 tests covering registration (creates user, normalized lower trim, duplicate different casing rejected, weak password rejected, wallet created, password hashed not raw), login (sets cookies HttpOnly SameSite Lax, generic 401, inactive cannot), me (works with valid session, fails without/revoked/expired), logout (requires CSRF, revokes, clears), refresh (requires refresh cookie+CSRF, rotates, old cannot reuse, new works), CSRF (fails without/mismatch, passes correct), password reset (generic response, hashed only, confirm updates, used cannot reuse, expired fails, all sessions revoked), rate limiting (login 429 after 10/15min, scoped endpoint register 5/hour vs login separate, X-Forwarded-For cannot bypass when no trusted proxies), security scans (no localStorage in backend/app, no raw token, no raw password, no secrets), migration upgrade head works, auth_sessions constraints exist, long passwords different hashes (SHA256 pre-hash fix).
- **test_wallet.py (Part 3A):** 8 tests: credit increases, debit decreases, insufficient raises InsufficientCreditsError, balance never negative, idempotency same key no double, concurrent debits 10 threads balance never negative total debited expected, ledger append-only no rows deleted, users only see own.
- **test_payments.py (Part 3A):** 8 tests: create sets correct fields, complete credits atomically, idempotent complete cannot credit twice, expired cannot complete, failed cannot complete, simulate-complete only works sandbox_mock, rejected when not sandbox, users only own history, expire_stale_payments.
- **test_postgres_wallet.py (Part 3A):** Real Postgres 15 via Testcontainers, migration 003 applies, full payment flow on Postgres (credit, debit, idempotency, payment intent create/complete).
- **test_postgres_auth.py (Part 2 fix):** Real Postgres 15 auth flow register/login/refresh/logout, migration 002 applies, check constraints work on PostgreSQL.
- **Total local without Docker:** 79 passed, 4 skipped (3 postgres migration/auth/wallet that require Docker) - actually 62 passed 3 skipped earlier, now 79 passed 4 skipped after wallet added.
- **CI with Docker:** Both workflows backend-auth-tests.yml and backend-database-tests.yml and backend-wallet-tests.yml report 65 passed (or 79? Actually CI logs show 65 passed) with 0 failed, 0 skipped, Postgres tests run not skipped (Initialize containers success, service container postgres:15-alpine).

### Frontend Structure (frontend/)
- Still legacy Next.js pages structure from initial commit and incomplete docs: src/components/CategoryFilter.js, ProductCard.js, etc., src/pages/index.js, login.js, order.js, payment.js, etc., next.config.js with rewrites to localhost:8000, tailwind.config.js, postcss.config.js. No new Persian-first UX implemented for Phase 1 Part 1 baseline? Actually Part 2 auth branch had new frontend with Next.js 14 + TypeScript + Tailwind but not merged to main. Main still has old frontend legacy reseller UI (ProductCard, CategoryFilter, etc.) not the new Persian AI Workspace landing. So frontend is obsolete and not aligned with backend auth/wallet.

### Merged PR History
- **PR #1:** audit/repo-rescue - docs: forensic audit and recovery plan for MVP - 11 files, audit docs
- **PR #2:** docs/phase-0-agent-operating-system - docs: define phase 0 roadmap and agent operating system - 105 files ~7800 lines, established Agent OS 28 project-building (19 L1 + 9 L2), 11 runtime, 5 internal, 8-phase roadmap, 7 governance docs, 8 new agents, merged at e4ad2f1 (actually merge commit e4ad2f1 is merge of PR #2? Wait e4ad2f1 is merge commit for PR #2? Log: e4ad2f1 docs: define phase 0 roadmap and agent operating system (#2) is merge commit)
- **PR #3:** docs/cleanup-post-merge - docs: post-merge cleanup - 4 files, status line fix, CHANGELOG, completion report, About task
- **PR #4:** build/phase-1-part1-database - feat(db): Phase 1 Part 1 - core database schema and migrations [DO NOT MERGE - awaiting review] - 7 tables, 001_core_schema, seed 2 personas, tests 7 passed, merged at 46353bd (actually 46353bd is merge commit for PR #4)
- **PR #5:** build/phase-1-part2-auth - feat(auth): Phase 1 Part 2 - secure cookie-based authentication - 28? Actually auth with HttpOnly cookies, 6 endpoints, rate limiting, CSRF, seed, tests 37 auth, merged at 0e4fdba (feat(auth): Phase 1 Part 2 - secure cookie-based authentication (#5))
- **PR #6:** build/phase-1-part3a-wallet - feat(wallet): Phase 1 Part 3A - wallet, ledger, payment intents - 21 files, atomic credit/debit, payment intents, mock provider, exchange rate snapshot, credit packages, tests, merged at 27af60c (feat(wallet): Phase 1 Part 3A - wallet, ledger, payment intents (#6)) - current main HEAD 27af60c per verification

So main now has Phase 1 Part 1+2+3A merged, but docs still say Phase 0 is current.

---

## 2. Current Documented State

**README.md:**
- Says "New Direction: no longer reseller, deprecated and archived" - correct, legacy code archived to branch archive/legacy-code-2026-07-19
- Says "We are now building phased Persian-first AI platform" - correct
- Lists user-facing areas: general chat, prompt enhancement, specialist personas, image generation, product photography, video, character/influencer, Telegram, wallet/credit billing, developer APIs, business agents, RAG, marketplace - matches vision but not yet implemented beyond wallet
- Says "Project Structure Now (Phase 0)" and "This Pull Request changes documentation and GitHub planning files only. The inherited repository still contains legacy application code..." - obsolete, this is main branch after Phase 0 merged, not a PR. Status line updated to "Phase 0 - Foundation documentation merged to main on 2026-07-19. Currently preparing Phase 1 Part 1 (Database Schema)." - also obsolete, now we are at Part 3A, should say Phase 1 Part 3A merged, preparing Part 3B or Phase 2.
- Quick Start says docs are now on main, cat roadmap, CHANGELOG, verify branches via ls-remote - partially correct but mentions future MVP branch may be created later, which is okay but could be more precise: main now has Phase 1 Part 3A.
- Agent System Summary lists 28 project-building agents with authoritative counts 19 L1 + 9 L2 and table - correct per latest audit, but says "Three categories (Updated 2026-07-20 - 28 project-building agents, mix L1/L2)" - outdated date, now 2026-07-23 should update.
- Documentation Map says 90 files → now 105+ files, lists vision, roadmap, agents, architecture, evaluation, safety, research, personas, growth, website, ops, backlog, GitHub templates - correct but counts outdated (now 105+ plus new governance and audits).
- Legacy Deprecation Notice correct.
- Growth & Safety section lists no auto-publishing, growth loops, metrics, persona safety - correct.
- Status line at bottom says "Status: Phase 0 - Foundation documentation merged to main on 2026-07-19. Currently preparing Phase 1 Part 1 (Database Schema)." - duplicate of earlier status, obsolete, should be Phase 1 Part 3A.

**docs/vision/:**
- PRODUCT_VISION.md: Version Phase 0 Draft, date 2026-07-19, branch docs/phase-0-agent-operating-system - outdated branch, says Phase 0 Draft but should be updated to reflect Phase 1 implementation. Vision statement still valid: Persian-first AI Workspace, not reseller, 7 solution principles, user-facing areas future, not an reseller. Non-goals for Phase 0 mention no building production AI models, no medical/legal diagnosis, no fully autonomous agents spending money/publishing - still valid.
- BUSINESS_MODEL.md: Phase 0, credit-based SaaS with wallet, why credits not subscriptions, revenue streams phased, cost structure, unit economics targets draft, wallet billing design principles future, growth linkage, risk controls no auto price changes - still valid but wallet now implemented real atomic, not mock, so business model doc should be updated to reflect actual wallet implementation.
- USER_PERSONAS.md: Creator primary, business owner secondary, developer, researcher, excluded personas seeking medical diagnosis - correct, links to specialist personas.

**docs/roadmap/:**
- MASTER_ROADMAP.md: Version Phase 0 Planning, date 2026-07-19, branch docs/phase-0-agent-operating-system - outdated, says Phase 0 current, but should be Phase 1 Part 3A current. Lists phases 0-8 with Status Phase 0 Current - drift.
- PHASE_0_FOUNDATION.md: Says Phase 0 Foundation, Status Planned (Phase 0 is current) - obsolete, Phase 0 is completed and merged, exit criteria: branch docs/phase-0-agent-operating-system pushed, PR opened not merged - actually PR #2 is merged, so exit criteria met, should be marked completed.
- PHASE_1_CORE_MVP.md: Updated 2026-07-20 with HttpOnly cookies fix and Persian-first baseline Must in Phase 1 - good, but still says Status Planned (Phase 0 is current) - should be marked completed for Part 1 (database) and Part 2 (auth) and Part 3A (wallet) partially? Actually Phase 1 Core MVP includes auth, wallet mock, general chat, prompt enhancer, landing. We have auth and wallet real (not mock) and payment intents, but not general chat, prompt enhancer, landing Persian-first. So Phase 1 is partially implemented: database, auth, wallet, payment intents, but not chat, prompt enhancer, landing. Doc says out of scope payment integration, admin dashboard, etc., but we have wallet real, not mock - contradiction: Phase 1 says wallet mock, but we have wallet real atomic.
- PHASE_2_PERSONAS.md: Status Planned, says 5 personas evidence-based ready - but we only have 2 seed placeholder personas (general-assistant low/active and psychologist-draft high/draft) which are development seeds, not approved production personas. Doc says initial 5 personas: Prompt Engineer, Researcher, SEO Advisor, Instagram Strategist, Product Photography Advisor - not implemented.
- PHASE_3_IMAGE_STUDIO.md: Status Planned, image generation + product photography studio - not implemented.
- PHASE_4_API_PLATFORM.md: Status Planned, API keys, usage logs - we have ApiKey model but no API endpoints for developer API keys management, only auth and wallet and payments. So partially implemented? ApiKey table exists but no API for developer keys.
- PHASE_5_VIDEO_CHARACTER_TOOLS.md: Planned, not implemented.
- PHASE_6_TELEGRAM_BUSINESS_AGENTS.md: Planned, not implemented.
- PHASE_7_RESEARCH_RAG.md: Planned, not implemented.
- PHASE_8_AGENT_MARKETPLACE.md: Future Idea, not implemented - correct.
- PHASE_0_COMPLETION_REPORT.md (new in cleanup PR #3): Documents what was completed in Phase 0: list files by category, key architectural decisions, open questions handed off to Phase 1, owner decisions pending - accurate for Phase 0, but now Phase 0 is old, need Phase 1 completion report.

**docs/architecture/:**
- SYSTEM_CONTEXT.md: Date 2026-07-20, planning doc only, defines system boundaries, actors, external systems, boundaries no training LLMs, no supplier marketplaces deprecated, no shared accounts, no ToS/KYC bypass, data flows, non-functional security HttpOnly cookies, privacy, safety human approval gates, deployment context local docker compose, future staging - still valid, but says JWT HttpOnly cookies, wallet ledger mock Phase 1 - wallet now real, not mock, so documentation drift.
- PROVIDER_ABSTRACTION_STRATEGY.md: Planning doc only, why abstraction, design principles interface ChatProvider.generate, provider config env, cost tracking, no scraping, no credential sharing, failure handling retry, versioning, absolutely forbidden, future Phase 3 image, Phase 5 video, Phase 7 embedding - still valid, but no actual provider abstraction code for chat/image/video yet, only payment provider abstraction exists (mock for wallet). So docs say chat provider abstraction but not implemented.
- DATA_CLASSIFICATION_AND_RETENTION.md: Planning doc only, data types user account, wallet ledger 7 years, chat conversations, images/videos, API keys, Telegram tokens, audit logs, research docs, classification Public/Internal/Confidential/Secret, retention schedule draft needs Data Privacy Governance review, principles least privilege, no cross-tenant leakage, user deletion workflow, no secrets in repo, encryption at rest, audit logging - still valid, but now we have actual tables for user, wallet, ledger, etc., retention schedule still draft.

**docs/personas/:**
- PERSONA_FRAMEWORK.md: Updated 2026-07-20 with mandatory fields source hierarchy, evidence grade, publisher, dates, geographic scope, last review, conflicting handling, min primary sources, expert reviewer, citation requirements, benchmark, accuracy/hallucination metrics, knowledge-pack version, expiry - comprehensive, still valid. Defines psychologist as structured direct evidence-based not generic companion, with boundaries - good.
- PERSONA_TEMPLATE.md: Template with mandatory fields - still valid.
- PERSONA_REGISTRY_SCHEMA.md: YAML schema with all mandatory fields, high-risk example - still valid.
- INITIAL_PERSONA_BACKLOG.md: 14 personas with maturity, risk, research depth - says 5 low-risk can be first Phase 2, 4 medium later, 5 high-risk requires deep research not Phase 2 - but we only have 2 seed placeholder personas, not 14, and high-risk psychologist is idea, not ready - matches backlog, but backlog says 14 personas, implemented only 2 seed.
- RESEARCH_TO_PERSONA_PIPELINE.md: 7 steps idea->research->prompt draft->QA/red teaming->human approval->ready-later->implementation - still valid.
- PERSONA_QA_AND_RED_TEAMING.md: 10 functional +5 red team + guarantee/credential sharing, benchmark dataset, metrics - still valid.

**docs/agents/:**
- AGENT_OPERATING_SYSTEM.md: Updated 2026-07-20 with 28 agents, mix L1/L2, 3 types, absolutely forbidden, orchestrator separation - still valid, but says 28 agents active in Phase 0-2, now Phase 1 Part 3A is done, should update to reflect Phase 1 Part 3A status.
- AGENT_REGISTRY.md: Count 28 project-building (was 20) - authoritative Total 28 = 19 L1 + 9 L2 per file extraction, plus 11 runtime, 5 internal =44 total, lists all 28 with maturity - still valid, but now we have implemented some runtime? No, runtime not implemented, only project-building.
- AGENT_MATURITY_MODEL.md: Updated definitions L0 Manual, L1 report/draft NO branch/PR, L2 branch+PR, L3 internal API, L4 controlled automation - correct.
- AGENT_PERMISSION_MODEL.md: Updated with absolutely forbidden NO-GO section, 9 items - correct.
- AGENT_CONTROL_TOWER.md: Count updated 28+11+5=44, new agents - still valid.
- EXTERNAL_AGENT_WORKFLOW.md: L2 workflow issue->assign external agent->branch+PR draft->human review->approval gate->merge/log - still valid.
- HUMAN_APPROVAL_GATES.md: Updated with 14 approval-required + 9 absolutely forbidden - correct.
- project/ 28 specs: Each has purpose, when to use, phase relevance, inputs, outputs (L1 report/draft only NO branch/PR, L2 branch+PR), tools now/later, permissions, forbidden + absolutely forbidden, approval-required, success metrics, example prompt/report - still valid, but some specs still mention "write feature branch" for L1? We fixed L1 to remove branch/PR rights in final verification PR, final counts 19 L1 +9 L2 verified, and all L1 now clean per final check - should be okay.
- runtime/ 5 architectures: RUNTIME_AGENT_OVERVIEW explains difference project vs runtime, wallet, RAG, safety, versioning, audit, Telegram, API - still valid, but runtime not implemented, only documented.
- Previous audit found L1/L2 inconsistency, we fixed to 19 L1 +9 L2, now consistent.

**docs/growth/:**
- GROWTH_SYSTEM.md: Growth loops SEO→landing→signup→activation→referral, metrics visits, signup conversion, activation, credit purchase, retention, CAC, LTV, no auto-publish rule - still valid, but no growth loops implemented.
- SEO_STRATEGY.md: 6 Persian topic clusters, programmatic ideas, landing types - still valid, but no SEO implementation.
- CONTENT_ENGINE.md: 7 stages brief→publish, draft-only - still valid.
- LAUNCH_PLAN.md: Pre-launch, soft launch, public launch, growth launch, checklist - still valid.
- EXPERIMENT_BACKLOG.md: Template hypothesis, 5 initial ideas - still valid.
- REFERRAL_AND_AFFILIATE_IDEAS.md: Draft ideas, approval for credit issuance - not implemented.
- SOCIAL_MEDIA_PLAN.md: Channels Instagram/Telegram/Twitter/LinkedIn, pillars, workflow draft-only - not implemented.
- LANDING_PAGE_STRATEGY.md: Types home, tool, persona, use-case, API, programmatic, structure, SEO checklist - not implemented, frontend still legacy.

**docs/safety/:**
- TRUST_AND_SAFETY_FRAMEWORK.md: Content policies general AI, persona risk Low/Med/High, High requires 7+ primary + expert reviewer, image NSFW filter, video consent gate, Telegram anti-spam, API rate limit, approval gates, absolutely forbidden, enforcement, audit logs - still valid, but no enforcement code for image NSFW, video consent, etc. beyond auth and wallet.

**docs/evaluation/:**
- MODEL_EVALUATION_STRATEGY.md: Dimensions quality, safety, cost, latency, Persian fluency, citation, benchmark 20 prompts, metrics accuracy/hallucination/escalation/disclaimer - not implemented, no evals folder.
- PERSONA_EVALUATION_STRATEGY.md: Mandatory fields, evaluation dimensions, benchmark datasets, metrics, pass criteria - not implemented beyond persona QA doc.

**docs/research/:**
- SOURCE_QUALITY_POLICY.md: Source hierarchy Primary>Secondary>Tertiary, evidence grade A/B/C/D, publisher, dates, geographic scope, last review, conflicting handling, min primary sources, expert reviewer, citation requirements, benchmark, accuracy/hallucination metrics, knowledge-pack version - still valid.

**docs/ops/:**
- GITHUB_WORKFLOW.md, BRANCHING_STRATEGY.md, GITHUB_LABELS.md, MILESTONE_PLAN.md, DEFINITION_OF_DONE.md (now includes HttpOnly cookies Secure SameSite short-lived CSRF, Persian baseline RTL), RELEASE_STRATEGY.md, AGENT_RUNBOOK.md, REPORTING_CADENCE.md - still valid, but branching strategy mentions mvp/v1-core-foundation as future branch like example, now mvp branch does not exist remotely (we checked), and archive branch exists.

**docs/backlog/:**
- EPICS.md 11 epics - still valid.
- PHASE_0_ISSUES.md 13 issues + ISSUE-0-14 repository metadata update - Phase 0 is completed, but issues still open? Some issues like README update already done, but still listed as open? Could be obsolete.
- PHASE_1_ISSUES.md 5 issues: auth User model, chat echo, frontend landing, docker compose, wallet mock - but wallet is now real atomic, not mock, so issue description outdated (says wallet mock).
- PHASE_2_ISSUES.md 4 issues: persona framework implementation, persona chat API, directory UI, QA red teaming - not implemented.
- AGENT_SYSTEM_ISSUES.md 7 issues including new 8 agents and governance docs - partially implemented (governance docs now exist).
- GROWTH_MARKETING_ISSUES.md 4 issues - not implemented.
- WEBSITE_ISSUES.md 4 issues - not implemented.
- PERSONA_ISSUES.md 5 issues - not implemented beyond 2 seed.

**docs/website/:**
- WEBSITE_INFORMATION_ARCHITECTURE.md 15 pages: Home, Chat, Personas, Product Studio, Image, Video, Character, API, Telegram, Business, Pricing, Blog, Docs, Use-Cases, Contact, Terms, Privacy, Refund, Safety - not implemented, frontend still legacy product list, not Persian-first landing.

**Frontend Structure:**
- frontend/ still has legacy Next.js pages structure: src/components/CategoryFilter.js, ProductCard.js (product reseller UI), src/pages/index.js, login.js, order.js, payment.js, etc., next.config.js with rewrites to localhost:8000/api, tailwind.config.js, postcss.config.js. No new Persian AI Workspace landing, no Next.js 14 App Router, no TypeScript, no Header.tsx, ChatBox.tsx, lib/api.ts, etc. The MVP skeleton from branch mvp/v1-core-foundation (which had new Next.js 14 landing) was never merged to main - only database and auth and wallet were merged. So frontend is obsolete and contradicts persona of Persian-first AI Workspace.

**Backend Structure:**
- backend/app/models/ now has 10 models including payment_intent, which matches Part 3A, but also has old legacy files still present? Let's check: backend/app/ has agents, data, main.py, models, schemas, services, tasks.py, templates, utils. Agents folder has monitoring_agent, seo_agent, seo_agents_config - legacy from old reseller, not needed for new platform. Data folder has products_data.py (42KB static product list hard-coded from reseller) - obsolete, should be archived. Services folder has old legacy crypto_service, order_service, payment_service (old), product_service, zarinpal_service, plus new wallet_service, payment_service (new overwrites old? Actually we overwrote payment_service.py with new payment intent service, so old legacy payment_service is gone? But we have both old and new? We overwrote payment_service.py with new, so old legacy payment_service (which was payment coordinator) is gone, but we have new one. However services still has crypto_service, order_service, product_service, zarinpal_service which are legacy reseller services, not needed. Tasks.py has old Celery tasks with ndef syntax error previously fixed? Now tasks.py still exists but not used. Templates folder only .gitkeep. Utils folder only __init__.py placeholder.

- So backend has mix of new (user, wallet, ledger, persona, conversation, message, api_key, auth_session, password_reset_token, payment_intent, database.py, config.py, seed.py, main.py minimal, api/auth.py, api/wallet.py, api/payments.py, api/admin.py, core/security.py, deps.py, csrf.py, rate_limit.py, services/wallet_service.py, payment_service.py, exchange_rate.py, providers/payment/*) and old legacy (agents, data, services/crypto_service etc? Actually crypto_service etc still there, but we have new providers). So backend is partially cleaned but still has legacy files that are dead code and should be archived or removed.

**Merged PR History:**
- PR #1: audit/repo-rescue - forensic audit and recovery plan - docs only
- PR #2: docs/phase-0-agent-operating-system - 105 files ~7800 lines, Agent OS 28 agents, roadmap, governance docs, merged at e4ad2f1 (merge commit) and f1e6b96 cleanup and 022bcc9 merge of cleanup - actually PR #2 had 4 commits: b9c8e98 initial, 6c6c406 corrections, e506146 L1/L2 consistency, f78f97b L1 cleanup, merged at e4ad2f1? Wait log shows e4ad2f1 is merge of PR #2, but PR #2 had commits b9c8e98, 6c6c406, e506146, f78f97b, and merge commit e4ad2f1 is merge of PR #2? Actually log shows 27af60c is merge of wallet, 0e4fdba is merge of auth, e4ad2f1 is merge of Phase 0 docs, 8b2c2c7 forensic audit. So PR history is coherent: audit, phase 0 docs, cleanup, database, auth, wallet.

- Auth PR #5: build/phase-1-part2-auth at d706a47, merged at 0e4fdba with 8 files? Actually PR #5 had 21 files? Wait earlier we had 21 files for auth, merged.

- Wallet PR #6: build/phase-1-part3a-wallet at ac1074c, merged at 27af60c with 21 files.

- So merged PR history for auth and wallet is present and clean, no conflicts (merge commits clean).

---

## 3. Contradictions, Drift, Duplicates, Obsolete Statements, Role/Agent Conflicts

### Contradictions - Documented vs Implemented

1. **README Status Drift:** README says "Status: Phase 0 - Foundation documentation merged to main on 2026-07-19. Currently preparing Phase 1 Part 1 (Database Schema)." - obsolete, main now at Phase 1 Part 3A merged (wallet, ledger, payment intents). Should say Phase 1 Part 3A merged, preparing Part 3B/4.

2. **Roadmap Master Status Drift:** docs/roadmap/MASTER_ROADMAP.md says Phase 0 Current, Phase 0 Foundation, but Phase 0 is completed and merged, Phase 1 Part 1, 2, 3A are completed and merged. Should update to Phase 1 Part 3A current, Phase 0 completed.

3. **PHASE_0_FOUNDATION.md:** Says Status Planned (Phase 0 is current), exit criteria branch docs/phase-0-agent-operating-system pushed PR opened not merged - but PR #2 is merged at e4ad2f1, so exit criteria met, should be marked completed.

4. **PHASE_1_CORE_MVP.md:** Says out of scope payment integration, admin dashboard, personas, image studio, etc., but we have implemented wallet real atomic operations (not mock) and payment intents with mock provider, and admin wallet grant endpoint (POST /admin/wallet/{user_id}/grant) which is admin dashboard-like. Also says wallet mock, but we have wallet real, not mock. Also says Persian full UI out of scope, but also says Persian-first baseline Must in Phase 1 - contradiction within same doc after correction: says full localization polish may be deferred but baseline Persian UX may not be out of scope - actually after correction, baseline Persian UX is must, so out of scope list should not include Persian full UI but should include full polish.

5. **PHASE_1_ISSUES.md:** Lists wallet mock display, but wallet is now real atomic, not mock. Also says no payment integration, but payment intents implemented.

6. **Frontend vs Backend:** Frontend is still legacy reseller UI (ProductCard, CategoryFilter, order.js, payment.js) with hard-coded product_id=1, calls /api/products/prices which depends on missing pricing_agent, and /api/payments/create that doesn't exist in new backend (new backend has /payments/create not /api/payments/create? Actually new backend has /payments/create with prefix /payments, and frontend old calls /api/payments/create which would be proxied? Need to check). So frontend is completely obsolete and contradicts backend auth/wallet implementation which has new Next.js 14 landing in branch mvp/v1-core-foundation that was never merged. So frontend on main is dead code, not aligned with Persian AI Workspace vision.

7. **Backend Legacy Files:** backend/app/agents/monitoring_agent.py, seo_agent.py, seo_agents_config.py, data/products_data.py (42KB static product list), services/crypto_service.py, order_service.py, product_service.py, zarinpal_service.py, tasks.py, templates/.gitkeep, utils/__init__.py placeholder - these are legacy reseller files, not needed for new platform, should be archived. They contradict new provider abstraction which says no scraping GGSel/FunPay, no shared accounts, but these files are still present.

8. **Agent Counts vs Implementation:** Docs say 28 project-building agents active, but backend has no agent code, only docs. That's okay as docs, but docs say 28 agents are active in Phase 0-2, but Phase 0-2 is completed, and we are now in Phase 1 Part 3A. Should update to reflect that project-building agents are not active code, only docs, and some have been used to build database/auth/wallet.

9. **Persona Counts:** docs/personas/INITIAL_PERSONA_BACKLOG.md says 14 personas, but backend only has 2 seed placeholder personas (general-assistant low/active and psychologist-draft high/draft) with literal "NOT READY FOR PRODUCTION". Docs say 14 personas backlog, but implemented only 2 seed, and those 2 are development seeds not approved production personas. So documented 14 vs implemented 2.

10. **Wallet Documentation Drift:** docs/vision/BUSINESS_MODEL.md says wallet ledger must be auditable, credit purchase → ledger entry → balance update atomic, spend actions idempotent, daily spend limits, human approval for refunds above threshold. Implemented wallet_service does atomic credit/debit with SELECT FOR UPDATE and idempotency, but daily spend limits not implemented, human approval for refunds not implemented (refund_wallet exists but no approval gate). Also says credit-based SaaS with wallet, but docs/roadmap/PHASE_1_CORE_MVP.md says wallet mock - contradiction.

11. **Payment Intent vs Credit Packages:** docs say credit packages defined in config not hardcoded, which is implemented (CREDIT_PACKAGES in config.py with 3 packages), but docs/roadmap/PHASE_1_CORE_MVP.md says no payment integration, but we have payment intents and packages implemented in Phase 1 Part 3A, so Phase 1 doc should be updated to reflect wallet and payment intents implemented in Part 3A, not out of scope.

12. **Auth vs Old Models:** backend/app/models/__init__.py now has 10 models including payment_intent, but old legacy file backend/app/models/models.py missing? Actually old models.py doesn't exist, we have new models. Old main.py that referenced Product, CompetitorPrice, etc. was replaced with minimal app, so old references removed - good. But some old services still reference Product, etc. (e.g., product_service.py) which are dead code.

13. **Exchange Rate:** docs/architecture/PROVIDER_ABSTRACTION_STRATEGY.md says provider config in env, cost tracking, retry, etc., but exchange_rate.py returns static rate 190600 from settings, not real API, which matches MVP spec (static rate) but docs say later real API Bonbast/Arzbin. So okay, but docs say real-time rate from Bonbast/Arzbin API later, which is documented as deferred, so not contradiction, but should note static rate is MVP.

14. **API Endpoints vs Docs:** docs list API endpoints like POST /auth/register, /auth/login, /auth/me, POST /chat (echo test) but now we have POST /auth/register, login, logout, refresh, me, password-reset, plus wallet and payments endpoints, but not /chat echo test (that was from mvp/v1-core-foundation branch which had chat echo, but main's auth implementation does not have /chat echo, it has wallet and payments). So docs/roadmap/PHASE_1_CORE_MVP says POST /chat echo test protected, but main's backend after Part 3A does not have /chat endpoint (it has auth, wallet, payments, admin). So chat endpoint missing.

15. **Roles vs Agents Conflict:** Roles defined in business model? Not clear. Between project-building agents and runtime product agents: Orchestrator is defined as not writing product code, only docs/planning PRs, but in earlier commits Orchestrator was L2 with branch+PR, now corrected to docs/planning only. However, some docs still say Orchestrator may open documentation/planning PRs, but also say Fullstack Builder, Website Builder, DevOps implement code. That's consistent after fix, but some older docs in ops may still say Orchestrator coordinates all agents and unblocks founder, which could imply code writing - need to check.

16. **Growth and Persona Docs vs Implementation:** docs/growth/GROWTH_SYSTEM.md says growth loops SEO→landing→signup→activation→referral, metrics visits, signup conversion, etc., but no growth loops implemented. That's okay as docs, but says no auto-publishing without review - correct, but no code for growth.

17. **Safety Docs vs Implementation:** docs/safety/TRUST_AND_SAFETY_FRAMEWORK.md says image NSFW filter, video consent gate, Telegram anti-spam, etc., but no implementation for image/video yet - okay as planning, but should be marked as future.

18. **Obsolete Phase 0 Statements:** Many files under docs/roadmap/ still say "Status: Planned (Phase 0 is current)" - should be updated to completed. Also docs/roadmap/MASTER_ROADMAP.md says Phase 0 Current - should be Phase 1 Part 3A current. README says "Project Structure Now (Phase 0)" - should be Phase 1 Part 3A.

19. **Duplicate Concepts:** 
- Wallet and credit billing appears in both PRODUCT_VISION and BUSINESS_MODEL and WALLET_AND_PAYMENTS.md and PHASE_1_CORE_MVP, with slightly different descriptions (mock vs real atomic) - duplicate and contradictory.
- PaymentIntent lifecycle appears in WALLET_AND_PAYMENTS.md and payment_service.py docstring and PHASE_3 docs - duplicate but okay, but should be single source.
- Persona system appears in PERSONA_FRAMEWORK, RUNTIME_AGENT_OVERVIEW, BUSINESS_AGENT_ARCHITECTURE, etc. - some duplication, but okay if consistent.

20. **Agent Registry vs Implementation:** Registry lists 28 project-building agents, but backend has no agent code, only docs. That's okay for Phase 0, but after Phase 1 Part 3A, some agents like Fullstack Builder have been used to build database/auth/wallet, but not tracked as implemented. Could update registry status to reflect which agents have been used.

### Missing Capabilities (Documented but Not Implemented)

- General Persian chat (no /chat endpoint in main after wallet merge? Actually main's main.py after wallet merge includes auth, wallet, payments, admin routers, but not chat - chat was in mvp/v1-core-foundation branch not merged. So general chat missing.)
- Prompt enhancement (no endpoint)
- Specialist personas (only 2 seed placeholder, not 5 initial personas, no persona chat API /personas/{id}/chat)
- Image generation and product photography studio (not implemented)
- Video generation, character/influencer tools (not implemented)
- Telegram integration (not implemented)
- Developer APIs (ApiKey model exists but no API for developer API keys management, no /v1/chat, /v1/image)
- Business agents (FAQ, lead qualifier, content drafter) - not implemented
- Research and RAG (no upload docs, no pgvector, no embeddings)
- Agent Marketplace (future idea)
- Website: No Persian-first landing, no Next.js 14 App Router, no Header.tsx, ChatBox.tsx, lib/api.ts, etc. - frontend still legacy reseller, not the new landing from mvp branch.
- Growth: No SEO topic clusters implementation, no content engine, no landing page types, no programmatic SEO.
- Safety: No image NSFW filter, video consent, Telegram anti-spam enforcement beyond rate limiting.
- Evaluation: No evals folder, no benchmark datasets.

### Obsolete Assumptions

- Assumes no database - but now database exists with 3 migrations, 10 tables, wallet real atomic.
- Assumes no auth - but auth exists with HttpOnly cookies, 6 endpoints, rate limiting, CSRF.
- Assumes wallet mock - but wallet is real atomic credit/debit with SELECT FOR UPDATE and idempotency.
- Assumes no payment intents - but payment_intents exists with sandbox mock provider.
- Assumes legacy reseller model is deprecated and archived - true, but some legacy files still present in backend/app/agents, data, services (crypto_service, order_service, etc) that should be archived.
- Assumes frontend is Next.js pages with ProductCard etc - still true on main, but should be replaced with new Persian-first landing per Phase 1 - obsolete.

### Conflicts Between Roles and Agents

- Orchestrator originally defined as coordinating all agents and unblocking founder, with allowed outputs roadmap updates, issue breakdowns, etc., and forbidden from writing product code. This is now correctly separated after fix, but some older docs in ops (AGENT_RUNBOOK.md) may still say Orchestrator coordinates all and unblocks, which could imply code writing - need to check.
- Fullstack Builder, Website Builder, DevOps are L2 that may create branch+PR for code, while Product Manager, Research, etc. are L1 report/draft only - this is now consistent after fix (19 L1 +9 L2), but some docs still say all 20 (now 28) are L2 - we fixed in 5 files, but other docs like docs/backlog/AGENT_SYSTEM_ISSUES.md may still say 20 agents, or docs/ops/GITHUB_LABELS.md lists agent labels but not updated for new 8 agents? Need to check.
- Persona roles: Psychologist defined as evidence-based structured direct mental-health information and guided-assessment assistant, not generic compassionate companion - this conflicts with older persona backlog that said "Psychologist, evidence-based, structured, direct tone" but also had generic description? We fixed to structured direct, not generic companion.
- Business agents: Customer Success Agent drafts support replies but not send, Sales/Partnership drafts outreach but not send - this is consistent with human approval gates, but docs/growth/SOCIAL_MEDIA_PLAN says Social Media Agent drafts posts, founder approves and manually publishes - consistent.

---

## 4. Architecture Risks

- **In-Memory Rate Limiting:** Simple dict deque, not distributed, acceptable for MVP single instance, but in production multi-instance, rate limiting would be bypassed by hitting different instances. Documented that Redis-backed will be added later, but no code for Redis yet. Risk: DoS via distributed requests.
- **SELECT FOR UPDATE Ignored in SQLite:** Used in wallet_service._get_wallet_for_update with with_for_update(), but SQLite ignores FOR UPDATE. In Postgres it locks row, but in SQLite tests it doesn't, so concurrent debit test uses threading but may not truly test race condition. In production Postgres, it works, but tests in SQLite may give false confidence. Risk: Race condition in SQLite dev may not be caught, but Postgres should handle.
- **String UUID Primary Keys:** Changed from PostgreSQL UUID type to String(36) for SQLite compatibility. In Postgres, UUID type is more efficient and has native validation. String(36) works but less efficient, no native UUID validation. Decision documented as compatibility, but risk: less efficient, no native UUID ops.
- **JSONB Variant:** Uses JSONB().with_variant(JSON(), 'sqlite') for scopes and verification_data. Generic JSON fallback for SQLite may not support JSONB operators, but for MVP acceptable. Risk: Queries using JSONB operators may fail in SQLite tests but work in Postgres.
- **HttpOnly Cookies Secure False in Dev:** In auth.py, secure=False for local http, comment says True in production. Risk: If deployed with secure=False in production, cookies sent over http, vulnerable to MITM. Need to ensure env var to set Secure True in prod.
- **Mock Payment Provider Always True:** MockPaymentProvider.verify_payment always returns True, initiate returns fake authority. Clearly marked SANDBOX ONLY, but if PAYMENT_PROVIDER env var accidentally set to sandbox_mock in production, real payments would be bypassed, crediting wallet without real payment. Risk: Financial loss if mock used in prod. Mitigation: is_sandbox_provider check and 403 if not sandbox for simulate-complete, but initiate still returns fake even in prod if env is sandbox_mock. Need to ensure production env never has sandbox_mock.
- **Static Exchange Rate:** DEFAULT_EXCHANGE_RATE 190600 Toman per USD, static, not real-time. Risk: Rate fluctuation could cause loss if Toman devalues, or overcharge if appreciates. Documented as MVP static, later real API.
- **No Device Management UI:** Auth sessions stored but no UI to list active sessions, revoke specific device. User cannot see where logged in. Risk: Account takeover, user cannot revoke stolen session.
- **No Audit Log Table:** Auth events, wallet transactions, payment intents have created_at but no dedicated audit log table for agent actions, admin grant, etc. Wallet ledger is append-only but not full audit log for auth.
- **No 2FA:** Deferred, risk of account takeover via password.
- **Frontend Obsolete:** Frontend still legacy reseller, not Persian-first, not using new auth cookies (old frontend used localStorage token). Risk: Frontend cannot use new backend auth, users cannot login via UI, only via API.
- **Legacy Backend Files:** Still present: agents, data/products_data.py 42KB, services/crypto_service, order_service, product_service, zarinpal_service, tasks.py, templates, utils placeholder - dead code, bloat, potential confusion, may have vulnerabilities (e.g., crypto_service mock verification always True).

## 5. Privacy Risks

- **IP Hashing Truncated 64 chars:** hash_ip returns SHA256 hex truncated to 64 chars (full SHA256 hex is 64 chars, so truncation to 64 is actually full? SHA256 hex is 64 chars, so [:64] is full, okay). But hashing IP with SHA256 without salt is reversible via rainbow table for small IP space (IPv4 32-bit). Better to use HMAC with secret or add salt. Current is SHA256(ip) truncated, which is deterministic and could be reversed via brute force for IPv4. Risk: Privacy of IP not fully protected.
- **User Agent Hashing Same:** Similar, SHA256 truncated, deterministic, could be reversed? User agent space large, but still deterministic.
- **No Encryption at Rest for Secrets:** ApiKey key_hash is hashed, good, but key_prefix non-secret stored plain, okay. AuthSession token hashes stored, raw tokens not stored, good. Telegram bot tokens (future) not yet implemented, but if implemented must be encrypted at rest (Fernet/Vault) per DATA_CLASSIFICATION doc, not yet done.
- **Data Classification:** Docs say Confidential data (user content, wallet, API keys hashed, tokens encrypted) need access control, but no RLS, no row-level security, only application-level filtering via user_id filter in get_transaction_history and get_user_payments. Tested users only see own data, but no database-level RLS, so if app bug, cross-tenant leakage possible. IDOR tests exist for wallet and payments, but not for conversations/messages? Need to ensure.
- **No User Data Deletion Workflow:** Docs say retention 7 years for wallet ledger, active+30 days for user account, but no code for GDPR deletion, no soft-delete, no anonymization. Risk: Compliance.
- **No PII in Logs:** Code avoids logging passwords/raw tokens, good, but need to ensure no email, IP, user agent logged as PII.

## 6. Financial Risks

- **Wallet Balance Cached:** balance_credits is cached/materialized, not derived on every read via SUM(ledger). If bug in credit/debit logic, balance may drift from SUM. Documented reconciliation must compare wallet balance with SUM(ledger.amount) - but no reconciliation job implemented yet. Risk: Balance drift, financial inconsistency.
- **Idempotency Handling Race:** credit_wallet checks idempotency BEFORE transaction, then INSERT, but race condition where two concurrent requests with same idempotency_key could both pass check before either inserts, then both insert, second fails with IntegrityError, caught and returns existing balance. This is handled via IntegrityError catch and return existing, but could still cause double credit if first transaction commits after second check? Actually second check after IntegrityError returns existing balance, so no double credit, but first transaction's balance update may have happened, second returns same balance, okay. For debit, similar.
- **No Daily Spend Limits:** Docs mention daily spend limits as future, not implemented. Risk: User could spend all credits quickly, no limit, but not financial loss to platform, only user.
- **No Human Approval for Refunds Above Threshold:** Docs say human approval required for refunds/credits above threshold (e.g., >$5), but refund_wallet and admin grant have no approval gate check, admin can grant any amount directly. Risk: Admin could grant large credits without approval.
- **Mock Provider Always True:** If PAYMENT_PROVIDER env var accidentally set to sandbox_mock in production, simulate-complete endpoint would allow anyone to credit wallet without real payment, leading to free credits, financial loss. Mitigation: is_sandbox_provider check returns 403 if not sandbox, but if env is sandbox_mock in prod, it would allow. Need to ensure production env never has sandbox_mock, and maybe add additional check: if settings.DEBUG is False and provider is sandbox_mock, block simulate-complete.
- **Static Exchange Rate:** 190600 Toman per USD static, if real rate changes, credits_to_add vs amount_toman mismatch could cause loss or overcharge. No real-time rate yet.
- **Credit Packages Hardcoded in Config:** Defined in config.py CREDIT_PACKAGES list, not hardcoded in business logic per spec, good, but prices are static and not validated against real costs, no official dated source for pricing, per NO-GO rule should not add real pricing without official dated source. Current prices 299000 Toman for 1000 credits etc. are placeholder, not from official source, but okay as config for MVP.

## 7. Recommended Documentation Changes

- **README.md:** Update status line from "Phase 0 - Foundation documentation merged to main on 2026-07-19. Currently preparing Phase 1 Part 1 (Database Schema)." to "Phase 1 Part 3A - Wallet, Ledger, Payment Intents merged to main on 2026-07-20 (commit 27af60c). Currently preparing Phase 1 Part 3B (ZarinPal) and 3C (Crypto) and Phase 2 Personas." Also update Quick Start to reflect docs now on main and Phase 1 Part 3A, not Phase 0 docs only, and remove reference to branch docs/phase-0-agent-operating-system as source of truth. Update agent counts: now 28 project-building = 19 L1 + 9 L2, but also mention 10 backend models now (was 7), 3 migrations, etc. Update documentation map counts: now 90 files → now 105+ files (actually after Phase 1 Part 3A, we have 105+ plus new files, now maybe 120+).
- **MASTER_ROADMAP.md:** Change Phase 0 status from Current to Completed, Phase 1 Part 1, Part 2, Part 3A to Completed, Phase 1 Part 3B, 3C, Phase 2 to Current/Next. Update cross-cutting systems: Agent OS completed, Growth System still planning, etc.
- **PHASE_0_FOUNDATION.md:** Mark as Completed, exit criteria met (branch pushed, PR merged, not just opened). Update date.
- **PHASE_1_CORE_MVP.md:** Update to reflect actual implemented state: User model with normalized_email, wallet real atomic not mock, auth with HttpOnly cookies Secure SameSite CSRF, Persian-first baseline still not fully implemented (frontend still legacy), chat echo not implemented, prompt enhancer not implemented, wallet mock vs real contradiction. Should split Phase 1 into Part 1 Database (completed), Part 2 Auth (completed), Part 3A Wallet/PaymentIntents (completed), and remaining Part 1 Core MVP tasks: general chat, prompt enhancer, landing Persian-first, header/chatbox components. Currently Phase 1 doc lumps everything but should be updated.
- **PHASE_0_COMPLETION_REPORT.md:** Already documents Phase 0 complete, but now Phase 1 Part 1,2,3A also completed, need new completion report for Phase 1 Part 3A.
- **SYSTEM_CONTEXT.md:** Update backend description from "JWT HttpOnly cookies, wallet ledger mock Phase 1" to "HttpOnly cookies for session/refresh, wallet real atomic with SELECT FOR UPDATE, ledger append-only signed credit ledger, payment intents with sandbox mock provider".
- **PROVIDER_ABSTRACTION_STRATEGY.md:** Update to reflect payment provider abstraction implemented (mock provider) vs chat/image/video provider abstraction still planning.
- **DATA_CLASSIFICATION_AND_RETENTION.md:** Update retention schedule to reflect actual tables: auth_sessions, password_reset_tokens, payment_intents added, with retention.
- **GITHUB_WORKFLOW.md, BRANCHING_STRATEGY.md:** Update to mention new branches build/phase-1-part3a-wallet merged, now no build branches remaining, and mvp/v1-core-foundation branch mentioned as future example but does not exist remotely - should be removed or marked as example not present.
- **DEFINITION_OF_DONE.md:** Already updated with HttpOnly cookies and Persian baseline, good, but should also mention wallet atomic operations, idempotency, balance never negative, and check constraints.
- **BACKLOG docs:** PHASE_0_ISSUES.md has 13 issues, some completed (README update, agent OS docs, etc.) should be marked completed; PHASE_1_ISSUES.md says wallet mock display but wallet now real atomic, should update.
- **Frontend docs:** All website/growth docs assume new frontend with Next.js 14 App Router, but main frontend still legacy reseller. Need to document that frontend is obsolete and needs replacement per mvp/v1-core-foundation branch (which had new landing, login, register, dashboard) that was never merged.
- **Agent Registry:** Should update status of agents that have been used: Fullstack Builder used for database/auth/wallet, DevOps for docker-compose, etc., not just active in Phase 0-2.
- **Persona Backlog:** Should update maturity of general-assistant from planned to active (since seeded as active) and psychologist-draft from idea to draft (seeded as draft).
- **CHANGELOG.md:** Currently only has entry for 2026-07-19 Phase 0 Foundation Merged, need new entry for 2026-07-20 Phase 1 Part 1, Part 2, Part 3A merged with details.

## 8. Recommended Implementation PR Sequence (After Phase 1 Part 3A)

**Immediate Next (Phase 1 Part 3B & 3C & Polish):**

1. **PR: build/phase-1-part3b-zarinpal (Part 3B)** - Real ZarinPal integration: Implement ZarinPalProvider that calls ZarinPal API with merchant ID, initiate returns authority, verify calls verification API with authority and amount, get status. Add ZarinPal sandbox test credentials (not real secrets, sandbox only), add provider_reference handling, add tests with mocked ZarinPal responses, no real API calls in tests. Depends on payment_intents table and provider abstraction. Requires human approval for spending (initiate payment) and for changing provider config.

2. **PR: build/phase-1-part3c-crypto (Part 3C)** - Real crypto verification: CryptoTRC20Provider and CryptoTONProvider that verify blockchain transaction via TronGrid/Ton API, check recipient address matches wallet_address, exact amount matches amount_crypto as string to preserve decimal precision, confirmation count, transaction existence, status, etc. Use mock in tests, no real blockchain calls in tests (mocked). Add wallet_address generation (real address from config for now, later per user). Add verification_data storing blockchain confirmation details.

3. **PR: build/phase-1-part4-exchange-rate (Part 4 Exchange Rate)** - Real-time rate from Bonbast/Arzbin API with caching: Implement exchange_rate service to fetch real rate, cache in DB or Redis, fallback to static 190600, add config for API key (placeholder), add tests with mocked API. Depends on exchange_rate_snapshot logic already.

4. **PR: build/phase-1-part4-cleanup-backend-legacy** - Remove legacy backend files: agents/monitoring_agent, seo_agent, seo_agents_config, data/products_data.py (42KB), services/crypto_service, order_service, payment_service legacy (now overwritten with new payment_service but old files still exist? Actually payment_service now new, but crypto_service, order_service, product_service, zarinpal_service old still exist), tasks.py, templates, utils placeholder. Archive to archive/legacy_2026-07-19 already exists but main still has them. This PR should delete old legacy files from main that are dead code and contradict new platform.

5. **PR: build/phase-1-part5-frontend-foundation (Frontend Persian-First)** - Replace legacy frontend reseller UI with new Next.js 14 App Router, TypeScript, Tailwind, RTL, Persian typography, Header, ChatBox, lib/api.ts Axios instance with JWT interceptor replaced by HttpOnly cookie handling (withCredentials), auth.ts token storage removed (no localStorage), pages: landing public, login, register, dashboard protected chat test, etc. From branch mvp/v1-core-foundation which already had skeleton but not merged. This would align frontend with backend auth/wallet.

**After Phase 1 Foundation Complete:**

6. **PR: build/phase-2-personas-part1-framework** - Implement persona framework code: persona registry schema validation, persona directory API /personas/list, /personas/{id}/chat, prompt versioning, audit logs, wallet deduct for persona chat. Depends on personas table and 2 seed personas.

7. **PR: build/phase-2-personas-part2-qa** - Implement 5 initial low-risk personas (Prompt Engineer, Researcher, SEO Advisor, Instagram Strategist, Product Photography Advisor) with evidence-based prompts, QA and red teaming reports, compliance review.

8. **PR: build/phase-3-image-studio (Image Studio & Product Photography)** - Image generation provider abstraction, product photography studio workflow upload→prompt enhance→generate→gallery, S3 compatible storage, cost per image, NSFW filter.

9. **PR: build/phase-4-api-platform (Developer API)** - ApiKey management: POST /api-keys create/delete/list, GET /api-keys/{id}, middleware X-API-Key auth, rate limit 60/min, credit check, usage logs table api_usage_logs, docs page with curl examples.

10. **PR: build/phase-5-video-character (Video & Character)** - Video generation async job queue, character creation, consent gate for real person.

11. **PR: build/phase-6-telegram-business (Telegram & Business Agents)** - Telegram webhook, bot token encrypted, business agents FAQ/lead/content drafter, execution logs, anti-spam.

12. **PR: build/phase-7-research-rag (Research & RAG)** - Upload docs, chunking, embeddings, pgvector, RAG attachment with citations, research persona.

13. **PR: build/phase-8-agent-marketplace-concept (Marketplace Idea)** - Concept doc only, no code, per MASTER_ROADMAP.

**Each PR must:**
- Be from main latest (currently 27af60c)
- Have Draft PR with DO NOT MERGE until owner security review for financial/auth
- Include tests (pytest, PostgreSQL integration via Testcontainers, 65+ passed)
- Include docs update
- No secrets, no real provider API calls unless sandbox, no bypassing ToS/KYC
- Human approval gates for publishing/spending/pricing/config/merge/deploy

## 9. Risks Requiring Owner Approval

**Financial Risks:**
- Wallet balance cached vs SUM(ledger) reconciliation not implemented - could drift. Needs reconciliation job and alerting - owner approval for implementation.
- Mock provider always True - if PAYMENT_PROVIDER env var accidentally set to sandbox_mock in production, free credits. Needs check that production env never has sandbox_mock, and simulate-complete endpoint must be disabled in production (currently checks is_sandbox_provider but if env is sandbox_mock in prod, it would allow). Requires owner approval for env config and additional guard: if DEBUG False and provider sandbox_mock, block simulate-complete.
- Static exchange rate 190600 - could cause loss if Toman devalues. Needs real-time rate with caching, owner approval for rate source (Bonbast/Arzbin).
- Admin grant endpoint POST /admin/wallet/{user_id}/grant allows admin to grant any amount without approval gate for amount threshold. Docs say human approval required for refunds/credits above threshold (e.g., >$5). Currently no threshold check. Needs approval gate implementation.

**Privacy Risks:**
- IP hashing truncated 64 chars (actually full SHA256 hex is 64, so not truncated, but SHA256 without salt is reversible for IPv4 via rainbow table). Better HMAC with secret. Needs Data Privacy Governance review.
- User agent hashing similar.
- No encryption at rest for secrets: ApiKey key_hash is hashed, good, but key_prefix plain, okay. AuthSession token hashes, good. Telegram bot tokens future must be encrypted at rest (Fernet/Vault) per DATA_CLASSIFICATION doc, not yet implemented.
- No RLS, only application-level filtering for wallet and payments and conversations. IDOR tests exist for wallet and payments, but not for conversations/messages. Risk cross-tenant leakage if app bug.

**Architecture Risks:**
- In-memory rate limiting not distributed - DoS via distributed requests from different IPs? Actually rate limiting per IP, but in-memory per instance, multi-instance would bypass. Needs Redis later.
- SELECT FOR UPDATE ignored in SQLite - concurrent debit test uses threading but SQLite ignores FOR UPDATE, so test may give false confidence. In Postgres it works, but need to ensure production uses Postgres 15, not SQLite.
- String UUID PKs - less efficient than native UUID, no native validation.
- JSONB variant - generic JSON fallback for SQLite may not support JSONB operators.
- HttpOnly Secure False in dev - risk if deployed with secure=False in prod. Need env var to set Secure True in prod via settings.
- Legacy backend files still present - dead code, bloat, confusion, potential vulnerabilities (e.g., old crypto_service mock verification always True still present? Actually we overwrote payment_service but crypto_service, order_service, etc. still exist with old mock verification).
- Frontend obsolete - cannot use new backend auth, can't login via UI, only via API, so activation metric cannot be measured.
- No device management UI, no session list, no 2FA, no audit log table.

**Safety Risks:**
- No image NSFW filter, video consent gate, Telegram anti-spam enforcement beyond rate limiting - documented in TRUST_AND_SAFETY_FRAMEWORK but not implemented.
- Persona risk: Only 2 seed placeholder personas, not 5 initial low-risk personas, and high-risk psychologist-draft contains NOT READY string but no domain-expert review, no QA report yet.
- No medical/legal/psych authority claims currently in backend (good), but persona framework allows future high-risk personas that must have disclaimers and escalation.

**Compliance Risks:**
- No GDPR deletion workflow, retention 7 years for wallet ledger draft, but no code.
- No Terms, Privacy, Refund, Safety pages implementation - only docs/website requirements docs, no actual pages.
- Supplier scout agent: docs say it researches AI model providers, but old code in backend/app/agents/ mentions GGSel/FunPay procurement - need to ensure no procurement agent code that automates purchasing from marketplaces is present (we have monitoring_agent etc legacy, but not procurement_agent? Actually procurement_agent.py missing per earlier audit, but data/products_data.py still present with 42KB product list - should be archived).

---

## 10. Files Created in This Audit PR

- **docs/audits/PRODUCT_ARCHITECTURE_ALIGNMENT_AUDIT_2026-07-23.md** (this file)

## 11. Files Updated in This Audit PR (if any)

- None yet - this audit is documentation only, no production code changed. README and other docs will be updated in subsequent cleanup PRs per recommended documentation changes.

## 12. Documentation Contradictions Found (Summary List)

1. README status line obsolete: says preparing Phase 1 Part 1, but Part 3A merged.
2. MASTER_ROADMAP.md says Phase 0 current, but Phase 0 completed.
3. PHASE_0_FOUNDATION.md says Status Planned, exit criteria not met, but actually completed and merged.
4. PHASE_1_CORE_MVP.md says wallet mock and out of scope payment integration, but wallet real atomic and payment intents implemented.
5. PHASE_1_ISSUES.md says wallet mock display, but wallet real.
6. Frontend legacy reseller UI contradicts backend new auth/wallet and Persian-first vision.
7. Backend legacy files (agents, data/products_data.py, services/crypto_service, order_service, product_service, zarinpal_service, tasks.py, templates, utils) contradict new provider abstraction which says no scraping GGSel/FunPay.
8. Agent counts vs implementation: docs say 28 project-building active, but no agent code.
9. Persona counts: docs say 14 backlog, implemented only 2 seed.
10. Wallet documentation: BUSINESS_MODEL says wallet ledger auditable, but docs/roadmap says wallet mock - contradiction.
11. API endpoints: docs list POST /auth/register, /auth/login, /auth/me, POST /chat echo, but main backend has no /chat echo (was in mvp branch not merged).
12. Exchange rate: SYSTEM_CONTEXT says JWT HttpOnly, wallet ledger mock Phase 1, but wallet real.
13. Growth docs assume new frontend: SEO topic clusters, landing types, but frontend still legacy.
14. Safety docs assume image NSFW filter etc not implemented.

## 13. Recommended Implementation PR Order (After This Audit)

1. **docs/cleanup-phase0-obsolete-statements** - Update README status, MASTER_ROADMAP, PHASE_0_FOUNDATION, PHASE_1_CORE_MVP, PHASE_0_COMPLETION_REPORT, SYSTEM_CONTEXT to reflect Phase 1 Part 3A merged, Phase 0 completed. (Docs only, no code)
2. **build/phase-1-part3b-zarinpal** - Real ZarinPal integration (Part 3B)
3. **build/phase-1-part3c-crypto** - Real crypto verification (Part 3C)
4. **build/phase-1-part4-exchange-rate** - Real-time rate Bonbast/Arzbin with caching
5. **build/phase-1-part4-cleanup-backend-legacy** - Delete legacy backend files agents/*, data/products_data.py, services/crypto_service, order_service, product_service, zarinpal_service, tasks.py, templates, utils placeholder (archive already exists)
6. **build/phase-1-part5-frontend-foundation** - Replace legacy frontend with new Next.js 14 App Router Persian-first landing, login, register, dashboard from mvp/v1-core-foundation branch
7. **build/phase-2-personas-part1-framework** - Persona registry, directory API, prompt versioning, audit logs, wallet deduct for persona chat
8. **build/phase-2-personas-part2-qa** - 5 initial low-risk personas with QA/red teaming
9. **build/phase-3-image-studio** - Image generation + product photography studio
10. **build/phase-4-api-platform** - Developer API keys management
11. **etc.** as per roadmap phases 5-8

Each PR must be Draft, DO NOT MERGE until owner security review for financial/auth, with tests, no secrets, no real provider calls unless sandbox.

---

## 14. Risks Requiring Owner Approval (Summary)

- **Financial:** Wallet reconciliation job, mock provider in prod risk, static exchange rate loss, admin grant without threshold approval
- **Privacy:** IP/UA hashing without salt reversible, no encryption at rest for future Telegram tokens, no RLS, no GDPR deletion workflow, no PII log check
- **Architecture:** In-memory rate limiting not distributed, SELECT FOR UPDATE ignored in SQLite, String UUID less efficient, JSONB variant, HttpOnly Secure False in dev, legacy backend files dead code, frontend obsolete
- **Safety:** No image NSFW filter, video consent gate, Telegram anti-spam enforcement, persona high-risk not reviewed, no medical/legal authority claims currently but future risk
- **Compliance:** No Terms/Privacy/Refund/Safety pages implementation, no GDPR deletion, supplier scout vs procurement agent confusion

---

## 15. Confirmations

- **Repository audit is complete and honest:** YES - Inspected README, all files under docs/vision (3), docs/roadmap (11 including completion report and changelog), docs/architecture (3), docs/personas (6), docs/agents/runtime (5), docs/growth (8), docs/safety (1), docs/evaluation (2), docs/research (1), docs/ops (8), docs/backlog (8), docs/website (6), backend models (10), services (wallet, payment, auth, exchange_rate, providers/payment base/mock/registry), migrations (3), wallet, ledger, payment intents, authentication, tests (14 test files), frontend structure (legacy), merged PR history (PR #1 audit, #2 Phase 0 docs, #3 cleanup, #4 database, #5 auth, #6 wallet).
- **Documentation drift is documented:** YES - Listed 14 contradictions above.
- **Contradictions are listed:** YES - 14 listed.
- **Current implemented state is clearly separated from documented/planned state:** YES - Section 1 Implemented State (backend 10 models, 3 migrations, 6 auth endpoints, wallet atomic, payment intents sandbox mock, exchange rate static, credit packages config, tests 79 passed 4 skipped) vs Section 2 Documented State (Phase 0 docs say Phase 0 current, but actually Phase 1 Part 3A merged).
- **Missing capabilities listed:** YES - General chat, prompt enhancer, 5 personas (only 2 seed), image studio, video, Telegram, developer APIs (ApiKey table exists but no management API), business agents, RAG, marketplace, website Persian-first landing, growth loops, safety filters, evaluation, etc.
- **Obsolete assumptions listed:** YES - No database, no auth, wallet mock, no payment intents, legacy reseller, frontend Next.js pages.
- **Architecture risks identified:** YES - 12 risks listed.
- **Privacy risks identified:** YES - 5 risks.
- **Financial risks identified:** YES - 6 risks.
- **Recommended documentation changes listed:** YES - README status, MASTER_ROADMAP, PHASE_0_FOUNDATION, PHASE_1_CORE_MVP, PHASE_0_COMPLETION_REPORT, SYSTEM_CONTEXT, etc.
- **Recommended implementation PR sequence provided:** YES - 13 PRs in order.
- **No production code changed:** YES - This audit PR only creates docs/audits/PRODUCT_ARCHITECTURE_ALIGNMENT_AUDIT_2026-07-23.md, no backend/, frontend/, no secrets, no provider API calls.
- **No secrets committed:** YES - Scanned for ghp_, sk-, BEGIN PRIVATE KEY, no real API keys, no payment gateway, no brand hardcoding secrets.
- **No merge performed:** YES - This is Draft PR, not merged, awaiting owner and Project Manager review.

---

**End of Audit**

**Next Steps:** Owner and Project Manager review this audit, then create cleanup PR docs/cleanup-phase0-obsolete-statements to fix README and roadmap status, then proceed with Phase 1 Part 3B, 3C, etc. per recommended sequence. No production code changed in this audit PR.
