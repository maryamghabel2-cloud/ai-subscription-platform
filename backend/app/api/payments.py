from fastapi import APIRouter, Depends, HTTPException, Request, Query
from sqlalchemy.orm import Session
from pydantic import BaseModel
from typing import Optional
from ..database import get_db
from ..core.deps import get_current_user
from ..core.csrf import validate_csrf
from ..core.security import hash_token
from ..models.user import User
from ..models.payment_intent import PaymentIntent
from ..services import payment_service
from ..services.exchange_rate import get_exchange_rate
from ..config import settings
from ..providers.payment.registry import is_sandbox_provider

router = APIRouter(prefix="/payments", tags=["payments"])

class CreatePaymentRequest(BaseModel):
    provider: str
    amount_toman: Optional[int] = None
    amount_usd: Optional[int] = None
    amount_crypto: Optional[str] = None
    crypto_currency: Optional[str] = None
    crypto_network: Optional[str] = None
    credits_to_add: int
    idempotency_key: str

class SimulateCompleteRequest(BaseModel):
    verification_data: Optional[dict] = None

@router.get("/packages")
def get_packages():
    """
    Public endpoint - returns available credit packages (from config, not hardcoded in code logic)
    """
    return {"packages": settings.CREDIT_PACKAGES, "exchange_rate_toman_per_usd": get_exchange_rate()}

@router.post("/create")
def create_payment(
    request: Request,
    payload: CreatePaymentRequest,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    # CSRF required for authenticated state-changing
    session_token = request.cookies.get("nv_session")
    if not session_token:
        raise HTTPException(status_code=401, detail="Not authenticated")
    from ..models.auth_session import AuthSession
    session_hash = hash_token(session_token)
    session = db.query(AuthSession).filter(AuthSession.session_token_hash == session_hash).first()
    if not session:
        raise HTTPException(status_code=401, detail="Invalid session")
    try:
        validate_csrf(request, session.csrf_token_hash, hash_token)
    except HTTPException as e:
        raise e

    try:
        intent = payment_service.create_payment_intent(
            db=db,
            user_id=current_user.id,
            provider=payload.provider,
            credits_to_add=payload.credits_to_add,
            amount_toman=payload.amount_toman,
            amount_usd=payload.amount_usd,
            amount_crypto=payload.amount_crypto,
            crypto_currency=payload.crypto_currency,
            crypto_network=payload.crypto_network,
            idempotency_key=payload.idempotency_key,
        )
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

    return {
        "id": intent.id,
        "user_id": intent.user_id,
        "provider": intent.provider,
        "status": intent.status,
        "amount_toman": intent.amount_toman,
        "amount_usd": intent.amount_usd,
        "amount_crypto": intent.amount_crypto,
        "crypto_currency": intent.crypto_currency,
        "crypto_network": intent.crypto_network,
        "provider_reference": intent.provider_reference,
        "wallet_address": intent.wallet_address,
        "credits_to_add": intent.credits_to_add,
        "exchange_rate_snapshot": intent.exchange_rate_snapshot,
        "expires_at": intent.expires_at,
        "created_at": intent.created_at,
    }

@router.post("/{payment_id}/simulate-complete")
def simulate_complete(
    payment_id: str,
    request: Request,
    payload: SimulateCompleteRequest = None,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    SANDBOX ONLY - Simulates successful payment verification, credits wallet
    Only works when PAYMENT_PROVIDER=sandbox_mock
    Must be disabled in production
    """
    if not is_sandbox_provider():
        raise HTTPException(status_code=403, detail="Simulate-complete only available with sandbox_mock provider. SANDBOX ONLY — NOT FOR PRODUCTION.")

    # CSRF required
    session_token = request.cookies.get("nv_session")
    if session_token:
        from ..models.auth_session import AuthSession
        session_hash = hash_token(session_token)
        session = db.query(AuthSession).filter(AuthSession.session_token_hash == session_hash).first()
        if session:
            try:
                validate_csrf(request, session.csrf_token_hash, hash_token)
            except HTTPException as e:
                raise e

    # Verify payment intent belongs to current user
    intent = db.query(PaymentIntent).filter(PaymentIntent.id == payment_id, PaymentIntent.user_id == current_user.id).first()
    if not intent:
        raise HTTPException(status_code=404, detail="Payment intent not found")

    verification_data = payload.verification_data if payload and payload.verification_data else {"mock": True, "simulated": True}

    try:
        completed = payment_service.complete_payment(db, payment_id, verification_data)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

    return {
        "id": completed.id,
        "status": completed.status,
        "credits_to_add": completed.credits_to_add,
        "verified_at": completed.verified_at,
    }

@router.get("/history")
def get_history(
    page: int = Query(1, ge=1),
    per_page: int = Query(20, ge=1, le=100),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    payments, total = payment_service.get_user_payments(db, current_user.id, page, per_page)
    return {
        "payments": [
            {
                "id": p.id,
                "provider": p.provider,
                "status": p.status,
                "amount_toman": p.amount_toman,
                "amount_usd": p.amount_usd,
                "amount_crypto": p.amount_crypto,
                "credits_to_add": p.credits_to_add,
                "exchange_rate_snapshot": p.exchange_rate_snapshot,
                "created_at": p.created_at,
                "expires_at": p.expires_at,
                "verified_at": p.verified_at,
            }
            for p in payments
        ],
        "total": total,
        "page": page,
        "per_page": per_page,
    }
