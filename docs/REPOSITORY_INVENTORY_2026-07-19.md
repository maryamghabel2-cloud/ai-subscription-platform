# Repository Inventory Audit - 2026-07-19

**Date:** 2026-07-19  
**Branch:** audit/repo-rescue-2026-07-19  
**Main HEAD SHA:** 6a6a454ed4b71321fe6904046defded1eed7ad82  
**Auditor:** Principal Architect / DevSecOps  

## Executive Summary of Tree

Actual tracked file count: 52 files (see git ls-files). README claims ~30+ files that do not exist.

### Missing Critical Files (claimed in README but absent)

- `backend/requirements.txt` - **MISSING** - Build blocker
- `backend/app/config.py` - **MISSING** - Imported by 8 modules
- `backend/app/database.py` - **MISSING** - Imported by 4 modules
- `backend/app/models/models.py` - **MISSING** - File is directory placeholder only (models/__init__.py is 3 lines comment)
- `backend/app/schemas/schemas.py` - **MISSING** - Same as models
- `backend/app/agents/pricing_agent.py` - **MISSING** - Imported by main.py, product_service, order_service
- `backend/app/agents/procurement_agent.py` - **MISSING** - Imported by main.py, tasks.py, order_service
- `backend/app/agents/delivery_agent.py` - **MISSING** - Imported by main.py, order_service
- `backend/app/utils/exchange_rate.py` - **MISSING** - Imported by main.py, order_service, monitoring_agent, crypto_service
- `backend/app/utils/crypto_utils.py` - **MISSING** - Imported by main.py, order_service
- `backend/app/utils/external_apis.py` - **MISSING** - Imported by main.py, product_service
- `frontend/package.json` - **MISSING** - Build blocker
- `frontend/package-lock.json` or `yarn.lock` - **MISSING**
- `docker/docker-compose.yml` - Location mismatch: README says docker/docker-compose.yml but actual is root `docker-compose.yml`
- `backend/app/templates/*.html` - Only .gitkeep exists, but main.py expects templates like index.html, products.html, order_detail.html, payment.html, 404.html, 500.html, error.html
- `backend/static/` directory - Missing, but main.py mounts /static
- `backend/app/data/products_data.py` exists but undocumented as the actual product list; README instead references supplier APIs not present
- `tests/` directory, `pytest.ini`, `alembic/`, `migrations/` - completely absent

### Files Present but Undocumented / Unexpected

- `backend/app/data/products_data.py` - 1094 lines, 42k, static product list hard-coded, not described in tree (README lists supplier integration instead)
- `backend/app/services/crypto_service.py` - Implements mock crypto verification, not mentioned in README tree
- `backend/app/services/zarinpal_service.py` - Zarinpal payment, mentioned nowhere in architecture tree
- `backend/app/services/payment_service.py` - Exists but README says services are product_service, order_service, payment_service (this one matches, but implementation is payment coordinator that doesn't match API endpoints)
- `backend/app/agents/seo_agent.py` + `seo_agents_config.py` - Documented vaguely as AI Agents but README tree claims pricing_agent, procurement_agent, delivery_agent, monitoring_agent - only monitoring_agent exists; SEO agents are new 2 files with 25+ agent definitions that are mostly stubs returning hard-coded Persian content (1911 lines)
- `frontend/src/pages/payment.js` - Added in second commit, not in initial tree, introduces new endpoint /api/payments/create that doesn't exist backend
- `frontend/src/pages/order.js` - Hard-coded product_id=1, uses placeholder price calculation

### Detailed Tracked File Table

| Path | File Type | Purpose | Status | Imported By | Missing Dependencies | Security Relevance | Recommended Action |
|---|---|---|---|---|---|---|---|
| `README.md` | Markdown | Documentation, architecture claim | **Broken/Outdated** | - | Claims many missing files; URLs point to non-existent repo maryamghabel3-debug vs maryamghabel2-cloud | Business-risk: lists supplier scraping, shared accounts | **Rewrite** - align with actual code, remove risky claims until authorized |
| `.gitignore` | Config | Ignore patterns | Implemented | - | - | Low | Keep |
| `LICENSE` | Legal | MIT license | Implemented | - | - | Low | Keep |
| `backend/.env.example` | Env template | Config template with placeholders | Implemented but risky | - | Contains placeholder secrets; no .env in repo (good) | Medium - shows expected secrets | Keep but sanitize and add comments |
| `backend/Dockerfile` | Docker | Backend image | **Broken** | docker-compose | References `backend/requirements.txt` which missing; uses deprecated apt-key, deprecated chromedriver LATEST_RELEASE; copies .env.example incorrectly | High - build fails, installs Chrome unnecessarily | **Rewrite** - minimal python:3.11-slim, no Chrome unless proven need |
| `backend/app/__init__.py` | Python package | Package marker | Implemented | - | - | None | Keep |
| `backend/app/main.py` | Python FastAPI | Main entry point, 400+ lines | **Broken** | uvicorn | Missing 9 modules: config, database, models.models, schemas.schemas, pricing_agent, procurement_agent, delivery_agent, exchange_rate, crypto_utils, external_apis; mounts static/templates that don't exist; CORS allow * + credentials True; auto create_all | Critical - app cannot start; security CORS; unsafe DB init | **Rewrite** modularly |
| `backend/app/config.py` | **Missing** | Settings | **Missing** | main.py, monitoring_agent, seo_agent, crypto_service, zarinpal_service, tasks.py, payment_service | - | High - secrets handling | **Create** from scratch with Pydantic Settings, env validation |
| `backend/app/database.py` | **Missing** | DB session, Base, engine | **Missing** | main.py, monitoring_agent, product_service, order_service | - | High - DB init | **Create** |
| `backend/app/models/__init__.py` | Python placeholder | Claims models package | Placeholder | - | - | - | Remove or populate with real Base import |
| `backend/app/models/models.py` | **Missing** | SQLAlchemy models: Product, CompetitorPrice, ExchangeRate, User, Order, SharedAccount, UserSharedAccount, ProcurementLog | **Missing** | main.py, monitoring_agent, product_service, order_service, etc. | - | Critical - no schema | **Rewrite** - need proper models with constraints, indexes |
| `backend/app/schemas/__init__.py` | Python placeholder | Pydantic schemas package | Placeholder | - | - | - | Same |
| `backend/app/schemas/schemas.py` | **Missing** | Pydantic: ProductInDB, CompetitorPriceInDB, ExchangeRateInDB, UserInDB, OrderInDB, PriceCalculationRequest/Response, HealthCheckResponse | **Missing** | main.py | - | Medium - validation missing | **Create** |
| `backend/app/services/__init__.py` | Python placeholder | Services package | Placeholder | - | - | - | Keep minimal |
| `backend/app/services/product_service.py` | Python service | Product business logic | **Broken** | tasks.py, main.py indirectly | Imports missing pricing_agent, external_api_handler, database get_db, Product model | Medium | **Repair** - needs DB + agent |
| `backend/app/services/order_service.py` | Python service | Order lifecycle | **Broken** | - | Missing agents, database, models, crypto_utils, exchange_rate_fetcher; uses blocking next(get_db()) in async context; no idempotency | High - payment handling | **Rewrite** |
| `backend/app/services/payment_service.py` | Python service | Coordinator Zarinpal + Crypto | **Placeholder/Broken** | - | Imports ZarinpalService, CryptoService, settings; but verify logic is incomplete | High - payment | **Repair** |
| `backend/app/services/crypto_service.py` | Python service | Crypto payment creation/verification | **Placeholder/Broken** | payment_service | Imports settings, get_usdt_rate (missing); verify_crypto_payment returns verified=True always (mock); generates QR via external api.qrserver.com | **P0 Critical** - mock verification | **Rewrite** with real blockchain checks or remove |
| `backend/app/services/zarinpal_service.py` | Python service | Zarinpal SOAP gateway | Implemented | payment_service | Uses requests library but not in requirements; handles errors via HTTPException | High - payment gateway | Repair - add dependency, add idempotency, sandbox flag |
| `backend/app/agents/__init__.py` | Python placeholder | Agents package | Placeholder | - | - | - | Keep |
| `backend/app/agents/monitoring_agent.py` | Python agent | Health checks, inventory | Implemented but **Broken** | tasks.py | Imports missing config, database.get_db, models, exchange_rate_fetcher; uses db.execute("SELECT 1") without text(); blocking DB in potentially async | Medium | Repair |
| `backend/app/agents/seo_agent.py` | Python agent | Coordinates 25+ SEO agents | **Placeholder** | - | Imports seo_agents_config, settings; 1911 lines of hard-coded Persian content, no real LLM/API calls; all methods return mock dictionaries | Low - dead code, bloat | **Remove/Archive** - not MVP |
| `backend/app/agents/seo_agents_config.py` | Python config | List of 25 SEO agents metadata | **Placeholder** | seo_agent | - | Low | Remove |
| `backend/app/agents/pricing_agent.py` | **Missing** | Price calculation agent claimed in README | **Missing** | main.py, product_service, order_service | - | High - pricing logic missing | **Create** |
| `backend/app/agents/procurement_agent.py` | **Missing** | Auto purchasing from GGSel etc | **Missing** | main.py, tasks.py, order_service | - | High - business risk (scraping) | **Defer/Flag** - remove until authorization |
| `backend/app/agents/delivery_agent.py` | **Missing** | Auto delivery of credentials | **Missing** | main.py, order_service | - | **P0** - plaintext credentials exposure | **Defer** |
| `backend/app/utils/__init__.py` | Python placeholder | Utils package | Placeholder | - | - | - | Keep |
| `backend/app/utils/exchange_rate.py` | **Missing** | USDT rate fetcher from Bitpin, Nobitex, Wallex | **Missing** | main.py, order_service, monitoring_agent, crypto_service, etc. | - | Medium | **Create** |
| `backend/app/utils/crypto_utils.py` | **Missing** | Crypto address generation, verification | **Missing** | main.py, order_service | - | Critical | **Create** or merge with crypto_service |
| `backend/app/utils/external_apis.py` | **Missing** | GGSel, FunPay, Oyunfor, Kie.ai APIs | **Missing** | main.py, product_service | - | High - scraping risk | **Defer** |
| `backend/app/tasks.py` | Python Celery | Background tasks | **Broken - Syntax Error** | celery beat/worker | Lines 32,43,54: `ndef` instead of `def`; imports missing config, procurement_agent, monitoring_agent, product_service | Medium - build fails | **Repair** - fix syntax, add celery config |
| `backend/app/data/products_data.py` | Python data | Hard-coded 1000+ lines product catalog | Implemented but **Duplicated** | - | - | Low | Keep for MVP but move to DB seed script |
| `backend/app/templates/.gitkeep` | Git marker | Keeps empty folder | Placeholder | - | Templates missing: main.py expects index.html, products.html, order_detail.html, payment.html, error.html, 404.html, 500.html | Low | Either create templates or remove Jinja mounting |
| `docker-compose.yml` | YAML | Local dev stack | **Broken** | - | Backend build fails due to missing requirements.txt; frontend build fails due to missing package.json; volumes override code; exposes 6379,3000,8000 unnecessarily; nginx expects certs that don't exist; certbot service unnecessary for dev | High - insecure ports, broken build | **Rewrite** |
| `docker/nginx/nginx.conf` | Nginx conf | Main nginx config | Implemented | - | - | Low | Keep |
| `docker/nginx/conf.d/default.conf` | Nginx conf | Vhost with SSL | **Broken** | - | Upstream backend:8000, frontend:3000 hard-coded; forces https redirect then listens 443 with ssl certs from /etc/letsencrypt/live/localhost that won't exist in dev; no http fallback; static location proxies to frontend incorrectly | High - blocks dev | **Rewrite** - http only for dev, optional https |
| `frontend/Dockerfile` | Docker | Frontend image | **Broken** | docker-compose | Copies frontend/package.json which missing; npm install would fail; uses node:18-alpine but no lock | High | **Rewrite** |
| `frontend/next.config.js` | JS config | Next.js config | **Broken** | - | Rewrites /api/:path* to http://localhost:8000 which works locally but in Docker frontend container localhost is self, not backend; should use env var; output standalone but no standalone config needed; CORS headers duplicate backend | Medium | **Repair** |
| `frontend/postcss.config.js` | JS config | PostCSS with tailwind, autoprefixer | Implemented | - | - | - | Keep |
| `frontend/tailwind.config.js` | JS config | Tailwind | Implemented | - | Content globs might miss some components | - | Keep |
| `frontend/public/.gitkeep` | Marker | - | Placeholder | - | - | - | Keep |
| `frontend/public/favicon.ico` | Binary | Icon | Implemented | - | - | - | Keep |
| `frontend/public/robots.txt` | Text | SEO robots | Implemented | - | - | - | Keep |
| `frontend/src/components/*` | React JS | UI components: CategoryFilter, CountdownTimer, ErrorBoundary, ExchangeRateDisplay, Layout, LoadingSpinner, PriceDisplay, ProductCard, ui/* | **Implemented** but **Unused?** | pages/index.js uses some | Depends on helpers, but helpers exist; uses axios which not declared | Low | Keep but audit for XSS |
| `frontend/src/pages/_app.js` | React | App wrapper fetches USDT rate from /api/exchange-rate | Implemented | - | Expects backend endpoint that missing half functionality | Medium | Repair |
| `frontend/src/pages/_document.js` | React | HTML lang fa dir rtl | Implemented | - | - | - | Keep |
| `frontend/src/pages/404.js`, `500.js` | React | Error pages | Implemented | - | - | - | Keep |
| `frontend/src/pages/api/hello.js` | Next.js API route | Demo hello | Placeholder | - | Dead code, not used | - | **Remove** |
| `frontend/src/pages/index.js` | React | Homepage product list, categories | **Broken/Partial** | - | Calls /api/products/prices but backend calculate_all_prices missing; formatPrice uses fa-IR; hard-coded featured products with replace logic fragile | Medium - API mismatch | **Repair** |
| `frontend/src/pages/login.js`, `register.js` | React | Auth mock | **Placeholder** | - | No real API call, just setTimeout and redirect; stores no token; backend has no /api/auth/* | High - missing auth | **Rewrite** |
| `frontend/src/pages/order.js` | React | Order creation page | **Broken** | - | Calls /api/products/calculate-price (exists but pricing_agent missing) then /api/orders/ with hard-coded product_id=1 ignoring product name; confirm-payment POST sends JSON {tx_hash} but backend expects query param ?tx_hash? Actually main.py defines `tx_hash: str` as query param not body, mismatch | **P1** - broken contract | **Repair** |
| `frontend/src/pages/order-success.js` | React | Success page | Implemented | - | Expects query params product, amount | Low | Keep |
| `frontend/src/pages/payment.js` | React | Payment page NEW | **Broken** | - | Calls /api/payments/create and /api/payments/verify which DO NOT EXIST in backend; backend has /api/orders/confirm-payment only; also mismatch in payload | **P0** - dead flow | **Rewrite** |
| `frontend/src/styles/globals.css` | CSS | Global styles | Implemented | - | - | - | Keep |
| `frontend/src/utils/api.js` | JS | Axios centralized calls | **Broken** | - | Creates axios instance, expects NEXT_PUBLIC_API_URL; methods like createOrder send JSON {product_id, quantity, payment_method} in body but backend main.py expects query params product_id, quantity, payment_method, not body; confirmPayment sends tx_hash in body vs query; getExchangeRate returns default on error (fallback) | High - contract mismatch | **Rewrite** |
| `frontend/src/utils/helpers.js` | JS | Helper utilities | Implemented | components | - | Low | Keep |

### Empty Directories

- `backend/app/templates/` - only .gitkeep, but code expects 7 HTML files
- `frontend/public/` - only favicon, robots, .gitkeep
- `backend/app/models/` - only __init__.py placeholder
- `backend/app/schemas/` - same
- `backend/app/utils/` - same
- `backend/app/services/` has files but 3 missing core services

### Duplicated / Conflicting Services

- `crypto_service.py` vs expected `utils/crypto_utils.py` - duplicate responsibility for crypto; service does mock, utils missing
- `product_service.py` vs `data/products_data.py` - one expects DB, other is static list; no sync
- `payment_service.py` vs `order_service.py` vs `zarinpal_service.py` - overlapping payment logic, no single source of truth
- SEO agents (1911 lines) vs core business agents (pricing, procurement, delivery) missing - conflicting priorities, bloat

### Dead Code

- `frontend/src/pages/api/hello.js` - Next.js example, never used
- `seo_agent.py` and `seo_agents_config.py` - 25 agents all returning hard-coded data, no integration with product flow
- `monitoring_agent.py` - health check logic exists but no endpoint exposes it beyond /api/health static; not wired to Prometheus or alerting
- `docker/nginx` + `certbot` services - certbot renewal loop irrelevant for MVP without domain

### Mismatched Backend/Frontend API Contracts (Critical)

| Frontend Call | Expected Backend | Actual Backend | Mismatch |
|---|---|---|---|
| `GET /api/exchange-rate` | Returns `{currency, rate, last_updated}` | main.py defines this, but relies on missing exchange_rate_fetcher | Backend will 500 |
| `GET /api/products/prices` | Returns `{prices: []}` | main.py calls missing pricing_agent.calculate_all_prices() | 500 |
| `POST /api/products/calculate-price` body `{product_name, supplier}` | main.py expects `PriceCalculationRequest` Pydantic but file missing, also tries pricing_agent.calculate_final_price | Will fail validation or 500 |
| `POST /api/orders/` frontend `api.js` sends body JSON, `order.js` sends `{product_id:1, quantity:1, payment_method:'crypto'}` | main.py defines `product_id: int, quantity: int = 1, payment_method: str = "crypto"` as **query parameters**, not body, and returns OrderInDB (missing) | FastAPI will 422 Unprocessable or 500 |
| `POST /api/orders/{id}/confirm-payment` frontend sends `{tx_hash: "0x..."}` in body, payment.js sends different shape | main.py defines `tx_hash: str` as query param, not body | 422 |
| `POST /api/payments/create` and `POST /api/payments/verify` | **Does not exist in backend** | payment.js calls these | 404 |
| `POST /api/auth/login`, `register`, `profile` | **Does not exist** | api.js login/register calls these | 404 |
| `GET /api/orders/{id}/status` | Exists but no auth, no user check | Frontend expects status enum | IDOR |

### Frontend Dependency Manifest Checks

- `frontend/package.json` **MISSING** - npm install cannot run. Required dependencies inferred from imports: `next`, `react`, `react-dom`, `axios`, `tailwindcss`, `postcss`, `autoprefixer`. No lock file, no version pinning -> supply chain risk.
- `backend/requirements.txt` **MISSING** - pip install cannot run. Inferred from imports: `fastapi`, `uvicorn`, `sqlalchemy`, `pydantic`, `python-multipart`, `celery`, `redis`, `requests`, `jinja2`, `python-dotenv`, `selenium` (from Dockerfile Chrome). No versions -> vulnerable.

### Summary of Recommended Actions by Category

- **Keep:** .gitignore, LICENSE, docker/nginx/nginx.conf (with mods), frontend components ui/*, helpers, globals.css, public assets, monitoring_agent (after repair), products_data as seed
- **Repair:** backend/app/main.py (split routers, fix CORS, remove template mounting or add templates), tasks.py (syntax), docker-compose.yml, nginx default.conf, next.config.js, api.js, order.js, index.js, services/* after adding missing core
- **Rewrite:** config.py, database.py, models/models.py, schemas/schemas.py, pricing_agent, crypto_service/payment logic, order state transitions, auth (missing)
- **Remove:** frontend/src/pages/api/hello.js, seo_agent.py + seo_agents_config.py (archive)
- **Defer/Flag:** procurement_agent, delivery_agent, external_apis (GGSel etc) - requires legal authorization, feature-flag OFF until approved; shared accounts feature; automated marketplace purchasing
- **Archive for later:** SEO agents config, docker certbot service, Chrome/Selenium from Dockerfile

## Verification Commands Executed

- `git ls-files | sort` -> listed 52 files
- `find . -type f | grep -v .git | sort` -> matches tracked + __pycache__
- `python -m compileall backend` -> SyntaxError in tasks.py ndef
- `cat backend/Dockerfile` -> copies missing requirements.txt
- Checked `backend/` manifest missing
- Checked `frontend/` manifest missing
