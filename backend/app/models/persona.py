from sqlalchemy import Column, Integer, String, DateTime, Text
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from ..database import Base

class Persona(Base):
    __tablename__ = "personas"

    id = Column(Integer, primary_key=True, index=True)
    slug = Column(String(100), unique=True, nullable=False, index=True)
    name_fa = Column(String(255), nullable=False)
    role_definition = Column(Text, nullable=False)
    tone = Column(String(100), nullable=True)
    risk_level = Column(String(20), nullable=False, default="low", index=True)  # low, medium, high
    status = Column(String(20), nullable=False, default="draft", index=True)  # draft, active, deprecated
    version = Column(String(20), nullable=False, default="v1.0.0")
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)

    conversations = relationship("Conversation", back_populates="persona")
