# WALLET AND PAYMENTS - Phase 1 Part 3A

**Date:** 2026-07-20
**Branch:** build/phase-1-part3a-wallet
**Status:** Sandbox mock provider only, no real payment gateway, no real blockchain

## Wallet Architecture (Append-Only Ledger)

**Design:** Append-only signed credit ledger (not double-entry). True double-entry would have separate debit/credit accounts with equal opposite entries; here single signed amount + cached wallet balance.

**Tables:**
- wallets: id PK, user_id FK unique (1 per user) RESTRICT, balance_credits int check >=0, timestamps
- ledger_transactions: id PK, wallet_id FK RESTRICT, amount signed int check <>0 (positive credit, negative debit), type (purchase, spend_chat, spend_image, refund, bonus, grant, etc.), reference_id nullable not FK (decoupled), idempotency_key unique (exactly one named UNIQUE constraint uq_ledger_idempotency_key), created_at

**Why append-only:**
- Financial safety: never UPDATE or DELETE ledger rows, history immutable
- Auditability: every credit movement has immutable record with idempotency_key
- Idempotency: duplicate requests with same key raise IntegrityError, no double processing on retries
- No UPDATE/DELETE in app logic, only INSERT, enforced by code convention, DB permissions deferred to Part 3 wallet/ledger PR
- reference_id not FK to keep decoupled
- Amount signed: positive credit, negative debit, never zero per check constraint

**Why balance can never be negative:**
- DB check constraint balance_credits >=0 on wallets table
- Code level check in debit_wallet: SELECT FOR UPDATE on wallet row, check balance >= amount, if insufficient raise InsufficientCreditsError, do NOT insert ledger, do NOT update balance
- SELECT FOR UPDATE locks wallet row until transaction commit, prevents race condition where two concurrent debits could both see balance 100 and both debit 80, leading to -60
- All amounts integers (no floating point for money) to avoid precision errors

**Why SELECT FOR UPDATE is used:**
- Prevents race condition in concurrent debit scenario
- Example: 10 simultaneous debit requests against one wallet with balance 100, each trying to debit 15. Without FOR UPDATE, all 10 could read balance 100 at same time, all think sufficient, all debit, leading to negative balance or overspend. With FOR UPDATE, first transaction locks wallet row, others wait, then re-read balance after lock, only 6 succeed (6*15=90, remaining 10), 4 fail with insufficient credits, balance never negative.
- Tested in test_wallet.py test_concurrent_debits with threading

**Atomic credit/debit:**
- BEGIN transaction
- Check idempotency BEFORE starting transaction (if key exists return same result)
- SELECT wallet FOR UPDATE (for debit, to lock)
- INSERT ledger
- UPDATE wallet balance
- COMMIT

**Idempotency mechanism:**
- idempotency_key unique indexed, exactly one named UNIQUE constraint
- Check BEFORE transaction: if exists, return existing result (balance)
- If race condition inserts same key concurrently, IntegrityError caught, then check again and return existing
- Same key returns same result without double processing

## Payment Flow Diagrams

### Toman (ZarinPal) Flow (Sandbox Mock in Part 3A, Real in 3B)
```
User -> POST /payments/create {provider: zarinpal, amount_toman: 299000, credits_to_add: 1000, idempotency_key}
Backend: validate at least one amount set, credits_to_add>0, snapshot exchange rate (190600), set expires_at now+30min, status pending, save payment_intents, initiate_payment via provider (mock returns fake authority)
Return: {id, provider, status pending, amount_toman, credits_to_add, provider_reference (authority), expires_at}

User -> Pays via ZarinPal (sandbox mock: no real payment)

Backend (sandbox simulate): POST /payments/{id}/simulate-complete (only when PAYMENT_PROVIDER=sandbox_mock)
- Checks is_sandbox_provider, CSRF, user owns payment
- Verifies idempotency (cannot complete twice)
- Atomically: update payment_intents status completed, verified_at now, verification_data, credit wallet with credits_to_add via credit_wallet with idempotency key payment_{id}_credit_{credits}
- Returns completed

Wallet balance increased, ledger entry type=payment, reference_id=payment_intent.id
```

### Crypto (USDT TRC20) Flow (Sandbox Mock in Part 3A, Real in 3C)
```
User -> POST /payments/create {provider: crypto_trc20, amount_crypto: "10.500000", crypto_currency: USDT, crypto_network: TRC20, credits_to_add: 1000, idempotency_key}
Backend: same as above, snapshot exchange rate, set wallet_address mock (mock_wallet_address_{provider}_{user_id}), status pending
Return: {id, provider, amount_crypto, crypto_currency, crypto_network, wallet_address (receive address), credits_to_add, expires_at}

User -> Sends crypto to wallet_address (sandbox mock: no real blockchain)

Backend simulate-complete same as above: credits wallet
```

## PaymentIntent Lifecycle
```
pending -> processing (optional intermediate, not used in sandbox)
pending -> completed (via complete_payment, only if not expired and status pending/processing, atomically credits wallet)
pending -> failed (via fail_payment, only if pending/processing, sets failure_reason)
pending -> expired (via expire_stale_payments cron, finds pending where expires_at < now, sets status expired)
processing -> completed/failed/expired similar
completed -> terminal, cannot complete again (idempotent check, raises PaymentAlreadyCompletedError)
failed -> terminal, cannot complete
expired -> terminal, cannot complete
refunded -> terminal (future, not implemented in 3A, would be refund_wallet)
```

## Idempotency Mechanism

- **PaymentIntent idempotency_key:** Unique constraint uq_payment_intents_idempotency_key, exactly one mechanism. If client retries create with same key, returns existing intent (no duplicate payment intents).
- **Ledger idempotency_key:** Unique constraint uq_ledger_idempotency_key, exactly one mechanism. If credit_wallet called twice with same key (e.g., retry after network failure), second call returns same balance without double credit, ledger has only one row with that key.
- **Payment completion idempotency:** complete_payment checks if payment_intent already completed, if so raises or returns already completed without double crediting wallet. Uses wallet_idempotency_key = f"payment_{id}_credit_{credits}" for ledger idempotency.
- **Why needed:** Network retries, client double-click, concurrent requests, blockchain reorgs - must not double credit.

## Exchange Rate Snapshot Logic

- For MVP: configurable static rate from settings EXCHANGE_RATE_TOMAN_PER_USD default 190600 Toman per USD
- At payment intent creation time, snapshot current rate via get_exchange_rate_snapshot() -> exchange_rate_snapshot field stored in payment_intents
- Later (not in this PR): real-time rate from Bonbast/Arzbin API, rate caching
- Why snapshot: If rate changes between creation and verification, we need to know rate at creation for audit and for converting Toman to USD to credits.

## Credit Packages and Pricing

Defined in config.CREDIT_PACKAGES (not hardcoded in code logic per spec):

```python
CREDIT_PACKAGES = [
    {"id": "basic_monthly", "name_fa": "پایه ماهانه", "credits": 1000, "price_toman": 299000, "price_usd_cents": 200},
    {"id": "pro_monthly", "name_fa": "حرفه‌ای ماهانه", "credits": 5000, "price_toman": 699000, "price_usd_cents": 500},
    {"id": "creator_monthly", "name_fa": "سازنده ماهانه", "credits": 15000, "price_toman": 1990000, "price_usd_cents": 1200},
]
```

- GET /payments/packages returns this list plus exchange_rate_toman_per_usd - public endpoint, no auth required
- Package prices match config - tested
- Credits to add comes from package or custom amount, validated >0

## Sandbox vs Production Providers

- **Provider abstraction:** backend/app/providers/payment/base.py abstract class with initiate_payment, verify_payment, get_payment_status. MockPaymentProvider in mock.py clearly marked "SANDBOX ONLY — NOT FOR PRODUCTION. Real verification required." - initiate returns fake authority/tx_hash, verify always True, get_status returns completed.
- **Registry:** registry.py selects provider via env var PAYMENT_PROVIDER, default sandbox_mock, future zarinpal (Part 3B), crypto_trc20 (Part 3C), crypto_ton. is_sandbox_provider() checks if provider == sandbox_mock.
- **Sandbox simulate-complete:** POST /payments/{id}/simulate-complete only works when PAYMENT_PROVIDER=sandbox_mock, otherwise 403 Forbidden - must be disabled in production. Simulates successful verification and credits wallet. This is the ONLY way to add credits from payment in sandbox.
- **Security:** No public confirm endpoint that can be called without auth+CSRF and ownership check, no real blockchain API calls in this PR, no real ZarinPal API calls, mock clearly marked.

## Security: No Public Confirm Endpoint

- complete_payment is internal service function, not directly exposed via public API without auth. The only public way to complete in sandbox is simulate-complete which requires authentication (get_current_user), CSRF, and checks is_sandbox_provider and that user owns payment intent.
- In production, real verification would be via ZarinPal callback with authority verification or blockchain confirmation with tx_hash validation, not via public simulate endpoint.
- Users can only see their own transactions and payments - get_transaction_history and get_user_payments filter by user_id, tested.

## Deferred: Real ZarinPal (Part 3B), Real Crypto (Part 3C)

- Part 3A: Only database schema, business logic atomic idempotent, mock/sandbox providers
- Part 3B: Real ZarinPal API integration - initiate_payment calls ZarinPal API with merchant ID, verify_payment calls ZarinPal verification API with authority and amount, get_payment_status
- Part 3C: Real crypto verification - blockchain API calls (TronGrid for TRC20, Ton API), verify recipient address matches wallet_address, exact amount matches amount_crypto with decimal precision preserved as string, confirmation count, transaction existence, etc.
- Part 3A: Exchange rate static, Part 3B/C: real-time rate from Bonbast/Arzbin with caching
- Part 3A: No real money processing, only mock credits

## Wallet Balance Never Negative - Enforcement

- DB level: CheckConstraint balance_credits >=0 on wallets table
- Code level: debit_wallet checks balance >= amount after SELECT FOR UPDATE, raises InsufficientCreditsError if insufficient, does NOT insert ledger, does NOT update balance
- Concurrency: SELECT FOR UPDATE locks wallet row, prevents race
- Tested: debit with insufficient raises error, balance never negative even under 10 concurrent debits, total debited equals expected (e.g., 100 initial, 10 threads debit 15 each, only 6 succeed = 90 debited, final balance 10, never negative)

## SELECT FOR UPDATE Rationale

See wallet architecture section above - prevents race condition, ensures atomic read-modify-write for balance.

## Credit Packages and Pricing - No Hardcoding

- Packages defined in config.CREDIT_PACKAGES, not hardcoded in business logic
- GET /payments/packages returns config packages
- Tests verify package prices match config

## Tests Summary

- Wallet operations: credit increases, debit decreases, insufficient raises, balance never negative, idempotency same key no double, concurrent debits 10 threads balance never negative, ledger append-only no rows deleted, users only see own transactions - all in test_wallet.py
- Payment intents: create sets correct fields, complete credits wallet atomically, idempotent complete cannot credit twice, expired cannot complete, failed cannot complete, simulate-complete only works with sandbox_mock, rejected when not sandbox, users only see own history - in test_payments.py
- Admin: admin can grant credits to any user, non-admin 403, grant creates ledger entry type=grant - in test_payments.py
- Exchange rate: service returns configured rate, payment intent stores snapshot - in test_payments.py
- Credit packages: GET /payments/packages returns correct list and prices match config - in test_payments.py
- PostgreSQL integration: Migration 003 applies on PostgreSQL 15, full payment flow on PostgreSQL - in test_postgres_wallet.py using Testcontainers

## CI

- Workflow backend-database-tests.yml updated to also run wallet/payment tests (pytest tests/ -v includes test_wallet, test_payments, test_postgres_wallet)
- Workflow backend-auth-tests.yml also runs all backend tests
- Both workflows use PostgreSQL 15 service container, Python 3.11, install requirements-dev.txt, alembic upgrade head, pytest, downgrade base, upgrade again
- Ensure PostgreSQL integration tests run in CI not skipped - Testcontainers available with Docker in ubuntu-latest
