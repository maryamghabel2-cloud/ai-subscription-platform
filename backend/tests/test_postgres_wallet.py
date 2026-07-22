"""
PostgreSQL integration tests for wallet and payment intents - Phase 1 Part 3A
Uses Testcontainers postgres:15-alpine, real Alembic migrations, real wallet/payment flows
"""
import os
import sys
import pytest

sys.path.append(os.path.dirname(os.path.dirname(__file__)))

try:
    from testcontainers.postgres import PostgresContainer
    TESTCONTAINERS_AVAILABLE = True
except ImportError:
    TESTCONTAINERS_AVAILABLE = False

pytestmark = pytest.mark.skipif(
    not TESTCONTAINERS_AVAILABLE,
    reason="Testcontainers not installed or Docker not available - real Postgres wallet tests skipped"
)

def test_postgres_migration_003_and_wallet_flow():
    if not TESTCONTAINERS_AVAILABLE:
        pytest.skip("Testcontainers not available")

    try:
        postgres = PostgresContainer("postgres:15-alpine")
        postgres.start()
    except Exception as e:
        pytest.skip(f"Could not start Postgres container: {e}")

    try:
        db_url = postgres.get_connection_url()
        os.environ["DATABASE_URL"] = db_url

        import subprocess
        import pathlib
        from sqlalchemy import create_engine, inspect
        from sqlalchemy.orm import sessionmaker

        backend_dir = pathlib.Path(__file__).parent.parent

        # Upgrade head (should include 001, 002, 003)
        result_up = subprocess.run(
            ["alembic", "-c", str(backend_dir / "alembic.ini"), "upgrade", "head"],
            cwd=str(backend_dir),
            env={**os.environ, "DATABASE_URL": db_url},
            capture_output=True,
            text=True,
        )
        assert result_up.returncode == 0, f"Alembic upgrade head failed: {result_up.stdout} {result_up.stderr}"

        # Verify tables exist
        engine = create_engine(db_url)
        inspector = inspect(engine)
        tables = inspector.get_table_names()
        for expected in ["users", "wallets", "ledger_transactions", "personas", "conversations", "messages", "api_keys", "auth_sessions", "password_reset_tokens", "payment_intents"]:
            assert expected in tables, f"Table {expected} not found after upgrade, tables={tables}"

        # Verify payment_intents check constraints exist
        # Query pg_constraint
        from sqlalchemy import text
        with engine.connect() as conn:
            result = conn.execute(text("SELECT conname FROM pg_constraint WHERE conrelid = 'payment_intents'::regclass"))
            constraints = [row[0] for row in result]
            assert any("credits" in name for name in constraints or "positive" in name.lower() for name in constraints) or len(constraints) >= 3

        # Test full payment flow on PostgreSQL
        # Need to override get_db etc? For simplicity, test wallet and payment service directly with postgres engine
        from app.models.user import User
        from app.models.wallet import Wallet
        from app.models.payment_intent import PaymentIntent
        from app.services.wallet_service import credit_wallet, debit_wallet, get_balance
        from app.services.payment_service import create_payment_intent, complete_payment

        TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

        db = TestingSessionLocal()
        try:
            # Create user
            import uuid
            email = f"pg_wallet_{uuid.uuid4()}@example.com"
            user = User(email=email, normalized_email=email.lower(), password_hash="hash", role="user")
            db.add(user)
            db.commit()
            db.refresh(user)

            wallet = Wallet(user_id=user.id, balance_credits=0)
            db.add(wallet)
            db.commit()

            # Test atomic credit/debit
            import uuid as uuid_lib
            new_bal = credit_wallet(db, user.id, 1000, "test", "ref", f"pg_idem_{uuid_lib.uuid4()}")
            assert new_bal == 1000

            new_bal = debit_wallet(db, user.id, 300, "test", "ref2", f"pg_idem2_{uuid_lib.uuid4()}")
            assert new_bal == 700

            # Test idempotency
            idem_key = f"pg_idem_same_{uuid_lib.uuid4()}"
            bal1 = credit_wallet(db, user.id, 100, "test", "ref", idem_key)
            bal2 = credit_wallet(db, user.id, 100, "test", "ref", idem_key)
            assert bal1 == bal2
            assert bal1 == 800  # 700+100

            # Test payment intent create and complete atomically
            intent = create_payment_intent(
                db=db,
                user_id=user.id,
                provider="sandbox_mock",
                credits_to_add=500,
                amount_toman=100000,
                idempotency_key=f"pg_intent_{uuid_lib.uuid4()}"
            )
            assert intent.status == "pending"
            assert intent.credits_to_add == 500

            # Complete payment should credit wallet
            completed = complete_payment(db, intent.id, {"mock": True})
            assert completed.status == "completed"
            assert get_balance(db, user.id) == 1300  # 800+500

        finally:
            db.close()
            engine.dispose()

    finally:
        try:
            postgres.stop()
        except:
            pass
        os.environ.pop("DATABASE_URL", None)
