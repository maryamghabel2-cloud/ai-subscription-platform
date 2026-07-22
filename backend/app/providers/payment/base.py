"""
Abstract PaymentProvider class
"""
from abc import ABC, abstractmethod
from typing import Dict, Any
from ...models.payment_intent import PaymentIntent

class PaymentProvider(ABC):
    """
    Abstract base for payment providers
    Methods:
    - initiate_payment(payment_intent) -> provider_reference: returns authority/tx_hash/address
    - verify_payment(payment_intent, callback_data) -> bool
    - get_payment_status(provider_reference) -> status string
    """

    @abstractmethod
    def initiate_payment(self, payment_intent: PaymentIntent) -> str:
        """Initiate payment, return provider_reference (authority, tx_hash, or fake for mock)"""
        pass

    @abstractmethod
    def verify_payment(self, payment_intent: PaymentIntent, callback_data: Dict[str, Any]) -> bool:
        """Verify payment callback, return True if verified"""
        pass

    @abstractmethod
    def get_payment_status(self, provider_reference: str) -> str:
        """Get payment status from provider"""
        pass
