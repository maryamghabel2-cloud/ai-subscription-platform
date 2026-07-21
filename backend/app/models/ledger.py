"""
LedgerTransaction is append-only by design.

Why append-only:
- Financial safety: never update or delete ledger rows. Balance is derived from sum of transactions or maintained via atomic insert + wallet update in same transaction, but history must be immutable.
- Auditability: every credit movement has an immutable record with idempotency_key to prevent double processing.
- Idempotency: idempotency_key is unique indexed, so duplicate requests with same key will raise IntegrityError and must not create second transaction. This prevents double credit/debit on retries, network issues, or replay.
- No UPDATE/DELETE allowed in application logic - only INSERT. This is enforced by code convention and documented here; DB permissions could further enforce read-only for app user on updates/deletes (future).
- reference_id links to external cause (e.g., conversation_id, message_id, admin action) but does not FK to keep ledger decoupled and always insertable even if referenced entity deleted (soft).
- amount is signed: positive = credit purchase/bonus/refund, negative = spend (chat, image, etc.)
- type: e.g., purchase, spend_chat, spend_image, refund, bonus, admin_adjustment
"""
from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Index
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from ..database import Base

class LedgerTransaction(Base):
    __tablename__ = "ledger_transactions"

    id = Column(Integer, primary_key=True, index=True)
    wallet_id = Column(Integer, ForeignKey("wallets.id", ondelete="RESTRICT"), nullable=False, index=True)
    amount = Column(Integer, nullable=False)  # signed: + credit, - debit
    type = Column(String(50), nullable=False, index=True)  # purchase, spend_chat, etc.
    reference_id = Column(String(255), nullable=True, index=True)  # external reference, not FK to keep append-only decoupled
    idempotency_key = Column(String(255), nullable=False, unique=True, index=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False, index=True)

    wallet = relationship("Wallet", back_populates="ledger_transactions")

    __table_args__ = (
        Index("ix_ledger_idempotency_key_unique", "idempotency_key", unique=True),
    )
