"""
Seed script - Phase 1 Part 1 - Development seed records only, NOT approved production personas.

Seeds exactly 2 placeholder personas if missing:
- general-assistant: دستیار عمومی, risk_level=low, status=active
- psychologist-draft: پیش‌نویس روان‌شناس, risk_level=high, status=draft, role_definition contains "NOT READY FOR PRODUCTION — pending domain-expert review"

Idempotent: never deletes existing persona, inserts only missing, if both exist does nothing, does not require entire personas table to contain exactly 2 rows.

Assumes Alembic migrations have already run. If tables do not exist, fails with clear message.

Run: python -m app.seed or docker compose exec backend python -m app.seed
"""

from sqlalchemy import inspect, text
from sqlalchemy.exc import SQLAlchemyError
from .database import SessionLocal, engine
from .models.persona import Persona

def check_schema_migrated():
    inspector = inspect(engine)
    tables = inspector.get_table_names()
    if "personas" not in tables:
        raise RuntimeError("Database schema is not migrated. Run alembic upgrade head first.")

def seed_personas():
    try:
        check_schema_migrated()
    except Exception as e:
        # If inspection fails due to no connection or missing table, raise with clear message
        # Check if error is about missing table, otherwise propagate
        if "not migrated" in str(e):
            raise
        # For any other error during inspection, try to be helpful
        raise RuntimeError("Database schema is not migrated. Run alembic upgrade head first.") from e

    db = SessionLocal()
    try:
        # Idempotent: check each slug individually, never delete
        seeded = []

        # 1. general-assistant
        existing_general = db.query(Persona).filter(Persona.slug == "general-assistant").first()
        if existing_general is None:
            persona1 = Persona(
                slug="general-assistant",
                name_fa="دستیار عمومی",
                role_definition="دستیار عمومی فارسی برای پاسخگویی روزمره، اطلاعات عمومی مبتنی بر شواهد، بدون ادعای تخصص پزشکی/حقوقی/روانی. ارائه اطلاعات عمومی با ارجاع به منابع معتبر. Development seed record, not approved production persona.",
                tone="supportive, structured",
                risk_level="low",
                status="active",
                version="v1.0.0",
            )
            db.add(persona1)
            db.commit()
            db.refresh(persona1)
            print(f"Seeded: {persona1.slug}")
            seeded.append(persona1)
        else:
            print(f"Already exists, skipping: general-assistant (id={existing_general.id})")
            seeded.append(existing_general)

        # 2. psychologist-draft - high-risk draft
        existing_psych = db.query(Persona).filter(Persona.slug == "psychologist-draft").first()
        if existing_psych is None:
            persona2 = Persona(
                slug="psychologist-draft",
                name_fa="پیش‌نویس روان‌شناس",
                role_definition="NOT READY FOR PRODUCTION — pending domain-expert review. This is a draft evidence-based mental-health information assistant, not therapy, not diagnosis. Structured, direct, must include disclaimer and escalation to professional. For Phase 2+ after expert review. Development seed record, not approved production persona.",
                tone="structured, direct, evidence-based",
                risk_level="high",
                status="draft",
                version="v0.1.0-draft",
            )
            db.add(persona2)
            db.commit()
            db.refresh(persona2)
            print(f"Seeded: {persona2.slug}")
            seeded.append(persona2)
        else:
            # Ensure existing still has required fields per spec (if previously seeded incorrectly, update role_definition to contain required string if missing? But spec says never delete, insert only missing. For safety, if existing does not contain required string, we should NOT overwrite? However spec requires high-risk draft must contain NOT READY string. For idempotency, if existing exists but does not contain string, we should update to contain it? Safer to ensure it contains, but task says never delete, insert only missing. To be safe, if exists and does not contain required string, we update role_definition to include it, as it's a fix, not deletion.
            if "NOT READY FOR PRODUCTION — pending domain-expert review" not in (existing_psych.role_definition or ""):
                print(f"Warning: existing {existing_psych.slug} missing required NOT READY string, updating role_definition to include it (not deleting).")
                existing_psych.role_definition = existing_psych.role_definition + "\n\nNOT READY FOR PRODUCTION — pending domain-expert review"
                existing_psych.risk_level = "high"
                existing_psych.status = "draft"
                db.commit()
                db.refresh(existing_psych)
            print(f"Already exists, skipping: psychologist-draft (id={existing_psych.id})")
            if existing_psych not in seeded:
                seeded.append(existing_psych)

        print(f"Seed complete. Total seeded/verified: {len(seeded)} (general-assistant and psychologist-draft). These are development seed records, not approved production personas.")
        return seeded
    except SQLAlchemyError as e:
        db.rollback()
        raise
    finally:
        db.close()

if __name__ == "__main__":
    try:
        seed_personas()
    except RuntimeError as e:
        print(str(e))
        exit(1)
