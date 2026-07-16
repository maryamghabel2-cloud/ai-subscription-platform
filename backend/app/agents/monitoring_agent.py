"""
Monitoring Agent for AI Subscription Platform
- Monitors system health
- Tracks errors and warnings
- Sends alerts for critical issues
"""

import logging
from datetime import datetime, timedelta
from typing import Dict, Any, List, Optional
from app.database import get_db
from app.models.models import Order, ProcurementLog, ExchangeRate
from app.config import settings
from app.utils.exchange_rate import exchange_rate_fetcher

logger = logging.getLogger(__name__)


class MonitoringAgent:
    """
    AI Agent for monitoring system health and performance
    """
    
    def __init__(self):
        self.alert_thresholds = {
            "failed_orders": 5,  # بیش از ۵ سفارش ناموفق در ۱ ساعت
            "procurement_failures": 3,  # بیش از ۳ خرید ناموفق در ۱ ساعت
            "exchange_rate_age": 300,  # نرخ تتر قدیمی‌تر از ۵ دقیقه
            "low_inventory": 2  # کمتر از ۲ اکانت اشتراکی برای محصولات پرفروش
        }
        self.last_alert_time = {}
        self.alert_cooldown = 3600  # ۱ ساعت
    
    def check_system_health(self) -> Dict[str, Any]:
        """
        Check overall system health
        :return: Dictionary with health status
        """
        db = next(get_db())
        
        health_status = {
            "timestamp": datetime.now().isoformat(),
            "status": "healthy",
            "checks": {},
            "alerts": []
        }
        
        # Check database connection
        try:
            db.execute("SELECT 1")
            health_status["checks"]["database"] = {"status": "healthy"}
        except Exception as e:
            health_status["checks"]["database"] = {"status": "unhealthy", "error": str(e)}
            health_status["status"] = "degraded"
            health_status["alerts"].append({
                "type": "database_error",
                "message": f"Database connection failed: {e}",
                "severity": "critical"
            })
        
        # Check exchange rate freshness
        try:
            latest_rate = db.query(ExchangeRate).filter(
                ExchangeRate.currency == "USDT"
            ).order_by(ExchangeRate.last_updated.desc()).first()
            
            if latest_rate:
                age = (datetime.now() - latest_rate.last_updated).total_seconds()
                if age > self.alert_thresholds["exchange_rate_age"]:
                    health_status["checks"]["exchange_rate"] = {
                        "status": "degraded",
                        "age_seconds": age
                    }
                    health_status["status"] = "degraded"
                    health_status["alerts"].append({
                        "type": "old_exchange_rate",
                        "message": f"Exchange rate is {age} seconds old",
                        "severity": "warning"
                    })
                else:
                    health_status["checks"]["exchange_rate"] = {
                        "status": "healthy",
                        "age_seconds": age
                    }
            else:
                health_status["checks"]["exchange_rate"] = {"status": "unhealthy"}
                health_status["status"] = "degraded"
                health_status["alerts"].append({
                    "type": "no_exchange_rate",
                    "message": "No exchange rate data found",
                    "severity": "critical"
                })
        except Exception as e:
            health_status["checks"]["exchange_rate"] = {"status": "unhealthy", "error": str(e)}
            health_status["status"] = "degraded"
        
        # Check recent failed orders
        try:
            one_hour_ago = datetime.now() - timedelta(hours=1)
            failed_orders = db.query(Order).filter(
                Order.status == "failed",
                Order.created_at >= one_hour_ago
            ).count()
            
            health_status["checks"]["failed_orders"] = {
                "status": "healthy" if failed_orders <= self.alert_thresholds["failed_orders"] else "degraded",
                "count": failed_orders
            }
            
            if failed_orders > self.alert_thresholds["failed_orders"]:
                health_status["status"] = "degraded"
                health_status["alerts"].append({
                    "type": "high_failed_orders",
                    "message": f"{failed_orders} failed orders in the last hour",
                    "severity": "warning"
                })
        except Exception as e:
            logger.error(f"Error checking failed orders: {e}")
        
        # Check procurement failures
        try:
            one_hour_ago = datetime.now() - timedelta(hours=1)
            procurement_failures = db.query(ProcurementLog).filter(
                ProcurementLog.status == "failed",
                ProcurementLog.created_at >= one_hour_ago
            ).count()
            
            health_status["checks"]["procurement_failures"] = {
                "status": "healthy" if procurement_failures <= self.alert_thresholds["procurement_failures"] else "degraded",
                "count": procurement_failures
            }
            
            if procurement_failures > self.alert_thresholds["procurement_failures"]:
                health_status["status"] = "degraded"
                health_status["alerts"].append({
                    "type": "high_procurement_failures",
                    "message": f"{procurement_failures} procurement failures in the last hour",
                    "severity": "critical"
                })
        except Exception as e:
            logger.error(f"Error checking procurement failures: {e}")
        
        return health_status
    
    def check_product_inventory(self) -> Dict[str, Any]:
        """
        Check inventory levels for shared accounts
        :return: Dictionary with inventory status
        """
        db = next(get_db())
        
        inventory_status = {
            "timestamp": datetime.now().isoformat(),
            "status": "healthy",
            "products": {},
            "alerts": []
        }
        
        try:
            # Get all products that are shared
            products = db.query(Product).filter(
                Product.is_active == True,
                Product.is_shared == True
            ).all()
            
            for product in products:
                # Count available shared accounts
                available = db.query(SharedAccount).filter(
                    SharedAccount.product_id == product.id,
                    SharedAccount.is_active == True,
                    SharedAccount.current_users < SharedAccount.max_users
                ).count()
                
                inventory_status["products"][product.name] = {
                    "available": available,
                    "status": "healthy" if available >= self.alert_thresholds["low_inventory"] else "low"
                }
                
                if available < self.alert_thresholds["low_inventory"]:
                    inventory_status["status"] = "degraded"
                    inventory_status["alerts"].append({
                        "type": "low_inventory",
                        "message": f"Low inventory for {product.name}: only {available} available",
                        "severity": "warning",
                        "product": product.name
                    })
        except Exception as e:
            logger.error(f"Error checking product inventory: {e}")
            inventory_status["status"] = "unhealthy"
            inventory_status["alerts"].append({
                "type": "inventory_check_error",
                "message": str(e),
                "severity": "critical"
            })
        
        return inventory_status
    
    def send_alert(self, alert_type: str, message: str, severity: str = "warning") -> bool:
        """
        Send alert notification (log or email)
        :return: True if alert was sent
        """
        try:
            # Check if we should send this alert (cooldown)
            last_time = self.last_alert_time.get(alert_type, 0)
            if datetime.now().timestamp() - last_time < self.alert_cooldown:
                return False
            
            self.last_alert_time[alert_type] = datetime.now().timestamp()
            
            # Log alert
            log_method = logger.error if severity == "critical" else logger.warning
            log_method(f"ALERT [{severity.upper()}]: {alert_type} - {message}")
            
            # In production, you could also send email/SMS here
            # For now, we'll just log it
            
            return True
        except Exception as e:
            logger.error(f"Error sending alert: {e}")
            return False
    
    def run_health_check(self) -> None:
        """
        Run complete health check and send alerts if needed
        """
        try:
            # Check system health
            health_status = self.check_system_health()
            
            if health_status["status"] != "healthy":
                for alert in health_status.get("alerts", []):
                    self.send_alert(
                        alert["type"],
                        alert["message"],
                        alert["severity"]
                    )
            
            # Check inventory
            inventory_status = self.check_product_inventory()
            
            if inventory_status["status"] != "healthy":
                for alert in inventory_status.get("alerts", []):
                    self.send_alert(
                        alert["type"],
                        alert["message"],
                        alert["severity"]
                    )
        except Exception as e:
            logger.error(f"Error running health check: {e}")


monitoring_agent = MonitoringAgent()
