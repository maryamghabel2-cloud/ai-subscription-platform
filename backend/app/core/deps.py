from fastapi import Depends, HTTPException, status, Request
from sqlalchemy.orm import Session
from datetime import datetime, timezone
from ..database import get_db
from ..models.user import User
from ..models.auth_session import AuthSession
from .security import hash_token

def get_current_user(request: Request, db: Session = Depends(get_db)) -> User:
    """
    Get current user from nv_session HttpOnly cookie
    Rules:
    - inactive users cannot authenticate
    - revoked sessions are invalid
    - expired sessions are invalid
    - users can only access their own auth/session data (enforced in service layer)
    """
    session_token = request.cookies.get("nv_session")
    if not session_token:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Not authenticated - missing session")

    session_hash = hash_token(session_token)
    session = db.query(AuthSession).filter(AuthSession.session_token_hash == session_hash).first()

    if not session:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid session")

    # Check revoked
    if session.revoked_at is not None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Session revoked")

    # Check expired
    now = datetime.now(timezone.utc)
    # Ensure expires_at is timezone aware, if naive assume UTC
    expires_at = session.expires_at
    if expires_at.tzinfo is None:
        expires_at = expires_at.replace(tzinfo=timezone.utc)
    if now > expires_at:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Session expired")

    # Update last_used_at (best effort, not critical)
    try:
        session.last_used_at = now
        db.commit()
    except:
        db.rollback()

    # Get user
    user = db.query(User).filter(User.id == session.user_id).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="User not found")

    if not user.is_active:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Inactive user")

    # Attach session to request state for later use (e.g., logout, refresh needs session)
    request.state.auth_session = session
    request.state.current_user = user

    return user

def require_admin(current_user: User = Depends(get_current_user)) -> User:
    """
    Admin-only dependency must check role == "admin"
    Do not create broad admin business endpoints in this PR - this is helper only
    """
    if current_user.role != "admin":
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Admin access required")
    return current_user
