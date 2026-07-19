from fastapi import HTTPException, Depends
from typing import Dict, Any, Optional
from app.services.zarinpal_service import ZarinpalService
from app.services.crypto_service import CryptoService
from app.config import settings


class PaymentService:
    """
    Main payment service that coordinates all payment methods
    """
    
    def __init__(self):
        self.zarinpal = ZarinpalService()
        self.crypto = CryptoService()
    
    async def create_payment(self, payment_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Create payment based on payment method
        
        Args:
            payment_data: Dictionary containing payment details
                - amount: Amount in Tomans
                - product_name: Name of the product
                - payment_method: 'zarinpal' or 'crypto'
                - callback_url: URL for payment callback
                - email: User email (optional)
                - mobile: User mobile (optional)
                - order_id: Order ID for tracking (optional)
                
        Returns:
            dict: Payment details for redirecting user
        """
        method = payment_data.get("payment_method", "crypto")
        amount = payment_data["amount"]
        product_name = payment_data["product_name"]
        
        if method == "zarinpal":
            # Convert tomans to rials (1 toman = 10 rials)
            amount_rials = amount * 10
            
            try:
                payment = self.zarinpal.create_payment(
                    amount=amount_rials,
                    description=f"خرید {product_name}",
                    callback_url=payment_data["callback_url"],
                    email=payment_data.get("email"),
                    mobile=payment_data.get("mobile")
                )
                return {
                    **payment,
                    "payment_method": "zarinpal",
                    "amount": amount,
                    "currency": "IRR",
                    "product_name": product_name
                }
            except HTTPException as e:
                raise e
            except Exception as e:
                raise HTTPException(
                    status_code=500,
                    detail=f"Error creating Zarinpal payment: {str(e)}"
                )
        
        elif method == "crypto":
            try:
                payment = await self.crypto.create_crypto_payment(
                    amount_toman=amount,
                    product_name=product_name,
                    order_id=payment_data.get("order_id")
                )
                return {
                    **payment,
                    "payment_method": "crypto",
                    "currency": "USDT",
                    "product_name": product_name
                }
            except HTTPException as e:
                raise e
            except Exception as e:
                raise HTTPException(
                    status_code=500,
                    detail=f"Error creating crypto payment: {str(e)}"
                )
        
        else:
            raise HTTPException(
                status_code=400,
                detail=f"Invalid payment method: {method}. Supported methods: zarinpal, crypto"
            )
    
    async def verify_payment(self, payment_method: str, **kwargs) -> Dict[str, Any]:
        """
        Verify payment based on method
        
        Args:
            payment_method: 'zarinpal' or 'crypto'
            **kwargs: Additional parameters based on method
                - For zarinpal: authority, amount
                - For crypto: payment_id, tx_hash, amount
                
        Returns:
            dict: Verification result
        """
        if payment_method == "zarinpal":
            try:
                authority = kwargs["authority"]
                amount = kwargs["amount"]
                
                result = self.zarinpal.verify_payment(
                    authority=authority,
                    amount=amount * 10  # Convert to rials
                )
                
                if result.get("success"):
                    return {
                        **result,
                        "payment_method": "zarinpal",
                        "verified": True,
                        "message": "Payment verified successfully"
                    }
                else:
                    return {
                        **result,
                        "payment_method": "zarinpal",
                        "verified": False,
                        "message": result.get("message", "Payment verification failed")
                    }
            except HTTPException as e:
                raise e
            except Exception as e:
                raise HTTPException(
                    status_code=500,
                    detail=f"Error verifying Zarinpal payment: {str(e)}"
                )
        
        elif payment_method == "crypto":
            try:
                payment_id = kwargs["payment_id"]
                tx_hash = kwargs["tx_hash"]
                amount = kwargs.get("amount")
                
                result = await self.crypto.verify_crypto_payment(
                    payment_id=payment_id,
                    tx_hash=tx_hash,
                    amount=amount
                )
                
                return {
                    **result,
                    "payment_method": "crypto",
                    "verified": result.get("verified", False),
                    "message": "Payment verified" if result.get("verified") else "Payment verification pending"
                }
            except HTTPException as e:
                raise e
            except Exception as e:
                raise HTTPException(
                    status_code=500,
                    detail=f"Error verifying crypto payment: {str(e)}"
                )
        
        else:
            raise HTTPException(
                status_code=400,
                detail=f"Invalid payment method: {payment_method}"
            )
    
    async def get_payment_status(self, payment_id: str, payment_method: str) -> Dict[str, Any]:
        """
        Get current status of a payment
        
        Args:
            payment_id: Payment identifier
            payment_method: Payment method used
            
        Returns:
            dict: Payment status
        """
        if payment_method == "crypto":
            return self.crypto.get_payment_status(payment_id)
        else:
            # For Zarinpal, we need to check with authority
            # This would need to be stored in database
            return {
                "payment_id": payment_id,
                "payment_method": payment_method,
                "status": "unknown",
                "message": "Payment status tracking not implemented for this method"
            }
    
    def get_supported_methods(self) -> Dict[str, Any]:
        """
        Get list of supported payment methods
        
        Returns:
            dict: Supported payment methods with details
        """
        return {
            "methods": [
                {
                    "id": "crypto",
                    "name": "پرداخت با تتر (USDT)",
                    "description": "پرداخت با ارز دیجیتال تتر (شبکه TRC20)",
                    "currency": "USDT",
                    "is_active": True,
                    "delivery_time": "فوری",
                    "fee": "۰%",
                    "min_amount": 100000,  # 100,000 Tomans
                    "max_amount": None
                },
                {
                    "id": "zarinpal",
                    "name": "زرین‌پال",
                    "description": "پرداخت با کارت بانکی از طریق درگاه زرین‌پال",
                    "currency": "IRR",
                    "is_active": True,
                    "delivery_time": "پس از تایید",
                    "fee": "۰.۹% + ۲۰۰ تومان",
                    "min_amount": 10000,  # 10,000 Tomans
                    "max_amount": 50000000  # 50,000,000 Tomans
                }
            ],
            "default": "crypto"
        }
