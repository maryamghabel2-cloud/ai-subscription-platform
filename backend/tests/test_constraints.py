"""
Test unique constraints and FK cascade decision documented
"""
import sys
import os
import uuid
import pytest

sys.path.append(os.path.dirname(os.path.dirname(__file__)))

from sqlalchemy import create_engine, event
from sqlalchemy.orm import sessionmaker
from sqlalchemy.exc import IntegrityError

from app.database import Base
from app.models.user import User
from app.models.wallet import Wallet
from app.models.ledger import LedgerTransaction
from app.models.persona import Persona

def get_session_factory():
    engine = create_engine("sqlite:///:memory:", connect_args={"check_same_thread": False})
    @event.listens_for(engine, "connect")
    def set_sqlite_pragma(dbapi_connection, connection_record):
        cursor = dbapi_connection.cursor()
        cursor.execute("PRAGMA foreign_keys=ON")
        cursor.close()
    Base.metadata.create_all(bind=engine)
    SessionFactory = sessionmaker(bind=engine)
    return SessionFactory, engine

def test_unique_email():
    SessionFactory, engine = get_session_factory()
    db = SessionFactory()
    try:
        user1 = User(email="test@example.com", normalized_email="test@example.com", password_hash="hash1", role="user")
        db.add(user1)
        db.commit()

        user2 = User(email="test@example.com", normalized_email="test@example.com", password_hash="hash2", role="user")
        db.add(user2)
        with pytest.raises(IntegrityError):
            db.commit()
        db.rollback()
    finally:
        db.close()

def test_idempotency_key_unique():
    """
    Duplicate insert with same idempotency_key must raise IntegrityError
    This is core for financial safety - prevents double processing on retries
    Test uses pytest.raises per quality requirement
    """
    SessionFactory, engine = get_session_factory()
    db = SessionFactory()
    try:
        email = f"user_{uuid.uuid4()}@example.com"
        user = User(email=email, normalized_email=email.lower(), password_hash="hash", role="user")
        db.add(user)
        db.commit()
        db.refresh(user)

        wallet = Wallet(user_id=user.id, balance_credits=100)
        db.add(wallet)
        db.commit()
        db.refresh(wallet)

        key = f"test-key-{uuid.uuid4()}"
        tx1 = LedgerTransaction(wallet_id=wallet.id, amount=10, type="purchase", idempotency_key=key)
        db.add(tx1)
        db.commit()

        tx2 = LedgerTransaction(wallet_id=wallet.id, amount=10, type="purchase", idempotency_key=key)
        db.add(tx2)
        with pytest.raises(IntegrityError):
            db.commit()
        db.rollback()
    finally:
        db.close()

def test_fk_restrict_documented():
    """
    FK cascade decision documented: default RESTRICT for financial safety.
    """
    SessionFactory, engine = get_session_factory()
    db = SessionFactory()
    try:
        email = f"fk_test_{uuid.uuid4()}@example.com"
        user = User(email=email, normalized_email=email.lower(), password_hash="hash", role="user")
        db.add(user)
        db.commit()
        db.refresh(user)

        wallet = Wallet(user_id=user.id, balance_credits=0)
        db.add(wallet)
        db.commit()

        # Try to delete user while wallet exists - should fail with RESTRICT
        db.delete(user)
        with pytest.raises(IntegrityError):
            db.commit()
        db.rollback()
    finally:
        db.close()

def test_wallet_unique_user_id():
    """One wallet per user - unique constraint on user_id, exactly one uniqueness mechanism"""
    SessionFactory, engine = get_session_factory()
    db = SessionFactory()
    try:
        email = f"wallet_unique_{uuid.uuid4()}@example.com"
        user = User(email=email, normalized_email=email.lower(), password_hash="hash", role="user")
        db.add(user)
        db.commit()
        db.refresh(user)

        w1 = Wallet(user_id=user.id, balance_credits=0)
        db.add(w1)
        db.commit()

        w2 = Wallet(user_id=user.id, balance_credits=10)
        db.add(w2)
        with pytest.raises(IntegrityError):
            db.commit()
        db.rollback()
    finally:
        db.close()
