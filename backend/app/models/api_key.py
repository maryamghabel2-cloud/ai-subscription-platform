from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, CheckConstraint, JSON
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from ..database import Base

# Use JSONB for PostgreSQL, fallback to generic JSON for SQLite to allow tests
# JSONB is acceptable per spec, generic JSON works on SQLite
ScopesType = JSONB().with_variant(JSON(), 'sqlite')

class ApiKey(Base):
    """
    ApiKey - stores only key_prefix (non-secret) and key_hash (secure), never raw key.
    Raw API keys are never stored - tested.
    """
    __tablename__ = "api_keys"
    __table_args__ = (
        CheckConstraint("rate_limit_per_minute > 0", name="ck_api_keys_rate_limit_positive"),
    )

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="RESTRICT"), nullable=False)
    key_prefix = Column(String(20), nullable=False)  # Non-secret prefix for identifying keys without storing raw key
    key_hash = Column(String(255), unique=True, nullable=False)  # Secure hash, never raw key, unique constraint uq_api_keys_key_hash
    scopes = Column(ScopesType, nullable=True, server_default="{}")  # PostgreSQL JSONB for MVP, acceptable per spec
    rate_limit_per_minute = Column(Integer, nullable=False, server_default="60")  # Renamed from rate_limit
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    revoked_at = Column(DateTime(timezone=True), nullable=True)

    user = relationship("User", back_populates="api_keys")
