from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
from ..database import get_db
from ..core.deps import get_current_user
from ..models.user import User
from ..services import wallet_service

router = APIRouter(prefix="/wallet", tags=["wallet"])

@router.get("/balance")
def get_balance(db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    balance = wallet_service.get_balance(db, current_user.id)
    return {"user_id": current_user.id, "balance_credits": balance}

@router.get("/transactions")
def get_transactions(
    page: int = Query(1, ge=1),
    per_page: int = Query(20, ge=1, le=100),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    transactions, total = wallet_service.get_transaction_history(db, current_user.id, page, per_page)
    return {
        "transactions": [
            {
                "id": t.id,
                "wallet_id": t.wallet_id,
                "amount": t.amount,
                "type": t.type,
                "reference_id": t.reference_id,
                "idempotency_key": t.idempotency_key,
                "created_at": t.created_at,
            }
            for t in transactions
        ],
        "total": total,
        "page": page,
        "per_page": per_page,
    }
