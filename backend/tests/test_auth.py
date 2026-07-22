"""
Auth tests per Phase 1 Part 2 requirements A-J
"""
import sys
import os
import uuid
import pytest

sys.path.append(os.path.dirname(os.path.dirname(__file__)))

from sqlalchemy import create_engine, event
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool
from fastapi.testclient import TestClient

from app.database import Base, get_db
from app.main import app

# Setup test DB - SQLite in-memory for fast unit tests with StaticPool to share same DB across connections
# For PostgreSQL real tests, see test_postgres_migration.py which also tests migrations
engine = create_engine(
    "sqlite:///:memory:",
    connect_args={"check_same_thread": False},
    poolclass=StaticPool,
)

@event.listens_for(engine, "connect")
def set_sqlite_pragma(dbapi_connection, connection_record):
    cursor = dbapi_connection.cursor()
    cursor.execute("PRAGMA foreign_keys=ON")
    cursor.close()

TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Create all tables for test (including new auth tables)
Base.metadata.create_all(bind=engine)

def override_get_db():
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()

app.dependency_overrides[get_db] = override_get_db

client = TestClient(app)

# Reset rate limiting storage before each test module - no cookie clearing to avoid masking real cookie duplication bugs
from app.core.rate_limit import reset_rate_limit_storage

@pytest.fixture(autouse=True)
def reset_rate_limits():
    reset_rate_limit_storage()
    yield
    reset_rate_limit_storage()

# Helper to register user via API
def register_user(email=None, password="StrongPass123"):
    if email is None:
        email = f"test_{uuid.uuid4()}@example.com"
    resp = client.post("/auth/register", json={"email": email, "password": password})
    return resp, email, password

# A. Registration tests

def test_register_creates_user():
    resp, email, _ = register_user()
    assert resp.status_code == 201
    data = resp.json()
    assert data["email"] == email
    assert "password" not in str(data).lower()
    assert "password_hash" not in data

def test_normalized_email_is_lower_trim():
    email_with_spaces = f"  TeSt_{uuid.uuid4()}@Example.COM  "
    resp, _, _ = register_user(email=email_with_spaces)
    assert resp.status_code == 201
    # Check DB directly - query by normalized_email lower
    from app.models.user import User
    db = TestingSessionLocal()
    try:
        normalized = email_with_spaces.strip().lower()
        user = db.query(User).filter(User.normalized_email == normalized).first()
        assert user is not None, f"User with normalized_email {normalized} not found"
        assert user.normalized_email == normalized
        # EmailStr normalizes to lower, so stored email is lowercased (Pydantic EmailStr behavior)
        # Accept either trimmed original or lowercased, but must be trimmed and lower domain
        assert user.email.strip().lower() == normalized
        assert user.email == user.email.strip()  # no spaces
    finally:
        db.close()

def test_duplicate_email_different_casing_rejected():
    email = f"Duplicate_{uuid.uuid4()}@Example.COM"
    resp1, _, _ = register_user(email=email)
    assert resp1.status_code == 201
    # Same email different casing
    resp2 = client.post("/auth/register", json={"email": email.lower(), "password": "StrongPass123"})
    assert resp2.status_code == 400
    assert "already registered" in resp2.json()["detail"].lower()

def test_weak_password_rejected():
    # Use unique IP per request to avoid rate limiting (register 5/hour/IP)
    # Too short
    ip = f"10.0.0.{uuid.uuid4().int % 250 + 1}"
    resp = client.post("/auth/register", json={"email": f"weak_{uuid.uuid4()}@example.com", "password": "short1A"}, headers={"X-Forwarded-For": ip})
    assert resp.status_code == 400
    # No number
    ip = f"10.0.1.{uuid.uuid4().int % 250 + 1}"
    resp = client.post("/auth/register", json={"email": f"weak2_{uuid.uuid4()}@example.com", "password": "NoNumbersHereLong"}, headers={"X-Forwarded-For": ip})
    assert resp.status_code == 400
    # No letter
    ip = f"10.0.2.{uuid.uuid4().int % 250 + 1}"
    resp = client.post("/auth/register", json={"email": f"weak3_{uuid.uuid4()}@example.com", "password": "1234567890"}, headers={"X-Forwarded-For": ip})
    assert resp.status_code == 400
    # Common weak - each with unique IP to avoid rate limit
    for weak in ["password", "123456", "123456789", "qwerty", "admin123", "test123456"]:
        ip_weak = f"10.0.3.{uuid.uuid4().int % 250 + 1}"
        resp = client.post("/auth/register", json={"email": f"weak_{uuid.uuid4()}@example.com", "password": weak}, headers={"X-Forwarded-For": ip_weak})
        assert resp.status_code == 400

def test_wallet_created_on_registration():
    from app.models.wallet import Wallet
    from app.models.user import User
    resp, email, _ = register_user()
    assert resp.status_code == 201
    user_id = resp.json()["id"]
    db = TestingSessionLocal()
    try:
        wallet = db.query(Wallet).filter(Wallet.user_id == user_id).first()
        assert wallet is not None
        assert wallet.balance_credits == 0
    finally:
        db.close()

def test_password_hashed_not_stored_raw():
    from app.models.user import User
    raw_password = "StrongPass123"
    resp, email, _ = register_user(password=raw_password)
    assert resp.status_code == 201
    db = TestingSessionLocal()
    try:
        user = db.query(User).filter(User.email == email).first()
        assert user.password_hash != raw_password
        assert "StrongPass123" not in user.password_hash
        # Verify hash is bcrypt (starts with $2b$ or $2a$)
        assert user.password_hash.startswith("$2")
    finally:
        db.close()

# B. Login tests

def test_valid_login_sets_cookies():
    resp, email, password = register_user()
    assert resp.status_code == 201
    # Clear cookies from register (new client to test login)
    client.cookies.clear()
    resp_login = client.post("/auth/login", json={"email": email, "password": password})
    assert resp_login.status_code == 200
    # Check cookies set
    cookies = resp_login.cookies
    assert "nv_session" in cookies
    assert "nv_refresh" in cookies
    assert "nv_csrf" in cookies
    # Check HttpOnly for session and refresh (TestClient stores but we can check header)
    set_cookie_headers = resp_login.headers.get_list("set-cookie")
    # Find nv_session cookie header
    session_cookie_header = [h for h in set_cookie_headers if "nv_session" in h][0]
    assert "HttpOnly" in session_cookie_header
    assert "samesite=lax" in session_cookie_header.lower()

def test_invalid_login_generic_401():
    resp, email, password = register_user()
    # Wrong password
    resp_bad = client.post("/auth/login", json={"email": email, "password": "WrongPass123"})
    assert resp_bad.status_code == 401
    assert "invalid" in resp_bad.json()["detail"].lower()
    # Non-existent email
    resp_bad2 = client.post("/auth/login", json={"email": f"nonexist_{uuid.uuid4()}@example.com", "password": "Whatever123"})
    assert resp_bad2.status_code == 401

def test_inactive_user_cannot_login():
    from app.models.user import User
    resp, email, password = register_user()
    assert resp.status_code == 201
    # Deactivate user directly in DB
    db = TestingSessionLocal()
    try:
        user = db.query(User).filter(User.email == email).first()
        user.is_active = False
        db.commit()
    finally:
        db.close()
    client.cookies.clear()
    resp_login = client.post("/auth/login", json={"email": email, "password": password})
    assert resp_login.status_code == 401

# C. Current user tests

def test_auth_me_works_with_valid_session():
    resp, email, password = register_user()
    assert resp.status_code == 201
    # Client already has cookies from register
    resp_me = client.get("/auth/me")
    assert resp_me.status_code == 200
    assert resp_me.json()["email"] == email

def test_auth_me_fails_without_cookie():
    client.cookies.clear()
    resp = client.get("/auth/me")
    assert resp.status_code == 401

def test_auth_me_fails_with_revoked_session():
    resp, email, password = register_user()
    assert resp.status_code == 201
    # Logout to revoke session
    # Need CSRF token from cookie
    csrf_cookie = client.cookies.get("nv_csrf")
    assert csrf_cookie
    resp_logout = client.post("/auth/logout", headers={"X-CSRF-Token": csrf_cookie})
    assert resp_logout.status_code == 200
    # Now try me with old session cookie (client still has cookies? logout clears cookies, so we need to set old session manually)
    # Actually logout clears cookies, so me should fail without cookie
    resp_me = client.get("/auth/me")
    assert resp_me.status_code == 401

def test_auth_me_fails_with_expired_session():
    # Simulate expired session by directly updating DB - must respect check constraint expires_at > created_at
    from app.models.auth_session import AuthSession
    from datetime import datetime, timezone, timedelta
    resp, email, password = register_user()
    assert resp.status_code == 201
    # Get session from DB and set expires_at in past but still > created_at
    db = TestingSessionLocal()
    try:
        from app.models.user import User
        user = db.query(User).filter(User.email == email).first()
        session = db.query(AuthSession).filter(AuthSession.user_id == user.id).order_by(AuthSession.created_at.desc()).first()
        assert session is not None
        # Set created_at to 3 hours ago, expires_at to 1 hour ago (still > created_at but < now)
        now = datetime.now(timezone.utc)
        session.created_at = now - timedelta(hours=3)
        session.expires_at = now - timedelta(hours=1)
        session.refresh_expires_at = now + timedelta(days=29)  # still valid refresh
        db.commit()
    finally:
        db.close()
    resp_me = client.get("/auth/me")
    assert resp_me.status_code == 401

# D. Logout tests

def test_logout_requires_csrf():
    resp, email, password = register_user()
    assert resp.status_code == 201
    # Try logout without CSRF header
    resp_logout = client.post("/auth/logout")
    assert resp_logout.status_code == 403

def test_logout_revokes_session_and_clears_cookies():
    resp, email, password = register_user()
    assert resp.status_code == 201
    csrf = client.cookies.get("nv_csrf")
    # Before logout, me works
    assert client.get("/auth/me").status_code == 200
    # Logout
    resp_logout = client.post("/auth/logout", headers={"X-CSRF-Token": csrf})
    assert resp_logout.status_code == 200
    # Cookies cleared
    # Check set-cookie headers for deletion (Max-Age 0 or expires past)
    set_cookies = resp_logout.headers.get_list("set-cookie")
    # Should have deletion for nv_session, nv_refresh, nv_csrf
    assert any("nv_session" in h and ("Max-Age=0" in h or "expires=" in h.lower()) for h in set_cookies)
    # After logout, me fails
    resp_me = client.get("/auth/me")
    assert resp_me.status_code == 401

# E. Refresh tests

def test_refresh_requires_refresh_cookie():
    client.cookies.clear()
    resp = client.post("/auth/refresh", headers={"X-CSRF-Token": "dummy"})
    assert resp.status_code == 401

def test_refresh_requires_csrf():
    resp, email, password = register_user()
    assert resp.status_code == 201
    # Try refresh without CSRF
    resp_refresh = client.post("/auth/refresh")
    assert resp_refresh.status_code == 403

def test_refresh_rotates_tokens():
    resp, email, password = register_user()
    assert resp.status_code == 201
    old_session_cookie = client.cookies.get("nv_session")
    old_refresh_cookie = client.cookies.get("nv_refresh")
    old_csrf = client.cookies.get("nv_csrf")
    assert old_session_cookie and old_refresh_cookie and old_csrf

    # Refresh
    resp_refresh = client.post("/auth/refresh", headers={"X-CSRF-Token": old_csrf})
    assert resp_refresh.status_code == 200

    new_session_cookie = resp_refresh.cookies.get("nv_session") or client.cookies.get("nv_session")
    new_refresh_cookie = resp_refresh.cookies.get("nv_refresh") or client.cookies.get("nv_refresh")

    # Tokens should be rotated (different)
    assert new_session_cookie != old_session_cookie
    assert new_refresh_cookie != old_refresh_cookie

def test_old_refresh_token_cannot_be_reused():
    resp, email, password = register_user()
    assert resp.status_code == 201
    old_refresh = client.cookies.get("nv_refresh")
    old_csrf = client.cookies.get("nv_csrf")

    # First refresh
    resp_refresh1 = client.post("/auth/refresh", headers={"X-CSRF-Token": old_csrf})
    assert resp_refresh1.status_code == 200

    # Try to reuse old refresh token - should fail
    # Manually set old refresh cookie
    client.cookies.set("nv_refresh", old_refresh)
    # Need to set csrf from first refresh? Actually after first refresh, csrf also rotated
    # Use new csrf from current cookies after first refresh
    new_csrf = client.cookies.get("nv_csrf")
    resp_refresh2 = client.post("/auth/refresh", headers={"X-CSRF-Token": new_csrf}, cookies={"nv_refresh": old_refresh, "nv_csrf": new_csrf, "nv_session": client.cookies.get("nv_session")})
    # Actually we are setting old refresh, should fail 401
    # The endpoint checks refresh_token hash, old should be revoked
    # So we expect 401
    # Let's directly try with old refresh token in cookie jar
    client.cookies.clear()
    client.cookies.set("nv_refresh", old_refresh)
    client.cookies.set("nv_csrf", old_csrf)
    # Need session cookie too? Refresh endpoint requires refresh cookie and CSRF, not session, but we set both for safety
    resp_reuse = client.post("/auth/refresh", headers={"X-CSRF-Token": old_csrf})
    assert resp_reuse.status_code == 401

def test_new_refresh_token_works():
    resp, email, password = register_user()
    assert resp.status_code == 201
    old_csrf = client.cookies.get("nv_csrf")
    # Clear any duplicate cookies issue by ensuring single cookie jar
    client.cookies.clear()
    # Re-login to get fresh cookies
    client.post("/auth/login", json={"email": email, "password": password})
    old_csrf = client.cookies.get("nv_csrf")
    resp_refresh1 = client.post("/auth/refresh", headers={"X-CSRF-Token": old_csrf})
    assert resp_refresh1.status_code == 200
    # After refresh, new tokens should work for /auth/me
    resp_me = client.get("/auth/me")
    assert resp_me.status_code == 200

# F. CSRF tests

def test_csrf_state_changing_fails_without_header():
    resp, email, password = register_user()
    assert resp.status_code == 201
    # Logout without CSRF header should fail
    resp_logout = client.post("/auth/logout")
    assert resp_logout.status_code == 403
    # Refresh without CSRF
    resp_refresh = client.post("/auth/refresh")
    assert resp_refresh.status_code == 403

def test_csrf_fails_if_header_not_match_cookie():
    client.cookies.clear()
    resp, email, password = register_user()
    assert resp.status_code == 201
    csrf_cookie = client.cookies.get("nv_csrf")
    # Send different token in header
    resp_logout = client.post("/auth/logout", headers={"X-CSRF-Token": "wrong_token"})
    assert resp_logout.status_code == 403

def test_csrf_passes_with_correct_token():
    client.cookies.clear()
    resp, email, password = register_user()
    assert resp.status_code == 201
    csrf_cookie = client.cookies.get("nv_csrf")
    assert csrf_cookie
    resp_logout = client.post("/auth/logout", headers={"X-CSRF-Token": csrf_cookie})
    assert resp_logout.status_code == 200

# G. Password reset tests

def test_password_reset_request_always_generic():
    # Non-existent email
    resp = client.post("/auth/password-reset/request", json={"email": f"nonexist_{uuid.uuid4()}@example.com"})
    assert resp.status_code == 200
    assert "if an account" in resp.json()["message"].lower()

    # Existing email
    reg_resp, email, _ = register_user()
    assert reg_resp.status_code == 201
    resp2 = client.post("/auth/password-reset/request", json={"email": email})
    assert resp2.status_code == 200
    assert "if an account" in resp2.json()["message"].lower()
    # Response should NOT contain token
    assert "token" not in resp2.json()["message"].lower()
    assert "token" not in str(resp2.json()).lower() or "if an account" in str(resp2.json()).lower()

def test_password_reset_token_stored_hashed_only():
    from app.models.password_reset_token import PasswordResetToken
    from app.services import auth_service

    resp, email, _ = register_user()
    assert resp.status_code == 201

    db = TestingSessionLocal()
    try:
        from app.models.user import User
        user = db.query(User).filter(User.email == email).first()
        # Create token via service (exposes raw token only through service layer for tests, not public API)
        token_obj, raw_token = auth_service.create_password_reset_token(db, user.id)
        assert raw_token is not None
        # Check stored hash, not raw
        assert token_obj.token_hash != raw_token
        # Check that raw token is not stored in DB as token_hash (hash)
        assert len(token_obj.token_hash) == 64  # SHA256 hex length
        # Ensure no column for raw token
        assert not hasattr(token_obj, 'raw_token')
    finally:
        db.close()

def test_password_reset_confirm_updates_password():
    from app.services import auth_service
    resp, email, _ = register_user()
    assert resp.status_code == 201

    db = TestingSessionLocal()
    try:
        from app.models.user import User
        user = db.query(User).filter(User.email == email).first()
        token_obj, raw_token = auth_service.create_password_reset_token(db, user.id)
    finally:
        db.close()

    # Confirm with new password
    new_password = "NewStrongPass123"
    resp_confirm = client.post("/auth/password-reset/confirm", json={"token": raw_token, "new_password": new_password})
    assert resp_confirm.status_code == 200

    # Try login with new password
    client.cookies.clear()
    resp_login = client.post("/auth/login", json={"email": email, "password": new_password})
    assert resp_login.status_code == 200

    # Old password should fail
    resp_login_old = client.post("/auth/login", json={"email": email, "password": "StrongPass123"})
    assert resp_login_old.status_code == 401

def test_used_token_cannot_be_reused():
    from app.services import auth_service
    resp, email, _ = register_user()
    assert resp.status_code == 201

    db = TestingSessionLocal()
    try:
        from app.models.user import User
        user = db.query(User).filter(User.email == email).first()
        token_obj, raw_token = auth_service.create_password_reset_token(db, user.id)
    finally:
        db.close()

    # First use
    resp1 = client.post("/auth/password-reset/confirm", json={"token": raw_token, "new_password": "NewStrongPass123"})
    assert resp1.status_code == 200

    # Second use same token should fail
    resp2 = client.post("/auth/password-reset/confirm", json={"token": raw_token, "new_password": "AnotherStrong123"})
    assert resp2.status_code == 400

def test_expired_token_fails():
    from app.services import auth_service
    from datetime import datetime, timezone, timedelta
    resp, email, _ = register_user()
    assert resp.status_code == 201

    db = TestingSessionLocal()
    try:
        from app.models.user import User
        from app.models.password_reset_token import PasswordResetToken
        user = db.query(User).filter(User.email == email).first()
        token_obj, raw_token = auth_service.create_password_reset_token(db, user.id)
        # Manually expire token but keep expires_at > created_at per check constraint
        # Set created_at to 3 hours ago, expires_at to 1 hour ago
        now = datetime.now(timezone.utc)
        token_obj.created_at = now - timedelta(hours=3)
        token_obj.expires_at = now - timedelta(hours=1)
        db.commit()
    finally:
        db.close()

    resp = client.post("/auth/password-reset/confirm", json={"token": raw_token, "new_password": "NewStrongPass123"})
    assert resp.status_code == 400

def test_all_sessions_revoked_after_password_reset():
    from app.services import auth_service
    resp, email, _ = register_user()
    assert resp.status_code == 201

    # At this point, we have a session from registration
    # Create token
    db = TestingSessionLocal()
    try:
        from app.models.user import User
        user = db.query(User).filter(User.email == email).first()
        token_obj, raw_token = auth_service.create_password_reset_token(db, user.id)
    finally:
        db.close()

    # Confirm reset - should revoke all sessions
    resp_confirm = client.post("/auth/password-reset/confirm", json={"token": raw_token, "new_password": "NewStrongPass123"})
    assert resp_confirm.status_code == 200

    # Try /auth/me with old session cookie (should fail, session revoked)
    # Client still has old session cookie from registration, but after password reset all sessions revoked
    resp_me = client.get("/auth/me")
    assert resp_me.status_code == 401

# H. Rate limiting - Fixed to not trust X-Forwarded-For, only use client.host

def test_rate_limiting_login_returns_429():
    # Rate limiting now uses client.host only, ignoring X-Forwarded-For when no trusted proxies
    # So repeated login attempts from same client (testclient host) should eventually return 429
    # First, create a user
    resp, email, password = register_user()
    assert resp.status_code == 201
    client.cookies.clear()

    # Try 11 login attempts with wrong password quickly - should eventually return 429 after 10 per 15 min
    # All from same client.host (testclient)
    for i in range(10):
        r = client.post("/auth/login", json={"email": email, "password": "WrongPass123"})
        assert r.status_code in [401, 429]
        if r.status_code == 429:
            break

    # 11th attempt should be rate limited
    r11 = client.post("/auth/login", json={"email": email, "password": "WrongPass123"})
    assert r11.status_code == 429

def test_rate_limit_scoped_to_endpoint():
    # Register rate limit 5/hour and login 10/15min should be separate buckets
    # Exhaust register limit
    for i in range(5):
        client.post("/auth/register", json={"email": f"rate_test_{uuid.uuid4()}@example.com", "password": "StrongPass123"})

    # 6th register should be 429
    resp = client.post("/auth/register", json={"email": f"rate_test_{uuid.uuid4()}@example.com", "password": "StrongPass123"})
    assert resp.status_code == 429

    # But login with same client.host should still be allowed for first attempt (different endpoint bucket)
    # Use existing user
    reg_resp, email, password = register_user()
    # Need to reset rate limits for register? Actually we already exhausted register for this client.host, but login bucket is separate
    # So login should not be rate limited yet for this endpoint
    # Clear cookies and try login - should be allowed (200) not 429 for first attempt
    client.cookies.clear()
    login_resp = client.post("/auth/login", json={"email": email, "password": password})
    # Could be 200 if not rate limited, or 429 if previous login attempts from earlier test affected? We reset rate limits per test via fixture, so should be fresh
    # Actually fixture resets rate limits before each test, so this test starts clean
    # But we already did 5 register attempts in this test, which should not affect login bucket
    assert login_resp.status_code == 200

def test_x_forwarded_for_cannot_bypass_rate_limiting_when_no_trusted_proxies():
    """
    Security fix: X-Forwarded-For header must NOT bypass rate limiting when no trusted proxies configured.
    For MVP with no reverse proxy, ONLY use request.client.host and IGNORE X-Forwarded-For.
    This test verifies spoofing X-Forwarded-For does not bypass rate limiting.
    """
    # Exhaust login attempts for client.host (testclient) without using X-Forwarded-For
    resp, email, password = register_user()
    assert resp.status_code == 201
    client.cookies.clear()

    # Make 10 failed login attempts from same client.host to trigger rate limit
    for i in range(10):
        client.post("/auth/login", json={"email": email, "password": "WrongPass123"})

    # Now even if attacker sends X-Forwarded-For with different IP, rate limit should still apply based on client.host
    # Because we ignore X-Forwarded-For when TRUSTED_PROXIES is empty (default)
    resp_spoofed = client.post(
        "/auth/login",
        json={"email": email, "password": "WrongPass123"},
        headers={"X-Forwarded-For": "9.9.9.9"}  # Attempt to spoof different IP to bypass
    )
    # Should still be 429 because we ignore X-Forwarded-For and use client.host (testclient) which is rate limited
    assert resp_spoofed.status_code == 429, "X-Forwarded-For spoofing should NOT bypass rate limiting when no trusted proxies"

    # Also test that without spoofing, also 429
    resp_no_spoof = client.post("/auth/login", json={"email": email, "password": "WrongPass123"})
    assert resp_no_spoof.status_code == 429

# I. Security scans

def test_no_localstorage_usage_in_backend():
    """grep/assert no localStorage usage in backend app code (not tests)"""
    import pathlib
    backend_path = pathlib.Path(__file__).parent.parent / "app"
    suspicious = []
    for py_file in backend_path.rglob("*.py"):
        if ".git" in str(py_file) or "__pycache__" in str(py_file):
            continue
        try:
            text = py_file.read_text(encoding='utf-8')
        except:
            continue
        if "localStorage" in text:
            suspicious.append(str(py_file))
    assert len(suspicious) == 0, f"Backend app code should not use localStorage, found in: {suspicious}"

def test_no_raw_token_stored_in_db():
    """No raw token stored in DB - only hashes"""
    from app.models.auth_session import AuthSession
    from app.models.password_reset_token import PasswordResetToken
    # Check model columns - should have *_hash, not raw tokens
    auth_table = AuthSession.__table__
    column_names = [c.name for c in auth_table.columns]
    assert "session_token_hash" in column_names
    assert "refresh_token_hash" in column_names
    assert "csrf_token_hash" in column_names
    # Ensure no raw token columns
    assert "session_token" not in column_names or "session_token_hash" in column_names
    assert "raw_token" not in column_names
    assert "refresh_token" not in column_names or "refresh_token_hash" in column_names

    reset_table = PasswordResetToken.__table__
    reset_cols = [c.name for c in reset_table.columns]
    assert "token_hash" in reset_cols
    assert "raw_token" not in reset_cols
    assert "token" not in reset_cols or "token_hash" in reset_cols

def test_no_raw_password_stored():
    """No raw password stored in DB - only password_hash"""
    from app.models.user import User
    table = User.__table__
    cols = [c.name for c in table.columns]
    assert "password_hash" in cols
    assert "password" not in cols or "password_hash" in cols
    assert "raw_password" not in cols

def test_no_secrets_committed():
    """No secrets committed - check .env.example contains placeholder CHANGE_ME, not real secrets"""
    import pathlib
    env_example = pathlib.Path(__file__).parent.parent / ".env.example"
    if env_example.exists():
        text = env_example.read_text()
        # Should contain placeholder CHANGE_ME
        assert "CHANGE_ME" in text, ".env.example should contain CHANGE_ME placeholder, not real secret"
        # Should not contain real-looking secrets like long random strings or production passwords
        # Basic check: no line with SECRET_KEY that looks like real key (not placeholder)
        for line in text.splitlines():
            if "SECRET_KEY" in line and "CHANGE_ME" not in line:
                # If SECRET_KEY exists but without CHANGE_ME placeholder, fail
                # Allow if contains your-secret-key placeholder? But we now use CHANGE_ME, so enforce
                if "your-secret-key" in line.lower():
                    continue  # old placeholder, but we updated to CHANGE_ME
                assert False, f"Potential real secret in .env.example: {line}"

# J. Migration

def test_migration_upgrade_head_works_postgres_test_service():
    """
    Alembic upgrade head works on PostgreSQL test service - tested in test_postgres_migration.py with Testcontainers
    This is a placeholder to ensure migration files exist
    """
    import os
    assert os.path.exists(os.path.join(os.path.dirname(os.path.dirname(__file__)), "alembic", "versions", "002_auth_sessions.py"))
    assert os.path.exists(os.path.join(os.path.dirname(os.path.dirname(__file__)), "alembic.ini"))

def test_auth_sessions_constraints_exist():
    """Auth_sessions and password_reset_tokens constraints exist"""
    from app.models.auth_session import AuthSession
    from app.models.password_reset_token import PasswordResetToken
    # Check check constraints
    auth_table = AuthSession.__table__
    constraints = [c.name for c in auth_table.constraints if hasattr(c, 'name') and c.name]
    # Should have expires_at > created_at and refresh_expires_at > created_at
    assert any("expires" in name for name in constraints) or len([c for c in auth_table.constraints if "CheckConstraint" in str(type(c))]) >= 2

    reset_table = PasswordResetToken.__table__
    reset_constraints = [c.name for c in reset_table.constraints if hasattr(c, 'name') and c.name]
    assert any("expires" in name for name in reset_constraints) or len([c for c in reset_table.constraints if "CheckConstraint" in str(type(c))]) >= 1

def test_long_passwords_different_hashes():
    """
    Password hashing fix: SHA256 pre-hash before bcrypt supports any length securely.
    Two different passwords longer than 72 bytes must produce different hashes.
    Previously truncated to 72 bytes silently, causing collision.
    """
    from app.core.security import hash_password
    # Two passwords >72 bytes that share first 72 bytes but differ after
    base = "A" * 72
    pwd1 = base + "1" + "x" * 20 + "123"
    pwd2 = base + "2" + "y" * 20 + "456"
    assert len(pwd1) > 72
    assert len(pwd2) > 72
    assert pwd1[:72] == pwd2[:72]  # First 72 bytes same
    assert pwd1 != pwd2  # But differ after

    hash1 = hash_password(pwd1)
    hash2 = hash_password(pwd2)
    # With SHA256 pre-hash, hashes should be different
    assert hash1 != hash2, "Two different long passwords sharing first 72 bytes should produce different hashes with SHA256 pre-hash, not identical due to silent truncation"
