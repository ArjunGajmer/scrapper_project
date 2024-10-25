import datetime
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
        results = db.query(ScrapRequest).filter(
            ScrapRequest.status == ScrapRequestStatus.REQUEST_CREATED).all()
        return [obj[0] for obj in results]

    @staticmethod
    def can_schedule(request: ScrapRequest):
        if request.status == ScrapRequestStatus.REQUEST_CREATED:
            return True

        if request == ScrapRequestStatus.FAILED and request.data_dump_info:
            data_dump_info = request.data_dump_info
            failed_at = datetime.datetime.fromisoformat(data_dump_info.get('last_tried'))
            retry_count = data_dump_info.get('retry_count')
            time_difference_wrt_retry = (datetime.datetime.now() - failed_at).total_seconds()
            return data_dump_info.get('retry') and retry_count < settings.MAX_RETRY_COUNT \
                and time_difference_wrt_retry >= settings.RETRY_DELAY

        return False

    def run(self):
        unprocessed_request = self.get_unprocessed_requests()
        for request in unprocessed_request:
            request: ScrapRequest = request
            if self.can_schedule(request=request):
                scrape_page.delay(request_id=request.id)
