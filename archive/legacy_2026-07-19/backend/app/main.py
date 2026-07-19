"""
FastAPI Application for AI Subscription Platform
Main entry point for the backend server
"""

from fastapi import FastAPI, Depends, HTTPException, Request, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse, RedirectResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session
from typing import Optional, List
import logging
import os
from datetime import datetime

from app.config import settings
from app.database import get_db, Base, engine
from app.models.models import (
    Product, CompetitorPrice, ExchangeRate, User, Order, 
    SharedAccount, UserSharedAccount, ProcurementLog
)
from app.schemas.schemas import (
    ProductInDB, CompetitorPriceInDB, ExchangeRateInDB, 
    UserInDB, OrderInDB, PriceCalculationRequest, 
    PriceCalculationResponse, HealthCheckResponse
)
from app.agents.pricing_agent import pricing_agent
from app.agents.procurement_agent import procurement_agent
from app.agents.delivery_agent import delivery_agent
from app.utils.exchange_rate import exchange_rate_fetcher
from app.utils.crypto_utils import crypto_utils
from app.utils.external_apis import external_api_handler

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Create database tables
try:
    Base.metadata.create_all(bind=engine)
    logger.info("Database tables created successfully")
except Exception as e:
    logger.error(f"Error creating database tables: {e}")

# Create FastAPI app
app = FastAPI(
    title=settings.PROJECT_NAME,
    version=settings.VERSION,
    description="AI Subscription Platform - Buy AI subscriptions and APIs at discounted prices",
    docs_url="/api/docs",
    redoc_url="/api/redoc",
    openapi_url="/api/openapi.json"
)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Mount static files
templates = Jinja2Templates(directory="templates")
app.mount("/static", StaticFiles(directory="static"), name="static")


# ==================== Health Check Endpoint ====================
@app.get("/api/health", response_model=HealthCheckResponse)
async def health_check():
    """Health check endpoint"""
    return {
        "status": "healthy",
        "version": settings.VERSION,
        "timestamp": datetime.now().isoformat(),
        "services": {
            "database": "healthy",
            "pricing_agent": "healthy",
            "procurement_agent": "healthy",
            "delivery_agent": "healthy"
        }
    }


# ==================== Exchange Rate Endpoints ====================
@app.get("/api/exchange-rate")
async def get_exchange_rate():
    """Get current USDT exchange rate"""
    try:
        rate = exchange_rate_fetcher.get_usdt_rate()
        return {
            "currency": "USDT",
            "rate": rate,
            "last_updated": datetime.now().isoformat()
        }
    except Exception as e:
        logger.error(f"Error getting exchange rate: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/api/exchange-rates")
async def get_all_exchange_rates():
    """Get all exchange rates"""
    try:
        rates = exchange_rate_fetcher.get_all_rates()
        return rates
    except Exception as e:
        logger.error(f"Error getting all exchange rates: {e}")
        raise HTTPException(status_code=500, detail=str(e))


# ==================== Product Endpoints ====================
@app.get("/api/products", response_model=List[ProductInDB])
async def get_all_products(db: Session = Depends(get_db)):
    """Get all active products"""
    try:
        products = db.query(Product).filter(Product.is_active == True).all()
        return products
    except Exception as e:
        logger.error(f"Error getting all products: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/api/products/{product_id}", response_model=ProductInDB)
async def get_product(product_id: int, db: Session = Depends(get_db)):
    """Get a specific product by ID"""
    try:
        product = db.query(Product).filter(Product.id == product_id).first()
        if not product:
            raise HTTPException(status_code=404, detail="Product not found")
        return product
    except Exception as e:
        logger.error(f"Error getting product {product_id}: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/api/products/prices")
async def get_all_prices():
    """Get calculated prices for all products"""
    try:
        prices = pricing_agent.calculate_all_prices()
        return {"prices": prices}
    except Exception as e:
        logger.error(f"Error calculating all prices: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/api/products/calculate-price", response_model=PriceCalculationResponse)
async def calculate_price(request: PriceCalculationRequest):
    """Calculate price for a specific product"""
    try:
        price_data = pricing_agent.calculate_final_price(request.product_name, request.supplier)
        return price_data
    except Exception as e:
        logger.error(f"Error calculating price for {request.product_name}: {e}")
        raise HTTPException(status_code=400, detail=str(e))


# ==================== Order Endpoints ====================
@app.post("/api/orders/", response_model=OrderInDB)
async def create_order(
    product_id: int,
    quantity: int = 1,
    payment_method: str = "crypto",
    db: Session = Depends(get_db)
):
    """Create a new order"""
    try:
        # Get product
        product = db.query(Product).filter(Product.id == product_id).first()
        if not product or not product.is_active:
            raise HTTPException(status_code=404, detail="Product not found or inactive")
        
        # Calculate price
        price_data = pricing_agent.calculate_final_price(product.name)
        
        # Get exchange rate
        exchange_rate = exchange_rate_fetcher.get_usdt_rate()
        
        # Calculate total price
        unit_price_tomans = price_data['final_price']
        total_price_tomans = unit_price_tomans * quantity
        
        # Generate order number
        order_number = f"ORD-{datetime.now().strftime('%Y%m%d%H%M%S')}-{os.urandom(4).hex()}"
        
        # Create order
        order = Order(
            order_number=order_number,
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
        
        # Generate payment address if crypto
        if payment_method == "crypto":
            payment_address = crypto_utils.generate_payment_address(order.id)
            payment_amount_crypto = crypto_utils.convert_to_crypto(
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
        raise HTTPException(status_code=400, detail=str(e))


@app.get("/api/orders/{order_id}", response_model=OrderInDB)
async def get_order(order_id: int, db: Session = Depends(get_db)):
    """Get order details"""
    try:
        order = db.query(Order).filter(Order.id == order_id).first()
        if not order:
            raise HTTPException(status_code=404, detail="Order not found")
        return order
    except Exception as e:
        logger.error(f"Error getting order {order_id}: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/api/orders/{order_id}/confirm-payment")
async def confirm_payment(
    order_id: int,
    tx_hash: str,
    db: Session = Depends(get_db)
):
    """Confirm crypto payment and process order"""
    try:
        order = db.query(Order).filter(Order.id == order_id).first()
        if not order:
            raise HTTPException(status_code=404, detail="Order not found")
        
        if order.status != "pending":
            raise HTTPException(status_code=400, detail="Order is not pending")
        
        # Verify payment (in production, verify with blockchain API)
        # For now, we'll assume payment is valid
        is_valid = crypto_utils.verify_crypto_payment(
            tx_hash,
            order.payment_amount_crypto,
            order.payment_crypto_currency
        )
        
        if not is_valid:
            raise HTTPException(status_code=400, detail="Invalid payment")
        
        # Update order status
        order.status = "paid"
        order.payment_tx_hash = tx_hash
        db.commit()
        
        # Process order with Procurement Agent
        procurement_success = procurement_agent.process_order(order_id)
        
        if procurement_success:
            # Deliver order with Delivery Agent
            delivery_agent.deliver_order(order_id)
            return {"status": "success", "message": "Order processed and delivered"}
        else:
            order.status = "procurement_failed"
            db.commit()
            raise HTTPException(status_code=500, detail="Failed to process order")
            
    except Exception as e:
        logger.error(f"Error confirming payment for order {order_id}: {e}")
        raise HTTPException(status_code=400, detail=str(e))


@app.get("/api/orders/{order_id}/status")
async def get_order_status(order_id: int, db: Session = Depends(get_db)):
    """Get order status"""
    try:
        order = db.query(Order).filter(Order.id == order_id).first()
        if not order:
            raise HTTPException(status_code=404, detail="Order not found")
        return {"status": order.status}
    except Exception as e:
        logger.error(f"Error getting order status {order_id}: {e}")
        raise HTTPException(status_code=500, detail=str(e))


# ==================== Shared Account Endpoints ====================
@app.post("/api/shared-accounts/")
async def create_shared_account(
    product_id: int,
    quantity: int = 1,
    db: Session = Depends(get_db)
):
    """Create new shared accounts"""
    try:
        shared_accounts = []
        for _ in range(quantity):
            account = procurement_agent.create_shared_account(product_id)
            if account:
                shared_accounts.append(account)
        
        return {"created": len(shared_accounts), "accounts": shared_accounts}
    except Exception as e:
        logger.error(f"Error creating shared accounts: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/api/shared-accounts/{account_id}")
async def get_shared_account(account_id: int, db: Session = Depends(get_db)):
    """Get shared account details"""
    try:
        account = db.query(SharedAccount).filter(SharedAccount.id == account_id).first()
        if not account:
            raise HTTPException(status_code=404, detail="Shared account not found")
        return account
    except Exception as e:
        logger.error(f"Error getting shared account {account_id}: {e}")
        raise HTTPException(status_code=500, detail=str(e))


# ==================== Admin Endpoints ====================
@app.post("/api/admin/products/")
async def create_product(
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
    shared_credits: Optional[int] = None,
    db: Session = Depends(get_db)
):
    """Create a new product (Admin only)"""
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
        raise HTTPException(status_code=400, detail=str(e))


@app.post("/api/admin/competitor-prices/")
async def add_competitor_price(
    product_id: int,
    competitor_site: str,
    price_tomans: int,
    competitor_url: Optional[str] = None,
    db: Session = Depends(get_db)
):
    """Add competitor price (Admin only)"""
    try:
        product = db.query(Product).filter(Product.id == product_id).first()
        if not product:
            raise HTTPException(status_code=404, detail="Product not found")
        
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
        raise HTTPException(status_code=400, detail=str(e))


# ==================== Frontend Routes ====================
@app.get("/")
async def read_root(request: Request):
    """Home page"""
    return templates.TemplateResponse("index.html", {"request": request})


@app.get("/products")
async def products_page(request: Request):
    """Products page"""
    try:
        prices = pricing_agent.calculate_all_prices()
        return templates.TemplateResponse("products.html", {
            "request": request,
            "prices": prices
        })
    except Exception as e:
        logger.error(f"Error loading products page: {e}")
        return templates.TemplateResponse("error.html", {
            "request": request,
            "error": str(e)
        }, status_code=500)


@app.get("/order/{order_id}")
async def order_detail_page(request: Request, order_id: int, db: Session = Depends(get_db)):
    """Order detail page"""
    try:
        order = db.query(Order).filter(Order.id == order_id).first()
        if not order:
            return templates.TemplateResponse("404.html", {"request": request}, status_code=404)
        
        return templates.TemplateResponse("order_detail.html", {
            "request": request,
            "order": order
        })
    except Exception as e:
        logger.error(f"Error loading order detail page: {e}")
        return templates.TemplateResponse("error.html", {
            "request": request,
            "error": str(e)
        }, status_code=500)


@app.get("/payment/{order_id}")
async def payment_page(request: Request, order_id: int, db: Session = Depends(get_db)):
    """Payment page"""
    try:
        order = db.query(Order).filter(Order.id == order_id).first()
        if not order:
            return templates.TemplateResponse("404.html", {"request": request}, status_code=404)
        
        return templates.TemplateResponse("payment.html", {
            "request": request,
            "order": order
        })
    except Exception as e:
        logger.error(f"Error loading payment page: {e}")
        return templates.TemplateResponse("error.html", {
            "request": request,
            "error": str(e)
        }, status_code=500)


# ==================== Error Handlers ====================
@app.exception_handler(404)
async def not_found_handler(request: Request, exc: HTTPException):
    return templates.TemplateResponse("404.html", {"request": request}, status_code=404)


@app.exception_handler(500)
async def server_error_handler(request: Request, exc: HTTPException):
    return templates.TemplateResponse("500.html", {"request": request}, status_code=500)


# ==================== Run Server ====================
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "app.main:app",
        host="0.0.0.0",
        port=8000,
        reload=True
    )
