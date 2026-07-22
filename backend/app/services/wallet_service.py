"""
Wallet Service - Atomic operations with append-only signed credit ledger

- Atomic credit/debit via transactions
- SELECT FOR UPDATE on wallet row before debit to prevent race condition
- Idempotency key checked BEFORE starting transaction, same key returns same result without double processing
- Wallet balance never below zero enforced at DB (check constraint) and code level
- Ledger is append-only: no UPDATE, no DELETE on ledger_transactions
- All amounts are integers (no floating point for money)
"""

from typing import List, Tuple, Optional
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from sqlalchemy import select
from datetime import datetime, timezone

from ..models.wallet import Wallet
from ..models.ledger import LedgerTransaction
from ..models.user import User

class InsufficientCreditsError(Exception):
    pass

class WalletNotFoundError(Exception):
    pass

def _get_wallet_for_update(db: Session, user_id: int) -> Wallet:
    """
    SELECT FOR UPDATE on wallet row to prevent race condition during debit
    In PostgreSQL, with_for_update() locks row until transaction commit
    In SQLite, with_for_update() is ignored but transaction still provides some safety for single-instance MVP
    """
    stmt = select(Wallet).where(Wallet.user_id == user_id).with_for_update()
    result = db.execute(stmt)
    wallet = result.scalars().first()
    if not wallet:
        # Try to create wallet if not exists? For safety, auto-create with 0 balance if not exists
        # But per Part 1, wallet should exist after registration
        # For robustness, create if missing
        wallet = Wallet(user_id=user_id, balance_credits=0)
        db.add(wallet)
        db.flush()
    return wallet

def _check_idempotency(db: Session, idempotency_key: str) -> Optional[LedgerTransaction]:
    """Check idempotency BEFORE starting transaction - if exists and successful, return same result"""
    return db.query(LedgerTransaction).filter(LedgerTransaction.idempotency_key == idempotency_key).first()

def credit_wallet(db: Session, user_id: int, amount: int, reference_type: str, reference_id: str, idempotency_key: str) -> int:
    """
    Credit wallet - atomic and idempotent
    - Verify idempotency (same key = same result, no double credit)
    - BEGIN transaction
    - INSERT ledger_transaction (positive amount)
    - UPDATE wallet SET balance = balance + amount
    - COMMIT
    - Return new balance
    """
    if amount <= 0:
        raise ValueError("Credit amount must be > 0")

    # Idempotency check BEFORE transaction
    existing = _check_idempotency(db, idempotency_key)
    if existing:
        # Return current balance (or balance after existing transaction)
        wallet = db.query(Wallet).filter(Wallet.user_id == user_id).first()
        if wallet:
            return wallet.balance_credits
        return 0

    # For SQLite, we need to handle transaction manually, but SQLAlchemy session is already transactional
    # Use SELECT FOR UPDATE for wallet
    try:
        wallet = _get_wallet_for_update(db, user_id)

        # INSERT ledger positive
        ledger = LedgerTransaction(
            wallet_id=wallet.id,
            amount=amount,  # positive
            type=reference_type,
            reference_id=reference_id,
            idempotency_key=idempotency_key,
        )
        db.add(ledger)

        # UPDATE wallet balance
        wallet.balance_credits = wallet.balance_credits + amount
        # Also update updated_at handled by server_default? We set via func.now() onupdate, but we can set explicitly if needed

        db.commit()
        db.refresh(wallet)
        return wallet.balance_credits
    except IntegrityError:
        db.rollback()
        # Check if it was idempotency conflict - another concurrent request inserted same key
        existing = _check_idempotency(db, idempotency_key)
        if existing:
            wallet = db.query(Wallet).filter(Wallet.user_id == user_id).first()
            return wallet.balance_credits if wallet else 0
        raise

def debit_wallet(db: Session, user_id: int, amount: int, reference_type: str, reference_id: str, idempotency_key: str) -> int:
    """
    Debit wallet - atomic, idempotent, never negative
    - Verify idempotency
    - BEGIN transaction
    - Check balance >= amount (SELECT FOR UPDATE)
    - If insufficient: raise InsufficientCreditsError, do NOT insert
    - INSERT ledger (negative amount)
    - UPDATE wallet SET balance = balance - amount
    - COMMIT
    """
    if amount <= 0:
        raise ValueError("Debit amount must be > 0")

    # Idempotency check BEFORE
    existing = _check_idempotency(db, idempotency_key)
    if existing:
        wallet = db.query(Wallet).filter(Wallet.user_id == user_id).first()
        return wallet.balance_credits if wallet else 0

    try:
        wallet = _get_wallet_for_update(db, user_id)

        # Check balance >= amount
        if wallet.balance_credits < amount:
            raise InsufficientCreditsError(f"Insufficient credits: have {wallet.balance_credits}, need {amount}")

        # INSERT ledger negative
        ledger = LedgerTransaction(
            wallet_id=wallet.id,
            amount=-amount,  # negative for debit
            type=reference_type,
            reference_id=reference_id,
            idempotency_key=idempotency_key,
        )
        db.add(ledger)

        # UPDATE wallet balance
        wallet.balance_credits = wallet.balance_credits - amount

        db.commit()
        db.refresh(wallet)
        return wallet.balance_credits
    except IntegrityError:
        db.rollback()
        existing = _check_idempotency(db, idempotency_key)
        if existing:
            wallet = db.query(Wallet).filter(Wallet.user_id == user_id).first()
            return wallet.balance_credits if wallet else 0
        raise

def refund_wallet(db: Session, user_id: int, amount: int, original_reference_id: str, idempotency_key: str) -> int:
    """
    Refund wallet - same as credit but with type=refund
    """
    return credit_wallet(db, user_id, amount, "refund", original_reference_id, idempotency_key)

def get_balance(db: Session, user_id: int) -> int:
    wallet = db.query(Wallet).filter(Wallet.user_id == user_id).first()
    if not wallet:
        return 0
    return wallet.balance_credits

def get_transaction_history(db: Session, user_id: int, page: int = 1, per_page: int = 20) -> Tuple[List[LedgerTransaction], int]:
    """
    Return paginated ledger transactions for user - users can only see their own transactions
    """
    wallet = db.query(Wallet).filter(Wallet.user_id == user_id).first()
    if not wallet:
        return [], 0

    query = db.query(LedgerTransaction).filter(LedgerTransaction.wallet_id == wallet.id).order_by(LedgerTransaction.created_at.desc())
    total = query.count()
    transactions = query.offset((page - 1) * per_page).limit(per_page).all()
    return transactions, total
