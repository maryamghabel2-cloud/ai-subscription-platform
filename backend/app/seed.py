"""
Seed script - Phase 1 Part 1
Creates exactly 2 placeholder personas for testing.

- دستیار عمومی (risk_level=low, status=active)
- پیش‌نویس روان‌شناس (risk_level=high, status=draft, role_definition contains "NOT READY FOR PRODUCTION — pending domain-expert review")

Run: python -m app.seed or docker compose exec backend python -m app.seed
"""

from .database import SessionLocal, Base, engine
from .models.persona import Persona

def seed_personas():
    # Ensure tables exist (for local sqlite dev, alembic would have created)
    Base.metadata.create_all(bind=engine)
    db = SessionLocal()
    try:
        # Check if already seeded
        existing = db.query(Persona).filter(Persona.slug.in_(["general-assistant", "draft-psychologist"])).all()
        if len(existing) >= 2:
            print(f"Seed already exists: {len(existing)} personas found, skipping creation to keep exactly 2")
            # Ensure exactly 2, not more
            # If more than 2, we would not delete, but test expects exactly 2 after fresh DB
            return existing

        # Clean if partially exists
        for p in existing:
            db.delete(p)
        db.commit()

        persona1 = Persona(
            slug="general-assistant",
            name_fa="دستیار عمومی",
            role_definition="دستیار عمومی فارسی برای پاسخگویی روزمره، اطلاعات عمومی مبتنی بر شواهد، بدون ادعای تخصص پزشکی/حقوقی/روانی. ارائه اطلاعات عمومی با ارجاع به منابع معتبر.",
            tone="supportive, structured",
            risk_level="low",
            status="active",
            version="v1.0.0",
        )

        persona2 = Persona(
            slug="draft-psychologist",
            name_fa="پیش‌نویس روان‌شناس",
            role_definition="NOT READY FOR PRODUCTION — pending domain-expert review. This is a draft evidence-based mental-health information assistant, not therapy, not diagnosis. Structured, direct, must include disclaimer and escalation to professional. For Phase 2+ after expert review.",
            tone="structured, direct, evidence-based",
            risk_level="high",
            status="draft",
            version="v0.1.0-draft",
        )

        db.add_all([persona1, persona2])
        db.commit()
        db.refresh(persona1)
        db.refresh(persona2)
        print(f"Seeded 2 personas: {persona1.slug} (low/active) and {persona2.slug} (high/draft)")
        return [persona1, persona2]
    finally:
        db.close()

if __name__ == "__main__":
    seed_personas()
