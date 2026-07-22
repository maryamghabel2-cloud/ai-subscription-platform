from fastapi import APIRouter, Depends, HTTPException, status, Request, Response
from sqlalchemy.orm import Session
from ..database import get_db
from ..schemas.auth import RegisterRequest, LoginRequest, UserResponse, GenericMessageResponse, PasswordResetRequest, PasswordResetConfirm
from ..services import auth_service
from ..core.deps import get_current_user
from ..core.csrf import validate_csrf
from ..core.rate_limit import check_rate_limit
from ..core.security import hash_token
from ..models.user import User
from ..models.auth_session import AuthSession
from ..config import settings

router = APIRouter(prefix="/auth", tags=["auth"])

def get_client_ip(request: Request) -> str:
    """
    Secure IP extraction - for MVP with no reverse proxy, ONLY use request.client.host and IGNORE X-Forwarded-For.
    Only trust X-Forwarded-For if request comes from a trusted proxy (settings.TRUSTED_PROXIES).
    This prevents X-Forwarded-For spoofing to bypass rate limiting.
    """
    client_host = request.client.host if request.client else ""
    # If trusted proxies configured and client is trusted, then trust X-Forwarded-For
    if settings.TRUSTED_PROXIES and client_host in settings.TRUSTED_PROXIES:
        forwarded = request.headers.get("X-Forwarded-For")
        if forwarded:
            # First IP in list is original client
            return forwarded.split(",")[0].strip()
    # Default: only use direct client host, ignore headers
    return client_host

@router.post("/register", response_model=UserResponse, status_code=201)
def register(request: Request, payload: RegisterRequest, response: Response, db: Session = Depends(get_db)):
    # Rate limiting: 5 per hour per IP - uses secure IP extraction
    ip = get_client_ip(request)
    if check_rate_limit("register", ip):
        raise HTTPException(status_code=429, detail="Too many registration attempts, try later")

    try:
        user = auth_service.create_user(db, payload.email, payload.password)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

    # Create auth session and set cookies
    user_agent = request.headers.get("User-Agent", "")
    session, raw_session, raw_refresh, raw_csrf = auth_service.create_auth_session(db, user.id, user_agent, ip)

    # Clear old cookies explicitly to avoid duplicate cookies
    response.delete_cookie(key="nv_session", path="/")
    response.delete_cookie(key="nv_refresh", path="/")
    response.delete_cookie(key="nv_csrf", path="/")

    # Set cookies per spec
    response.set_cookie(
        key="nv_session",
        value=raw_session,
        httponly=True,
        secure=False,  # Set True in production
        samesite="lax",
        max_age=30*60,
        path="/",
    )
    response.set_cookie(
        key="nv_refresh",
        value=raw_refresh,
        httponly=True,
        secure=False,
        samesite="lax",
        max_age=30*24*3600,
        path="/",
    )
    response.set_cookie(
        key="nv_csrf",
        value=raw_csrf,
        httponly=False,
        secure=False,
        samesite="lax",
        max_age=30*60,
        path="/",
    )

    return user

@router.post("/login", response_model=UserResponse)
def login(request: Request, payload: LoginRequest, response: Response, db: Session = Depends(get_db)):
    ip = get_client_ip(request)
    if check_rate_limit("login", ip):
        raise HTTPException(status_code=429, detail="Too many login attempts, try later")

    user = auth_service.authenticate_user(db, payload.email, payload.password)
    if not user:
        raise HTTPException(status_code=401, detail="Invalid email or password")

    if not user.is_active:
        raise HTTPException(status_code=401, detail="Invalid email or password")

    user_agent = request.headers.get("User-Agent", "")
    session, raw_session, raw_refresh, raw_csrf = auth_service.create_auth_session(db, user.id, user_agent, ip)

    # Clear old cookies explicitly before setting new to avoid duplicates
    response.delete_cookie(key="nv_session", path="/")
    response.delete_cookie(key="nv_refresh", path="/")
    response.delete_cookie(key="nv_csrf", path="/")

    response.set_cookie(key="nv_session", value=raw_session, httponly=True, secure=False, samesite="lax", max_age=30*60, path="/")
    response.set_cookie(key="nv_refresh", value=raw_refresh, httponly=True, secure=False, samesite="lax", max_age=30*24*3600, path="/")
    response.set_cookie(key="nv_csrf", value=raw_csrf, httponly=False, secure=False, samesite="lax", max_age=30*60, path="/")

    return user

@router.post("/logout", response_model=GenericMessageResponse)
def logout(request: Request, response: Response, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    session = getattr(request.state, 'auth_session', None)
    if not session:
        session_token = request.cookies.get("nv_session")
        if session_token:
            session_hash = hash_token(session_token)
            session = db.query(AuthSession).filter(AuthSession.session_token_hash == session_hash).first()

    if session:
        try:
            validate_csrf(request, session.csrf_token_hash, hash_token)
        except HTTPException as e:
            raise e
        auth_service.revoke_session(db, session)

    response.delete_cookie(key="nv_session", path="/")
    response.delete_cookie(key="nv_refresh", path="/")
    response.delete_cookie(key="nv_csrf", path="/")

    return {"message": "Logged out successfully"}

@router.post("/refresh", response_model=UserResponse)
def refresh(request: Request, response: Response, db: Session = Depends(get_db)):
    ip = get_client_ip(request)
    refresh_token = request.cookies.get("nv_refresh")
    if not refresh_token:
        raise HTTPException(status_code=401, detail="Refresh token missing")

    if check_rate_limit("refresh", f"{ip}:{refresh_token[:10]}"):
        raise HTTPException(status_code=429, detail="Too many refresh attempts")

    refresh_hash = hash_token(refresh_token)
    session = db.query(AuthSession).filter(AuthSession.refresh_token_hash == refresh_hash).first()
    if not session:
        raise HTTPException(status_code=401, detail="Invalid refresh token")

    try:
        validate_csrf(request, session.csrf_token_hash, hash_token)
    except HTTPException as e:
        raise e

    user_agent = request.headers.get("User-Agent", "")
    result = auth_service.refresh_auth_session(db, refresh_token, user_agent, ip)
    if not result:
        raise HTTPException(status_code=401, detail="Invalid or expired refresh token")

    new_session, raw_session, raw_refresh, raw_csrf = result

    # Fix: clear old cookies explicitly before setting new ones to avoid duplicate cookies
    response.delete_cookie("nv_csrf", path="/")
    response.delete_cookie("nv_session", path="/")
    response.delete_cookie("nv_refresh", path="/auth/refresh")
    response.delete_cookie("nv_refresh", path="/")

    # Set new cookies (rotated)
    response.set_cookie(key="nv_session", value=raw_session, httponly=True, secure=False, samesite="lax", max_age=30*60, path="/")
    response.set_cookie(key="nv_refresh", value=raw_refresh, httponly=True, secure=False, samesite="lax", max_age=30*24*3600, path="/")
    response.set_cookie(key="nv_csrf", value=raw_csrf, httponly=False, secure=False, samesite="lax", max_age=30*60, path="/")

    user = db.query(User).filter(User.id == new_session.user_id).first()
    return user

@router.get("/me", response_model=UserResponse)
def get_me(current_user: User = Depends(get_current_user)):
    return current_user

@router.post("/password-reset/request", response_model=GenericMessageResponse)
def password_reset_request(request: Request, payload: PasswordResetRequest, db: Session = Depends(get_db)):
    ip = get_client_ip(request)
    if check_rate_limit("password_reset_request", ip):
        raise HTTPException(status_code=429, detail="Too many password reset attempts")

    from ..core.security import normalize_email
    normalized = normalize_email(payload.email)
    user = db.query(User).filter(User.normalized_email == normalized).first()
    if user:
        auth_service.create_password_reset_token(db, user.id)

    return {"message": "If an account with that email exists, a password reset link has been created."}

@router.post("/password-reset/confirm", response_model=GenericMessageResponse)
def password_reset_confirm(payload: PasswordResetConfirm, db: Session = Depends(get_db)):
    try:
        success = auth_service.confirm_password_reset(db, payload.token, payload.new_password)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

    if not success:
        raise HTTPException(status_code=400, detail="Invalid or expired token")

    return {"message": "Password has been reset successfully"}
