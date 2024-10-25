import json
from typing import List, Dict

from app.config import settings
from app.db.local_file_storage import FileStoreManager
from app.services.persisters.base import DataPersister, ScrappedDataStats
from app.services.scrappers.base import PageScrappingData
from app.utils.caching import cache_data, get_cached_data, destroy_cached_data
from app.utils.format_strings import generate_unique_hash


class FilePersister(DataPersister):
    PATH = settings.SCRAPED_DATA_STORE

    def __init__(self, scrapping_info: PageScrappingData, search_key: str, match_keys: list):
        super().__init__(scrapping_info=scrapping_info)
        self._fetch_key = generate_unique_hash(self.scrapping_info.url)
        self.file_manager = FileStoreManager(fetch_key=self._fetch_key, base_path=self.PATH)
        self._match_keys: list = match_keys
        self._search_key: str = search_key
        self.__fetch_save_to_redis()

    def __del__(self):
        destroy_cached_data(f'scraped_data:{self._fetch_key}-*')

    def save(self, data: List[Dict[str, str]]):
        self.file_manager.update_and_append_data(new_data=data, search_key=self._search_key)

    def persist(self, data: List[Dict[str, str]]):
        update_data, create_data = self.__seg_update_and_create_data(data)
        self.save(data=update_data + create_data)
        return ScrappedDataStats(new_entry=len(create_data), updated=len(update_data))

    def __product_cache_key(self, identifier):
        return f'scraped_data:{self._fetch_key}-{identifier}'

    def __fetch_save_to_redis(self):
        raw_data = self.file_manager.read_data()
        for item in raw_data:
            cache_key = self.__product_cache_key(item[self._search_key])
            data = {match_key: item[match_key] for match_key in self._match_keys}
            cache_data(cache_key, json.dumps(data))

    def __seg_update_and_create_data(self, data_list: List[Dict[str, str]]):
        update_data = []
        create_data = []
        for data in data_list:
            identifier = data[self._search_key]
            cache_key = self.__product_cache_key(identifier)
            price = data['product_price']
            currency = data['currency']
            if cached_data := get_cached_data(cache_key):
                cached_data = json.loads(cached_data)
                if price == cached_data.get('product_price') and currency == cached_data.get('currency'):
                    continue
                update_data.append(data)
            else:
                create_data.append(data)
        return update_data, create_data
