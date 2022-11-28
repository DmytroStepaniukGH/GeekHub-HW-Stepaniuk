"""
3. http://quotes.toscrape.com/ - написати скрейпер для збору всієї доступної
   інформації про записи: цитата, автор, інфа про автора тощо.
   - збирається інформація з 10 сторінок сайту.
   - зберігати зібрані дані у CSV файл
"""

import csv
from dataclasses import dataclass, fields, astuple
import requests
from bs4 import BeautifulSoup


@dataclass
class Product:
    text: str
    author: str
    author_born: str
    author_description: str
    tags: str


class QuotesParser:
    URL = 'http://quotes.toscrape.com/'
    QUOTES_FIELDS = [field.name for field in fields(Product)]
    QUOTES_OUTPUT_CSV_PATH = 'quotes.csv'

    def get_site_quotes(self):
        page = requests.get(self.URL + 'page/1').content
        first_page_soup = BeautifulSoup(page, 'lxml')
        print(f'Get data from page 1')
        all_products = self.get_single_page_products(first_page_soup)

        number_of_pages = 10
        for page_number in range(2, number_of_pages + 1):
            print(f'Get data from page {page_number}')
            page = requests.get(self.URL + f'page/{page_number}').content
            soup = BeautifulSoup(page, 'lxml')
            all_products.extend(self.get_single_page_products(soup))

        return all_products

    def get_author_data(self, link):
        page = requests.get(self.URL + link).content
        soup = BeautifulSoup(page, 'lxml')
        born = soup.select_one('.author-born-date').text + ' ' \
            + soup.select_one('.author-born-location').text
        author_description = soup.select_one('.author-description').text

        return born, author_description

    def parse_single_quote(self, product_soup: BeautifulSoup):
        link = product_soup.select_one('a', href=True)['href']
        author_details = self.get_author_data(link)
        return Product(
            text=product_soup.select_one('.text').text,
            author=product_soup.select_one('.author').text,
            author_born=author_details[0],
            author_description=author_details[1],
            tags=product_soup.select_one('.keywords')['content']
        )

    def get_single_page_products(self, page_soup):
        products = page_soup.select('.quote')

        return [self.parse_single_quote(product_soup)
                for product_soup in products]

    def write_products_to_csv(self, products: [Product]):
        with open(self.QUOTES_OUTPUT_CSV_PATH, 'w',
                  encoding="utf-8") as file:
            writer = csv.writer(file)
            writer.writerow(self.QUOTES_FIELDS)
            writer.writerows([astuple(product) for product in products])
        return


if __name__ == '__main__':
    parser = QuotesParser()
    quotes = parser.get_site_quotes()
    parser.write_products_to_csv(quotes)
