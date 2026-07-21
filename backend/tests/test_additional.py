"""
Additional required final tests:
- Model/migration schema consistency
- Email uniqueness/normalization
- Seed idempotency and no deletion
- Raw API keys never stored
- Unicode/Bidi scan passes
- Append-only signed credit ledger terminology
"""
import sys
import os
import pathlib
import pytest

sys.path.append(os.path.dirname(os.path.dirname(__file__)))

from sqlalchemy import create_engine, event, inspect
from sqlalchemy.orm import sessionmaker
from app.database import Base
from app.models.user import User
from app.models.api_key import ApiKey
from app.models.persona import Persona

def get_session_factory():
    engine = create_engine("sqlite:///:memory:", connect_args={"check_same_thread": False})
    @event.listens_for(engine, "connect")
    def set_sqlite_pragma(dbapi_connection, connection_record):
        cursor = dbapi_connection.cursor()
        cursor.execute("PRAGMA foreign_keys=ON")
        cursor.close()
    Base.metadata.create_all(bind=engine)
    return sessionmaker(bind=engine), engine

def test_email_normalization_strategy():
    """Email uniqueness/normalization - normalized_email field"""
    SessionFactory, engine = get_session_factory()
    db = SessionFactory()
    try:
        # Create user with email and normalized_email lower
        email = "Test@Example.COM"
        normalized = email.strip().lower()
        user = User(email=email, normalized_email=normalized, password_hash="hash", role="user")
        db.add(user)
        db.commit()

        # Try to create another user with different case but same normalized should fail due to normalized_email unique
        user2 = User(email="test@example.com", normalized_email="test@example.com", password_hash="hash", role="user")
        db.add(user2)
        with pytest.raises(Exception):  # IntegrityError expected
            db.commit()
        db.rollback()

        # Check that normalized_email field exists and is unique
        assert hasattr(User, 'normalized_email')
        table = User.__table__
        # Check unique constraint exists for normalized_email
        unique_constraints = [c for c in table.constraints if any(col.name == 'normalized_email' for col in getattr(c, 'columns', []))]
        assert len(unique_constraints) >= 1, "normalized_email should have unique constraint"
    finally:
        db.close()

def test_raw_api_keys_never_stored():
    """Raw API keys are never stored - only key_prefix and key_hash"""
    # Check that ApiKey model does not have raw key column
    table = ApiKey.__table__
    column_names = [c.name for c in table.columns]
    assert "key" not in column_names or "key_hash" in column_names, "Should not have raw key column"
    assert "key_hash" in column_names, "key_hash must exist"
    assert "key_prefix" in column_names, "key_prefix non-secret field must exist per spec section 5D"
    assert "raw_key" not in column_names and "api_key" not in column_names, "Raw API key column should not exist"
    
    # Ensure key_prefix is non-secret and key_hash is secure
    # Simulate creating key
    SessionFactory, engine = get_session_factory()
    db = SessionFactory()
    try:
        user = User(email="apikey_test@example.com", normalized_email="apikey_test@example.com", password_hash="hash", role="user")
        db.add(user)
        db.commit()
        db.refresh(user)

        # Store only prefix and hash, never raw
        prefix = "sk_live_abc"
        hashed = "hashed_secure_value_123"
        key = ApiKey(user_id=user.id, key_prefix=prefix, key_hash=hashed, scopes={}, rate_limit_per_minute=60)
        db.add(key)
        db.commit()

        # Verify raw not stored
        retrieved = db.query(ApiKey).filter_by(key_hash=hashed).first()
        assert retrieved.key_prefix == prefix
        assert retrieved.key_hash == hashed
        # Ensure no attribute for raw key
        assert not hasattr(retrieved, 'raw_key')
    finally:
        db.close()

def test_seed_idempotency_and_no_deletion():
    """Seed idempotency: running seed twice does not duplicate, does not delete existing personas"""
    from app import seed as seed_module
    engine = create_engine("sqlite:///:memory:", connect_args={"check_same_thread": False})
    Base.metadata.create_all(bind=engine)
    SessionFactory = sessionmaker(bind=engine)

    # Monkey-patch
    original_SessionLocal = seed_module.SessionLocal
    original_engine = seed_module.engine

    seed_module.SessionLocal = SessionFactory
    seed_module.engine = engine

    try:
        # First run
        personas1 = seed_module.seed_personas()
        assert len(personas1) == 2

        # Add extra persona manually to test that seed does not delete existing
        db = SessionFactory()
        extra = Persona(slug="extra-persona", name_fa="اضافی", role_definition="extra", risk_level="low", status="active", version="v1.0.0")
        db.add(extra)
        db.commit()
        count_before = db.query(Persona).count()
        assert count_before == 3
        db.close()

        # Second run - should be idempotent, not duplicate, not delete extra
        personas2 = seed_module.seed_personas()
        db = SessionFactory()
        count_after = db.query(Persona).count()
        # Should still have 3 (2 seed + 1 extra), not 2 (which would mean deletion)
        assert count_after == 3, f"Seed should not delete existing personas, expected 3, got {count_after}"

        # Check that both required slugs still exist
        slugs = [p.slug for p in db.query(Persona).all()]
        assert "general-assistant" in slugs
        assert "psychologist-draft" in slugs
        assert "extra-persona" in slugs  # Extra preserved

        db.close()
    finally:
        seed_module.SessionLocal = original_SessionLocal
        seed_module.engine = original_engine

def test_append_only_signed_credit_ledger_not_double_entry():
    """Confirm terminology: append-only signed credit ledger, not double-entry"""
    from app.models.ledger import LedgerTransaction
    # Check docstring contains correct terminology
    doc = LedgerTransaction.__doc__ or ""
    assert "append-only signed credit ledger" in doc.lower() or "append-only signed credit ledger" in doc, f"Docstring should contain 'append-only signed credit ledger', got: {doc[:200]}"
    assert "double-entry" not in doc.lower() or "not double-entry" in doc.lower() or "not a true double-entry" in doc.lower(), f"Should not call it double-entry without negation, doc: {doc[:200]}"

    # Check DATABASE_SCHEMA.md contains correct terminology
    schema_path = pathlib.Path(__file__).parent.parent / "docs" / "DATABASE_SCHEMA.md"
    if schema_path.exists():
        text = schema_path.read_text()
        assert "append-only signed credit ledger" in text.lower(), "DATABASE_SCHEMA.md should contain append-only signed credit ledger terminology"
        # Should not claim double-entry without negation
        # Allow "not double-entry" or "not a true double-entry"
        if "double-entry" in text.lower():
            # Must have negation nearby
            assert "not double-entry" in text.lower() or "not a true double-entry" in text.lower(), "Should not call it double-entry without negation"

def test_unicode_bidi_scan_passes():
    """
    Scan all changed files for hidden or bidirectional Unicode:
    U+202A through U+202E, U+2066 through U+2069, other zero-width control characters
    Persian text itself is allowed.
    """
    root = pathlib.Path(__file__).parent.parent
    # Scan all files in backend/app/models, backend/app/seed.py, etc.
    suspicious_ranges = [
        (0x202A, 0x202E),  # Bidi embeddings/overrides
        (0x2066, 0x2069),  # Isolate controls
    ]
    zero_width = [0x200B, 0x200C, 0x200D, 0xFEFF, 0x00AD]  # zero-width, soft hyphen, etc. Some are allowed in Persian? ZWNJ 0x200C is allowed in Persian, so we should allow it.

    # For this scan, we consider U+202A-202E and U+2066-2069 as always suspicious, zero-width except ZWNJ as suspicious if unexpected
    # Persian uses ZWNJ (U+200C) legitimately, so allow it
    unexpected = []

    for file_path in root.rglob("*.py"):
        if ".git" in str(file_path) or "__pycache__" in str(file_path):
            continue
        # Only scan changed files per task: backend/app/models/*, seed.py, docs/DATABASE_SCHEMA.md etc.
        # For simplicity scan all py files in backend/app/models and seed.py and tests
        if "models" not in str(file_path) and "seed.py" not in str(file_path) and "tests" not in str(file_path):
            continue
        try:
            text = file_path.read_text(encoding='utf-8')
        except:
            continue
        for i, char in enumerate(text):
            code = ord(char)
            for start, end in suspicious_ranges:
                if start <= code <= end:
                    unexpected.append((str(file_path), i, hex(code), repr(char)))
            # Check zero-width except allowed ZWNJ
            if code in [0x200B, 0x200D, 0xFEFF, 0x00AD]:  # Allow 0x200C (ZWNJ) for Persian
                unexpected.append((str(file_path), i, hex(code), repr(char)))

    # Also scan docs/DATABASE_SCHEMA.md
    schema_file = root / "docs" / "DATABASE_SCHEMA.md"
    if schema_file.exists():
        text = schema_file.read_text(encoding='utf-8')
        for i, char in enumerate(text):
            code = ord(char)
            for start, end in suspicious_ranges:
                if start <= code <= end:
                    unexpected.append((str(schema_file), i, hex(code), repr(char)))
            if code in [0x200B, 0x200D, 0xFEFF, 0x00AD]:
                unexpected.append((str(schema_file), i, hex(code), repr(char)))

    assert len(unexpected) == 0, f"Unexpected bidirectional/zero-width control characters found: {unexpected[:10]}"

def test_model_migration_schema_consistency():
    """Model/migration schema consistency: Base.metadata vs migration file should match 7 tables"""
    # Check that migration file defines same tables as models
    migration_path = pathlib.Path(__file__).parent.parent / "alembic" / "versions" / "001_core_schema.py"
    text = migration_path.read_text()
    # Should contain create_table for all 7 tables
    for table in ["users", "wallets", "ledger_transactions", "personas", "conversations", "messages", "api_keys"]:
        assert f"'{table}'" in text or f'"{table}"' in text, f"Migration should create table {table}"
    
    # Check that models Base has same 7 tables
    tables = Base.metadata.tables.keys()
    expected = {"users", "wallets", "ledger_transactions", "personas", "conversations", "messages", "api_keys"}
    assert expected.issubset(set(tables)), f"Base.metadata missing tables: {expected - set(tables)}"
