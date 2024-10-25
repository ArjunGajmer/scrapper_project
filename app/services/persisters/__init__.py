from app.services.persisters.base import DataPersister
from app.services.persisters.file import FilePersister
from app.services.scrappers.base import PageScrappingData


def get_data_persister(scrapping_info: PageScrappingData) -> DataPersister:
    # based on the request url we can reroute it

    return FilePersister(scrapping_info, search_key='product_title', match_keys=['product_price', 'currency'])
