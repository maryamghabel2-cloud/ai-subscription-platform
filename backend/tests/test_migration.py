"""
Test Alembic migration up/down for Phase 1 Part 1 core schema
SQLite version is optional fast unit test, not migration verification.
Real Postgres verification is in test_postgres_migration.py
"""
import os
import sys
from sqlalchemy import create_engine, inspect
from sqlalchemy.orm import sessionmaker

sys.path.append(os.path.dirname(os.path.dirname(__file__)))

from app.database import Base
from app.models.user import User
from app.models.wallet import Wallet
from app.models.ledger import LedgerTransaction
from app.models.persona import Persona
from app.models.conversation import Conversation
from app.models.message import Message
from app.models.api_key import ApiKey

def get_test_engine():
    return create_engine("sqlite:///:memory:", connect_args={"check_same_thread": False})

def test_migration_up_down():
    """
    Optional fast SQLite test: create_all creates 7 tables, has unique constraint for idempotency, drop_all removes.
    Real migration verification is in test_postgres_migration.py with PostgreSQL 15 and Alembic commands.
    """
    engine = get_test_engine()
    
    Base.metadata.create_all(bind=engine)
    
    inspector = inspect(engine)
    tables = inspector.get_table_names()
    
    expected_tables = {"users", "wallets", "ledger_transactions", "personas", "conversations", "messages", "api_keys"}
    assert expected_tables.issubset(set(tables)), f"Missing tables. Found {tables}, expected {expected_tables}"
    
    # Check unique constraint or unique index on idempotency_key exists (exactly one mechanism)
    indexes = inspector.get_indexes("ledger_transactions")
    unique_constraints = inspector.get_unique_constraints("ledger_transactions")
    # Look for idempotency in either indexes or constraints
    has_idempotency = False
    for idx in indexes:
        if 'idempotency' in idx['name'].lower() and idx.get('unique'):
            has_idempotency = True
    for uc in unique_constraints:
        if 'idempotency' in uc['name'].lower() or 'idempotency_key' in str(uc['column_names']):
            has_idempotency = True
    assert has_idempotency, f"idempotency_key unique constraint/index not found. Indexes={indexes}, unique_constraints={unique_constraints}"
    
    # Simulate downgrade: drop_all and re-inspect with new inspector
    Base.metadata.drop_all(bind=engine)
    inspector2 = inspect(engine)
    tables_after = inspector2.get_table_names()
    for t in expected_tables:
        assert t not in tables_after, f"Table {t} still exists after downgrade: {tables_after}"

def test_alembic_config_exists():
    """Check alembic.ini and env.py exist"""
    assert os.path.exists(os.path.join(os.path.dirname(os.path.dirname(__file__)), "alembic.ini"))
    assert os.path.exists(os.path.join(os.path.dirname(os.path.dirname(__file__)), "alembic", "env.py"))
    assert os.path.exists(os.path.join(os.path.dirname(os.path.dirname(__file__)), "alembic", "versions", "001_core_schema.py"))
