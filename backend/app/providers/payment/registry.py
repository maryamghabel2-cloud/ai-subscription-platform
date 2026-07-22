"""
Provider selection via env var PAYMENT_PROVIDER
- sandbox_mock (default)
- zarinpal (future Part 3B)
- crypto_trc20 (future Part 3C)
- crypto_ton
"""

import os
from typing import Dict
from .base import PaymentProvider
from .mock import MockPaymentProvider

# Registry of providers - for now only mock, future will add real providers
_providers: Dict[str, PaymentProvider] = {
    "sandbox_mock": MockPaymentProvider(),
    # Future:
    # "zarinpal": ZarinPalProvider(),
    # "crypto_trc20": CryptoTRC20Provider(),
    # "crypto_ton": CryptoTONProvider(),
}

def get_payment_provider(provider_name: str = None) -> PaymentProvider:
    """
    Get payment provider by name, selected via env var PAYMENT_PROVIDER
    Default: sandbox_mock
    Env var: PAYMENT_PROVIDER=sandbox_mock (default), zarinpal, crypto_trc20, crypto_ton
    """
    if provider_name is None:
        provider_name = os.getenv("PAYMENT_PROVIDER", "sandbox_mock")

    provider = _providers.get(provider_name)
    if not provider:
        # Fallback to mock for unknown
        provider = _providers["sandbox_mock"]

    return provider

def is_sandbox_provider(provider_name: str = None) -> bool:
    """Check if current provider is sandbox_mock"""
    if provider_name is None:
        provider_name = os.getenv("PAYMENT_PROVIDER", "sandbox_mock")
    return provider_name == "sandbox_mock"
