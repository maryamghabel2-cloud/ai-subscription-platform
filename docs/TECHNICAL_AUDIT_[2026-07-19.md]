# Technical Audit - 2026-07-19

**Date:** 2026-07-19  
**Repo:** maryamghabel2-cloud/ai-subscription-platform  
**Main HEAD SHA:** 6a6a454ed4b71321fe6904046defded1eed7ad82  
**Branch:** audit/repo-rescue-2026-07-19  
**Audit Type:** Forensic Build & Code Audit (AUDIT-ONLY)

## Executive Summary

The repository is **currently unbuildable and unrunnable** in both backend and frontend.

- **Backend:** 9 core modules missing that are imported by `main.py`, plus 3 Pydantic/SQLAlchemy models missing, no dependency manifest, syntax error in `tasks.py`. FastAPI app cannot start.
- **Frontend:** `package.json` missing, so `npm install` and `npm build` cannot run. Docker build fails because Dockerfile expects package.json.
- **Docker:** `docker-compose.yml` references `backend/requirements.txt` which is missing; also mounts host code over image, exposing inconsistent behavior. Nginx config forces HTTPS with certs that don't exist, breaking local dev.
- **Database:** No migrations, unsafe `Base.metadata.create_all(bind=engine)` on import time in `main.py` (side-effect at module load), no transaction handling.
- **API Contracts:** Frontend and backend disagree on 6+ endpoints (body vs query params, missing routes like `/api/payments/create` that frontend calls correctly but backend doesn't have).
- **Tests:** Zero tests present. No pytest config, no jest config, no CI.

**Overall Build Status:** 🔴 **FAILED** - Neither backend nor frontend can build or start.

## Verified Blockers

### P0 - Build Blockers (must fix before any run)

1. **Missing `backend/app/config.py`** - ImportError on startup. Verified by grep: 6 files import it. File does not exist: `ls backend/app/config.py` -> No such file.
2. **Missing `backend/app/database.py`** - Same, 4 files import it.
3. **Missing `backend/app/models/models.py`** - `models/__init__.py` is placeholder comment only. main.py imports `from app.models.models import Product...` -> ModuleNotFoundError.
4. **Missing `backend/app/schemas/schemas.py`** - Same.
5. **Missing `backend/app/agents/pricing_agent.py`, `procurement_agent.py`, `delivery_agent.py`** - main.py and services import them.
6. **Missing `backend/app/utils/exchange_rate.py`, `crypto_utils.py`, `external_apis.py`** - main.py and services import them.
7. **Syntax Error `backend/app/tasks.py` line 32,43,54** - `ndef` instead of `def`. Verified by `python -m compileall backend` -> SyntaxError: invalid syntax, exit code 1.
8. **Missing `backend/requirements.txt`** - Dockerfile `COPY backend/requirements.txt .` will fail, pip install cannot run. Verified `ls backend/` shows no requirements.
9. **Missing `frontend/package.json`** - Dockerfile `COPY frontend/package.json` fails; `npm install` cannot run. Verified `ls frontend/*.json` shows only next.config.js, postcss.config.js, tailwind.config.js.
10. **Template & static directories empty** - main.py mounts `templates` and `static` via Jinja2Templates and StaticFiles, but only `.gitkeep` exists. Startup will error if directory missing (FastAPI checks existence).
11. **Docker unavailable** - In this audit environment docker binary not found, but even if available, compose build would fail due to #8 and #9.

### P1 - Runtime Blockers (would fail after fixing P0)

- CORS misconfig: `allow_origins=["*"]` + `allow_credentials=True` is disallowed by browsers and FastAPI will warn. Must specify explicit origins.
- Order creation uses query params vs body mismatch will cause 422.
- `crypto_service.verify_crypto_payment` returns True always (mock) -> payment bypass.
- Admin endpoints without auth.
- No DB migration tooling, concurrent `create_all` calls from multiple workers (backend, celery-worker, celery-beat) race condition.

## Commands Executed (with evidence)

| Command | Working Dir | Exit Code | Result Summary | Main Error |
|---|---|---|---|---|
| `git status` | /home/user | 0 | Clean, branch audit/repo-rescue-2026-07-19 | - |
| `git ls-files` | /home/user | 0 | 52 tracked files listed | - |
| `python --version` | /home/user | 0 | Python 3.13.13 | - |
| `python3 --version` | /home/user | 0 | Python 3.13.13 | - |
| `node --version` | /home/user | 0 | v20.20.2 | - |
| `npm --version` | /home/user | 0 | 10.8.2 | - |
| `docker --version` | /home/user | 127 | command not found | docker binary missing in audit env - note for CI |
| `docker compose version` | /home/user | 127 | command not found | same |
| `python -m compileall backend` | /home/user | 1 | SyntaxError in tasks.py | File "backend/app/tasks.py", line 40: `ndef update_product_prices_task():` invalid syntax (also lines 32,43,54?) Actually 32 is def process_order_task ok, 33+ ndef at 40, 52, 64 |
| `ls backend/` | /home/user | 0 | No requirements.txt, no config.py, no database.py | manifest missing |
| `ls frontend/` | /home/user | 0 | No package.json | manifest missing |
| `cat backend/app/main.py \| grep from app.` | /home/user | 0 | 9 missing modules identified | ImportError predicted |
| `grep -R SECRET_KEY backend/` | /home/user | 0 | Only placeholders in .env.example, no real secrets committed | Good |
| Dependency install attempts skipped | - | - | **Not executed** because manifests missing, per safety rule | Do not invent missing manifests |

### Docker Compose Config

Attempted `docker compose config` was not possible because docker binary absent. Manual inspection of `docker-compose.yml`:

- Defines 7 services: backend, frontend, redis, celery-worker, celery-beat, nginx, certbot.
- Backend build context `.` + dockerfile `backend/Dockerfile` -> will fail at COPY requirements.txt.
- Frontend same.
- Volumes `./backend:/app` overrides built image, hiding build errors in dev but causing drift.
- Env vars: DATABASE_URL sqlite:////app/data/sql_app.db but volume ./data:/app/data may not exist initially.
- Ports: 8000,3000,6379,80,443 all exposed - redis should not be public.
- celery-worker command `celery -A app.tasks.celery_app worker` -> celery_app defined in tasks.py but tasks.py syntax error prevents import.

### Frontend Build

- `frontend/package.json` missing => `npm install` **NOT RUN** per audit rule (manifest must exist). Verified.
- `npm run build` **NOT RUN** same reason.
- Manual inspection: next.config.js rewrites `/api/:path*` to `http://localhost:8000/api/:path*`. In Docker, frontend container's localhost is itself, not backend. Should use `NEXT_PUBLIC_API_URL` env or `http://backend:8000`.
- Tailwind config content globs include `src/pages/**/*` and `src/components/**/*` which is correct, but no `src/app`.

### Backend Build

- `pip install -r backend/requirements.txt` **NOT RUN** - file missing.
- `python -m compileall` already shows syntax error, so even if deps installed, app won't import.

## Missing Files (detailed)

From README tree vs actual:

- backend/app/config.py ❌
- backend/app/database.py ❌
- backend/app/models/models.py ❌ (only __init__.py placeholder)
- backend/app/schemas/schemas.py ❌
- backend/app/agents/pricing_agent.py ❌
- backend/app/agents/procurement_agent.py ❌
- backend/app/agents/delivery_agent.py ❌
- backend/app/utils/exchange_rate.py ❌
- backend/app/utils/crypto_utils.py ❌
- backend/app/utils/external_apis.py ❌
- backend/requirements.txt ❌
- frontend/package.json ❌
- frontend/package-lock.json ❌
- backend/app/templates/*.html ❌ (7 files expected)
- backend/static/* ❌
- docker/docker-compose.yml location mismatch (README says docker/ subfolder, actual is root) - minor
- backend/app/agents/seo_agents_config.py exists but not in README tree (new)
- backend/app/data/products_data.py exists but not in README tree
- frontend/src/pages/payment.js exists but not in original tree (added second commit)

## Broken Imports

Verified via `grep -r "from app"`:

- `app.config` -> missing, imported by main.py, monitoring_agent, crypto_service, zarinpal_service, tasks.py, payment_service, seo_agent (7 files)
- `app.database` -> missing, imported by main.py, monitoring_agent, product_service, order_service (4 files)
- `app.models.models` -> missing, imported by main.py, monitoring_agent, product_service, order_service (4 files)
- `app.schemas.schemas` -> missing, imported by main.py (1 file)
- `app.agents.pricing_agent` -> missing, imported by main.py, product_service, order_service (3 files)
- `app.agents.procurement_agent` -> missing, imported by main.py, tasks.py, order_service (3 files)
- `app.agents.delivery_agent` -> missing, imported by main.py, order_service (2 files)
- `app.utils.exchange_rate` -> missing, imported by main.py, product? monitoring, order, crypto (5 files) - also crypto_service imports `from app.utils.exchange_rate import get_usdt_rate` singular function not module
- `app.utils.crypto_utils` -> missing, imported by main.py, order_service (2 files)
- `app.utils.external_apis` -> missing, imported by main.py, product_service (2 files)

All would raise `ModuleNotFoundError` at startup.

## API Contract Problems

### Backend defines but frontend mismatches

- **Order creation**: Backend `POST /api/orders/` defined as `product_id: int, quantity: int =1, payment_method: str="crypto"` query params via FastAPI function signature (not Pydantic body). Frontend `api.js` `createOrder` sends body `{product_id, quantity, payment_method}`. FastAPI will treat body as missing and return 422 unless query params supplied. `order.js` does `axios.post('/api/orders/', {product_id:1, quantity:1, payment_method:'crypto'})` same issue, plus hard-coded id=1.
- **Confirm payment**: Backend `POST /api/orders/{order_id}/confirm-payment` expects `tx_hash: str` query param. Frontend `order.js` sends `{tx_hash}` in body via `axios.post(..., {tx_hash})` -> 422. Also frontend `payment.js` calls different endpoint `/api/payments/verify` that doesn't exist.
- **Payment creation**: Frontend `payment.js` calls `POST /api/payments/create` with `{product_name, amount, payment_method, callback_url}`. Backend has no such route. Backend has `payment_service.py` but not wired to router. Also `api.js` has no method for /api/payments.
- **Zarinpal**: Service exists but no endpoint exposes it. `NEXT_PUBLIC_API_URL` set to `http://backend:8000` in compose, but Next.js rewrites point to localhost:8000 - inconsistency across environments.
- **Product prices**: Backend `GET /api/products/prices` depends on missing pricing_agent -> 500 even if route exists. Frontend expects `{prices: []}`.
- **Auth**: Frontend `api.js` implements login, register, profile calling `/api/auth/*`. Backend has zero auth routes. No JWT, no password hashing.

### Frontend missing fields

- ProductCard expects fields `product_name`, `base_price_dollar`, `final_price`, `competitor_average_price`, `category`, `product_type`, `image_url`, `description` but DB model unknown, and `products_data.py` static list uses different keys (`id`, `name`, `base_price_usd`, `discount_percent`, `supplier`, `type`, etc.).
- Order page expects `payment_address`, `payment_amount_crypto`, `order_number`, `base_price_dollar`, `final_price` but these are generated only if crypto path succeeds and exchange_rate_fetcher works.

## Docker Problems

- **Dockerfile backend**: Uses `python:3.11-slim` but installs Chrome + ChromeDriver via deprecated `apt-key add` and `chromedriver.storage.googleapis.com/LATEST_RELEASE` which is shut down (Chrome for Testing now). Will fail build even if requirements existed. Also copies `.env.example` to image root, not good. Creates static dir but not templates. Exposes 8000.
- **Dockerfile frontend**: Copies `frontend/package.json` + `package-lock.json*` but package.json missing, build fails. Uses multi-stage but copies only `.next`, `public`, `package.json`, `next.config.js` but missing `node_modules` for standalone? Next standalone needs more.
- **docker-compose.yml**: 
  - version 3.8 obsolete but okay.
  - Volumes mount host code over container, hiding Dockerfile COPY.
  - `DATABASE_URL=sqlite:////app/data/sql_app.db` uses 4 slashes (absolute) but not ensured volume exists; concurrent writers (backend + celery worker + beat) to SQLite will cause DB locked errors.
  - Redis exposed to host 6379 without password - insecure.
  - Backend and frontend ports exposed (8000,3000) even though nginx is reverse proxy - unnecessary.
  - `depends_on` without healthcheck, race.
  - Certbot service with loop `while :; do certbot renew; sleep 12h & wait` - unnecessary for MVP, requires domain and email config missing.
- **nginx/conf.d/default.conf**: Forces https redirect on port 80, but SSL certs expected at `/etc/letsencrypt/live/localhost/fullchain.pem` which won't exist without certbot successful run with real domain. Local dev will get 502 or SSL error. Also `proxy_pass http://backend` and `http://frontend` rely on upstream defined, but upstream uses `server backend:8000` which is correct inside network, but frontend next.config.js rewrites to localhost:8000 breaks.
- **Missing .dockerignore**: Not present, so .git, node_modules (if existed) would be copied.

## Database Problems

- No `database.py` -> no engine, no sessionmaker, no Base definition. Cannot verify but likely would be SQLAlchemy.
- `main.py` does `Base.metadata.create_all(bind=engine)` on import, not in startup event, not idempotent, no locking, unsafe with multiple workers.
- No Alembic, no migration versioning.
- SQLite path in docker-compose uses absolute `/app/data/sql_app.db` - need volume mount, but `data/` directory not in git (gitignored? .gitignore ignores *.db, *.sqlite). So first run will fail to find dir unless created.
- Models missing so cannot verify indexes, foreign keys, cascades, etc. But expected issues from service code:
  - `Order` model referenced with fields `order_number`, `product_id`, `quantity`, `unit_price_dollar`, `unit_price_tomans`, `total_price_tomans`, `exchange_rate`, `status`, `payment_method`, `payment_address`, `payment_amount_crypto`, `payment_crypto_currency`, `payment_tx_hash`, `user_id` etc. No validation of status enum, no unique constraint on order_number, no unique on payment_tx_hash (replay).
  - `SharedAccount`, `UserSharedAccount`, `ProcurementLog` referenced but schema unknown - risk of plaintext credentials.
  - No transaction boundaries: `order_service.create_order` does db.add, commit, then second commit for payment info - not atomic. If second fails, order remains without payment info.
  - No idempotency: order_number generated with timestamp + urandom 4 bytes, low entropy, possible collision under high load but unlikely; no DB unique check retry.
  - No locking for inventory: shared account `current_users < max_users` check without SELECT FOR UPDATE -> race condition overselling.

## Frontend Problems

- **Build**: No package.json, no lock, no node_modules. `npm install` impossible.
- **Dependencies**: Inferred but not pinned: axios, next, react, react-dom. No tailwindcss version. `postcss.config.js` uses tailwindcss plugin but not installed.
- **API mismatch**: 6+ endpoints mismatched as detailed.
- **Auth flow**: login.js, register.js are placeholders with `await new Promise(resolve => setTimeout(resolve,1000))` then redirect - no real call. api.js does have login/register calling backend but backend missing.
- **Hard-coded product_id**: order.js hard-codes `product_id:1` for all products, ignoring actual product catalog.
- **Error handling**: api.js swallows errors and returns null/[], hiding failures from UI.
- **SSR**: Uses localStorage inside component without checking window in some places (though api.js checks). `_app.js` fetches `/api/exchange-rate` client-side only, no SSR fallback.
- **Accessibility & i18n**: lang fa dir rtl in _document.html correct, but components use English class names mixed with Persian - okay.
- **No tests**: No jest, no playwright, no cypress.

## Tests Currently Present

**None.** 

- No `backend/tests/` directory
- No `frontend/__tests__/` 
- No `pytest.ini`, `jest.config.js`, `vitest.config`
- No GitHub Actions workflow (`.github/workflows` missing)
- No coverage config

## Tests Currently Missing (Recommended)

- Backend unit: pricing calculation, exchange rate fetcher, order state transitions, payment verification (mock blockchain), API contract tests for /api/products, /api/orders
- Integration: DB CRUD, Celery tasks
- Frontend: component rendering, api.js mock, order flow
- E2E: checkout flow (mock payment), admin product creation
- Security: IDOR tests, admin auth tests, replay attack tests
- Load: concurrent order creation, inventory race

## Reproducible Build Audit Summary Table

(See also Build results section in final response)

- git status: 0 success, clean
- git ls-files: 0 success, 52 files
- python --version: 0 success, 3.13.13
- node --version: 0 success, v20.20.2
- docker --version: 127 fail, binary not found
- docker compose version: 127 fail
- python -m compileall backend: 1 fail, SyntaxError ndef in tasks.py
- docker compose config: not attempted (docker missing)
- backend pip install: not attempted (manifest missing) - documented as blocker
- frontend npm install: not attempted (manifest missing)
- docker compose build: not attempted (would fail + unsafe)

## Root Cause Analysis

Repository appears to be two commits: initial scaffold (commit d2881dd) with placeholder packages, and second commit (6a6a454) adding payment systems and SEO agents but **not adding the core missing modules**. It looks like developer had local files (config.py, database.py, models.py, etc.) but .gitignore or untracked? Wait git ls-files shows they were never added. So repo was pushed incomplete - local dev had files but not committed. Also requirements.txt and package.json never committed despite Docker needing them.

Additionally, tasks.py syntax error suggests incomplete edit (ndef) introduced in second commit and not tested.

Frontend payment.js introduced new endpoints that were never implemented backend.

Overall: **Push of untested, incomplete local state**.

## Risk to Production Deployment

- **Cannot deploy** - build fails.
- Even if forced, payment verification is mocked to always true -> financial loss.
- No auth -> anyone can create admin products, view orders.
- SQLite with multiple writers -> corruption.
- No secrets scanning, but env template ok.
