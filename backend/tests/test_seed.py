"""
Test seed script creates exactly 2 personas
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
    # Import seed function but use isolated DB
    from app import seed as seed_module

    # Override engine and SessionLocal for test isolation
    engine = get_engine()
    Base.metadata.create_all(bind=engine)
    Session = sessionmaker(bind=engine)
    
    # Monkey-patch seed's dependencies
    original_SessionLocal = seed_module.SessionLocal
    original_engine = seed_module.engine
    original_Base = seed_module.Base

    seed_module.SessionLocal = Session
    seed_module.engine = engine
    seed_module.Base = Base

    try:
        personas = seed_module.seed_personas()
        assert len(personas) == 2, f"Expected 2 personas, got {len(personas)}"

        # Verify in DB
        db = Session()
        count = db.query(Persona).count()
        assert count == 2, f"DB should have exactly 2 personas, got {count}"

        # Verify names and fields per spec
        p1 = db.query(Persona).filter(Persona.slug == "general-assistant").first()
        assert p1 is not None, "general-assistant not found"
        assert p1.name_fa == "دستیار عمومی"
        assert p1.risk_level == "low"
        assert p1.status == "active"

        p2 = db.query(Persona).filter(Persona.slug == "draft-psychologist").first()
        assert p2 is not None, "draft-psychologist not found"
        assert p2.name_fa == "پیش‌نویس روان‌شناس"
        assert p2.risk_level == "high"
        assert p2.status == "draft"
        assert "NOT READY FOR PRODUCTION — pending domain-expert review" in p2.role_definition

        db.close()
    finally:
        # Restore
        seed_module.SessionLocal = original_SessionLocal
        seed_module.engine = original_engine
        seed_module.Base = original_Base
