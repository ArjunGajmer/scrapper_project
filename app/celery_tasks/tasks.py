import datetime
import logging
from celery import shared_task

from app.services.scrapping_app import ScrappingApp

logger = logging.getLogger("celery")


@shared_task
def scrape_page(request_id: int):
    logger.info(f"Celery task for scraping {request_id}  Started: {datetime.datetime.now()}")
    ScrappingApp().process(request_id=request_id)
    logger.info(f"Celery task for scraping {request_id}  Completed: {datetime.datetime.now()}")
