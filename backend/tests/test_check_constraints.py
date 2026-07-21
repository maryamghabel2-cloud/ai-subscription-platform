"""
Test check constraints against PostgreSQL (and SQLite where possible)
Required constraints:
- users.role IN ('user', 'admin')
- wallets.balance_credits >= 0
- ledger_transactions.amount <> 0
- personas.risk_level IN ('low', 'medium', 'high')
- personas.status IN ('draft', 'active', 'deprecated')
- messages.role IN ('user', 'assistant', 'system')
- api_keys.rate_limit_per_minute > 0
"""
import sys
import os
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
from app.models.conversation import Conversation
from app.models.message import Message
from app.models.api_key import ApiKey

def get_session_factory():
    engine = create_engine("sqlite:///:memory:", connect_args={"check_same_thread": False})
    @event.listens_for(engine, "connect")
    def set_sqlite_pragma(dbapi_connection, connection_record):
        cursor = dbapi_connection.cursor()
        cursor.execute("PRAGMA foreign_keys=ON")
        cursor.close()
    Base.metadata.create_all(bind=engine)
    return sessionmaker(bind=engine), engine

def test_users_role_check():
    SessionFactory, engine = get_session_factory()
    db = SessionFactory()
    try:
        # Valid roles
        u1 = User(email="role_user@example.com", normalized_email="role_user@example.com", password_hash="hash", role="user")
        db.add(u1)
        db.commit()

        u2 = User(email="role_admin@example.com", normalized_email="role_admin@example.com", password_hash="hash", role="admin")
        db.add(u2)
        db.commit()

        # Invalid role should fail
        u_invalid = User(email="role_invalid@example.com", normalized_email="role_invalid@example.com", password_hash="hash", role="superuser")
        db.add(u_invalid)
        with pytest.raises(IntegrityError):
            db.commit()
        db.rollback()
    finally:
        db.close()

def test_wallets_balance_non_negative():
    SessionFactory, engine = get_session_factory()
    db = SessionFactory()
    try:
        user = User(email="balance_test@example.com", normalized_email="balance_test@example.com", password_hash="hash", role="user")
        db.add(user)
        db.commit()
        db.refresh(user)

        # Valid balance 0
        w1 = Wallet(user_id=user.id, balance_credits=0)
        db.add(w1)
        db.commit()

        # Clean for next test - need new user
        db.rollback()
        user2 = User(email="balance_test2@example.com", normalized_email="balance_test2@example.com", password_hash="hash", role="user")
        db.add(user2)
        db.commit()
        db.refresh(user2)

        # Invalid negative balance should fail
        w_invalid = Wallet(user_id=user2.id, balance_credits=-10)
        db.add(w_invalid)
        with pytest.raises(IntegrityError):
            db.commit()
        db.rollback()
    finally:
        db.close()

def test_ledger_amount_nonzero():
    SessionFactory, engine = get_session_factory()
    db = SessionFactory()
    try:
        user = User(email="ledger_amount@example.com", normalized_email="ledger_amount@example.com", password_hash="hash", role="user")
        db.add(user)
        db.commit()
        db.refresh(user)

        wallet = Wallet(user_id=user.id, balance_credits=100)
        db.add(wallet)
        db.commit()
        db.refresh(wallet)

        # Valid non-zero
        tx1 = LedgerTransaction(wallet_id=wallet.id, amount=10, type="purchase", idempotency_key="key-nonzero-1")
        db.add(tx1)
        db.commit()

        tx2 = LedgerTransaction(wallet_id=wallet.id, amount=-5, type="spend_chat", idempotency_key="key-nonzero-2")
        db.add(tx2)
        db.commit()

        # Invalid zero amount should fail
        tx_invalid = LedgerTransaction(wallet_id=wallet.id, amount=0, type="purchase", idempotency_key="key-nonzero-3")
        db.add(tx_invalid)
        with pytest.raises(IntegrityError):
            db.commit()
        db.rollback()
    finally:
        db.close()

def test_persona_risk_level_check():
    SessionFactory, engine = get_session_factory()
    db = SessionFactory()
    try:
        # Valid
        p1 = Persona(slug="test-low", name_fa="تست", role_definition="test", risk_level="low", status="draft", version="v1.0.0")
        db.add(p1)
        db.commit()

        p2 = Persona(slug="test-medium", name_fa="تست", role_definition="test", risk_level="medium", status="active", version="v1.0.0")
        db.add(p2)
        db.commit()

        p3 = Persona(slug="test-high", name_fa="تست", role_definition="test", risk_level="high", status="deprecated", version="v1.0.0")
        db.add(p3)
        db.commit()

        # Invalid
        p_invalid = Persona(slug="test-invalid-risk", name_fa="تست", role_definition="test", risk_level="critical", status="draft", version="v1.0.0")
        db.add(p_invalid)
        with pytest.raises(IntegrityError):
            db.commit()
        db.rollback()
    finally:
        db.close()

def test_persona_status_check():
    SessionFactory, engine = get_session_factory()
    db = SessionFactory()
    try:
        p_invalid = Persona(slug="test-invalid-status", name_fa="تست", role_definition="test", risk_level="low", status="archived", version="v1.0.0")
        db.add(p_invalid)
        with pytest.raises(IntegrityError):
            db.commit()
        db.rollback()
    finally:
        db.close()

def test_messages_role_check():
    SessionFactory, engine = get_session_factory()
    db = SessionFactory()
    try:
        user = User(email="msg_role@example.com", normalized_email="msg_role@example.com", password_hash="hash", role="user")
        db.add(user)
        db.commit()
        db.refresh(user)

        conv = Conversation(user_id=user.id, persona_id=None)
        db.add(conv)
        db.commit()
        db.refresh(conv)

        # Valid roles
        for role in ["user", "assistant", "system"]:
            msg = Message(conversation_id=conv.id, role=role, content="test")
            db.add(msg)
            db.commit()

        # Invalid role
        msg_invalid = Message(conversation_id=conv.id, role="invalid_role", content="test")
        db.add(msg_invalid)
        with pytest.raises(IntegrityError):
            db.commit()
        db.rollback()
    finally:
        db.close()

def test_api_keys_rate_limit_positive():
    SessionFactory, engine = get_session_factory()
    db = SessionFactory()
    try:
        user = User(email="rate_limit@example.com", normalized_email="rate_limit@example.com", password_hash="hash", role="user")
        db.add(user)
        db.commit()
        db.refresh(user)

        # Valid
        key1 = ApiKey(user_id=user.id, key_prefix="sk_test_123", key_hash="hash1", rate_limit_per_minute=60)
        db.add(key1)
        db.commit()

        # Invalid 0
        key_invalid = ApiKey(user_id=user.id, key_prefix="sk_test_456", key_hash="hash2", rate_limit_per_minute=0)
        db.add(key_invalid)
        with pytest.raises(IntegrityError):
            db.commit()
        db.rollback()

        # Invalid negative
        key_invalid2 = ApiKey(user_id=user.id, key_prefix="sk_test_789", key_hash="hash3", rate_limit_per_minute=-10)
        db.add(key_invalid2)
        with pytest.raises(IntegrityError):
            db.commit()
        db.rollback()
    finally:
        db.close()
