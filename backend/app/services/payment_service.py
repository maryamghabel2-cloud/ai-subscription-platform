"""
Payment Service
- Handles payment processing
- Manages crypto payments
"""

import logging
from typing import Optional, Dict, Any
from datetime import datetime
from sqlalchemy.orm import Session

from app.database import get_db
from app.models.models import Order
from app.utils.crypto_utils import crypto_utils
from app.utils.exchange_rate import exchange_rate_fetcher
from app.config import settings

logger = logging.getLogger(__name__)


class PaymentService:
    """
    Service for handling payments
    """
    
    def __init__(self):
        self.crypto_utils = crypto_utils
        self.exchange_rate_fetcher = exchange_rate_fetcher
    
    def generate_payment_address(self, order_id: int) -> str:
        """
        Generate a unique payment address for an order
        :param order_id: Order ID
        :return: Payment address
        """
        try:
            return self.crypto_utils.generate_payment_address(order_id)
        except Exception as e:
            logger.error(f"Error generating payment address for order {order_id}: {e}")
            return ""
    
    def calculate_crypto_amount(
        self,
        amount_tomans: int,
        crypto_currency: str = "USDT"
    ) -> float:
        """
        Calculate crypto amount from tomans
        :param amount_tomans: Amount in tomans
        :param crypto_currency: Crypto currency (USDT, BTC, ETH)
        :return: Amount in crypto
        """
        try:
            exchange_rate = self.exchange_rate_fetcher.get_usdt_rate()
            return self.crypto_utils.convert_to_crypto(
                amount_tomans,
                exchange_rate,
                crypto_currency
            )
        except Exception as e:
            logger.error(f"Error calculating crypto amount: {e}")
            return 0.0
    
    def verify_payment(
        self,
        order_id: int,
        tx_hash: str,
        db: Session
    ) -> bool:
        """
        Verify crypto payment
        :param order_id: Order ID
        :param tx_hash: Transaction hash
        :return: True if payment is valid
        """
        try:
            order = db.query(Order).filter(Order.id == order_id).first()
            if not order:
                logger.error(f"Order {order_id} not found")
                return False
            
            if not order.payment_amount_crypto or not order.payment_crypto_currency:
                logger.error(f"Order {order_id} has no payment info")
                return False
            
            # Verify payment (in production, use blockchain API)
            is_valid = self.crypto_utils.verify_crypto_payment(
                tx_hash,
                order.payment_amount_crypto,
                order.payment_crypto_currency
            )
            
            return is_valid
            
        except Exception as e:
            logger.error(f"Error verifying payment for order {order_id}: {e}")
            return False
    
    def get_payment_info(self, order_id: int, db: Session) -> Optional[Dict[str, Any]]:
        """
        Get payment information for an order
        :param order_id: Order ID
        :return: Payment info dictionary
        """
        try:
            order = db.query(Order).filter(Order.id == order_id).first()
            if not order:
                return None
            
            return {
                "method": order.payment_method,
                "address": order.payment_address,
                "amount_crypto": order.payment_amount_crypto,
                "currency": order.payment_crypto_currency,
                "amount_tomans": order.total_price_tomans,
                "tx_hash": order.payment_tx_hash,
                "status": order.status
            }
        except Exception as e:
            logger.error(f"Error getting payment info for order {order_id}: {e}")
            return None
    
    def get_network_fee(self, network: str = "TRC20") -> float:
        """
        Get network fee for crypto payment
        :param network: Network name (TRC20, BTC, ETH)
        :return: Network fee
        """
        try:
            return self.crypto_utils.get_crypto_network_fee(network)
        except Exception as e:
            logger.error(f"Error getting network fee: {e}")
            return 1.0  # Default fee
    
    def create_payment_link(self, order_id: int, db: Session) -> Optional[str]:
        """
        Create a payment link for an order
        (For future integration with payment gateways)
        :param order_id: Order ID
        :return: Payment link
        """
        try:
            order = db.query(Order).filter(Order.id == order_id).first()
            if not order:
                return None
            
            # For now, just return a placeholder
            # In production, integrate with a payment gateway
            return f"/payment/{order_id}/"
            
        except Exception as e:
            logger.error(f"Error creating payment link for order {order_id}: {e}")
            return None


payment_service = PaymentService()
