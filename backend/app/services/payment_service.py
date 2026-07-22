"""
Payment Intent Service - handles PaymentIntent lifecycle and wallet crediting

- This is the ONLY way to add credits from a payment (via complete_payment)
- All operations atomic and idempotent
- Exchange rate snapshot logic
"""

from typing import List, Tuple, Optional
from datetime import datetime, timezone, timedelta
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError

from ..models.payment_intent import PaymentIntent
from ..models.user import User
from .exchange_rate import get_exchange_rate_snapshot
from .wallet_service import credit_wallet
from ..providers.payment.registry import get_payment_provider

class PaymentIntentAlreadyExistsError(Exception):
    pass

class PaymentExpiredError(Exception):
    pass

class PaymentAlreadyCompletedError(Exception):
    pass

def create_payment_intent(
    db: Session,
    user_id: int,
    provider: str,
    credits_to_add: int,
    amount_toman: Optional[int] = None,
    amount_usd: Optional[int] = None,
    amount_crypto: Optional[str] = None,
    crypto_currency: Optional[str] = None,
    crypto_network: Optional[str] = None,
    idempotency_key: str = None,
) -> PaymentIntent:
    """
    Create payment intent - validate at least one amount field must be set, credits_to_add >0,
    snapshot current exchange rate, set expires_at = now +30 minutes, status pending
    """
    if not amount_toman and not amount_usd and not amount_crypto:
        raise ValueError("At least one amount field must be set (amount_toman, amount_usd, amount_crypto)")

    if credits_to_add <= 0:
        raise ValueError("credits_to_add must be > 0")

    if not idempotency_key:
        raise ValueError("idempotency_key is required")

    # Check idempotency - if payment intent with same key exists, return it (idempotent)
    existing = db.query(PaymentIntent).filter(PaymentIntent.idempotency_key == idempotency_key).first()
    if existing:
        return existing

    # Snapshot exchange rate
    exchange_rate_snapshot = get_exchange_rate_snapshot()

    now = datetime.now(timezone.utc)
    expires_at = now + timedelta(minutes=30)

    # For crypto, generate wallet_address placeholder (would be real address in Part 3C)
    wallet_address = None
    if provider in ["crypto_trc20", "crypto_ton"]:
        wallet_address = f"mock_wallet_address_{provider}_{user_id}_{now.timestamp()}"

    payment_intent = PaymentIntent(
        user_id=user_id,
        amount_toman=amount_toman,
        amount_usd=amount_usd,
        amount_crypto=amount_crypto,
        crypto_currency=crypto_currency,
        crypto_network=crypto_network,
        provider=provider,
        status="pending",
        idempotency_key=idempotency_key,
        exchange_rate_snapshot=exchange_rate_snapshot,
        credits_to_add=credits_to_add,
        created_at=now,
        expires_at=expires_at,
        wallet_address=wallet_address,
    )

    # Initiate payment via provider to get provider_reference
    try:
        provider_instance = get_payment_provider(provider)
        provider_reference = provider_instance.initiate_payment(payment_intent)
        payment_intent.provider_reference = provider_reference
    except Exception:
        # If provider initiation fails, still save intent but without reference? Or fail?
        # For MVP, we save intent even if provider fails, status pending, provider_reference None
        pass

    db.add(payment_intent)
    try:
        db.commit()
    except IntegrityError:
        db.rollback()
        # Race condition: another request with same idempotency_key inserted just now
        existing = db.query(PaymentIntent).filter(PaymentIntent.idempotency_key == idempotency_key).first()
        if existing:
            return existing
        raise

    db.refresh(payment_intent)
    return payment_intent

def complete_payment(db: Session, payment_intent_id: str, verification_data: dict = None) -> PaymentIntent:
    """
    Complete payment - only if status pending or processing and not expired
    Verify idempotency (cannot complete twice)
    Atomically: update PaymentIntent status to completed and credit wallet with credits_to_add
    This is the ONLY way to add credits from a payment
    """
    payment_intent = db.query(PaymentIntent).filter(PaymentIntent.id == payment_intent_id).first()
    if not payment_intent:
        raise ValueError("PaymentIntent not found")

    if payment_intent.status not in ["pending", "processing"]:
        raise PaymentAlreadyCompletedError(f"PaymentIntent status is {payment_intent.status}, cannot complete")

    now = datetime.now(timezone.utc)
    expires_at = payment_intent.expires_at
    if expires_at.tzinfo is None:
        expires_at = expires_at.replace(tzinfo=timezone.utc)
    if now > expires_at:
        # Expire it
        payment_intent.status = "expired"
        payment_intent.failed_at = now
        payment_intent.failure_reason = "Payment expired"
        db.commit()
        raise PaymentExpiredError("Payment expired")

    # Check if already completed (idempotency for complete)
    if payment_intent.status == "completed":
        return payment_intent

    # Atomically: update payment intent and credit wallet
    try:
        # Update payment intent
        payment_intent.status = "completed"
        payment_intent.verified_at = now
        payment_intent.verification_data = verification_data or {}

        # Credit wallet - this is the ONLY way to add credits from payment
        # Use idempotency key for ledger as well: payment_intent_id + credits
        wallet_idempotency_key = f"payment_{payment_intent.id}_credit_{payment_intent.credits_to_add}"
        # Note: credit_wallet itself checks idempotency for ledger, but we also need to ensure wallet credit is not double
        # We will call credit_wallet which is idempotent via ledger idempotency_key
        credit_wallet(
            db,
            user_id=payment_intent.user_id,
            amount=payment_intent.credits_to_add,
            reference_type="payment",
            reference_id=str(payment_intent.id),
            idempotency_key=wallet_idempotency_key,
        )

        db.commit()
        db.refresh(payment_intent)
        return payment_intent
    except Exception:
        db.rollback()
        raise

def fail_payment(db: Session, payment_intent_id: str, reason: str) -> PaymentIntent:
    """Fail payment - only if status pending or processing"""
    payment_intent = db.query(PaymentIntent).filter(PaymentIntent.id == payment_intent_id).first()
    if not payment_intent:
        raise ValueError("PaymentIntent not found")

    if payment_intent.status not in ["pending", "processing"]:
        raise ValueError(f"Cannot fail payment with status {payment_intent.status}")

    payment_intent.status = "failed"
    payment_intent.failed_at = datetime.now(timezone.utc)
    payment_intent.failure_reason = reason[:500] if reason else None
    db.commit()
    db.refresh(payment_intent)
    return payment_intent

def expire_stale_payments(db: Session) -> int:
    """Find all pending payments where expires_at < now and update status to expired - called by periodic task"""
    now = datetime.now(timezone.utc)
    stale_payments = db.query(PaymentIntent).filter(
        PaymentIntent.status == "pending",
        PaymentIntent.expires_at < now
    ).all()

    count = 0
    for payment in stale_payments:
        payment.status = "expired"
        payment.failed_at = now
        payment.failure_reason = "Expired by scheduler"
        count += 1

    db.commit()
    return count

def get_user_payments(db: Session, user_id: int, page: int = 1, per_page: int = 20) -> Tuple[List[PaymentIntent], int]:
    """Return paginated payment history for user - users can only see their own payments"""
    query = db.query(PaymentIntent).filter(PaymentIntent.user_id == user_id).order_by(PaymentIntent.created_at.desc())
    total = query.count()
    payments = query.offset((page - 1) * per_page).limit(per_page).all()
    return payments, total
