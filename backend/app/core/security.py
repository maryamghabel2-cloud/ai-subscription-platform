import re
import hashlib
import secrets
from typing import Tuple

import bcrypt

# Common weak passwords list per spec
COMMON_WEAK_PASSWORDS = {
    "password",
    "123456",
    "123456789",
    "qwerty",
    "admin123",
    "test123456",
}

def hash_password(password: str) -> str:
    """Hash password using bcrypt directly (avoid passlib compatibility issues), never log raw password"""
    # bcrypt has 72 bytes limit, truncate to 72 bytes for safety per passlib recommendation
    truncated = password[:72].encode('utf-8')
    hashed = bcrypt.hashpw(truncated, bcrypt.gensalt())
    return hashed.decode('utf-8')

def verify_password(password: str, password_hash: str) -> bool:
    """Verify password against hash, constant time - truncate to 72 bytes"""
    truncated = password[:72].encode('utf-8')
    try:
        return bcrypt.checkpw(truncated, password_hash.encode('utf-8'))
    except Exception:
        return False

def generate_secure_token(length: int = 32) -> str:
    """
    Generate secure random token for session, refresh, csrf, password reset
    Uses secrets.token_urlsafe for URL-safe tokens
    """
    return secrets.token_urlsafe(length)

def hash_token(raw_token: str) -> str:
    """
    Hash token with SHA256 for storage - only hashes stored, never raw tokens
    Raw tokens must never be stored in DB
    """
    return hashlib.sha256(raw_token.encode('utf-8')).hexdigest()

def hash_ip(ip_address: str) -> str:
    """Hash IP address for privacy, not storing raw IP"""
    if not ip_address:
        return ""
    return hashlib.sha256(ip_address.encode('utf-8')).hexdigest()[:64]

def hash_user_agent(user_agent: str) -> str:
    """Hash user agent for privacy"""
    if not user_agent:
        return ""
    return hashlib.sha256(user_agent.encode('utf-8')).hexdigest()[:64]

def normalize_email(email: str) -> str:
    """
    Normalize email: strip and lower
    Registration logic in Part 2 will use this same normalization
    Returns normalized_email
    """
    if not email:
        return ""
    return email.strip().lower()

def validate_password_strength(password: str) -> Tuple[bool, str]:
    """
    Password rules:
    - minimum 10 characters
    - must include at least one letter
    - must include at least one number
    - reject common weak passwords
    Returns (is_valid, error_message)
    """
    if not password:
        return False, "Password is required"

    if len(password) < 10:
        return False, "Password must be at least 10 characters"

    if not re.search(r"[A-Za-z]", password):
        return False, "Password must include at least one letter"

    if not re.search(r"[0-9]", password):
        return False, "Password must include at least one number"

    lowered = password.lower()
    if lowered in COMMON_WEAK_PASSWORDS:
        return False, "Password is too common, choose a stronger one"

    return True, ""
