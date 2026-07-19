import hashlib
import time
from typing import Dict, Any
from fastapi import HTTPException
from app.config import settings
from app.utils.exchange_rate import get_usdt_rate


class CryptoService:
    """
    Service for handling cryptocurrency payments (USDT, BTC, ETH, etc.)
    """
    
    def __init__(self):
        self.usdt_address = settings.CRYPTO_PAYMENT_ADDRESS
        self.network = settings.CRYPTO_NETWORK  # TRC20, ERC20, BEP20
    
    async def create_crypto_payment(self, amount_toman: int, product_name: str, order_id: str = None) -> Dict[str, Any]:
        """
        Create crypto payment request
        Returns payment details for user
        
        Args:
            amount_toman: Amount in Iranian Tomans
            product_name: Name of the product being purchased
            order_id: Optional order ID for tracking
            
        Returns:
            dict: Payment details including USDT amount, address, QR code, etc.
        """
        # Get current USDT rate
        try:
            usdt_rate = await get_usdt_rate()
        except Exception as e:
            # Fallback to default rate if API fails
            usdt_rate = 190000
            print(f"Warning: Could not fetch USDT rate, using fallback: {e}")
        
        # Calculate USDT amount
        usdt_amount = round(amount_toman / usdt_rate, 6)
        
        # Generate unique payment ID
        payment_id = self._generate_payment_id(order_id)
        
        # Generate QR code URL
        qrcode_url = self._generate_qrcode_url(payment_id, usdt_amount)
        
        return {
            "payment_id": payment_id,
            "order_id": order_id,
            "usdt_amount": usdt_amount,
            "usdt_address": self.usdt_address,
            "network": self.network,
            "amount_toman": amount_toman,
            "usdt_rate": usdt_rate,
            "product_name": product_name,
            "qrcode_url": qrcode_url,
            "payment_url": f"{self.network}://{self.usdt_address}?amount={usdt_amount}",
            "expires_in": 86400,  # 24 hours in seconds
            "created_at": int(time.time()),
            "status": "pending"
        }
    
    async def verify_crypto_payment(self, payment_id: str, tx_hash: str, amount: float = None) -> Dict[str, Any]:
        """
        Verify crypto payment using blockchain explorer
        
        Args:
            payment_id: Unique payment identifier
            tx_hash: Transaction hash from blockchain
            amount: Expected amount in USDT (optional)
            
        Returns:
            dict: Verification result
        """
        # In production, implement actual blockchain verification
        # For now, return mock verification (replace with real implementation)
        
        # TODO: Implement actual verification for each network:
        # - TRC20: Use TronGrid API (https://trongrid.io/)
        # - ERC20: Use Etherscan API (https://etherscan.io/apis)
        # - BEP20: Use BscScan API (https://bscscan.com/apis)
        
        # For demo purposes, we'll return a successful verification
        # In production, you should:
        # 1. Check if tx_hash exists on the blockchain
        # 2. Verify the amount matches
        # 3. Verify the recipient address matches
        # 4. Check for sufficient confirmations
        
        return {
            "verified": True,  # This should be based on actual blockchain check
            "payment_id": payment_id,
            "tx_hash": tx_hash,
            "amount": amount or 10.0,
            "confirmations": 6,
            "network": self.network,
            "status": "confirmed",
            "verified_at": int(time.time())
        }
    
    def get_payment_status(self, payment_id: str) -> Dict[str, Any]:
        """
        Get current status of a payment
        """
        # In production, check database or blockchain
        return {
            "payment_id": payment_id,
            "status": "pending",  # or "confirmed", "failed", "expired"
            "checked_at": int(time.time())
        }
    
    def _generate_payment_id(self, order_id: str = None) -> str:
        """Generate unique payment ID"""
        timestamp = str(int(time.time()))
        random_str = str(time.time()).split('.')[1][:6]
        base_string = f"{timestamp}{random_str}{settings.SECRET_KEY}"
        if order_id:
            base_string += order_id
        return hashlib.sha256(base_string.encode()).hexdigest()[:16]
    
    def _generate_qrcode_url(self, payment_id: str, amount: float) -> str:
        """Generate QR code URL for payment"""
        # Use a free QR code API
        data = f"{self.network}:{self.usdt_address}?amount={amount}&message=Payment for {payment_id}"
        return f"https://api.qrserver.com/v1/create-qr-code/?size=300x300&data={data}&format=png&bgcolor=FFFFFF&color=000000"
    
    async def check_transaction_on_blockchain(self, tx_hash: str) -> Dict[str, Any]:
        """
        Check transaction details on blockchain (placeholder for actual implementation)
        """
        # This is a placeholder - implement based on your network
        
        if self.network == "TRC20":
            # Use TronGrid API
            api_url = f"https://api.trongrid.io/v1/transactions/{tx_hash}"
            # Add API key if needed
            # response = requests.get(api_url)
            # return response.json()
            pass
        elif self.network == "ERC20":
            # Use Etherscan API
            api_url = f"https://api.etherscan.io/api?module=proxy&action=eth_getTransactionByHash&txhash={tx_hash}"
            # Add API key
            # response = requests.get(api_url)
            # return response.json()
            pass
        elif self.network == "BEP20":
            # Use BscScan API
            api_url = f"https://api.bscscan.com/api?module=proxy&action=eth_getTransactionByHash&txhash={tx_hash}"
            # Add API key
            # response = requests.get(api_url)
            # return response.json()
            pass
        
        # Mock response for now
        return {
            "tx_hash": tx_hash,
            "status": "success",
            "amount": 10.0,
            "to": self.usdt_address,
            "confirmations": 12
        }
