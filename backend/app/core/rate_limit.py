"""
Simple in-memory rate limiting for MVP.
Document that Redis-backed distributed rate limiting will be added later.

Rate limits per spec:
- register: 5 requests / hour / IP
- login: 10 requests / 15 minutes / IP
- password-reset request: 5 requests / hour / IP
- refresh: 30 requests / hour / session/user

Implementation: in-memory dict with timestamps, not distributed, acceptable for MVP single instance.
Future: Redis with sliding window.
"""

import time
from collections import defaultdict, deque
from typing import Dict, Deque

# In-memory storage: key -> deque of timestamps
# Key format: f"{endpoint}:{identifier}" e.g., "register:1.2.3.4" or "login:1.2.3.4" or "refresh:user_id:session_id"
_storage: Dict[str, Deque[float]] = defaultdict(deque)

# Rate limit configs: endpoint -> (max_requests, window_seconds)
RATE_LIMITS = {
    "register": (5, 3600),  # 5 per hour
    "login": (10, 15 * 60),  # 10 per 15 min
    "password_reset_request": (5, 3600),  # 5 per hour
    "refresh": (30, 3600),  # 30 per hour
}

def _is_rate_limited(key: str, max_requests: int, window_seconds: int) -> bool:
    now = time.time()
    window_start = now - window_seconds
    dq = _storage[key]
    # Remove old timestamps outside window
    while dq and dq[0] < window_start:
        dq.popleft()
    if len(dq) >= max_requests:
        return True
    dq.append(now)
    return False

def check_rate_limit(endpoint: str, identifier: str) -> bool:
    """
    Check if request should be rate limited.
    Returns True if rate limited (should return 429), False if allowed.
    """
    config = RATE_LIMITS.get(endpoint)
    if not config:
        return False
    max_req, window = config
    key = f"{endpoint}:{identifier}"
    return _is_rate_limited(key, max_req, window)

def reset_rate_limit_storage():
    """For tests: clear storage"""
    _storage.clear()

# For documentation: Redis-backed distributed rate limiting will be added later for multi-instance deployments
# See AUTHENTICATION.md
