"""
CSRF protection: double submit cookie pattern
- CSRF token stored in non-HttpOnly cookie nv_csrf
- Required in X-CSRF-Token header for state-changing authenticated requests
- Server stores hash of CSRF token in auth_sessions.csrf_token_hash and verifies
"""

from fastapi import Request, HTTPException, status

def get_csrf_token_from_cookie(request: Request) -> str:
    """Get CSRF token from cookie nv_csrf"""
    return request.cookies.get("nv_csrf", "")

def get_csrf_token_from_header(request: Request) -> str:
    """Get CSRF token from header X-CSRF-Token"""
    return request.headers.get("X-CSRF-Token", "") or request.headers.get("x-csrf-token", "")

def validate_csrf(request: Request, expected_hash: str, hash_func) -> None:
    """
    Validate CSRF: cookie token and header token must match and match stored hash
    expected_hash is csrf_token_hash stored in DB (hash of raw token)
    hash_func is function to hash raw token (hash_token)
    Raises 403 if invalid
    """
    cookie_token = get_csrf_token_from_cookie(request)
    header_token = get_csrf_token_from_header(request)

    if not cookie_token or not header_token:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="CSRF token missing")

    if cookie_token != header_token:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="CSRF token mismatch")

    # Verify that cookie token hash matches stored hash
    if not expected_hash:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="CSRF session invalid")

    # Hash the provided token and compare with stored hash
    # expected_hash is hash of raw token stored in DB
    provided_hash = hash_func(cookie_token)
    if provided_hash != expected_hash:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="CSRF token invalid")
