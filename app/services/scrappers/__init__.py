from typing import Type

from app.models import ScrapRequest
from app.services.scrappers.dental_product import DentalProductScrapper
from app.services.scrappers.base import PageScrapper


def get_scrapper(request: ScrapRequest) -> Type[PageScrapper]:
    # add logic based on request url
    return DentalProductScrapper
