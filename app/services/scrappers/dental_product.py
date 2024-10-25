import re
from typing import List, Dict
from urllib.parse import urlparse

from bs4 import BeautifulSoup

from app.services.scrappers.base import PageScrapper


class DentalProductScrapper(PageScrapper):
    def _clean_price(self, price_str: str) -> str:
        if not price_str:
            return ""
        price_match = re.search(r'[\d,]+', price_str)
        if price_match:
            return str(int(price_match.group().replace(',', '')))
        return ""

    def _get_currency(self, price_str: str) -> str:
        if not price_str:
            return ""
        currency_map = {
            '₹': 'INR',
            '$': 'USD',
            '€': 'EUR',
            '£': 'GBP'
        }
        currency_match = re.search(r'[₹$€£]', price_str)
        return currency_map.get(currency_match.group(), '') if currency_match else ""

    def _extract_price_info(self, price_tag) -> tuple:
        regular_price = ''
        currency = ''

        if price_tag:
            regular_price_tag = price_tag.find('del')
            if regular_price_tag:
                regular_price_str = regular_price_tag.find('span', class_='amount').text.strip()
                regular_price = self._clean_price(regular_price_str)
                currency = currency or self._get_currency(regular_price_str)
            elif price_tag.find('span', class_='amount'):
                regular_price_str = price_tag.find('span', class_='amount').text.strip()
                regular_price = self._clean_price(regular_price_str)
                currency = currency or self._get_currency(regular_price_str)

        return regular_price, currency

    def parser(self, response: str) -> List[Dict[str, str]]:
        soup = BeautifulSoup(markup=response, features="html.parser")
        products = soup.find_all('li', class_='product')
        parsed_products = []

        for product in products:
            try:
                img_tag = product.find('img', class_='attachment-woocommerce_thumbnail')
                image_url = img_tag.get('data-lazy-src') or img_tag.get('src') if img_tag else ''

                title_tag = product.find('h2', class_='woo-loop-product__title')
                product_title = title_tag.find('a').text.strip().strip(".") if title_tag else ''

                price_tag = product.find('span', class_='price')
                price, currency = self._extract_price_info(price_tag)
                file_path_to_save = urlparse(image_url).path.split('/')[-1]
                image_url = self.media_data_manager.get_load_add_save(image_url, file_path_to_save)
                product_data = {
                    'product_title': product_title,
                    'image_url': image_url,
                    'product_price': price,
                    'currency': currency
                }
                parsed_products.append(product_data)

            except Exception as e:
                continue

        return parsed_products
