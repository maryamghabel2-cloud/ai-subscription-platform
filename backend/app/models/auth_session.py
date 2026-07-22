import uuid
from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, CheckConstraint
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from ..database import Base

class AuthSession(Base):
    """
    Auth session - opaque session token auth, not JWT.
    Stores only token hashes, never raw tokens.
    ID is String UUID for compatibility with both PostgreSQL and SQLite (tests).
    """
    __tablename__ = "auth_sessions"
    __table_args__ = (
        CheckConstraint("expires_at > created_at", name="ck_auth_sessions_expires_gt_created"),
        CheckConstraint("refresh_expires_at > created_at", name="ck_auth_sessions_refresh_expires_gt_created"),
    )

    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    user_id = Column(Integer, ForeignKey("users.id", ondelete="RESTRICT"), nullable=False, index=True)
    session_token_hash = Column(String(255), unique=True, nullable=False, index=True)
    refresh_token_hash = Column(String(255), unique=True, nullable=False, index=True)
    csrf_token_hash = Column(String(255), nullable=False)
    user_agent_hash = Column(String(255), nullable=True)
    ip_hash = Column(String(255), nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    last_used_at = Column(DateTime(timezone=True), nullable=True)
    expires_at = Column(DateTime(timezone=True), nullable=False)
    refresh_expires_at = Column(DateTime(timezone=True), nullable=False)
    revoked_at = Column(DateTime(timezone=True), nullable=True)

    user = relationship("User", backref="auth_sessions")
