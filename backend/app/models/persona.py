from sqlalchemy import Column, Integer, String, DateTime, Text, CheckConstraint
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from ..database import Base

class Persona(Base):
    __tablename__ = "personas"
    __table_args__ = (
        CheckConstraint("risk_level IN ('low', 'medium', 'high')", name="ck_personas_risk_level_valid"),
        CheckConstraint("status IN ('draft', 'active', 'deprecated')", name="ck_personas_status_valid"),
    )

    id = Column(Integer, primary_key=True)  # No index=True
    slug = Column(String(100), unique=True, nullable=False)  # unique creates index
    name_fa = Column(String(255), nullable=False)
    role_definition = Column(Text, nullable=False)
    tone = Column(String(100), nullable=True)
    risk_level = Column(String(20), nullable=False, server_default="low")
    status = Column(String(20), nullable=False, server_default="draft")
    version = Column(String(20), nullable=False, server_default="v1.0.0")  # Semantic-version String - explicit decision: keep as String for flexibility (e.g., v1.0.0-draft), not integer, documented in DATABASE_SCHEMA.md
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)

    conversations = relationship("Conversation", back_populates="persona")
