"""
MockPaymentProvider - SANDBOX ONLY - NOT FOR PRODUCTION. Real verification required.

This provider is for testing and development only.
- initiate_payment: returns fake authority/tx_hash
- verify_payment: always returns True (for testing)
- get_payment_status: returns completed

Clearly marked as sandbox only.
"""

from typing import Dict, Any
import uuid
from .base import PaymentProvider
from ...models.payment_intent import PaymentIntent

class MockPaymentProvider(PaymentProvider):
    """
    SANDBOX ONLY — NOT FOR PRODUCTION. Real verification required.
    
    Mock provider for Part 3A wallet/payment tests.
    - initiate_payment returns fake authority/tx_hash
    - verify_payment always True
    - get_payment_status returns completed
    """

    def initiate_payment(self, payment_intent: PaymentIntent) -> str:
        # Return fake authority/tx_hash based on provider
        if payment_intent.provider == "zarinpal":
            return f"mock_authority_{uuid.uuid4().hex[:12]}"
        elif payment_intent.provider in ["crypto_trc20", "crypto_ton"]:
            return f"mock_tx_hash_{uuid.uuid4().hex}"
        else:
            return f"mock_ref_{uuid.uuid4().hex[:16]}"

    def verify_payment(self, payment_intent: PaymentIntent, callback_data: Dict[str, Any]) -> bool:
        # Always True for sandbox testing
        return True

    def get_payment_status(self, provider_reference: str) -> str:
        return "completed"
