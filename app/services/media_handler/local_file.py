import os

import requests

from app.config import settings
from app.services.media_handler.base import MediaDataManager
from app.services.scrappers.base import PageScrappingData
from app.utils.format_strings import generate_unique_hash


class LocalStorageBasedMediaManager(MediaDataManager):
    PATH = settings.PATH_TO_MEDIA_STORE

    def __init__(self, scrapping_info: PageScrappingData):
        self.scrapping_info: PageScrappingData = scrapping_info
        self._fetch_key = generate_unique_hash(self.scrapping_info.url)

    def get_load_add_save(self, url: str, file_save_path: str):
        return self._download_media(url=url, save_path=self.__setup(file_save_path=file_save_path))

    def _download_media(self, url: str, save_path: str):
        try:
            response = requests.get(url, stream=True)
            response.raise_for_status()
            with open(save_path, 'wb') as file:
                for chunk in response.iter_content(1024):
                    file.write(chunk)
            return save_path
        except requests.exceptions.RequestException as e:
            pass

    def __setup(self, file_save_path: str):
        os.makedirs(self.PATH, exist_ok=True)
        os.makedirs(os.path.join(self.PATH, self._fetch_key), exist_ok=True)
        return os.path.join(f"{self.PATH}/{self._fetch_key}", file_save_path)
