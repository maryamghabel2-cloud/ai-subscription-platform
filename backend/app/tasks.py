"""
Celery Tasks for AI Subscription Platform
- Background tasks for procurement, monitoring, etc.
"""

from celery import Celery
from app.config import settings
from app.agents.procurement_agent import procurement_agent
from app.agents.monitoring_agent import monitoring_agent
from app.services.product_service import product_service
import logging

logger = logging.getLogger(__name__)

# Initialize Celery
celery_app = Celery(
    "ai_subscription_tasks",
    broker=settings.REDIS_URL,
    backend=settings.REDIS_URL
)


@celery_app.task(bind=True, max_retries=3)
def process_order_task(self, order_id: int):
    """
    Celery task to process an order in the background
    """
    try:
        success = procurement_agent.process_order(order_id)
        if not success:
            # Retry after 5 minutes
            self.retry(countdown=300)
        return success
    except Exception as e:
        logger.error(f"Error in process_order_task for order {order_id}: {e}")
        return False


@celery_app.task
ndef update_product_prices_task():
    """
    Celery task to update product prices from suppliers
    """
    try:
        count = product_service.update_product_prices_from_suppliers()
        logger.info(f"Updated prices for {count} products")
        return count
    except Exception as e:
        logger.error(f"Error in update_product_prices_task: {e}")
        return 0


@celery_app.task
ndef health_check_task():
    """
    Celery task to run system health check
    """
    try:
        monitoring_agent.run_health_check()
        return True
    except Exception as e:
        logger.error(f"Error in health_check_task: {e}")
        return False


@celery_app.task
ndef inventory_check_task():
    """
    Celery task to check product inventory
    """
    try:
        inventory_status = monitoring_agent.check_product_inventory()
        logger.info(f"Inventory check: {inventory_status}")
        return inventory_status
    except Exception as e:
        logger.error(f"Error in inventory_check_task: {e}")
        return None


# Schedule periodic tasks
celery_app.conf.beat_schedule = {
    "update-product-prices": {
        "task": "ai_subscription_tasks.update_product_prices_task",
        "schedule": 3600.0,  # 1 hour
    },
    "health-check": {
        "task": "ai_subscription_tasks.health_check_task",
        "schedule": 300.0,  # 5 minutes
    },
    "inventory-check": {
        "task": "ai_subscription_tasks.inventory_check_task",
        "schedule": 1800.0,  # 30 minutes
    },
}
