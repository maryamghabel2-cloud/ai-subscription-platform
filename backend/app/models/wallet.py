from sqlalchemy import Column, Integer, DateTime, ForeignKey, UniqueConstraint, CheckConstraint
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from ..database import Base

class Wallet(Base):
    __tablename__ = "wallets"
    __table_args__ = (
        UniqueConstraint("user_id", name="uq_wallets_user_id"),  # Exactly one uniqueness mechanism for user_id
        CheckConstraint("balance_credits >= 0", name="ck_wallets_balance_non_negative"),
    )

    id = Column(Integer, primary_key=True)  # No index=True, PK already indexed
    user_id = Column(Integer, ForeignKey("users.id", ondelete="RESTRICT"), nullable=False)  # Unique via constraint above, no unique=True + index=True duplicate
    balance_credits = Column(Integer, nullable=False, server_default="0")
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now(), nullable=False)

    user = relationship("User", back_populates="wallet")
    ledger_transactions = relationship("LedgerTransaction", back_populates="wallet")
