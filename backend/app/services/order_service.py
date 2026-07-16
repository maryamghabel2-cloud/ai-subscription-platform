"""
Order Service
- Manages order-related business logic
- Handles order processing and fulfillment
"""

import logging
from typing import Optional, Dict, Any, List
from datetime import datetime
from sqlalchemy.orm import Session
import json

from app.database import get_db
from app.models.models import Order, User, Product, SharedAccount, UserSharedAccount
from app.agents.pricing_agent import pricing_agent
from app.agents.procurement_agent import procurement_agent
from app.agents.delivery_agent import delivery_agent
from app.utils.crypto_utils import crypto_utils
from app.utils.exchange_rate import exchange_rate_fetcher

logger = logging.getLogger(__name__)


class OrderService:
    """
    Service for managing orders and their lifecycle
    """
    
    def __init__(self):
        self.pricing_agent = pricing_agent
        self.procurement_agent = procurement_agent
        self.delivery_agent = delivery_agent
        self.crypto_utils = crypto_utils
        self.exchange_rate_fetcher = exchange_rate_fetcher
    
    def create_order(
        self,
        db: Session,
        user_id: Optional[int],
        product_id: int,
        quantity: int = 1,
        payment_method: str = "crypto"
    ) -> Optional[Order]:
        """Create a new order"""
        try:
            # Get product
            product = db.query(Product).filter(Product.id == product_id).first()
            if not product or not product.is_active:
                logger.error(f"Product {product_id} not found or inactive")
                return None
            
            # Calculate price
            price_data = self.pricing_agent.calculate_final_price(product.name)
            
            # Get exchange rate
            exchange_rate = self.exchange_rate_fetcher.get_usdt_rate()
            
            # Calculate prices
            unit_price_tomans = price_data['final_price']
            total_price_tomans = unit_price_tomans * quantity
            
            # Generate order number
            order_number = f"ORD-{datetime.now().strftime('%Y%m%d%H%M%S')}-{os.urandom(4).hex()}"
            
            # Create order
            order = Order(
                order_number=order_number,
                user_id=user_id,
                product_id=product_id,
                quantity=quantity,
                unit_price_dollar=product.base_price_dollar,
                unit_price_tomans=unit_price_tomans,
                total_price_tomans=total_price_tomans,
                exchange_rate=exchange_rate,
                status="pending",
                payment_method=payment_method
            )
            db.add(order)
            db.commit()
            db.refresh(order)
            
            # Generate payment info if crypto
            if payment_method == "crypto":
                payment_address = self.crypto_utils.generate_payment_address(order.id)
                payment_amount_crypto = self.crypto_utils.convert_to_crypto(
                    total_price_tomans,
                    exchange_rate,
                    "USDT"
                )
                
                order.payment_address = payment_address
                order.payment_amount_crypto = payment_amount_crypto
                order.payment_crypto_currency = "USDT"
                db.commit()
            
            return order
            
        except Exception as e:
            logger.error(f"Error creating order: {e}")
            db.rollback()
            return None
    
    def get_order(self, db: Session, order_id: int) -> Optional[Order]:
        """Get order by ID"""
        try:
            return db.query(Order).filter(Order.id == order_id).first()
        except Exception as e:
            logger.error(f"Error getting order {order_id}: {e}")
            return None
    
    def get_orders_by_user(self, db: Session, user_id: int) -> List[Order]:
        """Get all orders for a user"""
        try:
            return db.query(Order).filter(
                Order.user_id == user_id
            ).order_by(Order.created_at.desc()).all()
        except Exception as e:
            logger.error(f"Error getting orders for user {user_id}: {e}")
            return []
    
    def get_all_orders(self, db: Session, status: Optional[str] = None) -> List[Order]:
        """Get all orders, optionally filtered by status"""
        try:
            query = db.query(Order)
            if status:
                query = query.filter(Order.status == status)
            return query.order_by(Order.created_at.desc()).all()
        except Exception as e:
            logger.error(f"Error getting all orders: {e}")
            return []
    
    def update_order_status(
        self,
        db: Session,
        order_id: int,
        status: str,
        **kwargs
    ) -> Optional[Order]:
        """Update order status"""
        try:
            order = db.query(Order).filter(Order.id == order_id).first()
            if not order:
                return None
            
            order.status = status
            
            for key, value in kwargs.items():
                if hasattr(order, key):
                    setattr(order, key, value)
            
            order.updated_at = datetime.now()
            db.commit()
            db.refresh(order)
            return order
        except Exception as e:
            logger.error(f"Error updating order {order_id} status: {e}")
            db.rollback()
            return None
    
    def process_order(self, order_id: int) -> bool:
        """
        Process an order (buy from supplier and deliver to customer)
        :return: True if successful
        """
        db = next(get_db())
        
        try:
            order = db.query(Order).filter(Order.id == order_id).first()
            if not order:
                logger.error(f"Order {order_id} not found")
                return False
            
            if order.status != "paid":
                logger.warning(f"Order {order_id} is not paid")
                return False
            
            # Process with Procurement Agent
            success = self.procurement_agent.process_order(order_id)
            
            if success:
                # Deliver with Delivery Agent
                self.delivery_agent.deliver_order(order_id)
                return True
            else:
                self.update_order_status(db, order_id, "procurement_failed")
                return False
                
        except Exception as e:
            logger.error(f"Error processing order {order_id}: {e}")
            return False
    
    def confirm_payment(
        self,
        db: Session,
        order_id: int,
        tx_hash: str
    ) -> bool:
        """
        Confirm crypto payment and process order
        :return: True if payment is valid and order processed
        """
        try:
            order = db.query(Order).filter(Order.id == order_id).first()
            if not order:
                logger.error(f"Order {order_id} not found")
                return False
            
            if order.status != "pending":
                logger.warning(f"Order {order_id} is not pending")
                return False
            
            # Verify payment (in production, verify with blockchain API)
            # For demo purposes, we'll assume payment is valid
            is_valid = self.crypto_utils.verify_crypto_payment(
                tx_hash,
                order.payment_amount_crypto,
                order.payment_crypto_currency
            )
            
            if not is_valid:
                logger.error(f"Invalid payment for order {order_id}")
                return False
            
            # Update order status
            order.status = "paid"
            order.payment_tx_hash = tx_hash
            db.commit()
            
            # Process order
            return self.process_order(order_id)
            
        except Exception as e:
            logger.error(f"Error confirming payment for order {order_id}: {e}")
            return False
    
    def get_order_status(self, db: Session, order_id: int) -> Optional[str]:
        """Get order status"""
        try:
            order = db.query(Order).filter(Order.id == order_id).first()
            return order.status if order else None
        except Exception as e:
            logger.error(f"Error getting order status {order_id}: {e}")
            return None
    
    def cancel_order(self, db: Session, order_id: int) -> bool:
        """Cancel an order"""
        try:
            order = db.query(Order).filter(Order.id == order_id).first()
            if not order:
                return False
            
            if order.status not in ["pending", "paid"]:
                return False
            
            order.status = "cancelled"
            db.commit()
            return True
        except Exception as e:
            logger.error(f"Error cancelling order {order_id}: {e}")
            return False
    
    def get_orders_statistics(self, db: Session) -> Dict[str, Any]:
        """Get order statistics"""
        try:
            # Total orders
            total_orders = db.query(Order).count()
            
            # Orders by status
            status_counts = {}
            for status in ["pending", "paid", "processing", "delivered", "failed", "cancelled"]:
                count = db.query(Order).filter(Order.status == status).count()
                status_counts[status] = count
            
            # Total revenue
            total_revenue = db.query(Order).filter(
                Order.status == "delivered"
            ).with_entities(Order.total_price_tomans).all()
            total_revenue = sum([r[0] for r in total_revenue])
            
            # Recent orders
            recent_orders = db.query(Order).order_by(
                Order.created_at.desc()
            ).limit(10).all()
            
            return {
                "total_orders": total_orders,
                "status_counts": status_counts,
                "total_revenue": total_revenue,
                "recent_orders": [
                    {
                        "id": o.id,
                        "order_number": o.order_number,
                        "product_name": o.product.name if o.product else "Unknown",
                        "status": o.status,
                        "total_price": o.total_price_tomans,
                        "created_at": o.created_at
                    } for o in recent_orders
                ]
            }
        except Exception as e:
            logger.error(f"Error getting orders statistics: {e}")
            return {}


order_service = OrderService()
