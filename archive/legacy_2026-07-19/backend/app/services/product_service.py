"""
Product Service
- Manages product-related business logic
- Interacts with external APIs for product information
"""

import logging
from typing import Optional, Dict, Any, List
from datetime import datetime
from sqlalchemy.orm import Session

from app.database import get_db
from app.models.models import Product, CompetitorPrice
from app.agents.pricing_agent import pricing_agent
from app.utils.external_apis import external_api_handler

logger = logging.getLogger(__name__)


class ProductService:
    """
    Service for managing products and their prices
    """
    
    def __init__(self):
        self.pricing_agent = pricing_agent
        self.external_api_handler = external_api_handler
    
    def get_all_products(self, db: Session) -> List[Product]:
        """Get all active products"""
        try:
            return db.query(Product).filter(Product.is_active == True).all()
        except Exception as e:
            logger.error(f"Error getting all products: {e}")
            return []
    
    def get_product_by_id(self, db: Session, product_id: int) -> Optional[Product]:
        """Get product by ID"""
        try:
            return db.query(Product).filter(Product.id == product_id).first()
        except Exception as e:
            logger.error(f"Error getting product {product_id}: {e}")
            return None
    
    def get_product_by_name(self, db: Session, product_name: str) -> Optional[Product]:
        """Get product by name"""
        try:
            return db.query(Product).filter(Product.name == product_name).first()
        except Exception as e:
            logger.error(f"Error getting product {product_name}: {e}")
            return None
    
    def create_product(
        self,
        db: Session,
        name: str,
        description: Optional[str] = None,
        product_type: str = "account",
        category: str = "chat",
        base_price_dollar: float = 0.0,
        supplier: str = "ggsel",
        supplier_product_id: Optional[str] = None,
        image_url: Optional[str] = None,
        is_active: bool = True,
        is_shared: bool = False,
        shared_credits: Optional[int] = None
    ) -> Optional[Product]:
        """Create a new product"""
        try:
            product = Product(
                name=name,
                description=description,
                product_type=product_type,
                category=category,
                base_price_dollar=base_price_dollar,
                supplier=supplier,
                supplier_product_id=supplier_product_id,
                image_url=image_url,
                is_active=is_active,
                is_shared=is_shared,
                shared_credits=shared_credits
            )
            db.add(product)
            db.commit()
            db.refresh(product)
            return product
        except Exception as e:
            logger.error(f"Error creating product: {e}")
            db.rollback()
            return None
    
    def update_product(
        self,
        db: Session,
        product_id: int,
        **kwargs
    ) -> Optional[Product]:
        """Update product information"""
        try:
            product = db.query(Product).filter(Product.id == product_id).first()
            if not product:
                return None
            
            for key, value in kwargs.items():
                if hasattr(product, key):
                    setattr(product, key, value)
            
            product.updated_at = datetime.now()
            db.commit()
            db.refresh(product)
            return product
        except Exception as e:
            logger.error(f"Error updating product {product_id}: {e}")
            db.rollback()
            return None
    
    def get_product_prices(self, product_name: str) -> Dict[str, Any]:
        """Get calculated prices for a product"""
        try:
            return self.pricing_agent.calculate_final_price(product_name)
        except Exception as e:
            logger.error(f"Error calculating prices for {product_name}: {e}")
            return {"error": str(e)}
    
    def get_all_product_prices(self) -> List[Dict[str, Any]]:
        """Get calculated prices for all products"""
        try:
            return self.pricing_agent.calculate_all_prices()
        except Exception as e:
            logger.error(f"Error calculating all prices: {e}")
            return []
    
    def update_product_prices_from_suppliers(self) -> int:
        """
        Update product prices from external suppliers
        :return: Number of products updated
        """
        db = next(get_db())
        updated_count = 0
        
        try:
            # Get all products
            products = db.query(Product).all()
            
            for product in products:
                # Get current price from supplier
                current_price = self.external_api_handler.get_product_price(
                    product.name, 
                    product.supplier
                )
                
                if current_price and current_price != product.base_price_dollar:
                    product.base_price_dollar = current_price
                    product.updated_at = datetime.now()
                    db.commit()
                    updated_count += 1
            
            return updated_count
        except Exception as e:
            logger.error(f"Error updating product prices: {e}")
            db.rollback()
            return 0
    
    def add_competitor_price(
        self,
        db: Session,
        product_id: int,
        competitor_site: str,
        price_tomans: int,
        competitor_url: Optional[str] = None
    ) -> Optional[CompetitorPrice]:
        """Add competitor price for a product"""
        try:
            product = db.query(Product).filter(Product.id == product_id).first()
            if not product:
                return None
            
            competitor_price = CompetitorPrice(
                product_id=product_id,
                competitor_site=competitor_site,
                competitor_url=competitor_url,
                price_tomans=price_tomans
            )
            db.add(competitor_price)
            db.commit()
            db.refresh(competitor_price)
            return competitor_price
        except Exception as e:
            logger.error(f"Error adding competitor price: {e}")
            db.rollback()
            return None
    
    def get_competitor_prices(self, db: Session, product_id: int) -> List[CompetitorPrice]:
        """Get all competitor prices for a product"""
        try:
            return db.query(CompetitorPrice).filter(
                CompetitorPrice.product_id == product_id
            ).all()
        except Exception as e:
            logger.error(f"Error getting competitor prices: {e}")
            return []
    
    def get_products_by_category(self, db: Session, category: str) -> List[Product]:
        """Get products by category"""
        try:
            return db.query(Product).filter(
                Product.category == category,
                Product.is_active == True
            ).all()
        except Exception as e:
            logger.error(f"Error getting products by category {category}: {e}")
            return []
    
    def get_products_by_type(self, db: Session, product_type: str) -> List[Product]:
        """Get products by type"""
        try:
            return db.query(Product).filter(
                Product.product_type == product_type,
                Product.is_active == True
            ).all()
        except Exception as e:
            logger.error(f"Error getting products by type {product_type}: {e}")
            return []


product_service = ProductService()
