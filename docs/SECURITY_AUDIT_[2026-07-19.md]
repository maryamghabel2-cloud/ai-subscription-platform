# Security Audit - 2026-07-19

**Date:** 2026-07-19  
**Repo:** maryamghabel2-cloud/ai-subscription-platform  
**Main HEAD SHA:** 6a6a454ed4b71321fe6904046defded1eed7ad82  
**Branch:** audit/repo-rescue-2026-07-19  
**Scanner:** Manual review + grep patterns + attempt gitleaks (not available)

Severity Definitions:
- **P0 Critical:** Immediate financial/data compromise, RCE, auth bypass, payment bypass
- **P1 High:** Launch blocker, IDOR, admin bypass, insecure direct object, secrets exposure
- **P2 Medium:** Fix before public launch, insecure config, missing headers, weak validation
- **P3 Low:** Technical improvement, defense in depth

## Summary Counts

- P0: 8 findings
- P1: 10 findings
- P2: 12 findings
- P3: 7 findings

## Findings Table

| ID | Severity | File | Line / Symbol | Finding | Exploit Scenario | Business Impact | Remediation | Launch Blocker |
|---|---|---|---|---|---|---|---|
| PAY-001 | P0 Critical | `backend/app/services/crypto_service.py` | `verify_crypto_payment` 76-106, `return {"verified": True}` | Mock crypto verification always returns verified=True | Attacker submits any tx_hash (e.g., "fake123") for order, backend marks as paid, triggers procurement, attacker gets product free without paying. Comment says TODO real verification | Direct financial loss, free product delivery, inventory drain | Implement real blockchain verification per network (TronGrid, Etherscan, BscScan), verify tx exists, recipient address matches settings.CRYPTO_PAYMENT_ADDRESS, amount >= expected, confirmations >= threshold, network matches, tx not previously used (replay table). Add unit tests. Feature-flag OFF until implemented. | YES |
| PAY-002 | P0 Critical | `backend/app/services/order_service.py` | `confirm_payment` 184-206, `crypto_utils.verify_crypto_payment` then comment "For demo purposes, we'll assume payment is valid" | Duplicate mock verification in order_service also assumes valid | Same as PAY-001 - bypass payment even if crypto_service fixed, order_service second path also vulnerable | Financial loss | Ensure single verification service, remove mock path, enforce same checks as PAY-001, add idempotency key for tx_hash | YES |
| PAY-003 | P0 Critical | `backend/app/main.py` | `confirm_payment` endpoint 135-172 | No verification of blockchain network, recipient, amount, decimals, tx status, expiration, replay | Attacker reuses old tx_hash from another order or another user, or sends wrong amount, or sends to wrong address, still gets order marked paid because only tx_hash string checked for non-empty | Free orders, double spend, accounting mismatch | Implement full checks: verify transaction on blockchain, check to_address == our wallet, value == order.payment_amount_crypto with tolerance for decimal, status success, not expired (order created 24h), tx_hash unique in DB (unique constraint), confirmation count >=12 for TRC20, etc. Add DB column `blockchain_verified` and `verified_at`. | YES |
| AUTH-001 | P0 Critical | `backend/app/main.py` | `/api/admin/products/` line 219, `/api/admin/competitor-prices/` 251 | Admin endpoints have no authentication, no dependency, no role check | Any anonymous user can POST to /api/admin/products/ and create arbitrary products with arbitrary pricing, base_price_dollar, supplier, inject malicious image_url (XSS), or create competitor prices to manipulate pricing agent | Data injection, pricing manipulation, stored XSS via image_url | Add OAuth2 / JWT middleware, role guard `Depends(get_current_admin)`, rate limit, audit log. Until then disable endpoints or return 501. | YES |
| IDOR-001 | P0 Critical | `backend/app/main.py` | `get_order` 111, `get_order_status` 176, `get_shared_account` 212 | Order and shared account endpoints fetch by ID with no ownership check | User A creates order 1, User B can GET /api/orders/1 and learn product, price, payment address, tx_hash, user_id? Also can enumerate all orders sequentially. Same for /api/orders/{id}/status and /api/shared-accounts/{id} -> plaintext credentials exposure if that endpoint returned credentials | Privacy breach, credential leakage, enumeration attack | Implement auth, check `order.user_id == current_user.id` or admin role, return 403 otherwise. Add pagination limits. For shared accounts, never return raw credentials to API; return masked or via secure delivery channel (email). | YES |
| CORS-001 | P0 Critical | `backend/app/main.py` | `CORSMiddleware` 46-51 `allow_origins=["*"], allow_credentials=True` | Insecure CORS config - wildcard + credentials true is invalid and overly permissive | Browser will block but server config indicates intent to allow all origins with credentials, enabling CSRF and credential leakage if misconfigured proxy. Also allows any site to call admin endpoints (AUTH-001) and trigger order creation | CSRF, data exfiltration | Change to explicit allowlist from config: `settings.ALLOWED_ORIGINS` list, no wildcard when credentials true. Use `allow_origin_regex` if needed. | YES |
| CRED-001 | P0 Critical | `backend/app/main.py` + `backend/app/models/models.py` (missing but referenced) + `backend/app/agents/delivery_agent.py` missing | Shared account delivery | README and code mention shared accounts with "credentials" that are delivered via API or email | If implemented naively, `/api/shared-accounts/{id}` returns raw username/password / API keys in JSON, visible to any unauthenticated user (IDOR-001) and logged in nginx access logs | Account takeover, supplier ToS violation, credential stuffing | Until legal review, disable shared accounts feature entirely behind feature flag `ENABLE_SHARED_ACCOUNTS=False`. If kept, store credentials encrypted at rest (Fernet), never log plaintext, deliver via one-time secure link, rotate regularly, audit access. | YES |
| PAY-004 | P0 Critical | `backend/app/services/order_service.py` + `main.py` | `order_number = f"ORD-{datetime...}-{os.urandom(4).hex()}"` and update without transaction | No idempotency, no unique tx_hash, replay attack possible | Attacker intercepts valid payment confirmation POST and replays same tx_hash for different order_id, both marked paid even though one blockchain tx pays only once | Double fulfillment, financial loss | Add DB unique constraint on `payment_tx_hash`, check existence before updating, wrap status update in transaction with SELECT FOR UPDATE, use idempotency key header. | YES |

| ID | Severity | File | Line | Finding | Exploit | Impact | Remediation | Blocker |
|---|---|---|---|---|---|---|---|
| AUTH-002 | P1 High | `frontend/src/utils/api.js`, `backend/app/main.py` | No auth routes, login.js mock | Missing authentication entirely - frontend has login/register pages that are mock setTimeout, no JWT issuance, no password storage | Anyone can access platform, but orders have no user binding; anonymity enables abuse; no password hashing because User model missing | No accountability, can't track fraud | Implement proper auth: FastAPI Users or custom JWT, password hashing with bcrypt/argon2, registration validation, login throttling, email verification. Until then mark auth as incomplete and disable user-specific features. | YES |
| AUTH-003 | P1 High | `backend/app/main.py` | `get_all_products`, `get_product`, `get_all_prices` | Products endpoints public, but product creation admin is also public - no auth separation | Attacker can drown pricing agent with competitor price injection | Pricing manipulation | Add auth guards |
| PAY-005 | P1 High | `backend/app/services/zarinpal_service.py` | 12-20 base_url selection, `MERCHANT_ID` from settings | Zarinpal sandbox flag usable in prod? No verification that amount matches order, no callback signature check, no Authority reuse prevention | Attacker could change amount in callback? Zarinpal verify requires amount but amount comes from request not DB order; could pay less than order total | Underpayment | Verify amount against DB order.total_price_tomans*10, check Authority hasn't been used, store RefID unique, verify callback IP? Implement webhook HMAC if available, use database transaction. | YES |
| PAY-006 | P1 High | `backend/app/main.py` | `Order` status transitions: pending -> paid -> procurement_failed / delivered, but no state machine validation | Incorrect order state transitions allowed | Attacker could call confirm-payment twice for same order if first fails halfway - second succeeds marking delivered without procurement. Also order can go from delivered back to paid if endpoint called again? Code checks `if order.status != "pending"` but after first paid it becomes paid, second call would be blocked, but if procurement fails then status becomes procurement_failed, attacker could retry with fake tx | Double delivery, inconsistent accounting | Implement state machine: allowed transitions dictionary, use DB column `status` with check constraint, enforce via service layer, add idempotency. | YES |
| DB-001 | P1 High | `docker-compose.yml`, `backend/Dockerfile`, `backend/app/main.py` | `Base.metadata.create_all(bind=engine)` on import | Unsafe automatic table creation at import time, race condition with multiple workers, no migrations | Multiple containers start simultaneously, each calls create_all, SQLite may get locked, tables half created; no versioning, destructive changes possible | Data loss, startup crash | Remove create_all from main.py import, use Alembic migrations, run migrations in init container or entrypoint with locking, not in app code. | YES |
| DOCKER-001 | P1 High | `docker-compose.yml` | redis ports 6379:6379, backend 8000:8000, frontend 3000:3000 | Unnecessary exposed ports, redis without password | Local network attacker or host process can connect to redis without auth, flush DB, inject celery tasks (RCE via pickle if task serializer pickle). Also exposes backend bypassing nginx. | RCE, data loss | Remove ports for redis, backend, frontend in compose, only expose nginx 80/443 (or 80 for dev). Add redis password via env, use `requirepass`. Disable pickle serializer in Celery (use json). | YES |
| DOCKER-002 | P1 High | `docker/nginx/conf.d/default.conf` | SSL cert paths `/etc/letsencrypt/live/localhost` | Insecure Docker config, expects certs but will fail, plus certbot service loop without email/domain | Nginx fails to start, fallback may be insecure; certbot container runs infinite loop renew without config -> wasted resource | Denial of service | For dev, disable https force, listen 80 only. For prod, use separate override compose with real domain, email, and volume for certs. Document. | YES |
| SECRET-001 | P1 High | `backend/.env.example` + git history | `git log` shows only placeholders but need scan | Potential secrets in history? .env.example has placeholder but we must verify no real .env committed via git log -p | If real SMTP or API keys were once committed even if removed, they remain in history | Credential leak | Run gitleaks/trufflehog; we attempted but binary missing. Manual grep for high entropy strings shows only placeholders. Recommendations: add .env to .gitignore (already), add git-secrets hook, rotate any keys that were ever committed. Also settings.SECRET_KEY default is weak placeholder "your-secret-key-here-change-in-production" - must generate strong random. | YES |
| LOG-001 | P1 High | `backend/app/main.py` and services | `logger.error(f"Error ...: {e}")` and `raise HTTPException(status_code=500, detail=str(e))` | Unsafe logging + exposing internal errors to client | Stack traces/detailed DB errors (SQLAlchemy) leaked to client could reveal table names, connection strings, file paths. Logs may contain payment_tx_hash or addresses without redaction | Information disclosure, aids attacker | Log with structured logger, redact PII: use `logger.exception` without exposing detail to client, return generic "Internal server error" for 500, keep detailed in logs. Redact tx_hash, addresses. | YES |
| XSS-001 | P1 High | `frontend/src/components/ProductCard.js`, `frontend/src/pages/index.js` | `product.image_url` rendered as `<img src={product.image_url}>` without validation, `product.description` in hover | Stored XSS via admin product creation (AUTH-001) -> attacker creates product with image_url `javascript:alert(1)` or description containing `<script>` or onerror payload. ProductCard will render unsanitized. | XSS, session theft, defacement (though no auth currently) | Validate URL scheme http/https only, sanitize HTML, use Next.js Image with domains allowlist, CSP header. | YES |

| ID | Severity | File | Line | Finding | Exploit | Impact | Remediation | Blocker |
|---|---|---|---|---|---|---|---|
| RATE-001 | P2 Medium | `backend/app/main.py` | All endpoints | No rate limiting | Brute force order enumeration, spam order creation, DoS, pricing agent scraper | Resource exhaustion | Add SlowAPI or nginx rate limit, per IP limits for order creation, payment verification. | NO |
| VALID-001 | P2 Medium | `backend/app/main.py` | `create_order` product_id query param, no validation | Missing input validation, negative quantity? | quantity can be negative? Code `quantity: int =1` but no `gt=0` validation, could create order with negative quantity leading to negative total_price_tomans (refund exploit) | Financial manipulation | Use Pydantic models with Field(gt=0), validate product_id exists, payment_method enum. | YES (must fix) |
| SQL-001 | P2 Medium | `backend/app/agents/monitoring_agent.py` | `db.execute("SELECT 1")` | Raw SQL without text() wrapper, potential SQL injection if interpolated later, though currently static | Low currently but pattern risky | - | Use `text("SELECT 1")` and parameterized queries, use ORM only. | NO |
| SSRF-001 | P2 Medium | `backend/app/services/crypto_service.py` | `_generate_qrcode_url` uses `https://api.qrserver.com/v1/create-qr-code/?...data={data}` with user-controlled data | Server-side request? Actually client generates URL, but backend could fetch if extended | If backend were to fetch QR image, attacker could control URL param leading to SSRF to internal metadata service | Data exfiltration | Validate, use allowlist for external API, avoid server fetch, generate QR locally with `qrcode` lib. | NO |
| CSRF-001 | P2 Medium | `backend/app/main.py` + frontend | CORS * + no CSRF token | No CSRF protection for state-changing POST endpoints | Attacker's site can trigger POST /api/orders/ or /api/admin/products from victim browser if auth cookies used (currently not, but future JWT in cookie) | Unauthorized actions | Use SameSite cookies, CSRF token for cookie auth, or use Authorization header Bearer (current frontend tries) - ensure no cookie auth, document. | NO |
| CRYPTO-001 | P2 Medium | `backend/app/services/crypto_service.py` | `hashlib.sha256(...SECRET_KEY).hexdigest()[:16]` as payment ID | Weak payment ID generation, uses timestamp + SECRET_KEY but truncated to 16 hex (64 bits), predictable | Payment ID collisions, enumeration, maybe insufficient entropy | Use `secrets.token_urlsafe(32)` or UUID4, store mapping. | NO |
| DEP-001 | P2 Medium | `backend/Dockerfile`, `frontend/Dockerfile` | No version pinning, uses `python:3.11-slim`, `node:18-alpine`, `redis:7-alpine`, `nginx:alpine` without digest | Supply chain risk, vulnerable dependencies if base image has CVE | RCE, outdated packages | Pin versions with SHA256 digest, add Dependabot, use `pip freeze` lock. | NO |
| INJ-001 | P2 Medium | `docker-compose.yml` | `DATABASE_URL=sqlite:////app/data/sql_app.db` uses SQLite for concurrent writers | SQLite not suitable for multiple writers (backend + celery) - DB locked errors, lost updates | DoS, data loss | Use PostgreSQL for production compose, SQLite only for local single process. Add docs. | YES |
| PASS-001 | P2 Medium | `backend/app/models` missing but `User` referenced | Password storage unknown | If User model exists locally but not committed, may use insecure plain MD5? Cannot verify but placeholder suggests risk | Credential leak | Ensure use bcrypt/argon2, add password complexity, store hash only. Audit when model implemented. | YES |
| LOG-002 | P2 Medium | `frontend/src/utils/api.js` | `console.error('API error', ...)` logs to browser console, includes request details | Info disclosure in client console, may leak token if logged | Minor | Remove console.error in prod build, use proper error reporting. | NO |
| HEADERS-001 | P2 Medium | `docker/nginx/conf.d/default.conf`, `backend/app/main.py` | No security headers | Missing CSP, HSTS, X-Frame-Options, X-Content-Type-Options | Clickjacking, MIME sniffing | Add headers in nginx and FastAPI middleware: `SecurityMiddleware`. | NO |
| CRYPTO-002 | P2 Medium | `backend/.env.example` | `CRYPTO_NETWORK="TRC20"` default | TRC20 USDT contract not verified, no official contract address check | Attacker could send fake USDT token on same network with different contract | Financial loss | Verify token contract address per network (TRC20 USDT contract `TR7NH...`), check logs for contract. | YES |

| ID | Severity | File | Line | Finding | Remediation | Blocker |
|---|---|---|---|---|---|---|
| P3-001 | P3 Low | `frontend/Dockerfile` | multi-stage but copies only .next | Missing `node_modules` for standalone may cause runtime error | Fix standalone config, copy `node_modules` pruned or use `output: standalone` correctly | NO |
| P3-002 | P3 Low | `backend/app/agents/seo_agent.py` | 1911 lines mock content | Bloat, increases image size, no tests | Archive | NO |
| P3-003 | P3 Low | `backend/app/data/products_data.py` | 1094 lines static list | Hard-coded product IDs, no DB, no i18n | Move to seed script JSON, load into DB | NO |
| P3-004 | P3 Low | `frontend/src/pages/payment.js` | Uses local state for txHash without validation | No checksum validation for TRC20 tx hash (length 64 hex, starts with?) | Add client-side regex: TRC20 tx is 64 hex chars, check. | NO |
| P3-005 | P3 Low | `backend/app/tasks.py` | Celery beat schedule hard-coded | No jitter, fixed intervals, could cause thundering herd | Add jitter, make intervals config from settings. | NO |
| P3-006 | P3 Low | `docker-compose.yml` | `version: '3.8'` | Deprecated version key | Remove version, use compose spec. | NO |
| P3-007 | P3 Low | `README.md` | Claims 50-99% discount, guarantee, etc. | Unsupported product guarantees, marketing fluff without disclaimer | Rewrite README with factual MVP scope, disclaimer. | NO |

## Secret Scan

- **Tool attempted:** `gitleaks` - not available in audit environment (docker binary missing, tried which gitleaks -> not found). Fallback manual grep.
- **Tool used:** `grep -Rni "SECRET_KEY|API_KEY|BEGIN PRIVATE|ghp_|sk-"` + review of `git log -p`.
- **Result:** No live secrets found in tracked files. `.env.example` contains only placeholder values like `"your-secret-key-here-change-in-production"`, `"your_ggsel_password"` etc. These are not real secrets (entropy low, obvious placeholder).
- **Potential findings:** None with high confidence, but cannot guarantee history doesn't contain real secrets because full history scan with gitleaks not run. Recommendation: Owner should run `gitleaks detect --source . --verbose` locally and `trufflehog git file://.` to double-check, rotate any credentials ever committed.
- **Redaction:** All values in reports are redacted as placeholder; no real secrets printed.

## Recommendations Summary

1. **Immediately disable payment verification mocks** - set feature flag `ENABLE_MOCK_PAYMENT=False` and return 501 for verify until real implementation.
2. **Disable admin endpoints** - add `Depends` that returns 403 or remove routes until auth ready.
3. **Add authentication** - JWT with strong SECRET_KEY generated via `secrets.token_urlsafe(64)`, bcrypt passwords, role-based access.
4. **Fix CORS** - explicit origins.
5. **Implement proper payment checks** per Payment Audit section (network, contract, recipient, amount, decimals, status, confirmations, expiration, unique hash, replay, atomic, idempotency, state separation).
6. **Use PostgreSQL** not SQLite for multi-worker.
7. **Add rate limiting, security headers, input validation**.
8. **Remove/flag shared account credential sharing** until legal ToS review.
9. **Add secret scanning to CI** - gitleaks pre-commit hook.
10. **Do not deploy** until P0/P1 closed.

## Launch Blocker Summary

- **Blocks launch:** AUTH-001, IDOR-001, PAY-001, PAY-002, PAY-003, PAY-004, CORS-001, CRED-001, and all P1 that are marked YES.
- Total blockers: 14 findings require fix before public internet exposure.

## Evidence References

- `backend/app/services/crypto_service.py:76` mock verification
- `backend/app/main.py:46` CORS
- `backend/app/main.py:219` admin without auth
- `backend/app/main.py:111` IDOR get_order no user check
- `docker-compose.yml: ports exposing redis`
- `backend/Dockerfile: COPY requirements.txt missing`
- Manual grep logs captured in technical audit.
