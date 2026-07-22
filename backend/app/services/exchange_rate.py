"""
Exchange Rate Service - MVP static rate from settings
DEFAULT_EXCHANGE_RATE = 190600 Toman per USD
Later: real-time rate from Bonbast/Arzbin API, rate caching
"""

from ..config import settings

# Default exchange rate per spec
DEFAULT_EXCHANGE_RATE = 190600

def get_exchange_rate() -> int:
    """
    Return configurable static rate from settings
    For MVP: static rate, later real API
    """
    # Try to get from settings if exists, else default
    rate = getattr(settings, 'EXCHANGE_RATE_TOMAN_PER_USD', DEFAULT_EXCHANGE_RATE)
    # Also try attribute with different name
    if not rate:
        rate = DEFAULT_EXCHANGE_RATE
    return int(rate)

def get_exchange_rate_snapshot() -> int:
    """
    Snapshot current exchange rate for payment intent
    Stores Toman per USD at time of creation
    """
    return get_exchange_rate()
