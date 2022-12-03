"""
1. Викорисовуючи requests/BeautifulSoup, заходите на ось цей сайт
   "https://www.expireddomains.net/domain-lists/" (з ним будьте обережні),
    вибираєте будь-яку на ваш вибір доменну зону і парсите список  доменів
    з усіма відповідними колонками - доменів там буде десятки тисяч
    (звичайно ураховуючи пагінацію). Всі отримані значення зберегти в
    CSV файл.
"""
import csv
from dataclasses import dataclass, fields
import requests
import time
import random
from bs4 import BeautifulSoup


@dataclass
class Product:
    Domain: str
    BL: str
    DP: str
    ABY: str
    ACR: str
    Dmoz: str
    C: str
    N: str
    O: str
    D: str
    Reg: str
    RDT: str
    Traffic: str
    Valuation: str
    Price: str
    Bids: str
    Endtime: str


class DomainsParser:
    URL = 'https://www.expireddomains.net/godaddy-expired-domains/?start='
    DOMAIN_FIELDS = [field.name for field in fields(Product)]
    DOMAIN_OUTPUT_CSV_PATH = 'domains.csv'
    session = requests.Session()
    headers = {'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:94.0)'
                             ' Gecko/20100101 Firefox/94.0'}

    def get_domains(self):
        data = []
        for domains_per_number in range(0, 325, 25):
            print(f'Get data from page {int(domains_per_number / 25)}')
            page = self.session.get(self.URL + f'{domains_per_number}#listing',
                                    headers=self.headers).content
            soup = BeautifulSoup(page, 'lxml')
            table = soup.find('table', {"class": "base1"})
            table_body = table.find('tbody')

            rows = table_body.find_all('tr')
            for row in rows:
                cols = row.find_all('td')
                cols = [item.text for item in cols]
                data.append([item for item in cols])
            time_sleep = random.randint(10, 20)
            print(f'Sleep {time_sleep} sec')
            time.sleep(time_sleep)

        return data

    def write_domains_to_csv(self, domains):
        with open(self.DOMAIN_OUTPUT_CSV_PATH, 'w',
                  encoding="utf-8", newline='') as file:
            writer = csv.writer(file)
            writer.writerow(self.DOMAIN_FIELDS)
            writer.writerows([product for product in domains])


if __name__ == '__main__':
    parser = DomainsParser()
    domains = parser.get_domains()
    parser.write_domains_to_csv(domains)
