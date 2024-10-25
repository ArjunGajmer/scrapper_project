import abc
import enum
from typing import List, Dict, Any, Optional

import requests
from pydantic import BaseModel

from app.schemas.scrap_request import ScrapRequestConfig
from app.services.media_handler.base import MediaDataManager


class PageReadException(Exception):
    pass


class PageScrappingData(BaseModel):
    url: str
    config: ScrapRequestConfig


class PageScrapper(abc.ABC):

    def __init__(self, scrapping_info: PageScrappingData, media_data_manager: MediaDataManager):
        self.media_data_manager: media_data_manager = media_data_manager
        self.scrapping_info: PageScrappingData = scrapping_info

    def __fetch(self, page_number):
        url = f"{self.scrapping_info.url}/page/{page_number}/" if page_number > 1 else self.scrapping_info.url
        try:
            response = requests.get(url)
            response.raise_for_status()
            return response.text
        except Exception as e:
            raise PageReadException("Page Can't be read")

    @abc.abstractmethod
    def parser(self, response: str) -> List[Dict[str, str]]:
        pass

    def scrap(self):
        config = self.scrapping_info.config
        page_numbers = config.page_number
        for page_number in range(1, page_numbers + 1):
            data = self.__fetch(page_number)
            yield self.parser(data)
