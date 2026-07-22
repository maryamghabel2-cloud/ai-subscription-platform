from fastapi import APIRouter, Depends, HTTPException, Request
from sqlalchemy.orm import Session
from pydantic import BaseModel
from ..database import get_db
from ..core.deps import require_admin
from ..core.csrf import validate_csrf
from ..core.security import hash_token
from ..models.auth_session import AuthSession
from ..models.user import User
from ..services.wallet_service import credit_wallet
import uuid

router = APIRouter(prefix="/admin", tags=["admin"])

class GrantRequest(BaseModel):
    amount: int
    reason: str

@router.post("/wallet/{user_id}/grant")
def admin_grant_credits(
    user_id: int,
    payload: GrantRequest,
    request: Request,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_admin)
):
    # CSRF
    session_token = request.cookies.get("nv_session")
    if session_token:
        session_hash = hash_token(session_token)
        session = db.query(AuthSession).filter(AuthSession.session_token_hash == session_hash).first()
        if session:
            try:
                validate_csrf(request, session.csrf_token_hash, hash_token)
            except HTTPException as e:
                raise e

    if payload.amount <= 0:
        raise HTTPException(status_code=400, detail="Amount must be > 0")

    idempotency_key = f"admin_grant_{user_id}_{payload.amount}_{uuid.uuid4().hex}"

    try:
        new_balance = credit_wallet(
            db,
            user_id=user_id,
            amount=payload.amount,
            reference_type="grant",
            reference_id=f"admin_grant_by_{current_user.id}_{payload.reason}",
            idempotency_key=idempotency_key,
        )
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

    return {"user_id": user_id, "new_balance": new_balance, "granted": payload.amount, "reason": payload.reason}
