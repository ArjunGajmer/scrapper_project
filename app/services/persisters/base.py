import abc
from typing import Optional, List, Dict

from pydantic import BaseModel

from app.services.scrappers.base import PageScrappingData


class ScrappedDataStats(BaseModel):
    new_entry: Optional[int] = 0
    updated: Optional[int] = 0

    def __add__(self, other):
        self.new_entry += other.new_entry
        self.updated += other.updated
        return self


class DataPersister(abc.ABC):

    def __init__(self, scrapping_info: PageScrappingData, **kwargs):
        self.scrapping_info: PageScrappingData = scrapping_info

    @abc.abstractmethod
    def persist(self, data: List[Dict[str, str]]) -> ScrappedDataStats:
        pass


