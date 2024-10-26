import datetime
import logging
from typing import List

from sqlalchemy.orm import Session

from app.celery_tasks.tasks import scrape_page
from app.config import settings
from app.db.sql import get_db
from app.models.scrap_request import ScrapRequest
from app.schemas.scrap_request import ScrapRequestStatus


class ScrappingSchedular:

    @staticmethod
    def get_unprocessed_requests() -> List[int]:
        db: Session = get_db()
        results = db.query(ScrapRequest).filter(ScrapRequest.status == ScrapRequestStatus.REQUEST_CREATED.value).all()
        return results

    @staticmethod
    def can_schedule(request: ScrapRequest):
        if request.status == ScrapRequestStatus.REQUEST_CREATED.value:
            return True

        if request == ScrapRequestStatus.FAILED.value and request.data_dump_info:
            data_dump_info = request.data_dump_info
            failed_at = datetime.datetime.fromisoformat(data_dump_info.get('last_tried'))
            retry_count = data_dump_info.get('retry_count')
            time_difference_wrt_retry = (datetime.datetime.now() - failed_at).total_seconds()
            return data_dump_info.get('retry') and retry_count < settings.MAX_RETRY_COUNT \
                and time_difference_wrt_retry >= settings.RETRY_DELAY
        return False

    def run(self):
        print(f"Scheduling Request")
        unprocessed_request = self.get_unprocessed_requests()
        scheduled_request = 0
        for request in unprocessed_request:
            request: ScrapRequest = request
            if self.can_schedule(request=request):
                scheduled_request += 1
                scrape_page.delay(request_id=request.id)
        return scheduled_request


