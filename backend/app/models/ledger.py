from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, UniqueConstraint, CheckConstraint, Index
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from ..database import Base

class LedgerTransaction(Base):
    """
    LedgerTransaction is append-only signed credit ledger by design (not double-entry).

    Why append-only signed credit ledger:
    - Financial safety: never UPDATE or DELETE ledger rows. History must be immutable. Balance is cached/materialized in wallets.balance_credits but must be reconciled via SUM(ledger.amount).
    - Auditability: every credit movement has immutable record with idempotency_key to prevent double processing.
    - Idempotency: idempotency_key has exactly one uniqueness mechanism (named UNIQUE constraint) - duplicate requests with same key raise IntegrityError and must not create second transaction.
    - No UPDATE/DELETE allowed in application logic - only INSERT. Enforced by code convention; database-level immutability permissions/triggers deferred to wallet/ledger implementation PR (Part 3).
    - reference_id links to external cause but not FK to keep ledger decoupled.
    - amount is signed: positive credit, negative debit, never zero per check.
    - balance_credits is cached/materialized balance - Part 3 must update wallet balance and ledger insert atomically, reconciliation must compare wallet balance with SUM(ledger.amount).
    - Not double-entry: true double-entry would have separate debit/credit accounts; here single signed amount + cached balance. Append-only signed credit ledger terminology must be used.
    """
    __tablename__ = "ledger_transactions"
    __table_args__ = (
        UniqueConstraint("idempotency_key", name="uq_ledger_idempotency_key"),  # Exactly one uniqueness mechanism for idempotency_key
        CheckConstraint("amount <> 0", name="ck_ledger_amount_nonzero"),
        Index("ix_ledger_wallet_id", "wallet_id"),
        Index("ix_ledger_type", "type"),
        Index("ix_ledger_created_at", "created_at"),
    )

    id = Column(Integer, primary_key=True)  # No index=True
    wallet_id = Column(Integer, ForeignKey("wallets.id", ondelete="RESTRICT"), nullable=False)
    amount = Column(Integer, nullable=False)  # signed
    type = Column(String(50), nullable=False)
    reference_id = Column(String(255), nullable=True)
    idempotency_key = Column(String(255), nullable=False)  # uniqueness via constraint above
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)

    wallet = relationship("Wallet", back_populates="ledger_transactions")
