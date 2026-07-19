# Known Risks - 2026-07-19

**Date:** 2026-07-19  
**Repository:** ai-subscription-platform  
**Branch:** audit/repo-rescue-2026-07-19  
**Main SHA:** 6a6a454

This document lists business, legal, technical, and security risks that are **known but not yet mitigated**. Do not deploy until P0/P1 mitigated.

## Business & Legal Risks

### BR-001 Shared Consumer Accounts / Credential Sharing

**Description:** README and code mention "اکانت‌های اشتراکی" (shared accounts) where one purchased account is split among multiple users, each getting limited credits. Example: Midjourney Basic shared among many.

**Risk:** Violates Terms of Service of virtually all providers (OpenAI, Midjourney, Netflix, Spotify). Could lead to:
- Account bans, provider legal action
- Loss of customer funds if provider detects and bans
- Reputational damage
- Potential fraud if reselling API keys without authorization

**Evidence:** `backend/app/models` references SharedAccount, UserSharedAccount; `data/products_data.py` includes type shared; README line "اکانت‌های اشتراکی - گزینه‌های ارزان برای کاربران معمولی"

**Recommendation:** Feature flag `ENABLE_SHARED_ACCOUNTS=False` for MVP, disable endpoints `/api/shared-accounts/*`. Require written legal opinion and written authorization from each supplier before enabling. If kept, implement explicit user consent that shared use may be against provider ToS, and add monitoring for bans.

**Severity:** High business risk, launch blocker until legal clearance.

---

### BR-002 API Key Resale & ToS Violation

**Description:** Selling API credits (e.g., GPT-4 API, DALL·E 3 credits via Kie.ai) at discount suggests buying API keys/credits from marketplace and reselling.

**Risk:** Many AI providers prohibit resale. Could lead to API key revocation, billing disputes, chargebacks.

**Evidence:** `data/products_data.py` lists type `api_credit` for DALL·E 3, Stable Diffusion; README lists Kie.ai as supplier.

**Recommendation:** Flag `ENABLE_API_CREDIT_RESALE=False` until contracts reviewed. For MVP, sell only direct subscriptions where direct purchase is allowed.

---

### BR-003 Automated Purchasing from Marketplaces (GGSel, FunPay, Oyunfor)

**Description:** README claims "خرید خودکار از سایت‌های خارجی" via agents procurement_agent, using credentials GGSEL_USERNAME etc. This implies automated login and scraping of external sites.

**Risk:** 
- Scraping may violate those marketplaces' ToS
- Automated login could be considered unauthorized access (CFAA-like risk)
- Supplier could change HTML, break procurement, leaving orders stuck after payment
- Storing supplier usernames/passwords in .env is high risk; if leaked, attacker can drain supplier balance
- No evidence of supplier permission

**Evidence:** README "پشتیبانی از سایت‌های خارجی - تامین از GGSel, FunPay, Oyunfor, Kie.ai, ShareTool" + `.env.example` asks for GGSEL_USERNAME/PASSWORD + `external_apis.py` missing but referenced + `procurement_agent.py` missing but referenced + Dockerfile installs Chrome + Selenium suggests browser automation

**Recommendation:** Disable auto procurement for MVP. For MVP, manual fulfillment: admin buys manually after order paid. Feature flag `ENABLE_AUTO_PROCUREMENT=False`, return 501 for procuration endpoints. Procurement agent archived. Require written authorization from suppliers, use their official APIs (if exist) not scraping, implement per-supplier API key with limited scope, not username/password. Rotate credentials, store in vault not env file.

---

### BR-004 Supplier Scraping & IP Blocking

**Description:** If procurement uses Selenium Chrome to scrape, supplier may detect and block IP, causing DoS for all customers.

**Risk:** Operational.

**Recommendation:** Use official APIs only, implement retry with exponential backoff, circuit breaker, monitoring, and manual fallback. Until then, manual.

---

### BR-005 Bypassing Geographic Restrictions / Sanctions

**Description:** README lists products like Netflix Pakistan, Spotify Premium, Oyunfor Turkish gift cards at 90% discount. Claims ability to support Iranian users (Rial pricing, Zarinpal, USDT TRC20) for services that may be sanctioned or geo-blocked.

**Risk:** 
- Selling Turkish/Pakistani accounts to bypass geo-pricing may violate provider ToS and local laws
- US sanctions compliance - providing AI tools to sanctioned regions may be restricted; need legal review
- Payment via crypto to bypass sanctions could be seen as evasion

**Evidence:** `data/products_data.py` many products: netflix_turkey, spotify via different regions; README mentions "تامین از ... تخفیف ۶۰-۹۰٪" and "پرداخت با کریپتو - پشتیبانی از USDT..."

**Recommendation:** Seek legal counsel on OFAC/sanctions and provider geo-restriction. For MVP, avoid marketing claims about bypassing restrictions. Add disclaimer and terms that user is responsible for compliance. Feature flag regions that are clearly geo-bypass.

---

### BR-006 KYC / AML for Crypto Payments

**Description:** Accepting USDT TRC20 payments without KYC could be used for money laundering. Amounts may be large.

**Risk:** Regulatory.

**Recommendation:** Implement transaction monitoring, set max amount per order (e.g., 50M Tomans), log payment attempts, require user email/phone verified before crypto payment, integrate basic KYC for > threshold. Document AML policy. For MVP, manual review of all crypto payments mitigates but not fully.

---

### BR-007 Unsupported Product Guarantees

**Description:** README claims "گارانتی تا پایان دوره اشتراک" (guarantee until end of subscription) and "با تخفیف ۵۰٪ تا ۹۹٪". These guarantees may be unsupported if supplier bans accounts.

**Risk:** Consumer protection, chargebacks, false advertising.

**Recommendation:** Rewrite README to remove guarantees or add clear warranty terms with limitations. Add terms of service with refund policy.

---

## Technical Risks

### TR-001 Missing Core Modules -> Cannot Build

Already documented in TECHNICAL_AUDIT. Risk: no one can run project to test security fixes.

### TR-002 SQLite Concurrent Writers

Using SQLite with 3 writers (backend, celery worker, beat) -> DB locked, corrupted.

### TR-003 No Migrations

No Alembic, auto create_all -> schema drift, data loss on deploys.

### TR-004 Docker Nginx Forces HTTPS Without Certs

Local dev fails.

### TR-005 No Tests

Zero tests -> regressions.

### TR-006 Hard-coded Product IDs in Frontend

order.js hard-codes product_id=1 for all products -> wrong product delivered if order fulfilled manually.

---

## Security Risks (Summary referencing SECURITY_AUDIT)

- P0 mock payment verification -> free orders
- P0 admin endpoints public
- P0 IDOR orders
- P0 CORS wildcard + credentials
- P0 replay attacks, shared credential exposure
- P1 missing auth, insecure redis, unsafe logging, XSS via product creation

See SECURITY_AUDIT_2026-07-19.md for full list.

## Payment Risks

### PR-001 Duplicate Payment Processing & Double Spend

No uniqueness constraint on tx_hash, no idempotency. Attacker can reuse tx_hash.

### PR-002 Unvalidated Transaction Amount / Recipient

Mock verification doesn't check amount, recipient, network, contract, confirmations.

### PR-003 Invoice Expiration Not Enforced

Orders have no expires_at check; payment address could be reused months later.

### PR-004 Decimal Precision

USDT has 6 decimals (TRC20), but code uses round(amount/rate,6) without verifying on-chain decimals. May underpay by 0.000001.

### PR-005 Atomicity

Order status update and payment verification not atomic - could leave inconsistent state.

## Operational Risks

### OP-001 No Monitoring / Alerting

monitoring_agent exists but no Prometheus, no Grafana, no Sentry, no log aggregation. Failures silent.

### OP-002 No Backup

SQLite file in volume ./data without backup strategy.

### OP-003 No Rate Limiting

Spam orders, DoS.

### OP-004 Secrets Management

.env.example placeholder but no vault, no rotation, settings.SECRET_KEY default weak.

---

## Risk Matrix

| Risk ID | Category | Severity | Likelihood | Impact | Mitigation Owner | Status |
|---|---|---|---|---|---|---|
| BR-001 | Business | High | High | High | Legal + Product | Open - flag disabled |
| BR-002 | Business | High | Medium | High | Legal | Open |
| BR-003 | Business | Critical | High | High | Legal + Tech | Open - manual fulfillment only |
| BR-005 | Business | High | Medium | High | Legal | Open |
| TR-001 | Technical | Critical | High | High | Backend | In progress (PR1) |
| PAY-001 | Security | Critical | High | Critical | Backend | Open - mock disabled |
| AUTH-001 | Security | Critical | High | Critical | Backend | Open |
| IDOR-001 | Security | Critical | High | High | Backend | Open |

## Recommended Immediate Actions (Pre-MVP)

1. Disable all risky features via flags (shared accounts, auto procurement, mock payment, Zarinpal if not tested).
2. Close P0 security findings before any public deployment.
3. Obtain written authorization from suppliers or switch to manual fulfillment with official APIs only.
4. Legal review for ToS, sanctions, geo-bypass, guarantees.
5. Add secret scanning to CI, rotate any credentials ever committed.
6. Do not deploy until TECHNICAL_AUDIT build blockers resolved and tests passing.
7. Document that payment verification is manual for MVP - no auto delivery based on tx_hash alone.

## Long-term Considerations

- Consider pivoting from shared accounts to referral/group buying model that is compliant.
- Consider using official reseller programs (e.g., OpenAI doesn't have resale but some providers do).
- Implement proper KYC for crypto > threshold.
- Use PostgreSQL + Redis with password + Alembic from start.
- Add E2E monitoring, alerting, on-call.

---

**Owner acknowledgment required:** Owner must confirm they understand business risks BR-001 to BR-007 and explicitly decide to disable or seek authorization.
