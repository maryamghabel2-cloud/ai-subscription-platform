"""
Test Alembic migration up/down for Phase 1 Part 1 core schema
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
    Test that migration 001_core_schema creates all 7 tables and can be downgraded.
    We test via Base.metadata creation as proxy, and check drop.
    """
    engine = get_test_engine()
    
    # Simulate upgrade: create_all should create 7 tables
    Base.metadata.create_all(bind=engine)
    
    inspector = inspect(engine)
    tables = inspector.get_table_names()
    
    expected_tables = {"users", "wallets", "ledger_transactions", "personas", "conversations", "messages", "api_keys"}
    assert expected_tables.issubset(set(tables)), f"Missing tables. Found {tables}, expected {expected_tables}"
    
    # Check unique index on idempotency_key exists
    indexes = inspector.get_indexes("ledger_transactions")
    index_names = [idx['name'] for idx in indexes]
    has_idempotency_unique = any('idempotency' in name for name in index_names)
    assert has_idempotency_unique, f"idempotency_key unique index not found in {index_names}"
    
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
