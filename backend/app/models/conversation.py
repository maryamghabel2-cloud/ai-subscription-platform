from sqlalchemy import Column, Integer, DateTime, ForeignKey
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from ..database import Base

class Conversation(Base):
    """
    Conversation retention policy (deliberate decision for Phase 1):
    - Explicit conversation deletion MAY delete its messages (cascade).
    - This is chosen for MVP simplicity: when user deletes a conversation, its messages are also deleted.
    - Alternative considered: soft-delete and retain messages forever for audit. Deferred - for Phase 1 we use hard delete with cascade for messages, but RESTRICT for user/persona to prevent accidental loss of parent entities.
    - Documented consistently in DATABASE_SCHEMA.md, model relationships, DB FKs, and tests.
    - Conversations themselves are not soft-deleted currently; messages are NOT always preserved if conversation is explicitly deleted - this is intentional and documented.
    """
    __tablename__ = "conversations"

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="RESTRICT"), nullable=False)
    persona_id = Column(Integer, ForeignKey("personas.id", ondelete="RESTRICT"), nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)

    user = relationship("User", back_populates="conversations")
    persona = relationship("Persona", back_populates="conversations")
    # Explicit conversation deletion may delete its messages - cascade delete-orphan + DB FK CASCADE for consistency
    messages = relationship("Message", back_populates="conversation", cascade="all, delete-orphan", passive_deletes=False)
