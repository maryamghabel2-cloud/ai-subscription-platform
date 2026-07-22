"""
Test seed script creates exactly 2 personas, idempotent, no deletion
"""
import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(__file__)))

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.database import Base
from app.models.persona import Persona

def get_engine():
    return create_engine("sqlite:///:memory:", connect_args={"check_same_thread": False})

def test_seed_creates_exactly_two():
    # Import seed module
    from app import seed as seed_module

    engine = get_engine()
    Base.metadata.create_all(bind=engine)
    SessionFactory = sessionmaker(bind=engine)
    
    # Monkey-patch only SessionLocal and engine, not Base (seed no longer uses Base.create_all)
    original_SessionLocal = seed_module.SessionLocal
    original_engine = seed_module.engine

    seed_module.SessionLocal = SessionFactory
    seed_module.engine = engine

    try:
        # Mock check_schema_migrated to bypass table existence check for sqlite memory (we already created tables)
        # But seed checks inspector for personas table, which exists because we created_all
        personas = seed_module.seed_personas()
        assert len(personas) == 2, f"Expected 2 personas, got {len(personas)}"

        # Verify in DB
        db = SessionFactory()
        count = db.query(Persona).count()
        assert count == 2, f"DB should have exactly 2 personas, got {count}"

        # Verify names and fields per spec
        p1 = db.query(Persona).filter(Persona.slug == "general-assistant").first()
        assert p1 is not None, "general-assistant not found"
        assert p1.name_fa == "دستیار عمومی"
        assert p1.risk_level == "low"
        assert p1.status == "active"

        p2 = db.query(Persona).filter(Persona.slug == "psychologist-draft").first()
        assert p2 is not None, "psychologist-draft not found"
        assert p2.name_fa == "پیش‌نویس روان‌شناس"
        assert p2.risk_level == "high"
        assert p2.status == "draft"
        assert "NOT READY FOR PRODUCTION — pending domain-expert review" in p2.role_definition

        db.close()

        # Test idempotency - second run should not duplicate
        personas2 = seed_module.seed_personas()
        db = SessionFactory()
        count2 = db.query(Persona).count()
        assert count2 == 2, f"Second seed run should be idempotent, expected 2, got {count2}"
        db.close()

    finally:
        seed_module.SessionLocal = original_SessionLocal
        seed_module.engine = original_engine
