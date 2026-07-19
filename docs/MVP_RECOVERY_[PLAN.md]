# MVP Recovery Plan - AI Subscription Platform

**Date:** 2026-07-19  
**Branch:** audit/repo-rescue-2026-07-19  
**Base SHA:** 6a6a454  
**Goal:** Make repository buildable, secure minimal viable product (product listing + order creation + manual payment verification) without risky automation.

## Principles

- One PR = one focused purpose, <20 files, includes tests, acceptance criteria, independently reviewable
- No mixing refactoring with features
- No real payment activation, no supplier connections until authorized
- Keep SQLite for local dev if single worker, but plan PostgreSQL for prod
- All P0 security fixes before any public deployment
- Feature flags: `ENABLE_SHARED_ACCOUNTS=False`, `ENABLE_AUTO_PROCUREMENT=False`, `ENABLE_MOCK_PAYMENT=False`

## File Disposition

### Keep (as-is or minor repair)

- `.gitignore` (keep)
- `LICENSE` (keep)
- `backend/.env.example` (keep but improve comments, add missing vars)
- `docker/nginx/nginx.conf` (keep)
- `frontend/public/favicon.ico`, `robots.txt`
- `frontend/src/components/ui/*` (Button, Badge, Card, Input) - keep after XSS check
- `frontend/src/utils/helpers.js` - keep
- `frontend/src/styles/globals.css` - keep
- `frontend/src/components/ErrorBoundary.js`, `LoadingSpinner.js` - keep
- `backend/app/data/products_data.py` - keep as seed source, but not as runtime DB

### Repair (fix existing file, no rewrite)

- `backend/app/tasks.py` - fix syntax `ndef` -> `def`, add missing imports guard
- `docker-compose.yml` - remove exposed ports, add healthchecks, change SQLite to Postgres option, remove certbot for dev, add env file
- `docker/nginx/conf.d/default.conf` - split into dev (http only) and prod (https)
- `frontend/next.config.js` - fix rewrites to use env `NEXT_PUBLIC_API_URL` or `http://backend:8000` inside docker, remove duplicate CORS headers
- `frontend/src/utils/api.js` - fix contract mismatch (use query vs body), add proper error handling, add type checks
- `frontend/src/pages/index.js`, `order.js`, `order-success.js` - fix API calls to match backend, remove hardcoded product_id=1
- `backend/app/agents/monitoring_agent.py` - fix imports, use `text()`, remove blocking `next(get_db())`
- `backend/Dockerfile` - remove Chrome/Selenium unless needed, fix COPY requirements.txt existence, use non-root user
- `frontend/Dockerfile` - fix COPY package.json, use npm ci with lock, non-root

### Fully Rewrite (create new file, replace logic)

- `backend/app/config.py` - NEW: Pydantic Settings v2, env validation, `SECRET_KEY` generation, `ALLOWED_ORIGINS` list, `DATABASE_URL`, `REDIS_URL`, `CRYPTO_PAYMENT_ADDRESS`, network, `ENABLE_*` flags, `ZARINPAL_MERCHANT_ID`, `ZARINPAL_SANDBOX`
- `backend/app/database.py` - NEW: SQLAlchemy engine, SessionLocal, Base, get_db dependency
- `backend/app/models/models.py` - NEW: Proper models with UUID? Keep int but add: User (id, email, hashed_password, is_active, is_admin, created_at), Product (id, name unique, description, product_type enum, category, base_price_dollar, supplier nullable, image_url, is_active, is_shared, shared_credits, created_at, updated_at), CompetitorPrice, ExchangeRate, Order (id, order_number unique, user_id FK nullable, product_id FK, quantity, unit_price_dollar, unit_price_tomans, total_price_tomans, exchange_rate, status enum with check constraint, payment_method enum, payment_address nullable, payment_amount_crypto nullable, crypto_currency, payment_tx_hash unique nullable, expires_at, created_at, updated_at, blockchain_verified bool), PaymentAttempt (id, order_id FK, tx_hash unique, amount, status, verified_at), SharedAccount (separate secure vault, encrypted credentials - for MVP disabled), UserSharedAccount, ProcurementLog
- `backend/app/schemas/schemas.py` - NEW: Pydantic v2 schemas for all above, with validators (quantity gt 0, payment_method enum)
- `backend/app/agents/pricing_agent.py` - NEW: Simple pricing logic for MVP: get base price from DB, get USDT rate from exchange_rate fetcher, apply margin from settings, competitor avg if exists, return final price. No external scraping. Unit tests.
- `backend/app/services/crypto_service.py` - REWRITE to remove mock: for MVP, only generate payment address/amount, verification returns pending and requires manual admin approval. Document that real blockchain verification is deferred to PR 8. Add `verify_crypto_payment` that checks format only and marks as pending review, does NOT auto approve.
- `backend/app/utils/exchange_rate.py` - NEW: Simple fetcher with fallback to static 190000, cache in DB ExchangeRate table, no external API scraping beyond Bitpin public endpoint with timeout, circuit breaker. Return rate.
- `backend/app/utils/crypto_utils.py` - NEW or merge into crypto_service: address generation (for MVP same static address + order id memo), amount conversion.
- `backend/app/main.py` - REWRITE split into routers: `routers/health.py`, `routers/products.py`, `routers/orders.py`, `routers/admin.py` (with auth stub returning 403). Remove Jinja templates mounting or add minimal templates. Fix CORS, add startup event for DB creation via migration, not import.
- `frontend/src/pages/payment.js` - REWRITE to use existing `/api/orders/{id}/confirm-payment` instead of non-existing `/api/payments/*`. Or keep but wire backend route /api/payments/create to create order.
- `frontend/src/pages/login.js`, `register.js` - REWRITE to call real auth endpoints (which need backend implementation).

### Remove (delete from repo)

- `frontend/src/pages/api/hello.js` - demo file, dead code
- `backend/app/agents/seo_agent.py` - 1911 lines mock SEO, not MVP, bloat
- `backend/app/agents/seo_agents_config.py` - config for above
- `docker-compose` service `certbot` - remove for MVP dev, add overlap for prod later
- Chrome / Selenium installation from backend Dockerfile - unless procurement agent needs browser automation (which is deferred, so remove)

### Archive for Later (move to `archive/` or `docs/archive/` not built)

- SEO agents -> `archive/seo_agents/` (preserve but not active)
- `backend/app/data/products_data.py` original large list -> keep but move to `backend/app/data/seed/` as JSON
- Procurement agent concept, delivery agent, external_apis -> archive with README explaining legal review needed, not in MVP

## Recovery PRs - Step by Step

Each PR description includes: Title, Purpose, Files Changed (<20), Tests Required, Acceptance Criteria

### PR 1: Fix repo scaffolding & syntax - unblock build

**Title:** `fix: scaffold core config, database, models, schemas and syntax error`

**Purpose:** Make backend importable. Create minimal missing files so app can start (even if returns empty lists).

**Files:**

- NEW `backend/app/config.py` (Pydantic Settings, no secrets)
- NEW `backend/app/database.py` (SQLAlchemy Base, engine, get_db)
- NEW `backend/app/models/models.py` (minimal Product, Order, ExchangeRate, User, CompetitorPrice with only fields needed for main.py to import - keep simple)
- NEW `backend/app/schemas/schemas.py` (minimal ProductInDB, OrderInDB, PriceCalculationRequest/Response, HealthCheckResponse with dummy fields)
- FIX `backend/app/tasks.py` - replace `ndef` with `def`
- NEW `backend/requirements.txt` - minimal pinned versions: fastapi==0.110.*, uvicorn==0.29.*, sqlalchemy==2.0.*, pydantic==2.6.*, pydantic-settings==2.1.*, python-dotenv==1.0.*, jinja2==3.1.*, celery==5.3.*, redis==5.0.*, requests==2.31.*, python-multipart==0.0.9, passlib[bcrypt]==1.7.*, python-jose[cryptography]==3.3.*, qrcode (optional)
- Fix `backend/app/models/__init__.py` to export Base
- Fix `backend/app/schemas/__init__.py` similar

**Tests:**

- `backend/tests/test_imports.py` - test that `from app.main import app` does not raise.
- `python -m compileall backend` passes.
- `pytest backend/tests/test_imports.py` passes.

**Acceptance Criteria:**

- `python -m compileall backend` exit 0
- `python -c "from app.config import settings; print(settings.PROJECT_NAME)"` prints
- `python -c "from app.models.models import Product, Order"` works
- No real secrets in files
- Branch still not deploy

**Risk:** Low - only adds missing scaffolding, no business logic change.

---

### PR 2: Fix Docker build for backend

**Title:** `fix(docker): make backend Dockerfile buildable without Chrome`

**Purpose:** Backend image builds.

**Files:**

- EDIT `backend/Dockerfile` - remove Chrome/Chromedriver, use python:3.11-slim, create non-root user appuser, COPY requirements.txt, COPY app, no .env.example, expose 8000, CMD uvicorn.
- EDIT `docker-compose.yml` - for dev, only backend, redis, frontend, nginx. Remove certbot, celery-worker, celery-beat for now (add later). Remove ports for redis. Use env file. Add healthcheck for redis and backend.
- Add `backend/.dockerignore`

**Tests:**

- `docker build -f backend/Dockerfile -t test-backend .` (if docker available) or at least `docker compose config` validates.
- If docker not available in CI, at least verify Dockerfile syntax via `hadolint` or manual review.
- Document manual build command.

**Acceptance:**

- Dockerfile no longer references missing files except requirements.txt which now exists from PR1
- Image builds locally (owner to verify)
- No apt-key usage

---

### PR 3: Frontend dependency manifest and build fix

**Title:** `fix(frontend): add package.json and fix API contract`

**Purpose:** Frontend installable and buildable.

**Files:**

- NEW `frontend/package.json` - with dependencies: next 14.x, react 18.x, react-dom 18.x, axios 1.6.*, tailwindcss 3.4.*, postcss 8.*, autoprefixer 10.*, eslint. Pin versions. Scripts: dev, build, start, lint.
- NEW `frontend/package-lock.json` (generated via npm install, commit)
- FIX `frontend/Dockerfile` - npm ci, copy package.json/lock first, build.
- FIX `frontend/next.config.js` - rewrites: destination should be `${process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000'}/api/:path*` OR for docker use `http://backend:8000`. Better: use env var `NEXT_PUBLIC_API_URL` and fallback.
- FIX `frontend/src/utils/api.js` - align createOrder and confirmPayment to backend contract: use query params or change backend to accept body (prefer body). Decision: change backend to accept Pydantic body (more proper). So for this PR, document intended contract and implement frontend to send body, backend will be fixed in PR4. So api.js should send body `{product_id, quantity, payment_method}` and tx_hash in body `{tx_hash}` but backend currently expects query, so add TODO comment and temporarily send as query param to make current backend work: `api.post('/api/orders/?product_id=${productId}&quantity=${quantity}&payment_method=${paymentMethod}')`
- FIX `frontend/src/pages/order.js` - remove hard-coded product_id=1, instead need product lookup by name -> call getAllProducts, find product with matching name, use its id. Add fallback.
- Add `frontend/.dockerignore`

**Tests:**

- `npm install` succeeds
- `npm run build` succeeds (might fail due to backend missing but at least compiles)
- Add minimal `frontend/__tests__/api.test.js` mock axios.

**Acceptance:**

- `ls frontend/package.json` exists
- `npm ci` works
- `npm run build` exit 0 or at most warns about API unreachable, not syntax error
- Dockerfile builds

---

### PR 4: Split backend routers and fix API contracts

**Title:** `refactor(api): split main.py into routers and fix order/product contracts`

**Purpose:** Make API usable, fix CORS, remove template mounting.

**Files:**

- REWRITE `backend/app/main.py` - minimal: creates app, adds CORS with allowed origins from settings, includes routers, no auto create_all (use startup event that calls create_all only if DEBUG and for dev, but log warning).
- NEW `backend/app/routers/__init__.py`
- NEW `backend/app/routers/health.py` - /api/health
- NEW `backend/app/routers/exchange.py` - /api/exchange-rate, /api/exchange-rates using exchange_rate_fetcher (new utils file from PR5? For now stub returning 190000)
- NEW `backend/app/routers/products.py` - GET /api/products, GET /api/products/{id}, GET /api/products/prices (stub for now using pricing_agent), POST /api/products/calculate-price accepting body PriceCalculationRequest
- NEW `backend/app/routers/orders.py` - POST /api/orders/ now accepts body `OrderCreate` Pydantic (product_id, quantity, payment_method), GET /api/orders/{id} with ownership check placeholder (requires auth later, for now requires x-user-id header or returns 403 if no auth but allow for MVP with warning logs), POST /api/orders/{id}/confirm-payment accepts body `{tx_hash}` not query, GET status.
- NEW `backend/app/routers/admin.py` - all admin routes return 501 Not Implemented or 403 until auth PR
- EDIT `backend/app/models/models.py` from PR1 to add proper enums, constraints
- EDIT `backend/app/schemas/schemas.py` to add OrderCreate, OrderConfirmRequest etc.
- Remove Jinja templates mounting or add minimal `backend/app/templates/index.html` placeholder saying "Backend API - see /api/docs"

**Tests:**

- `pytest backend/tests/test_api_contracts.py` - test product endpoints, order creation with body, confirm payment with body, health.
- Test CORS does not allow * with credentials.
- Test admin returns 403/501 not 200.

**Acceptance:**

- `fastapi` docs at /api/docs shows correct schemas
- Frontend `api.js` calls now match backend (both body)
- No template dir error on startup
- `python -m app.main` (via uvicorn) starts without ModuleNotFoundError

---

### PR 5: Implement pricing and exchange rate for MVP (no external scraping)

**Title:** `feat(pricing): implement minimal pricing_agent and exchange_rate fetcher with fallback`

**Purpose:** Price calculation works without external supplier APIs.

**Files:**

- NEW `backend/app/utils/exchange_rate.py` - fetcher: tries to read latest ExchangeRate from DB, if older than 5 min tries fetch from Bitpin public API (or Coingecko) with timeout 5s, on failure fallback to 190000, stores to DB. Function `get_usdt_rate()` sync for now, `get_all_rates()`.
- NEW `backend/app/agents/pricing_agent.py` - `calculate_final_price(product_name, supplier='auto')` logic: get Product from DB or from static seed if not found, base_price_dollar * usdt_rate * (1+ margin) + competitor logic? For MVP: margin from settings.DEFAULT_MARGIN (0.30), payment fee. Return dict with base_price_dollar, base_price_tomans, final_price, margin, exchange_rate. `calculate_all_prices()` iterates DB products.
- EDIT `backend/app/services/product_service.py` - integrate pricing_agent
- Add seed script `backend/scripts/seed_products.py` that loads `data/products_data.py` into DB.
- EDIT `docker-compose.yml` to add volume for data

**Tests:**

- `test_pricing_agent.py` - test calculation with known rate, test fallback.
- `test_exchange_rate.py` - test fetcher returns int, test caching.
- `test_products_api.py` - GET /api/products/prices returns list with final_price.

**Acceptance:**

- /api/products/prices returns 200 with prices, not 500
- /api/exchange-rate returns rate
- No external API keys required

---

### PR 6: Harden order service and payment flow (manual verification)

**Title:** `fix(payment): harden order state machine and disable mock verification`

**Purpose:** Close P0 payment bypass, add idempotency, state machine.

**Files:**

- REWRITE `backend/app/services/order_service.py` - add state enum, allowed transitions dict, transaction boundaries (single commit), idempotency via order_number unique & tx_hash unique, check quantity gt 0, atomic update.
- REWRITE `backend/app/services/crypto_service.py` - remove auto verified True. New logic: `create_crypto_payment` generates payment_id via secrets.token_urlsafe, returns address, amount, expires 24h. `verify_crypto_payment` now only validates format (tx_hash length 64 hex), checks if tx_hash already used (DB query PaymentAttempt), if not, creates PaymentAttempt with status pending_review, returns verified=False, message "Manual review required". No auto marking order paid. Admin must manually confirm via admin endpoint (future).
- ADD `backend/app/models/models.py` - add PaymentAttempt table, add unique constraint on payment_tx_hash, add expires_at to Order
- EDIT `backend/app/routers/orders.py` - confirm-payment now calls crypto_service.verify_format, if already used returns 409, else updates order to "payment_pending_review" not "paid", returns message.
- ADD `backend/app/services/payment_service.py` - keep but mark zarinpal as disabled for MVP (feature flag)
- EDIT `frontend/src/pages/payment.js` - update to handle pending_review state, show message "Payment submitted, awaiting manual verification"
- EDIT `frontend/src/pages/order.js` - same

**Tests:**

- `test_order_state.py` - try invalid transition pending->delivered should fail
- `test_payment_replay.py` - submit same tx_hash twice, second should 409
- `test_negative_quantity.py` - should 422
- `test_order_idor.py` - without auth should 401 or 403 after auth implemented; for now test returns 403 if header missing.

**Acceptance:**

- No auto-verified True
- Replay of tx_hash blocked by unique constraint
- Order cannot go negative quantity
- Manual review flow documented

---

### PR 7: Add authentication and authorization

**Title:** `feat(auth): implement JWT auth and admin guard`

**Purpose:** Close AUTH-001, IDOR-001.

**Files:**

- NEW `backend/app/routers/auth.py` - register, login, me endpoints, password hashing bcrypt, JWT issuance via python-jose, token expiry from settings.
- NEW `backend/app/utils/security.py` - get_password_hash, verify_password, create_access_token, get_current_user, get_current_admin
- EDIT `backend/app/models/models.py` - ensure User has hashed_password, is_admin bool
- EDIT `backend/app/routers/orders.py` - add `Depends(get_current_user)`, check ownership: order.user_id must equal current_user.id or admin
- EDIT `backend/app/routers/admin.py` - add `Depends(get_current_admin)` to all routes, previously 501 now protected
- EDIT `frontend/src/utils/api.js` - handle token storage, add Authorization header
- EDIT `frontend/src/pages/login.js`, `register.js` - call real APIs
- NEW `backend/app/schemas/schemas.py` - UserCreate, UserLogin, Token

**Tests:**

- `test_auth.py` - register, login, get me, wrong password, expired token
- `test_idor.py` - user A cannot get order of user B
- `test_admin_guard.py` - non-admin cannot POST /api/admin/products

**Acceptance:**

- Admin endpoints require admin token, otherwise 403
- Orders require auth, IDOR blocked
- Passwords stored hashed, not plaintext

---

### PR 8: Real blockchain verification (deferred, feature-flagged)

**Title:** `feat(payment): implement real TronGrid verification behind flag (deferred)`

**Purpose:** Replace manual review with real blockchain check, but only after security review.

**Files:**

- EDIT `backend/app/services/crypto_service.py` - add `check_transaction_on_blockchain` real implementation using TronGrid API with API key from settings `TRONGRID_API_KEY`, verify to address, amount, contract (USDT TRC20 contract TR7NHqjeKQxGTCi8q8ZY4pL8otSzgjLj6t), confirmations >=12, status success, amount tolerance for decimals (USDT 6 decimals). Add replay check, expiration check.
- Add `TRONGRID_API_KEY`, `USDT_CONTRACT_TRC20` to settings.
- EDIT `backend/app/config.py` to add new vars, feature flag `ENABLE_REAL_CRYPTO_VERIFY=False` by default.
- Add `PaymentAttempt` blockchain verification fields.
- ADD tests with mocked TronGrid responses, no real network calls.

**Acceptance:**

- When flag False, manual review remains.
- When flag True and valid tx, order marked paid.
- When flag True and invalid amount/recipient, 400.
- No real payment activation in CI, only mocked tests.
- Requires owner decision to enable and provide API key.

**Note:** This PR is marked Defer until owner provides written approval and test wallet.

---

### PR 9: Database hardening - migrations and Postgres

**Title:** `chore(db): add Alembic migrations and Postgres support`

**Purpose:** Fix DB-001, INJ-001.

**Files:**

- NEW `backend/alembic/` config, env.py, versions/
- NEW `backend/alembic.ini`
- EDIT `backend/app/database.py` - support both sqlite and postgres via DATABASE_URL, add connection pooling for postgres.
- EDIT `docker-compose.yml` - add postgres service, profiles, remove sqlite for prod profile, keep sqlite for dev profile with single worker.
- EDIT `backend/app/main.py` startup - run migrations? Or document manual `alembic upgrade head`.
- Add `scripts/run_migrations.sh`

**Tests:**

- `alembic upgrade head` creates tables
- `alembic downgrade -1` works
- No `create_all` in main.py anymore

**Acceptance:**

- Migrations versioned
- No race condition warning
- Prod compose uses postgres

---

### PR 10: Frontend hardening and E2E minimal

**Title:** `fix(frontend): XSS hardening, CSP, and minimal E2E`

**Purpose:** Fix XSS-001, add security headers.

**Files:**

- EDIT `frontend/src/components/ProductCard.js` - validate image_url scheme, use Next/Image with domains allowlist.
- EDIT `frontend/src/pages/index.js`, etc. - sanitize description via DOMPurify or strip tags.
- EDIT `frontend/next.config.js` - add security headers: CSP, X-Frame-Options, X-Content-Type-Options, Referrer-Policy.
- ADD `frontend/src/utils/validation.js` - client side validators
- ADD `frontend/e2e/order_flow.spec.js` Playwright minimal (mock backend)
- EDIT `docker/nginx/conf.d/default.conf` - add security headers, rate limit.

**Tests:**

- Playwright e2e passes
- XSS payload in product name does not execute

**Acceptance:**

- No javascript: URL allowed
- CSP header present
- Rate limit works

---

### PR 11: Docs and CI

**Title:** `docs: final README rewrite and CI pipeline`

**Purpose:** Align README with actual implementation, add CI.

**Files:**

- REWRITE `README.md` - remove claims about GGSel etc unless flagged, document actual MVP features (product list, order, manual crypto verification), add build instructions, env vars, docker compose usage, testing, security notes.
- NEW `.github/workflows/ci.yml` - runs compileall, pytest, npm build, gitleaks, hadolint
- NEW `.gitleaks.toml` config
- NEW `CONTRIBUTING.md`, `SECURITY.md`
- EDIT `docs/*` final updates

**Tests:**

- CI passes
- README accurate vs `git ls-files`

**Acceptance:**

- README tree matches actual tree
- CI green
- No risky business claims

---

## Timeline Estimate (not committing, just guidance)

- PR1: 1 day
- PR2-3: 1 day each
- PR4-6: 2 days each (core logic)
- PR7: 2 days
- PR8: 3 days (deferred)
- PR9: 2 days
- PR10: 2 days
- PR11: 1 day

Total ~2-3 weeks for MVP buildable, plus security review.

## Feature Flags for MVP

In `config.py`:

- `ENABLE_SHARED_ACCOUNTS=False` - disable shared account API entirely until legal review
- `ENABLE_AUTO_PROCUREMENT=False` - disable procurement_agent, delivery_agent
- `ENABLE_MOCK_PAYMENT=False` - disable mock verification
- `ENABLE_REAL_CRYPTO_VERIFY=False` - deferred
- `ENABLE_ZARINPAL=False` - defer until sandbox tested
- `ENABLE_SEO_AGENTS=False` - remove
- `ENABLE_CELERY=True` but with single worker for dev

All disabled flags should cause endpoint to return 501 Not Implemented with message "Feature disabled, requires authorization".

## Owner Decisions Required (see Questions)

- Supplier authorization for GGSel, FunPay, Oyunfor, Kie.ai, ShareTool - written permission needed
- Shared accounts model - legal ToS violation?
- Payment method - keep crypto TRC20 only for MVP or also Zarinpal?
- Database - SQLite for dev, Postgres for prod?
- Auth - email/password only or also OAuth?
- Real blockchain verification - approve TronGrid API key and test wallet?

## Success Criteria for MVP

- Backend starts: `uvicorn app.main:app` no ImportError
- Frontend builds: `npm run build` exit 0
- Docker compose (dev profile) `docker compose up --build` starts backend, frontend, redis, nginx (http only) - no crash loop
- `/api/health` returns healthy
- `/api/products` returns seeded products (at least 5)
- `/api/products/prices` returns final_price calculated
- Create order flow works via frontend -> backend creates order with status pending, generates payment address
- Confirm payment with fake tx_hash returns pending_review not paid (no free delivery)
- Admin cannot be accessed without admin token
- IDOR blocked: user cannot see other's orders
- Tests: at least 10 backend unit tests, 3 frontend tests pass
- No P0 vulnerabilities remain
- README accurate
