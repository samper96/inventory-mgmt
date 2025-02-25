"""
Celery tasks used for product low stock alerts.
"""

from celery import Celery
from src.database import SessionLocal
from db_models import Product
import logging
from celery.schedules import crontab

logger = logging.getLogger(__name__)

# Create Celery app
celery = Celery(__name__, broker="redis://redis:6379/0", backend="redis://redis:6379/0")

# Configure scheduling recurring tasks (Celery Beat)
# Automatically run check_for_low_stock every 5 minutes
celery.conf.beat_schedule = {
    "check-every-5-minutes": {
        "task": "src.tasks.check_for_low_stock",
        "schedule": crontab(minute="*/5"),
        "args": (10,),  # threshold
    },
}


@celery.task
def check_for_low_stock(threshold=10):
    """
    Celery task to log products with stock < `threshold`.
    """
    db = SessionLocal()
    try:
        low_stock_products = db.query(Product).filter(Product.stock < threshold).all()
        if not low_stock_products:
            logger.info("No products below stock threshold.")
        else:
            for prod in low_stock_products:
                logger.warning("LOW STOCK ALERT! Product %s (ID=%d) -> stock=%d" % prod.name, prod.id, prod.stock)
    finally:
        db.close()
