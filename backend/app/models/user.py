from sqlalchemy import Column, Integer, String, Boolean, DateTime, CheckConstraint
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from ..database import Base

class User(Base):
    __tablename__ = "users"
    __table_args__ = (
        CheckConstraint("role IN ('user', 'admin')", name="ck_users_role_valid"),
    )

    id = Column(Integer, primary_key=True)  # No explicit index=True, PK already indexed
    email = Column(String(255), unique=True, nullable=False)  # unique creates index, no extra index=True
    normalized_email = Column(String(255), unique=True, nullable=False)  # explicit normalized for case-insensitive unique strategy, see DATABASE_SCHEMA.md
    password_hash = Column(String(255), nullable=False)
    role = Column(String(50), nullable=False, server_default="user")
    is_active = Column(Boolean, default=True, nullable=False, server_default="true")
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)

    wallet = relationship("Wallet", back_populates="user", uselist=False)
    conversations = relationship("Conversation", back_populates="user")
    api_keys = relationship("ApiKey", back_populates="user")
