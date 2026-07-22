import uuid
from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, CheckConstraint, Index
from sqlalchemy import JSON as GenericJSON
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from ..database import Base

# JSONB for Postgres, JSON variant for SQLite compatibility
VerificationDataType = JSONB().with_variant(GenericJSON(), 'sqlite')

class PaymentIntent(Base):
    __tablename__ = "payment_intents"
    __table_args__ = (
        CheckConstraint("expires_at > created_at", name="ck_payment_intents_expires_gt_created"),
        CheckConstraint("credits_to_add > 0", name="ck_payment_intents_credits_positive"),
        CheckConstraint("status IN ('pending', 'processing', 'completed', 'failed', 'expired', 'refunded')", name="ck_payment_intents_status_valid"),
        CheckConstraint("provider IN ('zarinpal', 'crypto_trc20', 'crypto_ton', 'sandbox_mock')", name="ck_payment_intents_provider_valid"),
        Index("ix_payment_intents_user_id", "user_id"),
        Index("ix_payment_intents_status", "status"),
        Index("ix_payment_intents_provider", "provider"),
        Index("ix_payment_intents_created_at", "created_at"),
    )

    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    user_id = Column(Integer, ForeignKey("users.id", ondelete="RESTRICT"), nullable=False)
    amount_toman = Column(Integer, nullable=True)
    amount_usd = Column(Integer, nullable=True)  # stored as cents
    amount_crypto = Column(String(50), nullable=True)  # exact string to preserve decimal precision
    crypto_currency = Column(String(20), nullable=True)  # USDT, TON, TRX
    crypto_network = Column(String(20), nullable=True)  # TRC20, TON
    provider = Column(String(50), nullable=False)  # zarinpal, crypto_trc20, crypto_ton, sandbox_mock
    provider_reference = Column(String(255), nullable=True)  # ZarinPal authority or tx_hash
    wallet_address = Column(String(255), nullable=True)  # crypto receive address
    status = Column(String(20), nullable=False, server_default="pending", default="pending")
    idempotency_key = Column(String(255), unique=True, nullable=False)
    exchange_rate_snapshot = Column(Integer, nullable=True)  # Toman per USD
    credits_to_add = Column(Integer, nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    expires_at = Column(DateTime(timezone=True), nullable=False)
    verified_at = Column(DateTime(timezone=True), nullable=True)
    failed_at = Column(DateTime(timezone=True), nullable=True)
    verification_data = Column(VerificationDataType, nullable=True)
    failure_reason = Column(String(500), nullable=True)

    user = relationship("User", backref="payment_intents")
