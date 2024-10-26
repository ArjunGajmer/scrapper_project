import contextlib
import datetime
import logging
from typing import Type, Union

from app.db.sql import get_db, write_and_commit
from app.models import ScrapRequest, User
from app.schemas.scrap_request import ScrapRequestStatus
from app.services.media_handler.base import MediaDataManager
from app.services.media_handler.local_file import LocalStorageBasedMediaManager
from app.services.notification_system import Notifier, get_notifier
from app.services.persisters import DataPersister, get_data_persister
from app.services.persisters.base import ScrappedDataStats
from app.services.scrappers import PageScrapper, get_scrapper
from app.services.scrappers.base import PageReadException, PageScrappingData


class ScrappingApp:

    def __init__(self):
        self._db = get_db()
        self._media_data_manager: Type[MediaDataManager] = LocalStorageBasedMediaManager
        self._persister: Union[DataPersister, None] = None  # generated on based on request
        self._scrapper: Union[PageScrapper, None] = None  # generate based on request
        self._notifier: Union[Type[Notifier], None] = None  # generated based on request user perference

    @staticmethod
    def can_process(request: ScrapRequest):
        if not request:
            logging.exception("No request found")
            return False
        if request.status not in [ScrapRequestStatus.REQUEST_CREATED.value, ScrapRequestStatus.FAILED.value]:
            logging.exception(f"Can't Process the scrapping Request as status is : {request.status}")
        return request.status in [ScrapRequestStatus.REQUEST_CREATED.value, ScrapRequestStatus.FAILED.value]

    def process(self, request_id):
        request: ScrapRequest = self._db.query(ScrapRequest).filter(ScrapRequest.id == request_id).first()
        if self.can_process(request=request):  # TODO remove
            try:
                self.__update_process_status(request=request, status=ScrapRequestStatus.IN_PROGRESS, stats=None)
                stats: ScrappedDataStats = self.scrap_and_persist(request=request)
                self.__update_process_status(request=request, status=ScrapRequestStatus.COMPLETED, stats=stats)
                return self.notify(request=request, stats=stats)
            except PageReadException as e:
                self.__update_process_status(request=request, status=ScrapRequestStatus.FAILED, stats=None,
                                             retry=True)
            except Exception as e:
                self.__update_process_status(request=request, status=ScrapRequestStatus.FAILED, stats=None)
                raise e

    def scrap_and_persist(self, request: ScrapRequest):
        page_scrapping_info = PageScrappingData(url=request.page_url, config=request.config)
        stats = ScrappedDataStats()
        media_manager = self._media_data_manager(scrapping_info=page_scrapping_info)
        self._scrapper: PageScrapper = get_scrapper(request)(scrapping_info=page_scrapping_info,
                                                             media_data_manager=media_manager)
        self._persister: DataPersister = get_data_persister(page_scrapping_info)
        for data in self._scrapper.scrap():
            stats += self._persister.persist(data=data)
        return stats

    def notify(self, request: ScrapRequest, stats: ScrappedDataStats):
        with contextlib.suppress(Exception):
            user: User = self._db.query(User).filter(User.id == request.user).first()
            self._notifier: Type[Notifier] = get_notifier(user=user)
            header = f"Data Scarping completed"
            body = f"Your request for scrapping data for : {request.page_url} is completed." \
                   f"\n\t\tTotal New entry: {stats.new_entry}" \
                   f"\n\t\tTotal Updated Entry: {stats.updated}"
            return self._notifier(user=user, header=header, body=body).notify()

    def __update_process_status(self, request: ScrapRequest, status: ScrapRequestStatus,
                                stats: Union[ScrappedDataStats, None],
                                retry: bool = False):
        request.status = status.value

        if status == ScrapRequestStatus.COMPLETED.value:
            data = {'stats': stats.dict()}
            request.data_dump_info = data

        elif status == ScrapRequestStatus.FAILED.value:
            existing_data = request.data_dump_info or {}
            data = {'retry_count': existing_data.get('retry_count', 0) + 1, 'retry': retry,
                    'last_tried': datetime.datetime.now().isoformat()}
            request.data_dump_info = data

        write_and_commit(model_instance=request, db=self._db)
