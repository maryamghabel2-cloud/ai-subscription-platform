"""
Auth service - handles user creation, session management, password reset
- No real email sending yet
- No real SMS
- No wallet business logic (wallet creation automatic per spec, but no debit/credit)
- No AI provider logic
"""

import uuid
from datetime import datetime, timedelta, timezone
from typing import Optional, Tuple
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError

from ..models.user import User
from ..models.wallet import Wallet
from ..models.auth_session import AuthSession
from ..models.password_reset_token import PasswordResetToken
from ..core.security import (
    hash_password,
    verify_password,
    generate_secure_token,
    hash_token,
    hash_ip,
    hash_user_agent,
    normalize_email,
    validate_password_strength,
)

# For tests: expose token only through service layer, not public API per spec
# In production, password reset token would be sent via email, not returned in API response

def create_user(db: Session, email: str, password: str, role: str = "user") -> User:
    normalized = normalize_email(email)
    
    # Validate password strength
    is_valid, msg = validate_password_strength(password)
    if not is_valid:
        raise ValueError(msg)
    
    # Check duplicate normalized_email
    existing = db.query(User).filter(User.normalized_email == normalized).first()
    if existing:
        raise ValueError("Email already registered")
    
    password_hash = hash_password(password)
    user = User(email=email.strip(), normalized_email=normalized, password_hash=password_hash, role=role, is_active=True)
    db.add(user)
    try:
        db.commit()
    except IntegrityError:
        db.rollback()
        raise ValueError("Email already registered")
    db.refresh(user)
    
    # Create wallet automatically if not already created per spec
    existing_wallet = db.query(Wallet).filter(Wallet.user_id == user.id).first()
    if not existing_wallet:
        wallet = Wallet(user_id=user.id, balance_credits=0)
        db.add(wallet)
        db.commit()
    
    return user

def authenticate_user(db: Session, email: str, password: str) -> Optional[User]:
    normalized = normalize_email(email)
    user = db.query(User).filter(User.normalized_email == normalized).first()
    if not user:
        return None
    if not user.is_active:
        return None
    if not verify_password(password, user.password_hash):
        return None
    return user

def create_auth_session(db: Session, user_id: int, user_agent: str = "", ip_address: str = "") -> Tuple[AuthSession, str, str, str]:
    """
    Create auth session
    Returns: (session_obj, raw_session_token, raw_refresh_token, raw_csrf_token)
    Only hashes stored in DB, never raw tokens
    """
    raw_session = generate_secure_token(32)
    raw_refresh = generate_secure_token(32)
    raw_csrf = generate_secure_token(32)

    session_hash = hash_token(raw_session)
    refresh_hash = hash_token(raw_refresh)
    csrf_hash = hash_token(raw_csrf)

    now = datetime.now(timezone.utc)
    expires_at = now + timedelta(minutes=30)
    refresh_expires_at = now + timedelta(days=30)

    session = AuthSession(
        user_id=user_id,
        session_token_hash=session_hash,
        refresh_token_hash=refresh_hash,
        csrf_token_hash=csrf_hash,
        user_agent_hash=hash_user_agent(user_agent) if user_agent else None,
        ip_hash=hash_ip(ip_address) if ip_address else None,
        created_at=now,
        last_used_at=now,
        expires_at=expires_at,
        refresh_expires_at=refresh_expires_at,
        revoked_at=None,
    )
    db.add(session)
    db.commit()
    db.refresh(session)

    return session, raw_session, raw_refresh, raw_csrf

def revoke_session(db: Session, session: AuthSession):
    session.revoked_at = datetime.now(timezone.utc)
    db.commit()

def refresh_auth_session(db: Session, refresh_token_raw: str, user_agent: str = "", ip_address: str = "") -> Optional[Tuple[AuthSession, str, str, str]]:
    """
    Verifies refresh token hash, rotates session token and refresh token, invalidates old refresh token
    Returns new (session, raw_session, raw_refresh, raw_csrf) or None if invalid
    """
    refresh_hash = hash_token(refresh_token_raw)
    session = db.query(AuthSession).filter(AuthSession.refresh_token_hash == refresh_hash).first()
    if not session:
        return None
    if session.revoked_at is not None:
        return None

    now = datetime.now(timezone.utc)
    refresh_expires_at = session.refresh_expires_at
    if refresh_expires_at.tzinfo is None:
        refresh_expires_at = refresh_expires_at.replace(tzinfo=timezone.utc)
    if now > refresh_expires_at:
        return None

    # Rotate: revoke old session and create new one for same user
    # Actually per spec: rotates session token and refresh token, invalidates old refresh token
    # Implementation: revoke old session
    session.revoked_at = now
    db.commit()

    # Create new session for same user
    return create_auth_session(db, session.user_id, user_agent, ip_address)

def create_password_reset_token(db: Session, user_id: int) -> Tuple[PasswordResetToken, str]:
    """
    Create password reset token - for tests expose token only through service layer, not public API
    Public API always returns generic message
    """
    raw_token = generate_secure_token(32)
    token_hash = hash_token(raw_token)

    now = datetime.now(timezone.utc)
    expires_at = now + timedelta(hours=1)

    # Revoke any existing unused tokens for same user? Optional, but we can keep multiple, but spec says token stored hashed only
    reset_token = PasswordResetToken(
        user_id=user_id,
        token_hash=token_hash,
        created_at=now,
        expires_at=expires_at,
        used_at=None,
    )
    db.add(reset_token)
    db.commit()
    db.refresh(reset_token)

    return reset_token, raw_token

def confirm_password_reset(db: Session, raw_token: str, new_password: str) -> bool:
    """
    Validate token, validate password strength, update password_hash, mark token used, revoke all existing sessions for user
    Returns True if successful
    """
    is_valid, msg = validate_password_strength(new_password)
    if not is_valid:
        raise ValueError(msg)

    token_hash = hash_token(raw_token)
    reset_token = db.query(PasswordResetToken).filter(PasswordResetToken.token_hash == token_hash).first()
    if not reset_token:
        return False
    if reset_token.used_at is not None:
        return False

    now = datetime.now(timezone.utc)
    expires_at = reset_token.expires_at
    if expires_at.tzinfo is None:
        expires_at = expires_at.replace(tzinfo=timezone.utc)
    if now > expires_at:
        return False

    # Update password
    user = db.query(User).filter(User.id == reset_token.user_id).first()
    if not user:
        return False

    user.password_hash = hash_password(new_password)
    reset_token.used_at = now

    # Revoke all existing sessions for that user
    sessions = db.query(AuthSession).filter(AuthSession.user_id == user.id, AuthSession.revoked_at == None).all()
    for s in sessions:
        s.revoked_at = now

    db.commit()
    return True
