from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Text, CheckConstraint
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from ..database import Base

class Message(Base):
    """
    Message retention: follows conversation deletion policy - explicit conversation deletion may delete its messages (cascade).
    Documented in Conversation model and DATABASE_SCHEMA.md.
    """
    __tablename__ = "messages"
    __table_args__ = (
        CheckConstraint("role IN ('user', 'assistant', 'system')", name="ck_messages_role_valid"),
    )

    id = Column(Integer, primary_key=True)
    conversation_id = Column(Integer, ForeignKey("conversations.id", ondelete="CASCADE"), nullable=False)  # CASCADE to match ORM cascade delete-orphan: explicit conversation deletion deletes messages
    role = Column(String(20), nullable=False)
    content = Column(Text, nullable=False)
    enhanced_prompt = Column(Text, nullable=True)
    provider_used = Column(String(100), nullable=True)  # placeholder
    cost_credits = Column(Integer, nullable=True)  # placeholder
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)

    conversation = relationship("Conversation", back_populates="messages")
